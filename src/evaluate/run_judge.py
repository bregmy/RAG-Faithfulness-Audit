"""Grade generated answers with a judge model.

Phase 1, per passage:  a yes/no judgment of whether each passage helps answer the question.
                       Scored once per unique (question, passage) pair and reused across
                       conditions; summarize.py turns it into context precision (share of
                       relevant passages in a context). This replaces Ragas ContextRelevance,
                       which scored 1.0 for every context in the pilot, even with 6 distractors.
Phase 2, per answer:   Ragas faithfulness (skipped for refusals) and answer relevancy.
Closed-book answers have no passages and are not judged.

Judges: "local" is the [judge] section of the config (Ollama). Other names refer to
[judges.<name>] sections (Gemini through its OpenAI-compatible API, Claude through Anthropic's
API; keys from the environment or .env).

Outputs (appended; finished items are skipped, so the script can be stopped and resumed):
  runs/<run_name>/judge_passages[_<judge>].jsonl
  runs/<run_name>/judge_answers[_<judge>].jsonl

Subsets (--subset, comma-separated): all, human (the answers in labels/validation_key.csv,
only meaningful for the run that was labeled), c4 (every C4 answer).
"""

from __future__ import annotations

import asyncio
import os
import time
import warnings

import ollama
import pandas as pd
from anthropic import Anthropic, AsyncAnthropic
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI
from ragas.embeddings import embedding_factory
from ragas.llms import llm_factory
from ragas.metrics.collections import AnswerRelevancy, Faithfulness

from src.common import (
    ROOT,
    append_jsonl,
    config_arg_parser,
    judge_suffix,
    load_config,
    read_jsonl,
    run_contexts_path,
    run_dir,
)
from src.evaluate.rules import is_refusal, strip_framing
from src.manifest import write_manifest

warnings.filterwarnings("ignore")
load_dotenv(ROOT / ".env", override=True)

HUMAN_KEY = ROOT / "labels/validation_key.csv"
SUBSETS = ("all", "human", "c4")

PASSAGE_PROMPT = """You are grading a search system. Decide whether the passage contains information that helps answer the question. Judge only relevance, not whether the information is true.

Question: {question}

Passage: {passage}

Reply with exactly one word: yes or no."""


def judge_settings(cfg: dict, judge: str) -> dict:
    if judge == "local":
        return {**cfg["judge"], "local": True}
    try:
        settings = dict(cfg["judges"][judge])
    except KeyError:
        raise SystemExit(f"No [judges.{judge}] section in the config; add one or use --judge local.")
    key = os.environ.get(settings["api_key_env"])
    if not key:
        raise SystemExit(f"{settings['api_key_env']} is not set; add it to {ROOT / '.env'}.")
    return {**settings, "api_key": key, "local": False}


def build_metrics(cfg: dict, jcfg: dict):
    provider = jcfg.get("provider", "openai")
    if provider == "anthropic":
        client = AsyncAnthropic(api_key=jcfg["api_key"], max_retries=8)
    else:
        client = AsyncOpenAI(base_url=jcfg["base_url"], api_key=jcfg.get("api_key", "ollama"), max_retries=8)
    extra = {k: jcfg[k] for k in ("temperature", "reasoning_effort") if jcfg.get(k) is not None}
    llm = llm_factory(jcfg["model"], provider=provider, client=client, max_tokens=jcfg["max_tokens"], **extra)
    if "temperature" not in jcfg:
        # Ragas otherwise adds its own sampling defaults, which some APIs reject.
        llm.model_args.pop("temperature", None)
        llm.model_args.pop("top_p", None)
    embed_client = AsyncOpenAI(base_url=cfg["judge"]["base_url"], api_key="ollama")
    embeddings = embedding_factory("openai", model=cfg["judge"]["embed_model"], client=embed_client)
    return Faithfulness(llm=llm), AnswerRelevancy(llm=llm, embeddings=embeddings)


async def score(metric, **kwargs) -> tuple[float | None, str | None]:
    try:
        result = await metric.ascore(**kwargs)
        value = result.value
        return (None if value is None or value != value else float(value)), None
    except Exception as exc:
        return None, repr(exc)[:300]


def make_passage_judge(jcfg: dict):
    if jcfg["local"]:
        def ask(prompt: str) -> str:
            response = ollama.chat(
                model=jcfg["model"],
                messages=[{"role": "user", "content": prompt}],
                think=False,
                options={"temperature": jcfg["temperature"], "num_predict": 8},
            )
            return response.message.content
    elif jcfg.get("provider") == "anthropic":
        client = Anthropic(api_key=jcfg["api_key"], max_retries=8)

        def ask(prompt: str) -> str:
            response = client.messages.create(
                model=jcfg["model"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=16,
            )
            return "".join(block.text for block in response.content if block.type == "text")
    else:
        client = OpenAI(base_url=jcfg["base_url"], api_key=jcfg["api_key"], max_retries=8)
        extra = {"reasoning_effort": jcfg["reasoning_effort"]} if jcfg.get("reasoning_effort") else {}

        def ask(prompt: str) -> str:
            response = client.chat.completions.create(
                model=jcfg["model"],
                messages=[{"role": "user", "content": prompt}],
                temperature=jcfg["temperature"],
                # Gemini can spend hidden reasoning tokens even with reasoning_effort="none".
                max_tokens=512,
                **extra,
            )
            return response.choices[0].message.content or ""

    def judge_passage(question: str, passage: str) -> tuple[bool | None, str]:
        raw = ask(PASSAGE_PROMPT.format(question=question, passage=passage)).strip()
        word = raw.lower().lstrip("*\"' ")
        if word.startswith("yes"):
            return True, raw
        if word.startswith("no"):
            return False, raw
        return None, raw

    return judge_passage


def fmt_time(seconds: float) -> str:
    h, rem = divmod(int(seconds), 3600)
    return f"{h}h{rem // 60:02d}m"


def run_passage_phase(jcfg: dict, generations: list[dict], contexts: dict, out_path, limit: int | None) -> None:
    pairs = {}
    for gen in generations:
        ctx = contexts[gen["context_id"]]
        for pid, text in zip(ctx["passage_ids"], ctx["passages"]):
            pairs.setdefault(f"{gen['question_id']}|{pid}", (gen["question"], text))

    done = {r["pair_id"] for r in read_jsonl(out_path) if r.get("relevant") is not None}
    todo = [(k, v) for k, v in pairs.items() if k not in done][:limit]
    print(f"Phase 1 (passage relevance): {len(pairs)} pairs, {len(done)} done, {len(todo)} remaining", flush=True)

    judge_passage = make_passage_judge(jcfg)
    start = time.time()
    for i, (pair_id, (question, text)) in enumerate(todo, 1):
        try:
            relevant, raw = judge_passage(question, text)
            error = None if relevant is not None else "unparseable"
        except Exception as exc:
            relevant, raw, error = None, "", repr(exc)[:300]
        append_jsonl(out_path, {"pair_id": pair_id, "relevant": relevant, "raw": raw, "error": error})
        if i % 25 == 0 or i == len(todo):
            elapsed = time.time() - start
            print(
                f"  [{i}/{len(todo)}] last={relevant}  elapsed={fmt_time(elapsed)}  "
                f"ETA={fmt_time(elapsed / i * (len(todo) - i))}",
                flush=True,
            )


async def run_answer_phase(
    cfg: dict, jcfg: dict, generations: list[dict], contexts: dict, out_path, limit: int | None
) -> None:
    faithfulness, answer_relevancy = build_metrics(cfg, jcfg)
    done = {r["gen_id"] for r in read_jsonl(out_path) if not r.get("errors")}
    todo = [g for g in generations if g["gen_id"] not in done][:limit]
    print(f"Phase 2 (answers): {len(generations)} answers, {len(done)} done, {len(todo)} remaining", flush=True)

    start = time.time()
    for i, gen in enumerate(todo, 1):
        ctx = contexts[gen["context_id"]]
        question, response = gen["question"], strip_framing(gen["response"])

        if not response.strip():
            # e.g. a reasoning model that used its whole token budget thinking; nothing to grade
            append_jsonl(out_path, {"gen_id": gen["gen_id"], "judged_response": "", "refused": False, "empty": True,
                                    "faithfulness": None, "answer_relevancy": None, "judge_model": jcfg["model"],
                                    "errors": None})
            print(f"  [{i}/{len(todo)}] {gen['condition']}/{gen['mitigation']}  empty answer, skipped", flush=True)
            continue

        refused = is_refusal(response)
        errors = {}
        if refused:
            faith = None
        else:
            faith, err = await score(
                faithfulness, user_input=question, response=response, retrieved_contexts=ctx["passages"]
            )
            if err:
                errors["faithfulness"] = err
        relevancy, err = await score(answer_relevancy, user_input=question, response=response)
        if err:
            errors["answer_relevancy"] = err

        append_jsonl(
            out_path,
            {
                "gen_id": gen["gen_id"],
                "judged_response": response,
                "refused": refused,
                "faithfulness": faith,
                "answer_relevancy": relevancy,
                "judge_model": jcfg["model"],
                "errors": errors or None,
            },
        )

        elapsed = time.time() - start
        faith_txt = "skip (refusal)" if refused else (f"{faith:.2f}" if faith is not None else "ERR")
        rel_txt = f"{relevancy:.2f}" if relevancy is not None else "ERR"
        print(
            f"  [{i}/{len(todo)}] {gen['condition']}/{gen['mitigation']}  faithfulness={faith_txt}  "
            f"answer_relevancy={rel_txt}  elapsed={fmt_time(elapsed)}  ETA={fmt_time(elapsed / i * (len(todo) - i))}",
            flush=True,
        )
        if errors:
            print(f"    errors: {errors}", flush=True)


def select_generations(generations: list[dict], subset: str) -> list[dict]:
    parts = {p.strip() for p in subset.split(",") if p.strip()}
    unknown = parts - set(SUBSETS)
    if unknown:
        raise SystemExit(f"Unknown subset(s) {sorted(unknown)}; choose from {', '.join(SUBSETS)}.")
    if "all" in parts:
        return generations
    keep = set()
    if "human" in parts:
        keep |= set(pd.read_csv(HUMAN_KEY)["gen_id"])
    if "c4" in parts:
        keep |= {g["gen_id"] for g in generations if g["condition"] == "C4"}
    return [g for g in generations if g["gen_id"] in keep]


async def run(cfg: dict, judge: str = "local", subset: str = "all", limit: int | None = None) -> None:
    jcfg = judge_settings(cfg, judge)
    out_dir = run_dir(cfg)
    suffix = judge_suffix(judge)
    write_manifest({**cfg, "active_judge": judge, "subset": subset}, out_dir, name=f"manifest_judge{suffix}.json")

    contexts = {c["context_id"]: c for c in read_jsonl(run_contexts_path(cfg))}
    generations = [
        g for g in read_jsonl(out_dir / "generations.jsonl") if "error" not in g and g["condition"] != "closed_book"
    ]
    generations = select_generations(generations, subset)
    print(f"Run: {cfg['run_name']} · judge: {judge} ({jcfg['model']}) · subset: {subset} "
          f"· {len(generations)} answers", flush=True)

    run_passage_phase(jcfg, generations, contexts, out_dir / f"judge_passages{suffix}.jsonl", limit)
    await run_answer_phase(cfg, jcfg, generations, contexts, out_dir / f"judge_answers{suffix}.jsonl", limit)
    print("Done.", flush=True)


async def main() -> None:
    parser = config_arg_parser(__doc__)
    parser.add_argument("--judge", default="local", help="local, or a [judges.<name>] section such as gemini or haiku")
    parser.add_argument("--subset", default="all", help=f"comma-separated: {', '.join(SUBSETS)}")
    parser.add_argument("--limit", type=int, default=None, help="grade at most this many items per phase (for testing)")
    args = parser.parse_args()
    await run(load_config(args.config), args.judge, args.subset, args.limit)


if __name__ == "__main__":
    asyncio.run(main())
