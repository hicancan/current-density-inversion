"""Canonical validation geometry generators.

Produces deterministic generated-geometry families as specified in E25 §5:
straight strip, parallel strips, rectangular loop, vertical via,
two-layer trace with return, four-layer via-return motif.

All coordinates in SI meters.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class RectConductor:
    """Rectangular cross-section conductor segment.

    Args:
        p0, p1: segment endpoints along centerline [m], shape (3,).
        width: cross-section width (in-plane, perpendicular to tangent) [m].
        thickness: cross-section thickness (out-of-plane) [m].
        current: current [A] flowing from p0 to p1.
        layer: layer label.
        tag: human-readable identifier.
    """
    p0: np.ndarray
    p1: np.ndarray
    width: float
    thickness: float
    current: float
    layer: str = "L1"
    tag: str = "cond"

    def __post_init__(self) -> None:
        for attr in ("p0", "p1"):
            arr = np.asarray(getattr(self, attr), dtype=float)
            if arr.shape != (3,):
                raise ValueError(f"{attr} must have shape (3,)")
            object.__setattr__(self, attr, arr)
        for attr in ("width", "thickness"):
            if getattr(self, attr) < 0:
                raise ValueError(f"{attr} must be non-negative")
        if getattr(self, "current") == 0:
            raise ValueError("current must be non-zero")

    @property
    def length(self) -> float:
        return float(np.linalg.norm(self.p1 - self.p0))

    @property
    def tangent(self) -> np.ndarray:
        L = self.length
        if L < 1e-30:
            raise ValueError("zero-length conductor")
        return (self.p1 - self.p0) / L

    @property
    def cross_section_area(self) -> float:
        return self.width * self.thickness

    @property
    def current_density(self) -> float:
        return self.current / self.cross_section_area

    def cross_section_axes(self) -> tuple[np.ndarray, np.ndarray]:
        """Return orthonormal axes (u, v) spanning the cross-section plane.

        u is approximately in the xy-plane; v is out-of-plane.
        """
        t = self.tangent
        z_axis = np.array([0.0, 0.0, 1.0])
        x_axis = np.array([1.0, 0.0, 0.0])
        seed = z_axis if abs(float(np.dot(t, z_axis))) < 0.92 else x_axis
        u = np.cross(t, seed)
        u = u / (np.linalg.norm(u) + 1e-30)
        v = np.cross(t, u)
        v = v / (np.linalg.norm(v) + 1e-30)
        return u, v


# ---------------------------------------------------------------------------
# Canonical geometry families
# ---------------------------------------------------------------------------

def make_straight_strip(
    length: float = 1e-3,
    width: float = 4e-5,
    thickness: float = 1e-5,
    current: float = 1e-3,
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
    direction: str = "x",
) -> list[RectConductor]:
    """Single straight rectangular conductor."""
    c = np.asarray(center, dtype=float)
    half = length / 2.0
    if direction == "x":
        p0 = c + np.array([-half, 0.0, 0.0])
        p1 = c + np.array([half, 0.0, 0.0])
    elif direction == "y":
        p0 = c + np.array([0.0, -half, 0.0])
        p1 = c + np.array([0.0, half, 0.0])
    else:
        raise ValueError("direction must be 'x' or 'y' for horizontal strips")
    return [RectConductor(p0=p0, p1=p1, width=width, thickness=thickness,
                          current=current, tag="straight_strip")]


def make_parallel_strips(
    length: float = 1e-3,
    width: float = 4e-5,
    thickness: float = 1e-5,
    current: float = 1e-3,
    spacing: float = 2e-4,
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> list[RectConductor]:
    """Two parallel strips with opposite currents (forward and return)."""
    c = np.asarray(center, dtype=float)
    half = length / 2.0
    hs = spacing / 2.0
    c1 = c + np.array([0.0, hs, 0.0])
    c2 = c + np.array([0.0, -hs, 0.0])
    return [
        RectConductor(
            p0=c1 + np.array([-half, 0.0, 0.0]),
            p1=c1 + np.array([half, 0.0, 0.0]),
            width=width, thickness=thickness,
            current=current, tag="parallel_strip_fwd",
        ),
        RectConductor(
            p0=c2 + np.array([-half, 0.0, 0.0]),
            p1=c2 + np.array([half, 0.0, 0.0]),
            width=width, thickness=thickness,
            current=-current, tag="parallel_strip_ret",
        ),
    ]


def make_rectangular_loop(
    width_x: float = 5e-4,
    height_y: float = 5e-4,
    trace_width: float = 4e-5,
    thickness: float = 1e-5,
    current: float = 1e-3,
    z: float = 0.0,
    center: tuple[float, float] = (0.0, 0.0),
) -> list[RectConductor]:
    """Rectangular current loop in the xy-plane."""
    cx, cy = center
    x0, x1 = cx - width_x / 2.0, cx + width_x / 2.0
    y0, y1 = cy - height_y / 2.0, cy + height_y / 2.0

    corners = [
        np.array([x0, y0, z]),
        np.array([x1, y0, z]),
        np.array([x1, y1, z]),
        np.array([x0, y1, z]),
    ]
    segments = []
    for idx in range(4):
        p0 = corners[idx]
        p1 = corners[(idx + 1) % 4]
        # Width convention: for y-directed segments swap
        w = trace_width
        segments.append(RectConductor(
            p0=p0, p1=p1,
            width=w, thickness=thickness,
            current=current, tag=f"rect_loop_{idx}",
        ))
    return segments


def make_vertical_via(
    z0: float = -5e-5,
    z1: float = 5e-5,
    radius: float = 2e-5,
    current: float = 1e-3,
    xy: tuple[float, float] = (0.0, 0.0),
) -> list[RectConductor]:
    """Vertical via approximated as a square cross-section conductor.

    Circular via is approximated with an equivalent square of side
    sqrt(pi)*radius so the cross-section area matches.
    """
    x, y = xy
    eq_side = np.sqrt(np.pi) * radius  # equal area
    return [RectConductor(
        p0=np.array([x, y, z0], dtype=float),
        p1=np.array([x, y, z1], dtype=float),
        width=eq_side, thickness=eq_side,
        current=current, tag="vertical_via",
    )]


def make_two_layer_trace_with_return(
    length: float = 1e-3,
    width: float = 4e-5,
    thickness: float = 1e-5,
    current: float = 1e-3,
    layer_gap: float = 5e-5,
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> list[RectConductor]:
    """Two-layer trace: forward current on L1, return on L2 with vias."""
    c = np.asarray(center, dtype=float)
    half = length / 2.0
    z_top = c[2] + layer_gap / 2.0
    z_bot = c[2] - layer_gap / 2.0

    conductors: list[RectConductor] = []
    # Top trace (forward)
    conductors.append(RectConductor(
        p0=np.array([c[0] - half, c[1], z_top]),
        p1=np.array([c[0] + half, c[1], z_top]),
        width=width, thickness=thickness,
        current=current, layer="L1", tag="trace_top_fwd",
    ))
    # Bottom trace (return)
    conductors.append(RectConductor(
        p0=np.array([c[0] + half, c[1], z_bot]),
        p1=np.array([c[0] - half, c[1], z_bot]),
        width=width, thickness=thickness,
        current=current, layer="L2", tag="trace_bot_ret",
    ))
    # Via at +x end (downward)
    conductors.append(RectConductor(
        p0=np.array([c[0] + half, c[1], z_top]),
        p1=np.array([c[0] + half, c[1], z_bot]),
        width=width, thickness=thickness,
        current=current, layer="via", tag="via_pos_x",
    ))
    # Via at -x end (upward)
    conductors.append(RectConductor(
        p0=np.array([c[0] - half, c[1], z_bot]),
        p1=np.array([c[0] - half, c[1], z_top]),
        width=width, thickness=thickness,
        current=current, layer="via", tag="via_neg_x",
    ))
    return conductors


def make_four_layer_via_return_motif(
    length: float = 1e-3,
    width: float = 4e-5,
    thickness: float = 1e-5,
    current: float = 1e-3,
    layer_gap: float = 5e-5,
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> list[RectConductor]:
    """Four-layer via-return motif:
    L1: forward, L2: return, L3: forward, L4: return
    connected by vias forming a folded path.
    """
    c = np.asarray(center, dtype=float)
    half = length / 2.0
    dz = layer_gap
    z = [c[2] + 1.5 * dz, c[2] + 0.5 * dz, c[2] - 0.5 * dz, c[2] - 1.5 * dz]

    conductors: list[RectConductor] = []
    # L1 trace: -x to +x
    conductors.append(RectConductor(
        p0=np.array([c[0] - half, c[1], z[0]]),
        p1=np.array([c[0] + half, c[1], z[0]]),
        width=width, thickness=thickness,
        current=current, layer="L1", tag="L1_fwd",
    ))
    # via L1->L2 at +x (down)
    conductors.append(RectConductor(
        p0=np.array([c[0] + half, c[1], z[0]]),
        p1=np.array([c[0] + half, c[1], z[1]]),
        width=width, thickness=thickness,
        current=current, layer="via12", tag="via_L1L2",
    ))
    # L2 trace: +x to -x
    conductors.append(RectConductor(
        p0=np.array([c[0] + half, c[1], z[1]]),
        p1=np.array([c[0] - half, c[1], z[1]]),
        width=width, thickness=thickness,
        current=current, layer="L2", tag="L2_ret",
    ))
    # via L2->L3 at -x (down)
    conductors.append(RectConductor(
        p0=np.array([c[0] - half, c[1], z[1]]),
        p1=np.array([c[0] - half, c[1], z[2]]),
        width=width, thickness=thickness,
        current=current, layer="via23", tag="via_L2L3",
    ))
    # L3 trace: -x to +x
    conductors.append(RectConductor(
        p0=np.array([c[0] - half, c[1], z[2]]),
        p1=np.array([c[0] + half, c[1], z[2]]),
        width=width, thickness=thickness,
        current=current, layer="L3", tag="L3_fwd",
    ))
    # via L3->L4 at +x (down)
    conductors.append(RectConductor(
        p0=np.array([c[0] + half, c[1], z[2]]),
        p1=np.array([c[0] + half, c[1], z[3]]),
        width=width, thickness=thickness,
        current=current, layer="via34", tag="via_L3L4",
    ))
    # L4 trace: +x to -x
    conductors.append(RectConductor(
        p0=np.array([c[0] + half, c[1], z[3]]),
        p1=np.array([c[0] - half, c[1], z[3]]),
        width=width, thickness=thickness,
        current=current, layer="L4", tag="L4_ret",
    ))
    return conductors


# ---------------------------------------------------------------------------
# Observation grid
# ---------------------------------------------------------------------------

def make_observation_grid(
    n: int = 21,
    fov_m: float = 1.2e-3,
    z_m: float = 8e-5,
) -> np.ndarray:
    """Uniform 2D observation grid at height z_m above origin.

    Returns array of shape (n*n, 3) with observation points in SI meters.
    """
    xs = np.linspace(-fov_m / 2, fov_m / 2, n)
    ys = np.linspace(-fov_m / 2, fov_m / 2, n)
    X, Y = np.meshgrid(xs, ys)
    pts = np.stack([X.ravel(), Y.ravel(), np.full_like(X.ravel(), z_m)], axis=-1)
    return pts
