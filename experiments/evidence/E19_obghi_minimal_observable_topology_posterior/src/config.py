"""Configuration loading and validation for E19 OBGHI."""

from __future__ import annotations

import json
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
    "noise_sigma",
    "case_count_per_family",
    "families",
    "observable_energy_ratio_threshold",
    "prior_variance",
    "hypothesis_log_priors",
    "decision",
    "baseline",
}


def load_config(path: str | Path) -> dict[str, Any]:
    """Load and validate an E19 JSON config."""
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

    if cfg["schema_version"] != "e19-obghi-config-v1":
        raise ValueError(f"Unsupported schema_version: {cfg['schema_version']}")

    n = int(cfg["grid_size"])
    if n < 6:
        raise ValueError("grid_size must be >= 6")

    if int(cfg["layer_count"]) != 4:
        raise ValueError("The minimal E19 evidence package currently requires 4 layers.")

    if float(cfg["noise_sigma"]) <= 0:
        raise ValueError("noise_sigma must be positive")

    if int(cfg["case_count_per_family"]) < 1:
        raise ValueError("case_count_per_family must be >= 1")

    prior = cfg["prior_variance"]
    for k in ["graph", "via", "gap", "return", "residual"]:
        if k not in prior:
            raise ValueError(f"prior_variance missing {k}")
        if float(prior[k]) <= 0:
            raise ValueError(f"prior_variance.{k} must be positive")

    for h in ["H0_no_via", "H1_via", "H2_model_gap", "H3_return_path"]:
        if h not in cfg["hypothesis_log_priors"]:
            raise ValueError(f"hypothesis_log_priors missing {h}")

    dec = cfg["decision"]
    if not (0.0 < float(dec["accept_posterior_threshold"]) < 1.0):
        raise ValueError("accept_posterior_threshold must be in (0, 1)")
    if not (0.0 < float(dec["reject_posterior_threshold"]) < 1.0):
        raise ValueError("reject_posterior_threshold must be in (0, 1)")
