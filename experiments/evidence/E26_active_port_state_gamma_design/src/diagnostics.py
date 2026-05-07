"""Critical pair diagnostics and trajectory analysis for E26."""

from __future__ import annotations

import numpy as np

from networks import HypothesisBundle
from operators import OperatorBundle
from port_states import PortState
from gamma import (
    compute_all_gammas, min_gamma, GammaResult,
    compute_current_path_overlap, compute_effective_resistance,
    CRITICAL_PAIRS,
)


def state_impact_diagnostics(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    state: PortState,
    noise_sigma: float,
    operator_rho: float,
) -> dict:
    """Compute how a single state changes all diagnostics."""
    gammas_single = compute_all_gammas(bundle, operator, [state], noise_sigma, operator_rho)

    overlaps = {}
    for h, g in CRITICAL_PAIRS:
        if h in bundle.hypotheses and g in bundle.hypotheses:
            overlaps[f"{h}__{g}"] = compute_current_path_overlap(
                bundle, state, h, g,
            )

    eff_resistances = {}
    for h_name in bundle.hypotheses:
        eff_resistances[h_name] = compute_effective_resistance(
            bundle, h_name, state,
        )

    return {
        "state_id": state.state_id,
        "kind": state.kind,
        "gamma_by_pair": {
            f"{h}__{g}": float(r.gamma) for (h, g), r in gammas_single.items()
        },
        "delta_by_pair": {
            f"{h}__{g}": float(r.delta) for (h, g), r in gammas_single.items()
        },
        "min_gamma": min_gamma(gammas_single),
        "current_path_overlap": overlaps,
        "effective_resistance": eff_resistances,
        "cost": float(state.cost),
    }


def gamma_trajectory(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    selected_states: list[PortState],
    noise_sigma: float,
    operator_rho: float,
) -> dict:
    """Track how Gamma evolves as states are added one by one."""
    trajectory = []
    for k in range(len(selected_states) + 1):
        subset = selected_states[:k]
        gammas = compute_all_gammas(bundle, operator, subset, noise_sigma, operator_rho)
        trajectory.append({
            "step": k,
            "states_included": k,
            "min_gamma": min_gamma(gammas),
            "gamma_by_pair": {
                f"{h}__{g}": float(r.gamma) for (h, g), r in gammas.items()
            },
            "delta_by_pair": {
                f"{h}__{g}": float(r.delta) for (h, g), r in gammas.items()
            },
            "separable_pairs": sum(1 for r in gammas.values() if r.is_separable),
            "total_pairs": len(gammas),
        })
    return {"trajectory": trajectory, "final_min_gamma": min_gamma(
        compute_all_gammas(bundle, operator, selected_states, noise_sigma, operator_rho),
    )}


def failure_mode_analysis(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    selected_states: list[PortState],
    noise_sigma: float,
    operator_rho: float,
    baselines: dict,
) -> dict:
    """Identify which failure mode dominates when Gamma is negative.

    Returns analysis of why positive Gamma cannot be achieved.
    """
    gammas = compute_all_gammas(bundle, operator, selected_states, noise_sigma, operator_rho)
    mg = min_gamma(gammas)

    failure_modes = []

    # Check state set weakness
    if len(selected_states) < 2:
        failure_modes.append({
            "mode": "state_set_too_weak",
            "detail": f"Only {len(selected_states)} states selected",
            "recommendation": "Increase max_selected_states or candidate pool",
        })

    # Check operator rho contribution
    worst_pair = min(gammas.items(), key=lambda x: x[1].gamma) if gammas else None
    if worst_pair:
        r = worst_pair[1]
        if r.delta < r.eps + r.tau + r.rho_h + r.rho_g:
            if r.delta < r.eps + r.tau * 0.5:
                failure_modes.append({
                    "mode": "topology_hypotheses_too_similar",
                    "detail": f"Delta={r.delta:.4f} for {worst_pair[0]} vs tau={r.tau:.4f}",
                    "recommendation": "Hypotheses may need more distinct edge topologies",
                })
            if r.rho_h > r.delta * 0.3:
                failure_modes.append({
                    "mode": "operator_rho_too_large",
                    "detail": f"rho={r.rho_h:.4f} exceeds 30% of delta={r.delta:.4f}",
                    "recommendation": "Reduce operator perturbation or calibrate rho",
                })

    # Check noise level
    if noise_sigma > 0.5:
        failure_modes.append({
            "mode": "measurement_noise_too_large",
            "detail": f"noise_sigma={noise_sigma:.4f}",
            "recommendation": "Reduce noise or increase signal amplitude",
        })

    # Check if network model flexibility is the issue
    if len(bundle.hypotheses) <= 2:
        failure_modes.append({
            "mode": "network_model_too_simple",
            "detail": f"Only {len(bundle.hypotheses)} hypotheses",
            "recommendation": "Add more hypothesis variants",
        })

    return {
        "min_gamma": mg,
        "positive_gamma_achieved": mg > 0,
        "failure_modes": failure_modes,
        "worst_pair": str(worst_pair[0]) if worst_pair else "none",
        "worst_pair_gamma": float(worst_pair[1].gamma) if worst_pair else 0.0,
    }
