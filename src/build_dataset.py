"""Build and validate Day 7 NIST dataset files from Day 6 outputs + unanswerable cases."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .config import DEFAULT_DAY6_ROOT, PROJECT_ROOT
from .day6_bridge import export_day6_chunks_from_pdfs, write_json

# Six near-topic unanswerable questions verified absent across all pages of
# NIST.AI.100-1.pdf (48p) and NIST.AI.600-1.pdf (64p).
UNANSWERABLE_CASES: list[dict[str, Any]] = [
    {
        "id": "u01",
        "split": "dev",
        "type": "unanswerable",
        "question": (
            "Under NIST AI 600-1, within how many calendar days or hours must a generative AI "
            "deployer notify the U.S. Department of Health and Human Services of a HIPAA-covered "
            "AI data breach?"
        ),
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "filter": None,
        "absence_reason": (
            "NIST AI 600-1 (p. 50, MG-4.1 / MG-4.3 context) mentions HIPAA breach reporting only "
            "as an illustrative legal/regulatory compliance example without specifying any "
            "notification deadline in hours or calendar days."
        ),
        "verification_note": (
            "Checked full text of NIST.AI.100-1.pdf and NIST.AI.600-1.pdf for 'hipaa', "
            "'health and human', '60 day', and '72 hour'."
        ),
    },
    {
        "id": "u02",
        "split": "dev",
        "type": "unanswerable",
        "question": (
            "What minimum training compute FLOP threshold (such as 10^26 FLOPs) does Executive "
            "Order 14110 or NIST AI 600-1 establish for mandatory dual-use foundation model "
            "safety reporting?"
        ),
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "filter": None,
        "absence_reason": (
            "NIST AI 600-1 (p. 5) references Executive Order 14110 as its mandate and mentions "
            "high compute utilization (p. 12), but neither NIST AI 100-1 nor 600-1 states any "
            "FLOP count or 10^26 reporting threshold."
        ),
        "verification_note": (
            "Checked full text of both NIST PDFs for 'flop', '14110', and 'compute'."
        ),
    },
    {
        "id": "u03",
        "split": "dev",
        "type": "unanswerable",
        "question": (
            "What EU AI Act risk tier and maximum global annual turnover fine percentage apply "
            "to generative AI confabulation under the NIST AI RMF?"
        ),
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "filter": None,
        "absence_reason": (
            "NIST AI 600-1 defines confabulation (p. 10) and NIST AI 100-1 discusses risk levels, "
            "but neither document defines EU AI Act risk tiers or monetary/turnover penalties."
        ),
        "verification_note": (
            "Checked full text of both NIST PDFs for 'eu ai', 'turnover', 'penalty', and 'penalties'."
        ),
    },
    {
        "id": "u04",
        "split": "test",
        "type": "unanswerable",
        "question": (
            "Which specific cryptographic watermarking standard (such as C2PA or Google SynthID) "
            "does NIST AI 600-1 mandate for tracking generative AI content provenance?"
        ),
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "filter": None,
        "absence_reason": (
            "NIST AI 600-1 discusses watermarking and content provenance generally (pp. 20, 23, "
            "37, 55-56), but never mentions C2PA, SynthID, or any single mandatory watermarking algorithm."
        ),
        "verification_note": (
            "Checked full text of both NIST PDFs for 'c2pa', 'synthid', and all 13 occurrences "
            "of 'watermark'."
        ),
    },
    {
        "id": "u05",
        "split": "test",
        "type": "unanswerable",
        "question": (
            "How many mandatory ISO/IEC 42001 clauses and annual external audit cycles are "
            "required to achieve official NIST AI RMF 1.0 certification?"
        ),
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "filter": None,
        "absence_reason": (
            "NIST AI 100-1 mentions technical standards and certifications generically (pp. 32, 46), "
            "but does not reference ISO/IEC 42001 clauses, audit cycles, or an AI RMF certification program."
        ),
        "verification_note": (
            "Checked full text of both NIST PDFs for '42001', 'iso/iec', 'accreditation', and 'certification'."
        ),
    },
    {
        "id": "u06",
        "split": "test",
        "type": "unanswerable",
        "question": (
            "What hard maximum training energy limit in megawatt-hours (MWh) or carbon threshold "
            "in tCO2e does NIST AI 600-1 enforce before prohibiting model deployment?"
        ),
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "filter": None,
        "absence_reason": (
            "NIST AI 600-1 discusses environmental impacts of compute (p. 12) and organizational "
            "minimum assurance thresholds (GV-1.3-002), but sets no numeric MWh or tCO2e limits."
        ),
        "verification_note": (
            "Checked full text of both NIST PDFs for 'mwh', 'co2', 'tco2', 'kwh', and 'threshold'."
        ),
    },
]


def convert_day6_question(raw_q: dict[str, Any]) -> dict[str, Any]:
    """Convert a Day 6 question into Day 7 JSON schema while keeping acceptable_gold."""
    gold: list[dict[str, Any]] = [
        {
            "source_id": raw_q["gold_source_id"],
            "page": int(raw_q["gold_page"]),
            "evidence": raw_q["evidence_quote"],
        }
    ]
    for alt in raw_q.get("acceptable_gold") or []:
        gold.append(
            {
                "source_id": alt["source_id"],
                "page": int(alt["page"]),
                "evidence": alt["evidence_quote"],
            }
        )
    out: dict[str, Any] = {
        "id": raw_q["id"],
        "split": raw_q["split"],
        "type": raw_q.get("type", "direct"),
        "question": raw_q["question"],
        "expected_answer": raw_q["expected_answer"],
        "gold": gold,
    }
    if raw_q.get("filter") is not None:
        out["filter"] = raw_q["filter"]
    return out


def build_agent_cases(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Combine answerable questions and near-topic unanswerable cases for agent eval."""
    cases: list[dict[str, Any]] = []
    for q in questions:
        case: dict[str, Any] = {
            "id": q["id"],
            "split": q["split"],
            "type": q.get("type", "direct"),
            "question": q["question"],
            "answerable": True,
            "expected_behavior": "search_and_answer",
            "expected_answer": q["expected_answer"],
            "gold": q["gold"],
        }
        if "filter" in q:
            case["filter"] = q["filter"]
        cases.append(case)
    for u in UNANSWERABLE_CASES:
        cases.append(dict(u))
    return cases


def build_and_validate(
    day6_root: Path = DEFAULT_DAY6_ROOT,
    output_dir: Path = PROJECT_ROOT / "data",
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Export Day 6 Strategy B chunks + converted questions + unanswerable agent cases."""
    starter_dir = PROJECT_ROOT / "starter"
    if str(starter_dir) not in sys.path:
        sys.path.insert(0, str(starter_dir))
    from baseline import validate as validate_starter  # type: ignore[import-not-found]

    chunks = export_day6_chunks_from_pdfs(day6_root=day6_root, max_size=1000)
    raw_questions = json.loads(
        (day6_root / "benchmark" / "questions.json").read_text(encoding="utf-8")
    )
    questions = [convert_day6_question(q) for q in raw_questions]

    # Verify every answerable gold evidence string appears verbatim in a chunk on (source_id, page).
    validate_starter(chunks, questions)

    cases = build_agent_cases(questions)
    write_json(output_dir / "nist_chunks.json", chunks)
    write_json(output_dir / "nist_questions.json", questions)
    write_json(output_dir / "nist_cases.json", cases)
    return chunks, questions, cases


def main() -> None:
    parser = argparse.ArgumentParser(description="Export and validate Day 7 NIST dataset from Day 6.")
    parser.add_argument("--day6-root", type=Path, default=DEFAULT_DAY6_ROOT)
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "data")
    args = parser.parse_args()

    chunks, questions, cases = build_and_validate(args.day6_root, args.output_dir)
    dev_ans = sum(1 for c in cases if c["split"] == "dev" and c["answerable"])
    dev_unans = sum(1 for c in cases if c["split"] == "dev" and not c["answerable"])
    test_ans = sum(1 for c in cases if c["split"] == "test" and c["answerable"])
    test_unans = sum(1 for c in cases if c["split"] == "test" and not c["answerable"])
    print(
        json.dumps(
            {
                "chunks": len(chunks),
                "answerable_questions": len(questions),
                "agent_cases_total": len(cases),
                "dev": {"answerable": dev_ans, "unanswerable": dev_unans},
                "test": {"answerable": test_ans, "unanswerable": test_unans},
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
