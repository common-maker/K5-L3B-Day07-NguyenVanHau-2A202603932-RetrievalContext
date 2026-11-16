"""Run real Agentic RAG evaluation and generate human-audit worksheets."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .agent import AgenticRagRunner
from .config import PROJECT_ROOT, load_settings
from .context import ChunkCorpusIndex
from .day6_bridge import Day6PgVectorClient, OpenAIQueryEmbedder, write_json
from .retrievers import (
    Bm25Retriever,
    DensePgVectorRetriever,
    HybridRrfRetriever,
    LlmRerankRetriever,
)


def _export_audit_worksheet(
    cases: list[dict[str, Any]],
    traces: list[dict[str, Any]],
    corpus_index: ChunkCorpusIndex,
    out_path: Path,
) -> None:
    """Create a readable Markdown worksheet for manual verification of every answer & citation."""
    case_by_id = {c["id"]: c for c in cases}
    lines = ["# Agent Output Audit Worksheet\n"]
    for tr in traces:
        cid = tr["query_id"]
        c = case_by_id[cid]
        lines.append(f"## {cid} ({c['split']} | answerable={c['answerable']} | status={tr['status']})")
        lines.append(f"- **Question:** {c['question']}")
        if c["answerable"]:
            lines.append(f"- **Expected answer:** {c.get('expected_answer', '')}")
            lines.append(f"- **Gold:** `{json.dumps(c.get('gold', []), ensure_ascii=False)}`")
        else:
            lines.append(f"- **Absence reason:** {c.get('absence_reason', '')}")
        lines.append(f"- **Search calls:** {tr.get('search_calls', 0)} | **Elapsed:** {tr.get('elapsed_ms', 0)} ms")
        lines.append(f"- **Agent answer:** {tr.get('answer', '')}")
        lines.append(f"- **Citations:** {tr.get('citations', [])}")
        if tr.get("error"):
            lines.append(f"- **Error:** `{tr['error']}`")
        for cited_id in tr.get("citations", []):
            chunk = corpus_index.by_id.get(cited_id)
            if chunk:
                lines.append(f"  - Cited `[{cited_id}]` ({chunk['source_id']} p.{chunk['page']}): {chunk['text']}")
        lines.append("")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def build_agent_runner(
    *,
    mode: str,
    chunks: list[dict[str, Any]],
    corpus_index: ChunkCorpusIndex,
    database_url: str,
    openai_api_key: str,
    embedding_model: str,
    embedding_dimensions: int,
    agent_model: str,
    rerank_model: str,
    primary_strategy: str = "hybrid_rerank",
    budget_chars: int = 2800,
) -> tuple[AgenticRagRunner, OpenAIQueryEmbedder, LlmRerankRetriever | None]:
    pg_client = Day6PgVectorClient(database_url, dimensions=embedding_dimensions, strategy="B")
    pg_client.health_check()
    embedder = OpenAIQueryEmbedder(
        api_key=openai_api_key,
        model_name=embedding_model,
        expected_dimensions=embedding_dimensions,
    )
    dense = DensePgVectorRetriever(pg_client, embedder, name="dense_pgvector")
    bm25 = Bm25Retriever(chunks, k1=1.5, b=0.75, name="bm25")

    if mode == "baseline":
        runner = AgenticRagRunner(
            api_key=openai_api_key,
            model=agent_model,
            primary_retriever=dense,
            lexical_retriever=None,
            corpus_index=corpus_index,
            multi_tool=False,
            max_searches=4,
            default_top_k=3,
            budget_chars=800,
            prioritize_latest_context=False,
        )
        return runner, embedder, None

    if mode == "tuned":
        hybrid = HybridRrfRetriever(dense, bm25, candidate_k=12, rrf_k=60, name="hybrid_rrf")
        reranker: LlmRerankRetriever | None = None
        if primary_strategy == "hybrid_rrf":
            primary: Any = hybrid
        elif primary_strategy == "hybrid_rerank":
            reranker = LlmRerankRetriever(
                hybrid,
                api_key=openai_api_key,
                model=rerank_model,
                candidate_k=12,
                name="hybrid_rerank",
            )
            primary = reranker
        else:
            raise ValueError(f"Unsupported primary_strategy '{primary_strategy}'.")

        runner = AgenticRagRunner(
            api_key=openai_api_key,
            model=agent_model,
            primary_retriever=primary,
            lexical_retriever=bm25,
            corpus_index=corpus_index,
            multi_tool=True,
            max_searches=4,
            default_top_k=4,
            budget_chars=budget_chars,
            prioritize_latest_context=True,
        )
        return runner, embedder, reranker

    raise ValueError(f"Unsupported mode '{mode}'; choose 'baseline' or 'tuned'.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Day 7 Agentic RAG benchmark on dev or test.")
    parser.add_argument("--chunks", type=Path, default=PROJECT_ROOT / "data" / "nist_chunks.json")
    parser.add_argument("--cases", type=Path, default=PROJECT_ROOT / "data" / "nist_cases.json")
    parser.add_argument("--split", choices=("dev", "test"), required=True)
    parser.add_argument("--mode", choices=("baseline", "tuned"), required=True)
    parser.add_argument("--primary-strategy", choices=("hybrid_rrf", "hybrid_rerank"), default="hybrid_rerank")
    parser.add_argument("--budget", type=int, default=2800)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "results" / "agent")
    args = parser.parse_args()

    settings = load_settings(require_db=True, require_openai=True)
    chunks = json.loads(args.chunks.read_text(encoding="utf-8"))
    all_cases = json.loads(args.cases.read_text(encoding="utf-8"))
    cases = [c for c in all_cases if c.get("split") == args.split]
    if not cases:
        raise ValueError(f"No cases found in split '{args.split}'.")

    corpus_index = ChunkCorpusIndex(chunks)
    runner, embedder, reranker = build_agent_runner(
        mode=args.mode,
        chunks=chunks,
        corpus_index=corpus_index,
        database_url=settings.database_url,
        openai_api_key=settings.openai_api_key,
        embedding_model=settings.embedding_model,
        embedding_dimensions=settings.embedding_dimensions,
        agent_model=settings.agent_model,
        rerank_model=settings.rerank_model,
        primary_strategy=args.primary_strategy,
        budget_chars=args.budget,
    )

    traces: list[dict[str, Any]] = []
    for case in cases:
        try:
            trace = runner.run_case(case)
        except Exception as exc:  # Record provider/DB error explicitly rather than faking results.
            trace = {
                "query_id": case["id"],
                "split": case["split"],
                "answerable": case["answerable"],
                "question": case["question"],
                "status": "error",
                "error": f"{type(exc).__name__}: {exc}",
                "events": [],
                "citations": [],
                "answer": "",
            }
        traces.append(trace)

    out_dir = args.output / f"{args.mode}-{args.split}"
    write_json(out_dir / "traces.json", traces)
    _export_audit_worksheet(cases, traces, corpus_index, out_dir / "audit_worksheet.md")

    # Skeleton review file with null grades so human auditor fills every label explicitly.
    review_skeleton = [
        {
            "query_id": t["query_id"],
            **({"answer_grade": None} if t["answerable"] else {"abstention_correct": None}),
            "citation_support": [None for _ in t.get("citations", [])],
            "note": "",
        }
        for t in traces
        if t.get("status") != "error"
    ]
    write_json(out_dir / "reviews_skeleton.json", review_skeleton)

    run_stats = {
        "mode": args.mode,
        "split": args.split,
        "cases": len(cases),
        "answered": sum(1 for t in traces if t["status"] == "answered"),
        "abstain": sum(1 for t in traces if t["status"] == "abstain"),
        "errors": sum(1 for t in traces if t["status"] == "error"),
        "agent_model": settings.agent_model,
        "chat_cost_usd": round(sum(float(t.get("chat_cost_usd", 0.0)) for t in traces), 6),
        "embed_tokens": embedder.total_prompt_tokens,
        "embed_cost_usd": round(embedder.estimated_cost_usd, 6),
        "rerank_cost_usd": round(reranker.estimated_cost_usd, 6) if reranker else 0.0,
        "total_elapsed_ms": round(sum(float(t.get("elapsed_ms", 0.0)) for t in traces), 2),
    }
    write_json(out_dir / "run_stats.json", run_stats)
    print(json.dumps(run_stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
