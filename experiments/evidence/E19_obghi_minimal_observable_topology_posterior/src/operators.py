"""Generated forward operators for four-layer sheet/via magnetic inversion.

The operator is intentionally lightweight and deterministic. It is not a
replacement for high-fidelity Maxwell/FEM/FastHenry validation. It gives E19 a
small but nontrivial generated domain where via, return-path, and model-gap
explanations can compete under a common observation operator.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


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


def _grid_positions(n: int, pitch_um: float) -> np.ndarray:
    coords = (np.arange(n, dtype=float) - (n - 1) / 2.0) * pitch_um * 1e-6
    xx, yy = np.meshgrid(coords, coords, indexing="xy")
    return np.stack([xx.ravel(), yy.ravel()], axis=1)


def _biot_savart_columns(
    obs: np.ndarray,
    src: np.ndarray,
    direction: np.ndarray,
    length_m: float,
) -> np.ndarray:
    """Return Bx/By/Bz columns for unit current element at src."""
    r = obs - src[None, :]
    norm = np.linalg.norm(r, axis=1)
    cross = np.cross(direction[None, :] * length_m, r)
    b = MU0_OVER_4PI * cross / (norm[:, None] ** 3 + EPS)
    return b.reshape(-1)


def build_operator(cfg: dict) -> OperatorBundle:
    n = int(cfg["grid_size"])
    layers = int(cfg["layer_count"])
    pitch = float(cfg["pixel_pitch_um"])
    dz = float(cfg["layer_spacing_um"]) * 1e-6
    sensor_h = float(cfg["sensor_height_um"]) * 1e-6
    pitch_m = pitch * 1e-6

    xy = _grid_positions(n, pitch)
    cell_count = n * n
    z_layers = -np.arange(layers, dtype=float) * dz
    obs = np.column_stack([xy[:, 0], xy[:, 1], np.full(cell_count, sensor_h)])

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
            columns.append(_biot_savart_columns(obs, src, np.array([0.0, 0.0, 1.0]), abs(dz)))
            names.append(f"V{layer}{layer+1}_{i}")
        via_slices[(layer, layer + 1)] = slice(start, len(columns))

    A = np.stack(columns, axis=1)
    col_norm = np.linalg.norm(A, axis=0)
    # Column normalization used only for numerical scale diagnostics and ridge baseline.
    # Bayesian evidence keeps explicit basis prior variances.
    index = {
        "n": n,
        "layers": layers,
        "cell_count": cell_count,
        "sheet_slices": sheet_slices,
        "via_slices": via_slices,
        "names": names,
        "z_layers_m": z_layers,
        "pitch_m": pitch_m,
    }
    positions = np.column_stack([xy[:, 0], xy[:, 1], np.zeros(cell_count)])
    return OperatorBundle(A=A, positions=positions, obs_positions=obs, index=index, column_norms=col_norm)


def operator_diagnostics(bundle: OperatorBundle) -> dict:
    A = bundle.A
    idx = bundle.index
    via_norms = []
    sheet_norms = []
    for sl in idx["via_slices"].values():
        via_norms.extend(bundle.column_norms[sl].tolist())
    for sl in idx["sheet_slices"].values():
        sheet_norms.extend(bundle.column_norms[sl].tolist())
    via_norms_arr = np.asarray(via_norms, dtype=float)
    sheet_norms_arr = np.asarray(sheet_norms, dtype=float)
    return {
        "shape": list(A.shape),
        "via_columns_nonzero": bool(np.all(via_norms_arr > 0)),
        "via_column_norm_min": float(np.min(via_norms_arr)),
        "via_column_norm_mean": float(np.mean(via_norms_arr)),
        "sheet_column_norm_mean": float(np.mean(sheet_norms_arr)),
        "condition_proxy": float(np.linalg.norm(A, ord="fro") / max(np.min(bundle.column_norms), 1e-30)),
    }


def current_vector_size(bundle: OperatorBundle) -> int:
    return int(bundle.A.shape[1])


def empty_current(bundle: OperatorBundle) -> np.ndarray:
    return np.zeros(current_vector_size(bundle), dtype=float)


def sheet_view(x: np.ndarray, bundle: OperatorBundle, layer: int, component: str) -> np.ndarray:
    n = int(bundle.index["n"])
    sl = bundle.index["sheet_slices"][(layer, component)]
    return x[sl].reshape(n, n)


def via_view(x: np.ndarray, bundle: OperatorBundle, layer0: int, layer1: int) -> np.ndarray:
    n = int(bundle.index["n"])
    sl = bundle.index["via_slices"][(layer0, layer1)]
    return x[sl].reshape(n, n)


def add_gaussian_sheet_mode(
    x: np.ndarray,
    bundle: OperatorBundle,
    layer: int,
    component: str,
    center: tuple[float, float],
    sigma_cells: float,
    amplitude: float,
) -> None:
    n = int(bundle.index["n"])
    yy, xx = np.mgrid[0:n, 0:n]
    cx, cy = center
    g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sigma_cells ** 2))
    g -= np.mean(g)
    sl = bundle.index["sheet_slices"][(layer, component)]
    x[sl] += amplitude * g.ravel()


def add_via_spot(
    x: np.ndarray,
    bundle: OperatorBundle,
    layer0: int,
    layer1: int,
    center: tuple[int, int],
    amplitude: float,
    radius: int = 0,
) -> None:
    n = int(bundle.index["n"])
    sl = bundle.index["via_slices"][(layer0, layer1)]
    arr = np.zeros((n, n), dtype=float)
    cx, cy = center
    for iy in range(max(0, cy - radius), min(n, cy + radius + 1)):
        for ix in range(max(0, cx - radius), min(n, cx + radius + 1)):
            arr[iy, ix] += amplitude
    x[sl] += arr.ravel()


def add_return_loop(x: np.ndarray, bundle: OperatorBundle, layer: int, amplitude: float) -> None:
    n = int(bundle.index["n"])
    jx = np.zeros((n, n), dtype=float)
    jy = np.zeros((n, n), dtype=float)
    margin = max(1, n // 6)
    jx[margin, margin:-margin] += amplitude
    jx[-margin - 1, margin:-margin] -= amplitude
    jy[margin:-margin, margin] -= amplitude
    jy[margin:-margin, -margin - 1] += amplitude
    x[bundle.index["sheet_slices"][(layer, "x")]] += jx.ravel()
    x[bundle.index["sheet_slices"][(layer, "y")]] += jy.ravel()
