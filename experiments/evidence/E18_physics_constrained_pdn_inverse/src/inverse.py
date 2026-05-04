"""Physics-constrained multilayer PDN inverse solver (E18.1).

E18.1 FIX: Uses column-normalized (scaled) operator for numerically stable
inversion. All solvers now support scaled mode.
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize as scipy_minimize

_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR.parent))

from src.forward_adapter import build_kcl_matrix, scale_operator, unscale_solution


def ridge_solve(A: np.ndarray, b: np.ndarray, alpha: float) -> np.ndarray:
    """Plain ridge regression: (A^T A + alpha I)^{-1} A^T b."""
    AtA = A.T @ A
    Atb = A.T @ b
    reg = alpha * np.eye(AtA.shape[0])
    return np.linalg.solve(AtA + reg, Atb)


def ridge_solve_scaled(A: np.ndarray, b: np.ndarray, alpha_rel: float) -> np.ndarray:
    """Ridge with column-normalized A for numerical stability."""
    A_s, b_s, col_norms, b_scale = scale_operator(A, b)
    AtA = A_s.T @ A_s
    alpha_abs = alpha_rel * float(np.mean(np.diag(AtA)))
    Atb = A_s.T @ b_s
    reg = alpha_abs * np.eye(AtA.shape[0])
    y = np.linalg.solve(AtA + reg, Atb)
    return unscale_solution(y, col_norms)


def constrained_ridge_solve(
    A: np.ndarray, b: np.ndarray, alpha: float,
    C: np.ndarray, cv: np.ndarray, cw: float
) -> np.ndarray:
    """Ridge regression with soft KCL constraint."""
    AtA = A.T @ A + cw * (C.T @ C)
    Atb = A.T @ b + cw * (C.T @ cv)
    reg = alpha * np.eye(AtA.shape[0])
    return np.linalg.solve(AtA + reg, Atb)


def constrained_ridge_solve_scaled(
    A: np.ndarray, b: np.ndarray, alpha_rel: float,
    C: np.ndarray, cv: np.ndarray, cw_rel: float
) -> np.ndarray:
    """Scaled constrained ridge for numerical stability."""
    A_s, b_s, col_norms, b_scale = scale_operator(A, b)
    # Scale C columns the same way
    C_s = C / col_norms[None, :]
    cv_s = cv  # already in constraint space
    AtA = A_s.T @ A_s
    alpha_abs = alpha_rel * float(np.mean(np.diag(AtA)))
    cw_abs = cw_rel * float(np.mean(np.diag(AtA)))
    M = AtA + cw_abs * (C_s.T @ C_s)
    rhs = A_s.T @ b_s + cw_abs * (C_s.T @ cv_s)
    reg = alpha_abs * np.eye(M.shape[0])
    y = np.linalg.solve(M + reg, rhs)
    return unscale_solution(y, col_norms)


def _smooth_l1(x: np.ndarray, eps: float = 1e-4) -> float:
    return float(np.sum(np.sqrt(x ** 2 + eps ** 2) - eps))


def _smooth_l1_grad(x: np.ndarray, eps: float = 1e-4) -> np.ndarray:
    return x / np.sqrt(x ** 2 + eps ** 2)


def graph_kcl_differentiable_inverse(
    A: np.ndarray,
    b_obs: np.ndarray,
    cfg: dict,
    n: int,
    *,
    use_projection: bool = True,
    use_via_sparsity: bool = True,
    use_kcl: bool = True,
) -> dict:
    """Physics-constrained multilayer PDN inverse (E18.1 scaled version).

    E18.1 FIX: Works in column-normalized space for numerical stability.
    """
    t0 = time.perf_counter()

    pl = n * n
    D = build_kcl_matrix(n, cfg)

    # Scale operator
    A_s, b_s, col_norms, b_scale = scale_operator(A, b_obs)
    D_s = D / col_norms[None, :]

    # Weights from config (relative)
    alpha_rel = float(cfg.get("ridge_alpha_rel", 1e-3))
    cw_rel = float(cfg.get("kcl_weight_rel", 1e-2))
    w_via_rel = float(cfg.get("via_sparsity_weight_rel", 1e-3))
    w_prior_rel = float(cfg.get("prior_weight_rel", 1e-3))
    max_iter = int(cfg.get("inverse_max_iter", 200))

    # Compute scale reference
    AtA_s = A_s.T @ A_s
    scale_ref = float(np.mean(np.diag(AtA_s)))
    alpha_abs = alpha_rel * scale_ref
    cw_abs = cw_rel * scale_ref if use_kcl else 0.0
    w_via_abs = w_via_rel * scale_ref if use_via_sparsity else 0.0
    w_prior_abs = w_prior_rel * scale_ref

    # Step 1: Warm-start with scaled constrained ridge
    DtD_s = D_s.T @ D_s
    cv = np.zeros(D_s.shape[0])
    M_init = AtA_s + cw_abs * DtD_s + alpha_abs * np.eye(AtA_s.shape[0])
    rhs_init = A_s.T @ b_s
    y_init = np.linalg.solve(M_init, rhs_init)

    # Step 2: L-BFGS-B optimization in scaled space
    via_start = 8 * pl
    via_end = 11 * pl
    Atb_s = A_s.T @ b_s
    n_calls = [0]

    def objective(y):
        n_calls[0] += 1
        res = A_s @ y - b_s
        loss = float(np.dot(res, res))
        if use_kcl:
            dv = D_s @ y
            loss += cw_abs * float(np.dot(dv, dv))
        if use_via_sparsity:
            loss += w_via_abs * _smooth_l1(y[via_start:via_end])
        diff = y - y_init
        loss += w_prior_abs * float(np.dot(diff, diff))
        return loss

    def gradient(y):
        g = 2.0 * (AtA_s @ y - Atb_s)
        if use_kcl:
            g += 2.0 * cw_abs * (DtD_s @ y)
        if use_via_sparsity:
            gv = np.zeros_like(y)
            gv[via_start:via_end] = w_via_abs * _smooth_l1_grad(y[via_start:via_end])
            g += gv
        g += 2.0 * w_prior_abs * (y - y_init)
        return g

    result = scipy_minimize(
        objective, y_init.copy(), jac=gradient, method="L-BFGS-B",
        options={"maxiter": max_iter, "ftol": 1e-14, "gtol": 1e-10},
    )
    y_opt = result.x

    # Step 3: Unscale first, then post-project in physical space
    x_opt_phys = unscale_solution(y_opt, col_norms)

    if use_projection:
        DtD_phys = D.T @ D
        proj_w = float(cfg.get("kcl_projection_weight", 5.0))
        PtP = np.eye(len(x_opt_phys)) + proj_w * DtD_phys
        x_result = np.linalg.solve(PtP, x_opt_phys)
    else:
        x_result = x_opt_phys

    t1 = time.perf_counter()

    # Diagnostics
    b_pred = A @ x_result
    physical_b_residual = float(np.sqrt(np.mean((b_pred - b_obs) ** 2)))
    kcl_residual_val = float(np.sqrt(np.mean((D @ x_result) ** 2)))

    return {
        "predicted": x_result,
        "init_ridge": unscale_solution(y_init, col_norms),
        "optimizer_result": {
            "success": bool(result.success),
            "n_iter": int(result.nit),
            "n_fev": n_calls[0],
            "final_loss": float(result.fun),
        },
        "physical_b_residual": physical_b_residual,
        "kcl_residual": kcl_residual_val,
        "topology_residual": kcl_residual_val,
        "runtime_s": t1 - t0,
        "scale_info": {
            "col_norm_min": float(np.min(col_norms)),
            "col_norm_max": float(np.max(col_norms)),
            "b_scale": b_scale,
            "scale_ref": scale_ref,
        },
    }
