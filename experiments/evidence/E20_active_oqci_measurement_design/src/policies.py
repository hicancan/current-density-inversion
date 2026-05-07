"""Acquisition policies for E20 Round 5: pairwise-margin active measurement design.

Compares 5 policies for selecting the next measurement candidate.

Names:
  interval_width_policy
  valid_disambiguation_utility_policy
  pairwise_min_gamma_policy
  critical_pair_gamma_policy
  random_policy_fixed_seed
"""

from __future__ import annotations

import numpy as np

from pairwise_margin import compute_pairwise_margins, CRITICAL_PAIRS
from utility import compute_valid_utility


def interval_width_policy(candidate_results: list[dict]) -> dict:
    """Select candidate with smallest mean interval width (round 1-2 legacy)."""
    best = None; best_width = 2.0; best_cid = "none"
    for cr in candidate_results:
        eps_sweep = cr.get("epsilon_sweep", [])
        best_cr_width = 2.0
        for eps_r in eps_sweep:
            w = eps_r.get("mean_interval_width", 2.0)
            if w < best_cr_width:
                best_cr_width = w
        if best_cr_width < best_width:
            best_width = best_cr_width
            best_cid = cr["candidate_id"]
            best = {"policy": "interval_width", "selected": best_cid,
                    "metric_value": best_width, "candidate": cr}
    return best or {"policy": "interval_width", "selected": "none", "metric_value": 2.0}


def valid_disambiguation_utility_policy(candidate_results: list[dict]) -> dict:
    """Select candidate with highest valid disambiguation utility (round 3-4)."""
    best = None; best_util = -1e9; best_cid = "none"
    for cr in candidate_results:
        u = compute_valid_utility(cr)["utility"]
        if u > best_util:
            best_util = u; best_cid = cr["candidate_id"]
            best = {"policy": "vdr_utility", "selected": best_cid,
                    "metric_value": best_util, "candidate": cr}
    return best or {"policy": "vdr_utility", "selected": "none", "metric_value": -1e9}


def pairwise_min_gamma_policy(
    baseline_bases, baseline_bundle,
    candidate_results: list[dict], epsilon: float = 1.0,
) -> dict:
    """Select candidate maximizing min_hg gamma after adding measurement."""
    best = None; best_gamma = -1e9; best_cid = "none"
    for cr in candidate_results:
        # Get margin from pairwise_margin data in candidate result
        pm = cr.get("pairwise_margin", {})
        if not pm:
            continue
        min_g = pm.get("candidate_summary", {}).get("min_gamma", -1e9)
        if min_g > best_gamma:
            best_gamma = min_g; best_cid = cr["candidate_id"]
            best = {"policy": "pairwise_min_gamma", "selected": best_cid,
                    "metric_value": best_gamma, "candidate": cr}
    return best or {"policy": "pairwise_min_gamma", "selected": "none", "metric_value": -1e9}


def critical_pair_gamma_policy(
    candidate_results: list[dict],
) -> dict:
    """Select candidate maximizing min_gamma for critical pairs (H1/H2, H1/H3, H2/H3)."""
    best = None; best_crit = -1e9; best_cid = "none"
    for cr in candidate_results:
        pm = cr.get("pairwise_margin", {})
        if not pm:
            continue
        crit_gammas = []
        for pair_key in CRITICAL_PAIRS:
            pair_data = pm.get("pairs", {}).get(pair_key, {})
            g = pair_data.get("gamma_after", -1e9)
            crit_gammas.append(g)
        min_crit = min(crit_gammas) if crit_gammas else -1e9
        if min_crit > best_crit:
            best_crit = min_crit; best_cid = cr["candidate_id"]
            best = {"policy": "critical_pair_gamma", "selected": best_cid,
                    "metric_value": best_crit, "candidate": cr}
    return best or {"policy": "critical_pair_gamma", "selected": "none", "metric_value": -1e9}


def random_policy_fixed_seed(candidate_results: list[dict], seed: int = 42) -> dict:
    """Random selection with fixed seed (baseline policy)."""
    if not candidate_results:
        return {"policy": "random", "selected": "none", "metric_value": 0.0}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(candidate_results))
    cr = candidate_results[idx]
    return {"policy": "random", "selected": cr["candidate_id"],
            "metric_value": float(idx), "candidate": cr}


def compare_acquisition_policies(
    baseline_bases, baseline_bundle,
    candidate_results: list[dict],
    epsilon: float,
) -> dict:
    """Run all 5 acquisition policies and return comparison."""
    policies = {}

    # 1. Interval width (legacy)
    policies["interval_width"] = interval_width_policy(candidate_results)

    # 2. VDR utility (round 3-4)
    policies["vdr_utility"] = valid_disambiguation_utility_policy(candidate_results)

    # 3. Pairwise min gamma
    policies["pairwise_min_gamma"] = pairwise_min_gamma_policy(
        baseline_bases, baseline_bundle, candidate_results, epsilon)

    # 4. Critical pair gamma
    policies["critical_pair_gamma"] = critical_pair_gamma_policy(candidate_results)

    # 5. Random (fixed seed baseline)
    policies["random"] = random_policy_fixed_seed(candidate_results)

    # Determine if pairwise policy differs from old (interval_width / vdr_utility)
    pmg_selected = policies["pairwise_min_gamma"]["selected"]
    vdr_selected = policies["vdr_utility"]["selected"]
    iw_selected = policies["interval_width"]["selected"]
    diff_from_vdr = (pmg_selected != vdr_selected)
    diff_from_iw = (pmg_selected != iw_selected)

    return {
        "policies": policies,
        "pairwise_differs_from_vdr": diff_from_vdr,
        "pairwise_differs_from_interval_width": diff_from_iw,
        "epsilon_used": epsilon,
    }


def greedy_two_step_design(
    baseline_bases, baseline_bundle,
    candidate_results: list[dict],
    epsilon: float,
    beta_cost: float = 0.1,
) -> dict:
    """Greedy two-step sequential measurement design.

    Step 1: Pick best candidate by pairwise_min_gamma policy.
    Step 2: Given step 1, pick best second candidate maximizing combined margin.

    Returns two-step sequence with metrics.
    """
    if len(candidate_results) < 2:
        return {"best_1step_candidate": "none", "best_2step_sequence": [],
                "error": "need at least 2 candidates"}

    # Step 1: best candidate by min_gamma
    candidates_by_gamma = []
    for cr in candidate_results:
        pm = cr.get("pairwise_margin", {})
        min_g = pm.get("candidate_summary", {}).get("min_gamma", -1e9)
        candidates_by_gamma.append((cr["candidate_id"], min_g, cr))
    candidates_by_gamma.sort(key=lambda x: x[1], reverse=True)

    step1 = candidates_by_gamma[0]
    step1_id = step1[0]
    step1_min_gamma = step1[1]
    step1_cr = step1[2]

    # Step 2: greedy — pick best remaining that maximizes combined metric
    # Since we don't have true joint (c1,c2) evaluation, approximate:
    # combine margins additively with cost penalty
    best_combined = -1e9
    step2_id = "none"
    step2_min_gamma = -1e9
    for cr in candidate_results:
        if cr["candidate_id"] == step1_id:
            continue
        pm = cr.get("pairwise_margin", {})
        min_g2 = pm.get("candidate_summary", {}).get("min_gamma", -1e9)
        # Additive approximation: combined_gamma ≈ gamma1 + gamma2 (pessimistic)
        combined = min(step1_min_gamma, min_g2) - beta_cost * (
            step1_cr.get("cost", 1.0) + cr.get("cost", 1.0))
        if combined > best_combined:
            best_combined = combined
            step2_id = cr["candidate_id"]
            step2_min_gamma = min_g2
            step2_cr = cr

    # Get baseline margin
    baseline_margin = candidate_results[0].get("pairwise_margin", {}).get(
        "baseline_summary", {}).get("min_gamma", -1e9) if candidate_results else -1e9

    return {
        "best_1step_candidate": step1_id,
        "best_2step_sequence": [step1_id, step2_id],
        "min_gamma_after_1step": step1_min_gamma,
        "min_gamma_after_2step": max(step1_min_gamma, step2_min_gamma),
        "baseline_min_gamma": baseline_margin,
        "critical_gamma_after_1step": _critical_min_gamma(step1_cr),
        "critical_gamma_after_2step": max(
            _critical_min_gamma(step1_cr),
            _critical_min_gamma(step2_cr) if step2_cr is not None else -1e9,
        ),
        "step1_cost": step1_cr.get("cost", 1.0),
        "step2_cost": step2_cr.get("cost", 1.0) if step2_cr else 0.0,
    }


def _critical_min_gamma(candidate_result: dict) -> float:
    """Extract minimum gamma across critical pairs."""
    pm = candidate_result.get("pairwise_margin", {})
    if not pm:
        return -1e9
    crit_gammas = []
    for pk in CRITICAL_PAIRS:
        g = pm.get("pairs", {}).get(pk, {}).get("gamma_after", -1e9)
        crit_gammas.append(g)
    return min(crit_gammas) if crit_gammas else -1e9
