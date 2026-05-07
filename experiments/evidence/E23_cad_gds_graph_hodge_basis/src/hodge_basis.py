"""Graph-Hodge basis construction for E23 round 3.

Uses SVD nullspace projection instead of pseudoinverse.
Reports nullspace_dim, retained_energy, collapsed_count.
"""
from __future__ import annotations

from typing import Any

import numpy as np


def build_port_basis(
    D: np.ndarray, q: np.ndarray, tol: float = 1e-8
) -> np.ndarray:
    i_port, residuals, rank, sv = np.linalg.lstsq(D, q, rcond=tol)
    residual = np.max(np.abs(D @ i_port - q))
    if residual > tol * 100:
        D_pinv = np.linalg.pinv(D, rcond=tol)
        i_port = D_pinv @ q
    return i_port.reshape(-1, 1)


def build_loop_basis(D: np.ndarray, tol: float = 1e-8) -> np.ndarray:
    U, s, Vt = np.linalg.svd(D, full_matrices=True)
    null_mask = s < tol * max(D.shape) * s[0] if s[0] > 0 else np.ones(len(s), dtype=bool)
    rank = int(np.sum(~null_mask))
    null_dim = D.shape[1] - rank
    if null_dim <= 0:
        return np.zeros((D.shape[1], 0))
    V_full = Vt.T
    return V_full[:, rank:]


def _interior_mask(D: np.ndarray, q: np.ndarray, tol: float = 1e-8) -> np.ndarray:
    return np.abs(q) < tol


def build_svd_nullspace(
    D: np.ndarray,
    interior_mask: np.ndarray,
    tol: float = 1e-8,
) -> tuple[np.ndarray, int, np.ndarray]:
    """Compute explicit SVD nullspace basis N for D_interior.

    D_interior @ N = 0 by construction.

    Returns (N, nullspace_dim, singular_values).
    """
    D_int = D[interior_mask, :]
    if D_int.shape[0] == 0 or D_int.shape[1] == 0:
        return np.eye(D.shape[1]), D.shape[1], np.ones(D.shape[1])

    U, s, Vt = np.linalg.svd(D_int, full_matrices=True)
    s_max = s[0] if s[0] > 0 else 1.0
    null_mask = s < tol * max(D_int.shape) * s_max
    rank = int(np.sum(~null_mask))
    null_dim = D_int.shape[1] - rank

    if null_dim <= 0:
        return np.zeros((D_int.shape[1], 0)), 0, s

    V_full = Vt.T  # (m, m)
    N = V_full[:, rank:]  # (m, null_dim)
    return N, null_dim, s


def project_via_modes_svd(
    H_via_raw: np.ndarray,
    N: np.ndarray,
    nullspace_dim: int,
) -> tuple[np.ndarray, list[float], list[float], int]:
    """Project raw via modes onto SVD nullspace N.

    v_proj = N @ (N^T @ v)

    Returns (H_via_proj, residuals, retained_energies, collapsed_count).
    """
    if H_via_raw.shape[1] == 0 or nullspace_dim == 0:
        return H_via_raw.copy(), [], [], 0

    m, n_modes = H_via_raw.shape
    H_proj = np.zeros((m, n_modes))
    residuals = []
    retained_energies = []
    collapsed = 0

    for k in range(n_modes):
        v_raw = H_via_raw[:, k].copy()
        v_norm = np.linalg.norm(v_raw)
        if v_norm < 1e-15:
            H_proj[:, k] = v_raw
            residuals.append(0.0)
            retained_energies.append(1.0)
            continue

        # SVD projection: v_proj = N @ (N^T @ v)
        coeffs = N.T @ v_raw
        v_proj = N @ coeffs

        proj_norm = np.linalg.norm(v_proj)
        retained = float((proj_norm / v_norm) ** 2)
        res = float(np.linalg.norm(v_proj - v_raw) / v_norm)

        H_proj[:, k] = v_proj
        residuals.append(res)
        retained_energies.append(retained)

        if proj_norm < 1e-10 * v_norm:
            collapsed += 1

    return H_proj, residuals, retained_energies, collapsed


def project_return_modes_svd(
    H_return_raw: np.ndarray,
    N: np.ndarray,
    nullspace_dim: int,
) -> tuple[np.ndarray, list[float], list[float], int]:
    """Project raw return modes onto SVD nullspace N."""
    if H_return_raw.shape[1] == 0 or nullspace_dim == 0:
        return H_return_raw.copy(), [], [], 0

    m, n_modes = H_return_raw.shape
    H_proj = np.zeros((m, n_modes))
    residuals = []
    retained_energies = []
    collapsed = 0

    for k in range(n_modes):
        v_raw = H_return_raw[:, k].copy()
        v_norm = np.linalg.norm(v_raw)
        if v_norm < 1e-15:
            H_proj[:, k] = v_raw
            residuals.append(0.0)
            retained_energies.append(1.0)
            continue

        coeffs = N.T @ v_raw
        v_proj = N @ coeffs
        proj_norm = np.linalg.norm(v_proj)
        retained = float((proj_norm / v_norm) ** 2)
        res = float(np.linalg.norm(v_proj - v_raw) / v_norm)

        H_proj[:, k] = v_proj
        residuals.append(res)
        retained_energies.append(retained)

        if proj_norm < 1e-10 * v_norm:
            collapsed += 1

    return H_proj, residuals, retained_energies, collapsed


def _build_raw_edge_basis(
    graph: dict[str, Any],
    edge_order: list[str],
    edge_kind: str,
    D: np.ndarray,
    existing_basis: np.ndarray | None = None,
) -> np.ndarray:
    indices = []
    for j, eid in enumerate(edge_order):
        if graph["edges"][eid]["kind"] == edge_kind:
            indices.append(j)
    if not indices:
        return np.zeros((D.shape[1], 0))
    m = D.shape[1]
    H = np.zeros((m, len(indices)))
    for k, j in enumerate(indices):
        H[j, k] = 1.0
    return _orthogonalize(H, existing_basis)


def build_via_basis(
    graph: dict[str, Any],
    edge_order: list[str],
    D: np.ndarray,
    existing_basis: np.ndarray | None = None,
) -> np.ndarray:
    return _build_raw_edge_basis(graph, edge_order, "via_edge", D, existing_basis)


def build_return_basis(
    graph: dict[str, Any],
    edge_order: list[str],
    D: np.ndarray,
    existing_basis: np.ndarray | None = None,
) -> np.ndarray:
    return _build_raw_edge_basis(graph, edge_order, "return_candidate", D, existing_basis)


def build_residual_basis(m: int, n_modes: int = 3, seed: int = 20260506) -> np.ndarray:
    if n_modes <= 0:
        return np.zeros((m, 0))
    rng = np.random.RandomState(seed)
    H_res = np.zeros((m, n_modes))
    for k in range(n_modes):
        phase = 2 * np.pi * k / n_modes
        for j in range(m):
            H_res[j, k] = np.sin(phase + 2 * np.pi * j / m)
    for k in range(n_modes):
        norm = np.linalg.norm(H_res[:, k])
        if norm > 1e-15:
            H_res[:, k] /= norm
    return H_res


def build_harmonic_basis(*args, **kwargs) -> np.ndarray:
    return np.zeros((kwargs.get("D", np.zeros((1, 1))).shape[1], 0))


def build_gap_basis(
    m: int,
    existing_basis: np.ndarray | None = None,
    n_modes: int = 2,
    seed: int = 20260506,
) -> np.ndarray:
    if n_modes <= 0:
        return np.zeros((m, 0))
    rng = np.random.RandomState(seed + 1)
    H_gap = np.zeros((m, n_modes))
    for k in range(n_modes):
        for j in range(m):
            H_gap[j, k] = np.cos(2 * np.pi * (j + 0.5) * (k + 1) / m)
        norm = np.linalg.norm(H_gap[:, k])
        if norm > 1e-15:
            H_gap[:, k] /= norm
    return _orthogonalize(H_gap, existing_basis)


def _orthogonalize(
    H_new: np.ndarray, existing: np.ndarray | None
) -> np.ndarray:
    if H_new.shape[1] == 0:
        return H_new
    if existing is not None and existing.shape[1] > 0:
        for k in range(H_new.shape[1]):
            for j in range(existing.shape[1]):
                if np.linalg.norm(existing[:, j]) > 1e-15:
                    proj = np.dot(H_new[:, k], existing[:, j]) / np.dot(existing[:, j], existing[:, j])
                    H_new[:, k] -= proj * existing[:, j]
    Q, R = np.linalg.qr(H_new) if H_new.shape[1] > 0 else (H_new, None)
    if Q.shape[1] > 0:
        norms = np.abs(np.diag(R)) if R is not None else np.ones(Q.shape[1])
        keep = norms > 1e-10 * np.max(norms) if np.max(norms) > 0 else np.ones(Q.shape[1], dtype=bool)
        return Q[:, keep]
    return Q


def _existing_from_blocks(blocks: list[np.ndarray]) -> np.ndarray | None:
    non_empty = [b for b in blocks if b.shape[1] > 0]
    if not non_empty:
        return None
    return np.hstack(non_empty)


def assemble_hodge_basis(
    graph: dict[str, Any],
    edge_order: list[str],
    D: np.ndarray,
    q: np.ndarray,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Assemble Graph-Hodge basis with SVD nullspace projected blocks."""
    tol = config.get("basis_rank_tolerance", 1e-8)
    m = D.shape[1]
    interior = _interior_mask(D, q, tol)

    # SVD nullspace for D_interior
    N, nullspace_dim, svd_s = build_svd_nullspace(D, interior, tol)

    # 1. Port basis
    H_port = build_port_basis(D, q, tol)

    # 2. Loop basis (nullspace of full D)
    H_loop = build_loop_basis(D, tol)

    # 3. Raw via basis
    existing = _existing_from_blocks([H_port, H_loop])
    H_via_raw = build_via_basis(graph, edge_order, D, existing)

    # 4. SVD-projected via basis
    H_via_proj, via_res, via_energy, via_collapsed = project_via_modes_svd(
        H_via_raw, N, nullspace_dim
    )

    # 5. Raw return basis
    existing = _existing_from_blocks([H_port, H_loop, H_via_raw])
    H_return_raw = build_return_basis(graph, edge_order, D, existing)

    # 6. SVD-projected return basis
    H_return_proj, return_res, return_energy, return_collapsed = project_return_modes_svd(
        H_return_raw, N, nullspace_dim
    )

    # 7. Harmonic basis
    existing = _existing_from_blocks([H_port, H_loop, H_via_proj, H_return_proj])
    H_harmonic = np.zeros((m, 0))

    # 8. Gap basis
    existing = _existing_from_blocks([H_port, H_loop, H_via_proj, H_return_proj, H_harmonic])
    existing_dim = existing.shape[1] if existing is not None else 0
    remaining = max(0, m - existing_dim)
    n_gap = min(2, max(0, remaining - 1))
    H_gap = build_gap_basis(m, existing, n_modes=n_gap)

    # 9. Residual basis
    existing = _existing_from_blocks([H_port, H_loop, H_via_proj, H_return_proj, H_harmonic, H_gap])
    existing_dim = existing.shape[1] if existing is not None else 0
    remaining = max(0, m - existing_dim)
    n_res = min(2, remaining)
    H_residual = build_residual_basis(m, n_modes=n_res)

    # Assemble full basis
    projected_blocks_list = [H_port, H_loop, H_via_proj, H_return_proj, H_harmonic, H_gap, H_residual]
    H_full = np.hstack([b for b in projected_blocks_list if b.shape[1] > 0])

    # Compute basis rank
    if H_full.shape[1] > 0:
        U, s, Vt = np.linalg.svd(H_full, full_matrices=False)
        basis_rank = int(np.sum(s > tol * s[0])) if s[0] > 0 else 0
        basis_rank = min(basis_rank, m)
        H_full = U[:, :basis_rank]
    else:
        s = np.array([])
        basis_rank = 0

    return {
        "blocks": {
            "port": H_port,
            "loop": H_loop,
            "via_raw": H_via_raw,
            "via": H_via_proj,
            "return_raw": H_return_raw,
            "return": H_return_proj,
            "harmonic": H_harmonic,
            "gap": H_gap,
            "residual": H_residual,
        },
        "block_dims": {
            "port": H_port.shape[1],
            "loop": H_loop.shape[1],
            "via": H_via_proj.shape[1],
            "return": H_return_proj.shape[1],
            "harmonic": H_harmonic.shape[1],
            "gap": H_gap.shape[1],
            "residual": H_residual.shape[1],
        },
        "raw_block_dims": {
            "via": H_via_raw.shape[1],
            "return": H_return_raw.shape[1],
        },
        "svd_nullspace": {
            "nullspace_dim": nullspace_dim,
            "projection_method": "SVD",
            "via_residuals": via_res,
            "via_retained_energy": via_energy,
            "via_collapsed_count": via_collapsed,
            "return_residuals": return_res,
            "return_retained_energy": return_energy,
            "return_collapsed_count": return_collapsed,
        },
        "projection_residuals": {
            "via": via_res,
            "return": return_res,
        },
        "projection_collapsed": {
            "via": [e < 1e-10 for e in via_energy],
            "return": [e < 1e-10 for e in return_energy],
        },
        "total_dim": basis_rank,
        "basis_matrix": H_full,
        "singular_values": s,
        "basis_rank": basis_rank,
        "edge_order": edge_order,
    }


def validate_basis(
    hodge_result: dict[str, Any],
    D: np.ndarray,
    q: np.ndarray,
    graph: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    """Validate Hodge basis with honest per-block KCL + SVD-specific metrics."""
    tol = config.get("kcl_residual_threshold", 1e-10)
    closure_tol = config.get("current_closure_threshold", 1e-10)

    interior = _interior_mask(D, q, tol)
    D_int = D[interior, :]

    per_block_kcl = {}
    per_block_closure = {}

    for name, block in hodge_result["blocks"].items():
        if block.shape[1] == 0:
            per_block_kcl[name] = 0.0
            per_block_closure[name] = 0.0
            continue
        residuals = []
        closures = []
        for k in range(block.shape[1]):
            i = block[:, k]
            if name == "port":
                r = float(np.max(np.abs(D @ i - q)))
            elif name in ("via", "return"):
                # SVD projected blocks: check KCL on interior nodes only
                # (port node rows can have non-zero D@i since current
                #  enters/exits through ports)
                r = float(np.max(np.abs(D_int @ i)))
            else:
                r = float(np.max(np.abs(D @ i)))
            residuals.append(r)
            if name == "port":
                c = abs(float(np.sum(D @ i) - np.sum(q)))
            else:
                c = abs(float(np.sum(D @ i)))
            closures.append(c)
        per_block_kcl[name] = float(np.max(residuals)) if residuals else 0.0
        per_block_closure[name] = float(np.max(closures)) if closures else 0.0

    port_loop_kcl = max(
        per_block_kcl.get("port", 0.0),
        per_block_kcl.get("loop", 0.0),
    )

    raw_block_names = ["via_raw", "return_raw", "gap", "residual"]
    raw_blocks_kcl = max(
        (per_block_kcl.get(n, 0.0) for n in raw_block_names),
        default=0.0,
    )

    projected_block_names = ["via", "return"]
    projected_blocks_kcl = max(
        (per_block_kcl.get(n, 0.0) for n in projected_block_names),
        default=0.0,
    )

    max_closure = max(per_block_closure.values()) if per_block_closure else 0.0

    svd_info = hodge_result.get("svd_nullspace", {})
    nullspace_dim = svd_info.get("nullspace_dim", 0)
    via_collapsed = svd_info.get("via_collapsed_count", 0)
    return_collapsed = svd_info.get("return_collapsed_count", 0)

    return {
        "kcl_residual_port_loop": port_loop_kcl,
        "kcl_residual_raw_blocks": raw_blocks_kcl,
        "kcl_residual_svd_projected_blocks": projected_blocks_kcl,
        "max_closure_error": max_closure,
        "port_loop_kcl_pass": port_loop_kcl < tol,
        "svd_projected_blocks_kcl_pass": projected_blocks_kcl < tol,
        "closure_pass": max_closure < closure_tol,
        "per_block_kcl": per_block_kcl,
        "per_block_closure": per_block_closure,
        "svd_nullspace_dim": nullspace_dim,
        "svd_via_collapsed_count": via_collapsed,
        "svd_return_collapsed_count": return_collapsed,
    }
