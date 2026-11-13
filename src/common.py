"""Shared helpers: config loading, paths, JSONL I/O, text normalization."""

from __future__ import annotations

import argparse
import json
import re
import string
import tomllib
from pathlib import Path
from typing import Any, Iterable, Iterator

ROOT = Path(__file__).resolve().parent.parent

PASSAGES_PATH = ROOT / "data/corpus/passages.jsonl"
QUESTIONS_PATH = ROOT / "data/questions/questions.jsonl"
CONTEXTS_PATH = ROOT / "data/perturbations/contexts.jsonl"
PROMPTS_DIR = ROOT / "prompts"


def load_config(path: str | Path) -> dict[str, Any]:
    with open(ROOT / path, "rb") as f:
        return tomllib.load(f)


def config_arg_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--config", default="configs/pilot.toml")
    return parser


def run_dir(cfg: dict[str, Any]) -> Path:
    d = ROOT / "runs" / cfg["run_name"]
    d.mkdir(parents=True, exist_ok=True)
    return d


def run_contexts_path(cfg: dict[str, Any]) -> Path:
    """The run's own snapshot of the perturbed contexts, so rebuilding data/ never changes a finished run."""
    return run_dir(cfg) / "contexts.jsonl"


def judge_suffix(judge: str) -> str:
    """File-name suffix for a judge's outputs; the primary local judge keeps the original names."""
    return "" if judge == "local" else f"_{judge}"


def results_dir(cfg: dict[str, Any]) -> Path:
    d = ROOT / "results" / cfg["run_name"]
    d.mkdir(parents=True, exist_ok=True)
    return d


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return list(iter_jsonl(path))


def iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Skips lines that are not valid JSON, e.g. one cut off by a crash; that item is simply redone."""
    if path.exists():
        with open(path, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if line.strip():
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        print(f"Skipping unreadable line {n} in {path.name} (probably cut off by a crash)")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+b") as f:
        # After a crash mid-write the file may not end in a newline; start a fresh line so the
        # new record is not glued onto the broken one.
        if f.tell() > 0:
            f.seek(-1, 2)
            if f.read(1) != b"\n":
                f.write(b"\n")
        f.write((json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8"))


def normalize_answer(text: str) -> str:
    """SQuAD-style normalization: lowercase, drop punctuation, articles, extra spaces."""
    text = text.lower()
    text = "".join(ch for ch in text if ch not in set(string.punctuation))
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    return " ".join(text.split())
