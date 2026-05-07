"""Graph-Hodge hypothesis basis construction for OQCI with multi-state support.

Adapted from E19.2 hypotheses.py. When bundle.n_states > 1, current-space
basis blocks are block-diagonalized across excitation states.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np

from operators import (
    OperatorBundle, empty_current, add_gaussian_sheet_mode,
    add_via_spot, add_return_loop,
)


HYPOTHESES = ["H0_no_via", "H1_via", "H2_model_gap", "H3_return_path"]


@dataclass
class BasisBlock:
    name: str; kind: str; matrix: np.ndarray; prior_variance: float
    is_current_basis: bool
    column_scales: np.ndarray = field(default_factory=lambda: np.zeros(0))
    column_names: list[str] = field(default_factory=list)


@dataclass
class HypothesisBasis:
    hypothesis: str; B: np.ndarray; blocks: list[BasisBlock]
    prior_var_vector: np.ndarray; kept_columns: list[str]
    dropped_columns: list[str]; current_basis: np.ndarray
    current_basis_scales: np.ndarray; column_metadata: list[dict]


def _candidate_centers(n: int) -> list[tuple[int, int]]:
    q1 = n // 3; q2 = (2 * n) // 3; c = n // 2
    return [(c, c), (q1, q1), (q2, q1), (q1, q2), (q2, q2)]


def _gaussian_field_pattern(bundle: OperatorBundle, center, sigma_cells, channel) -> np.ndarray:
    n = int(bundle.index["n"])
    yy, xx = np.mgrid[0:n, 0:n]
    cx, cy = center
    g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sigma_cells ** 2))
    g -= np.mean(g)
    out = np.zeros((3, n, n), dtype=float); out[channel] = g
    return out.reshape(-1)


def _forward_block(bundle: OperatorBundle, block: BasisBlock) -> np.ndarray:
    if block.is_current_basis:
        return bundle.A @ block.matrix
    n_states = max(1, bundle.n_states)
    obs_dim_total = bundle.A.shape[0]

    # Assemble per-state observation block (handles mixed-height stacking)
    def _per_height_stack() -> np.ndarray:
        if bundle.A_per_height is None or obs_dim_total == block.matrix.shape[0]:
            return block.matrix
        parts = []
        for A_h in bundle.A_per_height.values():
            h_rows = A_h.shape[0]
            if h_rows == block.matrix.shape[0]:
                parts.append(block.matrix)
            else:
                parts.append(np.zeros((h_rows, block.matrix.shape[1]), dtype=float))
        if parts:
            return np.concatenate(parts, axis=0)
        return block.matrix

    per_state_obs = _per_height_stack()
    if n_states <= 1 or per_state_obs.shape[0] * n_states == obs_dim_total:
        # Multi-state: tile per-state block
        if n_states > 1:
            return np.tile(per_state_obs, (n_states, 1))
        return per_state_obs
    # Fallback
    return np.tile(per_state_obs, (n_states, 1)) if n_states > 1 else per_state_obs


def _observable_filter(B, names, threshold_ratio):
    norms = np.linalg.norm(B, axis=0)
    if B.shape[1] == 0:
        return B, [], []
    max_norm = float(np.max(norms))
    if max_norm <= 0:
        return B[:, :0], [], names
    keep = norms >= threshold_ratio * max_norm
    kept_names = [n for n, k in zip(names, keep) if k]
    dropped_names = [n for n, k in zip(names, keep) if not k]
    return B[:, keep], kept_names, dropped_names


# ── graph / residual shared blocks ──

def graph_basis(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    n = int(bundle.index["n"])
    cols = []
    for layer in [0, int(bundle.index["layers"]) - 1]:
        for cx, cy in [(n / 2, n / 2), (n / 3, n / 3)]:
            x = empty_current(bundle)
            add_gaussian_sheet_mode(x, bundle, layer, "x", (cx, cy), max(2.0, n / 4.0), 1.0)
            cols.append(x)
            x2 = empty_current(bundle)
            add_gaussian_sheet_mode(x2, bundle, layer, "y", (cx, cy), max(2.0, n / 4.0), 1.0)
            cols.append(x2)
    H = np.stack(cols, axis=1)
    return BasisBlock("graph_smooth_sheet_modes", "graph", H, prior_var, True)


def residual_current_basis(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    n = int(bundle.index["n"])
    cols = []
    for layer in [0, int(bundle.index["layers"]) - 1]:
        for comp in ["x", "y"]:
            x = empty_current(bundle)
            add_gaussian_sheet_mode(x, bundle, layer, comp, (n / 2, n / 2), max(1.0, n / 8.0), 1.0)
            cols.append(x)
    H = np.stack(cols, axis=1)
    return BasisBlock("small_residual_current_modes", "residual", H, prior_var, True)


# ── H2_model_gap blocks ──

def registration_derivative_basis(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    n = int(bundle.index["n"])
    centers = [(n / 2, n / 2), (n / 3, n / 3), (2 * n / 3, 2 * n / 3)]
    sigma = max(1.5, n / 6.0)
    cols = []
    for center in centers:
        pat = _gaussian_field_pattern(bundle, center, sigma, 0).reshape(3, n, n)
        dg_dx = np.gradient(pat[0], axis=1); dg_dy = np.gradient(pat[0], axis=0)
        out = np.zeros((3, n, n), dtype=float); out[0] = dg_dx; out[1] = dg_dy
        cols.append(out.reshape(-1))
        out2 = np.zeros((3, n, n), dtype=float); out2[2] = 0.5 * (dg_dx - dg_dy)
        cols.append(out2.reshape(-1))
    U = np.stack(cols, axis=1)
    return BasisBlock("registration_derivative_basis", "gap_registration", U, prior_var, False)


def standoff_laplacian_basis(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    n = int(bundle.index["n"])
    centers = [(n / 2, n / 2), (n / 3, n / 3), (2 * n / 3, 2 * n / 3)]
    sigma = max(1.5, n / 6.0)
    cols = []
    for center in centers:
        for channel in [0, 1, 2]:
            pat = _gaussian_field_pattern(bundle, center, sigma, channel).reshape(3, n, n)
            dg_dx = np.gradient(pat[channel], axis=1); d2g = np.gradient(dg_dx, axis=1)
            dg_dy = np.gradient(pat[channel], axis=0); d2g2 = np.gradient(dg_dy, axis=0)
            lap = d2g + d2g2
            out = np.zeros((3, n, n), dtype=float); out[channel] = lap
            cols.append(out.reshape(-1))
    for center in centers:
        pat1 = _gaussian_field_pattern(bundle, center, sigma, 0)
        pat2 = _gaussian_field_pattern(bundle, center, 2.0 * sigma, 0)
        cols.append(pat2 - pat1)
    U = np.stack(cols, axis=1)
    return BasisBlock("standoff_laplacian_basis", "gap_standoff", U, prior_var, False)


def low_order_drift_basis(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    n = int(bundle.index["n"])
    cols = []
    for channel in [0, 1, 2]:
        out = np.zeros((3, n, n), dtype=float); out[channel] = 1.0
        cols.append(out.reshape(-1))
    for channel in [0, 1, 2]:
        ramp = np.linspace(-1.0, 1.0, n)
        out_a = np.zeros((3, n, n), dtype=float); out_a[channel] = np.tile(ramp[None, :], (n, 1))
        out_b = np.zeros((3, n, n), dtype=float); out_b[channel] = np.tile(ramp[:, None], (1, n))
        cols.append(out_a.reshape(-1)); cols.append(out_b.reshape(-1))
    U = np.stack(cols, axis=1)
    return BasisBlock("low_order_drift_basis", "gap_drift", U, prior_var, False)


# ── H1_via blocks ──

def via_vertical_modes(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    n = int(bundle.index["n"])
    cols = []
    for layer in range(int(bundle.index["layers"]) - 1):
        for center in _candidate_centers(n):
            x = empty_current(bundle)
            add_via_spot(x, bundle, layer, layer + 1, center, 1.0, radius=0)
            cols.append(x)
    H = np.stack(cols, axis=1)
    return BasisBlock("via_vertical_modes", "via_vertical", H, prior_var, True)


def via_sheet_compensation_modes(bundle: OperatorBundle, prior_var: float) -> BasisBlock:
    n = int(bundle.index["n"])
    cols = []
    for layer in range(int(bundle.index["layers"]) - 1):
        for center in _candidate_centers(n):
            x = empty_current(bundle)
            add_gaussian_sheet_mode(x, bundle, layer, "x", center, max(1.5, n / 7.0), 0.25)
            add_gaussian_sheet_mode(x, bundle, layer + 1, "x", center, max(1.5, n / 7.0), -0.25)
            cols.append(x)
    H = np.stack(cols, axis=1)
    return BasisBlock("via_sheet_compensation_modes", "via_compensation", H, prior_var, True)


# ── H3_return_path blocks ──

def _return_loop_pattern(bundle, layer, amplitude, cx, cy):
    n = int(bundle.index["n"]); margin = max(1, n // 6)
    jx = np.zeros((n, n), dtype=float); jy = np.zeros((n, n), dtype=float)
    i_cx, i_cy = int(cx * n), int(cy * n)
    l, r = max(0, i_cx - margin), min(n, i_cx + margin)
    t, b = max(0, i_cy - margin), min(n, i_cy + margin)
    if t < n and l < r: jx[t, l:r] += amplitude
    if b < n and l < r: jx[b, l:r] -= amplitude
    if 0 < r and t < b: jy[t:b, l] -= amplitude
    if r < n and t < b: jy[t:b, r] += amplitude
    x = empty_current(bundle)
    x[bundle.index["sheet_slices"][(layer, "x")]] += jx.ravel()
    x[bundle.index["sheet_slices"][(layer, "y")]] += jy.ravel()
    return x


def multi_position_return_loops(bundle, prior_var):
    bottom_layers = [int(bundle.index["layers"]) - 1, max(0, int(bundle.index["layers"]) - 2)]
    positions = [(0.5, 0.5), (0.25, 0.5), (0.75, 0.5), (0.5, 0.25), (0.5, 0.75)]
    cols = []
    for layer in bottom_layers:
        for cx, cy in positions:
            cols.append(_return_loop_pattern(bundle, layer, 1.0, cx, cy))
    H = np.stack(cols, axis=1)
    return BasisBlock("multi_position_return_loops", "return_loop", H, prior_var, True)


def edge_return_modes(bundle, prior_var):
    n = int(bundle.index["n"]); layer = int(bundle.index["layers"]) - 1
    margin = max(1, n // 6); cols = []
    for sign in [1.0, -1.0]:
        for (i_sl, j_sl), comp in [((slice(0, margin), slice(None)), "x"),
                                     ((slice(n - margin, n), slice(None)), "x"),
                                     ((slice(None), slice(0, margin)), "y"),
                                     ((slice(None), slice(n - margin, n)), "y")]:
            arr = np.zeros((n, n), dtype=float)
            arr[i_sl, j_sl] = sign
            x = empty_current(bundle)
            x[bundle.index["sheet_slices"][(layer, comp)]] += arr.ravel()
            cols.append(x)
    H = np.stack(cols, axis=1)
    return BasisBlock("edge_return_modes", "return_edge", H, prior_var, True)


def distributed_return_modes(bundle, prior_var):
    n = int(bundle.index["n"]); layer = int(bundle.index["layers"]) - 1
    x1 = empty_current(bundle)
    add_gaussian_sheet_mode(x1, bundle, layer, "x", (n / 2, n / 2), max(2.0, n / 4.0), 1.0)
    x2 = empty_current(bundle)
    add_gaussian_sheet_mode(x2, bundle, layer, "y", (n / 2, n / 2), max(2.0, n / 4.0), 1.0)
    H = np.stack([x1, x2, _return_loop_pattern(bundle, layer, 1.0, 0.5, 0.5),
                   _return_loop_pattern(bundle, layer, -1.0, 0.5, 0.5)], axis=1)
    return BasisBlock("distributed_return_modes", "return_edge", H, prior_var, True)


# ── build ──

def _block_diagonalize_current_block(block: BasisBlock, n_states: int, curr_dim_per_state: int) -> BasisBlock:
    """Create block-diagonal version for multi-state bundles."""
    if n_states <= 1 or not block.is_current_basis or block.matrix.shape[0] != curr_dim_per_state:
        return block
    k = block.matrix.shape[1]
    blocks_rows = []
    for s in range(n_states):
        row_parts = []
        for t in range(n_states):
            if s == t:
                row_parts.append(block.matrix)
            else:
                row_parts.append(np.zeros((curr_dim_per_state, k)))
        blocks_rows.append(np.concatenate(row_parts, axis=1))
    H_bd = np.concatenate(blocks_rows, axis=0)
    return BasisBlock(block.name + f"_ms{n_states}", block.kind, H_bd, block.prior_variance, True)


def build_hypothesis_basis(bundle: OperatorBundle, cfg: dict, hypothesis: str) -> HypothesisBasis:
    if hypothesis not in HYPOTHESES:
        raise ValueError(f"Unknown hypothesis: {hypothesis}")
    pv = cfg["prior_variance"]; threshold_ratio = float(cfg["observable_energy_ratio_threshold"])
    n_states = max(1, bundle.n_states)
    curr_dim_per_state = bundle.A.shape[1] // n_states if n_states > 1 else bundle.A.shape[1]

    all_blocks: list[BasisBlock] = [
        graph_basis(bundle, float(pv["graph"])),
        residual_current_basis(bundle, float(pv["residual"])),
    ]

    if hypothesis == "H1_via":
        all_blocks.append(via_vertical_modes(bundle, float(pv.get("via_vertical", 1.20))))
        all_blocks.append(via_sheet_compensation_modes(bundle, float(pv.get("via_compensation", 0.25))))
    elif hypothesis == "H2_model_gap":
        all_blocks.append(registration_derivative_basis(bundle, float(pv.get("gap_registration", 1.00))))
        all_blocks.append(standoff_laplacian_basis(bundle, float(pv.get("gap_standoff", 1.00))))
        all_blocks.append(low_order_drift_basis(bundle, float(pv.get("gap_drift", 0.40))))
    elif hypothesis == "H3_return_path":
        all_blocks.append(multi_position_return_loops(bundle, float(pv.get("return_loop", 1.20))))
        all_blocks.append(edge_return_modes(bundle, float(pv.get("return_edge", 0.60))))
        all_blocks.append(distributed_return_modes(bundle, float(pv.get("return_edge", 0.60))))

    # Block-diagonalize current-space blocks for multi-state
    if n_states > 1:
        all_blocks = [_block_diagonalize_current_block(b, n_states, curr_dim_per_state) for b in all_blocks]

    B_parts, kept, dropped = [], [], []
    current_parts, current_scales_list = [], []
    prior_var_list, metadata = [], []

    for block in all_blocks:
        raw_obs = _forward_block(bundle, block)
        obs_norms = np.linalg.norm(raw_obs, axis=0)
        eps_norm = np.maximum(obs_norms, 1e-30)
        block.column_scales = obs_norms
        block.column_names = [f"{block.kind}:{block.name}:{i}" for i in range(block.matrix.shape[1])]

        raw_obs_norm = raw_obs / eps_norm[None, :]
        B_keep_normed, kept_names, dropped_names = _observable_filter(raw_obs_norm, block.column_names, threshold_ratio)

        if not kept_names:
            dropped.extend(block.column_names)
            continue

        kept_indices = [i for i, n in enumerate(block.column_names) if n in kept_names]
        scales_j = np.sqrt(float(block.prior_variance)) / eps_norm[kept_indices]
        B_scaled = raw_obs[:, kept_indices] * scales_j[None, :]

        B_parts.append(B_scaled); kept.extend(kept_names); dropped.extend(dropped_names)

        for idx_j, i in enumerate(kept_indices):
            metadata.append({"block_name": block.name, "block_kind": block.kind,
                             "prior_var": block.prior_variance,
                             "original_norm": float(obs_norms[i]),
                             "scale_factor": float(scales_j[idx_j])})
            prior_var_list.append(1.0)

        if block.is_current_basis:
            curr_kept = block.matrix[:, kept_indices] * scales_j[None, :] if kept_indices else np.zeros((block.matrix.shape[0], 0))
            current_parts.append(curr_kept)
            current_scales_list.append(obs_norms[kept_indices] * scales_j if kept_indices else np.zeros(0))

    B = np.concatenate(B_parts, axis=1) if B_parts else np.zeros((bundle.A.shape[0], 0))
    current_basis = np.concatenate(current_parts, axis=1) if current_parts else np.zeros((bundle.A.shape[1], 0))
    current_basis_scales = np.concatenate(current_scales_list) if current_scales_list else np.zeros(0)
    prior_var_vector = np.array(prior_var_list, dtype=float) if prior_var_list else np.zeros(0)

    return HypothesisBasis(
        hypothesis=hypothesis, B=B, blocks=all_blocks,
        prior_var_vector=prior_var_vector, kept_columns=kept,
        dropped_columns=dropped, current_basis=current_basis,
        current_basis_scales=current_basis_scales, column_metadata=metadata,
    )


def build_all_hypothesis_bases(bundle: OperatorBundle, cfg: dict) -> dict[str, HypothesisBasis]:
    return {h: build_hypothesis_basis(bundle, cfg, h) for h in HYPOTHESES}


def subspace_principal_angle_deg(A, B, eps=1e-12):
    if A.size == 0 or B.size == 0 or A.shape[1] == 0 or B.shape[1] == 0:
        return 90.0
    qa, _ = np.linalg.qr(A); qb, _ = np.linalg.qr(B)
    s = np.linalg.svd(qa.T @ qb, compute_uv=False)
    if s.size == 0: return 90.0
    c = float(np.clip(np.max(s), -1.0, 1.0))
    return float(np.degrees(np.arccos(c + 0.0)))


# ── gap model reference patterns ──

def registration_pattern(n, center, sigma_cells, amplitude):
    yy, xx = np.mgrid[0:n, 0:n]; cx, cy = center
    g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sigma_cells ** 2))
    gx = np.gradient(g, axis=1); gy = np.gradient(g, axis=0)
    out = np.zeros((3, n, n), dtype=float)
    out[0] = amplitude * gx; out[1] = amplitude * gy
    out[2] = 0.5 * amplitude * (gx - gy)
    out -= np.mean(out, axis=(1, 2), keepdims=True)
    return out.reshape(-1)


def standoff_laplacian_pattern(clean_field, amplitude):
    n = int(round(np.sqrt(clean_field.size / 3)))
    f = clean_field.reshape(3, n, n); lap = np.zeros_like(f)
    for c in range(3):
        arr = f[c]
        lap[c] = (-4.0 * arr + np.roll(arr, 1, axis=0) + np.roll(arr, -1, axis=0) +
                  np.roll(arr, 1, axis=1) + np.roll(arr, -1, axis=1))
    norm = float(np.linalg.norm(lap.ravel()))
    if norm > 0: lap = lap / norm
    return amplitude * lap.reshape(-1)
