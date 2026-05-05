"""Configuration loading and validation for E19.2 OQCI."""

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
    "prior_variance",
    "nullspace_threshold",
    "baseline",
    "adversarial_pair_count",
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

    if cfg["schema_version"] != "e19_2-oqci-config-v1":
        raise ValueError(f"Unsupported schema_version: {cfg['schema_version']}")

    n = int(cfg["grid_size"])
    if n < 6:
        raise ValueError("grid_size must be >= 6")

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

    eps = cfg["epsilon_policy"]
    if eps["mode"] not in ("known_noise", "sensitivity"):
        raise ValueError(f"Unknown epsilon_policy mode: {eps['mode']}")
    if eps["mode"] == "known_noise":
        if float(eps.get("c", 1.5)) <= 0:
            raise ValueError("epsilon_policy.c must be positive")
    if eps["mode"] == "sensitivity":
        multipliers = eps.get("multipliers", [1.0])
        if not isinstance(multipliers, list) or len(multipliers) == 0:
            raise ValueError("epsilon_policy.multipliers must be a non-empty list")

    prior = cfg["prior_variance"]
    for k in ["graph", "residual"]:
        if k not in prior or float(prior[k]) <= 0:
            raise ValueError(f"prior_variance.{k} required and must be positive")


def compute_epsilon(cfg: dict, obs_dim: int) -> dict[str, float | list[float]]:
    """Compute epsilon threshold(s) for the consistent set.

    Returns a dict with the computed epsilon value(s) and metadata.
    """
    sigma = float(cfg["noise_sigma"])
    policy = cfg["epsilon_policy"]

    if policy["mode"] == "known_noise":
        c = float(policy.get("c", 1.5))
        eps = float(c * sigma * np.sqrt(obs_dim))
        return {"mode": "known_noise", "c": c, "epsilon": eps, "sigma": sigma, "obs_dim": obs_dim}

    if policy["mode"] == "sensitivity":
        multipliers = [float(m) for m in policy["multipliers"]]
        eps_values = [float(m * sigma * np.sqrt(obs_dim)) for m in multipliers]
        return {
            "mode": "sensitivity",
            "multipliers": multipliers,
            "epsilon_values": eps_values,
            "sigma": sigma,
            "obs_dim": obs_dim,
        }

    raise ValueError(f"Unknown epsilon mode: {policy['mode']}")
