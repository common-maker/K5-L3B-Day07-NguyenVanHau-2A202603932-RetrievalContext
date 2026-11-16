"""Bridge to Day 6 PostgreSQL/pgvector index, OpenAI embeddings, and chunk export."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

import psycopg
from openai import OpenAI

from .config import (
    ALLOWED_FILTERS,
    DEFAULT_DAY6_ROOT,
    estimate_embedding_cost_usd,
)

KNOWN_EMBEDDING_DIMS: dict[str, int] = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
    "text-embedding-ada-002": 1536,
}


def _to_pgvector_literal(vector: list[float]) -> str:
    return "[" + ",".join(f"{float(v):.8f}" for v in vector) + "]"


class OpenAIQueryEmbedder:
    """Real OpenAI query embedder compatible with the Day 6 document vector index."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "text-embedding-3-small",
        expected_dimensions: int = 1536,
    ) -> None:
        if not api_key.strip():
            raise RuntimeError("OPENAI_API_KEY is empty; real query embedding requires a valid key.")
        if model_name not in KNOWN_EMBEDDING_DIMS:
            raise ValueError(f"Unsupported embedding model '{model_name}'.")
        if KNOWN_EMBEDDING_DIMS[model_name] != expected_dimensions:
            raise ValueError(
                f"Dimension mismatch for {model_name}: expected {expected_dimensions}, "
                f"model outputs {KNOWN_EMBEDDING_DIMS[model_name]}."
            )
        self.model_name = model_name
        self.dimensions = expected_dimensions
        self.client = OpenAI(api_key=api_key)
        self.total_prompt_tokens = 0
        self.total_requests = 0
        self.total_elapsed_seconds = 0.0

    @property
    def estimated_cost_usd(self) -> float:
        return estimate_embedding_cost_usd(self.model_name, self.total_prompt_tokens)

    def embed_query(self, query: str) -> list[float]:
        """Embed a single non-empty query string and verify dimensionality."""
        if not query.strip():
            raise ValueError("Query string must not be empty.")
        t0 = time.perf_counter()
        response = self.client.embeddings.create(model=self.model_name, input=[query])
        self.total_elapsed_seconds += time.perf_counter() - t0
        self.total_requests += 1
        if response.usage and response.usage.prompt_tokens is not None:
            self.total_prompt_tokens += int(response.usage.prompt_tokens)
        vec = list(response.data[0].embedding)
        if len(vec) != self.dimensions:
            raise RuntimeError(f"Expected {self.dimensions} dims, got {len(vec)}.")
        return vec


class Day6PgVectorClient:
    """Read-only client for Day 6's `rag_chunks` PostgreSQL + pgvector table."""

    def __init__(self, database_url: str, dimensions: int = 1536, strategy: str = "B") -> None:
        if not database_url.strip():
            raise ValueError("database_url must not be empty.")
        self.database_url = database_url
        self.dimensions = dimensions
        self.strategy = strategy

    def health_check(self) -> dict[str, Any]:
        """Verify PostgreSQL version, pgvector extension, and stored chunk count."""
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                pg_version = cur.fetchone()[0]
                cur.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector';")
                row = cur.fetchone()
                if not row:
                    raise RuntimeError("pgvector extension is not installed in target database.")
                pgvector_version = row[0]
                cur.execute(
                    "SELECT COUNT(*) FROM rag_chunks WHERE strategy = %s;",
                    (self.strategy,),
                )
                chunk_count = int(cur.fetchone()[0])
        return {
            "postgres_version": pg_version,
            "pgvector_version": pgvector_version,
            "strategy": self.strategy,
            "chunk_count": chunk_count,
        }

    def fetch_chunks(self) -> list[dict[str, Any]]:
        """Export Day 6 chunks from PostgreSQL into Day 7 JSON chunk schema."""
        sql = """
            SELECT chunk_id, document_id, source, page, content, metadata
            FROM rag_chunks
            WHERE strategy = %s
            ORDER BY document_id ASC, page ASC, chunk_id ASC;
        """
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (self.strategy,))
                rows = cur.fetchall()
        return [
            {
                "id": chunk_id,
                "source_id": document_id,
                "source": source,
                "page": int(page),
                "text": content,
                "metadata": dict(metadata),
            }
            for chunk_id, document_id, source, page, content, metadata in rows
        ]

    def search_vector(
        self,
        query_vector: list[float],
        *,
        top_k: int = 3,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Query exact cosine distance `<=>` in Day 6's `rag_chunks` table."""
        if len(query_vector) != self.dimensions:
            raise ValueError(f"Query vector has {len(query_vector)} dims; expected {self.dimensions}.")
        if top_k < 1:
            raise ValueError("top_k must be >= 1.")

        where_clauses = ["strategy = %s"]
        filter_params: list[Any] = [self.strategy]
        if filters:
            for key, raw_val in filters.items():
                if raw_val is None:
                    continue
                if key not in ALLOWED_FILTERS:
                    raise ValueError(
                        f"Disallowed filter field '{key}'. Allowed: {sorted(ALLOWED_FILTERS)}"
                    )
                typed_val = ALLOWED_FILTERS[key](raw_val)
                where_clauses.append(f"{key} = %s")
                filter_params.append(typed_val)

        vec_literal = _to_pgvector_literal(query_vector)
        sql = f"""
            SELECT
                chunk_id,
                document_id,
                source,
                page,
                content,
                metadata,
                (embedding <=> %s::vector) AS cosine_distance
            FROM rag_chunks
            WHERE {" AND ".join(where_clauses)}
            ORDER BY embedding <=> %s::vector ASC, chunk_id ASC
            LIMIT %s;
        """
        params = [vec_literal, *filter_params, vec_literal, top_k]
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()

        results: list[dict[str, Any]] = []
        for rank, (chunk_id, document_id, source, page, content, metadata, dist) in enumerate(rows, start=1):
            dist_f = float(dist)
            results.append(
                {
                    "id": chunk_id,
                    "source_id": document_id,
                    "source": source,
                    "page": int(page),
                    "text": content,
                    "metadata": dict(metadata),
                    "score": round(1.0 - dist_f, 6),
                    "cosine_distance": round(dist_f, 6),
                    "rank": rank,
                }
            )
        return results


def _load_day6_module(module_name: str, file_path: Path) -> Any:
    """Load a Day 6 module without colliding with Day 7's `src` package name."""
    import importlib.util

    pkg_name = "_day6_src"
    if pkg_name not in sys.modules:
        pkg_spec = importlib.util.spec_from_file_location(pkg_name, file_path.parent / "__init__.py")
        assert pkg_spec and pkg_spec.loader
        pkg_mod = importlib.util.module_from_spec(pkg_spec)
        pkg_mod.__path__ = [str(file_path.parent)]
        sys.modules[pkg_name] = pkg_mod

    full_name = f"{pkg_name}.{module_name}"
    if full_name in sys.modules:
        return sys.modules[full_name]
    spec = importlib.util.spec_from_file_location(full_name, file_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[full_name] = mod
    spec.loader.exec_module(mod)
    return mod


def export_day6_chunks_from_pdfs(
    day6_root: Path = DEFAULT_DAY6_ROOT,
    max_size: int = 1000,
) -> list[dict[str, Any]]:
    """Deterministically reproduce Day 6 Strategy B chunks directly from Day 6 PDFs."""
    src_dir = day6_root / "starter" / "src"
    if not src_dir.exists():
        raise FileNotFoundError(f"Day 6 starter/src directory not found at {src_dir}")

    _load_day6_module("models", src_dir / "models.py")
    ingestion_mod = _load_day6_module("ingestion", src_dir / "ingestion.py")
    chunking_mod = _load_day6_module("chunking", src_dir / "chunking.py")

    pages, errors = ingestion_mod.load_corpus_from_manifest(day6_root / "data" / "manifest.json", day6_root)
    if errors:
        raise RuntimeError(f"Day 6 ingestion returned errors: {errors}")

    chunks: list[dict[str, Any]] = []
    for page in pages:
        for chunk in chunking_mod.by_paragraph(page, max_size=max_size):
            chunks.append(
                {
                    "id": chunk.chunk_id,
                    "source_id": chunk.document_id,
                    "source": chunk.source,
                    "page": int(chunk.page),
                    "text": chunk.text,
                    "metadata": dict(chunk.metadata),
                }
            )
    chunks.sort(key=lambda c: (c["source_id"], c["page"], c["id"]))
    return chunks


def write_json(path: Path, data: Any) -> None:
    """Write UTF-8 formatted JSON ensuring parent directories exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
