"""Physics-constrained multilayer PDN inverse solver.

Implements the graph_kcl_differentiable_inverse algorithm:
  1. Initialize with ridge solution
  2. Iteratively minimize composite loss:
     L = w_b * ||A*x - b||^2 + w_kcl * ||D*x||^2 + w_topo * ||D*x||^2
       + w_via * ||x_via||_1 + w_prior * ||x - x_ridge||^2
  3. Project via KCL divergence constraint

Uses scipy L-BFGS-B for CPU-first optimization.
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

from src.forward_adapter import build_div_matrix


def ridge_solve(A: np.ndarray, b: np.ndarray, alpha: float) -> np.ndarray:
    """Plain ridge regression: (A^T A + alpha I)^{-1} A^T b."""
    AtA = A.T @ A
    Atb = A.T @ b
    reg = alpha * np.eye(AtA.shape[0])
    return np.linalg.solve(AtA + reg, Atb)


def constrained_ridge_solve(
    A: np.ndarray, b: np.ndarray, alpha: float,
    C: np.ndarray, cv: np.ndarray, cw: float
) -> np.ndarray:
    """Ridge regression with soft KCL constraint."""
    AtA = A.T @ A + cw * (C.T @ C)
    Atb = A.T @ b + cw * (C.T @ cv)
    reg = alpha * np.eye(AtA.shape[0])
    return np.linalg.solve(AtA + reg, Atb)


def _smooth_l1(x: np.ndarray, eps: float = 1e-4) -> float:
    """Smooth approximation of L1 norm for differentiability."""
    return float(np.sum(np.sqrt(x ** 2 + eps ** 2) - eps))


def _smooth_l1_grad(x: np.ndarray, eps: float = 1e-4) -> np.ndarray:
    """Gradient of smooth L1."""
    return x / np.sqrt(x ** 2 + eps ** 2)


def graph_kcl_differentiable_inverse(
    A: np.ndarray,
    b_obs: np.ndarray,
    cfg: dict,
    n: int,
) -> dict:
    """Physics-constrained multilayer PDN inverse.

    Algorithm:
    1. Warm-start with ridge solution
    2. Optimize composite loss with L-BFGS-B:
       L = w_b * ||Ax - b||^2 + w_kcl * ||Dx||^2 + w_via * smooth_l1(x_via)
         + w_prior * ||x - x_init||^2
    3. Post-project via KCL constraint

    Returns dict with predicted currents, diagnostics, and timing.
    """
    t0 = time.perf_counter()

    pl = n * n
    D = build_div_matrix(n)

    # Weights from config
    w_b = float(cfg.get("inverse_b_weight", 1.0))
    w_kcl = float(cfg.get("inverse_kcl_weight", 0.5))
    w_topo = float(cfg.get("inverse_topo_weight", 0.3))
    w_via = float(cfg.get("inverse_via_sparsity_weight", 0.1))
    w_prior = float(cfg.get("inverse_layer_prior_weight", 0.05))
    max_iter = int(cfg.get("inverse_max_iter", 200))
    alpha = float(cfg.get("ridge_alpha", 0.01))

    # Step 1: Warm-start with constrained ridge
    cw = float(cfg.get("kcl_constraint_weight", 0.5))
    cv = np.zeros(D.shape[0])
    x_init = constrained_ridge_solve(A, b_obs, alpha, D, cv, cw)

    # Precompute for efficiency
    AtA = A.T @ A
    Atb = A.T @ b_obs
    DtD = D.T @ D
    b_norm2 = float(np.dot(b_obs, b_obs))

    via_start = 8 * pl  # start index of via channels
    via_end = 11 * pl

    # Step 2: L-BFGS-B optimization
    n_calls = [0]

    def objective(x):
        n_calls[0] += 1
        residual_b = A @ x - b_obs
        loss_b = w_b * float(np.dot(residual_b, residual_b))

        div_x = D @ x
        loss_kcl = w_kcl * float(np.dot(div_x, div_x))

        loss_via = w_via * _smooth_l1(x[via_start:via_end])

        diff = x - x_init
        loss_prior = w_prior * float(np.dot(diff, diff))

        total = loss_b + loss_kcl + loss_via + loss_prior
        return total

    def gradient(x):
        residual_b = A @ x - b_obs
        grad_b = 2.0 * w_b * (AtA @ x - Atb)

        grad_kcl = 2.0 * w_kcl * (DtD @ x)

        grad_via = np.zeros_like(x)
        grad_via[via_start:via_end] = w_via * _smooth_l1_grad(x[via_start:via_end])

        grad_prior = 2.0 * w_prior * (x - x_init)

        return grad_b + grad_kcl + grad_via + grad_prior

    result = scipy_minimize(
        objective,
        x_init.copy(),
        jac=gradient,
        method="L-BFGS-B",
        options={"maxiter": max_iter, "ftol": 1e-12, "gtol": 1e-8},
    )

    x_opt = result.x

    # Step 3: Post-projection via KCL
    # Soft projection: solve for x that minimizes ||x - x_opt||^2 s.t. D*x ≈ 0
    proj_weight = 10.0 * cw
    PtP = np.eye(len(x_opt)) + proj_weight * DtD
    Ptb_proj = x_opt + proj_weight * DtD @ np.zeros(len(x_opt))
    # Simpler: just solve (I + proj_w * D^T D) x_proj = x_opt
    x_proj = np.linalg.solve(PtP, x_opt)

    t1 = time.perf_counter()

    # Diagnostics
    b_pred = A @ x_proj
    b_residual_vec = b_pred - b_obs
    physical_b_residual = float(np.sqrt(np.mean(b_residual_vec ** 2)))
    kcl_residual = float(np.sqrt(np.mean((D @ x_proj) ** 2)))
    topology_residual = kcl_residual  # same constraint
    runtime = t1 - t0

    return {
        "predicted": x_proj,
        "init_ridge": x_init,
        "optimizer_result": {
            "success": bool(result.success),
            "n_iter": int(result.nit),
            "n_fev": n_calls[0],
            "final_loss": float(result.fun),
        },
        "physical_b_residual": physical_b_residual,
        "kcl_residual": kcl_residual,
        "topology_residual": topology_residual,
        "runtime_s": runtime,
    }
