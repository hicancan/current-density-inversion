"""Baseline state selection strategies for E26 comparison.

Implements:
- single_default_state
- all_pairwise_port_states
- random_states_fixed_seed
- max_current_norm_states
- max_effective_resistance_contrast_states
- oracle_truth_margin_states (marked nondeployable)
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from port_states import PortState, design_cost
from networks import HypothesisBundle, solve_network
from operators import OperatorBundle
from gamma import (
    compute_state_current, map_edge_currents_to_field,
    compute_all_gammas, min_gamma, GammaResult,
    compute_effective_resistance,
)


@dataclass
class BaselineResult:
    name: str
    selected_states: list[PortState]
    min_gamma: float
    total_cost: float
    gamma_results: dict[tuple[str, str], GammaResult]
    is_deployable: bool = True


def single_default_state(
    candidate_states: list[PortState],
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    noise_sigma: float,
    operator_rho: float,
) -> BaselineResult:
    """Single default port state: first available single-pair state."""
    default = [candidate_states[0]] if candidate_states else []
    gammas = compute_all_gammas(bundle, operator, default, noise_sigma, operator_rho)
    return BaselineResult(
        name="single_default",
        selected_states=default,
        min_gamma=min_gamma(gammas),
        total_cost=design_cost(default),
        gamma_results=gammas,
    )


def all_pairwise_port_states(
    candidate_states: list[PortState],
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    noise_sigma: float,
    operator_rho: float,
    max_states: int,
) -> BaselineResult:
    """Take all available pairwise port states up to max_states."""
    pairwise = [s for s in candidate_states if s.kind == "single_pair"]
    selected = pairwise[:max_states]
    gammas = compute_all_gammas(bundle, operator, selected, noise_sigma, operator_rho)
    return BaselineResult(
        name="all_pairwise",
        selected_states=selected,
        min_gamma=min_gamma(gammas),
        total_cost=design_cost(selected),
        gamma_results=gammas,
    )


def random_states(
    candidate_states: list[PortState],
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    noise_sigma: float,
    operator_rho: float,
    max_states: int,
    rng: np.random.Generator,
    n_trials: int = 10,
) -> BaselineResult:
    """Random state selection, best of n_trials."""
    best_result: BaselineResult | None = None
    best_mg = -np.inf

    for trial in range(n_trials):
        n_select = min(max_states, len(candidate_states))
        indices = rng.choice(len(candidate_states), size=n_select, replace=False)
        selected = [candidate_states[i] for i in indices]
        gammas = compute_all_gammas(bundle, operator, selected, noise_sigma, operator_rho)
        mg = min_gamma(gammas)
        if mg > best_mg:
            best_mg = mg
            best_result = BaselineResult(
                name=f"random_trial_{trial}",
                selected_states=selected,
                min_gamma=mg,
                total_cost=design_cost(selected),
                gamma_results=gammas,
            )

    if best_result is None:
        best_result = BaselineResult(
            name="random_fallback",
            selected_states=[],
            min_gamma=-np.inf,
            total_cost=0.0,
            gamma_results={},
        )
    best_result.name = "random_best_of_n"
    return best_result


def max_current_norm_states(
    candidate_states: list[PortState],
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    noise_sigma: float,
    operator_rho: float,
    max_states: int,
) -> BaselineResult:
    """Select states with maximum total current norm (most excitation)."""
    scored = []
    for s in candidate_states:
        total_norm = 0.0
        for h_name in bundle.hypotheses:
            i_e = compute_state_current(bundle, h_name, s)
            total_norm += float(np.linalg.norm(i_e))
        scored.append((total_norm, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [s for _, s in scored[:max_states]]
    gammas = compute_all_gammas(bundle, operator, selected, noise_sigma, operator_rho)
    return BaselineResult(
        name="max_current_norm",
        selected_states=selected,
        min_gamma=min_gamma(gammas),
        total_cost=design_cost(selected),
        gamma_results=gammas,
    )


def max_effective_resistance_contrast_states(
    candidate_states: list[PortState],
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    noise_sigma: float,
    operator_rho: float,
    max_states: int,
) -> BaselineResult:
    """Select states that maximize effective resistance contrast between hypotheses."""
    scored = []
    for s in candidate_states:
        reffs = []
        for h_name in bundle.hypotheses:
            reffs.append(compute_effective_resistance(bundle, h_name, s))
        contrast = max(reffs) - min(reffs) if reffs else 0.0
        scored.append((contrast, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [s for _, s in scored[:max_states]]
    gammas = compute_all_gammas(bundle, operator, selected, noise_sigma, operator_rho)
    return BaselineResult(
        name="max_eff_resistance_contrast",
        selected_states=selected,
        min_gamma=min_gamma(gammas),
        total_cost=design_cost(selected),
        gamma_results=gammas,
    )


def oracle_truth_margin_states(
    candidate_states: list[PortState],
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    noise_sigma: float,
    operator_rho: float,
    max_states: int,
    true_hypothesis: str = "H1_via",
) -> BaselineResult:
    """Oracle: select states that maximize Gamma vs the true hypothesis.

    NON-DEPLOYABLE. Uses knowledge of true hypothesis.
    """
    remaining = list(candidate_states)
    selected: list[PortState] = []

    for _ in range(max_states):
        best_s: PortState | None = None
        best_mg = -np.inf
        for cand in remaining:
            test_set = selected + [cand]
            gammas = compute_all_gammas(bundle, operator, test_set, noise_sigma, operator_rho)
            # Focus on pairs involving the true hypothesis
            true_gammas = [r.gamma for (h, g), r in gammas.items()
                          if h == true_hypothesis or g == true_hypothesis]
            score = min(true_gammas) if true_gammas else -np.inf
            if score > best_mg:
                best_mg = score
                best_s = cand

        if best_s is None:
            break
        selected.append(best_s)
        remaining.remove(best_s)

    gammas = compute_all_gammas(bundle, operator, selected, noise_sigma, operator_rho)
    return BaselineResult(
        name="oracle_truth_margin",
        selected_states=selected,
        min_gamma=min_gamma(gammas),
        total_cost=design_cost(selected),
        gamma_results=gammas,
        is_deployable=False,
    )


def run_all_baselines(
    candidate_states: list[PortState],
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    noise_sigma: float,
    operator_rho: float,
    max_states: int,
    rng: np.random.Generator,
) -> dict[str, BaselineResult]:
    """Run all baseline strategies and return results."""
    return {
        "single_default": single_default_state(
            candidate_states, bundle, operator, noise_sigma, operator_rho,
        ),
        "all_pairwise": all_pairwise_port_states(
            candidate_states, bundle, operator, noise_sigma, operator_rho, max_states,
        ),
        "random": random_states(
            candidate_states, bundle, operator, noise_sigma, operator_rho, max_states, rng,
        ),
        "max_current_norm": max_current_norm_states(
            candidate_states, bundle, operator, noise_sigma, operator_rho, max_states,
        ),
        "max_eff_resistance_contrast": max_effective_resistance_contrast_states(
            candidate_states, bundle, operator, noise_sigma, operator_rho, max_states,
        ),
        "oracle_truth_margin": oracle_truth_margin_states(
            candidate_states, bundle, operator, noise_sigma, operator_rho, max_states,
        ),
    }
