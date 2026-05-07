"""Pairwise robust margin computation for E20 Round 5.

For hypothesis pair (h,g) under measurement M:
  delta_hg(M) = min ||B_h theta_h - B_g theta_g||     (subspace separation)
  Gamma_hg(M) = delta_hg(M) - tau_g(M) - epsilon(M)   (robust margin)
"""

from __future__ import annotations

import numpy as np

from hypotheses import HYPOTHESES, HypothesisBasis
from operators import OperatorBundle


def subspace_separation(B_h: np.ndarray, B_g: np.ndarray) -> float:
    """Minimum distance between two linear subspaces.

    delta_hg = sigma_min of Q_{joint} where Q_joint spans [B_h, -B_g].
    Equivalently: smallest singular value of projection onto orthogonal complement.
    """
    if B_h.shape[1] == 0 and B_g.shape[1] == 0:
        return 0.0
    if B_h.shape[1] == 0:
        return float(np.min(np.linalg.norm(B_g, axis=0)))
    if B_g.shape[1] == 0:
        return float(np.min(np.linalg.norm(B_h, axis=0)))

    # Stack: C = [B_h, -B_g], then delta = sigma_min(C) gives min ||B_h a - B_g b||
    C = np.concatenate([B_h, -B_g], axis=1)
    if C.shape[1] == 0:
        return 0.0
    s = np.linalg.svd(C, compute_uv=False)
    return float(s[-1]) if s.size > 0 else 0.0


def subspace_principal_angle_deg(B_h: np.ndarray, B_g: np.ndarray) -> float:
    """Smallest principal angle between two subspaces (degrees)."""
    if B_h.shape[1] == 0 or B_g.shape[1] == 0:
        return 90.0
    Qh, _ = np.linalg.qr(B_h)
    Qg, _ = np.linalg.qr(B_g)
    s = np.linalg.svd(Qh.T @ Qg, compute_uv=False)
    if s.size == 0:
        return 90.0
    cos_theta = float(np.clip(np.max(s), 0.0, 1.0))
    return float(np.degrees(np.arccos(cos_theta)))


def intersection_rank(B_h: np.ndarray, B_g: np.ndarray, tol: float = 1e-6) -> int:
    """Estimate rank of subspace intersection by counting near-zero singular values."""
    C = np.concatenate([B_h, -B_g], axis=1)
    if C.shape[1] == 0:
        return 0
    s = np.linalg.svd(C, compute_uv=False)
    max_s = s[0] if s.size > 0 else 1.0
    if max_s < 1e-30:
        return int(C.shape[1])
    return int(np.sum(s / max_s < tol))


def compute_pairwise_margins(
    bases: dict[str, HypothesisBasis],
    bundle: OperatorBundle,
    epsilon: float = 1.0,
) -> dict:
    """Compute all pairwise subspace separations, principal angles, and robust margins.

    Pairs: all 6 combinations of (H0, H1, H2, H3).

    Returns dict with per-pair and summary metrics.
    """
    pairs = [
        ("H0_no_via", "H1_via"),
        ("H0_no_via", "H2_model_gap"),
        ("H0_no_via", "H3_return_path"),
        ("H1_via", "H2_model_gap"),
        ("H1_via", "H3_return_path"),
        ("H2_model_gap", "H3_return_path"),
    ]

    result = {"pairs": {}, "summary": {}}

    for hi, hj in pairs:
        Bh = bases[hi].B
        Bg = bases[hj].B

        delta = subspace_separation(Bh, Bg)
        angle = subspace_principal_angle_deg(Bh, Bg)
        isect_rank = intersection_rank(Bh, Bg)
        # Robust margin: separation minus acceptance threshold minus noise
        gamma = delta - epsilon * 2.0  # tau_g + epsilon_noise

        pair_key = f"{hi}__{hj}"
        result["pairs"][pair_key] = {
            "delta": float(delta),
            "gamma": float(gamma),
            "principal_angle_deg": float(angle),
            "intersection_rank": isect_rank,
            "dim_h": Bh.shape[1],
            "dim_g": Bg.shape[1],
            "epsilon": epsilon,
        }

    # Summary
    deltas = [v["delta"] for v in result["pairs"].values()]
    gammas = [v["gamma"] for v in result["pairs"].values()]
    result["summary"] = {
        "min_delta": float(np.min(deltas)),
        "min_gamma": float(np.min(gammas)),
        "max_delta": float(np.max(deltas)),
        "pairs_with_positive_gamma": sum(1 for g in gammas if g > 0),
        "pairs_with_positive_delta": sum(1 for d in deltas if d > 0),
        "critical_pairs": [
            k for k, v in result["pairs"].items()
            if v["gamma"] <= 0 or v["principal_angle_deg"] <= 1.0
        ],
    }

    return result


CRITICAL_PAIRS = ["H1_via__H2_model_gap", "H1_via__H3_return_path", "H2_model_gap__H3_return_path"]


def compute_pairwise_margin_gain(
    baseline_bases: dict[str, HypothesisBasis],
    candidate_bases: dict[str, HypothesisBasis],
    baseline_bundle: OperatorBundle,
    candidate_bundle: OperatorBundle,
    epsilon: float = 1.0,
) -> dict:
    """Compute before/after pairwise margins for a candidate measurement.

    Returns per-pair delta_before, delta_after, gamma_before, gamma_after, gamma_gain.
    """
    before = compute_pairwise_margins(baseline_bases, baseline_bundle, epsilon)
    after = compute_pairwise_margins(candidate_bases, candidate_bundle, epsilon)

    pairs_output = {}
    for pair_key in before["pairs"]:
        bp = before["pairs"][pair_key]
        ap = after["pairs"][pair_key]
        pairs_output[pair_key] = {
            "delta_before": bp["delta"],
            "delta_after": ap["delta"],
            "gamma_before": bp["gamma"],
            "gamma_after": ap["gamma"],
            "gamma_gain": ap["gamma"] - bp["gamma"],
            "principal_angle_before": bp["principal_angle_deg"],
            "principal_angle_after": ap["principal_angle_deg"],
            "intersection_rank_before": bp["intersection_rank"],
            "intersection_rank_after": ap["intersection_rank"],
            "dim_h": bp["dim_h"],
            "dim_g": bp["dim_g"],
        }

    return {
        "pairs": pairs_output,
        "baseline_summary": before["summary"],
        "candidate_summary": after["summary"],
        "min_gamma_gain": after["summary"]["min_gamma"] - before["summary"]["min_gamma"],
        "epsilon": epsilon,
        "candidate_id": "?",
    }
