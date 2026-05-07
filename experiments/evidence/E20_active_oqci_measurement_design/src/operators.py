"""Forward operators for E20 OQCI with multi-height, component masking, and multi-state.

Adapted from E19.2 operators.py. Supports:
- multi-height stacking
- component masking per height
- block-diagonal multi-state operators for excitation-state perturbation
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from config import component_mask


MU0_OVER_4PI = 1e-7
EPS = 1e-18


@dataclass(frozen=True)
class OperatorBundle:
    A: np.ndarray
    positions: np.ndarray
    obs_positions: np.ndarray
    index: dict[str, object]
    column_norms: np.ndarray
    channel_count: int = 3
    heights: tuple[float, ...] | None = None
    A_per_height: dict[str, np.ndarray] | None = None
    per_height_components: dict[str, list[str]] | None = None
    n_states: int = 1


def _grid_positions(n: int, pitch_um: float) -> np.ndarray:
    coords = (np.arange(n, dtype=float) - (n - 1) / 2.0) * pitch_um * 1e-6
    xx, yy = np.meshgrid(coords, coords, indexing="xy")
    return np.stack([xx.ravel(), yy.ravel()], axis=1)


def _biot_savart_columns(
    obs: np.ndarray, src: np.ndarray, direction: np.ndarray, length_m: float,
) -> np.ndarray:
    r = obs - src[None, :]
    norm = np.linalg.norm(r, axis=1)
    cross = np.cross(direction[None, :] * length_m, r)
    b = MU0_OVER_4PI * cross / (norm[:, None] ** 3 + EPS)
    return b.reshape(-1)


def build_operator(
    n: int, layers: int, pitch: float, dz: float, sensor_h: float,
) -> tuple[np.ndarray, dict]:
    """Build a single-height Biot-Savart operator and its index."""
    pitch_m = pitch * 1e-6
    dz_m = dz * 1e-6
    sensor_m = sensor_h * 1e-6

    xy = _grid_positions(n, pitch)
    cell_count = n * n
    z_layers = -np.arange(layers, dtype=float) * dz_m
    obs = np.column_stack([xy[:, 0], xy[:, 1], np.full(cell_count, sensor_m)])

    columns: list[np.ndarray] = []
    names: list[str] = []
    sheet_slices: dict[tuple[int, str], slice] = {}
    via_slices: dict[tuple[int, int], slice] = {}

    for layer in range(layers):
        z = z_layers[layer]
        start = len(columns)
        for i in range(cell_count):
            src = np.array([xy[i, 0], xy[i, 1], z], dtype=float)
            columns.append(_biot_savart_columns(obs, src, np.array([1.0, 0.0, 0.0]), pitch_m))
            names.append(f"L{layer}_Jx_{i}")
        sheet_slices[(layer, "x")] = slice(start, len(columns))

        start = len(columns)
        for i in range(cell_count):
            src = np.array([xy[i, 0], xy[i, 1], z], dtype=float)
            columns.append(_biot_savart_columns(obs, src, np.array([0.0, 1.0, 0.0]), pitch_m))
            names.append(f"L{layer}_Jy_{i}")
        sheet_slices[(layer, "y")] = slice(start, len(columns))

    for layer in range(layers - 1):
        z_mid = 0.5 * (z_layers[layer] + z_layers[layer + 1])
        start = len(columns)
        for i in range(cell_count):
            src = np.array([xy[i, 0], xy[i, 1], z_mid], dtype=float)
            columns.append(_biot_savart_columns(obs, src, np.array([0.0, 0.0, 1.0]), abs(dz_m)))
            names.append(f"V{layer}{layer+1}_{i}")
        via_slices[(layer, layer + 1)] = slice(start, len(columns))

    A = np.stack(columns, axis=1)
    col_norm = np.linalg.norm(A, axis=0)
    index = {
        "n": n, "layers": layers, "cell_count": cell_count,
        "sheet_slices": sheet_slices, "via_slices": via_slices,
        "names": names, "z_layers_m": z_layers, "pitch_m": pitch_m,
    }
    return A, index


def multi_height_operator_stack(cfg: dict) -> OperatorBundle:
    n = int(cfg["grid_size"]); layers = int(cfg["layer_count"])
    pitch = float(cfg["pixel_pitch_um"]); dz = float(cfg["layer_spacing_um"])
    heights = [float(h) for h in cfg["sensor_heights_um"]]

    per_height: dict[str, np.ndarray] = {}
    A_parts: list[np.ndarray] = []
    base_index = None

    for h in heights:
        A_h, idx = build_operator(n, layers, pitch, dz, h)
        A_parts.append(A_h)
        per_height[str(h)] = A_h
        if base_index is None:
            base_index = idx

    A = np.concatenate(A_parts, axis=0) if A_parts else np.empty((0, 0))
    assert base_index is not None
    col_norm = np.linalg.norm(A, axis=0)

    obs_positions_parts = []
    for h in heights:
        xy = _grid_positions(n, pitch)
        obs_positions_parts.append(np.column_stack([xy[:, 0], xy[:, 1], np.full(n * n, h * 1e-6)]))
    positions = np.column_stack([xy[:, 0], xy[:, 1], np.zeros(n * n)])

    return OperatorBundle(
        A=A, positions=positions,
        obs_positions=np.concatenate(obs_positions_parts, axis=0) if obs_positions_parts else np.empty((0, 3)),
        index=base_index, column_norms=col_norm,
        heights=tuple(heights),
        A_per_height=per_height,
        per_height_components={str(h): ["Bx", "By", "Bz"] for h in heights},
    )


def build_candidate_operator(
    cfg: dict, baseline_heights: list[float],
    candidate_height: float, candidate_components: list[str],
) -> OperatorBundle:
    n = int(cfg["grid_size"]); layers = int(cfg["layer_count"])
    pitch = float(cfg["pixel_pitch_um"]); dz = float(cfg["layer_spacing_um"])
    n_pixels = n * n

    A_parts: list[np.ndarray] = []
    base_index = None
    per_height_indexed: dict[str, np.ndarray] = {}
    per_height_comp: dict[str, list[str]] = {}

    for h in baseline_heights:
        A_h, idx = build_operator(n, layers, pitch, dz, h)
        A_parts.append(A_h)
        key = str(h)
        per_height_indexed[key] = A_h
        per_height_comp[key] = ["Bx", "By", "Bz"]
        if base_index is None:
            base_index = idx

    A_cand, _ = build_operator(n, layers, pitch, dz, candidate_height)
    mask = component_mask(candidate_components, n_pixels)
    A_cand_masked = A_cand[mask, :]
    A_parts.append(A_cand_masked)
    cand_key = f"{candidate_height}_cand"
    per_height_indexed[cand_key] = A_cand_masked
    per_height_comp[cand_key] = candidate_components

    A = np.concatenate(A_parts, axis=0) if A_parts else np.empty((0, 0))
    assert base_index is not None
    col_norm = np.linalg.norm(A, axis=0)

    all_heights = list(baseline_heights) + [candidate_height]
    obs_positions_parts = []
    for h in all_heights:
        xy = _grid_positions(n, pitch)
        obs_positions_parts.append(np.column_stack([xy[:, 0], xy[:, 1], np.full(n_pixels, h * 1e-6)]))
    positions = np.column_stack([xy[:, 0], xy[:, 1], np.zeros(n_pixels)])

    return OperatorBundle(
        A=A, positions=positions,
        obs_positions=np.concatenate(obs_positions_parts, axis=0) if obs_positions_parts else np.empty((0, 3)),
        index=base_index, column_norms=col_norm,
        heights=tuple(all_heights),
        A_per_height=per_height_indexed,
        per_height_components=per_height_comp,
    )


# ── multi-state operator ──────────────────────────────────────────────────

def build_multi_state_operator(base_bundle: OperatorBundle, n_states: int) -> OperatorBundle:
    """Build a block-diagonal multi-state operator.

    A_stacked = diag(A_base, A_base, ..., A_base)  (n_states blocks)
    Each state has independent current parameters.
    """
    if n_states <= 1:
        return OperatorBundle(
            A=base_bundle.A.copy(), positions=base_bundle.positions.copy(),
            obs_positions=base_bundle.obs_positions.copy(),
            index=dict(base_bundle.index),
            column_norms=base_bundle.column_norms.copy(),
            channel_count=base_bundle.channel_count,
            heights=base_bundle.heights,
            A_per_height=dict(base_bundle.A_per_height) if base_bundle.A_per_height else None,
            per_height_components=dict(base_bundle.per_height_components) if base_bundle.per_height_components else None,
            n_states=1,
        )

    A_base = base_bundle.A
    curr_dim_per_state = A_base.shape[1]
    obs_dim_per_state = A_base.shape[0]

    # Build block-diagonal A
    blocks = []
    for s in range(n_states):
        row_block = []
        for t in range(n_states):
            if s == t:
                row_block.append(A_base)
            else:
                row_block.append(np.zeros((obs_dim_per_state, curr_dim_per_state)))
        blocks.append(np.concatenate(row_block, axis=1))
    A_stacked = np.concatenate(blocks, axis=0)

    # Extend column norms (replicate per state)
    col_norms_stacked = np.tile(base_bundle.column_norms, n_states)

    # Extend index: multiply column ranges
    base_idx = dict(base_bundle.index)
    base_idx["n_states"] = n_states
    base_idx["curr_dim_per_state"] = curr_dim_per_state
    for key in list(base_idx["sheet_slices"].keys()):
        sl = base_idx["sheet_slices"][key]
        base_idx["sheet_slices"][key] = slice(sl.start, sl.stop)

    # Extended via/sheet slices (only for state 0; other states need offset)
    for s in range(n_states):
        offset = s * curr_dim_per_state
        if s == 0:
            continue
        for key in list(base_idx["via_slices"].keys()):
            sl0 = base_idx["via_slices"][key]
            base_idx[f"via_slices_s{s}_{key}"] = slice(sl0.start + offset, sl0.stop + offset)
        for key in list(base_idx["sheet_slices"].keys()):
            sl0 = base_idx["sheet_slices"][key]
            base_idx[f"sheet_slices_s{s}_{key}"] = slice(sl0.start + offset, sl0.stop + offset)

    # Obs positions: tile per state
    obs_stacked = np.tile(base_bundle.obs_positions, (n_states, 1))
    pos_stacked = np.tile(base_bundle.positions, (n_states, 1))

    return OperatorBundle(
        A=A_stacked, positions=pos_stacked, obs_positions=obs_stacked,
        index=base_idx, column_norms=col_norms_stacked,
        channel_count=base_bundle.channel_count,
        heights=base_bundle.heights,
        A_per_height=dict(base_bundle.A_per_height) if base_bundle.A_per_height else None,
        per_height_components=dict(base_bundle.per_height_components) if base_bundle.per_height_components else None,
        n_states=n_states,
    )


def build_default_operator(cfg: dict) -> OperatorBundle:
    return multi_height_operator_stack(cfg)


def operator_diagnostics(bundle: OperatorBundle) -> dict:
    A = bundle.A; idx = bundle.index
    via_norms = []; sheet_norms = []
    for sl in idx["via_slices"].values():
        via_norms.extend(bundle.column_norms[sl].tolist())
    for sl in idx["sheet_slices"].values():
        sheet_norms.extend(bundle.column_norms[sl].tolist())
    via_arr = np.asarray(via_norms, dtype=float); sheet_arr = np.asarray(sheet_norms, dtype=float)
    return {
        "shape": list(A.shape),
        "via_columns_nonzero": bool(np.all(via_arr > 0)),
        "via_column_norm_min": float(np.min(via_arr)),
        "via_column_norm_mean": float(np.mean(via_arr)),
        "sheet_column_norm_mean": float(np.mean(sheet_arr)),
        "condition_proxy": float(np.linalg.norm(A, ord="fro") / max(np.min(bundle.column_norms), 1e-30)),
        "heights_um": list(bundle.heights) if bundle.heights else [],
        "obs_dim": int(A.shape[0]), "current_dim": int(A.shape[1]),
        "n_states": int(bundle.n_states),
    }


def current_vector_size(bundle: OperatorBundle) -> int:
    return int(bundle.A.shape[1])


def empty_current(bundle: OperatorBundle) -> np.ndarray:
    return np.zeros(current_vector_size(bundle), dtype=float)


def add_gaussian_sheet_mode(x, bundle, layer, component, center, sigma_cells, amplitude):
    n = int(bundle.index["n"])
    yy, xx = np.mgrid[0:n, 0:n]
    cx, cy = center
    g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sigma_cells ** 2))
    g -= np.mean(g)
    sl = bundle.index["sheet_slices"][(layer, component)]
    x[sl] += amplitude * g.ravel()


def add_via_spot(x, bundle, layer0, layer1, center, amplitude, radius=0):
    n = int(bundle.index["n"])
    sl = bundle.index["via_slices"][(layer0, layer1)]
    arr = np.zeros((n, n), dtype=float)
    cx, cy = center
    for iy in range(max(0, cy - radius), min(n, cy + radius + 1)):
        for ix in range(max(0, cx - radius), min(n, cx + radius + 1)):
            arr[iy, ix] += amplitude
    x[sl] += arr.ravel()


def add_return_loop(x, bundle, layer, amplitude):
    n = int(bundle.index["n"])
    jx = np.zeros((n, n), dtype=float); jy = np.zeros((n, n), dtype=float)
    margin = max(1, n // 6)
    jx[margin, margin:-margin] += amplitude
    jx[-margin - 1, margin:-margin] -= amplitude
    jy[margin:-margin, margin] -= amplitude
    jy[margin:-margin, -margin - 1] += amplitude
    x[bundle.index["sheet_slices"][(layer, "x")]] += jx.ravel()
    x[bundle.index["sheet_slices"][(layer, "y")]] += jy.ravel()


def observation_dim(bundle: OperatorBundle) -> int:
    return int(bundle.A.shape[0])
