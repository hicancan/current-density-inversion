"""Transfer matrix computation for E28.

T_y = A @ C @ D^T @ L^+ @ B

where:
- A: Biot-Savart operator (M_obs x E)
- C: conductance matrix (E x E, diagonal)
- D^T: incidence matrix transpose (E x V)
- L^+: pseudo-inverse of graph Laplacian L = D C D^T (V x V)
- B: port excitation matrix (V x S)
- T_y: magnetic transfer matrix (M_obs x S)
"""

from __future__ import annotations

import numpy as np

from operators import OperatorBundle, PortExcitation
from hypotheses import ConductanceModel

LAPLACIAN_RCOND = 1e-10


def compute_transfer_matrix(
    bundle: OperatorBundle,
    cond: ConductanceModel,
    ports: PortExcitation,
    rcond: float = LAPLACIAN_RCOND,
) -> np.ndarray:
    """Compute T_y = A @ C @ D^T @ L^+ @ B.

    Uses pinv with rcond for numerical stability.
    """
    A = bundle.A
    D = bundle.D
    C = cond.C
    B_mat = ports.B

    L = D @ C @ D.T
    Linv = np.linalg.pinv(L, rcond=rcond)

    T_y = A @ C @ D.T @ Linv @ B_mat
    return T_y


def compute_all_transfer_matrices(
    bundle: OperatorBundle,
    cond_models: dict[str, ConductanceModel],
    ports: PortExcitation,
) -> dict[str, np.ndarray]:
    """Compute transfer matrix for each hypothesis."""
    return {
        h: compute_transfer_matrix(bundle, cond, ports)
        for h, cond in cond_models.items()
    }


def transfer_matrix_diagnostics(T_y: np.ndarray, hypothesis: str) -> dict:
    """Compute diagnostics for a single transfer matrix."""
    M, S = T_y.shape
    U, sv, Vt = np.linalg.svd(T_y, full_matrices=False)
    effective_rank = int(np.sum(sv > 1e-10 * sv[0])) if sv[0] > 0 else 0
    return {
        "hypothesis": hypothesis,
        "shape": [M, S],
        "singular_values": sv.tolist(),
        "effective_rank": effective_rank,
        "condition_number": float(sv[0] / max(sv[-1] if len(sv) > 0 else 1, 1e-30)),
        "frobenius_norm": float(np.linalg.norm(T_y, "fro")),
        "max_column_norm": float(np.max(np.linalg.norm(T_y, axis=0))),
        "min_column_norm": float(np.min(np.linalg.norm(T_y, axis=0) + 1e-30)),
    }


def all_transfer_matrix_diagnostics(
    T_matrices: dict[str, np.ndarray],
) -> dict:
    return {h: transfer_matrix_diagnostics(T, h) for h, T in T_matrices.items()}
