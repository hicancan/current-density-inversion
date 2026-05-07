"""Valid disambiguation utility with regularization comparison (round 4)."""

from __future__ import annotations

import numpy as np


def compute_valid_utility(candidate_result: dict) -> dict:
    """Compute valid-disambiguation utility across epsilon sweep. Uses best regularized VDR if available."""
    cost = candidate_result.get("cost", 1.0)
    eps_sweep = candidate_result.get("epsilon_sweep", [])

    if not eps_sweep:
        return {"utility": -cost, "method": "valid_disambiguation",
                "per_epsilon_utilities": {}, "best_epsilon": None}

    per_epsilon = {}
    for eps_r in eps_sweep:
        eps_mult = eps_r.get("epsilon_multiplier", 0.0)
        vdr = eps_r.get("valid_disambiguation_rate", 0.0)
        ticr = eps_r.get("truth_in_consistent_set_rate", 0.0)
        swr = eps_r.get("singleton_wrong_rate", 0.0)
        er = eps_r.get("empty_rate", 0.0)
        util = float(vdr + 0.5 * ticr - 2.0 * swr - 1.0 * er - cost)
        per_epsilon[str(eps_mult)] = util

    best_mult = max(per_epsilon, key=lambda k: per_epsilon[k])
    best_util = per_epsilon[best_mult]

    # Regularized metrics
    reg_vdr = candidate_result.get("best_regularized_vdr", 0.0)
    reg_beats = candidate_result.get("regularization_beats_ols", False)
    reg_mode = candidate_result.get("best_regularized_fit_mode", "none")
    reg_lambda = candidate_result.get("best_regularized_lambda", 0.0)

    return {
        "utility": float(best_util),
        "method": "valid_disambiguation",
        "per_epsilon_utilities": per_epsilon,
        "best_epsilon_multiplier": float(best_mult),
        "best_epsilon_utility": best_util,
        "regularized_vdr": reg_vdr,
        "regularization_beats_ols": reg_beats,
        "regularized_fit_mode": reg_mode,
        "regularized_lambda": reg_lambda,
    }


def rank_candidates(
    baseline_oqci: dict,
    baseline_nullspace: dict,
    baseline_pairwise: dict,
    candidate_results: list[dict],
    weights: dict,
) -> dict:
    scored = []
    for cr in candidate_results:
        util = compute_valid_utility(cr)
        scored.append({
            "candidate_id": cr["candidate_id"],
            "height_um": cr["height_um"], "components": cr["components"],
            "n_states": cr.get("n_states", 1),
            "utility": util["utility"], "utility_detail": util,
            "regularized_vdr": util["regularized_vdr"],
            "regularization_beats_ols": util["regularization_beats_ols"],
        })

    scored.sort(key=lambda x: x["utility"], reverse=True)

    # Best per epsilon
    best_by_eps = {}
    for entry in scored:
        per_eps = entry.get("utility_detail", {}).get("per_epsilon_utilities", {})
        for eps_str, u_val in per_eps.items():
            if eps_str not in best_by_eps or u_val > best_by_eps[eps_str]["utility"]:
                best_by_eps[eps_str] = {"candidate_id": entry["candidate_id"], "utility": u_val}

    # Best regularized
    best_reg = None
    best_reg_vdr = -1.0
    for cr in candidate_results:
        rv = cr.get("best_regularized_vdr", 0.0)
        if rv > best_reg_vdr:
            best_reg_vdr = rv
            best_reg = {
                "candidate_id": cr["candidate_id"],
                "vdr": rv,
                "fit_mode": cr.get("best_regularized_fit_mode", "none"),
                "lambda": cr.get("best_regularized_lambda", 0.0),
                "beats_ols": cr.get("regularization_beats_ols", False),
            }

    return {
        "ranking": scored,
        "best_global": scored[0]["candidate_id"] if scored else "none",
        "best_utility": scored[0]["utility"] if scored else 0.0,
        "best_per_epsilon": best_by_eps,
        "best_regularized": best_reg,
        "candidate_count": len(scored),
        "any_improved": any(s["utility"] > 0 for s in scored),
        "any_regularization_beats_ols": any(
            cr.get("regularization_beats_ols", False) for cr in candidate_results
        ),
    }
