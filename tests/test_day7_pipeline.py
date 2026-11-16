"""Offline unit tests for Day 7 retrievers, context engineering, dataset builder, and agent loop."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agent import AgenticRagRunner
from src.build_dataset import UNANSWERABLE_CASES, convert_day6_question
from src.context import ChunkCorpusIndex, evidence_hit, pack_context
from src.retrievers import Bm25Retriever, HybridRrfRetriever, reciprocal_rank_fusion


def _make_chunks() -> list[dict]:
    return [
        {
            "id": "doc1:p001:para:000",
            "source_id": "doc1",
            "source": "doc1.pdf",
            "page": 1,
            "text": "GV-1.7-002 Consider data retention requirements when decommissioning GAI systems.",
            "metadata": {"year": 2024, "document_type": "genai_profile", "section": "govern"},
        },
        {
            "id": "doc1:p002:para:000",
            "source_id": "doc1",
            "source": "doc1.pdf",
            "page": 2,
            "text": "Continued from page 1: also consider data leakage after decommissioning.",
            "metadata": {"year": 2024, "document_type": "genai_profile", "section": "govern"},
        },
        {
            "id": "doc2:p001:para:000",
            "source_id": "doc2",
            "source": "doc2.pdf",
            "page": 1,
            "text": "Risk tolerance refers to an organization's readiness to bear risk.",
            "metadata": {"year": 2023, "document_type": "core_framework", "section": "foundational"},
        },
    ]


class _FakeToolCall:
    def __init__(self, call_id: str, name: str, arguments: dict) -> None:
        self.id = call_id
        self.function = SimpleNamespace(name=name, arguments=json.dumps(arguments))

    def model_dump(self) -> dict:
        return {
            "id": self.id,
            "type": "function",
            "function": {"name": self.function.name, "arguments": self.function.arguments},
        }


class _FakeClient:
    def __init__(self, turns: list[list[_FakeToolCall]]) -> None:
        self._turns = iter(turns)
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        tcs = next(self._turns)
        usage = SimpleNamespace(prompt_tokens=100, completion_tokens=20, prompt_tokens_details=None)
        msg = SimpleNamespace(content=None, tool_calls=tcs)
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)], usage=usage)


class Day7PipelineTests(unittest.TestCase):
    def test_bm25_exact_code_and_filter(self) -> None:
        chunks = _make_chunks()
        bm25 = Bm25Retriever(chunks)
        hits = bm25.search("GV-1.7-002 decommissioning", top_k=3)
        self.assertEqual(hits[0]["id"], "doc1:p001:para:000")

        filtered = bm25.search("risk tolerance", filters={"year": 2024}, top_k=3)
        self.assertEqual(filtered, [])

        with self.assertRaises(ValueError):
            bm25.search("risk", filters={"gold": "leak"}, top_k=3)

    def test_rrf_and_hybrid_fusion(self) -> None:
        chunks = _make_chunks()
        bm25 = Bm25Retriever(chunks)
        fused = reciprocal_rank_fusion(
            [
                ("dense", [chunks[2], chunks[0]], 1.0),
                ("bm25", [chunks[0], chunks[1]], 1.0),
            ],
            rrf_k=60,
            top_k=2,
        )
        self.assertEqual(fused[0]["id"], "doc1:p001:para:000")
        self.assertEqual(fused[0]["fusion_ranks"], {"dense": 2, "bm25": 1})

        hybrid = HybridRrfRetriever(bm25, bm25, candidate_k=3)
        self.assertEqual(hybrid.search("GV-1.7-002 decommissioning", top_k=1)[0]["id"], "doc1:p001:para:000")

    def test_context_neighbors_and_evidence_hit(self) -> None:
        chunks = _make_chunks()
        idx = ChunkCorpusIndex(chunks)
        neighbors = idx.get_neighbors("doc1:p001:para:000", window=1)
        self.assertEqual([n["id"] for n in neighbors], ["doc1:p002:para:000"])

        ctx, ids = pack_context(
            [chunks[0]], budget_chars=1200, corpus_index=idx, expand_neighbors=True, neighbor_top_n=1
        )
        self.assertEqual(ids, ["doc1:p001:para:000", "doc1:p002:para:000"])
        self.assertLessEqual(len(ctx), 1200)
        self.assertTrue(
            evidence_hit(chunks[0], [{"source_id": "doc1", "page": 1, "evidence": "GV-1.7-002"}])
        )

    def test_convert_preserves_acceptable_gold_and_unanswerables(self) -> None:
        raw = {
            "id": "q07",
            "split": "dev",
            "type": "truc_tiep",
            "question": "Q?",
            "expected_answer": "A",
            "gold_source_id": "s1",
            "gold_page": 10,
            "evidence_quote": "quote1",
            "acceptable_gold": [{"source_id": "s2", "page": 20, "evidence_quote": "quote2"}],
            "filter": None,
        }
        converted = convert_day6_question(raw)
        self.assertEqual(len(converted["gold"]), 2)
        self.assertNotIn("filter", converted)
        self.assertGreaterEqual(sum(1 for u in UNANSWERABLE_CASES if u["split"] == "dev"), 2)
        self.assertGreaterEqual(sum(1 for u in UNANSWERABLE_CASES if u["split"] == "test"), 2)

    def test_agent_multi_tool_citation_and_abstention(self) -> None:
        chunks = _make_chunks()
        idx = ChunkCorpusIndex(chunks)
        bm25 = Bm25Retriever(chunks)
        runner = AgenticRagRunner(
            api_key="test-key-not-used",
            primary_retriever=bm25,
            lexical_retriever=bm25,
            corpus_index=idx,
            multi_tool=True,
            budget_chars=2400,
        )
        runner.client = _FakeClient(
            [
                [_FakeToolCall("c1", "search_hybrid", {"query": "GV-1.7-002"})],
                [_FakeToolCall("c2", "get_neighbor_chunks", {"chunk_id": "doc1:p001:para:000"})],
                [
                    _FakeToolCall(
                        "c3",
                        "submit_final_answer",
                        {
                            "decision": "answer",
                            "answer": "Consider data retention [doc1:p001:para:000] and leakage [doc1:p002:para:000].",
                            "citations": ["doc1:p001:para:000", "doc1:p002:para:000"],
                        },
                    )
                ],
            ]
        )
        trace = runner.run_case(
            {"id": "q1", "split": "dev", "answerable": True, "question": "Decommissioning?"}
        )
        self.assertEqual(trace["status"], "answered")
        self.assertEqual(trace["search_calls"], 2)
        self.assertEqual(trace["citations"], ["doc1:p001:para:000", "doc1:p002:para:000"])

        # Missing citation forces safe abstention.
        runner.client = _FakeClient(
            [
                [_FakeToolCall("c1", "search_hybrid", {"query": "GV-1.7-002"})],
                [
                    _FakeToolCall(
                        "c2",
                        "submit_final_answer",
                        {"decision": "answer", "answer": "Made up", "citations": ["fake-id"]},
                    )
                ],
            ]
        )
        bad = runner.run_case({"id": "q2", "split": "dev", "answerable": True, "question": "Q?"})
        self.assertEqual(bad["status"], "abstain")
        self.assertEqual(bad["citations"], [])

    def test_errors_and_invalid_configs_fail_loudly(self) -> None:
        from src.day6_bridge import Day6PgVectorClient, OpenAIQueryEmbedder

        with self.assertRaises(RuntimeError):
            OpenAIQueryEmbedder(api_key="", model_name="text-embedding-3-small", expected_dimensions=1536)
        with self.assertRaises(ValueError):
            OpenAIQueryEmbedder(api_key="dummy", model_name="text-embedding-3-small", expected_dimensions=768)

        pg = Day6PgVectorClient("postgresql://user:pass@127.0.0.1:59999/db", dimensions=1536)
        with self.assertRaises(ValueError):
            pg.search_vector([0.1, 0.2], top_k=3)

        class _BrokenRetriever:
            name = "broken"

            def search(self, query: str, *, filters=None, top_k: int = 3):
                raise ConnectionError("pgvector unavailable")

        runner = AgenticRagRunner(
            api_key="test-key-not-used",
            primary_retriever=_BrokenRetriever(),
            multi_tool=False,
        )
        runner.client = _FakeClient([[_FakeToolCall("c1", "search_vector", {"query": "test"})]])
        with self.assertRaises(ConnectionError):
            runner.run_case({"id": "q3", "split": "dev", "answerable": True, "question": "Q?"})

    def test_bootstrap_pgvector_row_validation(self) -> None:
        from src.bootstrap_pgvector import build_upsert_rows, embed_documents_openai

        chunks = _make_chunks()[:1]
        rows = build_upsert_rows("B", chunks, [[0.1, 0.2, 0.3]], dimensions=3)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "B")
        self.assertEqual(rows[0][1], "doc1:p001:para:000")

        with self.assertRaises(ValueError):
            build_upsert_rows("B", chunks, [[0.1, 0.2]], dimensions=3)
        with self.assertRaises(ValueError):
            build_upsert_rows("B", [], [], dimensions=3)
        with self.assertRaises(RuntimeError):
            embed_documents_openai(["hello"], api_key="", model_name="text-embedding-3-small")


if __name__ == "__main__":
    unittest.main()
