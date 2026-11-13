"""Statistics and figures for a finished run.

Reads runs/<run_name>/scored.csv (run summarize first) and writes to results/<run_name>/:
  stats.md                     all tables below, readable
  ci_table.csv                 means with 95% bootstrap CIs per condition x mitigation
  paired_tests.csv             mitigation and condition comparisons (McNemar / Wilcoxon, Holm-adjusted)
  c4_outcomes.csv              what the model answered when the gold passage was contradicted
  faithful_vs_correct.csv      2x2 of judge faithfulness (>= 0.5) against correctness
  position.csv                 correctness and faithfulness by where the gold passage sat
  memory.csv                   results split by whether the model knew the answer closed-book
  figures/*.pdf, figures/*.png
"""

from __future__ import annotations

import itertools

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from src.common import config_arg_parser, load_config, results_dir, run_dir

CONDITIONS = ["C0", "C1", "C2", "C3", "C4", "C5"]
MITIGATIONS = ["M0", "M1", "M2"]
MIT_LABELS = {"M0": "M0 baseline", "M1": "M1 strict + refusal", "M2": "M2 context-faithful"}
COLORS = {"M0": "#4C72B0", "M1": "#DD8452", "M2": "#55A868"}
FAITHFUL_THRESHOLD = 0.5
EQUIV_MARGIN = 0.10
N_BOOT = 2000
SEED = 42


def load(cfg: dict) -> pd.DataFrame:
    df = pd.read_csv(run_dir(cfg) / "scored.csv")
    for col in ["correct", "correct_strict", "followed_fake"]:
        df[col] = df[col].map({True: 1.0, False: 0.0, "True": 1.0, "False": 0.0})
    df["refused"] = df["refused"].astype(float)
    # Faithfulness and answer relevancy are only defined for answers that are not refusals.
    for col in ["faithfulness", "answer_relevancy"]:
        df.loc[df["refused"] == 1, col] = np.nan
    return df


def bootstrap_ci(values: pd.Series, rng: np.random.Generator) -> tuple[float, float, float, int]:
    x = values.dropna().to_numpy(dtype=float)
    if len(x) == 0:
        return np.nan, np.nan, np.nan, 0
    means = rng.choice(x, size=(N_BOOT, len(x)), replace=True).mean(axis=1)
    return x.mean(), *np.percentile(means, [2.5, 97.5]), len(x)


def ci_table(df: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    metrics = ["correct", "refused", "faithfulness", "answer_relevancy", "context_precision", "followed_fake"]
    rows = []
    for (cond, mit), g in df[df["condition"] != "closed_book"].groupby(["condition", "mitigation"]):
        for m in metrics:
            mean, lo, hi, n = bootstrap_ci(g[m], rng)
            if n:
                rows.append({"condition": cond, "mitigation": mit, "metric": m, "mean": mean, "lo": lo, "hi": hi, "n": n})
    cb = df[df["condition"] == "closed_book"]
    mean, lo, hi, n = bootstrap_ci(cb["correct"], rng)
    rows.append({"condition": "closed_book", "mitigation": "-", "metric": "correct", "mean": mean, "lo": lo, "hi": hi, "n": n})
    return pd.DataFrame(rows)


def mcnemar(a: pd.Series, b: pd.Series) -> dict:
    """Exact McNemar test on paired binary outcomes (binomial test on the discordant pairs)."""
    pair = pd.concat([a, b], axis=1).dropna()
    only_a = int(((pair.iloc[:, 0] == 1) & (pair.iloc[:, 1] == 0)).sum())
    only_b = int(((pair.iloc[:, 0] == 0) & (pair.iloc[:, 1] == 1)).sum())
    p = stats.binomtest(only_a, only_a + only_b, 0.5).pvalue if only_a + only_b else 1.0
    return {
        "test": "McNemar (exact)",
        "n_pairs": len(pair),
        "mean_a": pair.iloc[:, 0].mean(),
        "mean_b": pair.iloc[:, 1].mean(),
        "effect": pair.iloc[:, 1].mean() - pair.iloc[:, 0].mean(),
        "effect_name": "difference (b - a)",
        "detail": f"discordant: only a={only_a}, only b={only_b}",
        "p": p,
    }


def wilcoxon(a: pd.Series, b: pd.Series) -> dict:
    """Wilcoxon signed-rank test with matched-pairs rank-biserial correlation as effect size."""
    pair = pd.concat([a, b], axis=1).dropna()
    diff = (pair.iloc[:, 1] - pair.iloc[:, 0]).to_numpy()
    nonzero = diff[diff != 0]
    if len(nonzero) == 0:
        p, r = 1.0, 0.0
    else:
        p = stats.wilcoxon(nonzero).pvalue
        ranks = stats.rankdata(np.abs(nonzero))
        r = (ranks[nonzero > 0].sum() - ranks[nonzero < 0].sum()) / ranks.sum()
    return {
        "test": "Wilcoxon signed-rank",
        "n_pairs": len(pair),
        "mean_a": pair.iloc[:, 0].mean(),
        "mean_b": pair.iloc[:, 1].mean(),
        "effect": r,
        "effect_name": "rank-biserial r",
        "detail": f"non-zero differences: {len(nonzero)}",
        "p": p,
    }


def holm(p: pd.Series) -> pd.Series:
    order = p.sort_values().index
    m = len(p)
    adjusted, running = {}, 0.0
    for i, idx in enumerate(order):
        running = max(running, min(1.0, (m - i) * p[idx]))
        adjusted[idx] = running
    return pd.Series(adjusted)[p.index]


def wide(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    return df.pivot_table(index="question_id", columns=["condition", "mitigation"], values=metric, aggfunc="mean")


def paired_tests(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    binary = {"C0": ["correct"], "C1": ["correct"], "C2": ["correct"], "C3": ["correct"],
              "C4": ["correct", "followed_fake"], "C5": ["refused"]}
    tables = {m: wide(df, m) for m in ["correct", "refused", "followed_fake", "faithfulness"]}

    def add(family: str, metric: str, a: tuple, b: tuple) -> None:
        t = tables[metric]
        if a not in t.columns or b not in t.columns:
            return
        test = wilcoxon if metric == "faithfulness" else mcnemar
        rows.append({"family": family, "metric": metric, "a": " ".join(a), "b": " ".join(b), **test(t[a], t[b])})

    for cond in CONDITIONS:
        for m_a, m_b in itertools.combinations(MITIGATIONS, 2):
            for metric in binary[cond] + ["faithfulness"]:
                add("mitigation", metric, (cond, m_a), (cond, m_b))
    for mit in MITIGATIONS:
        for cond in ["C1", "C2", "C3", "C4"]:
            for metric in ["correct", "faithfulness"]:
                add("condition vs C0", metric, ("C0", mit), (cond, mit))
        for metric in ["correct", "faithfulness"]:
            add("random vs related noise", metric, ("C1", mit), ("C2", mit))

    out = pd.DataFrame(rows)
    out["p_holm"] = out.groupby("family")["p"].transform(holm)
    return out


def c4_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    c4 = df[df["condition"] == "C4"].copy()
    gold, fake, refused = c4["correct"] == 1, c4["followed_fake"] == 1, c4["refused"] == 1
    c4["outcome"] = np.select(
        [refused, gold & fake, gold, fake],
        ["refused", "both", "gold only", "fake only"],
        default="neither",
    )
    order = ["gold only", "fake only", "both", "neither", "refused"]
    counts = c4.groupby("mitigation")["outcome"].value_counts().unstack(fill_value=0)
    return counts.reindex(columns=order, fill_value=0)


def faithful_vs_correct(df: pd.DataFrame) -> pd.DataFrame:
    sub = df[df["condition"].isin(["C0", "C1", "C2", "C3", "C4"]) & df["faithfulness"].notna()].copy()
    sub["faithful"] = np.where(sub["faithfulness"] >= FAITHFUL_THRESHOLD, "faithful", "unfaithful")
    sub["right"] = np.where(sub["correct"] == 1, "correct", "wrong")
    sub["cell"] = sub["faithful"] + " & " + sub["right"]
    order = ["faithful & correct", "faithful & wrong", "unfaithful & correct", "unfaithful & wrong"]
    return sub.groupby("condition")["cell"].value_counts().unstack(fill_value=0).reindex(columns=order, fill_value=0)


def position_table(df: pd.DataFrame) -> pd.DataFrame:
    sub = df[df["condition"].isin(["C1", "C2", "C3", "C4"]) & df["gold_position"].notna()].copy()
    sub["slot"] = np.select(
        [sub["gold_position"] == 1, sub["gold_position"] == sub["n_passages"]],
        ["first", "last"],
        default="middle",
    )
    rows = []
    for slot, g in sub.groupby("slot"):
        rows.append({
            "slot": slot,
            "n": len(g),
            "correct": g["correct"].mean(),
            "faithfulness": g["faithfulness"].mean(),
        })
    table = pd.DataFrame(rows).set_index("slot").reindex(["first", "middle", "last"])
    contingency = pd.crosstab(sub["slot"], sub["correct"])
    chi2, p, _, _ = stats.chi2_contingency(contingency)
    kw = stats.kruskal(*[g["faithfulness"].dropna() for _, g in sub.groupby("slot")])
    table.attrs["tests"] = (
        f"Correctness by slot: chi-square = {chi2:.2f}, p = {p:.3f}. "
        f"Faithfulness by slot: Kruskal-Wallis H = {kw.statistic:.2f}, p = {kw.pvalue:.3f}."
    )
    return table


def memory_table(df: pd.DataFrame) -> pd.DataFrame:
    """Split answerable results by whether the model already answered correctly with no passages."""
    known = df[df["condition"] == "closed_book"].set_index("question_id")["correct"] == 1
    sub = df[df["condition"].isin(["C0", "C1", "C2", "C3", "C4"])].copy()
    sub["known_closed_book"] = sub["question_id"].map(known)
    rows = []
    for (cond, mit, k), g in sub.groupby(["condition", "mitigation", "known_closed_book"]):
        rows.append({
            "condition": cond,
            "mitigation": mit,
            "known_closed_book": bool(k),
            "n": len(g),
            "correct": g["correct"].mean(),
            "followed_fake": g["followed_fake"].mean() if cond == "C4" else np.nan,
            "faithfulness": g["faithfulness"].mean(),
        })
    return pd.DataFrame(rows)


def c4_memory_test(df: pd.DataFrame) -> str:
    known = df[df["condition"] == "closed_book"].set_index("question_id")["correct"] == 1
    c4 = df[df["condition"] == "C4"].copy()
    c4["known"] = c4["question_id"].map(known)
    lines = []
    for mit, g in c4.groupby("mitigation"):
        table = pd.crosstab(g["known"], g["followed_fake"])
        if table.shape == (2, 2):
            _, p = stats.fisher_exact(table)
            rate = g.groupby("known")["followed_fake"].mean()
            lines.append((mit, rate.get(True, np.nan), rate.get(False, np.nan), p))
    adjusted = holm(pd.Series([p for *_, p in lines]))
    return "; ".join(
        f"{mit}: followed fake {known_rate:.2f} when known closed-book vs {unknown_rate:.2f} when not "
        f"(Fisher exact p = {p:.3f}, Holm-adjusted over mitigations p = {p_adj:.3f})"
        for (mit, known_rate, unknown_rate, p), p_adj in zip(lines, adjusted)
    )


def paired_differences(df: pd.DataFrame, metric_cols: dict[str, str]) -> pd.DataFrame:
    """Bootstrap CIs for paired differences in means, with a TOST-style equivalence check.

    Equivalence at margin m holds (alpha = 0.05) when the 90% CI of the difference lies inside [-m, m].
    """
    rng = np.random.default_rng(SEED)
    comparisons = [(("C0", mit), (cond, mit)) for mit in MITIGATIONS for cond in ["C1", "C2", "C3"]]
    comparisons += [(("C1", mit), ("C2", mit)) for mit in MITIGATIONS]
    rows = []
    for label, col in metric_cols.items():
        t = wide(df, col)
        for a, b in comparisons:
            pair = pd.concat([t[a], t[b]], axis=1).dropna()
            diff = (pair.iloc[:, 1] - pair.iloc[:, 0]).to_numpy()
            boots = rng.choice(diff, size=(N_BOOT, len(diff)), replace=True).mean(axis=1)
            lo95, hi95 = np.percentile(boots, [2.5, 97.5])
            lo90, hi90 = np.percentile(boots, [5, 95])
            rows.append({
                "metric": label, "a": " ".join(a), "b": " ".join(b), "n_pairs": len(diff),
                "diff_b_minus_a": diff.mean(), "ci95_lo": lo95, "ci95_hi": hi95, "ci90_lo": lo90, "ci90_hi": hi90,
                f"equivalent_within_{EQUIV_MARGIN:.2f}": bool(lo90 > -EQUIV_MARGIN and hi90 < EQUIV_MARGIN),
            })
    return pd.DataFrame(rows)


def strict_sensitivity(df: pd.DataFrame) -> pd.DataFrame:
    """Re-run the correctness comparisons with the strict (exact containment) rule."""
    strict = df.assign(correct=df["correct_strict"])
    tests = paired_tests(strict)
    return tests[tests["metric"] == "correct"].reset_index(drop=True)


def refusal_tradeoff(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mit, g in df[df["condition"].isin(CONDITIONS)].groupby("mitigation"):
        c5 = g[g["condition"] == "C5"]
        rows.append({
            "mitigation": mit,
            "refusal C5 unanswerable (n=20)": c5[~c5["answerable"]]["refused"].mean(),
            "refusal C5 gold removed (n=75)": c5[c5["answerable"]]["refused"].mean(),
            "over-refusal C0-C4 (gold present)": g[g["condition"] != "C5"]["refused"].mean(),
        })
    return pd.DataFrame(rows).set_index("mitigation")


def save(fig: plt.Figure, out_dir, name: str) -> None:
    fig.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(out_dir / f"{name}.{ext}", dpi=200, bbox_inches="tight")
    plt.close(fig)


def grouped_bars(ax, ci: pd.DataFrame, metric: str, conditions: list[str], ylabel: str) -> None:
    width = 0.26
    x = np.arange(len(conditions))
    for i, mit in enumerate(MITIGATIONS):
        sel = ci[(ci["metric"] == metric) & (ci["mitigation"] == mit)].set_index("condition").reindex(conditions)
        err = np.vstack([sel["mean"] - sel["lo"], sel["hi"] - sel["mean"]])
        ax.bar(x + (i - 1) * width, sel["mean"], width, yerr=err, capsize=2,
               label=MIT_LABELS[mit], color=COLORS[mit])
    ax.set_xticks(x, conditions)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.3)


def figures(df: pd.DataFrame, ci: pd.DataFrame, c4: pd.DataFrame, trade: pd.DataFrame, out_dir) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 9})

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
    grouped_bars(axes[0], ci, "correct", CONDITIONS[:5], "Correctness (lenient)")
    cb = ci[(ci["condition"] == "closed_book")].iloc[0]
    axes[0].axhline(cb["mean"], color="grey", ls="--", lw=1)
    axes[0].text(-0.45, cb["mean"] + 0.02, "closed-book", color="grey", ha="left", fontsize=7,
                 bbox={"facecolor": "white", "edgecolor": "none", "pad": 1})
    axes[0].set_title("Correctness")
    grouped_bars(axes[1], ci, "faithfulness", CONDITIONS, "Ragas faithfulness")
    axes[1].set_title("Faithfulness (non-refused answers)")
    axes[1].legend(loc="lower left", fontsize=7)
    save(fig, out_dir, "fig_correct_faithfulness")

    fig, ax = plt.subplots(figsize=(4.5, 3))
    shares = c4.div(c4.sum(axis=1), axis=0).reindex(MITIGATIONS)
    palette = {"gold only": "#55A868", "fake only": "#C44E52", "both": "#8172B2", "neither": "#937860", "refused": "#BBBBBB"}
    left = np.zeros(len(shares))
    for col in shares.columns:
        ax.barh(MITIGATIONS, shares[col], left=left, color=palette[col], label=col)
        left += shares[col].to_numpy()
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Share of C4 answers")
    ax.set_title("Answers when a passage contradicts the gold passage")
    ax.legend(ncol=3, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.25))
    save(fig, out_dir, "fig_c4_outcomes")

    fig, ax = plt.subplots(figsize=(4.5, 3))
    x = np.arange(len(MITIGATIONS))
    cols = list(trade.columns)
    for i, (col, color) in enumerate(zip(cols, ["#4C72B0", "#8DA0CB", "#C44E52"])):
        ax.bar(x + (i - 1) * 0.26, trade.loc[MITIGATIONS, col], 0.26, label=col, color=color)
    ax.set_xticks(x, [MIT_LABELS[m] for m in MITIGATIONS], fontsize=7)
    ax.set_ylabel("Refusal rate")
    ax.set_ylim(0, 1)
    ax.set_title("Refusal: wanted (C5) vs unwanted (C0-C4)")
    ax.legend(fontsize=7)
    ax.grid(axis="y", alpha=0.3)
    save(fig, out_dir, "fig_refusal_tradeoff")

    fig, ax = plt.subplots(figsize=(4.5, 3))
    sel = ci[(ci["metric"] == "context_precision") & (ci["mitigation"] == "M0")].set_index("condition").reindex(CONDITIONS)
    ax.bar(CONDITIONS, sel["mean"], yerr=np.vstack([sel["mean"] - sel["lo"], sel["hi"] - sel["mean"]]),
           capsize=3, color="#4C72B0")
    corr = ci[(ci["metric"] == "correct") & (ci["mitigation"] == "M0")].set_index("condition").reindex(CONDITIONS[:5])
    ax.plot(CONDITIONS[:5], corr["mean"], "o-", color="#C44E52", label="M0 correctness")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Context precision")
    ax.set_title("Share of relevant passages vs correctness")
    ax.legend(fontsize=7)
    ax.grid(axis="y", alpha=0.3)
    save(fig, out_dir, "fig_context_precision")


def fmt_ci(ci: pd.DataFrame, metric: str) -> pd.DataFrame:
    sel = ci[ci["metric"] == metric].copy()
    sel["value"] = sel.apply(lambda r: f"{r['mean']:.3f} [{r['lo']:.3f}, {r['hi']:.3f}]", axis=1)
    return sel.pivot(index="condition", columns="mitigation", values="value").fillna("")


def main() -> None:
    args = config_arg_parser(__doc__).parse_args()
    cfg = load_config(args.config)
    df = load(cfg)
    res = results_dir(cfg)

    ci = ci_table(df)
    tests = paired_tests(df)
    c4 = c4_outcomes(df)
    fvc = faithful_vs_correct(df)
    pos = position_table(df)
    mem = memory_table(df)
    trade = refusal_tradeoff(df)
    diffs = paired_differences(df, {"correct": "correct", "correct_strict": "correct_strict",
                                    "faithfulness": "faithfulness"})
    strict_tests = strict_sensitivity(df)
    strict_fvc = faithful_vs_correct(df.assign(correct=df["correct_strict"]))

    diffs.round(4).to_csv(res / "noise_equivalence.csv", index=False)
    strict_tests.round(4).to_csv(res / "sensitivity_strict_tests.csv", index=False)
    ci.round(4).to_csv(res / "ci_table.csv", index=False)
    tests.round(4).to_csv(res / "paired_tests.csv", index=False)
    c4.to_csv(res / "c4_outcomes.csv")
    fvc.to_csv(res / "faithful_vs_correct.csv")
    pos.round(4).to_csv(res / "position.csv")
    mem.round(4).to_csv(res / "memory.csv", index=False)
    trade.round(4).to_csv(res / "refusal_tradeoff.csv")
    figures(df, ci, c4, trade, res / "figures")

    show = tests[["family", "metric", "a", "b", "n_pairs", "mean_a", "mean_b", "effect", "effect_name", "detail", "p", "p_holm"]]
    sections = [
        f"# Statistics: {cfg['run_name']}\n",
        f"Bootstrap: {N_BOOT} resamples of questions, seed {SEED}. Faithfulness and answer relevancy use "
        "non-refused answers only. Paired tests match the same question across two cells; p-values are "
        "Holm-adjusted within each family (`p_holm`).\n",
    ]
    for metric, title in [("correct", "Correctness (lenient; C5 = refusal)"), ("refused", "Refusal rate"),
                          ("faithfulness", "Faithfulness"), ("answer_relevancy", "Answer relevancy"),
                          ("context_precision", "Context precision"), ("followed_fake", "Followed fake (C4)")]:
        sections.append(f"## {title}: mean [95% CI]\n\n" + fmt_ci(ci, metric).to_markdown() + "\n")
    sections += [
        "## Paired tests\n\n" + show.to_markdown(index=False, floatfmt=".3f") + "\n",
        "## C4 outcomes (counts)\n\n" + c4.to_markdown() + "\n",
        f"## Faithfulness (>= {FAITHFUL_THRESHOLD}) vs correctness, C0-C4 non-refused (counts)\n\n" + fvc.to_markdown() + "\n",
        "## Gold passage position (C1-C4, all mitigations)\n\n" + pos.to_markdown(floatfmt=".3f") + "\n\n" + pos.attrs["tests"] + "\n",
        "## Refusal trade-off\n\n" + trade.to_markdown(floatfmt=".3f") + "\n",
        "## Prior knowledge (closed-book correct vs not)\n\n" + mem.to_markdown(index=False, floatfmt=".3f")
        + "\n\nC4 and memory: " + c4_memory_test(df) + "\n",
        f"## Noise conditions: paired differences with 95% and 90% CIs (equivalence margin ±{EQUIV_MARGIN:.2f})\n\n"
        "Equivalent = the 90% CI lies entirely inside the margin (two one-sided tests at alpha 0.05).\n\n"
        + diffs.to_markdown(index=False, floatfmt=".3f") + "\n",
        "## Sensitivity: correctness tests with the strict rule\n\n"
        + strict_tests[["family", "a", "b", "n_pairs", "mean_a", "mean_b", "effect", "detail", "p", "p_holm"]]
        .to_markdown(index=False, floatfmt=".3f") + "\n",
        "## Sensitivity: faithfulness vs strict correctness (counts)\n\n" + strict_fvc.to_markdown() + "\n",
    ]
    (res / "stats.md").write_text("\n".join(sections))
    print("\n".join(sections))
    print(f"Wrote {res / 'stats.md'} and figures in {res / 'figures'}")


if __name__ == "__main__":
    main()
