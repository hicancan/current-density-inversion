"""Pairwise distances between transfer matrix invariants.

Computes raw-field and invariant distances for all hypothesis pairs.
"""

from __future__ import annotations

import numpy as np

from invariants import (
    projector_distance,
    gram_distance,
    principal_angle_spectrum,
    differential_matrix,
    pairwise_differential_matrix,
)

HYP_PAIRS = [
    ("H0_no_via", "H1_via"),
    ("H0_no_via", "H2_model_gap"),
    ("H0_no_via", "H3_return_path"),
    ("H1_via", "H2_model_gap"),
    ("H1_via", "H3_return_path"),
    ("H2_model_gap", "H3_return_path"),
]

CRITICAL_PAIRS = [
    ("H0_no_via", "H1_via"),
    ("H1_via", "H3_return_path"),
]


def raw_field_distance(T1: np.ndarray, T2: np.ndarray) -> float:
    """Raw stacked field Frobenius distance."""
    return float(np.linalg.norm(T1 - T2, "fro"))


def raw_diff_distance(T1: np.ndarray, T2: np.ndarray) -> float:
    """Distance between differential matrices (common-mode canceled)."""
    d1 = differential_matrix(T1)
    d2 = differential_matrix(T2)
    return float(np.linalg.norm(d1 - d2, "fro"))


def normalized_raw_distance(T1: np.ndarray, T2: np.ndarray) -> float:
    """Normalized raw field distance (per-column norm)."""
    n1 = np.linalg.norm(T1, axis=0)
    n2 = np.linalg.norm(T2, axis=0)
    n1_safe = np.where(n1 > 1e-14, n1, 1.0)
    n2_safe = np.where(n2 > 1e-14, n2, 1.0)
    T1n = T1 / n1_safe[None, :]
    T2n = T2 / n2_safe[None, :]
    return float(np.linalg.norm(T1n - T2n, "fro"))


def compute_all_pairwise_distances(
    T_matrices: dict[str, np.ndarray],
) -> dict:
    """Compute all distance families for every hypothesis pair.

    Returns a consolidated dict with:
    - raw_frobenius
    - raw_normalized
    - raw_differential
    - projector_distance
    - gram_distance
    - principal_angle_spectrum
    """
    result = {"pairs": {}, "summary": {}}

    for hi, hj in HYP_PAIRS:
        Ti = T_matrices[hi]
        Tj = T_matrices[hj]

        raw_frob = raw_field_distance(Ti, Tj)
        raw_norm = normalized_raw_distance(Ti, Tj)
        raw_diff = raw_diff_distance(Ti, Tj)
        proj_dist = projector_distance(Ti, Tj)
        gram_dist = gram_distance(Ti, Tj)
        angles = principal_angle_spectrum(Ti, Tj)

        pair_key = f"{hi}__{hj}"
        result["pairs"][pair_key] = {
            "raw_frobenius": raw_frob,
            "raw_normalized": raw_norm,
            "raw_differential": raw_diff,
            "projector_distance": proj_dist,
            "gram_distance": gram_dist,
            "min_principal_angle_deg": angles["min_angle_deg"],
            "n_principal_angles": angles["n_angles"],
            "dim_Ti": list(Ti.shape),
            "dim_Tj": list(Tj.shape),
        }

    # Summary statistics
    all_raw = [p["raw_frobenius"] for p in result["pairs"].values()]
    all_proj = [p["projector_distance"] for p in result["pairs"].values()]
    all_gram = [p["gram_distance"] for p in result["pairs"].values()]
    all_diff = [p["raw_differential"] for p in result["pairs"].values()]

    result["summary"] = {
        "n_pairs": len(HYP_PAIRS),
        "raw_frobenius_mean": float(np.mean(all_raw)),
        "raw_frobenius_min": float(np.min(all_raw)),
        "projector_distance_mean": float(np.mean(all_proj)),
        "projector_distance_min": float(np.min(all_proj)),
        "gram_distance_mean": float(np.mean(all_gram)),
        "gram_distance_min": float(np.min(all_gram)),
        "differential_distance_mean": float(np.mean(all_diff)),
        "differential_distance_min": float(np.min(all_diff)),
    }

    return result
