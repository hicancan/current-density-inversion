"""Biot-Savart forward operators for E23 round 4.

Includes centerline, finite-width surrogate, registration-gap surrogate,
and deep-layer-shift surrogate operator stress ladder.
"""
from __future__ import annotations

from typing import Any

import numpy as np

MU0_OVER_4PI = 1e-7


def sensor_grid(
    grid_size: int, z: float = 0.35,
    x_range: tuple[float, float] = (-1.0, 6.0),
    y_range: tuple[float, float] = (-1.5, 1.5),
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    xs = np.linspace(x_range[0], x_range[1], grid_size)
    ys = np.linspace(y_range[0], y_range[1], grid_size)
    X, Y = np.meshgrid(xs, ys)
    Z = np.full_like(X, z)
    return X, Y, Z, xs, ys


def forward_biot_savart_edge(
    src_pos: tuple[float, float], dst_pos: tuple[float, float],
    src_z_um: float, dst_z_um: float,
    X: np.ndarray, Y: np.ndarray, Z: np.ndarray,
    current: float = 1.0,
) -> np.ndarray:
    """Compute B-field from a single edge with given current.

    Returns Bxyz array of shape (grid_size, grid_size, 3).
    """
    cx = (src_pos[0] + dst_pos[0]) / 2.0
    cy = (src_pos[1] + dst_pos[1]) / 2.0
    cz = (src_z_um + dst_z_um) / 2.0 * 1e-3

    dx = dst_pos[0] - src_pos[0]
    dy = dst_pos[1] - src_pos[1]
    dz = (dst_z_um - src_z_um) * 1e-3
    dl = np.array([dx, dy, dz])

    dl_norm = np.linalg.norm(dl)
    if dl_norm < 1e-15:
        return np.zeros((X.shape[0], X.shape[1], 3))

    rx = X - cx
    ry = Y - cy
    rz = Z - cz
    r_norm = np.sqrt(rx**2 + ry**2 + rz**2)
    r_norm = np.maximum(r_norm, 1e-9)

    r_cube = r_norm ** 3
    # Convert mm^3 to m^3: multiply by (1e-3)^3 = 1e-9
    r_cube_m = r_cube * 1e-9

    cx_val = dl[1] * rz - dl[2] * ry
    cy_val = dl[2] * rx - dl[0] * rz
    cz_val = dl[0] * ry - dl[1] * rx

    # dl is in mm, convert cross product to m: multiply by 1e-3
    scale = MU0_OVER_4PI * current / r_cube_m * 1e-3

    B = np.zeros((X.shape[0], X.shape[1], 3))
    B[:, :, 0] = cx_val * scale
    B[:, :, 1] = cy_val * scale
    B[:, :, 2] = cz_val * scale

    return B


# ---------------------------------------------------------------------------
# Operator stress ladder
# ---------------------------------------------------------------------------

def build_centerline_operator(
    graph: dict[str, Any],
    edge_order: list[str],
    grid_size: int,
    sensor_z: float,
    x_range: tuple[float, float] = (-1.0, 6.0),
    y_range: tuple[float, float] = (-1.5, 1.5),
) -> np.ndarray:
    """Original centerline Biot-Savart operator.

    Each edge contributes one column: A[:, j] = B_centerline(edge_j, I=1).
    """
    m = len(edge_order)
    n_obs = grid_size * grid_size * 3
    A = np.zeros((n_obs, m))

    X, Y, Z, xs, ys = sensor_grid(grid_size, sensor_z, x_range, y_range)

    for j, eid in enumerate(edge_order):
        ed = graph["edges"][eid]
        src_pos = ed.get("src_pos", (0.0, 0.0))
        dst_pos = ed.get("dst_pos", (0.0, 0.0))
        src_z = ed.get("src_z_um", 0.0)
        dst_z = ed.get("dst_z_um", 0.0)
        B_edge = forward_biot_savart_edge(src_pos, dst_pos, src_z, dst_z, X, Y, Z, 1.0)
        A[:, j] = B_edge.ravel()

    return A


def build_finite_width_surrogate_operator(
    graph: dict[str, Any],
    edge_order: list[str],
    grid_size: int,
    sensor_z: float,
    x_range: tuple[float, float] = (-1.0, 6.0),
    y_range: tuple[float, float] = (-1.5, 1.5),
    n_filaments: int = 3,
) -> np.ndarray:
    """Finite-width surrogate: split each edge into n_filaments parallel sub-filaments.

    Sub-filaments are spaced width/3 apart perpendicular to edge direction.
    Current is split equally: I_filament = 1/n_filaments.
    """
    m = len(edge_order)
    n_obs = grid_size * grid_size * 3
    A = np.zeros((n_obs, m))

    X, Y, Z, xs, ys = sensor_grid(grid_size, sensor_z, x_range, y_range)

    for j, eid in enumerate(edge_order):
        ed = graph["edges"][eid]
        sx, sy = ed.get("src_pos", (0.0, 0.0))
        dx_p, dy_p = ed.get("dst_pos", (0.0, 0.0))
        src_z = ed.get("src_z_um", 0.0)
        dst_z = ed.get("dst_z_um", 0.0)

        # Edge direction and perpendicular direction (in XY plane)
        ex = dx_p - sx
        ey = dy_p - sy
        length = np.hypot(ex, ey)
        if length < 1e-9:
            B_edge = forward_biot_savart_edge((sx, sy), (dx_p, dy_p), src_z, dst_z, X, Y, Z, 1.0)
            A[:, j] = B_edge.ravel()
            continue

        # Unit perpendicular (rotate 90 deg CCW)
        nx = -ey / length
        ny = ex / length

        width_mm = ed.get("width_um", 100.0) * 1e-3
        spacing = width_mm / n_filaments

        B_sum = np.zeros((X.shape[0], X.shape[1], 3))
        for k in range(n_filaments):
            offset = spacing * (k - (n_filaments - 1) / 2.0)
            osx = sx + nx * offset
            osy = sy + ny * offset
            odx = dx_p + nx * offset
            ody = dy_p + ny * offset
            B_sub = forward_biot_savart_edge(
                (osx, osy), (odx, ody), src_z, dst_z, X, Y, Z, 1.0 / n_filaments
            )
            B_sum += B_sub

        A[:, j] = B_sum.ravel()

    return A


def build_registration_gap_surrogate_operator(
    graph: dict[str, Any],
    edge_order: list[str],
    grid_size: int,
    sensor_z: float,
    x_range: tuple[float, float] = (-1.0, 6.0),
    y_range: tuple[float, float] = (-1.5, 1.5),
    jitter_sigma_mm: float = 0.1,
    seed: int = 20260506,
) -> np.ndarray:
    """Registration-gap surrogate: add deterministic jitter to sensor positions.

    Simulates sensor misalignment/registration error by shifting each
    grid point by a small random offset.
    """
    m = len(edge_order)
    n_obs = grid_size * grid_size * 3
    A = np.zeros((n_obs, m))

    X, Y, Z, xs, ys = sensor_grid(grid_size, sensor_z, x_range, y_range)
    rng = np.random.RandomState(seed)
    X_jit = X + rng.normal(0, jitter_sigma_mm, X.shape)
    Y_jit = Y + rng.normal(0, jitter_sigma_mm, Y.shape)
    Z_jit = Z  # no z-jitter for registration

    for j, eid in enumerate(edge_order):
        ed = graph["edges"][eid]
        src_pos = ed.get("src_pos", (0.0, 0.0))
        dst_pos = ed.get("dst_pos", (0.0, 0.0))
        src_z = ed.get("src_z_um", 0.0)
        dst_z = ed.get("dst_z_um", 0.0)
        B_edge = forward_biot_savart_edge(src_pos, dst_pos, src_z, dst_z, X_jit, Y_jit, Z_jit, 1.0)
        A[:, j] = B_edge.ravel()

    return A


def build_deep_layer_shift_surrogate_operator(
    graph: dict[str, Any],
    edge_order: list[str],
    grid_size: int,
    sensor_z: float,
    x_range: tuple[float, float] = (-1.0, 6.0),
    y_range: tuple[float, float] = (-1.5, 1.5),
    shift_um: float = 50.0,
) -> np.ndarray:
    """Deep-layer-shift surrogate: shift z of deeper layers to simulate
    layer-thickness uncertainty and standoff errors for buried traces.

    Edges on layers with |z_mid| > 15um get an additional z-shift.
    """
    m = len(edge_order)
    n_obs = grid_size * grid_size * 3
    A = np.zeros((n_obs, m))

    X, Y, Z, xs, ys = sensor_grid(grid_size, sensor_z, x_range, y_range)

    for j, eid in enumerate(edge_order):
        ed = graph["edges"][eid]
        src_pos = ed.get("src_pos", (0.0, 0.0))
        dst_pos = ed.get("dst_pos", (0.0, 0.0))
        src_z = ed.get("src_z_um", 0.0)
        dst_z = ed.get("dst_z_um", 0.0)

        # Shift deeper layers
        avg_z = (abs(src_z) + abs(dst_z)) / 2.0
        if avg_z > 15.0:
            src_z += shift_um * np.sign(src_z) if abs(src_z) > 0 else shift_um
            dst_z += shift_um * np.sign(dst_z) if abs(dst_z) > 0 else shift_um

        B_edge = forward_biot_savart_edge(src_pos, dst_pos, src_z, dst_z, X, Y, Z, 1.0)
        A[:, j] = B_edge.ravel()

    return A


# Backward-compatible alias
build_forward_operator = build_centerline_operator
