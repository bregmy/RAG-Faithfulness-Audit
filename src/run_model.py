"""Run the whole evaluation for any Ollama model: generate -> judge -> summarize.

Everything except the model comes from the base config (configs/full.toml by default), and
every run reuses the base run's frozen contexts, so all models see identical passages.

Examples:
  uv run python -m src.run_model --model llama3.1:8b
  uv run python -m src.run_model --model mistral:7b --judge local --steps gen,judge,summarize
  uv run python -m src.run_model --model qwen3:8b --judge gemini,haiku --subset human,c4 --steps judge,summarize
  uv run python -m src.run_model --model deepseek-r1:32b --think on --num-predict 4096   # reasoning model
  uv run python -m src.run_model --model llama3.1:8b --name smoke_llama --questions 2 --limit 3   # quick test

Outputs:
  runs/<name>/generations.jsonl, judge_*.jsonl, scored*.csv, manifests
  results/<name>/summary*.csv / .md
The default <name> is the base run name ("full") for the base model, else "full_<model>".
"""

from __future__ import annotations

import argparse
import asyncio
import copy
import re
import shutil
import subprocess

import ollama

from src.analysis import summarize
from src.common import load_config, run_contexts_path, run_dir
from src.evaluate import run_judge
from src.generate import run_generation

STEPS = ("gen", "judge", "summarize")


def default_name(base_cfg: dict, model: str) -> str:
    if model == base_cfg["generator"]["model"]:
        return base_cfg["run_name"]
    return f"{base_cfg['run_name']}_{re.sub(r'[^A-Za-z0-9.]+', '-', model).strip('-')}"


def ensure_model(model: str) -> None:
    installed = {m.model for m in ollama.list().models}
    if model in installed or f"{model}:latest" in installed:
        return
    print(f"Pulling {model} ...", flush=True)
    subprocess.run(["ollama", "pull", model], check=True)


def parse_list(value: str, allowed: tuple[str, ...] | None = None) -> list[str]:
    items = [v.strip() for v in value.split(",") if v.strip()]
    if allowed:
        bad = [v for v in items if v not in allowed]
        if bad:
            raise SystemExit(f"Unknown value(s) {bad}; choose from {', '.join(allowed)}.")
    return items


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", required=True, help="Ollama model tag that answers the questions, e.g. llama3.1:8b")
    parser.add_argument("--name", help="run folder name (default: full_<model>, or full for the base model)")
    parser.add_argument("--config", default="configs/full.toml", help="base config")
    parser.add_argument("--judge", default="local",
                        help="comma-separated judges: local, gemini, haiku (see [judges.*] in the config), or none")
    parser.add_argument("--steps", default=",".join(STEPS), help=f"comma-separated: {', '.join(STEPS)}")
    parser.add_argument("--subset", default="all", help="answers to judge: all, human, c4 (comma-separated)")
    parser.add_argument("--think", choices=["on", "off"],
                        help="override the config's thinking setting (reasoning models such as deepseek-r1 need on: "
                             "with off their reasoning leaks into the answer text)")
    parser.add_argument("--num-predict", type=int,
                        help="max output tokens per answer, including thinking (config default 256)")
    parser.add_argument("--questions", type=int, help="only the first N answerable questions and 1 unanswerable (testing)")
    parser.add_argument("--limit", type=int, help="judge at most N items per phase (testing)")
    args = parser.parse_args()

    base = load_config(args.config)
    steps = parse_list(args.steps, STEPS)
    judges = [] if args.judge == "none" else parse_list(args.judge)

    cfg = copy.deepcopy(base)
    cfg["generator"]["model"] = args.model
    cfg["run_name"] = args.name or default_name(base, args.model)
    if args.think:
        cfg["generator"]["think"] = args.think == "on"
    if args.num_predict:
        cfg["generator"]["num_predict"] = args.num_predict
    if args.questions:
        cfg["experiment"]["max_answerable"] = args.questions
        cfg["experiment"]["max_unanswerable"] = 1

    if cfg["run_name"] != base["run_name"]:
        frozen = run_contexts_path(base)
        target = run_contexts_path(cfg)
        if not frozen.exists():
            raise SystemExit(f"{frozen} not found; run the base config first so its contexts are frozen.")
        if not target.exists():
            shutil.copyfile(frozen, target)
            print(f"Using the frozen contexts from {frozen}", flush=True)

    print(f"Run '{cfg['run_name']}': model={args.model}  steps={steps}  judges={judges or 'none'}  "
          f"subset={args.subset}  folder={run_dir(cfg)}", flush=True)

    if "gen" in steps:
        ensure_model(args.model)
        print("\n== Generation ==", flush=True)
        run_generation.run(cfg)

    if "judge" in steps:
        for judge in judges:
            print(f"\n== Judging with '{judge}' ==", flush=True)
            if judge == "local":
                ensure_model(cfg["judge"]["model"])
            asyncio.run(run_judge.run(cfg, judge, args.subset, args.limit))

    if "summarize" in steps:
        for judge in judges or ["local"]:
            print(f"\n== Summary ({judge} judge) ==", flush=True)
            summarize.run(cfg, judge)


if __name__ == "__main__":
    main()
