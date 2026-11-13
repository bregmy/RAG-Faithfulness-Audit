"""Side-by-side tables across answer models and across judges.

  uv run python -m src.analysis.compare models
    -> results/model_comparison.md / .csv
       every results/full*/summary.csv (one per answer model), key measures per condition x mitigation
  uv run python -m src.analysis.compare judges [--run full]
    -> results/<run>/judge_comparison.md
       each judge (local, gemini, haiku, ...) against both human annotators, judge-vs-judge agreement,
       and how each judge scores C4 answers that repeated the injected falsehood
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats

from src.analysis.human_validation import FAITHFUL_THRESHOLD, KEY, SHEET, SHEET2, SUPPORT_SCORE, kappa
from src.common import ROOT, read_jsonl

MEASURES = ["correct_rate", "refusal_rate", "faithfulness", "followed_fake_rate", "context_precision"]


def models() -> None:
    rows = []
    for summary in sorted((ROOT / "results").glob("full*/summary.csv")):
        run = summary.parent.name
        manifest = ROOT / "runs" / run / "manifest_generation.json"
        model = json.loads(manifest.read_text())["config"]["generator"]["model"] if manifest.exists() else run
        rows.append(pd.read_csv(summary).assign(model=model))
    if not rows:
        raise SystemExit("No results/full*/summary.csv found; run the summarize step first.")
    df = pd.concat(rows)
    df.to_csv(ROOT / "results/model_comparison.csv", index=False)

    sections = [f"# Answer models compared\n\nModels: {', '.join(df['model'].unique())}\n"]
    for measure in MEASURES:
        table = df.pivot_table(index=["condition", "mitigation"], columns="model", values=measure)
        if table.notna().any().any():
            sections.append(f"## {measure}\n\n" + table.to_markdown(floatfmt=".3f") + "\n")
    out = ROOT / "results/model_comparison.md"
    out.write_text("\n".join(sections))
    print("\n".join(sections))
    print(f"Wrote {out}")


def load_judges(run: str) -> dict[str, dict[str, float]]:
    judges = {}
    for path in sorted((ROOT / "runs" / run).glob("judge_answers*.jsonl")):
        name = path.stem.removeprefix("judge_answers").removeprefix("_") or "local"
        judges[name] = {r["gen_id"]: r["faithfulness"] for r in read_jsonl(path) if r.get("faithfulness") is not None}
    return judges


def judges(run: str) -> None:
    key = pd.read_csv(KEY)[["item", "gen_id", "condition"]]
    labels = {}
    for name, sheet in (("A", SHEET), ("B", SHEET2)):
        s = pd.read_csv(sheet, keep_default_na=False).set_index("item")["human_support"].astype(str)
        labels[name] = key.set_index("item")["gen_id"].to_frame().join(
            s.str.strip().str.lower().map(SUPPORT_SCORE).rename("support")
        ).dropna().set_index("gen_id")["support"]
    found = load_judges(run)

    rows = []
    for judge, faith in found.items():
        row = {"judge": judge}
        for annot, support in labels.items():
            ids = [g for g in support.index if g in faith]
            j = np.array([faith[g] >= FAITHFUL_THRESHOLD for g in ids], dtype=int)
            h = np.array([support[g] == 1 for g in ids], dtype=int)
            row |= {
                f"n_{annot}": len(ids),
                f"accuracy_vs_{annot}": (j == h).mean() if ids else np.nan,
                f"kappa_vs_{annot}": kappa(j, h) if ids else np.nan,
                f"spearman_vs_{annot}": stats.spearmanr([faith[g] for g in ids], support[ids]).statistic
                if len(ids) > 2 else np.nan,
            }
        rows.append(row)

    pairs = []
    for a, b in combinations(found, 2):
        ids = sorted(set(found[a]) & set(found[b]))
        if ids:
            x = np.array([found[a][g] >= FAITHFUL_THRESHOLD for g in ids], dtype=int)
            y = np.array([found[b][g] >= FAITHFUL_THRESHOLD for g in ids], dtype=int)
            pairs.append({"judges": f"{a} vs {b}", "n": len(ids), "agreement": (x == y).mean(), "kappa": kappa(x, y)})

    scored = pd.read_csv(ROOT / "runs" / run / "scored.csv")
    fake_ids = scored.loc[(scored["condition"] == "C4") & (scored["followed_fake"] == True) & ~scored["refused"], "gen_id"]
    fake = []
    for judge, faith in found.items():
        vals = [faith[g] for g in fake_ids if g in faith]
        if vals:
            fake.append({"judge": judge, "n_judged": len(vals), "mean_faithfulness": np.mean(vals),
                         "share_rated_faithful": np.mean([v >= FAITHFUL_THRESHOLD for v in vals])})

    text = (
        f"# Judges compared: {run}\n\n"
        f"Faithful = judge score >= {FAITHFUL_THRESHOLD}; human positive = 'supported'. "
        "Annotators A and B labeled the same sampled answers (non-refusals only here).\n\n"
        "## Each judge against the human annotators\n\n"
        + pd.DataFrame(rows).to_markdown(index=False, floatfmt=".3f")
        + "\n\n## Judge-vs-judge agreement (answers both judged)\n\n"
        + (pd.DataFrame(pairs).to_markdown(index=False, floatfmt=".3f") if pairs else "Only one judge found.")
        + f"\n\n## C4 answers that repeated the injected falsehood ({len(fake_ids)} non-refused)\n\n"
        "A high score means the judge calls these answers grounded even though they are false.\n\n"
        + (pd.DataFrame(fake).to_markdown(index=False, floatfmt=".3f") if fake else "No judged C4 answers.")
        + "\n"
    )
    out = ROOT / "results" / run / "judge_comparison.md"
    out.write_text(text)
    print(text)
    print(f"Wrote {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["models", "judges"])
    parser.add_argument("--run", default="full", help="run whose judges to compare (judges)")
    args = parser.parse_args()
    models() if args.command == "models" else judges(args.run)


if __name__ == "__main__":
    main()
