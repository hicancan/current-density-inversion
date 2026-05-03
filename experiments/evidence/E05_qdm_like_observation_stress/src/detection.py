from __future__ import annotations

import numpy as np
from scipy.signal import correlate2d
from scipy.ndimage import gaussian_filter


def dog_filter(field: np.ndarray, sigma_small: float, sigma_large: float):
    return gaussian_filter(field, sigma_small, mode="reflect") - gaussian_filter(field, sigma_large, mode="reflect")


def dog_filter_B(B: np.ndarray, sigma_small: float, sigma_large: float):
    out = np.empty_like(B)
    for c in range(B.shape[-1]):
        out[..., c] = dog_filter(B[..., c], sigma_small, sigma_large)
    return out


def crop_patch(arr: np.ndarray, center: tuple[int, int], radius: int):
    cy, cx = center
    return arr[cy-radius:cy+radius+1, cx-radius:cx+radius+1, ...]


def normalize_template(T: np.ndarray):
    T0 = T - np.mean(T, axis=(0, 1), keepdims=True)
    norm = np.sqrt(np.sum(T0**2)) + 1e-30
    return T0 / norm


def matched_filter_score_map(B: np.ndarray, template: np.ndarray, channels=(0, 1)):
    """Multi-channel normalized correlation using a local template."""
    T = normalize_template(template[..., channels])
    score = np.zeros(B.shape[:2], dtype=float)
    for local_idx, c in enumerate(channels):
        img = B[..., c] - np.mean(B[..., c])
        score += correlate2d(img, T[..., local_idx], mode="same", boundary="symm")
    denom = np.sqrt(np.mean(B[..., channels] ** 2)) + 1e-30
    return score / denom


def peak_location(score: np.ndarray, dx_m: float, fov_m: float):
    iy, ix = np.unravel_index(np.argmax(score), score.shape)
    n = score.shape[0]
    x = -fov_m / 2 + ix * dx_m
    y = -fov_m / 2 + iy * dx_m
    return iy, ix, x, y, float(score[iy, ix])


def loc_error_um(loc, true_xy=(0.0, 0.0)):
    _, _, x, y, _ = loc
    return float(np.sqrt((x - true_xy[0]) ** 2 + (y - true_xy[1]) ** 2) * 1e6)
