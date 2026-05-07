"""Configuration loading and validation for E24 network profile inversion."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_KEYS = {
    "schema_version", "random_seed", "layout_count", "multiport_layout_count",
    "state_count", "hypothesis_count", "case_count_per_family", "noise_sigma",
    "grid_size_min", "grid_size_max", "layer_count", "sensor_heights_um",
    "pixel_pitch_um", "layer_spacing_um", "epsilon_policy", "regularization_lambda",
    "operator_stress_count", "families",
}


def load_config(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {p}")
    cfg = json.loads(p.read_text(encoding="utf-8"))
    _validate(cfg)
    return cfg


def _validate(cfg: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_KEYS.difference(cfg))
    if missing:
        raise ValueError(f"Config missing required keys: {missing}")
    if cfg["schema_version"] != "e24-network-profile-config-v1":
        raise ValueError(f"Unsupported schema_version: {cfg['schema_version']}")
    if cfg["layout_count"] < 1:
        raise ValueError("layout_count must be >= 1")
    if cfg["state_count"] not in (1, 2, 4):
        raise ValueError("state_count must be in {1,2,4}")
    if cfg["hypothesis_count"] < 4:
        raise ValueError("hypothesis_count must be >= 4")
    if cfg["noise_sigma"] <= 0:
        raise ValueError("noise_sigma must be positive")

    eps = cfg["epsilon_policy"]
    if eps["mode"] not in ("known_noise", "sensitivity"):
        raise ValueError(f"Unknown epsilon_policy mode: {eps['mode']}")
