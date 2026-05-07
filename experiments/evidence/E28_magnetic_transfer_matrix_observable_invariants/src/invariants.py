"""Nuisance-invariant representations of the magnetic transfer matrix.

Provides three invariant families:
1. Column-space projector: P_h = Q_h Q_h^T (invariant to invertible mixing)
2. Whitened Gram matrix: G_bar_h (cancels per-state amplitude scale)
3. Differential common-mode cancellation: Delta y

Also computes invariant distances and principal angle spectra.
"""

from __future__ import annotations

import numpy as np

EPS = 1e-14


# ── 1. Column-space projector ──────────────────────────────────────────────

def column_space_projector(T: np.ndarray) -> np.ndarray:
    """Orthogonal projector onto the column space of T.

    P = Q Q^T, where Q = orth(T).

    Returns projector matrix (M_obs x M_obs) and Q basis.
    """
    if T.size == 0 or T.shape[1] == 0:
        M = T.shape[0] if T.size > 0 else 0
        return np.zeros((M, M), dtype=float), np.zeros((M, 0), dtype=float)

    Q, _ = np.linalg.qr(T)
    r = int(np.linalg.matrix_rank(T))
    Q = Q[:, :r]
    P = Q @ Q.T
    return P, Q


def projector_distance(T1: np.ndarray, T2: np.ndarray) -> float:
    """Distance between column-space projectors: ||P1 - P2||_F / sqrt(2).

    Range: [0, 1]. Invariant to invertible mixing of columns.
    """
    P1, _ = column_space_projector(T1)
    P2, _ = column_space_projector(T2)
    if P1.size == 0 or P2.size == 0:
        return 0.0
    return float(np.linalg.norm(P1 - P2, "fro") / np.sqrt(2.0))


def principal_angle_spectrum(T1: np.ndarray, T2: np.ndarray) -> dict:
    """Compute principal angles between column spaces of T1 and T2."""
    if T1.size == 0 or T2.size == 0 or T1.shape[1] == 0 or T2.shape[1] == 0:
        return {"angles_deg": [], "min_angle_deg": 90.0, "max_angle_deg": 90.0, "n_angles": 0}

    Q1, _ = np.linalg.qr(T1)
    Q2, _ = np.linalg.qr(T2)
    s = np.linalg.svd(Q1.T @ Q2, compute_uv=False)
    s_clipped = np.clip(s, 0.0, 1.0)
    angles = np.degrees(np.arccos(s_clipped))
    return {
        "angles_deg": angles.tolist(),
        "min_angle_deg": float(np.min(angles)) if len(angles) > 0 else 90.0,
        "max_angle_deg": float(np.max(angles)) if len(angles) > 0 else 90.0,
        "n_angles": len(angles),
    }


# ── 2. Whitened Gram matrix ────────────────────────────────────────────────

def whitened_gram(T: np.ndarray) -> np.ndarray:
    """Compute whitened (correlation) Gram matrix.

    G = T^T @ T
    G_bar = diag(G)^{-1/2} @ G @ diag(G)^{-1/2}

    This cancels per-state amplitude scale variations.
    """
    if T.size == 0 or T.shape[1] == 0:
        S = T.shape[1] if T.size > 0 else 0
        return np.zeros((S, S), dtype=float)

    G = T.T @ T
    d = np.diag(G)
    d_inv_sqrt = np.where(d > EPS, 1.0 / np.sqrt(d), 0.0)
    D_inv_sqrt = np.diag(d_inv_sqrt)
    G_bar = D_inv_sqrt @ G @ D_inv_sqrt
    return G_bar


def gram_distance(T1: np.ndarray, T2: np.ndarray) -> float:
    """Distance between whitened Gram matrices: ||G_bar1 - G_bar2||_F."""
    G1 = whitened_gram(T1)
    G2 = whitened_gram(T2)
    if G1.size == 0 or G2.size == 0:
        return 0.0
    return float(np.linalg.norm(G1 - G2, "fro"))


# ── 3. Differential common-mode cancellation ───────────────────────────────

def differential_matrix(T: np.ndarray, ref_col: int = 0) -> np.ndarray:
    """Subtract reference column for common-mode cancellation.

    Delta_T[:, s] = T[:, s] - T[:, ref_col]
    """
    if T.size == 0 or T.shape[1] <= 1:
        return T.copy() if T.size > 0 else np.zeros((0, 0))
    ref = T[:, ref_col:ref_col + 1]
    return T - ref


def pairwise_differential_matrix(T: np.ndarray) -> np.ndarray:
    """All pairwise differential columns: T[:, a] - T[:, b] for a < b."""
    if T.size == 0 or T.shape[1] <= 1:
        return T
    M, S = T.shape
    n_pairs = S * (S - 1) // 2
    result = np.zeros((M, n_pairs), dtype=float)
    idx = 0
    for a in range(S):
        for b in range(a + 1, S):
            result[:, idx] = T[:, a] - T[:, b]
            idx += 1
    return result


def raw_stacked_field(T: np.ndarray) -> np.ndarray:
    """Raw stacked field (for comparison): just flatten T."""
    return T.ravel().reshape(-1, 1) if T.ndim == 2 else T.ravel()


# ── 4. Invariant computation for all hypotheses ────────────────────────────

def compute_all_invariants(
    T_matrices: dict[str, np.ndarray],
) -> dict:
    """Compute all invariant representations for each hypothesis."""
    projectors = {}
    grams = {}
    diffs = {}

    for h, T in T_matrices.items():
        P, Q = column_space_projector(T)
        projectors[h] = {"P": P, "Q": Q}
        grams[h] = {"G_bar": whitened_gram(T)}
        diffs[h] = {"delta": differential_matrix(T), "delta_pairwise": pairwise_differential_matrix(T)}

    return {
        "projectors": projectors,
        "grams": grams,
        "differentials": diffs,
    }


def invariant_sanity_checks(
    T_matrices: dict[str, np.ndarray],
    invariants: dict,
) -> dict:
    """Run sanity checks on invariant computations."""
    checks = {}

    # Projector: check P^2 = P (idempotent) and P^T = P (symmetric)
    for h, proj_data in invariants["projectors"].items():
        P = proj_data["P"]
        if P.size > 0:
            idempotent = float(np.linalg.norm(P @ P - P, "fro"))
            symmetric = float(np.linalg.norm(P - P.T, "fro"))
            checks[f"projector_{h}_idempotent"] = idempotent < 1e-8
            checks[f"projector_{h}_symmetric"] = symmetric < 1e-8
        else:
            checks[f"projector_{h}_idempotent"] = True
            checks[f"projector_{h}_symmetric"] = True

    # Gram: check diagonal = 1 (whitened)
    for h, gram_data in invariants["grams"].items():
        G = gram_data["G_bar"]
        if G.size > 0 and G.shape[0] > 0:
            diag_ok = float(np.max(np.abs(np.diag(G) - 1.0))) < 1e-8
            checks[f"gram_{h}_whitened"] = diag_ok
        else:
            checks[f"gram_{h}_whitened"] = True

    # Differential: check ref column is zero
    for h, diff_data in invariants["differentials"].items():
        delta = diff_data["delta"]
        if delta.size > 0 and delta.shape[1] > 0:
            ref_norm = float(np.linalg.norm(delta[:, 0]))
            checks[f"differential_{h}_ref_zero"] = ref_norm < 1e-10
        else:
            checks[f"differential_{h}_ref_zero"] = True

    return checks
