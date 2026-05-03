from __future__ import annotations

from dataclasses import replace
from typing import Dict, List, Sequence

import numpy as np

from .forward import field_from_segments, make_observation_grid
from .types import CaseRecord, Segment


def _all_segments(record: CaseRecord) -> list[Segment]:
    return (
        list(record.sheet_segments)
        + list(record.via_candidates)
        + list(record.return_candidates)
        + list(record.artifact_candidates)
    )


def make_second_excitation_state(
    record: CaseRecord,
    cfg: dict,
    rng: np.random.Generator,
    policy: str = "random_independent",
) -> CaseRecord:
    """Create a second synthetic excitation for the same graph and hypothesis."""

    obs_grid = make_observation_grid(
        n=int(cfg["grid"]["n"]),
        fov_m=float(cfg["grid"]["fov_m"]),
        obs_z_m=float(cfg["grid"].get("obs_z_m", 0.0)),
    )
    currents: Dict[str, float] = {}
    for seg in _all_segments(record):
        current = float(record.truth_currents.get(seg.name, 0.0))
        if current == 0.0:
            continue
        if policy == "random_independent":
            if seg.prior_group == "sheet":
                factor = rng.uniform(0.55, 1.35)
            else:
                # Different excitation states need not scale all branches equally.
                factor = rng.uniform(0.75, 1.75) * rng.choice([-1.0, 1.0])
        elif policy == "sheet_rescale":
            factor = rng.uniform(0.35, 1.60) if seg.prior_group == "sheet" else rng.uniform(0.85, 1.15)
        elif policy == "extra_boost":
            factor = rng.uniform(0.60, 0.95) if seg.prior_group == "sheet" else rng.uniform(1.60, 2.25)
        elif policy == "extra_sign_flip":
            factor = rng.uniform(0.85, 1.15) if seg.prior_group == "sheet" else -rng.uniform(0.85, 1.45)
        elif policy == "low_noise_repeat":
            factor = 1.0
        elif policy == "h0_disambiguation":
            factor = rng.uniform(0.35, 0.65) if seg.prior_group == "sheet" else rng.uniform(1.75, 2.35)
        elif policy == "h1_h2_separation":
            if seg.prior_group == "via":
                factor = rng.uniform(1.90, 2.50)
            elif seg.prior_group == "return":
                factor = -rng.uniform(1.20, 1.80)
            elif seg.prior_group == "artifact":
                factor = rng.uniform(0.55, 0.95)
            else:
                factor = rng.uniform(0.75, 1.05)
        elif policy == "max_expected_margin":
            factor = rng.uniform(0.45, 0.75) if seg.prior_group == "sheet" else rng.uniform(2.00, 2.80) * rng.choice([-1.0, 1.0])
        elif policy == "min_expected_entropy":
            group_factor = {
                "sheet": 0.70,
                "via": 2.10,
                "return": -1.55,
                "artifact": -1.25,
            }
            factor = group_factor.get(seg.prior_group, 1.0)
        else:
            raise ValueError(f"unknown multistate policy: {policy}")
        currents[seg.name] = current * float(factor)
    if not currents:
        currents = dict(record.truth_currents)
    b_clean = field_from_segments(
        _all_segments(record),
        currents,
        obs_grid,
        edge_steps=int(cfg["geometry"]["edge_discretization"]),
        via_steps=int(cfg["geometry"]["via_discretization"]),
    )
    default_noise = 0.004 if policy == "low_noise_repeat" else 0.010
    rel_noise = float(cfg.get("multistate", {}).get("second_state_noise_std_relative_to_max_abs_b", default_noise))
    sigma = rel_noise * max(float(np.max(np.abs(b_clean))), 1e-30)
    b_obs = b_clean + rng.normal(0.0, sigma, size=b_clean.shape)
    metadata = dict(record.metadata)
    metadata.update(
        {
            "multi_state_role": "state_2",
            "second_state_noise_sigma_t": sigma,
            "claim_boundary": "Synthetic second excitation only; not active measurement data.",
        }
    )
    return replace(
        record,
        case_id=f"{record.case_id}__state2",
        b_clean=b_clean,
        b_obs=b_obs,
        truth_currents=currents,
        metadata=metadata,
    )


def joint_hypothesis_scores(per_state_results: Sequence[dict]) -> dict[str, float]:
    """Average hypothesis scores across states."""

    labels = list(per_state_results[0].keys())
    return {
        label: float(np.mean([state[label].score for state in per_state_results]))
        for label in labels
    }


def best_joint_hypothesis(per_state_results: Sequence[dict]) -> str:
    scores = joint_hypothesis_scores(per_state_results)
    return min(scores, key=scores.get)
