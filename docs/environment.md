# Environment Record

Set up on October 29, 2026 (Phase 1). Update this file whenever a model, library, or machine changes.

## Machines

| Machine | Role | Specs |
|---|---|---|
| MacBook (macOS 27.0) | Index building and answer generation | Apple M4 Pro, 48 GB RAM; ~20 GB disk free |
| ThinkPad T490 (always on) | Gemini judging (planned) | Specs to be recorded |

All answer generation must run on the Mac, so outputs aren't affected by hardware differences.

## Software

| Component | Version |
|---|---|
| Python | 3.12.12 (managed by `uv`, pinned in `.python-version`) |
| Ollama | 0.34.1 |
| ollama (Python) | 0.6.3 |
| chromadb | 1.5.9 |
| ragas | 0.4.3 |
| langchain-community | 0.4.1 (**pinned**; 0.4.2 removed a module Ragas 0.4.3 imports) |
| langchain-google-genai | 4.4.2 |
| pandas | 3.1.0 |
| scipy | 1.18.1 |
| matplotlib | 3.11.2 |

Exact versions of every package are locked in `uv.lock`.

## Models

| Role | Model | Ollama ID | Details |
|---|---|---|---|
| Generator (primary) | `qwen3:8b` | `500a1f067a9f` | 8.2B params, Q4_K_M, 40,960 context; run with `think=False` |
| Generator (optional, scale comparison) | `qwen3.8:27b` | `22130167c4c2` | 17 GB |
| Embeddings | `nomic-embed-text:latest` | `0a109f422b47` | 768 dimensions |
| Judge | Gemini (exact version TBD) | — | Pin the exact version before the pilot |

## Smoke test (passed)

- All libraries import.
- `qwen3:8b` with `think=False`, temperature 0, seed 42 answered the Normandy test question with `"France."` and produced no thinking text.
- `nomic-embed-text` returned a 768-dimension embedding.
- Gemini: **not yet tested** (needs the API key in `.env`).

## Common commands

- Run Python in the project environment: `uv run python ...`
- Start Jupyter: `uv run jupyter lab`
- Add a package: `uv add <package>`
