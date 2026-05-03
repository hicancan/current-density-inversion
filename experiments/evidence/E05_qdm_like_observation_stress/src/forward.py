from __future__ import annotations

import numpy as np
from dataclasses import dataclass

MU0 = 4 * np.pi * 1e-7


@dataclass(frozen=True)
class Segment:
    p0: np.ndarray
    p1: np.ndarray
    current_A: float
    name: str = "segment"

    @staticmethod
    def make(p0, p1, current_A, name="segment"):
        return Segment(np.asarray(p0, dtype=float), np.asarray(p1, dtype=float), float(current_A), name)


def make_grid(fov_m: float, n: int):
    x = np.linspace(-fov_m / 2, fov_m / 2, n)
    y = np.linspace(-fov_m / 2, fov_m / 2, n)
    X, Y = np.meshgrid(x, y, indexing="xy")
    dx = x[1] - x[0]
    return X, Y, dx


def standoff_plane(X, Y, z0_m: float, alpha: float = 0.0, beta: float = 0.0):
    return z0_m + alpha * X + beta * Y


def observation_points(X, Y, Z):
    return np.stack([X, Y, Z], axis=-1)


def biot_savart_segments(segments: list[Segment], obs_points: np.ndarray, n_sub: int = 200, eps: float = 1e-18):
    """Numerically integrate Biot-Savart over finite line segments.

    Parameters
    ----------
    segments:
        List of current-carrying line segments in SI units.
    obs_points:
        Array with shape (..., 3), in SI units.
    n_sub:
        Number of midpoint subdivisions per segment.
    eps:
        Small regularizer for numerical safety.

    Returns
    -------
    B:
        Array with shape (..., 3), Tesla.
    """
    B = np.zeros_like(obs_points, dtype=float)
    pref = MU0 / (4 * np.pi)
    flat_obs = obs_points.reshape(-1, 3)
    flat_B = np.zeros_like(flat_obs)
    for seg in segments:
        dl_total = seg.p1 - seg.p0
        dl = dl_total / n_sub
        mids = seg.p0 + (np.arange(n_sub)[:, None] + 0.5) * dl
        # process in chunks over subdivisions to keep memory bounded
        for mid in mids:
            r = flat_obs - mid[None, :]
            r_norm = np.linalg.norm(r, axis=1)
            denom = np.maximum(r_norm**3, eps)
            cross = np.cross(dl[None, :], r)
            flat_B += pref * seg.current_A * cross / denom[:, None]
    return flat_B.reshape(obs_points.shape)


def make_two_layer_via_circuit(current_A: float, d1: float, d2: float, length: float = 0.00145):
    """A minimal L1 -> via -> L2 current path.

    L1: horizontal x-segment ending at via.
    Via: vertical segment from layer1 to layer2.
    L2: vertical y-segment leaving via.
    Coordinates: sample surface z=0, layers below surface z=-d.
    """
    half = length / 2
    layer1 = [Segment.make([-half, 0.0, -d1], [0.0, 0.0, -d1], current_A, "layer1_x")]
    via = [Segment.make([0.0, 0.0, -d1], [0.0, 0.0, -d2], current_A, "via_down")]
    layer2 = [Segment.make([0.0, 0.0, -d2], [0.0, half, -d2], current_A, "layer2_y")]
    return layer1, layer2, via


def bxy_energy(B):
    return float(np.sqrt(np.mean(B[..., 0] ** 2 + B[..., 1] ** 2)))


def high_frequency_energy(field2d: np.ndarray, cutoff_fraction: float = 0.28):
    """Rough high-frequency energy for diagnostics."""
    F = np.fft.fftshift(np.fft.fft2(field2d))
    n, m = field2d.shape
    yy, xx = np.ogrid[-n//2:n//2, -m//2:m//2]
    rr = np.sqrt((xx / (m / 2)) ** 2 + (yy / (n / 2)) ** 2)
    mask = rr >= cutoff_fraction
    return float(np.mean(np.abs(F[mask]) ** 2))
