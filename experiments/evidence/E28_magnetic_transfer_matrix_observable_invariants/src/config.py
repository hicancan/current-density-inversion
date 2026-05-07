"""Configuration loading and validation for E28 transfer invariants."""

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
    "sensor_heights_um",
    "noise_sigma",
    "n_port_states",
    "g_sheet",
    "g_via_nominal",
    "g_via_h0",
    "g_return_enhance",
    "g_return_suppress",
    "noise_frac_t_mat",
    "families",
    "case_count_per_family",
    "nuisance_types",
    "nuisance_magnitudes",
    "invariant_eps_threshold",
    "tau_multiplier",
    "port_config",
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

    if cfg["schema_version"] != "e28-transfer-invariants-config-v1":
        raise ValueError(f"Unsupported schema_version: {cfg['schema_version']}")

    n = int(cfg["grid_size"])
    if n < 6:
        raise ValueError("grid_size must be >= 6")

    if int(cfg["layer_count"]) < 2:
        raise ValueError("layer_count must be >= 2")

    if float(cfg["noise_sigma"]) <= 0:
        raise ValueError("noise_sigma must be positive")

    if int(cfg["case_count_per_family"]) < 1:
        raise ValueError("case_count_per_family must be >= 1")

    if int(cfg["n_port_states"]) < 2:
        raise ValueError("n_port_states must be >= 2")

    heights = cfg["sensor_heights_um"]
    if not isinstance(heights, list) or len(heights) < 1:
        raise ValueError("sensor_heights_um must be a non-empty list")

    port_cfg = cfg["port_config"]
    if port_cfg.get("scheme") not in ("diagonal_pairs", "boundary_corners", "adjacent_pairs"):
        raise ValueError(f"Unknown port scheme: {port_cfg.get('scheme')}")
