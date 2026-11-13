"""Write a reproducibility manifest (config, library versions, model digests) for a run."""

from __future__ import annotations

import datetime as dt
import importlib.metadata as md
import json
import platform
import subprocess
import sys
from pathlib import Path

import ollama

from src.common import ROOT

PACKAGES = ["ollama", "chromadb", "ragas", "langchain-community", "openai", "pandas", "scipy"]


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError:
        return None


def write_manifest(cfg: dict, out_dir: Path, name: str = "manifest_generation.json") -> None:
    models = {m.model: m.digest for m in ollama.list().models}
    manifest = {
        "created": dt.datetime.now().isoformat(timespec="seconds"),
        "config": cfg,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "packages": {p: md.version(p) for p in PACKAGES},
        "ollama_models": models,
        "git_commit": _git_commit(),
    }
    (out_dir / name).write_text(json.dumps(manifest, indent=2))
