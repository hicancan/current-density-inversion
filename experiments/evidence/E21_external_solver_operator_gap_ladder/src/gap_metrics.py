"""Operator-gap metrics: field-level and spectral comparisons.

Computes:
- component RMSE and relative field error
- spectral error by spatial frequency
- sign/polarity consistency
- divB proxy residual
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np


@dataclass
class FieldGap:
    pair_name: str
    rel_rmse: float = 0.0
    per_component_rel_rmse: Dict[str, float] = field(default_factory=dict)
    spectral_low_k: float = 0.0
    spectral_high_k: float = 0.0
    polarity_consistency: float = 0.0
    sign_match_rate: float = 0.0
    divB_residual_a: float = 0.0
    divB_residual_b: float = 0.0
    raw_l2_diff: float = 0.0


def compute_field_gap(
    B_a: np.ndarray,
    B_b: np.ndarray,
    dx_m: float,
    pair_name: str,
    components: Tuple[str, ...] = ("Bx", "By", "Bz"),
) -> FieldGap:
    """Compute field-level operator gap between two field maps.

    Args:
        B_a, B_b: Field maps, shape (n, n, 3).
        dx_m: Grid spacing in meters.
        pair_name: Label for this operator pair.
        components: Component names.

    Returns:
        FieldGap dataclass with all gap metrics.
    """
    diff = B_a - B_b
    norm_b = np.linalg.norm(B_b)
    norm_a = np.linalg.norm(B_a)
    eps = 1e-30

    rel_rmse = float(np.sqrt(np.mean(diff**2)) / (np.sqrt(np.mean(B_b**2)) + eps))
    raw_l2 = float(np.linalg.norm(diff) / (norm_b + eps))

    per_comp = {}
    for c, name in enumerate(components):
        nc = np.linalg.norm(B_b[..., c])
        per_comp[name] = float(np.linalg.norm(diff[..., c]) / (nc + eps))

    # Spectral decomposition via 2D FFT
    n = B_a.shape[0]
    fa = np.fft.fft2(B_a.reshape(n, n, 3), axes=(0, 1))
    fb = np.fft.fft2(B_b.reshape(n, n, 3), axes=(0, 1))
    fdiff = fa - fb

    freqs = np.fft.fftfreq(n, d=dx_m)
    kx, ky = np.meshgrid(freqs, freqs, indexing="xy")
    k_mag = np.sqrt(kx**2 + ky**2)
    k_median = float(np.median(k_mag[k_mag > 0])) if np.any(k_mag > 0) else 1.0

    low_mask = k_mag <= k_median
    high_mask = k_mag > k_median

    spec_low = float(np.sum(np.abs(fdiff) * low_mask[..., None]) / (np.sum(np.abs(fb) * low_mask[..., None]) + eps))
    spec_high = float(np.sum(np.abs(fdiff) * high_mask[..., None]) / (np.sum(np.abs(fb) * high_mask[..., None]) + eps))

    # Sign/polarity: per-pixel sign agreement
    sign_a = np.sign(B_a)
    sign_b = np.sign(B_b)
    # Only count pixels with nonzero signal in both
    nonzero = (np.abs(B_a) > 1e-20) & (np.abs(B_b) > 1e-20)
    if np.any(nonzero):
        sign_match = float(np.mean((sign_a[nonzero] == sign_b[nonzero]).astype(float)))
    else:
        sign_match = 1.0

    # Polarity consistency: correlation of sign patterns
    flat_a = B_a.reshape(-1, 3)
    flat_b = B_b.reshape(-1, 3)
    norms_a = np.linalg.norm(flat_a, axis=1)
    norms_b = np.linalg.norm(flat_b, axis=1)
    nonzero_mask = (norms_a > 1e-20) & (norms_b > 1e-20)
    if np.sum(nonzero_mask) > 10:
        corr = np.sum(flat_a[nonzero_mask] * flat_b[nonzero_mask]) / (
            np.sqrt(np.sum(flat_a[nonzero_mask]**2) * np.sum(flat_b[nonzero_mask]**2)) + eps
        )
        polarity = max(0.0, float(corr))
    else:
        polarity = 0.0

    # divB proxy
    div_a = _divB_proxy(B_a, dx_m)
    div_b = _divB_proxy(B_b, dx_m)

    return FieldGap(
        pair_name=pair_name,
        rel_rmse=rel_rmse,
        per_component_rel_rmse=per_comp,
        spectral_low_k=spec_low,
        spectral_high_k=spec_high,
        polarity_consistency=polarity,
        sign_match_rate=sign_match,
        divB_residual_a=div_a,
        divB_residual_b=div_b,
        raw_l2_diff=raw_l2,
    )


def _divB_proxy(B: np.ndarray, dx_m: float) -> float:
    n = B.shape[0]
    dBx_dx = np.zeros_like(B[..., 0])
    dBy_dy = np.zeros_like(B[..., 1])
    if n >= 3:
        dBx_dx[1:-1, :] = (B[2:, :, 0] - B[:-2, :, 0]) / (2 * dx_m)
        dBy_dy[:, 1:-1] = (B[:, 2:, 1] - B[:, :-2, 1]) / (2 * dx_m)
    divB = dBx_dx + dBy_dy
    return float(np.sqrt(np.mean(divB**2)))


def compute_all_gaps(
    field_maps: Dict[str, np.ndarray],
    dx_m: float,
) -> List[FieldGap]:
    """Compute pairwise operator gaps for all field maps."""
    names = sorted(field_maps.keys())
    gaps = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            name_a, name_b = names[i], names[j]
            pair = f"{name_a}_vs_{name_b}"
            gap = compute_field_gap(field_maps[name_a], field_maps[name_b], dx_m, pair)
            gaps.append(gap)
    return gaps


def compute_unit_sanity(field_maps: Dict[str, np.ndarray]) -> Dict[str, bool]:
    """Check that all field maps have same shape."""
    if not field_maps:
        return {"same_shape": True, "count": 0}
    shapes = {name: B.shape for name, B in field_maps.items()}
    first_shape = list(shapes.values())[0]
    all_same = all(s == first_shape for s in shapes.values())
    return {"same_shape": all_same, "shape": first_shape, "count": len(field_maps)}
