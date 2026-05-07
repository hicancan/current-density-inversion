"""Configuration loading for E23."""
from __future__ import annotations

import json
from pathlib import Path


def load_config(path: str | Path) -> dict:
    """Load JSON config file. Returns empty dict if missing."""
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))
