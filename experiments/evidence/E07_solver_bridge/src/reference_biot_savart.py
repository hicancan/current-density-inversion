"""Biot-Savart reference models for exp07 solver cross-validation."""

from __future__ import annotations

import math
import numpy as np
from geometry import Segment

MU0 = 4.0 * math.pi * 1.0e-7
MU0_OVER_4PI = 1.0e-7


def _orthonormal_cross_section_axes(direction: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    direction = direction / (np.linalg.norm(direction) + 1e-30)
    z_axis = np.array([0.0, 0.0, 1.0])
    x_axis = np.array([1.0, 0.0, 0.0])
    seed = z_axis if abs(float(np.dot(direction, z_axis))) < 0.92 else x_axis
    u = np.cross(direction, seed)
    u = u / (np.linalg.norm(u) + 1e-30)
    v = np.cross(direction, u)
    v = v / (np.linalg.norm(v) + 1e-30)
    return u, v


def subdivide_segment(segment: Segment, n: int) -> tuple[np.ndarray, np.ndarray, float]:
    start = np.asarray(segment.start, dtype=float)
    end = np.asarray(segment.end, dtype=float)
    n = max(1, int(n))
    edges = np.linspace(0.0, 1.0, n + 1)
    p0 = start[None, :] + (end - start)[None, :] * edges[:-1, None]
    p1 = start[None, :] + (end - start)[None, :] * edges[1:, None]
    mid = 0.5 * (p0 + p1)
    dl = p1 - p0
    return mid, dl, segment.current_a


def segment_field(points: np.ndarray, segment: Segment, n_sub: int = 24) -> np.ndarray:
    """Return B(points) for one segment, shape [P, 3]."""
    points = np.asarray(points, dtype=float)
    mid, dl, current = subdivide_segment(segment, n_sub)
    # P x S x 3
    r = points[:, None, :] - mid[None, :, :]
    r_norm = np.linalg.norm(r, axis=-1)
    r_norm = np.maximum(r_norm, 1e-15)
    cross = np.cross(dl[None, :, :], r, axis=-1)
    contrib = MU0_OVER_4PI * current * cross / (r_norm[..., None] ** 3)
    return contrib.sum(axis=1)


def field_from_segments(points: np.ndarray, segments: list[Segment] | tuple[Segment, ...], n_sub: int = 24) -> np.ndarray:
    total = np.zeros((len(points), 3), dtype=float)
    for seg in segments:
        total += segment_field(points, seg, n_sub=n_sub)
    return total


def expand_finite_width_filaments(
    segment: Segment,
    n_width: int = 5,
    n_thickness: int = 3,
    quantize_m: float | None = None,
) -> list[Segment]:
    """Approximate a finite-width conductor by parallel current filaments.

    quantize_m is kept only for reference-sensitivity probes; exp07 no longer
    uses it as a PyPEEC substitute.
    """
    start = np.asarray(segment.start, dtype=float)
    end = np.asarray(segment.end, dtype=float)
    direction = end - start
    norm = np.linalg.norm(direction)
    if norm < 1e-30:
        return [segment]
    direction = direction / norm
    u, v = _orthonormal_cross_section_axes(direction)
    # For horizontal traces, u/v come from the automatic cross-section axes. For a
    # vertical via, this makes a small grid around the via axis.
    w_offsets = np.linspace(-0.5, 0.5, max(1, int(n_width))) * segment.width_m
    t_offsets = np.linspace(-0.5, 0.5, max(1, int(n_thickness))) * segment.thickness_m
    n_total = len(w_offsets) * len(t_offsets)
    out = []
    for i, ow in enumerate(w_offsets):
        for j, ot in enumerate(t_offsets):
            offset = ow * u + ot * v
            s = start + offset
            e = end + offset
            if quantize_m is not None and quantize_m > 0:
                s = np.round(s / quantize_m) * quantize_m
                e = np.round(e / quantize_m) * quantize_m
            out.append(
                Segment(
                    start=tuple(float(x) for x in s),
                    end=tuple(float(x) for x in e),
                    current_a=segment.current_a / n_total,
                    width_m=0.0,
                    thickness_m=0.0,
                    layer=segment.layer,
                    tag=f"{segment.tag}__fw_{i}_{j}",
                )
            )
    return out


def finite_width_segments(
    segments: list[Segment] | tuple[Segment, ...],
    n_width: int = 5,
    n_thickness: int = 3,
    quantize_m: float | None = None,
) -> list[Segment]:
    out: list[Segment] = []
    for seg in segments:
        out.extend(expand_finite_width_filaments(seg, n_width=n_width, n_thickness=n_thickness, quantize_m=quantize_m))
    return out


def reshape_field(flat_field: np.ndarray, grid_shape: tuple[int, int]) -> np.ndarray:
    """Return [3, H, W] from [P, 3]."""
    h, w = grid_shape
    return flat_field.reshape(h, w, 3).transpose(2, 0, 1)


def field_magnitude(B_chw: np.ndarray) -> np.ndarray:
    return np.sqrt(np.sum(B_chw ** 2, axis=0))
