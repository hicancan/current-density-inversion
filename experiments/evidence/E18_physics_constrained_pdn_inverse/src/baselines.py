"""Baseline methods for E18.1 unified comparison.

E18.1: Adds zero_predictor, oracle, scaled variants, and ablations.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR.parent))

from src.forward_adapter import build_kcl_matrix
from src.inverse import (
    ridge_solve, ridge_solve_scaled,
    constrained_ridge_solve, constrained_ridge_solve_scaled,
    graph_kcl_differentiable_inverse,
)


# --- Sanity baselines ---

def bl_zero_predictor(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    n = int(cfg["grid_size"])
    return np.zeros(11 * n * n)


def bl_oracle_ground_truth(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    return case["flat_ground_truth"].copy()


# --- Scientific baselines ---

def bl_naive_single_layer(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    n = int(cfg["grid_size"]); pl = n * n
    bf = case["field"].ravel()
    As = A[:, :2 * pl].copy()
    pred = np.zeros(11 * pl)
    pred[:2 * pl] = ridge_solve_scaled(As, bf, float(cfg.get("ridge_alpha_rel", 1e-3)))
    return pred


def bl_incorrect_two_layer(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    n = int(cfg["grid_size"]); pl = n * n
    bf = case["field"].ravel()
    sel = list(range(0, 2 * pl)) + list(range(6 * pl, 8 * pl))
    As = A[:, sel].copy()
    sol = ridge_solve_scaled(As, bf, float(cfg.get("ridge_alpha_rel", 1e-3)))
    pred = np.zeros(11 * pl)
    for si, col in enumerate(sel):
        pred[col] = sol[si]
    return pred


def bl_ridge_unscaled(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    return ridge_solve(A, case["field"].ravel(), float(cfg.get("ridge_alpha", 0.01)))


def bl_ridge_scaled(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    return ridge_solve_scaled(A, case["field"].ravel(), float(cfg.get("ridge_alpha_rel", 1e-3)))


def bl_graph_kcl_aware_unscaled(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    n = int(cfg["grid_size"])
    D = build_kcl_matrix(n, cfg)
    cw = float(cfg.get("kcl_constraint_weight", 0.5))
    cv = np.zeros(D.shape[0])
    return constrained_ridge_solve(
        A, case["field"].ravel(), float(cfg.get("ridge_alpha", 0.01)), D, cv, cw
    )


def bl_graph_kcl_aware_scaled(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    n = int(cfg["grid_size"])
    D = build_kcl_matrix(n, cfg)
    cv = np.zeros(D.shape[0])
    return constrained_ridge_solve_scaled(
        A, case["field"].ravel(),
        float(cfg.get("ridge_alpha_rel", 1e-3)),
        D, cv, float(cfg.get("kcl_weight_rel", 1e-2))
    )


# --- New method variants ---

def bl_new_scaled(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    n = int(cfg["grid_size"])
    result = graph_kcl_differentiable_inverse(A, case["field"].ravel(), cfg, n)
    return result["predicted"]


def bl_new_no_projection(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    n = int(cfg["grid_size"])
    result = graph_kcl_differentiable_inverse(
        A, case["field"].ravel(), cfg, n, use_projection=False
    )
    return result["predicted"]


def bl_new_no_via_sparsity(case: dict, A: np.ndarray, cfg: dict) -> np.ndarray:
    n = int(cfg["grid_size"])
    result = graph_kcl_differentiable_inverse(
        A, case["field"].ravel(), cfg, n, use_via_sparsity=False
    )
    return result["predicted"]


# --- Registry ---

SANITY_BASELINES = {
    "zero_predictor": bl_zero_predictor,
    "oracle_ground_truth": bl_oracle_ground_truth,
}

SCIENTIFIC_BASELINES = {
    "naive_single_layer": bl_naive_single_layer,
    "incorrect_two_layer": bl_incorrect_two_layer,
    "ridge_unscaled": bl_ridge_unscaled,
    "ridge_scaled": bl_ridge_scaled,
    "graph_kcl_aware_unscaled": bl_graph_kcl_aware_unscaled,
    "graph_kcl_aware_scaled": bl_graph_kcl_aware_scaled,
}

NEW_METHODS = {
    "graph_kcl_differentiable_inverse_scaled": bl_new_scaled,
    "new_no_projection": bl_new_no_projection,
    "new_no_via_sparsity": bl_new_no_via_sparsity,
}

# All methods (order matters for leaderboard)
ALL_METHODS = {**SANITY_BASELINES, **SCIENTIFIC_BASELINES, **NEW_METHODS}

# Backward compat
BASELINES = {**SCIENTIFIC_BASELINES}
