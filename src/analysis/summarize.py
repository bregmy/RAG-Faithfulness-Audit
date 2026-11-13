"""Combine generations, judge scores, and text checks into tables.

Outputs:
  runs/<run_name>/scored.csv       one row per answer, all fields (open in LibreOffice/Excel)
  results/<run_name>/summary.csv   averages per condition x mitigation
  results/<run_name>/summary.md    the same tables, readable
Works before judging is finished; missing judge scores are left blank.
"""

from __future__ import annotations

import pandas as pd

from src.common import (
    QUESTIONS_PATH,
    config_arg_parser,
    judge_suffix,
    load_config,
    read_jsonl,
    results_dir,
    run_contexts_path,
    run_dir,
)
from src.evaluate.rules import contains_any, is_refusal, matches_any

ANSWERABLE_CONDITIONS = {"C0", "C1", "C2", "C3", "C4", "closed_book"}


def context_precision(ctx: dict, question_id: str, relevance: dict) -> float | None:
    values = [relevance.get(f"{question_id}|{pid}") for pid in ctx.get("passage_ids", [])]
    if not values or any(v is None for v in values):
        return None
    return sum(values) / len(values)


def build_scored(cfg: dict, judge: str = "local") -> pd.DataFrame:
    out_dir = run_dir(cfg)
    suffix = judge_suffix(judge)
    questions = {q["question_id"]: q for q in read_jsonl(QUESTIONS_PATH)}
    contexts = {c["context_id"]: c for c in read_jsonl(run_contexts_path(cfg))}
    judged = {r["gen_id"]: r for r in read_jsonl(out_dir / f"judge_answers{suffix}.jsonl")}
    relevance = {r["pair_id"]: r["relevant"] for r in read_jsonl(out_dir / f"judge_passages{suffix}.jsonl")}

    rows = []
    for g in read_jsonl(out_dir / "generations.jsonl"):
        if "error" in g:
            continue
        q = questions[g["question_id"]]
        ctx = contexts.get(g["context_id"]) or {}
        j = judged.get(g["gen_id"], {})
        response = g["response"]
        refused = is_refusal(response)
        substitute = ctx.get("substitute_answer")
        is_c4 = g["condition"] == "C4"

        correct = correct_strict = None
        if q["answerable"] and g["condition"] in ANSWERABLE_CONDITIONS:
            correct = matches_any(response, q["gold_answers"])
            correct_strict = contains_any(response, q["gold_answers"])
        elif g["condition"] == "C5":
            correct = correct_strict = refused

        rows.append(
            {
                "gen_id": g["gen_id"],
                "question_id": g["question_id"],
                "question": q["question"],
                "answerable": q["answerable"],
                "condition": g["condition"],
                "mitigation": g["mitigation"],
                "repeat": g["repeat"],
                "gold_answers": " | ".join(q["gold_answers"]),
                "response": response,
                "refused": refused,
                "empty": not response.strip(),
                "correct": correct,
                "correct_strict": correct_strict,
                "fake_answer": substitute if is_c4 else None,
                "followed_fake": matches_any(response, [substitute]) if is_c4 else None,
                "faithfulness": j.get("faithfulness"),
                "answer_relevancy": j.get("answer_relevancy"),
                "context_precision": context_precision(ctx, g["question_id"], relevance) if ctx else None,
                "gold_position": ctx["roles"].index("gold") + 1 if "gold" in ctx.get("roles", []) else None,
                "n_passages": len(ctx.get("roles", [])),
                "latency_s": g["latency_s"],
            }
        )
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    def agg(group: pd.DataFrame) -> pd.Series:
        not_refused = group[~group["refused"]]
        return pd.Series(
            {
                "n": len(group),
                "correct_rate": group["correct"].astype("float").mean(),
                "correct_strict_rate": group["correct_strict"].astype("float").mean(),
                "refusal_rate": group["refused"].mean(),
                "no_answer_rate": group["empty"].mean(),
                "faithfulness": pd.to_numeric(not_refused["faithfulness"]).mean(),
                "answer_relevancy": pd.to_numeric(not_refused["answer_relevancy"]).mean(),
                "context_precision": pd.to_numeric(group["context_precision"]).mean(),
                "followed_fake_rate": group["followed_fake"].astype("float").mean(),
                "n_judged": group["answer_relevancy"].notna().sum(),
            }
        )

    return df.groupby(["condition", "mitigation"]).apply(agg, include_groups=False).reset_index().round(3)


def run(cfg: dict, judge: str = "local") -> None:
    suffix = judge_suffix(judge)
    df = build_scored(cfg, judge)
    df.to_csv(run_dir(cfg) / f"scored{suffix}.csv", index=False)

    summary = summarize(df)
    res = results_dir(cfg)
    summary.to_csv(res / f"summary{suffix}.csv", index=False)

    notes = (
        f"# Summary: {cfg['run_name']} (generator: {cfg['generator']['model']}, judge: {judge})\n\n"
        f"Answers: {len(df)} · judged: {int(df['answer_relevancy'].notna().sum())}\n\n"
        "- `correct_rate`: answer matches a gold answer leniently (all numbers and at least 2/3 of the words; "
        "C0–C4 and closed_book). For C5 it is the refusal rate, because refusing is correct there. "
        "`correct_strict_rate` requires the exact gold answer.\n"
        "- `no_answer_rate`: empty answers, e.g. a reasoning model that used its whole token budget thinking. "
        "They count as incorrect and are not refusals.\n"
        "- `faithfulness` and `answer_relevancy`: means over answers that were **not** refusals.\n"
        "- `context_precision`: share of passages in the context that the judge rated relevant to the question.\n"
        "- `followed_fake_rate`: C4 only; the answer matches the substituted (false) answer.\n\n"
    )
    (res / f"summary{suffix}.md").write_text(notes + summary.to_markdown(index=False) + "\n")
    print(summary.to_string(index=False))
    print(f"\nWrote {run_dir(cfg) / f'scored{suffix}.csv'} and {res / f'summary{suffix}.md'}")


def main() -> None:
    parser = config_arg_parser(__doc__)
    parser.add_argument("--judge", default="local", help="which judge's scores to use (local, gemini, haiku, ...)")
    args = parser.parse_args()
    run(load_config(args.config), args.judge)


if __name__ == "__main__":
    main()
