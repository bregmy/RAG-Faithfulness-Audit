"""Phase 2: build the corpus and question set from SQuAD v2 validation.csv.

Outputs:
  data/corpus/passages.jsonl     one row per paragraph of the sampled articles
  data/questions/questions.jsonl answerable + unanswerable questions (shuffled, fixed order)
"""

from __future__ import annotations

import ast
import random
import re
from collections import defaultdict

import pandas as pd

from src.common import (
    PASSAGES_PATH,
    QUESTIONS_PATH,
    ROOT,
    config_arg_parser,
    load_config,
    normalize_answer,
    write_jsonl,
)


def parse_answers(raw: str) -> list[dict]:
    """Parse the numpy-repr `answers` column into [{'text', 'start'}, ...].

    Example input:
      {'text': array(['France', 'France'], dtype=object), 'answer_start': array([159, 159], dtype=int32)}
    """
    cleaned = re.sub(r",\s*dtype=\w+\)", ")", raw).replace("array(", "(")
    parsed = ast.literal_eval(cleaned)
    texts = list(parsed["text"])
    starts = [int(s) for s in parsed["answer_start"]]
    return [{"text": t, "start": s} for t, s in zip(texts, starts)]


def main() -> None:
    args = config_arg_parser(__doc__).parse_args()
    cfg = load_config(args.config)
    dcfg = cfg["data"]
    rng = random.Random(cfg["seed"])

    df = pd.read_csv(ROOT / dcfg["csv"], dtype=str, keep_default_na=False)
    df["answers_parsed"] = df["answers"].map(parse_answers)

    misaligned = sum(
        1
        for ctx, answers in zip(df["context"], df["answers_parsed"])
        for a in answers
        if ctx[a["start"] : a["start"] + len(a["text"])] != a["text"]
    )
    print(f"Loaded {len(df)} rows; misaligned answer spans: {misaligned}")

    titles = sorted(df["title"].unique())
    chosen_titles = sorted(rng.sample(titles, dcfg["n_articles"]))
    sub = df[df["title"].isin(chosen_titles)]

    passages = []
    passage_id_of: dict[str, str] = {}
    for a_idx, title in enumerate(chosen_titles):
        contexts = list(dict.fromkeys(sub.loc[sub["title"] == title, "context"]))
        for p_idx, ctx in enumerate(contexts):
            pid = f"a{a_idx:02d}_p{p_idx:03d}"
            passage_id_of[ctx] = pid
            passages.append({"passage_id": pid, "title": title, "text": ctx})
    write_jsonl(PASSAGES_PATH, passages)

    answerable_by_passage = defaultdict(list)
    unanswerable = []
    for row in sub.itertuples(index=False):
        answers = row.answers_parsed
        base = {
            "question_id": row.id,
            "title": row.title,
            "question": row.question,
            "gold_passage_id": passage_id_of[row.context],
        }
        if not answers:
            unanswerable.append({**base, "answerable": False, "gold_answers": []})
            continue
        primary = answers[0]
        if len(primary["text"].split()) > dcfg["max_answer_words"]:
            continue
        if normalize_answer(primary["text"]) in normalize_answer(row.question):
            continue
        gold = list(dict.fromkeys(a["text"] for a in answers))
        answerable_by_passage[base["gold_passage_id"]].append(
            {**base, "answerable": True, "gold_answers": gold, "primary_answer": primary["text"]}
        )

    # At most one answerable question per passage, for topical diversity.
    pids = sorted(answerable_by_passage)
    rng.shuffle(pids)
    answerable = [rng.choice(answerable_by_passage[pid]) for pid in pids[: dcfg["n_answerable"]]]
    rng.shuffle(unanswerable)
    unanswerable = unanswerable[: dcfg["n_unanswerable"]]

    questions = answerable + unanswerable
    rng.shuffle(questions)
    write_jsonl(QUESTIONS_PATH, questions)

    print(f"Articles: {len(chosen_titles)}  Passages: {len(passages)}")
    print(f"Questions: {len(answerable)} answerable + {len(unanswerable)} unanswerable")


if __name__ == "__main__":
    main()
