"""Forward Biot-Savart operator for E26 port-network current model.

Self-contained four-layer grid operator; independent of E19_2 imports.
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
    index: dict[str, object]
    column_norms: np.ndarray
    sensor_height_um: float


def grid_positions(n: int, pitch_um: float) -> np.ndarray:
    coords = (np.arange(n, dtype=float) - (n - 1) / 2.0) * pitch_um * 1e-6
    xx, yy = np.meshgrid(coords, coords, indexing="xy")
    return np.stack([xx.ravel(), yy.ravel()], axis=1)


def biot_savart_columns(
    obs: np.ndarray, src: np.ndarray, direction: np.ndarray, length_m: float,
) -> np.ndarray:
    r = obs - src[None, :]
    norm = np.linalg.norm(r, axis=1)
    cross = np.cross(direction[None, :] * length_m, r)
    return (MU0_OVER_4PI * cross / (norm[:, None] ** 3 + EPS)).reshape(-1)


def build_operator(
    n: int, layers: int, pitch: float, dz: float, sensor_h: float,
) -> tuple[np.ndarray, dict]:
    pitch_m = pitch * 1e-6
    dz_m = dz * 1e-6
    sensor_m = sensor_h * 1e-6
    xy = grid_positions(n, pitch)
    cell_count = n * n
    z_layers = -np.arange(layers, dtype=float) * dz_m
    obs = np.column_stack([xy[:, 0], xy[:, 1], np.full(cell_count, sensor_m)])

    columns: list[np.ndarray] = []
    sheet_slices: dict[tuple[int, str], slice] = {}
    via_slices: dict[tuple[int, int], slice] = {}

    for layer in range(layers):
        z = z_layers[layer]
        start = len(columns)
        for i in range(cell_count):
            src = np.array([xy[i, 0], xy[i, 1], z], dtype=float)
            columns.append(biot_savart_columns(obs, src, np.array([1.0, 0.0, 0.0]), pitch_m))
        sheet_slices[(layer, "x")] = slice(start, len(columns))
        start = len(columns)
        for i in range(cell_count):
            src = np.array([xy[i, 0], xy[i, 1], z], dtype=float)
            columns.append(biot_savart_columns(obs, src, np.array([0.0, 1.0, 0.0]), pitch_m))
        sheet_slices[(layer, "y")] = slice(start, len(columns))

    for layer in range(layers - 1):
        z_mid = 0.5 * (z_layers[layer] + z_layers[layer + 1])
        start = len(columns)
        for i in range(cell_count):
            src = np.array([xy[i, 0], xy[i, 1], z_mid], dtype=float)
            columns.append(biot_savart_columns(obs, src, np.array([0.0, 0.0, 1.0]), abs(dz_m)))
        via_slices[(layer, layer + 1)] = slice(start, len(columns))

    A = np.stack(columns, axis=1)
    col_norm = np.linalg.norm(A, axis=0)
    index = {
        "n": n, "layers": layers, "cell_count": cell_count,
        "sheet_slices": sheet_slices, "via_slices": via_slices,
        "z_layers_m": z_layers, "pitch_m": pitch_m,
    }
    return A, index


def build_default_operator(cfg: dict) -> OperatorBundle:
    n = int(cfg["grid_size"])
    layers = 4
    pitch = float(cfg["pixel_pitch_um"])
    dz = float(cfg.get("layer_spacing_um", 2.0))
    sensor_h = float(cfg["sensor_height_um"])
    A, idx = build_operator(n, layers, pitch, dz, sensor_h)
    col_norm = np.linalg.norm(A, axis=0)
    xy = grid_positions(n, pitch)
    positions = np.column_stack([xy[:, 0], xy[:, 1], np.zeros(n * n)])
    return OperatorBundle(A=A, positions=positions, index=idx, column_norms=col_norm, sensor_height_um=sensor_h)
