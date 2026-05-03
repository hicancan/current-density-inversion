"""Finite-segment Biot-Savart forward model.

All units are SI:
- coordinates: metre
- current: ampere
- magnetic field: tesla
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

MU0 = 4.0e-7 * np.pi


@dataclass(frozen=True)
class Segment:
    """A directed finite current segment.

    The current flows from p0 to p1.  The physical current amplitude is I_A.
    """

    p0: tuple[float, float, float]
    p1: tuple[float, float, float]
    I_A: float
    name: str = "segment"
    group: str = "unknown"


def make_grid(fov_m: float, n: int, sensor_z_m: float = 0.0):
    """Return X, Y, Z meshgrids in SI units."""
    x = np.linspace(-fov_m / 2.0, fov_m / 2.0, n)
    y = np.linspace(-fov_m / 2.0, fov_m / 2.0, n)
    X, Y = np.meshgrid(x, y, indexing="xy")
    Z = np.full_like(X, sensor_z_m, dtype=float)
    return X, Y, Z


def field_from_segment(X: np.ndarray, Y: np.ndarray, Z: np.ndarray, seg: Segment, n_quad: int = 160, eps: float = 1e-24) -> np.ndarray:
    """Compute B field from one finite segment by midpoint quadrature.

    Returns array with shape (H, W, 3).
    """
    p0 = np.asarray(seg.p0, dtype=float)
    p1 = np.asarray(seg.p1, dtype=float)
    dl_total = p1 - p0
    dl = dl_total / float(n_quad)
    # Midpoints along the segment.
    t = (np.arange(n_quad, dtype=float) + 0.5) / float(n_quad)
    pts = p0[None, :] + t[:, None] * dl_total[None, :]

    B = np.zeros(X.shape + (3,), dtype=float)
    obs = np.stack([X, Y, Z], axis=-1)
    pref = MU0 * seg.I_A / (4.0 * np.pi)
    for p in pts:
        R = obs - p
        r2 = np.sum(R * R, axis=-1) + eps
        r3 = r2 ** 1.5
        cross = np.cross(dl, R)
        B += pref * cross / r3[..., None]
    return B


def field_from_segments(X: np.ndarray, Y: np.ndarray, Z: np.ndarray, segments: list[Segment], n_quad: int = 160) -> np.ndarray:
    """Compute total B field from a list of segments."""
    B = np.zeros(X.shape + (3,), dtype=float)
    for seg in segments:
        B += field_from_segment(X, Y, Z, seg, n_quad=n_quad)
    return B


def group_field(X: np.ndarray, Y: np.ndarray, Z: np.ndarray, segments: list[Segment], group: str, n_quad: int = 160) -> np.ndarray:
    return field_from_segments(X, Y, Z, [s for s in segments if s.group == group], n_quad=n_quad)


def norm_field(B: np.ndarray) -> np.ndarray:
    return np.sqrt(np.sum(B * B, axis=-1))


def rel_l2(a: np.ndarray, b: np.ndarray, eps: float = 1e-30) -> float:
    return float(np.linalg.norm((a - b).ravel()) / (np.linalg.norm(b.ravel()) + eps))
