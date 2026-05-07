"""Finite-width surrogate forward operator.

Adds finite conductor width, depth shifts, weak return currents, and
observation nuisances (PSF blur, noise) on top of the centerline operator.
"""

from __future__ import annotations

from typing import List, Tuple

import numpy as np
from scipy.ndimage import gaussian_filter

from operators_centerline import segment_field, make_grid


def finite_width_forward(
    points: np.ndarray,
    geometry_segments: List[Tuple[np.ndarray, np.ndarray, str]],
    width_um: float = 20.0,
    n_filaments: int = 5,
    n_steps: int = 80,
    depth_shift_um: float = 3.0,
    return_scale: float = 0.8,
    ground_z_um: float = -75.0,
    psf_sigma_px: float = 0.0,
    noise_std_uT: float = 0.0,
    rng: np.random.Generator | None = None,
) -> Tuple[np.ndarray, dict]:
    """Finite-width surrogate: each horizontal segment is spread across filaments,
    depth-shifted, with optional return and observation nuisances.

    Returns B_total (N, 3) and dict of segment fields.
    """
    width_m = width_um * 1e-6
    dz = depth_shift_um * 1e-6
    z_ground = ground_z_um * 1e-6

    B_total = np.zeros((points.shape[0], 3), dtype=float)
    segment_fields = {}

    for p0, p1, name in geometry_segments:
        B_seg = np.zeros((points.shape[0], 3), dtype=float)
        direction = p1 - p0
        is_horizontal = abs(direction[2]) < 1e-12

        if is_horizontal:
            dxy = direction[:2]
            norm = np.linalg.norm(dxy)
            tangent = dxy / max(norm, 1e-18)
            normal_xy = np.array([-tangent[1], tangent[0]])
            offsets_xy = np.linspace(-0.5, 0.5, n_filaments) * width_m
            for off in offsets_xy:
                shift = np.array([normal_xy[0] * off, normal_xy[1] * off, dz])
                B_seg += segment_field(
                    points, p0 + shift, p1 + shift, 1.0 / n_filaments, n_steps=n_steps
                )
            if return_scale > 0:
                for off in offsets_xy:
                    shift = np.array([normal_xy[0] * off * 1.8, normal_xy[1] * off * 1.8, z_ground - (p0[2] + dz)])
                    B_seg += segment_field(
                        points,
                        np.array([p0[0] + shift[0], p0[1] + shift[1], z_ground]),
                        np.array([p1[0] + shift[0], p1[1] + shift[1], z_ground]),
                        -return_scale / n_filaments,
                        n_steps=n_steps,
                    )
        else:
            # Vertical segment: spread as a cluster of parallel vertical filaments
            via_radius_m = 5e-6
            offsets_via = [(0.0, 0.0), (via_radius_m * 0.6, 0), (-via_radius_m * 0.6, 0),
                           (0, via_radius_m * 0.6), (0, -via_radius_m * 0.6)]
            for ox, oy in offsets_via:
                shift = np.array([ox, oy, dz])
                B_seg += segment_field(
                    points, p0 + shift, p1 + shift, 1.0 / len(offsets_via), n_steps=n_steps
                )

        segment_fields[name] = B_seg
        B_total += B_seg

    if noise_std_uT > 0:
        if rng is None:
            rng = np.random.default_rng(0)
        B_total += rng.normal(scale=noise_std_uT * 1e-6, size=B_total.shape)

    return B_total, segment_fields


def apply_psf_blur(field_map: np.ndarray, sigma_px: float) -> np.ndarray:
    """Apply per-component Gaussian PSF blur. field_map shape: (n, n, 3)."""
    if sigma_px <= 0:
        return field_map.copy()
    return np.stack(
        [gaussian_filter(field_map[..., c], sigma=sigma_px, mode="nearest") for c in range(3)],
        axis=-1,
    )


def add_noise(field_map: np.ndarray, noise_std_uT: float, rng: np.random.Generator | None = None) -> np.ndarray:
    if noise_std_uT <= 0:
        return field_map.copy()
    if rng is None:
        rng = np.random.default_rng(0)
    return field_map + rng.normal(scale=noise_std_uT * 1e-6, size=field_map.shape)


# --- Round 2: Stronger operator perturbations ---

def missing_return_forward(
    points: np.ndarray,
    geometry_segments: List[Tuple[np.ndarray, np.ndarray, str]],
    width_um: float = 20.0,
    n_filaments: int = 5,
    n_steps: int = 80,
    depth_shift_um: float = 3.0,
    noise_std_uT: float = 0.0,
    rng: np.random.Generator | None = None,
) -> Tuple[np.ndarray, dict]:
    """Finite-width operator with NO return current — models missing ground plane.

    This is a deliberately incomplete forward: the missing return creates
    a large field-level and decision-level gap versus the full operator.
    """
    return finite_width_forward(
        points, geometry_segments,
        width_um=width_um, n_filaments=n_filaments, n_steps=n_steps,
        depth_shift_um=depth_shift_um, return_scale=0.0,  # NO return
        ground_z_um=-75.0,
        noise_std_uT=noise_std_uT, rng=rng,
    )


def deep_layer_shift_forward(
    points: np.ndarray,
    geometry_segments: List[Tuple[np.ndarray, np.ndarray, str]],
    n_steps: int = 80,
    depth_shift_um: float = 15.0,
    noise_std_uT: float = 0.0,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Centerline forward with large depth perturbation.

    Shifts all segments by a large depth offset (e.g. 15um instead of 3um),
    simulating a severe layer-registration error.
    """
    from operators_centerline import segment_field
    dz = depth_shift_um * 1e-6
    B_total = np.zeros((points.shape[0], 3), dtype=float)
    for p0, p1, _ in geometry_segments:
        dp = np.array([0.0, 0.0, dz])
        B_total += segment_field(points, p0 + dp, p1 + dp, 1.0)
    if noise_std_uT > 0:
        if rng is None:
            rng = np.random.default_rng(0)
        B_total += rng.normal(scale=noise_std_uT * 1e-6, size=B_total.shape)
    return B_total, {}


def registration_gap_forward(
    points: np.ndarray,
    geometry_segments: List[Tuple[np.ndarray, np.ndarray, str]],
    n_steps: int = 80,
    shift_x_um: float = 10.0,
    shift_y_um: float = 5.0,
    noise_std_uT: float = 0.0,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Centerline forward with a spatial registration offset.

    Simulates a tilt/alignment error by shifting the observation grid.
    The field is computed at shifted observation positions.
    """
    from operators_centerline import segment_field
    dx = shift_x_um * 1e-6
    dy = shift_y_um * 1e-6
    shifted_points = points + np.array([dx, dy, 0.0])[None, :]
    B_total = np.zeros((shifted_points.shape[0], 3), dtype=float)
    for p0, p1, _ in geometry_segments:
        B_total += segment_field(shifted_points, p0, p1, 1.0, n_steps=n_steps)
    if noise_std_uT > 0:
        if rng is None:
            rng = np.random.default_rng(0)
        B_total += rng.normal(scale=noise_std_uT * 1e-6, size=B_total.shape)
    return B_total, {}
