"""Forward operator adapter for E18.

Builds the same Biot-Savart forward operator matrix A as E15, mapping
11*n*n current/via channels to 3*m*m sensor field values.
Also provides the KCL divergence constraint matrix.
"""
from __future__ import annotations
import numpy as np

MU0_OVER_4PI = 1e-7
LAYER_IDS = ["L1", "L2", "L3", "L4"]


def grid_centers(cfg: dict):
    n = int(cfg["grid_size"])
    x0, x1, y0, y1 = cfg["in_plane_extent"]
    xs = np.linspace(x0 + (x1 - x0) / (2 * n), x1 - (x1 - x0) / (2 * n), n)
    ys = np.linspace(y0 + (y1 - y0) / (2 * n), y1 - (y1 - y0) / (2 * n), n)
    return xs, ys, xs[1] - xs[0], ys[1] - ys[0]


def sensor_grid(cfg: dict):
    m = int(cfg["sensor_grid_size"])
    x0, x1, y0, y1 = cfg["in_plane_extent"]
    xs = np.linspace(x0, x1, m)
    ys = np.linspace(y0, y1, m)
    xx, yy = np.meshgrid(xs, ys)
    zz = np.full_like(xx, float(cfg["sensor_z"]))
    return xx, yy, zz, np.stack([xx, yy, zz], axis=-1)


def build_forward_operator(cfg: dict):
    """Build the Biot-Savart forward operator A.

    Returns (A, via_base_index) where A is (3*m*m, 11*n*n) and
    via_base_index is 8*n*n (start of via channels).
    """
    n = int(cfg["grid_size"])
    m = int(cfg["sensor_grid_size"])
    depths = {l: float(cfg["layer_depths"][l]) for l in LAYER_IDS}
    xs, ys, dx, dy = grid_centers(cfg)
    dA = dx * dy
    pts = sensor_grid(cfg)[3].reshape(-1, 3)
    ns = len(pts)
    pl = n * n
    A = np.zeros((3 * ns, 11 * pl))

    for li, lid in enumerate(LAYER_IDS):
        z = depths[lid]
        for iy in range(n):
            py = ys[iy]
            for ix in range(n):
                px = xs[ix]
                r = pts - np.array([px, py, z])
                n3 = np.maximum(np.linalg.norm(r, axis=1) ** 3, 1e-18)
                f = MU0_OVER_4PI * dA / n3
                rz = r[:, 2]
                rx = r[:, 0]
                ry = r[:, 1]
                jc = li * 2 * pl + iy * n + ix
                jyc = jc + pl
                # Jx contribution: dB = mu0/(4pi) * (Jx x r) / |r|^3 * dA
                A[0::3, jc] = 0.0
                A[1::3, jc] = -f * rz
                A[2::3, jc] = f * ry
                # Jy contribution
                A[0::3, jyc] = f * rz
                A[1::3, jyc] = 0.0
                A[2::3, jyc] = -f * rx
    return A, 8 * pl


def build_div_matrix(n: int):
    """Build the discrete divergence matrix for KCL constraint.

    Returns D of shape (4*n*n, 11*n*n).
    """
    pl = n * n
    D = np.zeros((4 * pl, 11 * pl))
    sc = float(n)
    for layer in range(4):
        base = layer * pl
        jxb = layer * 2 * pl
        jyb = jxb + pl
        for iy in range(n):
            for ix in range(n):
                row = base + iy * n + ix
                nx = (ix + 1) % n
                ny = (iy + 1) % n
                D[row, jxb + iy * n + nx] = sc
                D[row, jxb + iy * n + ix] = -sc
                D[row, jyb + ny * n + ix] = sc
                D[row, jyb + iy * n + ix] = -sc
    return D


def forward_predict(A: np.ndarray, x: np.ndarray, field_shape: tuple):
    """Predict B field from current vector x."""
    return (A @ x).reshape(field_shape)
