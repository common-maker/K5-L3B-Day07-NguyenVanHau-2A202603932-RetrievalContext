"""Benchmark validation, agent evaluation runner, worksheet generator, and strict scorer."""
from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any

from advanced.ingest import DATA_DIR, RESULTS_DIR

BENCHMARK_PATH = DATA_DIR / "benchmark.json"


def _normalize_q(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", text.lower())).strip()


def validate_benchmark(benchmark_path: Path = BENCHMARK_PATH) -> dict[str, Any]:
    data = json.loads(benchmark_path.read_text(encoding="utf-8"))
    dev = data.get("dev", [])
    test = data.get("test", [])

    all_ids = [x["id"] for x in dev + test]
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("Duplicate benchmark IDs found.")

    dev_qs = {_normalize_q(x["question"]) for x in dev}
    test_qs = {_normalize_q(x["question"]) for x in test}
    overlap = dev_qs & test_qs
    if overlap:
        raise ValueError(f"Normalized question overlap between dev and test: {overlap}")

    dev_counts = Counter(x["category"] for x in dev)
    test_counts = Counter(x["category"] for x in test)

    dev_answerable = sum(v for k, v in dev_counts.items() if k != "unanswerable")
    if dev_answerable < 15 or dev_counts["unanswerable"] < 3:
        raise ValueError(f"dev split must have >=15 answerable and >=3 unanswerable, got {dict(dev_counts)}")

    req_test = {
        "table": 6,
        "image_diagram": 5,
        "chart": 5,
        "multi_hop": 4,
        "text": 4,
        "unanswerable": 6,
    }
    for cat, minimum in req_test.items():
        if test_counts[cat] < minimum:
            raise ValueError(f"test split category '{cat}' requires >= {minimum}, got {test_counts[cat]}")

    if len(test) < 30:
        raise ValueError(f"test split requires >= 30 items, got {len(test)}")

    return {
        "status": "valid",
        "dev_total": len(dev),
        "dev_by_category": dict(dev_counts),
        "test_total": len(test),
        "test_by_category": dict(test_counts),
    }


def write_audit_worksheet(
    items: list[dict[str, Any]],
    traces: list[dict[str, Any]],
    out_path: Path,
) -> None:
    by_id = {t["id"]: t for t in traces}
    lines = ["# Advanced Multimodal Audit Worksheet", ""]
    for idx, item in enumerate(items, 1):
        tr = by_id[item["id"]]
        lines.append(f"## {idx}. `{item['id']}` (`{item['category']}`)")
        lines.append(f"- **Question:** {item['question']}")
        lines.append(f"- **Gold / Expected:** {item.get('expected_answer', '')}")
        lines.append(f"- **Gold Evidence:** {item.get('evidence', '')} (pages: {item.get('pages', [])})")
        lines.append(f"- **Status:** `{tr['status']}` | **Decision:** `{tr['decision']}` | **Viewed:** `{tr['viewed_images']}`")
        lines.append(f"- **Citations:** `{tr['citations']}`")
        lines.append(f"- **Agent Answer:** {tr['answer']}")
        if tr.get("error"):
            lines.append(f"- **Error:** `{tr['error']}`")
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def score_reviews(
    items: list[dict[str, Any]],
    traces: list[dict[str, Any]],
    reviews: list[dict[str, Any]],
) -> dict[str, Any]:
    trace_by_id = {t["id"]: t for t in traces}
    rev_by_id = {r["id"]: r for r in reviews}
    if len(rev_by_id) != len(items):
        missing = [x["id"] for x in items if x["id"] not in rev_by_id]
        raise ValueError(f"Missing reviews for IDs: {missing}")

    cat_pass: Counter[str] = Counter()
    cat_total: Counter[str] = Counter()
    passed = 0
    errors = 0

    for item in items:
        qid = item["id"]
        cat = item["category"]
        cat_total[cat] += 1
        tr = trace_by_id[qid]
        rev = rev_by_id[qid]
        if tr["status"] != "ok":
            errors += 1
            is_pass = False
        else:
            is_pass = bool(rev["pass"])
        if is_pass:
            passed += 1
            cat_pass[cat] += 1

    total = len(items)
    pct = (passed / total * 100.0) if total else 0.0
    total_ms = round(sum(float(t.get("latency_ms", 0.0)) for t in traces), 2)
    total_cost = round(sum(float(t.get("total_cost_usd", 0.0)) for t in traces), 6)

    by_category = {
        cat: {
            "passed": cat_pass[cat],
            "total": cat_total[cat],
            "ratio": f"{cat_pass[cat]}/{cat_total[cat]}",
            "pct": round(cat_pass[cat] / cat_total[cat] * 100.0, 2) if cat_total[cat] else 0.0,
        }
        for cat in sorted(cat_total)
    }
    return {
        "total": total,
        "passed": passed,
        "ratio": f"{passed}/{total}",
        "pass_pct": round(pct, 2),
        "meets_90pct_threshold": pct >= 90.0,
        "errors": errors,
        "total_latency_ms": total_ms,
        "total_cost_usd": total_cost,
        "by_category": by_category,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate, run, and score Advanced Multimodal benchmark.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--benchmark", default=str(BENCHMARK_PATH))

    p_run = sub.add_parser("run")
    p_run.add_argument("--split", choices=["dev", "test"], required=True)
    p_run.add_argument("--tag", default="v1")
    p_run.add_argument("--model", default="gpt-4.1-mini")
    p_run.add_argument("--max-steps", type=int, default=5)
    p_run.add_argument("--benchmark", default=str(BENCHMARK_PATH))

    p_score = sub.add_parser("score")
    p_score.add_argument("--split", choices=["dev", "test"], required=True)
    p_score.add_argument("--tag", required=True)
    p_score.add_argument("--reviews", required=True)
    p_score.add_argument("--benchmark", default=str(BENCHMARK_PATH))

    args = parser.parse_args()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    bm_path = Path(args.benchmark)

    if args.cmd == "validate":
        print(json.dumps(validate_benchmark(bm_path), indent=2))
        return

    data = json.loads(bm_path.read_text(encoding="utf-8"))
    items = data[args.split]

    if args.cmd == "run":
        from advanced.agent import MultimodalAgentRunner

        runner = MultimodalAgentRunner(model=args.model, max_steps=args.max_steps)
        t0 = time.perf_counter()
        traces: list[dict[str, Any]] = []
        for idx, item in enumerate(items, 1):
            tr = runner.run_question(item)
            traces.append(tr)
            print(
                f"[{idx}/{len(items)}] {item['id']} ({item['category']}) -> {tr['decision']} "
                f"| viewed={len(tr['viewed_images'])} | cost=${tr['total_cost_usd']:.4f} | {tr['latency_ms']:.0f}ms",
                flush=True,
            )

        traces_path = RESULTS_DIR / f"{args.split}_{args.tag}_traces.json"
        stats_path = RESULTS_DIR / f"{args.split}_{args.tag}_run_stats.json"
        worksheet_path = RESULTS_DIR / f"{args.split}_{args.tag}_audit_worksheet.md"

        traces_path.write_text(json.dumps(traces, indent=2, ensure_ascii=False), encoding="utf-8")
        write_audit_worksheet(items, traces, worksheet_path)
        run_stats = {
            "split": args.split,
            "tag": args.tag,
            "model": args.model,
            "cases": len(traces),
            "answered": sum(1 for t in traces if t["decision"] == "answered"),
            "abstain": sum(1 for t in traces if t["decision"] == "abstain"),
            "errors": sum(1 for t in traces if t["status"] != "ok"),
            "total_cost_usd": round(sum(t["total_cost_usd"] for t in traces), 6),
            "total_elapsed_s": round(time.perf_counter() - t0, 2),
        }
        stats_path.write_text(json.dumps(run_stats, indent=2), encoding="utf-8")
        print(json.dumps(run_stats, indent=2))
        return

    if args.cmd == "score":
        traces_path = RESULTS_DIR / f"{args.split}_{args.tag}_traces.json"
        traces = json.loads(traces_path.read_text(encoding="utf-8"))
        reviews = json.loads(Path(args.reviews).read_text(encoding="utf-8"))
        summary = score_reviews(items, traces, reviews)
        out_path = RESULTS_DIR / f"{args.split}_{args.tag}_summary.json"
        out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
