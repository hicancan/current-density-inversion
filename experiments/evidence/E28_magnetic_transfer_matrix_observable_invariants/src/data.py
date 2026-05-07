"""Data generation for E28 consistent set analysis.

Generates observed transfer matrices by adding noise to the clean transfer
matrices, simulating the measurement process.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from operators import OperatorBundle, PortExcitation
from hypotheses import ConductanceModel
from transfer_matrix import compute_transfer_matrix

FAMILY_TO_TRUTH = {
    "no_via_clean": "H0_no_via",
    "single_via_observable": "H1_via",
    "dense_via_cluster": "H1_via",
    "model_gap_registration": "H2_model_gap",
    "model_gap_standoff": "H2_model_gap",
    "return_path_deep_loop": "H3_return_path",
}

HYP_TO_FAMILY = {v: k for k, v in FAMILY_TO_TRUTH.items()}


@dataclass
class TransferCase:
    case_id: str
    family: str
    truth_hypothesis: str
    T_clean: np.ndarray
    T_observed: np.ndarray
    noise_std: float
    metadata: dict


def generate_transfer_cases(
    bundle: OperatorBundle,
    cond_models: dict[str, ConductanceModel],
    ports: PortExcitation,
    cfg: dict,
) -> list[TransferCase]:
    """Generate cases: each case is an observed (noisy) transfer matrix.

    The truth hypothesis determines the clean transfer matrix.
    Noise is added to simulate measurement error.
    """
    rng = np.random.default_rng(int(cfg["random_seed"]))
    noise_sigma = float(cfg["noise_sigma"])
    noise_frac = float(cfg["noise_frac_t_mat"])
    families = cfg["families"]
    count = int(cfg["case_count_per_family"])

    cases: list[TransferCase] = []

    for family in families:
        if family not in FAMILY_TO_TRUTH:
            raise ValueError(f"Unknown family: {family}")
        truth = FAMILY_TO_TRUTH[family]
        T_clean = compute_transfer_matrix(bundle, cond_models[truth], ports)

        for i in range(count):
            # Per-element noise std: sigma for sensor noise, plus fraction of per-element signal
            t_norm = float(np.linalg.norm(T_clean, "fro"))
            n_elements = max(T_clean.size, 1)
            signal_per_element = t_norm / np.sqrt(n_elements)
            noise_level = max(noise_sigma, noise_frac * signal_per_element)
            noise = rng.normal(0.0, noise_level, size=T_clean.shape)
            T_obs = T_clean + noise

            cases.append(TransferCase(
                case_id=f"E28_{family}_{i:03d}",
                family=family,
                truth_hypothesis=truth,
                T_clean=T_clean,
                T_observed=T_obs,
                noise_std=float(noise_level),
                metadata={
                    "generator": "E28_transfer_invariants_v1",
                    "family": family,
                    "noise_sigma": noise_sigma,
                    "noise_frac": noise_frac,
                    "noise_level": float(noise_level),
                    "expected_frob_noise": float(noise_level * np.sqrt(n_elements)),
                },
            ))

    return cases


def consistent_set_analysis(
    cases: list[TransferCase],
    T_matrices: dict[str, np.ndarray],
    eps: float,
) -> dict:
    """Compute consistent set for each case.

    A hypothesis h is consistent with observed T_obs if:
        ||T_obs - T_h||_F <= eps

    Returns per-case consistent sets and aggregate statistics.
    """
    per_case = []
    truth_in_consistent = 0
    singleton_correct = 0
    singleton_wrong = 0
    ambiguity_count = 0
    empty_count = 0

    for case in cases:
        residuals = {}
        for h, T_h in T_matrices.items():
            residuals[h] = float(np.linalg.norm(case.T_observed - T_h, "fro"))

        consistent = [h for h, r in residuals.items() if r <= eps]
        non_consistent = [h for h, r in residuals.items() if r > eps]

        if case.truth_hypothesis in consistent:
            truth_in_consistent += 1
        if len(consistent) == 1 and consistent[0] == case.truth_hypothesis:
            singleton_correct += 1
        if len(consistent) == 1 and consistent[0] != case.truth_hypothesis:
            singleton_wrong += 1
        if len(consistent) > 1:
            ambiguity_count += 1
        if len(consistent) == 0:
            empty_count += 1

        per_case.append({
            "case_id": case.case_id,
            "family": case.family,
            "truth": case.truth_hypothesis,
            "consistent": consistent,
            "non_consistent": non_consistent,
            "residuals": residuals,
        })

    n = max(len(cases), 1)

    return {
        "per_case": per_case,
        "n_cases": len(cases),
        "consistent_set_nonempty_rate": (n - empty_count) / n,
        "ambiguity_rate": ambiguity_count / n,
        "empty_rate": empty_count / n,
        "truth_in_consistent_rate": truth_in_consistent / n,
        "singleton_correct_rate": singleton_correct / n,
        "singleton_wrong_rate": singleton_wrong / n,
        "epsilon": eps,
    }
