from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def _load() -> dict[str, dict]:
    path = Path(__file__).with_name("monsters.json")
    return json.loads(path.read_text())


def lookup(ref: str) -> dict:
    if not ref.startswith("SRD."):
        raise KeyError(f"Unknown reference: {ref}")
    key = ref.split(".", 1)[1]
    data = _load()
    if key not in data:
        raise KeyError(f"Unknown SRD entry: {ref}")
    return data[key]
