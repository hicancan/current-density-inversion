"""Simple via template matching utilities."""
from __future__ import annotations

import numpy as np
from scipy.signal import fftconvolve


def whiten_channels(B: np.ndarray, eps: float = 1e-30) -> np.ndarray:
    """Zero-mean/unit-std per channel."""
    W = B.copy().astype(float)
    for c in range(W.shape[-1]):
        W[..., c] -= np.mean(W[..., c])
        W[..., c] /= np.std(W[..., c]) + eps
    return W


def normalized_template_score(field_bxy: np.ndarray, template_bxy: np.ndarray, eps: float = 1e-30) -> np.ndarray:
    """Compute normalized cross-correlation score for two-channel Bxy data.

    field_bxy and template_bxy have shape (H, W, 2). The template is assumed centered.
    """
    F = whiten_channels(field_bxy)
    T = whiten_channels(template_bxy)
    # Zero out far tails in template weighting implicitly by subtracting mean and normalizing.
    score = np.zeros(F.shape[:2], dtype=float)
    norm_t = 0.0
    for c in range(2):
        # Correlate with flipped template via convolution.
        score += fftconvolve(F[..., c], T[::-1, ::-1, c], mode="same")
        norm_t += np.sum(T[..., c] ** 2)
    # local norm of field patch; approximate with convolution of squared field with template support.
    support = np.ones(T.shape[:2], dtype=float)
    local_norm = np.zeros_like(score)
    for c in range(2):
        local_norm += fftconvolve(F[..., c] ** 2, support[::-1, ::-1], mode="same")
    return score / (np.sqrt(local_norm * norm_t) + eps)


def peak_location(score: np.ndarray, x: np.ndarray, y: np.ndarray):
    idx = np.unravel_index(np.nanargmax(score), score.shape)
    return {"iy": int(idx[0]), "ix": int(idx[1]), "x_m": float(x[idx[1]]), "y_m": float(y[idx[0]]), "score": float(score[idx])}
