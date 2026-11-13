"""Check the automatic judge against human labels.

Step 1 (sample): write a labeling sheet with judge scores hidden.
  uv run python -m src.analysis.human_validation sample --config configs/full.toml
  -> labels/validation_sheet.csv   fill in the human_* columns (keep it as CSV)
  -> labels/validation_items.md    the same items, easier to read
  -> labels/validation_key.csv     judge and rule scores; do not open it before labeling

Step 2 (agree): compare the filled-in sheet with the judge.
  uv run python -m src.analysis.human_validation agree --config configs/full.toml
  -> results/<run_name>/human_validation.md
  Add --sheet labels/validation_sheet_annotator2.csv to compare a second annotator with the judge
  (-> human_validation_annotator2.md).

Step 3 (iaa): agreement between the two annotators and the items they disagree on.
  uv run python -m src.analysis.human_validation iaa --config configs/full.toml
  -> results/<run_name>/inter_annotator.md
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from src.common import ROOT, config_arg_parser, load_config, read_jsonl, results_dir, run_contexts_path, run_dir
from src.evaluate.rules import matches_any

LABELS_DIR = ROOT / "labels"
SHEET = LABELS_DIR / "validation_sheet.csv"
SHEET2 = LABELS_DIR / "validation_sheet_annotator2.csv"
ITEMS = LABELS_DIR / "validation_items.md"
KEY = LABELS_DIR / "validation_key.csv"
CONDITIONS = ["C0", "C1", "C2", "C3", "C4", "C5"]
PER_CONDITION = 12
N_REFUSALS = 8
FAITHFUL_THRESHOLD = 0.5
SUPPORT_SCORE = {"supported": 1.0, "partial": 0.5, "unsupported": 0.0}
SEED = 42


def sample(cfg: dict) -> None:
    df = pd.read_csv(run_dir(cfg) / "scored.csv")
    contexts = {c["context_id"]: c for c in read_jsonl(run_contexts_path(cfg))}
    df = df[df["condition"].isin(CONDITIONS)].copy()
    df["context_id"] = df["question_id"] + "_" + df["condition"]
    rng = np.random.default_rng(SEED)

    # Per condition, half the answers the judge called faithful and half it did not (when there are
    # enough), spread over the three prompts, so agreement is measured on both kinds of verdict.
    def spread(pool: pd.DataFrame, n: int) -> pd.DataFrame:
        """Random n rows, taking from the three prompts in turn."""
        pool = pool.sample(frac=1, random_state=int(rng.integers(1e9)))
        pool = pool.assign(turn=pool.groupby("mitigation").cumcount())
        return pool.sort_values(["turn", "mitigation"]).head(n).drop(columns="turn")

    picks = []
    answered = df[~df["refused"] & df["faithfulness"].notna()]
    for cond in CONDITIONS:
        pool = answered[answered["condition"] == cond]
        low = spread(pool[pool["faithfulness"] < FAITHFUL_THRESHOLD], PER_CONDITION // 2)
        high = spread(pool[pool["faithfulness"] >= FAITHFUL_THRESHOLD], PER_CONDITION - len(low))
        picks += [low, high]
    refusals = spread(df[df["refused"]], N_REFUSALS)
    picks.append(refusals)
    sel = pd.concat(picks).sample(frac=1, random_state=SEED).reset_index(drop=True)
    sel.insert(0, "item", range(1, len(sel) + 1))

    def passages_text(context_id: str) -> str:
        return "\n\n".join(f"[{i}] {p}" for i, p in enumerate(contexts[context_id]["passages"], 1))

    sheet = pd.DataFrame({
        "item": sel["item"],
        "question": sel["question"],
        "gold_answers": np.where(sel["answerable"], sel["gold_answers"], "(no answer exists)"),
        "passages": sel["context_id"].map(passages_text),
        "answer": sel["response"],
        "human_support": "",
        "human_correct": "",
        "human_refusal": "",
        "notes": "",
    })
    key = sel[["item", "gen_id", "condition", "mitigation", "answerable", "refused", "correct",
               "followed_fake", "faithfulness", "answer_relevancy"]]

    LABELS_DIR.mkdir(exist_ok=True)
    if SHEET.exists():
        raise SystemExit(f"{SHEET} already exists; delete it first if you really want a new sample.")
    sheet.to_csv(SHEET, index=False)
    key.to_csv(KEY, index=False)
    blocks = [
        f"## Item {r.item}\n\n**Question:** {r.question}\n\n**Gold answer(s):** {r.gold_answers}\n\n"
        f"**Passages:**\n\n{r.passages}\n\n**Answer:** {r.answer}\n"
        for r in sheet.itertuples()
    ]
    ITEMS.write_text("# Validation items\n\nLabel these in `validation_sheet.csv`.\n\n" + "\n---\n\n".join(blocks))
    print(f"Wrote {len(sheet)} items to {SHEET} and {ITEMS} (key: {KEY})")
    print(key.groupby(["condition", "mitigation"]).size().unstack(fill_value=0))


def kappa(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.asarray(a), np.asarray(b)
    observed = (a == b).mean()
    expected = sum((a == c).mean() * (b == c).mean() for c in np.union1d(a, b))
    return np.nan if expected == 1 else (observed - expected) / (1 - expected)


def kappa_ci(a: np.ndarray, b: np.ndarray, rng: np.random.Generator, n_boot: int = 2000) -> tuple[float, float]:
    idx = rng.integers(0, len(a), size=(n_boot, len(a)))
    values = np.array([kappa(a[i], b[i]) for i in idx])
    return tuple(np.nanpercentile(values, [2.5, 97.5]))


def agreement_row(name: str, judge: np.ndarray, human: np.ndarray, rng: np.random.Generator) -> dict:
    lo, hi = kappa_ci(judge, human, rng)
    return {
        "check": name,
        "n": len(judge),
        "accuracy": (judge == human).mean(),
        "cohen_kappa": kappa(judge, human),
        "kappa_95ci": f"[{lo:.2f}, {hi:.2f}]",
        "judge_positive": judge.mean(),
        "human_positive": human.mean(),
    }


def population_estimate(cfg: dict, labeled: pd.DataFrame) -> pd.DataFrame:
    run = pd.read_csv(run_dir(cfg) / "scored.csv")
    run = run[run["condition"].isin(CONDITIONS) & ~run["refused"] & run["faithfulness"].notna()]
    rows = []
    for cond, g in run.groupby("condition"):
        share_faithful = (g["faithfulness"] >= FAITHFUL_THRESHOLD).mean()
        lab = labeled[labeled["condition"] == cond]
        hi, lo = lab[lab["judge"] == 1], lab[lab["judge"] == 0]

        def weighted(ok: pd.Series) -> float:
            return share_faithful * ok[hi.index].mean() + (1 - share_faithful) * ok[lo.index].mean()

        p_sup_hi, p_sup_lo = (hi["support"] == 1).mean(), (lo["support"] == 1).mean()
        rows.append({
            "condition": cond,
            "n_answers": len(g),
            "p_judge1_human1": share_faithful * p_sup_hi,
            "p_judge1_human0": share_faithful * (1 - p_sup_hi),
            "p_judge0_human1": (1 - share_faithful) * p_sup_lo,
            "p_judge0_human0": (1 - share_faithful) * (1 - p_sup_lo),
            "judge_mean_faithfulness": g["faithfulness"].mean(),
            "judge_share_faithful": share_faithful,
            "human_supported_given_judge_faithful": (hi["support"] == 1).mean(),
            "human_supported_given_judge_unfaithful": (lo["support"] == 1).mean(),
            "est_human_supported": weighted(lab["support"] == 1),
            "est_human_supported_or_partial": weighted(lab["support"] >= 0.5),
        })
    return pd.DataFrame(rows)


def yes_no(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().map({"yes": 1, "y": 1, "no": 0, "n": 0})


def agree(cfg: dict, sheet=SHEET) -> None:
    labels = pd.read_csv(sheet)
    key = pd.read_csv(KEY)
    df = labels.merge(key, on="item")
    df["support"] = df["human_support"].astype(str).str.strip().str.lower().map(SUPPORT_SCORE)
    df["h_correct"] = yes_no(df["human_correct"])
    df["h_refusal"] = yes_no(df["human_refusal"])
    rng = np.random.default_rng(SEED)
    rows, notes = [], []

    f = df[df["support"].notna() & df["faithfulness"].notna()]
    if len(f):
        judge = (f["faithfulness"] >= FAITHFUL_THRESHOLD).astype(int).to_numpy()
        rows.append(agreement_row("faithful: judge >= 0.5 vs human 'supported'", judge,
                                  (f["support"] == 1).astype(int).to_numpy(), rng))
        rows.append(agreement_row("faithful: judge >= 0.5 vs human 'supported' or 'partial'", judge,
                                  (f["support"] >= 0.5).astype(int).to_numpy(), rng))
        rho = stats.spearmanr(f["faithfulness"], f["support"])
        notes.append(f"Spearman correlation between judge faithfulness and human support "
                     f"(supported=1, partial=0.5, unsupported=0): rho = {rho.statistic:.3f}, p = {rho.pvalue:.4f}, n = {len(f)}.")
        f = f.assign(judge=judge, human=(f["support"] == 1).astype(int))
        by_cond = f.groupby("condition").apply(
            lambda g: pd.Series({"n": len(g), "agreement": (g["judge"] == g["human"]).mean(),
                                 "judge_faithful": g["judge"].mean(), "human_supported": g["human"].mean()}),
            include_groups=False,
        )
        by_verdict = pd.crosstab(
            f["judge"].map({1: "judge faithful (>= 0.5)", 0: "judge unfaithful (< 0.5)"}),
            f["human_support"].str.strip().str.lower(), margins=True,
        )
        estimate = population_estimate(cfg, f)
        cells = ["p_judge1_human1", "p_judge1_human0", "p_judge0_human1", "p_judge0_human0"]
        joint = estimate[cells].mul(estimate["n_answers"], axis=0).sum() / estimate["n_answers"].sum()
        accuracy = joint["p_judge1_human1"] + joint["p_judge0_human0"]
        judge_pos = joint["p_judge1_human1"] + joint["p_judge1_human0"]
        human_pos = joint["p_judge1_human1"] + joint["p_judge0_human1"]
        expected = judge_pos * human_pos + (1 - judge_pos) * (1 - human_pos)
        notes.append(
            "Prevalence-weighted agreement (the balanced sample re-weighted to the run's mix of judge verdicts, "
            f"C0-C5): accuracy = {accuracy:.3f}, Cohen's kappa = {(accuracy - expected) / (1 - expected):.3f}, "
            f"judge faithful = {judge_pos:.3f}, human supported = {human_pos:.3f}."
        )
        estimate = estimate.drop(columns=cells + ["n_answers"])
    else:
        by_cond = by_verdict = estimate = pd.DataFrame()

    # The run's `correct` column means "refused" for C5, so compare gold-answer matching directly.
    c = df[df["answerable"] & df["h_correct"].notna()]
    if len(c):
        rule = c.apply(lambda r: matches_any(r["answer"], r["gold_answers"].split(" | ")), axis=1)
        rows.append(agreement_row("correct: lenient rule vs human", rule.astype(int).to_numpy(),
                                  c["h_correct"].astype(int).to_numpy(), rng))
    r = df[df["h_refusal"].notna()]
    if len(r):
        rows.append(agreement_row("refusal: regex vs human", r["refused"].astype(int).to_numpy(),
                                  r["h_refusal"].astype(int).to_numpy(), rng))

    missing = int((df["support"].isna() & (df["h_refusal"] != 1)).sum())
    if missing > 0:
        notes.append(f"Warning: {missing} non-refusal items have no human_support label yet.")
    table = pd.DataFrame(rows)
    sections = [
        f"# Human validation: {cfg['run_name']}\n\nLabels: `{sheet.name}` · items: {len(df)}\n\n"
        + (table.to_markdown(index=False, floatfmt=".3f") if len(table) else "No labels found.")
        + "\n\n" + "\n\n".join(notes) + "\n",
    ]
    if len(by_cond):
        sections += [
            "## Human labels by judge verdict (counts)\n\n" + by_verdict.to_markdown() + "\n",
            "## Faithfulness agreement by condition (balanced sample)\n\n" + by_cond.to_markdown(floatfmt=".3f") + "\n",
            "## Estimated share of answers humans would rate supported (whole run)\n\n"
            "The sample has equal numbers of judge-faithful and judge-unfaithful answers per condition. "
            "Here the human rate within each verdict is re-weighted by how common that verdict is among all "
            "non-refused answers in the run.\n\n" + estimate.to_markdown(index=False, floatfmt=".3f") + "\n",
        ]
    text = "\n".join(sections)
    suffix = sheet.stem.removeprefix("validation_sheet")
    out = results_dir(cfg) / f"human_validation{suffix}.md"
    out.write_text(text)
    print(text)
    print(f"Wrote {out}")


def iaa(cfg: dict, sheet_a=SHEET, sheet_b=SHEET2) -> None:
    """Agreement between two annotators, plus the items they disagree on."""
    a = pd.read_csv(sheet_a, dtype=str, keep_default_na=False).set_index("item")
    b = pd.read_csv(sheet_b, dtype=str, keep_default_na=False).set_index("item")
    rng = np.random.default_rng(SEED)
    clean = lambda s: s.str.strip().str.lower()
    rows = []

    def add(name: str, x: pd.Series, y: pd.Series) -> None:
        mask = (x != "") & (y != "")
        x, y = x[mask].to_numpy(), y[mask].to_numpy()
        lo, hi = kappa_ci(x, y, rng)
        rows.append({"label": name, "n": len(x), "agreement": (x == y).mean(),
                     "cohen_kappa": kappa(x, y), "kappa_95ci": f"[{lo:.2f}, {hi:.2f}]"})

    sa, sb = clean(a["human_support"]), clean(b["human_support"])
    add("support (3 levels)", sa, sb)
    add("support: 'supported' vs not", sa.where(sa == "", (sa == "supported").astype(str)),
        sb.where(sb == "", (sb == "supported").astype(str)))
    add("support: 'supported' or 'partial' vs 'unsupported'", sa.where(sa == "", (sa != "unsupported").astype(str)),
        sb.where(sb == "", (sb != "unsupported").astype(str)))
    add("correct", clean(a["human_correct"]), clean(b["human_correct"]))
    add("refusal", clean(a["human_refusal"]), clean(b["human_refusal"]))

    cols = ["human_support", "human_correct", "human_refusal"]
    differ = (a[cols].apply(clean) != b[cols].apply(clean)).any(axis=1)
    disagreements = pd.DataFrame({
        "question": a.loc[differ, "question"],
        "answer": a.loc[differ, "answer"],
        **{f"A {c.removeprefix('human_')}": a.loc[differ, c] for c in cols},
        **{f"B {c.removeprefix('human_')}": b.loc[differ, c] for c in cols},
        "A notes": a.loc[differ, "notes"],
        "B notes": b.loc[differ, "notes"],
    })
    text = (
        f"# Inter-annotator agreement: {cfg['run_name']}\n\n"
        f"Annotator A: `{sheet_a.name}` · annotator B: `{sheet_b.name}` · items: {len(a)}\n\n"
        + pd.DataFrame(rows).to_markdown(index=False, floatfmt=".3f")
        + f"\n\n## Items with any disagreement ({int(differ.sum())})\n\n"
        + disagreements.to_markdown(floatfmt=".3f") + "\n"
    )
    out = results_dir(cfg) / "inter_annotator.md"
    out.write_text(text)
    print(text)
    print(f"Wrote {out}")


def main() -> None:
    parser = config_arg_parser(__doc__)
    parser.add_argument("command", choices=["sample", "agree", "iaa"])
    parser.add_argument("--sheet", default=str(SHEET), help="labeled sheet to compare with the judge (agree)")
    args = parser.parse_args()
    cfg = load_config(args.config)
    if args.command == "sample":
        sample(cfg)
    elif args.command == "agree":
        agree(cfg, Path(args.sheet).resolve())
    else:
        iaa(cfg)


if __name__ == "__main__":
    main()
