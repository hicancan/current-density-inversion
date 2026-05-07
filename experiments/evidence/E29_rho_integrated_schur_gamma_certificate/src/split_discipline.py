"""Calibration/evaluation split discipline.

Strictly enforces:
- Calibration geometries determine epsilon, tau, and rho recommended values.
- Evaluation geometries report positive_gamma_rate, wrong_accept_rate,
  truth_missing_rate, empty_rate.
- No threshold is chosen from evaluation rows.
"""
from __future__ import annotations

import numpy as np


def split_geometries(
    edges: np.ndarray,
    widths: np.ndarray,
    thicknesses: np.ndarray,
    defects: list[dict],
    calibration_fraction: float = 0.5,
    seed: int = 42,
) -> dict:
    """Split geometries and defects into calibration and evaluation sets.

    Args:
        edges: (E, 2, 3) edge endpoints.
        widths: (E,) edge widths.
        thicknesses: (E,) edge thicknesses.
        defects: list of candidate defect dicts.
        calibration_fraction: fraction of defects assigned to calibration.
        seed: random seed for reproducible split.

    Returns dict with calibration and evaluation subsets.
    """
    rng = np.random.default_rng(seed)
    n_defects = len(defects)

    indices = rng.permutation(n_defects)
    n_cal = max(1, int(n_defects * calibration_fraction))

    cal_indices = sorted(indices[:n_cal].tolist())
    eval_indices = sorted(indices[n_cal:].tolist())

    cal_defects = [defects[i] for i in cal_indices]
    eval_defects = [defects[i] for i in eval_indices]

    return {
        "calibration": {
            "defect_indices": cal_indices,
            "defects": cal_defects,
            "n_defects": len(cal_defects),
            "role": "determines epsilon, tau, rho recommended values",
        },
        "evaluation": {
            "defect_indices": eval_indices,
            "defects": eval_defects,
            "n_defects": len(eval_defects),
            "role": "reports positive_gamma_rate, wrong_accept_rate, truth_missing_rate, empty_rate",
        },
        "calibration_fraction": calibration_fraction,
        "seed": seed,
        "split_discipline_note": (
            "Thresholds (epsilon, tau) are computed exclusively from "
            "calibration geometries. Evaluation geometries only report rates. "
            "No threshold is chosen from evaluation rows."
        ),
    }


def split_audit(split_info: dict) -> dict:
    """Audit the calibration/evaluation split for discipline violations.

    Returns dict with audit results.
    """
    cal_n = split_info["calibration"]["n_defects"]
    eval_n = split_info["evaluation"]["n_defects"]
    total = cal_n + eval_n

    violations = []
    if cal_n == 0:
        violations.append("calibration set is empty")
    if eval_n == 0:
        violations.append("evaluation set is empty")
    if cal_n > eval_n + total * 0.2:
        violations.append(
            f"calibration set ({cal_n}) is suspiciously large vs evaluation ({eval_n})"
        )

    # Check that defect types are represented in both splits
    cal_types = {d["defect_type"] for d in split_info["calibration"]["defects"]}
    eval_types = {d["defect_type"] for d in split_info["evaluation"]["defects"]}

    missing_from_cal = eval_types - cal_types
    missing_from_eval = cal_types - eval_types

    if missing_from_eval:
        violations.append(
            f"defect types in calibration missing from evaluation: {missing_from_eval}"
        )

    return {
        "calibration_count": cal_n,
        "evaluation_count": eval_n,
        "total_count": total,
        "calibration_fraction": cal_n / max(total, 1),
        "violations": violations,
        "discipline_enforced": len(violations) == 0,
        "calibration_defect_types": sorted(cal_types),
        "evaluation_defect_types": sorted(eval_types),
        "types_missing_from_calibration": sorted(missing_from_cal),
        "types_missing_from_evaluation": sorted(missing_from_eval),
    }
