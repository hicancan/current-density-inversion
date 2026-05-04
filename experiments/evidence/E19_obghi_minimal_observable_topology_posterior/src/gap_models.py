"""Gap model reference pattern generators for oracle tests.

These produce registration-derivative and standoff-laplacian patterns in
observation (B-field) space. They are reference patterns used to construct
truth model-gap signals for controlled experiments, not basis columns.
"""

from __future__ import annotations

import numpy as np


def registration_pattern(
    n: int,
    center: tuple[float, float],
    sigma_cells: float,
    amplitude: float,
) -> np.ndarray:
    """Generate a registration-gradient B-field pattern.

    Returns a flattened (3*n*n,) array with dG/dx on Bx, dG/dy on By,
    and (dG/dx - dG/dy) on Bz, all zero-mean per channel.
    """
    yy, xx = np.mgrid[0:n, 0:n]
    cx, cy = center
    g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sigma_cells ** 2))
    gx = np.gradient(g, axis=1)
    gy = np.gradient(g, axis=0)
    out = np.zeros((3, n, n), dtype=float)
    out[0] = amplitude * gx
    out[1] = amplitude * gy
    out[2] = 0.5 * amplitude * (gx - gy)
    out -= np.mean(out, axis=(1, 2), keepdims=True)
    return out.reshape(-1)


def standoff_laplacian_pattern(
    clean_field: np.ndarray,
    amplitude: float,
) -> np.ndarray:
    """Generate a standoff-laplacian B-field pattern from a clean field.

    Applies a 5-point finite-difference Laplacian to each vector channel
    of the clean field, normalises to unit norm, and scales by amplitude.
    """
    n = int(round(np.cbrt(clean_field.size / 3)))
    f = clean_field.reshape(3, n, n)
    lap = np.zeros_like(f)
    for c in range(3):
        arr = f[c]
        lap[c] = (
            -4.0 * arr
            + np.roll(arr, 1, axis=0)
            + np.roll(arr, -1, axis=0)
            + np.roll(arr, 1, axis=1)
            + np.roll(arr, -1, axis=1)
        )
    norm = float(np.linalg.norm(lap.ravel()))
    if norm > 0:
        lap = lap / norm
    return amplitude * lap.reshape(-1)


def multi_channel_gaussian(
    n: int,
    center: tuple[float, float],
    sigma_cells: float,
    channels: tuple[int, ...] = (0, 1, 2),
) -> np.ndarray:
    """Generate a zero-mean Gaussian B-field pattern on specified channels.

    Returns a flattened (3*n*n,) array with the same Gaussian on each
    requested channel.
    """
    yy, xx = np.mgrid[0:n, 0:n]
    cx, cy = center
    g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sigma_cells ** 2))
    g -= np.mean(g)
    out = np.zeros((3, n, n), dtype=float)
    for ch in channels:
        out[ch] = g
    return out.reshape(-1)


def laplacian_gaussian_pattern(
    n: int,
    center: tuple[float, float],
    sigma_cells: float,
    channel: int,
) -> np.ndarray:
    """Generate a Laplacian-of-Gaussian B-field pattern on one channel.

    Returns a flattened (3*n*n,) array.
    """
    yy, xx = np.mgrid[0:n, 0:n]
    cx, cy = center
    r2 = (xx - cx) ** 2 + (yy - cy) ** 2
    s2 = sigma_cells ** 2
    g = np.exp(-r2 / (2.0 * s2))
    lap = (r2 / s2 - 2.0) / s2 * g
    lap -= np.mean(lap)
    out = np.zeros((3, n, n), dtype=float)
    out[channel] = lap
    return out.reshape(-1)


def blurred_minus_original_pattern(
    n: int,
    center: tuple[float, float],
    sigma_cells: float,
    channel: int,
) -> np.ndarray:
    """Generate a blurred-minus-original B-field pattern.

    Returns difference of two Gaussians at sigma and 2*sigma, zero-mean.
    """
    yy, xx = np.mgrid[0:n, 0:n]
    cx, cy = center
    g1 = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sigma_cells ** 2))
    g2 = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * (2.0 * sigma_cells) ** 2))
    diff = g2 - g1
    diff -= np.mean(diff)
    out = np.zeros((3, n, n), dtype=float)
    out[channel] = diff
    return out.reshape(-1)
