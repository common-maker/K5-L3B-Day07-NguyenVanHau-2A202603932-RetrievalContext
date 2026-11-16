"""PostgreSQL pgvector store and hybrid/BM25 retrievers for the Advanced Multimodal Challenge.

Uses a completely separate table (`rag_multimodal`) from Core Lab (`rag_chunks`).
"""
from __future__ import annotations

import json
import math
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any

import psycopg

from src.bootstrap_pgvector import embed_documents_openai
from src.config import estimate_embedding_cost_usd, load_settings
from src.day6_bridge import OpenAIQueryEmbedder

from advanced.ingest import CHUNKS_PATH, DATA_DIR

STORE_STATS_PATH = DATA_DIR / "store_stats.json"
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:[.\-_/][A-Za-z0-9]+)*")


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for tok in TOKEN_RE.findall(text.lower()):
        tokens.append(tok)
        if any(sep in tok for sep in (".", "-", "_", "/")):
            for sub in re.split(r"[.\-_/]+", tok):
                if sub and sub != tok:
                    tokens.append(sub)
    return tokens


def _vector_literal(vec: list[float]) -> str:
    return "[" + ",".join(f"{x:.8f}" for x in vec) + "]"


def ensure_multimodal_schema(database_url: str, dimensions: int = 1536) -> None:
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS rag_multimodal (
                    chunk_id TEXT PRIMARY KEY,
                    doc_id TEXT NOT NULL,
                    page INTEGER NOT NULL,
                    section TEXT NOT NULL,
                    modality TEXT NOT NULL,
                    label TEXT NOT NULL,
                    bbox_pt JSONB,
                    bbox_norm JSONB,
                    crop_path TEXT,
                    render_path TEXT NOT NULL,
                    content TEXT NOT NULL,
                    embedding vector({dimensions}) NOT NULL
                );
                """
            )
            cur.execute("CREATE INDEX IF NOT EXISTS idx_rag_multimodal_page ON rag_multimodal (page);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_rag_multimodal_modality ON rag_multimodal (modality);")
        conn.commit()


def ingest_to_pgvector(chunks_path: Path = CHUNKS_PATH) -> dict[str, Any]:
    settings = load_settings(require_db=True, require_openai=True)
    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    ensure_multimodal_schema(settings.database_url, settings.embedding_dimensions)

    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT chunk_id FROM rag_multimodal;")
            existing_ids = {row[0] for row in cur.fetchall()}

    missing = [c for c in chunks if c["chunk_id"] not in existing_ids]
    prompt_tokens = 0
    embed_cost = 0.0
    t0 = time.perf_counter()

    if missing:
        texts = [c["content"] for c in missing]
        vectors, prompt_tokens, _ = embed_documents_openai(
            texts,
            api_key=settings.openai_api_key,
            model_name=settings.embedding_model,
            expected_dimensions=settings.embedding_dimensions,
            batch_size=64,
        )
        embed_cost = estimate_embedding_cost_usd(settings.embedding_model, prompt_tokens)

        with psycopg.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                for ch, vec in zip(missing, vectors):
                    cur.execute(
                        """
                        INSERT INTO rag_multimodal (
                            chunk_id, doc_id, page, section, modality, label,
                            bbox_pt, bbox_norm, crop_path, render_path, content, embedding
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s, %s, %s::vector)
                        ON CONFLICT (chunk_id) DO UPDATE SET
                            content = EXCLUDED.content,
                            embedding = EXCLUDED.embedding,
                            crop_path = EXCLUDED.crop_path,
                            render_path = EXCLUDED.render_path;
                        """,
                        (
                            ch["chunk_id"],
                            ch["doc_id"],
                            int(ch["page"]),
                            ch["section"],
                            ch["modality"],
                            ch["label"],
                            json.dumps(ch["bbox_pt"]) if ch["bbox_pt"] is not None else None,
                            json.dumps(ch["bbox_norm"]) if ch["bbox_norm"] is not None else None,
                            ch["crop_path"],
                            ch["render_path"],
                            ch["content"],
                            _vector_literal(vec),
                        ),
                    )
            conn.commit()

    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM rag_multimodal;")
            total_rows = int(cur.fetchone()[0])

    stats = {
        "table": "rag_multimodal",
        "expected_chunks": len(chunks),
        "db_rows": total_rows,
        "newly_embedded": len(missing),
        "embed_tokens": prompt_tokens,
        "embed_cost_usd": round(embed_cost, 6),
        "elapsed_s": round(time.perf_counter() - t0, 2),
    }
    STORE_STATS_PATH.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    return stats


class MultimodalBM25:
    """In-memory Okapi BM25 over multimodal_chunks.json."""

    def __init__(self, chunks: list[dict[str, Any]], k1: float = 1.5, b: float = 0.75) -> None:
        self.chunks = chunks
        self.by_id = {c["chunk_id"]: c for c in chunks}
        self.k1 = k1
        self.b = b
        self.doc_tokens = [tokenize(f"{c['label']} {c['content']}") for c in chunks]
        self.doc_tf = [Counter(toks) for toks in self.doc_tokens]
        self.doc_len = [len(toks) for toks in self.doc_tokens]
        self.avgdl = (sum(self.doc_len) / len(self.doc_len)) if self.doc_len else 1.0
        df: Counter[str] = Counter()
        for toks in self.doc_tokens:
            for t in set(toks):
                df[t] += 1
        n = len(chunks)
        self.idf = {t: math.log(1.0 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def search(
        self,
        query: str,
        *,
        top_k: int = 8,
        modality: str | None = None,
        section: str | None = None,
    ) -> list[dict[str, Any]]:
        q_toks = tokenize(query)
        if not q_toks:
            return []
        scored: list[tuple[float, int]] = []
        for idx, ch in enumerate(self.chunks):
            if modality and ch["modality"] != modality:
                continue
            if section and ch["section"] != section:
                continue
            tf = self.doc_tf[idx]
            dl = self.doc_len[idx]
            score = 0.0
            for t in q_toks:
                if t not in tf:
                    continue
                f = tf[t]
                idf = self.idf.get(t, 0.0)
                score += idf * (f * (self.k1 + 1.0)) / (f + self.k1 * (1.0 - self.b + self.b * dl / self.avgdl))
            if score > 0.0:
                scored.append((score, idx))
        scored.sort(key=lambda x: -x[0])
        out: list[dict[str, Any]] = []
        for rank, (sc, idx) in enumerate(scored[:top_k], 1):
            item = dict(self.chunks[idx])
            item["score"] = round(float(sc), 6)
            item["rank"] = rank
            out.append(item)
        return out


class MultimodalHybridRetriever:
    """Hybrid Dense (pgvector) + BM25 RRF retriever + page-context accessor."""

    def __init__(self, chunks_path: Path = CHUNKS_PATH) -> None:
        settings = load_settings(require_db=True, require_openai=True)
        self.database_url = settings.database_url
        self.embedder = OpenAIQueryEmbedder(
            api_key=settings.openai_api_key,
            model_name=settings.embedding_model,
            expected_dimensions=settings.embedding_dimensions,
        )
        self.chunks: list[dict[str, Any]] = json.loads(chunks_path.read_text(encoding="utf-8"))
        self.by_id: dict[str, dict[str, Any]] = {c["chunk_id"]: c for c in self.chunks}
        self.by_label: dict[str, dict[str, Any]] = {
            c["label"].strip().lower(): c
            for c in self.chunks
            if c.get("crop_path") and c.get("label")
        }
        self.bm25 = MultimodalBM25(self.chunks)

    def search_dense(
        self,
        query: str,
        *,
        top_k: int = 12,
        modality: str | None = None,
        section: str | None = None,
    ) -> tuple[list[dict[str, Any]], int, float]:
        prev_tokens = self.embedder.total_prompt_tokens
        q_vec = self.embedder.embed_query(query)
        tokens = self.embedder.total_prompt_tokens - prev_tokens
        cost = estimate_embedding_cost_usd(self.embedder.model_name, tokens)
        clauses: list[str] = []
        params: list[Any] = [_vector_literal(q_vec)]
        if modality:
            clauses.append("modality = %s")
            params.append(modality)
        if section:
            clauses.append("section = %s")
            params.append(section)
        where_sql = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        params.append(_vector_literal(q_vec))
        params.append(top_k)

        sql = f"""
            SELECT chunk_id, doc_id, page, section, modality, label,
                   bbox_pt, bbox_norm, crop_path, render_path, content,
                   1.0 - (embedding <=> %s::vector) AS score
            FROM rag_multimodal
            {where_sql}
            ORDER BY embedding <=> %s::vector ASC
            LIMIT %s;
        """
        rows: list[dict[str, Any]] = []
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                for rank, r in enumerate(cur.fetchall(), 1):
                    rows.append(
                        {
                            "chunk_id": r[0],
                            "doc_id": r[1],
                            "page": int(r[2]),
                            "section": r[3],
                            "modality": r[4],
                            "label": r[5],
                            "bbox_pt": r[6],
                            "bbox_norm": r[7],
                            "crop_path": r[8],
                            "render_path": r[9],
                            "content": r[10],
                            "score": round(float(r[11]), 6),
                            "rank": rank,
                        }
                    )
        return rows, tokens, cost

    def search_hybrid(
        self,
        query: str,
        *,
        top_k: int = 6,
        candidate_k: int = 15,
        modality: str | None = None,
        section: str | None = None,
        rrf_k: int = 60,
    ) -> tuple[list[dict[str, Any]], int, float]:
        dense_res, tokens, cost = self.search_dense(query, top_k=candidate_k, modality=modality, section=section)
        bm25_res = self.bm25.search(query, top_k=candidate_k, modality=modality, section=section)

        scores: dict[str, float] = {}
        items: dict[str, dict[str, Any]] = {}
        for rank, item in enumerate(dense_res, 1):
            cid = item["chunk_id"]
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + rank)
            items[cid] = item
        for rank, item in enumerate(bm25_res, 1):
            cid = item["chunk_id"]
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + rank)
            items.setdefault(cid, item)

        ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
        out: list[dict[str, Any]] = []
        for r_idx, (cid, sc) in enumerate(ranked, 1):
            entry = dict(items[cid])
            entry["score"] = round(sc, 6)
            entry["rank"] = r_idx
            out.append(entry)
        return out, tokens, cost

    def search_exact(
        self,
        query: str,
        *,
        top_k: int = 6,
        modality: str | None = None,
        section: str | None = None,
    ) -> list[dict[str, Any]]:
        return self.bm25.search(query, top_k=top_k, modality=modality, section=section)

    def get_page_context(self, page: int, window: int = 0) -> list[dict[str, Any]]:
        lo = max(1, page - window)
        hi = page + window
        return [c for c in self.chunks if lo <= int(c["page"]) <= hi]

    def check_exact_phrase(self, phrase: str, *, limit: int = 5) -> dict[str, Any]:
        needle = phrase.strip().lower()
        if not needle:
            return {"phrase": phrase, "match_count": 0, "matches": []}
        matches: list[dict[str, Any]] = []
        for ch in self.chunks:
            hay = f"{ch['label']}\n{ch['content']}".lower()
            idx = hay.find(needle)
            if idx != -1:
                start = max(0, idx - 120)
                end = min(len(hay), idx + len(needle) + 200)
                matches.append(
                    {
                        "chunk_id": ch["chunk_id"],
                        "page": ch["page"],
                        "modality": ch["modality"],
                        "label": ch["label"],
                        "crop_path": ch["crop_path"],
                        "snippet": f"{ch['label']}\n{ch['content']}"[start:end],
                    }
                )
        if not matches:
            return {
                "phrase": phrase,
                "match_count": 0,
                "matches": [],
                "note": "Exact phrase NOT found anywhere across all 154 pages.",
            }
        return {"phrase": phrase, "match_count": len(matches), "matches": matches[:limit]}


def main() -> None:
    stats = ingest_to_pgvector()
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
