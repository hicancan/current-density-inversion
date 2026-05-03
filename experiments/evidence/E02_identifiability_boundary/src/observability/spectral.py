"""Fourier-domain Biot--Savart forward and inverse operators.

The equations follow the standard thin-sheet, quasi-static, free-space model
used for 2D sheet-current reconstruction. The sheet current lies in z=0 and
is measured on a plane at z=h.

Fourier convention:
    np.fft.fftfreq returns cycles / metre. We convert to angular wavenumber
    k_rad = 2*pi*cycles/metre. Derivatives use i*k_rad.
"""
from __future__ import annotations

import numpy as np

from .constants import MU0, EPS
from .grid import Grid2D


def streamfunction_current(grid: Grid2D, seed: int = 7) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate a smooth divergence-free sheet current from a stream function.

    Jx = d psi / dy, Jy = - d psi / dx.
    Units are arbitrary but scaled into A/m. The output is useful for testing
    spectral inversions because it is approximately divergence-free.
    """
    x, y = grid.coordinates()
    rng = np.random.default_rng(seed)
    psi = np.zeros_like(x, dtype=float)

    # A mixture of Gaussian vortices, with signs and widths spanning scales.
    for _ in range(7):
        cx = rng.uniform(-0.32, 0.32) * grid.fov_m
        cy = rng.uniform(-0.32, 0.32) * grid.fov_m
        sigma = rng.uniform(0.035, 0.12) * grid.fov_m
        amp = rng.uniform(-1.0, 1.0)
        psi += amp * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2.0 * sigma**2))

    # Spectral derivatives reduce finite-difference divergence artifacts.
    kx, ky, _ = grid.angular_frequencies()
    psi_hat = np.fft.fft2(psi)
    jx = np.real(np.fft.ifft2(1j * ky * psi_hat))
    jy = np.real(np.fft.ifft2(-1j * kx * psi_hat))

    # Scale to a practical sheet-current range: max |J| ~ 1 A/m.
    mag = np.sqrt(jx**2 + jy**2)
    scale = np.max(mag) + EPS
    jx = jx / scale
    jy = jy / scale
    return jx, jy, psi


def manhattan_sheet_current(grid: Grid2D) -> tuple[np.ndarray, np.ndarray]:
    """Create a simple divergence-free Manhattan-style current pattern.

    This is not intended to be a full EDA model. It gives exp02 a second,
    less smooth target than random stream functions.
    """
    x, y = grid.coordinates()
    jx = np.zeros_like(x)
    jy = np.zeros_like(x)

    def stripe(coord: np.ndarray, center: float, width: float) -> np.ndarray:
        return np.exp(-0.5 * ((coord - center) / width) ** 8)

    # Two long horizontal tracks and two vertical returns. The opposing flows
    # avoid a large nonzero DC current component.
    width = 0.025 * grid.fov_m
    jx += 1.0 * stripe(y, -0.18 * grid.fov_m, width)
    jx += -0.85 * stripe(y, 0.20 * grid.fov_m, width)
    jy += 0.65 * stripe(x, -0.23 * grid.fov_m, width)
    jy += -0.65 * stripe(x, 0.25 * grid.fov_m, width)

    # Taper near boundaries to reduce periodic discontinuity.
    r = np.maximum(np.abs(x), np.abs(y)) / (0.5 * grid.fov_m)
    window = 0.5 * (1 + np.cos(np.pi * np.clip((r - 0.75) / 0.25, 0, 1)))
    return jx * window, jy * window


def _safe_unit_k(kx: np.ndarray, ky: np.ndarray, kmag: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    k_safe = np.where(kmag > 0, kmag, 1.0)
    return kx / k_safe, ky / k_safe


def forward_sheet_fft(
    jx: np.ndarray, jy: np.ndarray, grid: Grid2D, standoff_m: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Map sheet current (Jx,Jy) to magnetic field (Bx,By,Bz)."""
    if jx.shape != (grid.n, grid.n) or jy.shape != (grid.n, grid.n):
        raise ValueError("current arrays must match grid size")
    kx, ky, kmag = grid.angular_frequencies()
    _, ky_u = _safe_unit_k(kx, ky, kmag)
    kx_u, _ = _safe_unit_k(kx, ky, kmag)

    exp_decay = np.exp(-kmag * standoff_m)
    pref = 0.5 * MU0 * exp_decay
    jx_hat = np.fft.fft2(jx)
    jy_hat = np.fft.fft2(jy)

    bx_hat = pref * jy_hat
    by_hat = -pref * jx_hat
    bz_hat = pref * (1j * ky_u * jx_hat - 1j * kx_u * jy_hat)
    bz_hat = np.where(kmag > 0, bz_hat, 0.0)

    bx = np.real(np.fft.ifft2(bx_hat))
    by = np.real(np.fft.ifft2(by_hat))
    bz = np.real(np.fft.ifft2(bz_hat))
    return bx, by, bz


def inverse_bxy_fft(
    bx: np.ndarray,
    by: np.ndarray,
    grid: Grid2D,
    standoff_m: float,
    regularization: float = 0.0,
    k_cut_rad_per_m: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Invert sheet current from transverse magnetic field Bx, By.

    regularization is a simple Wiener-like stabilizer in the inverse gain.
    k_cut_rad_per_m optionally applies a smooth Gaussian low-pass to avoid
    unphysical high-k amplification when noise is present.
    """
    kx, ky, kmag = grid.angular_frequencies()
    bx_hat = np.fft.fft2(bx)
    by_hat = np.fft.fft2(by)
    gain = (2.0 / MU0) * np.exp(kmag * standoff_m)
    if regularization > 0:
        # Damp high inverse gains: gain / (1 + reg * gain^2)
        gain = gain / (1.0 + regularization * gain**2)
    if k_cut_rad_per_m is not None and k_cut_rad_per_m > 0:
        gain = gain * np.exp(-0.5 * (kmag / k_cut_rad_per_m) ** 2)
    jx_hat = -gain * by_hat
    jy_hat = gain * bx_hat
    return np.real(np.fft.ifft2(jx_hat)), np.real(np.fft.ifft2(jy_hat))


def inverse_bz_fft(
    bz: np.ndarray,
    grid: Grid2D,
    standoff_m: float,
    regularization: float = 0.0,
    k_cut_rad_per_m: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Invert divergence-free sheet current from Bz.

    The k=0 component is not observable from Bz and is set to zero.
    """
    kx, ky, kmag = grid.angular_frequencies()
    kx_u, ky_u = _safe_unit_k(kx, ky, kmag)
    bz_hat = np.fft.fft2(bz)
    gain = (2.0 / MU0) * np.exp(kmag * standoff_m)
    if regularization > 0:
        gain = gain / (1.0 + regularization * gain**2)
    if k_cut_rad_per_m is not None and k_cut_rad_per_m > 0:
        gain = gain * np.exp(-0.5 * (kmag / k_cut_rad_per_m) ** 2)

    mask = kmag > 0
    jx_hat = np.zeros_like(bz_hat, dtype=complex)
    jy_hat = np.zeros_like(bz_hat, dtype=complex)
    jx_hat[mask] = gain[mask] * (ky_u[mask] / (1j)) * bz_hat[mask]
    jy_hat[mask] = -gain[mask] * (kx_u[mask] / (1j)) * bz_hat[mask]
    return np.real(np.fft.ifft2(jx_hat)), np.real(np.fft.ifft2(jy_hat))


def add_noise_like(field: np.ndarray, relative: float, rng: np.random.Generator) -> np.ndarray:
    """Add Gaussian noise with std = relative * max(abs(field))."""
    sigma = relative * (np.max(np.abs(field)) + EPS)
    return field + rng.normal(0.0, sigma, size=field.shape)


def relative_l2(pred: tuple[np.ndarray, np.ndarray], truth: tuple[np.ndarray, np.ndarray]) -> float:
    px, py = pred
    tx, ty = truth
    num = np.sqrt(np.sum((px - tx) ** 2 + (py - ty) ** 2))
    den = np.sqrt(np.sum(tx**2 + ty**2)) + EPS
    return float(num / den)


def attenuation_for_feature(feature_size_m: np.ndarray, standoff_m: float) -> np.ndarray:
    """Return exp(-kz) using k=2*pi/lambda for a spatial feature size lambda."""
    return np.exp(-2.0 * np.pi * standoff_m / np.asarray(feature_size_m))


def recoverable_feature_size(standoff_m: float, attenuation_threshold: float) -> float:
    """Smallest lambda with exp(-2*pi*z/lambda) >= threshold."""
    if not (0.0 < attenuation_threshold < 1.0):
        raise ValueError("attenuation_threshold must be in (0,1)")
    return float(2.0 * np.pi * standoff_m / (-np.log(attenuation_threshold)))
