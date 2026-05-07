"""Sequential refusal policy for E26.

After each state is added, computes the consistent set C_k(Y).
Stops if |C_k| = 1 and min Gamma > 0.
Refuses if k = S_max and min Gamma <= 0.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np

from networks import HypothesisBundle
from operators import OperatorBundle
from port_states import PortState
from gamma import (
    compute_state_current, map_edge_currents_to_field,
    compute_all_gammas, min_gamma, compute_profile_delta, GammaResult,
)


@dataclass
class RefusalStep:
    step: int
    state: PortState
    consistent_set: list[str]
    consistent_set_size: int
    min_gamma: float
    residuals: dict[str, float]
    decision: str  # "continue", "stop_identified", "refuse"


@dataclass
class RefusalTrace:
    steps: list[RefusalStep] = field(default_factory=list)
    final_decision: str = "continue"  # "identified", "refused", "max_states_reached"
    identified_hypothesis: str | None = None
    states_used: int = 0


def compute_observation(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    state: PortState,
    true_hypothesis: str,
    noise_sigma: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate noisy observation for a port state under the true hypothesis."""
    i_true = compute_state_current(bundle, true_hypothesis, state)
    f_true = map_edge_currents_to_field(i_true, bundle, operator, true_hypothesis)
    noise = rng.normal(0.0, noise_sigma, size=f_true.shape)
    return f_true + noise


def compute_residuals(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    observations: list[tuple[PortState, np.ndarray]],
) -> dict[str, float]:
    """Compute residual for each hypothesis given all observations.

    For each hypothesis h, residual = sum_s ||y_s - F_h(s)||^2.
    """
    residuals = {}
    for h_name in bundle.hypotheses:
        total_residual = 0.0
        for state, y in observations:
            i_h = compute_state_current(bundle, h_name, state)
            f_h = map_edge_currents_to_field(i_h, bundle, operator, h_name)
            total_residual += float(np.linalg.norm(y - f_h))
        residuals[h_name] = total_residual
    return residuals


def consistent_set_from_residuals(
    residuals: dict[str, float],
    tau: float,
) -> list[str]:
    """Return hypotheses with residual <= tau."""
    return [h for h, r in residuals.items() if r <= tau]


def run_refusal_policy(
    bundle: HypothesisBundle,
    operator: OperatorBundle,
    selected_states: list[PortState],
    true_hypothesis: str,
    noise_sigma: float,
    operator_rho: float,
    rng: np.random.Generator,
    tau_scale: float = 1.5,
    S_max: int | None = None,
) -> RefusalTrace:
    """Run sequential refusal policy as states are added.

    Args:
        bundle: Hypothesis bundle for the layout.
        operator: Forward operator.
        selected_states: Ordered list of selected states to test.
        true_hypothesis: Ground truth hypothesis for synthetic data.
        noise_sigma: Measurement noise standard deviation.
        operator_rho: Operator perturbation bound.
        rng: Random number generator.
        tau_scale: Multiplier for acceptance threshold.
        S_max: Maximum states before forced refusal.
    """
    obs_dim = operator.A.shape[0]
    tau = tau_scale * noise_sigma * np.sqrt(obs_dim)

    observations: list[tuple[PortState, np.ndarray]] = []
    trace = RefusalTrace()

    S_max = S_max if S_max is not None else len(selected_states)

    for k, state in enumerate(selected_states):
        y = compute_observation(bundle, operator, state, true_hypothesis, noise_sigma, rng)
        observations.append((state, y))

        residuals = compute_residuals(bundle, operator, observations)
        consistent = consistent_set_from_residuals(residuals, tau)

        used_states = observations  # current set
        gammas = compute_all_gammas(
            bundle, operator, [s for s, _ in used_states], noise_sigma, operator_rho,
        )
        mg = min_gamma(gammas)

        if len(consistent) == 1 and mg > 0:
            decision = "stop_identified"
        elif k + 1 >= S_max and mg <= 0:
            decision = "refuse"
        else:
            decision = "continue"

        step = RefusalStep(
            step=k + 1,
            state=state,
            consistent_set=consistent,
            consistent_set_size=len(consistent),
            min_gamma=mg,
            residuals=residuals,
            decision=decision,
        )
        trace.steps.append(step)

        if decision == "stop_identified":
            trace.final_decision = "identified"
            trace.identified_hypothesis = consistent[0]
            trace.states_used = k + 1
            return trace
        elif decision == "refuse":
            trace.final_decision = "refused"
            trace.states_used = k + 1
            return trace

    trace.final_decision = "max_states_reached"
    trace.states_used = len(selected_states)
    return trace


def compute_expected_states_used(
    traces: list[RefusalTrace],
) -> float:
    """Average number of states used across multiple refusal traces."""
    if not traces:
        return 0.0
    return float(np.mean([t.states_used for t in traces]))


def compute_wrong_accept_rate(
    traces: list[RefusalTrace],
    true_hypotheses: list[str],
) -> float:
    """Rate at which a wrong hypothesis is accepted (misidentified)."""
    if not traces:
        return 0.0
    wrong = 0
    for trace, truth in zip(traces, true_hypotheses):
        if trace.final_decision == "identified" and trace.identified_hypothesis != truth:
            wrong += 1
    return wrong / len(traces)


def compute_truth_missing_rate(
    traces: list[RefusalTrace],
    true_hypotheses: list[str],
) -> float:
    """Rate at which the true hypothesis is missing from the consistent set."""
    if not traces:
        return 0.0
    missing = 0
    for trace, truth in zip(traces, true_hypotheses):
        last_step = trace.steps[-1] if trace.steps else None
        if last_step and truth not in last_step.consistent_set:
            missing += 1
    return missing / len(traces)
