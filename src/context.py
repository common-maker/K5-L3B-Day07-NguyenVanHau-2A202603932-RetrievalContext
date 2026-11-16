"""Context engineering utilities: formatting, dedup packing, and neighbor expansion."""
from __future__ import annotations

import re
from typing import Any


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def evidence_hit(chunk: dict[str, Any], gold: list[dict[str, Any]]) -> bool:
    """Return True if any gold entry matches chunk source_id, page, and normalized evidence substring."""
    norm_text = collapse_ws(chunk["text"])
    return any(
        chunk["source_id"] == g["source_id"]
        and int(chunk["page"]) == int(g["page"])
        and collapse_ws(g["evidence"]) in norm_text
        for g in gold
    )


def format_chunk_block(chunk: dict[str, Any]) -> str:
    """Format a chunk with explicit provenance metadata for model context."""
    section = chunk.get("metadata", {}).get("section", "")
    year = chunk.get("metadata", {}).get("year", "")
    header = f"[{chunk['id']} | {chunk['source_id']} | p.{chunk['page']}"
    if section:
        header += f" | section={section}"
    if year:
        header += f" | year={year}"
    header += "]"
    return f"{header}\n{chunk['text']}"


class ChunkCorpusIndex:
    """Lookup helper enabling deterministic adjacent-chunk expansion."""

    def __init__(self, chunks: list[dict[str, Any]]) -> None:
        ordered = sorted(chunks, key=lambda c: (c["source_id"], int(c["page"]), c["id"]))
        self.ordered = ordered
        self.by_id: dict[str, dict[str, Any]] = {c["id"]: c for c in ordered}
        self._pos: dict[str, int] = {c["id"]: idx for idx, c in enumerate(ordered)}

    def get_neighbors(self, chunk_id: str, window: int = 1) -> list[dict[str, Any]]:
        """Return adjacent chunks within the same document (`source_id`)."""
        if chunk_id not in self._pos or window < 1:
            return []
        idx = self._pos[chunk_id]
        doc_id = self.ordered[idx]["source_id"]
        neighbors: list[dict[str, Any]] = []
        for offset in range(-window, window + 1):
            if offset == 0:
                continue
            pos = idx + offset
            if 0 <= pos < len(self.ordered) and self.ordered[pos]["source_id"] == doc_id:
                neighbors.append(self.ordered[pos])
        return neighbors


def pack_context(
    candidates: list[dict[str, Any]],
    *,
    budget_chars: int = 800,
    corpus_index: ChunkCorpusIndex | None = None,
    expand_neighbors: bool = False,
    neighbor_top_n: int = 1,
) -> tuple[str, list[str]]:
    """Pack deduplicated chunks into context up to `budget_chars`.

    Optionally expands immediate same-document neighbor chunks for the top-ranked
    hits to repair page-boundary breaks or recover parent headers.
    """
    if budget_chars < 1:
        raise ValueError("budget_chars must be >= 1.")

    expanded: list[dict[str, Any]] = []
    for idx, cand in enumerate(candidates):
        expanded.append(cand)
        if expand_neighbors and corpus_index is not None and idx < neighbor_top_n:
            expanded.extend(corpus_index.get_neighbors(cand["id"], window=1))

    blocks: list[str] = []
    ids: list[str] = []
    seen: set[str] = set()
    for chunk in expanded:
        cid = chunk["id"]
        if cid in seen:
            continue
        seen.add(cid)
        block = format_chunk_block(chunk)
        candidate_ctx = "\n\n".join(blocks + [block])
        if len(candidate_ctx) <= budget_chars:
            blocks.append(block)
            ids.append(cid)

    return "\n\n".join(blocks), ids
