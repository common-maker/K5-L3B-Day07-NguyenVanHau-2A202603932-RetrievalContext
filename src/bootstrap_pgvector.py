"""Standalone Day 6 PostgreSQL + pgvector bootstrapper for grader reproducibility.

Connects to Day 6's existing `rag_chunks` table when already populated, or initializes
the schema and embeds `data/nist_chunks.json` with `text-embedding-3-small` (1536 dims)
when run on a clean database. Never uses random/mock vectors.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any

import psycopg

from .config import PROJECT_ROOT, create_openai_client, estimate_embedding_cost_usd, load_settings
from .day6_bridge import KNOWN_EMBEDDING_DIMS, Day6PgVectorClient, _to_pgvector_literal


def create_day6_schema(database_url: str, dimensions: int = 1536) -> None:
    """Create the exact `rag_chunks` schema and indexes used in Day 6."""
    if dimensions <= 0:
        raise ValueError("dimensions must be positive.")
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS rag_chunks (
                    strategy TEXT NOT NULL,
                    chunk_id TEXT NOT NULL,
                    document_id TEXT NOT NULL,
                    source TEXT NOT NULL,
                    page INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    document_type TEXT NOT NULL,
                    section TEXT NOT NULL,
                    content TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    metadata JSONB NOT NULL,
                    embedding vector({dimensions}) NOT NULL,
                    PRIMARY KEY (strategy, chunk_id)
                );
                """
            )
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_rag_chunks_strategy_doc
                ON rag_chunks (strategy, document_id);
                """
            )
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_rag_chunks_strategy_filters
                ON rag_chunks (strategy, year, document_type, section);
                """
            )
        conn.commit()


def build_upsert_rows(
    strategy: str,
    chunks: list[dict[str, Any]],
    vectors: list[list[float]],
    dimensions: int = 1536,
) -> list[tuple[Any, ...]]:
    """Validate chunk/vector alignment and format parameterized PostgreSQL rows."""
    if not strategy.strip():
        raise ValueError("strategy must not be empty.")
    if not chunks:
        raise ValueError("chunks must not be empty.")
    if len(chunks) != len(vectors):
        raise ValueError(f"chunks ({len(chunks)}) and vectors ({len(vectors)}) length mismatch.")

    rows: list[tuple[Any, ...]] = []
    for idx, (chunk, vec) in enumerate(zip(chunks, vectors)):
        if len(vec) != dimensions:
            raise ValueError(f"Vector {idx} has {len(vec)} dims; expected {dimensions}.")
        meta = dict(chunk.get("metadata", {}))
        rows.append(
            (
                strategy,
                chunk["id"],
                chunk["source_id"],
                chunk["source"],
                int(chunk["page"]),
                int(meta["year"]),
                str(meta["document_type"]),
                str(meta["section"]),
                chunk["text"],
                hashlib.sha256(chunk["text"].encode("utf-8")).hexdigest(),
                json.dumps(meta, ensure_ascii=False),
                _to_pgvector_literal(vec),
            )
        )
    return rows


def embed_documents_openai(
    texts: list[str],
    *,
    api_key: str,
    model_name: str = "text-embedding-3-small",
    expected_dimensions: int = 1536,
    batch_size: int = 64,
) -> tuple[list[list[float]], int, float]:
    """Embed chunk texts in batches via real OpenAI Embeddings API."""
    if not api_key.strip():
        raise RuntimeError("OPENAI_API_KEY is missing; real embeddings require a valid key.")
    if model_name not in KNOWN_EMBEDDING_DIMS or KNOWN_EMBEDDING_DIMS[model_name] != expected_dimensions:
        raise ValueError(f"Incompatible embedding model '{model_name}' for {expected_dimensions} dims.")

    client = create_openai_client(api_key)
    vectors: list[list[float]] = []
    prompt_tokens = 0
    t0 = time.perf_counter()

    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        resp = client.embeddings.create(model=model_name, input=batch)
        if resp.usage and resp.usage.prompt_tokens is not None:
            prompt_tokens += int(resp.usage.prompt_tokens)
        ordered = sorted(resp.data, key=lambda item: item.index)
        for item in ordered:
            vec = list(item.embedding)
            if len(vec) != expected_dimensions:
                raise RuntimeError(f"Expected {expected_dimensions} dims, got {len(vec)}.")
            vectors.append(vec)

    elapsed = round(time.perf_counter() - t0, 3)
    return vectors, prompt_tokens, elapsed


def upsert_chunks(
    database_url: str,
    strategy: str,
    chunks: list[dict[str, Any]],
    vectors: list[list[float]],
    dimensions: int = 1536,
) -> None:
    """Idempotently upsert chunks + embeddings into `rag_chunks`."""
    rows = build_upsert_rows(strategy, chunks, vectors, dimensions=dimensions)
    chunk_ids = [c["id"] for c in chunks]
    with psycopg.connect(database_url) as conn:
        with conn.transaction():
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO rag_chunks (
                        strategy, chunk_id, document_id, source, page,
                        year, document_type, section, content, content_hash,
                        metadata, embedding
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::vector)
                    ON CONFLICT (strategy, chunk_id) DO UPDATE SET
                        document_id = EXCLUDED.document_id,
                        source = EXCLUDED.source,
                        page = EXCLUDED.page,
                        year = EXCLUDED.year,
                        document_type = EXCLUDED.document_type,
                        section = EXCLUDED.section,
                        content = EXCLUDED.content,
                        content_hash = EXCLUDED.content_hash,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding;
                    """,
                    rows,
                )
                cur.execute(
                    """
                    DELETE FROM rag_chunks
                    WHERE strategy = %s AND NOT (chunk_id = ANY(%s));
                    """,
                    (strategy, chunk_ids),
                )


def bootstrap_pgvector(
    *,
    chunks_path: Path,
    strategy: str = "B",
    check_only: bool = False,
    force_reembed: bool = False,
) -> dict[str, Any]:
    """Verify or populate Day 6 `rag_chunks` in PostgreSQL + pgvector."""
    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    settings = load_settings(require_db=True, require_openai=False)
    create_day6_schema(settings.database_url, dimensions=settings.embedding_dimensions)

    client = Day6PgVectorClient(
        settings.database_url,
        dimensions=settings.embedding_dimensions,
        strategy=strategy,
    )
    health = client.health_check()
    existing_ids = {c["id"] for c in client.fetch_chunks()}
    expected_ids = {c["id"] for c in chunks}

    if existing_ids == expected_ids and not force_reembed:
        return {
            "status": "already_populated",
            "health": health,
            "expected_chunks": len(chunks),
            "embed_tokens": 0,
            "embed_cost_usd": 0.0,
        }

    if check_only:
        raise RuntimeError(
            f"pgvector table missing expected chunks: found {len(existing_ids)}, expected {len(expected_ids)}."
        )

    settings_openai = load_settings(require_db=True, require_openai=True)
    vectors, tokens, embed_seconds = embed_documents_openai(
        [c["text"] for c in chunks],
        api_key=settings_openai.openai_api_key,
        model_name=settings_openai.embedding_model,
        expected_dimensions=settings_openai.embedding_dimensions,
    )
    upsert_chunks(
        settings_openai.database_url,
        strategy,
        chunks,
        vectors,
        dimensions=settings_openai.embedding_dimensions,
    )
    cost = round(estimate_embedding_cost_usd(settings_openai.embedding_model, tokens), 6)
    return {
        "status": "bootstrapped",
        "health": client.health_check(),
        "expected_chunks": len(chunks),
        "embed_tokens": tokens,
        "embed_seconds": embed_seconds,
        "embed_cost_usd": cost,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify or bootstrap Day 6 pgvector chunks for Day 7.")
    parser.add_argument("--chunks", type=Path, default=PROJECT_ROOT / "data" / "nist_chunks.json")
    parser.add_argument("--strategy", default="B")
    parser.add_argument("--check", action="store_true", help="Fail if DB does not already hold all chunks.")
    parser.add_argument("--force-reembed", action="store_true", help="Re-embed and overwrite chunks.")
    args = parser.parse_args()

    result = bootstrap_pgvector(
        chunks_path=args.chunks,
        strategy=args.strategy,
        check_only=args.check,
        force_reembed=args.force_reembed,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
