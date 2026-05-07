"""Baseline state design strategies and signal computation for E27."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from operators import (
    OperatorBundle,
    CandidateDefect,
    solve_potential,
    edge_currents,
    schur_edge_current_perturbation,
    magnetic_signature,
    compute_edge_signal,
    design_schur_states,
    design_random_states,
    design_max_current_norm_states,
    design_max_resistance_contrast_states,
    design_oracle_states,
)


@dataclass
class BaselineResult:
    """Result of a baseline state-design strategy over all defects."""
    strategy: str
    states: list[np.ndarray]
    per_defect_signals: dict[str, list[float]]  # defect_id -> [signal per state]
    per_defect_gammas: dict[str, list[float]]   # defect_id -> [gamma per state]
    max_signals: dict[str, float]                # defect_id -> max signal across states
    max_gammas: dict[str, float]                 # defect_id -> max gamma across states
    mean_signal: float
    mean_gamma: float
    positive_gamma_rate: float


def run_strategy(
    bundle: OperatorBundle,
    strategy_name: str,
    states: list[np.ndarray],
    candidates: list[CandidateDefect],
    cfg: dict,
    W: np.ndarray | None = None,
) -> BaselineResult:
    """Run a state-design strategy over all candidate defects and compute signals/gammas."""
    from operators import compute_edge_gamma

    per_defect_signals: dict[str, list[float]] = {}
    per_defect_gammas: dict[str, list[float]] = {}
    max_signals: dict[str, float] = {}
    max_gammas: dict[str, float] = {}

    for defect in candidates:
        sigs = []
        gams = []
        for b in states:
            phi = solve_potential(bundle, b)
            signal = compute_edge_signal(bundle, phi, defect, W)
            gamma = compute_edge_gamma(bundle, signal, cfg)
            sigs.append(signal)
            gams.append(gamma)
        per_defect_signals[defect.defect_id] = sigs
        per_defect_gammas[defect.defect_id] = gams
        max_signals[defect.defect_id] = max(sigs) if sigs else 0.0
        max_gammas[defect.defect_id] = max(gams) if gams else -np.inf

    all_signals = [s for sigs in per_defect_signals.values() for s in sigs]
    all_gammas = [g for gams in per_defect_gammas.values() for g in gams]
    positive_count = sum(1 for g in all_gammas if g > 0)
    positive_rate = positive_count / len(all_gammas) if all_gammas else 0.0

    return BaselineResult(
        strategy=strategy_name,
        states=states,
        per_defect_signals=per_defect_signals,
        per_defect_gammas=per_defect_gammas,
        max_signals=max_signals,
        max_gammas=max_gammas,
        mean_signal=float(np.mean(all_signals)) if all_signals else 0.0,
        mean_gamma=float(np.mean(all_gammas)) if all_gammas else 0.0,
        positive_gamma_rate=positive_rate,
    )


def compute_pairwise_defect_delta(
    bundle: OperatorBundle,
    candidates: list[CandidateDefect],
    states: list[np.ndarray],
    W: np.ndarray | None = None,
) -> dict[tuple[str, str], float]:
    """Compute pairwise defect discrimination delta: ||W(dY_q - dY_r)||_2."""
    pairwise: dict[tuple[str, str], float] = {}

    # Precompute signatures per defect per state
    sigs_per_defect: dict[str, list[np.ndarray]] = {}
    for defect in candidates:
        sigs = []
        for b in states:
            phi = solve_potential(bundle, b)
            delta_i = schur_edge_current_perturbation(bundle, phi, defect)
            delta_y = magnetic_signature(bundle, delta_i)
            if W is not None:
                delta_y = W @ delta_y
            sigs.append(delta_y)
        sigs_per_defect[defect.defect_id] = sigs

    for i, d1 in enumerate(candidates):
        for j, d2 in enumerate(candidates):
            if i >= j:
                continue
            max_delta = 0.0
            for s_idx in range(len(states)):
                diff = sigs_per_defect[d1.defect_id][s_idx] - sigs_per_defect[d2.defect_id][s_idx]
                delta = float(np.linalg.norm(diff))
                max_delta = max(max_delta, delta)
            pairwise[(d1.defect_id, d2.defect_id)] = max_delta

    return pairwise


def compute_pairwise_defect_gamma(
    pairwise_delta: dict[tuple[str, str], float],
    defects: list[CandidateDefect],
    cfg: dict,
) -> dict[tuple[str, str], float]:
    """Compute pairwise Gamma = delta - epsilon - rho_q - rho_r - tau."""
    epsilon = float(cfg["noise_sigma"])
    tau = float(cfg["decision"]["tau_threshold"])
    rho_base = float(cfg["operator_perturbation"]["rho_scale"])

    defect_map = {d.defect_id: d for d in defects}
    pairwise_gamma: dict[tuple[str, str], float] = {}

    for (id1, id2), delta in pairwise_delta.items():
        rho1 = rho_base * delta
        rho2 = rho_base * delta
        gamma = delta - epsilon - rho1 - rho2 - tau
        pairwise_gamma[(id1, id2)] = gamma

    return pairwise_gamma


def run_all_baselines(
    bundle: OperatorBundle,
    candidates: list[CandidateDefect],
    cfg: dict,
    W: np.ndarray | None = None,
) -> list[BaselineResult]:
    """Run all baseline strategies and return results."""
    results: list[BaselineResult] = []

    bl_cfg = cfg["baselines"]
    n_states = int(bl_cfg["random_state_count"])

    # 1. Random states
    random_states = design_random_states(bundle, cfg, n_states)
    results.append(run_strategy(bundle, "random", random_states, candidates, cfg, W))

    # 2. Max current norm states
    max_current_states = design_max_current_norm_states(bundle, cfg, n_states)
    results.append(run_strategy(bundle, "max_current_norm", max_current_states, candidates, cfg, W))

    # 3. Max resistance contrast states
    max_res_states = design_max_resistance_contrast_states(bundle, candidates, cfg, n_states)
    results.append(run_strategy(bundle, "max_resistance_contrast", max_res_states, candidates, cfg, W))

    # 4. Schur voltage-drop states (core new method)
    n_schur = int(cfg["schur"]["state_count"])
    schur_states = design_schur_states(bundle, candidates, cfg, n_schur)
    results.append(run_strategy(bundle, "schur_voltage_drop", schur_states, candidates, cfg, W))

    # 5. Oracle states (non-deployable upper bound)
    oracle_states = design_oracle_states(bundle, candidates, cfg, n_states)
    results.append(run_strategy(bundle, "oracle", oracle_states, candidates, cfg, W))

    return results


def to_summary_dict(result: BaselineResult) -> dict:
    """Convert BaselineResult to a compact summary dict."""
    return {
        "strategy": result.strategy,
        "state_count": len(result.states),
        "mean_signal": result.mean_signal,
        "mean_gamma": result.mean_gamma,
        "positive_gamma_rate": result.positive_gamma_rate,
        "defect_count": len(result.max_signals),
        "best_defect_signal": float(max(result.max_signals.values())) if result.max_signals else 0.0,
        "best_defect_gamma": float(max(result.max_gammas.values())) if result.max_gammas else -1.0,
    }
