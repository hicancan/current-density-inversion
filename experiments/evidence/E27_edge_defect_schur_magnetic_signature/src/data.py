"""Generated E27 edge-defect cases with ground-truth magnetic signatures."""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np

from operators import (
    OperatorBundle,
    CandidateDefect,
    solve_potential,
    edge_currents,
    schur_potential_perturbation,
    schur_edge_current_perturbation,
    magnetic_signature,
)


@dataclass
class GeneratedCase:
    case_id: str
    family: str
    truth_defect: CandidateDefect
    phi_baseline: np.ndarray
    i_baseline: np.ndarray
    phi_defect: np.ndarray
    i_defect: np.ndarray
    delta_i: np.ndarray
    delta_y: np.ndarray
    y_clean: np.ndarray
    y_observed: np.ndarray
    W: np.ndarray | None = None

    def to_metrics_dict(self) -> dict:
        return {
            "case_id": self.case_id,
            "family": self.family,
            "defect_id": self.truth_defect.defect_id,
            "edge_role": self.truth_defect.edge_role,
            "alpha": float(self.truth_defect.alpha),
            "R_q": float(self.truth_defect.R_q),
            "baseline_current_norm": float(np.linalg.norm(self.i_baseline)),
            "defect_current_norm": float(np.linalg.norm(self.i_defect)),
            "delta_i_norm": float(np.linalg.norm(self.delta_i)),
            "delta_y_norm": float(np.linalg.norm(self.delta_y)),
            "y_clean_shape": list(self.y_clean.shape),
        }


def _generate_baseline_state(bundle: OperatorBundle, rng: np.random.Generator) -> np.ndarray:
    """Generate a baseline port excitation state for the network."""
    V = bundle.D.shape[0]
    u = int(rng.integers(0, V))
    v = int(rng.integers(0, V))
    while v == u:
        v = int(rng.integers(0, V))
    b = np.zeros(V, dtype=float)
    b[u] = 1.0
    b[v] = -1.0
    return b


def generate_case(
    bundle: OperatorBundle,
    cfg: dict,
    family: str,
    index: int,
    defect: CandidateDefect,
    rng: np.random.Generator,
) -> GeneratedCase:
    """Generate a single edge-defect case with ground-truth magnetic signature."""
    b_baseline = _generate_baseline_state(bundle, rng)

    # Baseline potential and currents (no defect)
    phi_baseline = solve_potential(bundle, b_baseline)
    i_baseline = edge_currents(bundle, phi_baseline)
    y_clean_baseline = bundle.A @ i_baseline

    # Defect-perturbed potential and currents (Sherman-Morrison)
    phi_defect = schur_potential_perturbation(bundle, phi_baseline, defect)
    i_defect = edge_currents(bundle, phi_defect)
    y_clean_defect = bundle.A @ i_defect

    delta_i = i_defect - i_baseline
    delta_y = y_clean_defect - y_clean_baseline

    # Add noise
    sigma = float(cfg["noise_sigma"])
    noise = rng.normal(0.0, sigma, size=bundle.A.shape[0])
    y_observed = y_clean_defect + noise

    return GeneratedCase(
        case_id=f"E27_{family}_{index:03d}",
        family=family,
        truth_defect=defect,
        phi_baseline=phi_baseline,
        i_baseline=i_baseline,
        phi_defect=phi_defect,
        i_defect=i_defect,
        delta_i=delta_i,
        delta_y=delta_y,
        y_clean=y_clean_defect,
        y_observed=y_observed,
    )


def generate_cases(bundle: OperatorBundle, cfg: dict, defects: list[CandidateDefect]) -> list[GeneratedCase]:
    """Generate all cases: one per candidate defect."""
    rng = np.random.default_rng(int(cfg["random_seed"]) + 3333)
    cases: list[GeneratedCase] = []

    # Group defects by family
    family_defects: dict[str, list[CandidateDefect]] = {}
    for d in defects:
        family_defects.setdefault(d.family, []).append(d)

    count_per_family = int(cfg["case_count_per_family"])
    for family in cfg["families"]:
        if family not in family_defects:
            continue
        family_list = family_defects[family]
        for i in range(min(count_per_family, len(family_list))):
            cases.append(generate_case(bundle, cfg, family, i, family_list[i], rng))

    return cases


def compute_sherman_morrison_validation_error(
    bundle: OperatorBundle,
    phi_baseline: np.ndarray,
    defect: CandidateDefect,
) -> float:
    """Validate Sherman-Morrison formula against direct solve.

    Direct: Solve (L + alpha*a_q*a_q^T) phi_direct = b (gauge fixed).
    SM: phi_sm = phi_baseline - (alpha*v_q/(1+alpha*R_q)) * G * a_q.

    Returns ||phi_sm - phi_direct||_2 / ||phi_direct||_2.
    """
    from operators import schur_potential_perturbation
    import numpy as np

    phi_sm = schur_potential_perturbation(bundle, phi_baseline, defect)

    V = bundle.D.shape[0]
    a_int = defect.a_q[1:]
    L_perturbed = bundle.L + defect.alpha * np.outer(a_int, a_int)

    # Get b from the baseline solution
    b_int = bundle.L @ phi_baseline[1:]
    try:
        phi_direct_int = np.linalg.solve(L_perturbed, b_int)
    except np.linalg.LinAlgError:
        phi_direct_int = np.linalg.lstsq(L_perturbed, b_int, rcond=None)[0]

    phi_direct = np.zeros(V, dtype=float)
    phi_direct[1:] = phi_direct_int

    rel_err = float(np.linalg.norm(phi_sm - phi_direct) / max(np.linalg.norm(phi_direct), 1e-16))
    return rel_err
