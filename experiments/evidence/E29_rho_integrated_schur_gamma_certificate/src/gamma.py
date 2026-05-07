"""Gamma computation with all ablation variants.

Computes:

    Gamma = S - epsilon - tau - rho

for five ablation variants:

1. no_rho:          Gamma = S - epsilon - tau
2. rss_rho:         Gamma = S - epsilon - tau - rho_rss
3. conservative_rho: Gamma = S - epsilon - tau - rho_cons
4. e23_old_rho:     Gamma = S - epsilon - tau - rho_e23_old
5. e25_calibrated:  Gamma = S - epsilon - tau - rho_e25 (same as conservative)

Conservative gamma governs claims.
"""
from __future__ import annotations

import numpy as np


def compute_gamma_ablations(
    schur_signal_max: float,
    rho_components: dict,
    epsilon: float,
    tau: float,
) -> dict:
    """Compute Gamma for all ablation variants.

    Args:
        schur_signal_max: S_q = max_k ||W * Delta Y_q||_2
        rho_components: dict from rho_local.compute_full_rho_decomposition
        epsilon: noise threshold
        tau: acceptance threshold

    Returns dict with gamma values and metadata for each ablation.
    """
    S = schur_signal_max

    rho_cons = rho_components["rho_combined_conservative"]["absolute_radius"]
    rho_rss = rho_components["rho_combined_rss"]["absolute_radius"]
    rho_e23 = rho_components["rho_combined_e23_old"]["absolute_radius"]

    gamma_no_rho = S - epsilon - tau
    gamma_rss = S - epsilon - tau - rho_rss
    gamma_cons = S - epsilon - tau - rho_cons
    gamma_e23_old = S - epsilon - tau - rho_e23
    gamma_e25_cal = S - epsilon - tau - rho_cons  # E25 conservative = cons

    return {
        "schur_signal": S,
        "epsilon": epsilon,
        "tau": tau,
        "rho_conservative": rho_cons,
        "rho_rss": rho_rss,
        "rho_e23_old": rho_e23,
        "rho_e25_calibrated": rho_cons,
        "gamma_no_rho": gamma_no_rho,
        "gamma_rss_rho": gamma_rss,
        "gamma_conservative_rho": gamma_cons,
        "gamma_e23_old_rho": gamma_e23_old,
        "gamma_e25_calibrated_rho": gamma_e25_cal,
        "conservative_pass": gamma_cons > 0,
        "rss_pass": gamma_rss > 0,
        "no_rho_pass": gamma_no_rho > 0,
        "e23_old_pass": gamma_e23_old > 0,
        "e25_calibrated_pass": gamma_e25_cal > 0,
    }


def compute_all_defect_gammas(
    schur_results: list[dict],
    rho_components: dict,
    epsilon: float,
    tau: float,
) -> list[dict]:
    """Compute Gamma ablations for all defect Schur signals."""
    results = []
    for sr in schur_results:
        gamma_info = compute_gamma_ablations(
            sr["signal_max"], rho_components, epsilon, tau,
        )
        results.append({
            "defect_id": sr["defect_id"],
            "defect_type": sr["defect_type"],
            "affected_edges": sr["affected_edges"],
            "perturbation_magnitude": sr["perturbation_magnitude"],
            **gamma_info,
        })
    return results


def compute_aggregate_rates(gamma_results: list[dict]) -> dict:
    """Compute aggregate pass rates from defect-level gamma results.

    Returns:
        dict with positive_gamma_rate, wrong_accept_rate,
        truth_missing_rate, empty_rate for each ablation variant.
    """
    n = max(len(gamma_results), 1)

    rates = {}
    for key in ["no_rho", "rss_rho", "conservative_rho", "e23_old_rho", "e25_calibrated_rho"]:
        pass_key = f"{key}_pass"
        n_pass = sum(1 for g in gamma_results if g.get(pass_key, False))
        rates[f"positive_{key}_rate"] = n_pass / n

    # wrong_accept_rate: fraction of defects with positive gamma that are NOT via/trace types
    # (i.e., defects that would be falsely accepted as real)
    structural_types = {"via_absence", "edge_break", "trace_width_error"}
    n_conservative_pass = sum(
        1 for g in gamma_results
        if g.get("conservative_pass", False)
    )
    n_wrong_pass = sum(
        1 for g in gamma_results
        if g.get("conservative_pass", False)
        and g["defect_type"] not in structural_types
    )
    rates["wrong_accept_rate_conservative"] = (
        n_wrong_pass / max(n_conservative_pass, 1)
    )

    # truth_missing_rate: fraction of structural defects that are NOT accepted
    n_structural = sum(
        1 for g in gamma_results
        if g["defect_type"] in structural_types
    )
    n_structural_missed = sum(
        1 for g in gamma_results
        if g["defect_type"] in structural_types
        and not g.get("conservative_pass", False)
    )
    rates["truth_missing_rate"] = n_structural_missed / max(n_structural, 1)

    # empty_rate: fraction of defects with zero or negative gamma across ALL ablations
    n_all_negative = sum(
        1 for g in gamma_results
        if (not g.get("no_rho_pass", False)
            and not g.get("rss_pass", False)
            and not g.get("conservative_pass", False))
    )
    rates["empty_rate"] = n_all_negative / n

    return rates


def compute_thresholds_from_calibration(
    calibration_schur_results: list[dict],
    noise_sigma: float,
    obs_dim: int,
    tau_multiplier: float = 2.5,
) -> dict:
    """Compute epsilon and tau from calibration set.

    Strictly: thresholds are set from calibration geometries only.
    """
    # epsilon = noise_sigma * sqrt(obs_dim) * multiplier
    epsilon = noise_sigma * np.sqrt(max(1, obs_dim)) * tau_multiplier

    # tau = median signal of calibration defects (3-sigma threshold)
    calibration_signals = [s["signal_max"] for s in calibration_schur_results]
    tau = float(np.median(calibration_signals)) * 0.3 if calibration_signals else epsilon

    return {
        "epsilon": epsilon,
        "tau": tau,
        "noise_sigma": noise_sigma,
        "obs_dim": obs_dim,
        "tau_multiplier": tau_multiplier,
        "calibration_defect_count": len(calibration_schur_results),
        "calibration_signal_median": float(np.median(calibration_signals)) if calibration_signals else 0.0,
    }
