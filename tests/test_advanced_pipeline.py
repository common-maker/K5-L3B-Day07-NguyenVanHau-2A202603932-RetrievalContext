"""Unit tests for the Advanced Multimodal RAG pipeline (no network/API calls)."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from advanced.evaluate import score_reviews, validate_benchmark
from advanced.ingest import _chunk_text, classify_page_section
from advanced.store import MultimodalBM25, tokenize


class AdvancedPipelineTests(unittest.TestCase):
    def test_tokenize_preserves_model_and_table_tokens(self) -> None:
        toks = tokenize("Table 12 Gemini 1.5 Pro HumanEval BFCL")
        self.assertIn("table", toks)
        self.assertIn("12", toks)
        self.assertIn("1.5", toks)
        self.assertIn("humaneval", toks)

    def test_chunk_text_respects_max_chars_and_overlap(self) -> None:
        sample = "\n\n".join([f"Paragraph {i} " + ("word " * 40) for i in range(6)])
        chunks = _chunk_text(sample, max_chars=500, overlap_chars=60)
        self.assertGreater(len(chunks), 2)
        for ch in chunks[:-1]:
            self.assertLessEqual(len(ch), 750)

    def test_classify_page_section(self) -> None:
        self.assertEqual(classify_page_section(1, ""), "front_matter")
        self.assertEqual(classify_page_section(12, ""), "main_body")
        self.assertEqual(classify_page_section(80, ""), "references")
        self.assertEqual(classify_page_section(100, ""), "contributors_acknowledgments")
        self.assertEqual(classify_page_section(120, ""), "appendix")

    def test_bm25_exact_table_and_modality_filter(self) -> None:
        chunks = [
            {
                "chunk_id": "c1",
                "page": 3,
                "section": "main_body",
                "modality": "table",
                "label": "Table 1",
                "content": "Table 1 Gemini 1.5 Pro Win-rate 78.1%",
            },
            {
                "chunk_id": "c2",
                "page": 5,
                "section": "main_body",
                "modality": "chart",
                "label": "Figure 2",
                "content": "Figure 2 Bar chart MATH 67.7 HumanEval 84.1",
            },
        ]
        bm25 = MultimodalBM25(chunks)
        res = bm25.search("HumanEval", modality="chart")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["chunk_id"], "c2")

    def test_validate_benchmark_and_strict_scorer(self) -> None:
        dev = [{"id": f"d{i}", "category": "text", "question": f"Dev question {i}?"} for i in range(15)] + [
            {"id": f"du{i}", "category": "unanswerable", "question": f"Dev unanswerable {i}?"} for i in range(3)
        ]
        test = (
            [{"id": f"tt{i}", "category": "table", "question": f"Test table {i}?"} for i in range(6)]
            + [{"id": f"ti{i}", "category": "image_diagram", "question": f"Test img {i}?"} for i in range(5)]
            + [{"id": f"tc{i}", "category": "chart", "question": f"Test chart {i}?"} for i in range(5)]
            + [{"id": f"tm{i}", "category": "multi_hop", "question": f"Test multi {i}?"} for i in range(4)]
            + [{"id": f"tx{i}", "category": "text", "question": f"Test text {i}?"} for i in range(4)]
            + [{"id": f"tu{i}", "category": "unanswerable", "question": f"Test unans {i}?"} for i in range(6)]
        )
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bench.json"
            p.write_text(json.dumps({"dev": dev, "test": test}), encoding="utf-8")
            res = validate_benchmark(p)
            self.assertEqual(res["test_total"], 30)

        traces = [
            {
                "id": item["id"],
                "status": "error" if idx == 0 else "ok",
                "latency_ms": 100.0,
                "total_cost_usd": 0.01,
            }
            for idx, item in enumerate(test)
        ]
        reviews = [{"id": item["id"], "pass": True} for item in test]
        summary = score_reviews(test, traces, reviews)
        self.assertEqual(summary["passed"], 29)
        self.assertEqual(summary["errors"], 1)
        self.assertTrue(summary["meets_90pct_threshold"])

    def test_check_exact_phrase_logic(self) -> None:
        from advanced.store import MultimodalHybridRetriever

        chunks = [
            {"chunk_id": "c1", "page": 30, "modality": "table", "label": "Table 11", "crop_path": "p030_table_1.png", "content": "HumanEval 84.1%"},
            {"chunk_id": "c2", "page": 43, "modality": "table", "label": "Table 21", "crop_path": "p043_table_1.png", "content": "AIME 2024 7/30"},
        ]
        # Construct lightweight stub without DB/OpenAI
        r = MultimodalHybridRetriever.__new__(MultimodalHybridRetriever)
        r.chunks = chunks
        r.by_label = {c["label"].lower(): c for c in chunks}
        hit = r.check_exact_phrase("AIME 2024")
        miss = r.check_exact_phrase("AIME 2025")
        self.assertEqual(hit["match_count"], 1)
        self.assertEqual(miss["match_count"], 0)
        self.assertIn("table 11", r.by_label)


if __name__ == "__main__":
    unittest.main()
