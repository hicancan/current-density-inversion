"""Baseline methods for E18 unified comparison.

All baselines operate on the same forward operator A and return a flat
predicted vector of shape (11*n*n,).
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR.parent))

from src.forward_adapter import build_div_matrix
from src.inverse import ridge_solve, constrained_ridge_solve


def bl_naive_single_layer(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    """Naive single-layer baseline: invert only L1 (top layer)."""
    n = int(cfg["grid_size"])
    pl = n * n
    bf = case["field"].ravel()
    As = A[:, :2 * pl].copy()
    pred = np.zeros(11 * pl)
    pred[:2 * pl] = ridge_solve(As, bf, float(cfg["ridge_alpha"]))
    return pred


def bl_incorrect_two_layer(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    """Incorrect two-layer: invert L1 + L4 only, ignoring inner layers."""
    n = int(cfg["grid_size"])
    pl = n * n
    bf = case["field"].ravel()
    sel = list(range(0, 2 * pl)) + list(range(6 * pl, 8 * pl))
    As = A[:, sel].copy()
    sol = ridge_solve(As, bf, float(cfg["ridge_alpha"]))
    pred = np.zeros(11 * pl)
    for si, col in enumerate(sel):
        pred[col] = sol[si]
    return pred


def bl_ridge_least_squares(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    """Full ridge regression over all 11 channels."""
    return ridge_solve(A, case["field"].ravel(), float(cfg["ridge_alpha"]))


def bl_graph_kcl_aware(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    """Graph/KCL-aware constrained ridge."""
    n = int(cfg["grid_size"])
    D = build_div_matrix(n)
    cw = float(cfg["kcl_constraint_weight"])
    cv = np.zeros(D.shape[0])
    return constrained_ridge_solve(
        A, case["field"].ravel(), float(cfg["ridge_alpha"]), D, cv, cw
    )


BASELINES = {
    "naive_single_layer": bl_naive_single_layer,
    "incorrect_two_layer": bl_incorrect_two_layer,
    "ridge_least_squares": bl_ridge_least_squares,
    "graph_kcl_aware": bl_graph_kcl_aware,
}
