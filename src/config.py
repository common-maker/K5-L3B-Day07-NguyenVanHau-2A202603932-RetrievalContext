"""Environment configuration and OpenAI token/cost accounting helpers."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DAY6_ROOT = PROJECT_ROOT.parent / "K5-L3-Day06-DataIngestionEngineering"

# Official OpenAI API list pricing (USD per 1M tokens).
EMBEDDING_PRICE_PER_1M: dict[str, float] = {
    "text-embedding-3-small": 0.02,
    "text-embedding-3-large": 0.13,
    "text-embedding-ada-002": 0.10,
}

CHAT_PRICE_PER_1M: dict[str, tuple[float, float, float]] = {
    # model: (input_per_1m, cached_input_per_1m, output_per_1m)
    "gpt-4.1-mini": (0.40, 0.10, 1.60),
    "gpt-4o-mini": (0.15, 0.075, 0.60),
    "gpt-4.1": (2.00, 0.50, 8.00),
}

ALLOWED_FILTERS: dict[str, type] = {
    "year": int,
    "document_type": str,
    "section": str,
    "document_id": str,
}


@dataclass(frozen=True)
class Settings:
    database_url: str
    openai_api_key: str
    embedding_model: str
    embedding_dimensions: int
    agent_model: str
    rerank_model: str


def load_settings(env_file: Path | None = None, *, require_db: bool = True, require_openai: bool = True) -> Settings:
    """Load environment variables from Day 7 .env or Day 6 fallback without printing secrets."""
    candidates: list[Path] = []
    if env_file is not None:
        candidates.append(env_file)
    else:
        candidates.append(PROJECT_ROOT / ".env")
        candidates.append(DEFAULT_DAY6_ROOT / "starter" / ".env")

    for path in candidates:
        if path.exists():
            load_dotenv(path, override=False)

    database_url = os.getenv("DATABASE_URL", "").strip()
    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small").strip() or "text-embedding-3-small"
    embedding_dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536").strip() or "1536")
    agent_model = os.getenv("AGENT_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"
    rerank_model = os.getenv("RERANK_MODEL", agent_model).strip() or agent_model

    if require_db and not database_url:
        raise RuntimeError("DATABASE_URL is missing; configure .env before connecting to PostgreSQL.")
    if require_openai and not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is missing; configure .env before calling OpenAI.")

    return Settings(
        database_url=database_url,
        openai_api_key=openai_api_key,
        embedding_model=embedding_model,
        embedding_dimensions=embedding_dimensions,
        agent_model=agent_model,
        rerank_model=rerank_model,
    )


def create_openai_client(api_key: str, *, max_retries: int = 6, timeout: float = 45.0) -> OpenAI:
    """Create a configured OpenAI client with bounded retries for transient DNS/socket blips."""
    if not api_key.strip():
        raise RuntimeError("OPENAI_API_KEY is missing or empty.")
    return OpenAI(api_key=api_key, max_retries=max_retries, timeout=timeout)


def estimate_embedding_cost_usd(model: str, prompt_tokens: int) -> float:
    """Compute estimated USD cost for OpenAI embedding input tokens."""
    rate = EMBEDDING_PRICE_PER_1M.get(model, 0.0)
    return (max(0, prompt_tokens) / 1_000_000.0) * rate


def estimate_chat_cost_usd(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    cached_tokens: int = 0,
) -> float:
    """Compute estimated USD cost for OpenAI chat completions."""
    in_rate, cached_rate, out_rate = CHAT_PRICE_PER_1M.get(model, (0.0, 0.0, 0.0))
    uncached = max(0, prompt_tokens - cached_tokens)
    return (
        (uncached / 1_000_000.0) * in_rate
        + (max(0, cached_tokens) / 1_000_000.0) * cached_rate
        + (max(0, completion_tokens) / 1_000_000.0) * out_rate
    )
