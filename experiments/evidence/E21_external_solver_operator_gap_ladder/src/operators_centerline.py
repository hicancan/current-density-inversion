"""Centerline Biot-Savart and analytic reference forward operators."""

from __future__ import annotations

from typing import List, Tuple

import numpy as np

from config import GridConfig

MU0 = 4e-7 * np.pi


def make_grid(cfg: GridConfig) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    fov_m = cfg.fov_um * 1e-6
    coords = np.linspace(-fov_m / 2, fov_m / 2, cfg.n)
    X, Y = np.meshgrid(coords, coords, indexing="xy")
    Z = np.full_like(X, cfg.measurement_z_um * 1e-6)
    points = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
    return X, Y, Z, points


def segment_field(
    points: np.ndarray,
    p0: np.ndarray,
    p1: np.ndarray,
    current: float = 1.0,
    n_steps: int = 80,
) -> np.ndarray:
    """Biot-Savart field for a finite straight segment via midpoint quadrature.

    Returns B in Tesla, shape (N, 3).
    """
    p0 = np.asarray(p0, dtype=float)
    p1 = np.asarray(p1, dtype=float)
    dl = (p1 - p0) / n_steps
    ts = (np.arange(n_steps) + 0.5) / n_steps
    mids = p0[None, :] + ts[:, None] * (p1 - p0)[None, :]
    eps_val = 1e-18
    B = np.zeros((points.shape[0], 3), dtype=float)
    for mid in mids:
        r = points - mid[None, :]
        r_norm = np.linalg.norm(r, axis=1)
        cross = np.cross(dl[None, :], r)
        B += cross / (r_norm[:, None] ** 3 + eps_val)
    return MU0 * current / (4 * np.pi) * B


def infinite_wire_field(
    points: np.ndarray,
    direction: np.ndarray,
    point_on_wire: np.ndarray,
    current: float = 1.0,
) -> np.ndarray:
    """Analytic infinite straight-wire Biot-Savart field (2D slice).

    For a wire along direction d (unit vector), field at observation point r:
    B = (μ₀ I) / (2π) * (d × r_perp) / |r_perp|²

    This is an analytic reference operator, not a numerical approximation.
    """
    d = np.asarray(direction, dtype=float)
    d = d / np.linalg.norm(d)
    pw = np.asarray(point_on_wire, dtype=float)
    r = points - pw[None, :]
    r_parallel = np.sum(r * d[None, :], axis=1, keepdims=True) * d[None, :]
    r_perp = r - r_parallel
    r_perp_sq = np.sum(r_perp * r_perp, axis=1)
    cross = np.cross(d[None, :], r_perp)
    eps_val = 1e-18
    return MU0 * current / (2 * np.pi) * cross / (r_perp_sq[:, None] + eps_val)


def centerline_forward(
    points: np.ndarray,
    geometry_segments: List[Tuple[np.ndarray, np.ndarray, str]],
    n_steps: int = 80,
) -> np.ndarray:
    """Compute forward field from a list of (p0, p1, name) segments.

    Each segment carries 1.0 A unit current. Returns B_total (N, 3) and segment fields dict.
    """
    B_total = np.zeros((points.shape[0], 3), dtype=float)
    segment_fields = {}
    for p0, p1, name in geometry_segments:
        B_seg = segment_field(points, p0, p1, current=1.0, n_steps=n_steps)
        segment_fields[name] = B_seg
        B_total += B_seg
    return B_total, segment_fields


def analytic_reference_forward(
    points: np.ndarray,
    geometry_segments: List[Tuple[np.ndarray, np.ndarray, str]],
) -> np.ndarray:
    """Analytic reference: use infinite-wire approximation for horizontal segments,
    fall back to centerline numerical for vertical ones.

    Returns B_total (N, 3) and segment fields dict.
    """
    B_total = np.zeros((points.shape[0], 3), dtype=float)
    segment_fields = {}
    for p0, p1, name in geometry_segments:
        direction = p1 - p0
        if abs(direction[2]) < 1e-12:
            B_seg = infinite_wire_field(points, direction, p0, current=1.0)
        else:
            B_seg = segment_field(points, p0, p1, current=1.0, n_steps=80)
        segment_fields[name] = B_seg
        B_total += B_seg
    return B_total, segment_fields


def compute_divB_proxy(B: np.ndarray, dx_m: float, n: int) -> float:
    """Compute a divB proxy residual from a 3-component field map.

    B shape: (n, n, 3). Uses central finite differences. Returns RMS residual.
    """
    dBx_dx = np.zeros_like(B[..., 0])
    dBy_dy = np.zeros_like(B[..., 1])
    dBx_dx[1:-1, :] = (B[2:, :, 0] - B[:-2, :, 0]) / (2 * dx_m)
    dBy_dy[:, 1:-1] = (B[:, 2:, 1] - B[:, :-2, 1]) / (2 * dx_m)
    divB = dBx_dx + dBy_dy
    return float(np.sqrt(np.mean(divB**2)))
