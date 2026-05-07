"""Configuration loading and validation for E20 Active OQCI."""

from __future__ import annotations

import json
import numpy as np
from pathlib import Path
from typing import Any, Mapping


REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "random_seed",
    "grid_size",
    "layer_count",
    "pixel_pitch_um",
    "layer_spacing_um",
    "sensor_height_um",
    "sensor_heights_um",
    "noise_sigma",
    "case_count_per_family",
    "families",
    "observable_energy_ratio_threshold",
    "epsilon_policy",
    "epsilon_multipliers",
    "prior_variance",
    "nullspace_threshold",
    "baseline",
    "adversarial_pair_count",
    "candidate_pool",
    "utility_weights",
}

COMPONENT_ROW_INDICES = {
    "Bx": 0,
    "By": 1,
    "Bz": 2,
}


def load_config(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {p}")
    cfg = json.loads(p.read_text(encoding="utf-8"))
    validate_config(cfg)
    return cfg


def validate_config(cfg: Mapping[str, Any]) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL_KEYS.difference(cfg))
    if missing:
        raise ValueError(f"Config missing required keys: {missing}")

    if cfg["schema_version"] not in ("e20-active-oqci-config-v1", "e20-active-oqci-config-v2"):
        raise ValueError(f"Unsupported schema_version: {cfg['schema_version']}")

    n = int(cfg["grid_size"])
    if n < 4:
        raise ValueError("grid_size must be >= 4")

    if int(cfg["layer_count"]) != 4:
        raise ValueError("layer_count must be 4")

    if float(cfg["noise_sigma"]) <= 0:
        raise ValueError("noise_sigma must be positive")

    if int(cfg["case_count_per_family"]) < 1:
        raise ValueError("case_count_per_family must be >= 1")

    heights = cfg["sensor_heights_um"]
    if not isinstance(heights, list) or len(heights) < 1:
        raise ValueError("sensor_heights_um must be a non-empty list")
    for h in heights:
        if float(h) <= 0:
            raise ValueError(f"sensor_heights_um values must be positive, got {h}")

    eps_mult = cfg["epsilon_multipliers"]
    if not isinstance(eps_mult, list) or len(eps_mult) < 1:
        raise ValueError("epsilon_multipliers must be a non-empty list")

    eps = cfg["epsilon_policy"]
    if eps["mode"] not in ("known_noise", "sensitivity"):
        raise ValueError(f"Unknown epsilon_policy mode: {eps['mode']}")

    pool = cfg["candidate_pool"]
    if not isinstance(pool, list) or len(pool) < 1:
        raise ValueError("candidate_pool must be a non-empty list")

    weights = cfg["utility_weights"]
    for k in ["interval_width", "near_null", "pairwise_distance", "wrong_accept", "cost"]:
        if k not in weights:
            raise ValueError(f"utility_weights missing key: {k}")


def component_mask(components: list[str], n_pixels: int) -> np.ndarray:
    """Build a boolean row mask for selecting observation rows matching components.

    Observation rows are interleaved: Bx_0, By_0, Bz_0, Bx_1, By_1, Bz_1, ...
    """
    mask = np.zeros(3 * n_pixels, dtype=bool)
    for comp in components:
        idx = COMPONENT_ROW_INDICES[comp]
        mask[idx::3] = True
    return mask
