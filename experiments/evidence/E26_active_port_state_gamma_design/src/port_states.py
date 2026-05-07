"""Feasible port-state set generation for E26.

A port excitation b ∈ R^p satisfies:
  sum(b) = 0               (KCL conservation)
  |b_j| <= I_max_j         (per-port current limit)
  ||b||_1 <= 2 * I_max     (total current limit)

Candidate set U_1:
  - Single-pair states: b = e_a - e_b  for a != b
  - Balanced multi-source/multi-sink patterns
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class PortState:
    state_id: str
    b: np.ndarray           # port current vector (p,)
    kind: str                # "single_pair", "balanced_pair", "multi_source"
    cost: float              # c(b) = alpha + beta*|b|_0 + gamma*|b|_2^2
    metadata: dict


def generate_feasible_states(
    layout,
    rng: np.random.Generator,
    max_states: int = 24,
    I_max: float = 2.0,
    alpha: float = 1.0,
    beta: float = 0.5,
    gamma: float = 0.1,
) -> list[PortState]:
    """Generate the feasible port-state candidate set for a layout.

    Returns a list of PortState objects satisfying hardware constraints.
    """
    p = layout.p
    states: list[PortState] = []

    # 1. Single-pair states: e_a - e_b for all a != b
    pair_idx = 0
    for a in range(p):
        for b_idx in range(p):
            if a == b_idx:
                continue
            b_vec = np.zeros(p, dtype=float)
            b_vec[a] = 1.0
            b_vec[b_idx] = -1.0
            c = alpha + beta * float(np.count_nonzero(b_vec)) + gamma * float(np.sum(b_vec ** 2))
            states.append(PortState(
                state_id=f"pair_{pair_idx:03d}_p{a}_p{b_idx}",
                b=b_vec, kind="single_pair", cost=c,
                metadata={"ports": [int(a), int(b_idx)], "amplitude": 1.0},
            ))
            pair_idx += 1

    # 2. Balanced two-pair states: e_a - e_b + e_c - e_d
    balanced_idx = 0
    if p >= 4:
        for _ in range(min(p * 4, max_states // 2)):
            nodes = rng.choice(p, size=4, replace=False)
            b_vec = np.zeros(p, dtype=float)
            b_vec[nodes[0]] = 0.7
            b_vec[nodes[1]] = -0.7
            b_vec[nodes[2]] = 0.3
            b_vec[nodes[3]] = -0.3
            c = alpha + beta * float(np.count_nonzero(b_vec)) + gamma * float(np.sum(b_vec ** 2))
            states.append(PortState(
                state_id=f"balanced_{balanced_idx:03d}",
                b=b_vec, kind="balanced_pair", cost=c,
                metadata={"ports": nodes.tolist(), "amplitudes": [0.7, -0.7, 0.3, -0.3]},
            ))
            balanced_idx += 1

    # 3. Scaled single-pair states (different amplitudes)
    scale_idx = 0
    amp_values = [0.5, 1.5]
    for amp in amp_values:
        for a in range(min(p, 3)):
            for b_idx in range(min(p, 3)):
                if a == b_idx:
                    continue
                b_vec = np.zeros(p, dtype=float)
                b_vec[a] = amp
                b_vec[b_idx] = -amp
                c = alpha + beta * float(np.count_nonzero(b_vec)) + gamma * float(np.sum(b_vec ** 2))
                states.append(PortState(
                    state_id=f"scaled_{scale_idx:03d}_amp{amp}_p{a}_p{b_idx}",
                    b=b_vec, kind="single_pair", cost=c,
                    metadata={"ports": [int(a), int(b_idx)], "amplitude": amp},
                ))
                scale_idx += 1

    # 4. Multi-source patterns (one source, multiple sinks)
    if p >= 3:
        multi_idx = 0
        for _ in range(min(p * 2, 8)):
            source = int(rng.integers(0, p))
            sinks = [s for s in range(p) if s != source]
            n_sinks = min(len(sinks), rng.integers(2, min(p, 4)))
            sink_nodes = list(rng.choice(sinks, size=n_sinks, replace=False))
            b_vec = np.zeros(p, dtype=float)
            b_vec[source] = 1.0
            sink_amp = 1.0 / n_sinks
            for s in sink_nodes:
                b_vec[s] = -sink_amp
            c = alpha + beta * float(np.count_nonzero(b_vec)) + gamma * float(np.sum(b_vec ** 2))
            states.append(PortState(
                state_id=f"multi_{multi_idx:03d}",
                b=b_vec, kind="multi_source", cost=c,
                metadata={"source": source, "sinks": sink_nodes},
            ))
            multi_idx += 1

    # 5. Add amplitude-varied versions of select states
    varied_idx = 0
    for base_state in list(states)[:8]:
        for factor in [0.5, 2.0]:
            b_varied = base_state.b * factor
            if np.max(np.abs(b_varied)) > I_max * 2:
                continue
            c = alpha + beta * float(np.count_nonzero(b_varied)) + gamma * float(np.sum(b_varied ** 2))
            states.append(PortState(
                state_id=f"varied_{varied_idx:03d}",
                b=b_varied, kind=base_state.kind, cost=c,
                metadata={"base": base_state.state_id, "factor": factor},
            ))
            varied_idx += 1

    # Deduplicate and trim
    seen = set()
    unique_states = []
    for s in states:
        key = tuple(np.round(s.b, 8))
        if key not in seen:
            seen.add(key)
            unique_states.append(s)

    return unique_states[:max_states]


def state_measurement_cost(state: PortState) -> float:
    """Measurement cost for a single state."""
    return state.cost


def design_cost(selected_states: list[PortState]) -> float:
    """Total cost of a measurement design U."""
    return sum(s.cost for s in selected_states)
