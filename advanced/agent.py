"""Multimodal Agentic RAG runner for the Advanced Challenge (Gemini 1.5 154-page PDF)."""
from __future__ import annotations

import base64
import json
import time
from pathlib import Path
from typing import Any

from src.config import PROJECT_ROOT, create_openai_client, estimate_chat_cost_usd, load_settings

from advanced.ingest import CROPS_DIR, RENDERS_DIR
from advanced.store import MultimodalHybridRetriever

SYSTEM_PROMPT = """You are a rigorous Multimodal Document QA Agent analyzing the 154-page Gemini 1.5 Technical Report (arXiv:2403.05530).

Rules:
1. Ground every factual claim strictly in retrieved text chunks and visual images (tables, charts, diagrams) you inspect during this session.
2. Whenever a question asks about a Table or Figure, call `view_image` using its exact `label` (e.g., `label="Figure 3"` or `label="Table 11"`)—never guess `region_id` numbers. Use `view_full_page=true` if you need surrounding context.
3. Whenever a question names a specific benchmark, model, chip, or version (e.g., `GPQA-Diamond`, `AIME 2025`, `DeepSeek-V3`, `H100`), call `check_exact_phrase` on that exact name! If `match_count == 0`, DO NOT substitute a similar-sounding name—immediately call `submit_final_answer` with `decision="abstain"` and `citations=[]`.
4. For multi-hop or prose/probability questions, call `get_page_context` on the relevant page(s) to read the surrounding body text in addition to viewing any chart/table image, and verify evidence from ALL required pages before calling `submit_final_answer`.
5. CRITICAL ABSTENTION RULE: If the specific requested number, benchmark score, optimizer/schedule, threshold, or attribute is NOT stated in the document—or if your answer states that a requested benchmark/model/metric is not mentioned, not reported, or not supported—you MUST set `decision="abstain"` and `citations=[]`. Never set `decision="answered"` when the requested detail is missing.
6. When `decision="answered"`, copy ONLY the exact `chunk_id` or `cite_as` / `image_tag` strings returned by the tools into `citations`—never invent new IDs."""


TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "search_multimodal",
            "description": "Hybrid dense + BM25 search across all 154 pages (text, tables, charts, diagrams).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query."},
                    "top_k": {"type": "integer", "default": 4, "minimum": 1, "maximum": 8},
                    "modality": {
                        "type": "string",
                        "enum": ["text", "table", "chart", "image_diagram"],
                        "description": "Optional modality filter.",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_exact",
            "description": "Exact lexical BM25 search for specific identifiers like 'Table 12', 'Figure 8', 'Kalamang', or benchmark names.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "default": 4, "minimum": 1, "maximum": 8},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_page_context",
            "description": "Fetch all indexed text chunks and visual region IDs on a specific page (optionally ±1 neighbor page).",
            "parameters": {
                "type": "object",
                "properties": {
                    "page": {"type": "integer", "minimum": 1, "maximum": 154},
                    "window": {"type": "integer", "default": 0, "minimum": 0, "maximum": 1},
                },
                "required": ["page"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_exact_phrase",
            "description": "Case-insensitive exact substring check across all 154 pages. Use this to verify whether an exact benchmark/model/term name exists (match_count=0 proves it is absent).",
            "parameters": {
                "type": "object",
                "properties": {
                    "phrase": {"type": "string", "description": "Exact phrase to verify, e.g. 'GPQA-Diamond' or 'AIME 2025'."}
                },
                "required": ["phrase"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "view_image",
            "description": "Inspect the deterministic high-res crop of a Table/Figure (by exact label like 'Figure 3' or region_id) or the full page PNG.",
            "parameters": {
                "type": "object",
                "properties": {
                    "page": {"type": "integer", "minimum": 1, "maximum": 154},
                    "label": {
                        "type": "string",
                        "description": "Exact caption label such as 'Figure 3' or 'Table 11'. Preferred over guessing region_id.",
                    },
                    "region_id": {
                        "type": "string",
                        "description": "Exact region_id returned by a search tool (e.g. 'p008_figure_1').",
                    },
                    "view_full_page": {"type": "boolean", "default": False},
                },
                "required": ["page"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "submit_final_answer",
            "description": "Submit final answer or abstention after gathering and verifying evidence.",
            "parameters": {
                "type": "object",
                "properties": {
                    "decision": {"type": "string", "enum": ["answered", "abstain"]},
                    "answer": {"type": "string"},
                    "citations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of supporting chunk_ids or viewed region/page IDs (empty if abstaining).",
                    },
                    "reason": {"type": "string"},
                },
                "required": ["decision", "answer", "citations", "reason"],
            },
        },
    },
]


def _encode_png(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


class MultimodalAgentRunner:
    def __init__(
        self,
        *,
        model: str = "gpt-4.1-mini",
        max_steps: int = 5,
        max_searches: int = 4,
        max_images: int = 2,
    ) -> None:
        settings = load_settings(require_db=True, require_openai=True)
        self.client = create_openai_client(settings.openai_api_key)
        self.retriever = MultimodalHybridRetriever()
        self.model = model
        self.max_steps = max_steps
        self.max_searches = max_searches
        self.max_images = max_images

    def run_question(self, item: dict[str, Any]) -> dict[str, Any]:
        t0 = time.perf_counter()
        question = item["question"]
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]

        seen_ids: set[str] = set()
        viewed_images: list[str] = []
        search_count = 0
        events: list[dict[str, Any]] = []
        total_prompt = 0
        total_cached = 0
        total_completion = 0
        embed_tokens = 0
        embed_cost = 0.0
        submission: dict[str, Any] | None = None

        try:
            for step in range(1, self.max_steps + 1):
                force_submit = step == self.max_steps
                kwargs: dict[str, Any] = {
                    "model": self.model,
                    "temperature": 0.0,
                    "messages": messages,
                    "tools": TOOLS,
                }
                if force_submit:
                    kwargs["tool_choice"] = {"type": "function", "function": {"name": "submit_final_answer"}}

                resp = self.client.chat.completions.create(**kwargs)
                usage = resp.usage
                if usage:
                    total_prompt += int(usage.prompt_tokens or 0)
                    total_completion += int(usage.completion_tokens or 0)
                    details = getattr(usage, "prompt_tokens_details", None)
                    if details is not None:
                        total_cached += int(getattr(details, "cached_tokens", 0) or 0)

                msg = resp.choices[0].message
                assistant_msg: dict[str, Any] = {"role": "assistant", "content": msg.content or ""}
                if msg.tool_calls:
                    assistant_msg["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                        }
                        for tc in msg.tool_calls
                    ]
                messages.append(assistant_msg)

                if not msg.tool_calls:
                    if step < self.max_steps:
                        messages.append(
                            {
                                "role": "user",
                                "content": "You must call `submit_final_answer` now with your decision, answer, and exact citations.",
                            }
                        )
                        continue
                    break

                pending_image_parts: list[dict[str, Any]] = []

                for tc in msg.tool_calls:
                    fname = tc.function.name
                    args = json.loads(tc.function.arguments or "{}")

                    if fname == "search_multimodal":
                        if search_count >= self.max_searches:
                            msg_limit = json.dumps({"status": "limit_reached", "message": "Search limit reached; call submit_final_answer."})
                            events.append({"step": step, "tool": fname, "args": args, "limit_reached": True})
                            messages.append({"role": "tool", "tool_call_id": tc.id, "content": msg_limit})
                            continue
                        search_count += 1
                        q = args.get("query", "")
                        top_k = min(4, int(args.get("top_k", 3)))
                        mod = args.get("modality")
                        hits, etok, ecost = self.retriever.search_hybrid(q, top_k=top_k, modality=mod)
                        embed_tokens += etok
                        embed_cost += ecost
                        for h in hits:
                            seen_ids.add(h["chunk_id"])
                            seen_ids.add(f"p{h['page']:03d}")
                        payload = [
                            {
                                "chunk_id": h["chunk_id"],
                                "page": h["page"],
                                "modality": h["modality"],
                                "label": h["label"],
                                "crop_path": h["crop_path"],
                                "score": h["score"],
                                "content": h["content"][:900],
                            }
                            for h in hits
                        ]
                        events.append({"step": step, "tool": fname, "args": args, "hit_ids": [h["chunk_id"] for h in hits]})
                        if not payload:
                            content_str = json.dumps({"status": "no_exact_matches", "query": q, "note": "Zero exact lexical matches across all 154 pages."})
                        else:
                            content_str = json.dumps(payload, ensure_ascii=False)
                        messages.append({"role": "tool", "tool_call_id": tc.id, "content": content_str})

                    elif fname == "search_exact":
                        if search_count >= self.max_searches:
                            msg_limit = json.dumps({"status": "limit_reached", "message": "Search limit reached; call submit_final_answer."})
                            events.append({"step": step, "tool": fname, "args": args, "limit_reached": True})
                            messages.append({"role": "tool", "tool_call_id": tc.id, "content": msg_limit})
                            continue
                        search_count += 1
                        q = args.get("query", "")
                        top_k = min(4, int(args.get("top_k", 3)))
                        hits = self.retriever.search_exact(q, top_k=top_k)
                        for h in hits:
                            seen_ids.add(h["chunk_id"])
                            seen_ids.add(f"p{h['page']:03d}")
                        payload = [
                            {
                                "chunk_id": h["chunk_id"],
                                "page": h["page"],
                                "modality": h["modality"],
                                "label": h["label"],
                                "crop_path": h["crop_path"],
                                "score": h["score"],
                                "content": h["content"][:900],
                            }
                            for h in hits
                        ]
                        events.append({"step": step, "tool": fname, "args": args, "hit_ids": [h["chunk_id"] for h in hits]})
                        if not payload:
                            content_str = json.dumps({"status": "no_exact_matches", "query": q, "note": "Zero exact lexical matches across all 154 pages."})
                        else:
                            content_str = json.dumps(payload, ensure_ascii=False)
                        messages.append({"role": "tool", "tool_call_id": tc.id, "content": content_str})

                    elif fname == "get_page_context":
                        if search_count >= self.max_searches:
                            msg_limit = json.dumps({"status": "limit_reached", "message": "Search limit reached; call submit_final_answer."})
                            events.append({"step": step, "tool": fname, "args": args, "limit_reached": True})
                            messages.append({"role": "tool", "tool_call_id": tc.id, "content": msg_limit})
                            continue
                        search_count += 1
                        page = int(args["page"])
                        window = int(args.get("window", 0))
                        chunks = self.retriever.get_page_context(page, window=window)
                        for h in chunks:
                            seen_ids.add(h["chunk_id"])
                            seen_ids.add(f"p{h['page']:03d}")
                        payload = [
                            {
                                "chunk_id": h["chunk_id"],
                                "page": h["page"],
                                "modality": h["modality"],
                                "label": h["label"],
                                "crop_path": h["crop_path"],
                                "content": h["content"][:1000],
                            }
                            for h in chunks
                        ]
                        events.append({"step": step, "tool": fname, "args": args, "chunk_count": len(chunks)})
                        messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(payload, ensure_ascii=False)})

                    elif fname == "check_exact_phrase":
                        if search_count >= self.max_searches:
                            msg_limit = json.dumps({"status": "limit_reached", "message": "Search limit reached; call submit_final_answer."})
                            events.append({"step": step, "tool": fname, "args": args, "limit_reached": True})
                            messages.append({"role": "tool", "tool_call_id": tc.id, "content": msg_limit})
                            continue
                        search_count += 1
                        res = self.retriever.check_exact_phrase(args.get("phrase", ""))
                        for m in res.get("matches", []):
                            seen_ids.add(m["chunk_id"])
                            seen_ids.add(f"p{m['page']:03d}")
                        events.append({"step": step, "tool": fname, "args": args, "match_count": res["match_count"]})
                        messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(res, ensure_ascii=False)})

                    elif fname == "view_image":
                        if len(viewed_images) >= self.max_images:
                            msg_limit = json.dumps({"status": "limit_reached", "message": "Image view limit reached; call submit_final_answer."})
                            events.append({"step": step, "tool": fname, "args": args, "limit_reached": True})
                            messages.append({"role": "tool", "tool_call_id": tc.id, "content": msg_limit})
                            continue
                        page = int(args["page"])
                        label_arg = (args.get("label") or "").strip().lower()
                        region_id = args.get("region_id")
                        if label_arg and label_arg in self.retriever.by_label:
                            matched_chunk = self.retriever.by_label[label_arg]
                            page = int(matched_chunk["page"])
                            region_id = matched_chunk["chunk_id"].split(":")[-1]
                        view_full = bool(args.get("view_full_page", False))
                        img_path: Path | None = None
                        tag = f"p{page:03d}"
                        if region_id and not view_full:
                            cand = CROPS_DIR / f"{region_id}.png"
                            if cand.exists():
                                img_path = cand
                                tag = region_id
                                seen_ids.add(region_id)
                                seen_ids.add(f"gemini-1-5-report:{region_id}")
                        if img_path is None:
                            cand = RENDERS_DIR / f"p{page:03d}.png"
                            if cand.exists():
                                img_path = cand
                                tag = f"p{page:03d}_full"
                        seen_ids.add(f"p{page:03d}")
                        seen_ids.add(tag)

                        if img_path and img_path.exists():
                            viewed_images.append(tag)
                            pending_image_parts.append({"type": "text", "text": f"Image for {tag} (page {page}):"})
                            pending_image_parts.append(
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/png;base64,{_encode_png(img_path)}", "detail": "high"},
                                }
                            )
                            tool_resp = {"status": "ok", "image_tag": tag, "cite_as": tag, "page": page}
                        else:
                            tool_resp = {"status": "not_found", "page": page, "region_id": region_id}
                        events.append({"step": step, "tool": fname, "args": args, "result": tool_resp})
                        messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(tool_resp)})

                    elif fname == "submit_final_answer":
                        decision = args.get("decision", "abstain")
                        raw_cits = [str(c).strip().strip("[]") for c in (args.get("citations") or [])]
                        valid_cits = [c for c in raw_cits if c in seen_ids]
                        if decision == "answered" and not valid_cits:
                            decision = "abstain"
                        if decision == "abstain":
                            valid_cits = []
                        submission = {
                            "decision": decision,
                            "answer": args.get("answer", ""),
                            "citations": valid_cits,
                            "raw_citations": raw_cits,
                            "reason": args.get("reason", ""),
                        }
                        events.append({"step": step, "tool": fname, "args": submission})
                        messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps({"status": "submitted"})})

                if pending_image_parts:
                    messages.append({"role": "user", "content": pending_image_parts})

                if submission is not None:
                    break

            chat_cost = estimate_chat_cost_usd(self.model, total_prompt, total_cached, total_completion)
            return {
                "id": item["id"],
                "category": item["category"],
                "question": question,
                "status": "ok" if submission is not None else "error",
                "decision": submission["decision"] if submission else "error",
                "answer": submission["answer"] if submission else "",
                "citations": submission["citations"] if submission else [],
                "viewed_images": viewed_images,
                "events": events,
                "latency_ms": round((time.perf_counter() - t0) * 1000.0, 2),
                "chat_cost_usd": round(chat_cost, 6),
                "embed_cost_usd": round(embed_cost, 6),
                "total_cost_usd": round(chat_cost + embed_cost, 6),
                "error": None if submission is not None else "Agent ended without calling submit_final_answer",
            }
        except Exception as exc:
            return {
                "id": item["id"],
                "category": item["category"],
                "question": question,
                "status": "error",
                "decision": "error",
                "answer": "",
                "citations": [],
                "viewed_images": viewed_images,
                "events": events,
                "latency_ms": round((time.perf_counter() - t0) * 1000.0, 2),
                "chat_cost_usd": 0.0,
                "embed_cost_usd": round(embed_cost, 6),
                "total_cost_usd": round(embed_cost, 6),
                "error": f"{type(exc).__name__}: {exc}",
            }
