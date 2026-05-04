"""Simple baselines for E19.

The baseline is intentionally modest: ridge reconstructs the full current map
and then applies heuristic topology labels based on via and deep return energy.
This is not expected to be a strong final method; it provides a sanity contrast
against posterior topology reasoning.
"""

from __future__ import annotations

import numpy as np

from operators import OperatorBundle


def ridge_current_reconstruction(y: np.ndarray, bundle: OperatorBundle, alpha: float) -> np.ndarray:
    A = bundle.A
    norms = np.linalg.norm(A, axis=0)
    scale = np.maximum(norms, 1e-30)
    As = A / scale[None, :]
    lhs = As.T @ As + float(alpha) * np.eye(As.shape[1])
    rhs = As.T @ y
    coef = np.linalg.solve(lhs, rhs)
    return coef / scale


def classify_ridge(x: np.ndarray, bundle: OperatorBundle, cfg: dict) -> str:
    idx = bundle.index
    via_energy = 0.0
    for sl in idx["via_slices"].values():
        via_energy += float(np.linalg.norm(x[sl]))
    bottom_energy = 0.0
    last = int(idx["layers"]) - 1
    for comp in ["x", "y"]:
        bottom_energy += float(np.linalg.norm(x[idx["sheet_slices"][(last, comp)]]))

    sheet_energy = 0.0
    for sl in idx["sheet_slices"].values():
        sheet_energy += float(np.linalg.norm(x[sl]))

    via_ratio = via_energy / max(sheet_energy + via_energy, 1e-18)
    bottom_ratio = bottom_energy / max(sheet_energy, 1e-18)

    # Model-gap cannot be discovered by a current-only ridge map; this is a
    # deliberate limitation recorded in baseline metrics.
    if via_ratio > 0.075:
        return "H1_via"
    if bottom_ratio > 0.42:
        return "H3_return_path"
    return "H0_no_via"


def run_ridge_baseline(case, bundle: OperatorBundle, cfg: dict) -> dict:
    alpha = float(cfg["baseline"]["ridge_alpha"])
    x = ridge_current_reconstruction(case.field_observed, bundle, alpha)
    pred = classify_ridge(x, bundle, cfg)
    return {
        "case_id": case.case_id,
        "truth": case.truth_hypothesis,
        "predicted": pred,
        "correct": pred == case.truth_hypothesis,
    }
