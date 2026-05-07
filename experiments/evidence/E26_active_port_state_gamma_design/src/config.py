"""Configuration loading and validation for E26 Active Port-State Gamma Design."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_KEYS = {
    "schema_version",
    "random_seed",
    "layout_count",
    "port_count_min",
    "port_count_max",
    "grid_size",
    "pixel_pitch_um",
    "sensor_height_um",
    "noise_sigma",
    "max_selected_states",
    "candidate_state_count_min",
    "hypothesis_count",
    "operator_rho",
    "gate_thresholds",
}


def load_config(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {p}")
    cfg = json.loads(p.read_text(encoding="utf-8"))
    validate_config(cfg)
    return cfg


def validate_config(cfg: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_KEYS - set(cfg.keys()))
    if missing:
        raise ValueError(f"Config missing required keys: {missing}")
    if cfg["schema_version"] != "e26-active-port-gamma-config-v1":
        raise ValueError(f"Unsupported schema_version: {cfg['schema_version']}")
    if int(cfg["layout_count"]) < 1:
        raise ValueError("layout_count must be >= 1")
    if int(cfg["grid_size"]) < 4:
        raise ValueError("grid_size must be >= 4")
    if float(cfg["noise_sigma"]) <= 0:
        raise ValueError("noise_sigma must be positive")
    if int(cfg["max_selected_states"]) < 1:
        raise ValueError("max_selected_states must be >= 1")
