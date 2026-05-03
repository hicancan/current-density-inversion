"""Finite straight-current-segment Biot-Savart forward model.

This module deliberately starts with finite line segments instead of a neural
network. It implements the minimal physics sanity check required before any
inverse model is trained.

The magnetic field of a finite straight segment from p0 to p1 is computed using
an analytic integral. For a segment direction u, length L, observation point r,
R = r - p0, a = R·u, r_perp = R - a u, rho = |r_perp|, the integral is

    B(r) = mu0 I/(4*pi) * (u × r_perp)
           * [ (L-a)/(rho^2 sqrt(rho^2+(L-a)^2))
               + a/(rho^2 sqrt(rho^2+a^2)) ].

All units are SI.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .constants import MU0, FOUR_PI


@dataclass(frozen=True)
class CurrentSegment:
    """A finite straight current segment.

    Args:
        p0: segment start point [m], shape (3,)
        p1: segment end point [m], shape (3,)
        current: current flowing from p0 to p1 [A]
        name: optional label
    """

    p0: np.ndarray
    p1: np.ndarray
    current: float
    name: str = "segment"

    def __post_init__(self) -> None:
        p0 = np.asarray(self.p0, dtype=float)
        p1 = np.asarray(self.p1, dtype=float)
        if p0.shape != (3,) or p1.shape != (3,):
            raise ValueError("p0 and p1 must have shape (3,)")
        if np.allclose(p0, p1):
            raise ValueError("segment endpoints must not coincide")
        object.__setattr__(self, "p0", p0)
        object.__setattr__(self, "p1", p1)

    @property
    def length(self) -> float:
        return float(np.linalg.norm(self.p1 - self.p0))

    @property
    def unit(self) -> np.ndarray:
        return (self.p1 - self.p0) / self.length


def b_field_from_segment(
    points: np.ndarray,
    segment: CurrentSegment,
    min_rho: float = 1.0e-12,
) -> np.ndarray:
    """Compute B field from one finite segment at observation points.

    Args:
        points: observation points, shape (..., 3), SI meters.
        segment: CurrentSegment.
        min_rho: floor for perpendicular distance to avoid singular numerical
            overflow exactly on the wire.

    Returns:
        B field array with shape (..., 3), SI tesla.
    """
    pts = np.asarray(points, dtype=float)
    if pts.shape[-1] != 3:
        raise ValueError("points must have shape (..., 3)")

    p0 = segment.p0
    u = segment.unit
    L = segment.length
    I = segment.current

    R = pts - p0  # (..., 3)
    a = np.sum(R * u, axis=-1, keepdims=True)  # (..., 1)
    r_perp = R - a * u
    rho2 = np.sum(r_perp * r_perp, axis=-1)
    rho2_safe = np.maximum(rho2, min_rho**2)

    a_scalar = a[..., 0]
    term1 = (L - a_scalar) / (rho2_safe * np.sqrt(rho2_safe + (L - a_scalar) ** 2))
    term2 = a_scalar / (rho2_safe * np.sqrt(rho2_safe + a_scalar**2))
    integral = term1 + term2  # (...,)

    cross = np.cross(u, r_perp)  # (..., 3)
    B = (MU0 * I / FOUR_PI) * cross * integral[..., None]

    # Observation exactly on segment is singular; if users accidentally query
    # the wire centerline, we return finite values at min_rho. This experiment
    # always places the measurement plane above the current sources.
    return B


def b_field_from_segments(
    points: np.ndarray,
    segments: list[CurrentSegment],
    min_rho: float = 1.0e-12,
) -> np.ndarray:
    """Sum B fields from many finite segments."""
    if not segments:
        raise ValueError("segments list must not be empty")
    B = np.zeros_like(points, dtype=float)
    for seg in segments:
        B += b_field_from_segment(points, seg, min_rho=min_rho)
    return B


def make_straight_wire(
    length: float,
    current: float,
    axis: str = "x",
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
    name: str = "straight_wire",
) -> list[CurrentSegment]:
    """Create one finite straight wire centered at center."""
    c = np.asarray(center, dtype=float)
    half = length / 2.0
    if axis == "x":
        p0 = c + np.array([-half, 0.0, 0.0])
        p1 = c + np.array([half, 0.0, 0.0])
    elif axis == "y":
        p0 = c + np.array([0.0, -half, 0.0])
        p1 = c + np.array([0.0, half, 0.0])
    elif axis == "z":
        p0 = c + np.array([0.0, 0.0, -half])
        p1 = c + np.array([0.0, 0.0, half])
    else:
        raise ValueError("axis must be one of {'x', 'y', 'z'}")
    return [CurrentSegment(p0=p0, p1=p1, current=current, name=name)]


def make_rect_loop(
    width: float,
    height: float,
    current: float,
    z: float = 0.0,
    center: tuple[float, float] = (0.0, 0.0),
    clockwise: bool = False,
) -> list[CurrentSegment]:
    """Create a rectangular current loop in the z plane.

    Args:
        width: x-size [m]
        height: y-size [m]
        current: loop current [A]
        z: loop plane z [m]
        center: loop center [m]
        clockwise: current orientation when viewed from +z.
    """
    cx, cy = center
    x0, x1 = cx - width / 2.0, cx + width / 2.0
    y0, y1 = cy - height / 2.0, cy + height / 2.0
    pts_ccw = [
        np.array([x0, y0, z]),
        np.array([x1, y0, z]),
        np.array([x1, y1, z]),
        np.array([x0, y1, z]),
    ]
    if clockwise:
        pts = list(reversed(pts_ccw))
    else:
        pts = pts_ccw
    segments: list[CurrentSegment] = []
    for idx in range(4):
        segments.append(
            CurrentSegment(
                p0=pts[idx],
                p1=pts[(idx + 1) % 4],
                current=current,
                name=f"rect_loop_{idx}",
            )
        )
    return segments


def make_vertical_via(
    z0: float,
    z1: float,
    current: float,
    xy: tuple[float, float] = (0.0, 0.0),
    name: str = "vertical_via",
) -> list[CurrentSegment]:
    """Create a vertical current segment representing a via.

    Current flows from z0 to z1 at fixed (x,y). Use z1 > z0 for upward current.
    """
    x, y = xy
    return [
        CurrentSegment(
            p0=np.array([x, y, z0], dtype=float),
            p1=np.array([x, y, z1], dtype=float),
            current=current,
            name=name,
        )
    ]
