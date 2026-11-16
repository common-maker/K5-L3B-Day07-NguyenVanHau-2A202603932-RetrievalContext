# Day 7 Source Code (`src/`)

Implements the Day 7 Agentic RAG & Context Engineering pipeline connected to the Day 6 PostgreSQL/`pgvector` NIST corpus:

- `config.py`: Environment loader (`.env` / Day 6 `.env` fallback), filter whitelist (`ALLOWED_FILTERS`), and OpenAI token pricing helpers.
- `day6_bridge.py`: Read-only PostgreSQL + `pgvector` client (`Day6PgVectorClient`), OpenAI query embedder (`OpenAIQueryEmbedder`), and deterministic Day 6 Strategy `B` chunk exporter.
- `bootstrap_pgvector.py`: Verifies an existing Day 6 `rag_chunks` index (`--check`) or initializes schema + embeds `data/nist_chunks.json` via `text-embedding-3-small` on a standalone Docker `pgvector` container (`docker-compose.yml`).
- `build_dataset.py`: Exports Day 6 chunks (`data/nist_chunks.json`), converts answerable questions (`data/nist_questions.json`), and builds combined answerable + unanswerable evaluation cases (`data/nist_cases.json`).
- `retrievers.py`: `DensePgVectorRetriever`, `Bm25Retriever`, `HybridRrfRetriever`, `LlmRerankRetriever`, and `QueryRewriteRetriever`.
- `context.py`: Deduplicating budget packer (`pack_context`), same-document adjacent-chunk lookup (`ChunkCorpusIndex`), and gold evidence matcher (`evidence_hit`).
- `agent.py`: Real OpenAI tool-calling agent (`AgenticRagRunner`) supporting multi-tool retrieval (`search_hybrid`, `search_lexical`, `get_neighbor_chunks`), prompt-injection isolation, inline `[chunk_id]` citation enforcement, and safe abstention.
- `eval_retrieval.py`: Reproducible retrieval benchmark evaluator emitting `Hit@1`, `Evidence Hit@3`, `Context Evidence Rate`, `MRR@3`, latency, and cost.
- `eval_agent.py`: Reproducible agent runner saving full tool-call traces, run stats, and human-audit worksheets.
