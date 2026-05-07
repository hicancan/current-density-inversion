"""Forward operator: Biot-Savart mapping from edge currents to sensor fields.

Builds observation operator A_h for each topology, mapping network edge
currents to magnetic field measurements at sensor positions.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from graphs import TopologyGraph

MU0_OVER_4PI = 1e-7
EPS = 1e-18


@dataclass
class ForwardBundle:
    A: np.ndarray           # stacked sensor matrix (M_total, |E|)
    A_per_height: dict[float, np.ndarray]
    heights: tuple[float, ...]
    sensor_xy: np.ndarray   # (sensor_count, 2) in meters
    graph: TopologyGraph


def _biot_savart_segment(
    obs: np.ndarray, src_start: np.ndarray, src_end: np.ndarray
) -> np.ndarray:
    """Biot-Savart for a finite straight current segment (3D).

    Approximates field contribution from unit current along edge.
    Uses the finite-length formula:

      B(r) = (mu0/4pi) * I * (dl x (r - r')) / |r - r'|^3

    integrated along [src_start, src_end].
    """
    dl = src_end - src_start  # edge vector
    mid = 0.5 * (src_start + src_end)
    r = obs - mid[None, :]
    norm = np.linalg.norm(r, axis=1)
    cross = np.cross(dl[None, :], r)
    b = MU0_OVER_4PI * cross / (norm[:, None] ** 3 + EPS)
    return b.reshape(-1)  # (3*sensor_count,)


def build_forward_operator(
    graph: TopologyGraph, sensor_heights_um: list[float],
    sensor_grid_n: int, sensor_pitch_um: float,
) -> ForwardBundle:
    """Build stacked multi-height Biot-Savart operator.

    For each sensor height, computes A_h and stacks them vertically.
    The sensor grid is independent from the current graph grid.
    """
    pitch_m = sensor_pitch_um * 1e-6
    heights_m = [h * 1e-6 for h in sensor_heights_um]

    # Sensor positions (xy grid)
    coords = (np.arange(sensor_grid_n, dtype=float) - (sensor_grid_n - 1) / 2.0) * pitch_m
    xx, yy = np.meshgrid(coords, coords, indexing="xy")
    sensor_xy = np.column_stack([xx.ravel(), yy.ravel()])
    sensor_count = sensor_grid_n * sensor_grid_n

    A_parts: list[np.ndarray] = []
    A_per_height: dict[float, np.ndarray] = {}

    for h in heights_m:
        obs = np.column_stack([sensor_xy, np.full(sensor_count, h)])
        columns: list[np.ndarray] = []

        for e in range(graph.edge_count):
            u, v = graph.edges[e]
            src_start = graph.node_positions[u]
            src_end = graph.node_positions[v]
            columns.append(_biot_savart_segment(obs, src_start, src_end))

        A_h = np.column_stack(columns)
        A_parts.append(A_h)
        A_per_height[h * 1e6] = A_h

    A = np.concatenate(A_parts, axis=0) if A_parts else np.zeros((0, graph.edge_count))

    return ForwardBundle(
        A=A,
        A_per_height=A_per_height,
        heights=tuple(sensor_heights_um),
        sensor_xy=sensor_xy,
        graph=graph,
    )


def forward_multistate(
    bundle: ForwardBundle, I: np.ndarray, noise_sigma: float, rng: np.random.Generator
) -> np.ndarray:
    """Compute stacked multi-state field observations with noise.

    Args:
        bundle: forward operator
        I: edge currents (|E|, S)
        noise_sigma: noise std
        rng: random generator

    Returns:
        Y: stacked observations, shape (M_total * S,)
    """
    S = I.shape[1]
    obs_per_state = bundle.A.shape[0]

    Y = np.zeros(obs_per_state * S, dtype=float)
    for s in range(S):
        clean = bundle.A @ I[:, s]
        noise = rng.normal(0.0, noise_sigma, size=obs_per_state)
        Y[s * obs_per_state:(s + 1) * obs_per_state] = clean + noise
    return Y


def forward_clean_multistate(bundle: ForwardBundle, I: np.ndarray) -> np.ndarray:
    """Noise-free forward for multi-state currents."""
    S = I.shape[1]
    obs_per_state = bundle.A.shape[0]
    Y = np.zeros(obs_per_state * S, dtype=float)
    for s in range(S):
        Y[s * obs_per_state:(s + 1) * obs_per_state] = bundle.A @ I[:, s]
    return Y


def operator_diagnostics(bundle: ForwardBundle) -> dict:
    A = bundle.A
    col_norms = np.linalg.norm(A, axis=0)
    col_norms = np.maximum(col_norms, 1e-30)
    return {
        "shape": list(A.shape),
        "obs_dim": int(A.shape[0]),
        "current_dim": int(A.shape[1]),
        "heights_um": list(bundle.heights),
        "column_norm_min": float(np.min(col_norms)),
        "column_norm_mean": float(np.mean(col_norms)),
        "column_norm_max": float(np.max(col_norms)),
        "fro_norm": float(np.linalg.norm(A, ord="fro")),
    }
