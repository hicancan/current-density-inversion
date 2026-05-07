"""Configuration loading and validation for E27."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "random_seed",
    "grid_size",
    "layer_count",
    "pixel_pitch_um",
    "layer_spacing_um",
    "sensor_height_um",
    "noise_sigma",
    "case_count_per_family",
    "families",
    "candidate_defect_families",
    "schur",
    "baselines",
    "decision",
    "operator_perturbation",
}


def load_config(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {p}")
    cfg = json.loads(p.read_text(encoding="utf-8"))
    validate_config(cfg)
    return cfg


def validate_config(cfg: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL_KEYS - set(cfg.keys()))
    if missing:
        raise ValueError(f"Config missing required keys: {missing}")

    if cfg["schema_version"] != "e27-edge-defect-schur-v1":
        raise ValueError(f"Unsupported schema_version: {cfg['schema_version']}")

    n = int(cfg["grid_size"])
    if n < 4:
        raise ValueError("grid_size must be >= 4")

    if int(cfg["layer_count"]) < 2:
        raise ValueError("layer_count must be >= 2")

    if float(cfg["noise_sigma"]) <= 0:
        raise ValueError("noise_sigma must be positive")

    if int(cfg["case_count_per_family"]) < 1:
        raise ValueError("case_count_per_family must be >= 1")

    schur = cfg["schur"]
    for k in ["conductance_range", "alpha_nominal", "alpha_removal_scale"]:
        if k not in schur:
            raise ValueError(f"schur missing {k}")

    dec = cfg["decision"]
    for k in ["accept_threshold_gamma", "reject_threshold_gamma", "tau_threshold"]:
        if k not in dec:
            raise ValueError(f"decision missing {k}")
