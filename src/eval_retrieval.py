"""Run reproducible retrieval & context benchmarks on dev or test split."""
from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT, load_settings
from .context import ChunkCorpusIndex, evidence_hit, pack_context
from .day6_bridge import Day6PgVectorClient, OpenAIQueryEmbedder, write_json
from .retrievers import (
    BaseRetriever,
    Bm25Retriever,
    DensePgVectorRetriever,
    HybridRrfRetriever,
    LlmRerankRetriever,
    QueryRewriteRetriever,
)


def evaluate_retrieval_method(
    *,
    config_name: str,
    retriever: BaseRetriever,
    questions: list[dict[str, Any]],
    corpus_index: ChunkCorpusIndex,
    budget_chars: int = 800,
    expand_neighbors: bool = False,
    neighbor_top_n: int = 1,
    top_k: int = 3,
    extra_cost_fn: Any = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Evaluate a retriever over answerable questions, always scoring top-3 ranking."""
    traces: list[dict[str, Any]] = []
    cost_before = extra_cost_fn() if extra_cost_fn else 0.0

    for q in questions:
        t0 = time.perf_counter()
        raw_results = retriever.search(q["question"], filters=q.get("filter"), top_k=top_k)
        top3 = raw_results[:3]
        context, context_ids = pack_context(
            top3,
            budget_chars=budget_chars,
            corpus_index=corpus_index,
            expand_neighbors=expand_neighbors,
            neighbor_top_n=neighbor_top_n,
        )
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)

        packed_chunks = [corpus_index.by_id[cid] for cid in context_ids if cid in corpus_index.by_id]
        marked_top3 = [{**r, "hit": evidence_hit(r, q["gold"])} for r in top3]
        hit1 = bool(marked_top3 and marked_top3[0]["hit"])
        hit3 = any(r["hit"] for r in marked_top3)
        context_hit = any(evidence_hit(c, q["gold"]) for c in packed_chunks)
        rr = next((1.0 / (idx + 1) for idx, r in enumerate(marked_top3) if r["hit"]), 0.0)

        rewrite_info = getattr(retriever, "last_rewrite_trace", None)
        traces.append(
            {
                "query_id": q["id"],
                "split": q["split"],
                "type": q.get("type", ""),
                "question": q["question"],
                "filter": q.get("filter"),
                "config": config_name,
                "budget_chars": budget_chars,
                "expand_neighbors": expand_neighbors,
                "rewrite_trace": rewrite_info,
                "gold": q["gold"],
                "results": marked_top3,
                "context": context,
                "context_ids": context_ids,
                "context_chars": len(context),
                "elapsed_ms": elapsed_ms,
                "hit1": hit1,
                "hit3": hit3,
                "context_hit": context_hit,
                "reciprocal_rank": round(rr, 4),
            }
        )

    n = len(traces)
    h1 = sum(t["hit1"] for t in traces)
    h3 = sum(t["hit3"] for t in traces)
    ch = sum(t["context_hit"] for t in traces)
    total_ms = round(sum(t["elapsed_ms"] for t in traces), 2)
    extra_cost = round((extra_cost_fn() if extra_cost_fn else 0.0) - cost_before, 6)

    summary = {
        "config": config_name,
        "n": n,
        "hit1": h1,
        "hit1_ratio": f"{h1}/{n}",
        "hit1_pct": round(100.0 * h1 / n, 1) if n else 0.0,
        "hit3": h3,
        "hit3_ratio": f"{h3}/{n}",
        "hit3_pct": round(100.0 * h3 / n, 1) if n else 0.0,
        "context_hit": ch,
        "context_hit_ratio": f"{ch}/{n}",
        "context_hit_pct": round(100.0 * ch / n, 1) if n else 0.0,
        "mrr_at_3": round(statistics.mean(t["reciprocal_rank"] for t in traces), 4) if n else 0.0,
        "avg_context_chars": round(statistics.mean(t["context_chars"] for t in traces), 1) if n else 0.0,
        "median_ms": round(statistics.median(t["elapsed_ms"] for t in traces), 2) if n else 0.0,
        "total_ms": total_ms,
        "extra_cost_usd": extra_cost,
        "budget_chars": budget_chars,
        "expand_neighbors": expand_neighbors,
    }
    return traces, summary


def build_retrieval_configs(
    chunks: list[dict[str, Any]],
    *,
    database_url: str,
    openai_api_key: str,
    embedding_model: str,
    embedding_dimensions: int,
    rerank_model: str,
) -> tuple[dict[str, dict[str, Any]], OpenAIQueryEmbedder, list[Any]]:
    """Construct all retrieval methods and dev improvement configurations."""
    pg_client = Day6PgVectorClient(database_url, dimensions=embedding_dimensions, strategy="B")
    health = pg_client.health_check()
    if health["chunk_count"] != len(chunks):
        raise RuntimeError(
            f"DB chunk count ({health['chunk_count']}) differs from JSON chunks ({len(chunks)})."
        )

    embedder = OpenAIQueryEmbedder(
        api_key=openai_api_key,
        model_name=embedding_model,
        expected_dimensions=embedding_dimensions,
    )
    dense = DensePgVectorRetriever(pg_client, embedder, name="dense_pgvector")
    bm25 = Bm25Retriever(chunks, k1=1.5, b=0.75, name="bm25")
    hybrid = HybridRrfRetriever(dense, bm25, candidate_k=12, rrf_k=60, name="hybrid_rrf")
    rerank = LlmRerankRetriever(
        hybrid, api_key=openai_api_key, model=rerank_model, candidate_k=12, name="hybrid_rerank"
    )
    rewrite_base = QueryRewriteRetriever(
        hybrid, api_key=openai_api_key, model=rerank_model, candidate_k=8, name="query_rewrite_hybrid"
    )
    rewrite_rerank = LlmRerankRetriever(
        rewrite_base, api_key=openai_api_key, model=rerank_model, candidate_k=12, name="rewrite_hybrid_rerank"
    )

    configs: dict[str, dict[str, Any]] = {
        "m1_dense_baseline": {
            "retriever": dense,
            "budget_chars": 800,
            "expand_neighbors": False,
            "cost_fn": lambda: embedder.estimated_cost_usd,
        },
        "m2_bm25_lexical": {
            "retriever": bm25,
            "budget_chars": 800,
            "expand_neighbors": False,
            "cost_fn": lambda: 0.0,
        },
        "m3_hybrid_rrf": {
            "retriever": hybrid,
            "budget_chars": 800,
            "expand_neighbors": False,
            "cost_fn": lambda: embedder.estimated_cost_usd,
        },
        "imp1_hybrid_rerank_b2400": {
            "retriever": rerank,
            "budget_chars": 2400,
            "expand_neighbors": False,
            "cost_fn": lambda: embedder.estimated_cost_usd + rerank.estimated_cost_usd,
        },
        "imp2_rewrite_rerank_neighbors_b2800": {
            "retriever": rewrite_rerank,
            "budget_chars": 2800,
            "expand_neighbors": True,
            "neighbor_top_n": 1,
            "cost_fn": lambda: (
                embedder.estimated_cost_usd
                + rewrite_base.estimated_cost_usd
                + rewrite_rerank.estimated_cost_usd
            ),
        },
    }
    return configs, embedder, [rerank, rewrite_base, rewrite_rerank]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Day 7 retrieval configurations.")
    parser.add_argument("--chunks", type=Path, default=PROJECT_ROOT / "data" / "nist_chunks.json")
    parser.add_argument("--questions", type=Path, default=PROJECT_ROOT / "data" / "nist_questions.json")
    parser.add_argument("--split", choices=("dev", "test"), required=True)
    parser.add_argument(
        "--configs",
        nargs="+",
        default=[
            "m1_dense_baseline",
            "m2_bm25_lexical",
            "m3_hybrid_rrf",
            "imp1_hybrid_rerank_b2400",
            "imp2_rewrite_rerank_neighbors_b2800",
        ],
    )
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "results" / "retrieval")
    args = parser.parse_args()

    settings = load_settings(require_db=True, require_openai=True)
    chunks = json.loads(args.chunks.read_text(encoding="utf-8"))
    all_questions = json.loads(args.questions.read_text(encoding="utf-8"))
    questions = [q for q in all_questions if q.get("split") == args.split]
    if not questions:
        raise ValueError(f"No questions found in split '{args.split}'.")

    corpus_index = ChunkCorpusIndex(chunks)
    all_configs, _embedder, _models = build_retrieval_configs(
        chunks,
        database_url=settings.database_url,
        openai_api_key=settings.openai_api_key,
        embedding_model=settings.embedding_model,
        embedding_dimensions=settings.embedding_dimensions,
        rerank_model=settings.rerank_model,
    )

    summaries: list[dict[str, Any]] = []
    out_dir = args.output / args.split
    for cname in args.configs:
        if cname not in all_configs:
            raise ValueError(f"Unknown config '{cname}'. Available: {sorted(all_configs)}")
        cfg = all_configs[cname]
        traces, summary = evaluate_retrieval_method(
            config_name=cname,
            retriever=cfg["retriever"],
            questions=questions,
            corpus_index=corpus_index,
            budget_chars=cfg["budget_chars"],
            expand_neighbors=cfg["expand_neighbors"],
            neighbor_top_n=cfg.get("neighbor_top_n", 1),
            extra_cost_fn=cfg["cost_fn"],
        )
        write_json(out_dir / f"{cname}_traces.json", traces)
        summaries.append(summary)

    write_json(out_dir / "summary.json", summaries)
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
