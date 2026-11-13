"""Phase 5: generate answers with the local model for every context x mitigation x repeat.

Also generates one closed-book (no context) answer per answerable question, to tell
memorized answers apart from grounded ones.

Output: runs/<run_name>/generations.jsonl (appended; already-finished items are skipped,
so the script can be stopped and resumed).
"""

from __future__ import annotations

import shutil
import time

import ollama

from src.common import (
    CONTEXTS_PATH,
    PROMPTS_DIR,
    QUESTIONS_PATH,
    append_jsonl,
    config_arg_parser,
    load_config,
    read_jsonl,
    run_contexts_path,
    run_dir,
)
from src.manifest import write_manifest

PROMPT_FILES = {
    "M0": "M0_baseline.txt",
    "M1": "M1_strict_refusal.txt",
    "M2": "M2_context_faithful.txt",
    "closed_book": "closed_book.txt",
}


def select_questions(cfg: dict) -> list[dict]:
    ecfg = cfg["experiment"]
    questions = read_jsonl(QUESTIONS_PATH)
    answerable = [q for q in questions if q["answerable"]][: ecfg["max_answerable"]]
    unanswerable = [q for q in questions if not q["answerable"]][: ecfg["max_unanswerable"]]
    return answerable + unanswerable


def format_context(passages: list[str], mitigation: str) -> str:
    if mitigation == "M2":
        return " ".join(p.replace('"', "'") for p in passages)
    return "\n\n".join(f"[{i}] {p}" for i, p in enumerate(passages, 1))


def build_prompt(template: str, question: str, passages: list[str], mitigation: str) -> str:
    return template.format(
        context=format_context(passages, mitigation),
        question=question,
        question_stripped=question.rstrip(" ?"),
    )


def supports_thinking(model: str) -> bool:
    return "thinking" in (ollama.show(model).capabilities or [])


def generate(cfg: dict, prompt: str, seed: int, think: bool | None) -> dict:
    gcfg = cfg["generator"]
    start = time.time()
    response = ollama.generate(
        model=gcfg["model"],
        prompt=prompt,
        think=think,
        options={
            "temperature": gcfg["temperature"],
            "seed": seed,
            "num_ctx": gcfg["num_ctx"],
            "num_predict": gcfg["num_predict"],
        },
    )
    record = {
        "response": response.response.strip(),
        "latency_s": round(time.time() - start, 2),
        "prompt_tokens": response.prompt_eval_count,
        "output_tokens": response.eval_count,
    }
    if response.thinking:
        record["thinking"] = response.thinking.strip()
    if response.done_reason == "length":
        record["truncated"] = True
    return record


def run(cfg: dict) -> None:
    out_dir = run_dir(cfg)
    out_path = out_dir / "generations.jsonl"
    write_manifest(cfg, out_dir)

    templates = {k: (PROMPTS_DIR / v).read_text() for k, v in PROMPT_FILES.items()}
    questions = select_questions(cfg)
    qids = {q["question_id"] for q in questions}
    qmap = {q["question_id"]: q for q in questions}
    ecfg = cfg["experiment"]
    snapshot = run_contexts_path(cfg)
    if not snapshot.exists():
        shutil.copyfile(CONTEXTS_PATH, snapshot)
        print(f"Saved a snapshot of the contexts to {snapshot}")
    contexts = [
        c for c in read_jsonl(snapshot) if c["question_id"] in qids and c["condition"] in ecfg["conditions"]
    ]

    jobs = []
    for q in questions:
        if q["answerable"]:
            jobs.append({"gen_id": f"{q['question_id']}_closed_book_r0", "question_id": q["question_id"],
                         "context_id": None, "condition": "closed_book", "mitigation": "closed_book",
                         "repeat": 0, "passages": []})
    for c in contexts:
        for m in ecfg["mitigations"]:
            for r in range(ecfg["repeats"]):
                jobs.append({"gen_id": f"{c['context_id']}_{m}_r{r}", "question_id": c["question_id"],
                             "context_id": c["context_id"], "condition": c["condition"], "mitigation": m,
                             "repeat": r, "passages": c["passages"]})

    done = {row["gen_id"] for row in read_jsonl(out_path) if "error" not in row}
    todo = [j for j in jobs if j["gen_id"] not in done]
    print(f"{len(jobs)} generations total, {len(done)} already done, {len(todo)} to run", flush=True)

    # Models without a thinking mode reject the think flag, so it is only sent to those that have one.
    think = cfg["generator"]["think"] if supports_thinking(cfg["generator"]["model"]) else None
    for i, job in enumerate(todo, 1):
        question = qmap[job["question_id"]]["question"]
        prompt = build_prompt(templates[job["mitigation"]], question, job["passages"], job["mitigation"])
        seed = cfg["seed"] + job["repeat"]
        record = {k: v for k, v in job.items() if k != "passages"}
        record.update({"question": question, "model": cfg["generator"]["model"], "seed": seed})
        try:
            record.update(generate(cfg, prompt, seed, think))
        except Exception as exc:
            record["error"] = repr(exc)
        append_jsonl(out_path, record)
        if i % 10 == 0 or i == len(todo):
            print(f"  {i}/{len(todo)}  last: [{job['condition']}/{job['mitigation']}] "
                  f"{record.get('response', record.get('error'))[:80]!r}", flush=True)


def main() -> None:
    args = config_arg_parser(__doc__).parse_args()
    run(load_config(args.config))


if __name__ == "__main__":
    main()
