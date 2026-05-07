"""Gamma computation and state selection algorithms for E26.

Core: robust profile margin Gamma_{hg}(U) for each hypothesis pair.
Implements greedy gamma and two-step lookahead state selection.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from networks import (
    solve_network, HypothesisBundle, PortLayout, HYPOTHESIS_NAMES,
)
from port_states import PortState, design_cost
from operators import OperatorBundle

CRITICAL_PAIRS = [
    ("H1_via", "H3_return"),
    ("H1_via", "H2_model_gap"),
    ("H3_return", "H0_open"),
    ("H1_via", "H0_open"),
    ("H2_model_gap", "H3_return"),
    ("H0_open", "H2_model_gap"),
]


@dataclass
class StateObservation:
    """Observation of a port state under a hypothesis."""
    state: PortState
    hypothesis: str
    edge_currents: np.ndarray
    magnetic_field: np.ndarray       # A @ i_edge (or mapped to sensor field)
    effective_resistance: float
    current_norm: float


@dataclass
class GammaResult:
    pair: tuple[str, str]
    delta: float                      # profile distance
    tau: float                        # threshold for hypothesis g
    eps: float                        # noise epsilon
    rho_h: float                      # operator perturbation for h
    rho_g: float                      # operator perturbation for g
    gamma: float                      # robust margin
    is_separable: bool                # gamma > 0


@dataclass
class SelectionTrace:
    step: int
    selected_state: PortState
    min_gamma_before: float
    min_gamma_after: float
    improvement: float
    consistent_set_size: int
    truth_missing: bool
    wrong_accept: bool


def compute_state_current(
    bundle: HypothesisBundle, hypothesis: str, state: PortState,
) -> np.ndarray:
    """Compute edge currents for a hypothesis and port state."""
    hyp = bundle.hypotheses[hypothesis]
    return solve_network(hyp, state.b, bundle.layout)


def map_edge_currents_to_field(
    edge_currents: np.ndarray,
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    hypothesis: str,
) -> np.ndarray:
    """Map edge currents to magnetic field at sensor positions.

    Uses a simplified mapping: project edge currents onto the operator's
    current basis via incidence-weighted spatial distribution.
    """
    n_cells = operator.index["cell_count"]
    layers = operator.index["layers"]
    layout = bundle.layout
    n_internal = layout.n_internal
    side = max(2, int(np.round(np.sqrt(n_internal))))

    # Distribute edge currents to grid cells
    # Each internal node maps to a region of cells
    cells_per_node_side = max(1, int(np.sqrt(n_cells)) // side)
    total_cells = n_cells * layers * 2 + n_cells * (layers - 1)  # sheet + via dims

    field = np.zeros(operator.A.shape[0], dtype=float)

    # Simplified mapping: use the operator's columns directly
    # Map edge currents to operator current vector
    current_full = np.zeros(operator.A.shape[1], dtype=float)

    sheet_slices = operator.index["sheet_slices"]
    via_slices = operator.index["via_slices"]

    # Map node-potential derived edge currents to spatial current distribution
    # Use incidence matrix to get node injection, then distribute to cells
    D = bundle.incidence_matrices[hypothesis]
    node_injection = D @ edge_currents  # (n_internal,)

    # Distribute node injection to grid cells in the top layer
    for node in range(n_internal):
        ny = node // side
        nx = node % side
        cell_y_start = ny * cells_per_node_side
        cell_x_start = nx * cells_per_node_side

        injection = node_injection[node]
        if abs(injection) < 1e-15:
            continue

        # Map to x and y sheet currents in the first (top) layer
        for dy in range(cells_per_node_side):
            for dx in range(cells_per_node_side):
                cell_idx = (cell_y_start + dy) * int(np.sqrt(n_cells)) + (cell_x_start + dx)
                if cell_idx >= n_cells:
                    continue
                if (0, "x") in sheet_slices:
                    sl_x = sheet_slices[(0, "x")]
                    current_full[sl_x.start + cell_idx] += injection * 0.5 / (cells_per_node_side ** 2)
                if (0, "y") in sheet_slices:
                    sl_y = sheet_slices[(0, "y")]
                    current_full[sl_y.start + cell_idx] += injection * 0.5 / (cells_per_node_side ** 2)

    field = operator.A @ current_full
    return field


def compute_profile_delta(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    states: list[PortState],
    h: str, g: str,
    noise_sigma: float,
) -> float:
    """Compute profile distance delta_{hg}(U) for a set of states.

    delta = min ||F_h(U, theta_h) - F_g(U, theta_g)||_2
    where F_h stacks the magnetic field predictions for all states.

    For computational tractability, use the conservative proxy:
    delta = mean over states of ||field_h(s) - field_g(s)||_2
    """
    if not states:
        return 0.0

    deltas = []
    for state in states:
        i_h = compute_state_current(bundle, h, state)
        i_g = compute_state_current(bundle, g, state)
        f_h = map_edge_currents_to_field(i_h, bundle, operator, h)
        f_g = map_edge_currents_to_field(i_g, bundle, operator, g)
        d = float(np.linalg.norm(f_h - f_g))
        deltas.append(d)

    return float(np.mean(deltas)) if deltas else 0.0


def compute_gamma(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    states: list[PortState],
    h: str, g: str,
    noise_sigma: float,
    operator_rho: float,
    tau_scale: float = 1.5,
) -> GammaResult:
    """Compute robust profile margin Gamma_{hg}(U)."""
    delta = compute_profile_delta(bundle, operator, states, h, g, noise_sigma)

    # Tau: acceptance threshold (scaled by observation dimension)
    obs_dim = operator.A.shape[0]
    tau_g = tau_scale * noise_sigma * np.sqrt(obs_dim)

    # Epsilon: noise level
    eps = noise_sigma * np.sqrt(obs_dim)

    rho_h = operator_rho
    rho_g = operator_rho

    gamma_val = delta - tau_g - eps - rho_h - rho_g

    return GammaResult(
        pair=(h, g),
        delta=delta,
        tau=tau_g,
        eps=eps,
        rho_h=rho_h,
        rho_g=rho_g,
        gamma=gamma_val,
        is_separable=gamma_val > 0,
    )


def compute_all_gammas(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    states: list[PortState],
    noise_sigma: float,
    operator_rho: float,
    critical_pairs: list[tuple[str, str]] | None = None,
) -> dict[tuple[str, str], GammaResult]:
    """Compute Gamma for all critical pairs."""
    pairs = critical_pairs if critical_pairs is not None else CRITICAL_PAIRS
    result = {}
    for h, g in pairs:
        if h in bundle.hypotheses and g in bundle.hypotheses:
            result[(h, g)] = compute_gamma(
                bundle, operator, states, h, g, noise_sigma, operator_rho,
            )
    return result


def min_gamma(gamma_results: dict) -> float:
    """Minimum Gamma across all pairs."""
    if not gamma_results:
        return -np.inf
    return min(r.gamma for r in gamma_results.values())


def greedy_gamma_selection(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    candidate_states: list[PortState],
    noise_sigma: float,
    operator_rho: float,
    max_states: int,
    critical_pairs: list[tuple[str, str]] | None = None,
) -> tuple[list[PortState], list[SelectionTrace]]:
    """Greedy state selection maximizing min Gamma improvement per cost.

    Returns (selected_states, trace).
    """
    selected: list[PortState] = []
    remaining = list(candidate_states)
    trace: list[SelectionTrace] = []

    for step in range(max_states):
        if not remaining:
            break

        gamma_before = min_gamma(compute_all_gammas(
            bundle, operator, selected, noise_sigma, operator_rho, critical_pairs,
        ))

        best_state: PortState | None = None
        best_score = -np.inf
        best_gamma_after = -np.inf

        for cand in remaining:
            test_set = selected + [cand]
            gammas = compute_all_gammas(
                bundle, operator, test_set, noise_sigma, operator_rho, critical_pairs,
            )
            mg = min_gamma(gammas)
            score = mg - gamma_before - cand.cost

            if score > best_score:
                best_score = score
                best_state = cand
                best_gamma_after = mg

        if best_state is None:
            break

        selected.append(best_state)
        remaining.remove(best_state)

        # Recompute consistent set diagnostics
        trace.append(SelectionTrace(
            step=step + 1,
            selected_state=best_state,
            min_gamma_before=gamma_before,
            min_gamma_after=best_gamma_after,
            improvement=best_gamma_after - gamma_before,
            consistent_set_size=_estimate_consistent_set_size(bundle, operator, selected, noise_sigma),
            truth_missing=False,  # updated by caller
            wrong_accept=False,
        ))

    return selected, trace


def two_step_lookahead_selection(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    candidate_states: list[PortState],
    noise_sigma: float,
    operator_rho: float,
    max_states: int,
    critical_pairs: list[tuple[str, str]] | None = None,
) -> tuple[list[PortState], list[SelectionTrace]]:
    """Two-step lookahead state selection.

    At each step, evaluate all (b, b') pairs and pick the one that maximizes
    min Gamma(U + {b, b'}) - cost(b) - cost(b').
    """
    selected: list[PortState] = []
    remaining = list(candidate_states)
    trace: list[SelectionTrace] = []

    step = 0
    while step < max_states and remaining:
        gamma_before = min_gamma(compute_all_gammas(
            bundle, operator, selected, noise_sigma, operator_rho, critical_pairs,
        ))

        best_pair: tuple[PortState | None, PortState | None] = (None, None)
        best_score = -np.inf
        best_gamma_after = -np.inf

        if len(remaining) >= 2 and step + 1 < max_states:
            for i in range(min(len(remaining), 20)):
                for j in range(i + 1, min(len(remaining), 20)):
                    cand1, cand2 = remaining[i], remaining[j]
                    test_set = selected + [cand1, cand2]
                    gammas = compute_all_gammas(
                        bundle, operator, test_set, noise_sigma, operator_rho, critical_pairs,
                    )
                    mg = min_gamma(gammas)
                    score = mg - gamma_before - cand1.cost - cand2.cost

                    if score > best_score:
                        best_score = score
                        best_pair = (cand1, cand2)
                        best_gamma_after = mg

        # Also try single-step for odd max_states or final step
        for cand in remaining:
            test_set = selected + [cand]
            gammas = compute_all_gammas(
                bundle, operator, test_set, noise_sigma, operator_rho, critical_pairs,
            )
            mg = min_gamma(gammas)
            score = mg - gamma_before - cand.cost

            if score > best_score:
                best_score = score
                best_pair = (cand, None)
                best_gamma_after = mg

        if best_pair[0] is None:
            break

        for s in best_pair:
            if s is not None and s in remaining:
                selected.append(s)
                remaining.remove(s)
                step += 1
                trace.append(SelectionTrace(
                    step=step,
                    selected_state=s,
                    min_gamma_before=gamma_before,
                    min_gamma_after=best_gamma_after,
                    improvement=best_gamma_after - gamma_before,
                    consistent_set_size=_estimate_consistent_set_size(bundle, operator, selected, noise_sigma),
                    truth_missing=False,
                    wrong_accept=False,
                ))

    return selected, trace


def _estimate_consistent_set_size(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    states: list[PortState],
    noise_sigma: float,
) -> int:
    """Estimate how many hypotheses would be in the consistent set.

    Uses the minimum residual across hypotheses as a proxy.
    Returns: number of hypotheses whose residual <= threshold.
    """
    if not states:
        return len(bundle.hypotheses)

    residuals = {}
    for h_name in bundle.hypotheses:
        total_residual = 0.0
        for state in states:
            i_h = compute_state_current(bundle, h_name, state)
            f_h = map_edge_currents_to_field(i_h, bundle, operator, h_name)
            # Compare against a "reference" field from the first hypothesis
            # Simplified: use the field norm as a proxy for residual
            total_residual += float(np.linalg.norm(f_h))
        residuals[h_name] = total_residual

    if not residuals:
        return 0

    min_res = min(residuals.values())
    threshold = min_res + 3.0 * noise_sigma * np.sqrt(operator.A.shape[0])

    return sum(1 for r in residuals.values() if r <= threshold)


def compute_current_path_overlap(
    bundle: HypothesisBundle,
    state: PortState,
    h: str, g: str,
) -> float:
    """Current-path overlap between two hypotheses for a given state.

    Maps edge currents to node injection space (same dimension for all hypotheses)
    then computes cosine similarity there.
    """
    i_h = compute_state_current(bundle, h, state)
    i_g = compute_state_current(bundle, g, state)
    D_h = bundle.incidence_matrices[h]
    D_g = bundle.incidence_matrices[g]
    n_h = D_h @ i_h
    n_g = D_g @ i_g
    dot = float(np.abs(np.dot(n_h, n_g)))
    denom = float(np.linalg.norm(n_h)) * float(np.linalg.norm(n_g)) + 1e-18
    return dot / denom


def compute_effective_resistance(
    bundle: HypothesisBundle,
    hypothesis: str,
    state: PortState,
) -> float:
    """Effective resistance between the primary source-sink pair."""
    i_e = compute_state_current(bundle, hypothesis, state)
    power = float(np.sum(i_e ** 2 * bundle.hypotheses[hypothesis].resistances))
    current_mag = float(np.sum(np.abs(state.b))) / 2.0
    if current_mag < 1e-15:
        return np.inf
    return power / (current_mag ** 2)
