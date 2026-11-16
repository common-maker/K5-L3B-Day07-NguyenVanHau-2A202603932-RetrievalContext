"""Deterministic multimodal ingestion for Gemini 1.5 Technical Report (arXiv:2403.05530, 154 pages).

Stages:
  1. extract: Downloads PDF, renders all 154 pages, extracts per-page text +
     deterministic PDF bounding-box crops for every captioned Table and Figure (no LLM-guessed bboxes).
  2. vision: Calls gpt-4.1-mini Vision on deterministic crops to produce structured
     searchable cards for retrieval (never used to guess crop coordinates).
  3. chunks: Combines page text chunks + structured visual/table cards into
     advanced/data/multimodal_chunks.json + advanced/data/index_stats.json.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import time
from pathlib import Path
from typing import Any

import httpx

from src.config import PROJECT_ROOT, create_openai_client, estimate_chat_cost_usd, load_settings

ADV_ROOT = PROJECT_ROOT / "advanced"
RAW_DIR = ADV_ROOT / "raw"
RENDERS_DIR = ADV_ROOT / "renders"
CROPS_DIR = ADV_ROOT / "crops"
DATA_DIR = ADV_ROOT / "data"
RESULTS_DIR = ADV_ROOT / "results"

PDF_URL = "https://arxiv.org/pdf/2403.05530.pdf"
PDF_PATH = RAW_DIR / "gemini_1_5_2403.05530.pdf"
DOC_ID = "gemini-1-5-report"
DOC_TITLE = "Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context"
DOC_VERSION = "arXiv:2403.05530v5 (Dec 2024)"
DOC_LICENSE = "arXiv.org perpetual, non-exclusive license / Google DeepMind Technical Report (public access)"

PAGE_META_PATH = DATA_DIR / "pages_meta.json"
VISUAL_CARDS_PATH = DATA_DIR / "visual_cards.json"
CHUNKS_PATH = DATA_DIR / "multimodal_chunks.json"
INDEX_STATS_PATH = DATA_DIR / "index_stats.json"

CAPTION_RE = re.compile(r"^(Figure|Table)\s+(\d+)\s*\|")
PAGE_RENDER_DPI = 150
CROP_RENDER_DPI = 220


def ensure_dirs() -> None:
    for d in (RAW_DIR, RENDERS_DIR, CROPS_DIR, DATA_DIR, RESULTS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def download_pdf(pdf_path: Path = PDF_PATH) -> Path:
    ensure_dirs()
    if pdf_path.exists() and pdf_path.stat().st_size > 1_000_000:
        return pdf_path
    with httpx.Client(follow_redirects=True, timeout=90.0, verify=False) as client:
        resp = client.get(PDF_URL)
        resp.raise_for_status()
        pdf_path.write_bytes(resp.content)
    return pdf_path


def _group_words_into_lines(words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = []
    for w in sorted(words, key=lambda x: (round(x["top"], 1), x["x0"])):
        if not lines or abs(w["top"] - lines[-1]["top"]) > 3.5:
            lines.append(
                {
                    "top": float(w["top"]),
                    "bottom": float(w["bottom"]),
                    "x0": float(w["x0"]),
                    "x1": float(w["x1"]),
                    "text": w["text"],
                }
            )
        else:
            lines[-1]["text"] += " " + w["text"]
            lines[-1]["bottom"] = max(lines[-1]["bottom"], float(w["bottom"]))
            lines[-1]["x0"] = min(lines[-1]["x0"], float(w["x0"]))
            lines[-1]["x1"] = max(lines[-1]["x1"], float(w["x1"]))
    return lines


def _extract_caption_blocks(page: Any, lines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Find every 'Figure N | ...' or 'Table N | ...' caption via pdfplumber page.search()."""
    hits = page.search(r"(?:Figure|Table)\s+\d+\s*\|", regex=True)
    if not hits:
        return []
    hits = sorted(hits, key=lambda h: (float(h["top"]), float(h["x0"])))

    caps: list[dict[str, Any]] = []
    for h in hits:
        label = h["text"].rstrip("| ").strip()
        kind = "table" if label.startswith("Table") else "figure"
        num = int(re.search(r"\d+", label).group(0))
        htop = float(h["top"])
        hbot = float(h["bottom"])
        hx0 = float(h["x0"])
        hx1 = float(h["x1"])

        start_idx = None
        for idx, ln in enumerate(lines):
            if abs(ln["top"] - htop) <= 6.0 and ln["bottom"] >= htop and ln["top"] <= hbot + 2.0:
                start_idx = idx
                break

        if start_idx is None:
            caps.append(
                {
                    "kind": kind,
                    "number": num,
                    "label": label,
                    "caption": label,
                    "cap_bbox": [round(hx0, 2), round(htop, 2), round(hx1, 2), round(hbot, 2)],
                }
            )
            continue

        cap_top = min(htop, lines[start_idx]["top"])
        cap_bottom = max(hbot, lines[start_idx]["bottom"])
        cap_x0 = min(hx0, lines[start_idx]["x0"])
        cap_x1 = max(hx1, lines[start_idx]["x1"])
        texts = [lines[start_idx]["text"].strip()]

        j = start_idx + 1
        while j < len(lines):
            gap = lines[j]["top"] - cap_bottom
            nxt = lines[j]["text"].strip()
            if gap > 8.0 or CAPTION_RE.match(nxt) or re.match(r"^\d+(\.\d+)*\s+[A-Z]", nxt):
                break
            if len(texts) >= 6:
                break
            texts.append(nxt)
            cap_bottom = lines[j]["bottom"]
            cap_x0 = min(cap_x0, lines[j]["x0"])
            cap_x1 = max(cap_x1, lines[j]["x1"])
            j += 1

        caps.append(
            {
                "kind": kind,
                "number": num,
                "label": label,
                "caption": " ".join(texts),
                "cap_bbox": [round(cap_x0, 2), round(cap_top, 2), round(cap_x1, 2), round(cap_bottom, 2)],
            }
        )
    return caps


def _compute_deterministic_bbox(
    page: Any,
    cap: dict[str, Any],
    prev_cap_bottom: float,
    lines: list[dict[str, Any]],
) -> list[float]:
    """Compute exact PDF bounding box [x0, y0, x1, y1] in points using PDF layout objects."""
    pw, ph = float(page.width), float(page.height)
    cx0, ctop, cx1, cbot = cap["cap_bbox"]
    band_top_min = max(48.0, prev_cap_bottom + 6.0)
    band_bot_max = ctop - 1.0

    if cap["kind"] == "figure":
        objs = []
        for obj in list(page.images) + list(page.rects) + list(page.curves) + list(page.lines):
            otop = float(obj.get("top", 0.0))
            obottom = float(obj.get("bottom", 0.0))
            ox0 = float(obj.get("x0", 0.0))
            ox1 = float(obj.get("x1", 0.0))
            if otop < 46.0 or obottom > ph - 35.0:
                continue
            if obottom >= band_top_min and otop <= band_bot_max:
                objs.append((ox0, otop, ox1, obottom))
        if objs:
            x0 = max(20.0, min(min(o[0] for o in objs), cx0) - 16.0)
            y0 = max(42.0, min(o[1] for o in objs) - 14.0)
            x1 = min(pw - 20.0, max(max(o[2] for o in objs), cx1) + 16.0)
            y1 = min(ph - 24.0, cbot + 10.0)
            if y1 - y0 >= 40.0:
                return [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)]

    h_rules = []
    for obj in list(page.lines) + list(page.rects):
        otop = float(obj.get("top", 0.0))
        obottom = float(obj.get("bottom", 0.0))
        ox0 = float(obj.get("x0", 0.0))
        ox1 = float(obj.get("x1", 0.0))
        if otop < 46.0 or obottom > ph - 35.0:
            continue
        if (ox1 - ox0) > 100.0 and otop >= band_top_min and obottom <= band_bot_max:
            h_rules.append((ox0, otop, ox1, obottom))

    if h_rules:
        x0 = max(20.0, min(min(r[0] for r in h_rules), cx0) - 16.0)
        y0 = max(42.0, min(r[1] for r in h_rules) - 14.0)
        x1 = min(pw - 20.0, max(max(r[2] for r in h_rules), cx1) + 16.0)
        y1 = min(ph - 24.0, cbot + 10.0)
        if y1 - y0 >= 35.0:
            return [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)]

    band_lines = [l for l in lines if l["top"] >= band_top_min and l["bottom"] <= band_bot_max]
    y0 = band_lines[0]["top"] - 10.0 if band_lines else max(42.0, ctop - 220.0)
    return [24.0, round(max(42.0, y0), 2), round(pw - 24.0, 2), round(min(ph - 24.0, cbot + 10.0), 2)]


def classify_page_section(page_num: int, text: str) -> str:
    if page_num <= 2:
        return "front_matter"
    if 75 <= page_num <= 98:
        return "references"
    if 99 <= page_num <= 106:
        return "contributors_acknowledgments"
    if page_num >= 107:
        return "appendix"
    return "main_body"


def extract_pages_and_crops(pdf_path: Path = PDF_PATH) -> list[dict[str, Any]]:
    import pdfplumber
    import pypdfium2 as pdfium
    from PIL import Image

    ensure_dirs()
    pdf_doc = pdfium.PdfDocument(str(pdf_path))
    pages_meta: list[dict[str, Any]] = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for idx in range(total_pages):
            pno = idx + 1
            page = pdf.pages[idx]
            pw, ph = float(page.width), float(page.height)
            raw_text = (page.extract_text() or "").strip()
            layout_text = (page.extract_text(layout=True) or "").strip()

            render_path = RENDERS_DIR / f"p{pno:03d}.png"
            if not render_path.exists():
                bitmap = pdf_doc[idx].render(scale=PAGE_RENDER_DPI / 72.0)
                bitmap.to_pil().save(render_path, format="PNG")

            words = page.extract_words(keep_blank_chars=False)
            lines = _group_words_into_lines(words)
            caps = _extract_caption_blocks(page, lines)

            regions: list[dict[str, Any]] = []
            prev_bottom = 42.0
            high_res_img: Image.Image | None = None
            scale = CROP_RENDER_DPI / 72.0

            for r_idx, cap in enumerate(caps, 1):
                bbox_pt = _compute_deterministic_bbox(page, cap, prev_bottom, lines)
                prev_bottom = cap["cap_bbox"][3]

                crop_filename = f"p{pno:03d}_{cap['kind']}_{r_idx}.png"
                crop_path = CROPS_DIR / crop_filename
                if not crop_path.exists():
                    if high_res_img is None:
                        high_res_img = pdf_doc[idx].render(scale=scale).to_pil()
                    ix0 = max(0, int(bbox_pt[0] * scale))
                    iy0 = max(0, int(bbox_pt[1] * scale))
                    ix1 = min(high_res_img.width, int(bbox_pt[2] * scale))
                    iy1 = min(high_res_img.height, int(bbox_pt[3] * scale))
                    if ix1 > ix0 + 10 and iy1 > iy0 + 10:
                        high_res_img.crop((ix0, iy0, ix1, iy1)).save(crop_path, format="PNG")

                bbox_norm = [
                    round(bbox_pt[0] / pw * 1000, 1),
                    round(bbox_pt[1] / ph * 1000, 1),
                    round(bbox_pt[2] / pw * 1000, 1),
                    round(bbox_pt[3] / ph * 1000, 1),
                ]
                regions.append(
                    {
                        "region_id": f"p{pno:03d}_{cap['kind']}_{r_idx}",
                        "kind": cap["kind"],
                        "label": cap["label"],
                        "caption": cap["caption"],
                        "bbox_pt": bbox_pt,
                        "bbox_norm": bbox_norm,
                        "crop_path": str(crop_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                    }
                )

            section = classify_page_section(pno, raw_text)
            pages_meta.append(
                {
                    "page": pno,
                    "section": section,
                    "width_pt": round(pw, 2),
                    "height_pt": round(ph, 2),
                    "text_chars": len(raw_text),
                    "text": raw_text,
                    "layout_text": layout_text,
                    "num_images": len(page.images),
                    "num_rects": len(page.rects),
                    "num_curves": len(page.curves),
                    "render_path": str(render_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                    "regions": regions,
                }
            )

    PAGE_META_PATH.write_text(json.dumps(pages_meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return pages_meta


def _encode_image_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def build_vision_cards(
    pages_meta: list[dict[str, Any]],
    *,
    model: str = "gpt-4.1-mini",
) -> dict[str, Any]:
    """Enrich every deterministic crop with a structured searchable description using Vision."""
    settings = load_settings(require_db=False, require_openai=True)
    client = create_openai_client(settings.openai_api_key)

    existing: dict[str, dict[str, Any]] = {}
    if VISUAL_CARDS_PATH.exists():
        for card in json.loads(VISUAL_CARDS_PATH.read_text(encoding="utf-8")):
            existing[card["region_id"]] = card

    cards: list[dict[str, Any]] = []
    total_cost = 0.0
    total_prompt_tokens = 0
    total_completion_tokens = 0

    for pm in pages_meta:
        pno = pm["page"]
        for reg in pm["regions"]:
            rid = reg["region_id"]
            if rid in existing:
                cards.append(existing[rid])
                continue
            crop_abs = PROJECT_ROOT / reg["crop_path"]
            if not crop_abs.exists():
                continue

            prompt = (
                f"You are indexing page {pno} of the Gemini 1.5 Technical Report.\n"
                f"Region label: {reg['label']}\n"
                f"Caption: {reg['caption']}\n\n"
                "Analyze this cropped figure/table image and return strict JSON with keys:\n"
                '- "modality": one of "table", "chart", "image_diagram"\n'
                '- "title": short descriptive title including the label\n'
                '- "summary": 2-4 factual sentences describing what is shown, axes/legends/units if chart, columns/rows if table, or components if diagram\n'
                '- "structured_content": full Markdown table (for tables) or bulleted key values/data points/observations (for charts and diagrams)\n'
                '- "keywords": list of 5-10 key terms, model names, benchmarks, or units\n'
                "Only state values clearly visible in the image. Do not guess illegible numbers."
            )

            resp = client.chat.completions.create(
                model=model,
                temperature=0.0,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{_encode_image_b64(crop_abs)}",
                                    "detail": "high",
                                },
                            },
                        ],
                    }
                ],
            )
            usage = resp.usage
            pt = int(usage.prompt_tokens or 0) if usage else 0
            ct = int(usage.completion_tokens or 0) if usage else 0
            total_prompt_tokens += pt
            total_completion_tokens += ct
            total_cost += estimate_chat_cost_usd(model, pt, 0, ct)

            parsed = json.loads(resp.choices[0].message.content or "{}")
            card = {
                "region_id": rid,
                "page": pno,
                "section": pm["section"],
                "label": reg["label"],
                "caption": reg["caption"],
                "bbox_pt": reg["bbox_pt"],
                "bbox_norm": reg["bbox_norm"],
                "crop_path": reg["crop_path"],
                "render_path": pm["render_path"],
                "modality": parsed.get("modality", reg["kind"]),
                "title": parsed.get("title", reg["label"]),
                "summary": parsed.get("summary", ""),
                "structured_content": parsed.get("structured_content", ""),
                "keywords": parsed.get("keywords", []),
            }
            cards.append(card)
            existing[rid] = card
            VISUAL_CARDS_PATH.write_text(json.dumps(cards, indent=2, ensure_ascii=False), encoding="utf-8")

    VISUAL_CARDS_PATH.write_text(json.dumps(cards, indent=2, ensure_ascii=False), encoding="utf-8")
    return {
        "cards_count": len(cards),
        "prompt_tokens": total_prompt_tokens,
        "completion_tokens": total_completion_tokens,
        "vision_cost_usd": round(total_cost, 6),
    }


def _chunk_text(text: str, max_chars: int = 1200, overlap_chars: int = 150) -> list[str]:
    text = text.strip()
    if not text:
        return []
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if len(paragraphs) == 1 and len(paragraphs[0]) > max_chars:
        paragraphs = [p.strip() for p in text.splitlines() if p.strip()]

    chunks: list[str] = []
    cur: list[str] = []
    cur_len = 0
    for para in paragraphs:
        if cur and cur_len + len(para) + 1 > max_chars:
            joined = "\n".join(cur)
            chunks.append(joined)
            tail = joined[-overlap_chars:] if overlap_chars > 0 and len(joined) > overlap_chars else ""
            cur = [tail, para] if tail else [para]
            cur_len = sum(len(x) for x in cur) + len(cur)
        else:
            cur.append(para)
            cur_len += len(para) + 1
    if cur:
        chunks.append("\n".join(cur))
    return chunks


def build_multimodal_chunks(
    pages_meta: list[dict[str, Any]],
    cards: list[dict[str, Any]],
    vision_meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    chunks: list[dict[str, Any]] = []

    for pm in pages_meta:
        pno = pm["page"]
        sec = pm["section"]
        src_text = pm["layout_text"] if pm["regions"] else pm["text"]
        text_parts = _chunk_text(src_text, max_chars=1200, overlap_chars=150)
        for idx, part in enumerate(text_parts):
            chunks.append(
                {
                    "chunk_id": f"{DOC_ID}:p{pno:03d}:text:{idx:03d}",
                    "doc_id": DOC_ID,
                    "page": pno,
                    "section": sec,
                    "modality": "text",
                    "label": f"Page {pno} text",
                    "bbox_pt": None,
                    "bbox_norm": None,
                    "crop_path": None,
                    "render_path": pm["render_path"],
                    "content": part,
                }
            )

    for card in cards:
        pno = card["page"]
        kw_line = ", ".join(str(k) for k in card.get("keywords", []))
        content = (
            f"[{card['label']}] {card['title']}\n"
            f"Caption: {card['caption']}\n"
            f"Summary: {card['summary']}\n"
            f"Details:\n{card['structured_content']}\n"
            f"Keywords: {kw_line}"
        ).strip()
        chunks.append(
            {
                "chunk_id": f"{DOC_ID}:{card['region_id']}",
                "doc_id": DOC_ID,
                "page": pno,
                "section": card["section"],
                "modality": card["modality"],
                "label": card["label"],
                "bbox_pt": card["bbox_pt"],
                "bbox_norm": card["bbox_norm"],
                "crop_path": card["crop_path"],
                "render_path": card["render_path"],
                "content": content,
            }
        )

    CHUNKS_PATH.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")

    by_modality: dict[str, int] = {}
    by_section: dict[str, int] = {}
    for ch in chunks:
        by_modality[ch["modality"]] = by_modality.get(ch["modality"], 0) + 1
        by_section[ch["section"]] = by_section.get(ch["section"], 0) + 1

    stats = {
        "doc_id": DOC_ID,
        "title": DOC_TITLE,
        "version": DOC_VERSION,
        "source_url": PDF_URL,
        "license": DOC_LICENSE,
        "total_pages": len(pages_meta),
        "pages_indexed": len({ch["page"] for ch in chunks}),
        "total_regions_cropped": sum(len(pm["regions"]) for pm in pages_meta),
        "total_chunks": len(chunks),
        "chunks_by_modality": by_modality,
        "chunks_by_section": by_section,
        "vision_indexing": vision_meta or {},
    }
    INDEX_STATS_PATH.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest Gemini 1.5 PDF with deterministic bbox crops.")
    parser.add_argument("--stage", choices=["extract", "vision", "chunks", "all"], default="all")
    parser.add_argument("--vision-model", default="gpt-4.1-mini")
    args = parser.parse_args()

    t0 = time.perf_counter()
    pdf_path = download_pdf()

    if args.stage in ("extract", "all"):
        pages_meta = extract_pages_and_crops(pdf_path)
        print(f"Extracted {len(pages_meta)} pages and {sum(len(p['regions']) for p in pages_meta)} deterministic crops.")
    else:
        pages_meta = json.loads(PAGE_META_PATH.read_text(encoding="utf-8"))

    vision_meta: dict[str, Any] = {}
    if args.stage in ("vision", "all"):
        vision_meta = build_vision_cards(pages_meta, model=args.vision_model)
        print("Vision indexing:", json.dumps(vision_meta))

    if args.stage in ("chunks", "all"):
        cards = json.loads(VISUAL_CARDS_PATH.read_text(encoding="utf-8")) if VISUAL_CARDS_PATH.exists() else []
        stats = build_multimodal_chunks(pages_meta, cards, vision_meta=vision_meta)
        stats["elapsed_s"] = round(time.perf_counter() - t0, 2)
        INDEX_STATS_PATH.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
