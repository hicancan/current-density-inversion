"""Resolution operator diagnostics for OQCI.

Copied from E19.2 resolution.py.
"""

from __future__ import annotations

import numpy as np

from operators import OperatorBundle


def resolution_operator(bundle: OperatorBundle, alpha: float = 0.0) -> np.ndarray:
    A = bundle.A
    AtA = A.T @ A
    if alpha > 0:
        R = np.linalg.solve(AtA + alpha * np.eye(AtA.shape[0]), AtA)
    else:
        try:
            Ainv = np.linalg.pinv(A)
            R = Ainv @ A
        except np.linalg.LinAlgError:
            return np.zeros((A.shape[1], A.shape[1]))
    return R


def resolution_diagnostics(bundle: OperatorBundle, alpha: float = 1e-6) -> dict:
    R = resolution_operator(bundle, alpha)
    dim = R.shape[0]

    trace_R = float(np.trace(R))
    eigenvalues = np.sort(np.linalg.eigvalsh(R))[::-1]
    resolution_rank = sum(1 for ev in eigenvalues if ev > 0.5)

    n_sample = min(10, dim)
    indices = np.linspace(0, dim - 1, n_sample, dtype=int)
    psf_widths = []
    for i in indices:
        col = R[:, i]
        diag_val = abs(col[i])
        total_energy = np.linalg.norm(col)
        psf_widths.append({
            "index": int(i),
            "diagonal": float(diag_val),
            "total_energy": float(total_energy),
            "diagonal_ratio": float(diag_val / max(total_energy, 1e-18)),
        })

    condition_number = float(eigenvalues[0] / max(eigenvalues[-1], 1e-18)) if eigenvalues.size > 1 else 0.0

    return {
        "dimension": dim,
        "trace_R": trace_R,
        "trace_ratio": trace_R / dim,
        "resolution_rank": resolution_rank,
        "resolution_rank_ratio": resolution_rank / dim,
        "condition_number": condition_number,
        "eigenvalue_summary": {
            "top_5": eigenvalues[:5].tolist(),
            "bottom_5": eigenvalues[-5:].tolist() if len(eigenvalues) >= 5 else eigenvalues.tolist(),
        },
        "psf_sample": psf_widths,
    }


def effective_observable_rank(bundle: OperatorBundle) -> dict:
    _, S, _ = np.linalg.svd(bundle.A, compute_uv=False)
    s_max = S[0] if S.size > 0 else 1.0
    thresholds = [0.01, 0.05, 0.10]
    result = {
        "singular_values_top_10": S[:10].tolist(),
        "max_singular_value": float(s_max),
        "min_singular_value": float(S[-1]) if S.size > 0 else 0.0,
    }
    for t in thresholds:
        rank = sum(1 for s in S if s > t * s_max)
        result[f"effective_rank_at_{t:.2f}"] = rank
    result["total_rank"] = int(S.size)
    return result
