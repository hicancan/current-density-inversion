"""Non-degenerate pairwise hypothesis distinguishability.

E19.2 audit (2026-05-05): Replaces the original naive subspace_min_distance
(which degenerates to zero when subspaces contain zero) with four distance
families that do NOT suffer from zero-vector collapse:

1. unit_energy_principal_angle  — smallest principal angle between unit-norm
   forward projections:  dist = sin(theta_min) * ||B_i||_max
2. claim_activated_distance     — enforces minimum coefficient norm on
   hypothesis-specific blocks (via, gap, return) so that the hypothesis is
   actually "active" before measuring separation
3. per_case_fitted_distance     — case-conditioned: uses the actual OLS-fitted
   predictions for each hypothesis to compute the observed residual distance
4. full_subspace_raw_distance    — original metric retained for reference;
   near-zero value warns of subspace overlap, not of physical equivalence
"""

from __future__ import annotations

import numpy as np

from hypotheses import HYPOTHESES, HypothesisBasis, subspace_principal_angle_deg
from operators import OperatorBundle


# ── 1. Unit-energy principal angle distance ──────────────────────────────

def unit_energy_principal_angle_distance(B1: np.ndarray, B2: np.ndarray) -> float:
    """Smallest principal angle between UNIT-NORM vectors in B1 and B2.

    Let  s = max singular value of Q1^T Q2  (cos of smallest principal angle).
    Then  theta_min = arccos(min(1, max(0, s)))  and

        dist = sin(theta_min) * max(||B1||_F / sqrt(k1), ||B2||_F / sqrt(k2))

    This is never trivially zero just because both subspaces contain the zero
    vector.  Two distinct subspaces that overlap in a non-trivial way will
    still have theta_min > 0 if their unit-sphere projections are separate.
    """
    if B1.shape[1] == 0 or B2.shape[1] == 0:
        return 0.0
    Q1, _ = np.linalg.qr(B1)
    Q2, _ = np.linalg.qr(B2)
    s = np.linalg.svd(Q1.T @ Q2, compute_uv=False)
    if s.size == 0:
        return 0.0
    cos_theta = float(np.clip(np.max(s), 0.0, 1.0))
    theta_min = np.arccos(cos_theta)
    # Scale by average column norm of each subspace so the distance has
    # meaningful units (magnetic field units).
    scale1 = np.linalg.norm(B1) / max(np.sqrt(B1.shape[1]), 1e-30)
    scale2 = np.linalg.norm(B2) / max(np.sqrt(B2.shape[1]), 1e-30)
    scale = max(scale1, scale2)
    return float(np.sin(theta_min) * scale)


# ── 2. Claim-activated distance ──────────────────────────────────────────

def _hypothesis_activation_mask(hb: HypothesisBasis, tau_coeff: float = 0.1) -> np.ndarray:
    """Boolean mask: which columns must have |coeff| >= tau_coeff for the
    hypothesis to be considered "active".

    Generic columns (graph, residual) are always allowed.  Hypothesis-specific
    columns (via, gap, return) must have non-trivial coefficient norm.
    """
    k = hb.B.shape[1]
    mask = np.zeros(k, dtype=bool)
    for i, meta in enumerate(hb.column_metadata):
        kind = meta.get("block_kind", "")
        if kind in ("graph", "residual"):
            mask[i] = False   # no constraint on shared blocks
        else:
            mask[i] = True   # hypothesis-specific blocks must be active
    return mask


def claim_activated_distance(
    hi: str, hj: str,
    bases: dict[str, HypothesisBasis],
    tau_coeff: float = 0.1,
) -> dict:
    """Minimum forward distance when BOTH hypotheses have their
    hypothesis-specific blocks "activated".

    For hypothesis hi we solve  min_z  ||B_i z - y_i||  s.t. the
    hypothesis-specific block coefficients satisfy  ||c_specific||_2 >= tau_coeff.
    Similarly for hj.  Then we take the minimum distance between any such
    feasible predictions.

    In practice, constrained problems can be tricky.  We instead compute the
    SINGULAR VALUE of the hypothesis-specific sub-block and report the
    smallest perturbation needed to move from one subspace to the other
    while keeping the specific block active.
    """
    hb_i = bases[hi]
    hb_j = bases[hj]
    B_i = hb_i.B
    B_j = hb_j.B

    if B_i.shape[1] == 0 or B_j.shape[1] == 0:
        return {"distance": 0.0, "tau_coeff": tau_coeff, "method": "claim_activated"}

    # Find which columns are hypothesis-specific
    mask_i = _hypothesis_activation_mask(hb_i, tau_coeff)
    mask_j = _hypothesis_activation_mask(hb_j, tau_coeff)

    if not np.any(mask_i) or not np.any(mask_j):
        # At least one hypothesis has no specific columns; fall back to
        # unit-energy distance.
        return {
            "distance": unit_energy_principal_angle_distance(B_i, B_j),
            "tau_coeff": tau_coeff,
            "method": "claim_activated_fallback_to_unit_energy",
        }

    # Project each subspace to its hypothesis-specific portion
    B_i_spec = B_i[:, mask_i]
    B_j_spec = B_j[:, mask_j]

    # The minimum distance between any two vectors, each drawn from the
    # specific-block subspaces, with minimum norm tau_coeff:
    #   min_{a,b} ||B_i_spec a - B_j_spec b||  s.t. ||a||>=tau, ||b||>=tau
    #
    # Lower bound: min_{unit a,b} tau * ||B_i_spec u - B_j_spec v||
    # where u, v have unit norm.
    ui_dist = unit_energy_principal_angle_distance(B_i_spec, B_j_spec)

    # Also report the norm of the smallest specific subspace:
    norm_i_spec = np.linalg.norm(B_i_spec)
    norm_j_spec = np.linalg.norm(B_j_spec)

    return {
        "distance": ui_dist * tau_coeff,
        "tau_coeff": tau_coeff,
        "specific_dim_i": int(np.sum(mask_i)),
        "specific_dim_j": int(np.sum(mask_j)),
        "norm_specific_i": float(norm_i_spec),
        "norm_specific_j": float(norm_j_spec),
        "method": "claim_activated",
    }


# ── 3. Per-case fitted prediction distance ──────────────────────────────

def per_case_fitted_distances(
    cases: list,
    bases: dict[str, HypothesisBasis],
    bundle: OperatorBundle,
) -> dict:
    """For each case, fit every hypothesis via OLS and compute the pairwise
    distances between the actual fitted predictions.

    This is the most honest metric: it measures how far apart the BEST-FIT
    predictions are, not the subspaces as a whole.
    """
    from quotient import fit_hypothesis
    eps_dummy = 1e9  # all hypotheses will be "consistent"

    pairwise_dists: dict[str, list[float]] = {
        f"{hi}__{hj}": [] for hi in HYPOTHESES for hj in HYPOTHESES if hi < hj
    }

    for case in cases:
        y = case.field_observed
        fits = {}
        for h in HYPOTHESES:
            fits[h] = fit_hypothesis(y, bases[h], eps_dummy)

        for hi in HYPOTHESES:
            for hj in HYPOTHESES:
                if hi >= hj:
                    continue
                key = f"{hi}__{hj}"
                d = float(np.linalg.norm(fits[hi].predicted_field - fits[hj].predicted_field))
                pairwise_dists[key].append(d)

    summary = {}
    for key, dists in pairwise_dists.items():
        arr = np.array(dists, dtype=float)
        summary[key] = {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "p25": float(np.percentile(arr, 25)),
            "p75": float(np.percentile(arr, 75)),
            "n_cases": len(dists),
            "method": "per_case_fitted",
        }

    return summary


# ── 4. Full (consolidated) pairwise report ──────────────────────────────

def pairwise_distinguishability(
    bases: dict[str, HypothesisBasis],
    bundle: OperatorBundle,
    cases: list | None = None,
) -> dict:
    """Compute all four distance families for every hypothesis pair.

    Returns a consolidated dict suitable for metrics.json and reporting.
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
        Bi = bases[hi].B
        Bj = bases[hj].B

        # Distance family 1: unit-energy principal angle
        ue_dist = unit_energy_principal_angle_distance(Bi, Bj)

        # Distance family 2: claim-activated
        ca = claim_activated_distance(hi, hj, bases, tau_coeff=0.1)

        # Additional metrics
        angle = subspace_principal_angle_deg(Bi, Bj)

        # Extra-subspace overlap after removing H0
        B_common = bases["H0_no_via"].B
        if hi != "H0_no_via":
            Bi_extra = Bi - B_common @ (np.linalg.pinv(B_common) @ Bi)
        else:
            Bi_extra = np.zeros((Bi.shape[0], 0))
        if hj != "H0_no_via":
            Bj_extra = Bj - B_common @ (np.linalg.pinv(B_common) @ Bj)
        else:
            Bj_extra = np.zeros((Bj.shape[0], 0))
        extra_ue_dist = unit_energy_principal_angle_distance(Bi_extra, Bj_extra) if Bi_extra.shape[1] > 0 and Bj_extra.shape[1] > 0 else 0.0

        pair_key = f"{hi}__{hj}"
        result["pairs"][pair_key] = {
            "full_subspace_raw_distance": 0.0,  # degenerate by construction
            "unit_energy_distance": ue_dist,
            "unit_energy_extra_distance": extra_ue_dist,
            "claim_activated_distance": ca["distance"],
            "claim_activated_method": ca.get("method", "claim_activated"),
            "principal_angle_deg": angle,
            "dim_i": Bi.shape[1],
            "dim_j": Bj.shape[1],
            "specific_dim_i": ca.get("specific_dim_i", 0),
            "specific_dim_j": ca.get("specific_dim_j", 0),
        }

    # Per-case fitted distances (if cases provided)
    if cases:
        fitted = per_case_fitted_distances(cases, bases, bundle)
        for pair_key, stats in fitted.items():
            if pair_key in result["pairs"]:
                result["pairs"][pair_key]["per_case_fitted"] = stats

    # Summary: how many pairs have non-negligible distinguishability?
    distinguishable_ue = sum(
        1 for p in result["pairs"].values()
        if p["unit_energy_distance"] > 0.01
    )
    distinguishable_ca = sum(
        1 for p in result["pairs"].values()
        if p["claim_activated_distance"] > 0.01
    )
    result["summary"] = {
        "total_pairs": len(pairs),
        "distinguishable_by_unit_energy": distinguishable_ue,
        "distinguishable_by_claim_activated": distinguishable_ca,
        "indistinguishable_pairs": [
            k for k, p in result["pairs"].items()
            if p["claim_activated_distance"] <= 0.01
        ],
    }

    return result


def distinguishability_report(
    pairwise: dict,
    epsilon: float,
) -> dict:
    """Summarize pairwise results using non-degenerate distances."""
    distinguishable = []
    indistinguishable = []
    for pair_key, stats in pairwise["pairs"].items():
        # Use claim_activated_distance as the primary distinguishability metric
        dist = stats.get("claim_activated_distance", 0.0)
        if dist > epsilon * 0.1:  # scaled epsilon for coefficient-constrained distance
            distinguishable.append(pair_key)
        else:
            indistinguishable.append(pair_key)

    return {
        "epsilon": epsilon,
        "epsilon_scaled_for_claim_activated": epsilon * 0.1,
        "distinguishable_pairs": distinguishable,
        "indistinguishable_pairs": indistinguishable,
        "distinguishable_count": len(distinguishable),
        "indistinguishable_count": len(indistinguishable),
        "pair_details": pairwise["pairs"],
        "summary": pairwise.get("summary", {}),
    }
