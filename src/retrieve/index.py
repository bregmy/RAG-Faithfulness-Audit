"""Phase 3: Chroma index over the corpus, embedded locally with nomic-embed-text.

Run as a module to (re)build the index:  uv run python -m src.retrieve.index
"""

from __future__ import annotations

from typing import Any

import chromadb
import ollama

from src.common import PASSAGES_PATH, ROOT, config_arg_parser, load_config, read_jsonl

# nomic-embed-text expects task prefixes on its inputs.
DOC_PREFIX = "search_document: "
QUERY_PREFIX = "search_query: "


def get_collection(cfg: dict[str, Any]) -> chromadb.Collection:
    client = chromadb.PersistentClient(path=str(ROOT / cfg["retrieval"]["chroma_dir"]))
    return client.get_or_create_collection(
        cfg["retrieval"]["collection"], metadata={"hnsw:space": "cosine"}
    )


def embed(texts: list[str], model: str, prefix: str) -> list[list[float]]:
    return ollama.embed(model=model, input=[prefix + t for t in texts]).embeddings


def search(collection: chromadb.Collection, query: str, model: str, n: int) -> list[str]:
    """Return passage IDs ranked by similarity to the query."""
    result = collection.query(query_embeddings=embed([query], model, QUERY_PREFIX), n_results=n)
    return result["ids"][0]


def main() -> None:
    args = config_arg_parser(__doc__).parse_args()
    cfg = load_config(args.config)
    model = cfg["retrieval"]["embed_model"]
    passages = read_jsonl(PASSAGES_PATH)

    client = chromadb.PersistentClient(path=str(ROOT / cfg["retrieval"]["chroma_dir"]))
    try:
        client.delete_collection(cfg["retrieval"]["collection"])
    except Exception:
        pass
    collection = get_collection(cfg)

    batch = 64
    for i in range(0, len(passages), batch):
        chunk = passages[i : i + batch]
        collection.add(
            ids=[p["passage_id"] for p in chunk],
            documents=[p["text"] for p in chunk],
            metadatas=[{"title": p["title"]} for p in chunk],
            embeddings=embed([p["text"] for p in chunk], model, DOC_PREFIX),
        )
    print(f"Indexed {collection.count()} passages into {cfg['retrieval']['chroma_dir']}")


if __name__ == "__main__":
    main()
