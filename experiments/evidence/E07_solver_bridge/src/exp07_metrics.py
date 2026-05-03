"""Metrics and gates for exp07 solver cross-validation."""

from __future__ import annotations

import math
import numpy as np


def rel_l2(a: np.ndarray, b: np.ndarray, eps: float = 1e-30) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.linalg.norm(a - b) / (np.linalg.norm(b) + eps))


def max_abs(a: np.ndarray) -> float:
    return float(np.max(np.abs(np.asarray(a))))


def b_magnitude(B: np.ndarray) -> np.ndarray:
    return np.sqrt(np.sum(np.asarray(B) ** 2, axis=0))


def peak_index(B: np.ndarray) -> tuple[int, int]:
    mag = b_magnitude(B)
    idx = int(np.argmax(mag))
    return tuple(int(x) for x in np.unravel_index(idx, mag.shape))


def peak_location_error_px(a: np.ndarray, b: np.ndarray) -> float:
    ia = peak_index(a)
    ib = peak_index(b)
    return float(math.sqrt((ia[0] - ib[0]) ** 2 + (ia[1] - ib[1]) ** 2))


def via_bz_over_bxy(B: np.ndarray, center_exclusion_px: int = 1) -> float:
    """Return max |Bz| / max sqrt(Bx^2+By^2), excluding singular center pixels."""
    B = np.asarray(B)
    bx, by, bz = B[0], B[1], B[2]
    mask = np.ones_like(bz, dtype=bool)
    h, w = bz.shape
    cy, cx = h // 2, w // 2
    r = int(center_exclusion_px)
    mask[max(0, cy - r) : min(h, cy + r + 1), max(0, cx - r) : min(w, cx + r + 1)] = False
    numerator = float(np.max(np.abs(bz[mask])))
    denominator = float(np.max(np.sqrt(bx[mask] ** 2 + by[mask] ** 2))) + 1e-30
    return numerator / denominator


def is_strictly_decreasing(values: list[float], atol: float = 0.0) -> bool:
    return all(values[i] > values[i + 1] + atol for i in range(len(values) - 1))


def finite_median(values: list[float]) -> float:
    vals = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    return float(np.median(vals)) if len(vals) else float("nan")


def pass_fail(value: bool) -> str:
    return "PASS" if bool(value) else "FAIL"
