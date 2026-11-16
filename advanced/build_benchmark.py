"""Validate and optionally regenerate the dev (18) and test (30) benchmark JSON."""
from __future__ import annotations

import json

from advanced.evaluate import BENCHMARK_PATH, validate_benchmark


def main() -> None:
    if not BENCHMARK_PATH.exists():
        raise FileNotFoundError(f"Missing {BENCHMARK_PATH}")
    print(json.dumps(validate_benchmark(BENCHMARK_PATH), indent=2))


if __name__ == "__main__":
    main()
