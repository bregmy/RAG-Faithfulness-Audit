"""Phase 4: build the perturbed contexts (conditions C0-C5) for every question.

Conditions (answerable questions):
  C0 clean         gold passage only
  C1 random        gold + 3 random passages from other articles
  C2 related       gold + 3 high-similarity passages that do not contain the answer
  C3 noisy         gold + 3 related + 3 random distractors (7 passages)
  C4 contradictory gold + a copy of gold with the answer entity substituted + 2 related
  C5 unanswerable  4 related passages, gold removed
Unanswerable SQuAD questions only get C5: their source paragraph + 3 related passages.

Passage order is shuffled per (question, condition) with a fixed seed, and the
positions of the gold / injected passages are recorded.

Output: data/perturbations/contexts.jsonl
"""

from __future__ import annotations

import json
import random
import re
from typing import Any

import pandas as pd

from src.common import (
    CONTEXTS_PATH,
    PASSAGES_PATH,
    QUESTIONS_PATH,
    ROOT,
    config_arg_parser,
    load_config,
    normalize_answer,
    read_jsonl,
    write_jsonl,
)
from src.evaluate.rules import matches_answer, matches_any

OVERRIDES_PATH = ROOT / "data/perturbations/substitute_overrides.json"
from src.ingest.build_dataset import parse_answers
from src.retrieve.index import get_collection, search


WH_WORDS = ["who", "whom", "whose", "when", "where", "which", "what", "why", "how"]


def wh_word(question: str) -> str:
    tokens = re.findall(r"[a-z]+", question.lower())
    return next((t for t in tokens if t in WH_WORDS), "other")


def perturb_number(answer: str, rng: random.Random) -> str:
    """Change every number in the answer while keeping its format.

    Years shift by 5-40, decades ("1950s") by 10-30 in steps of 10.
    """

    def replace(match: re.Match) -> str:
        digits = match.group(0)
        value = int(digits)
        is_decade = match.string[match.end() : match.end() + 1] == "s"
        if len(digits) == 4 and 1000 <= value <= 2099 and is_decade:
            return str(value + rng.choice([-1, 1]) * 10 * rng.randint(1, 3))
        if len(digits) == 4 and 1000 <= value <= 2099:
            return str(value + rng.choice([-1, 1]) * rng.randint(5, 40))
        while True:
            new = "".join(str(rng.randint(0, 9)) for _ in digits)
            if len(digits) > 1 and new[0] == "0":
                continue
            if new != digits:
                return new

    return re.sub(r"\d+", replace, answer)


def is_descending_range(text: str) -> bool:
    match = re.search(r"(\d+)\s*[–-]\s*(\d+)", text)
    return bool(match) and int(match.group(1)) > int(match.group(2))


def usable_substitute(q: dict, gold_text: str, candidate: str) -> bool:
    """The substitute must differ from every gold answer and must not already appear in the gold passage."""
    n = normalize_answer(candidate)
    gold_norm = {normalize_answer(a) for a in q["gold_answers"]}
    return (
        bool(n)
        and n not in gold_norm
        and n not in normalize_answer(gold_text)
        and not matches_any(candidate, q["gold_answers"])
        and not any(matches_answer(g, candidate) for g in q["gold_answers"])
    )


def pick_substitute(
    q: dict, gold_text: str, pool: list[dict], rng: random.Random, overrides: dict[str, str]
) -> str:
    """Build a plausible wrong answer that does not appear in the gold passage.

    Hand-reviewed overrides take priority. Otherwise numeric answers get their digits changed,
    and other answers are drawn from answers to questions with the same wh-word, preferring
    the same article so the substitute is on-topic.
    """
    primary = q["primary_answer"]

    if q["question_id"] in overrides:
        candidate = overrides[q["question_id"]]
        if not usable_substitute(q, gold_text, candidate):
            raise ValueError(f"Override {candidate!r} for {q['question_id']} conflicts with the gold passage/answer")
        return candidate

    def usable(a: str) -> bool:
        return usable_substitute(q, gold_text, a)

    if re.search(r"\d", primary):
        for _ in range(50):
            candidate = perturb_number(primary, rng)
            if usable(candidate) and not is_descending_range(candidate):
                return candidate

    wh = wh_word(q["question"])
    n_words = len(primary.split())
    shape_ok = [
        p
        for p in pool
        if not re.search(r"\d", p["answer"])
        and p["answer"][:1].isupper() == primary[:1].isupper()
        and abs(len(p["answer"].split()) - n_words) <= 1
        and usable(p["answer"])
    ]
    for filt in (
        lambda p: p["title"] == q["title"] and p["wh"] == wh,
        lambda p: p["wh"] == wh,
        lambda p: True,
    ):
        candidates = sorted({p["answer"] for p in shape_ok if filt(p)})
        if candidates:
            return rng.choice(candidates)
    raise ValueError(f"No substitute found for question {q['question_id']}")


def make_conflicting(gold_text: str, gold_answers: list[str], substitute: str) -> str:
    variants = sorted({a for a in gold_answers if a in gold_text}, key=len, reverse=True)
    pattern = "|".join(re.escape(v) for v in variants)
    return re.sub(pattern, substitute, gold_text)


def contains_answer(text: str, answers: list[str]) -> bool:
    """True if the passage contains the answer, exactly or leniently (e.g. "defensins" for "β-defensins")."""
    norm = normalize_answer(text)
    return any(normalize_answer(a) in norm for a in answers) or matches_any(text, answers)


def assemble(items: list[tuple[str, str, str]], rng: random.Random) -> dict[str, Any]:
    """items: (passage_id, role, text). Shuffle and record roles by position."""
    items = items[:]
    rng.shuffle(items)
    return {
        "passages": [text for _, _, text in items],
        "passage_ids": [pid for pid, _, _ in items],
        "roles": [role for _, role, _ in items],
    }


def main() -> None:
    args = config_arg_parser(__doc__).parse_args()
    cfg = load_config(args.config)
    rcfg = cfg["retrieval"]
    passages = {p["passage_id"]: p for p in read_jsonl(PASSAGES_PATH)}
    questions = read_jsonl(QUESTIONS_PATH)
    collection = get_collection(cfg)
    k = rcfg["k"]

    df = pd.read_csv(ROOT / cfg["data"]["csv"], dtype=str, keep_default_na=False)
    answer_pool = [
        {"answer": answers[0]["text"], "title": title, "wh": wh_word(question)}
        for title, question, answers in zip(df["title"], df["question"], df["answers"].map(parse_answers))
        if answers and len(answers[0]["text"].split()) <= cfg["data"]["max_answer_words"]
    ]
    overrides = {}
    if OVERRIDES_PATH.exists():
        overrides = {k: v for k, v in json.loads(OVERRIDES_PATH.read_text()).items() if not k.startswith("_")}
    rows = []
    hits = []
    short = []
    for q in questions:
        rng = random.Random(f"{cfg['seed']}-{q['question_id']}")
        gold_id = q["gold_passage_id"]
        gold = passages[gold_id]
        ranked = search(collection, q["question"], rcfg["embed_model"], rcfg["candidate_pool"])

        related = [
            pid
            for pid in ranked
            if pid != gold_id and not (q["answerable"] and contains_answer(passages[pid]["text"], q["gold_answers"]))
        ]
        if len(related) < 4:
            short.append(q["question_id"])
        others = sorted(
            pid
            for pid, p in passages.items()
            if p["title"] != q["title"] and not (q["answerable"] and contains_answer(p["text"], q["gold_answers"]))
        )
        randoms = rng.sample(others, 3)

        def items(pids: list[str], role: str) -> list[tuple[str, str, str]]:
            return [(pid, role, passages[pid]["text"]) for pid in pids]

        gold_item = [(gold_id, "gold", gold["text"])]
        conditions: dict[str, dict[str, Any]] = {}

        if q["answerable"]:
            rank = ranked.index(gold_id) + 1 if gold_id in ranked else None
            hits.append(rank is not None and rank <= k)
            substitute = pick_substitute(q, gold["text"], answer_pool, rng, overrides)
            conflicting = make_conflicting(gold["text"], q["gold_answers"], substitute)
            conditions = {
                "C0": assemble(gold_item, rng),
                "C1": assemble(gold_item + items(randoms, "random"), rng),
                "C2": assemble(gold_item + items(related[:3], "related"), rng),
                "C3": assemble(gold_item + items(related[:3], "related") + items(randoms, "random"), rng),
                "C4": assemble(
                    gold_item + [(gold_id + "_conflict", "conflict", conflicting)] + items(related[:2], "related"),
                    rng,
                ),
                "C5": assemble(items(related[:4], "related"), rng),
            }
            extra = {"substitute_answer": substitute, "gold_retrieval_rank": rank}
        else:
            conditions = {"C5": assemble(gold_item + items(related[:3], "related"), rng)}
            extra = {"substitute_answer": None, "gold_retrieval_rank": None}

        for cond, ctx in conditions.items():
            rows.append(
                {
                    "context_id": f"{q['question_id']}_{cond}",
                    "question_id": q["question_id"],
                    "condition": cond,
                    **ctx,
                    **extra,
                }
            )

    write_jsonl(CONTEXTS_PATH, rows)
    print(f"Wrote {len(rows)} contexts for {len(questions)} questions")
    print(f"Retriever hit@{k} for gold passage (answerable): {sum(hits)}/{len(hits)} = {sum(hits)/len(hits):.2f}")
    print(f"Hand-reviewed substitutes applied: {sum(q['question_id'] in overrides for q in questions)}")
    if short:
        print(f"WARNING: fewer than 4 answer-free related passages for {len(short)} questions: {short}")


if __name__ == "__main__":
    main()
