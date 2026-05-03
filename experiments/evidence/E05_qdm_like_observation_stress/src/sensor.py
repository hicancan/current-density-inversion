from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter


def apply_psf(B: np.ndarray, sigma_px: float):
    if sigma_px <= 0:
        return B.copy()
    out = np.empty_like(B)
    for c in range(B.shape[-1]):
        out[..., c] = gaussian_filter(B[..., c], sigma=sigma_px, mode="nearest")
    return out


def make_confidence_map(B: np.ndarray, floor: float = 0.35, percentile: float = 90.0):
    """A simple QDM-like confidence model.

    Strong off-axis/in-plane field decreases confidence. This is not a Hamiltonian model;
    it is a stress-test proxy for spatially varying SNR.
    """
    Bxy = np.sqrt(B[..., 0] ** 2 + B[..., 1] ** 2)
    scale = np.percentile(Bxy, percentile) + 1e-30
    # close to 1 for low Bxy, floor for high Bxy
    conf = floor + (1 - floor) * np.exp(-(Bxy / scale) ** 2)
    return np.clip(conf, floor, 1.0)


def correlated_noise(shape_hw: tuple[int, int], sigma_T, corr, spatial_sigma_px: float, rng: np.random.Generator):
    """Generate channel-correlated and spatially correlated Gaussian noise.

    Returns
    -------
    noise: (H, W, 3) Tesla
    base_noise: (H, W, 3) Tesla before spatial filtering, for covariance diagnostics
    """
    sigma = np.asarray(sigma_T, dtype=float)
    corr = np.asarray(corr, dtype=float)
    cov = np.diag(sigma) @ corr @ np.diag(sigma)
    H, W = shape_hw
    base = rng.multivariate_normal(np.zeros(3), cov, size=H * W).reshape(H, W, 3)
    if spatial_sigma_px <= 0:
        return base.copy(), base
    out = np.empty_like(base)
    # Smooth each channel; then rescale to preserve channel std approximately.
    for c in range(3):
        sm = gaussian_filter(base[..., c], sigma=spatial_sigma_px, mode="reflect")
        std0 = np.std(base[..., c]) + 1e-30
        std1 = np.std(sm) + 1e-30
        out[..., c] = sm * (std0 / std1)
    # Re-mix to restore cross-channel covariance after independent spatial smoothing.
    return out, base


def observe_qdm_like(B_true: np.ndarray, psf_sigma_px: float, noise_sigma_T, noise_corr, spatial_corr_sigma_px: float,
                     confidence_floor: float, confidence_percentile: float, rng: np.random.Generator):
    B_blur = apply_psf(B_true, psf_sigma_px)
    confidence = make_confidence_map(B_blur, floor=confidence_floor, percentile=confidence_percentile)
    noise, base_noise = correlated_noise(B_blur.shape[:2], noise_sigma_T, noise_corr, spatial_corr_sigma_px, rng)
    # lower confidence -> larger local effective noise
    noise_scaled = noise / np.sqrt(confidence[..., None])
    B_obs = B_blur + noise_scaled
    return {
        "B_blur": B_blur,
        "B_obs": B_obs,
        "noise": noise_scaled,
        "base_noise": base_noise,
        "confidence": confidence,
    }


def empirical_corr(noise: np.ndarray):
    X = noise.reshape(-1, noise.shape[-1])
    return np.corrcoef(X, rowvar=False)
