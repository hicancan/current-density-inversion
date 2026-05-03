"""Measurement grid helpers."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class XYGrid:
    """A planar measurement grid at constant z.

    Attributes:
        x: 2D array of x coordinates [m]
        y: 2D array of y coordinates [m]
        z: 2D array of z coordinates [m]
        points: array with shape (ny, nx, 3), observation positions [m]
    """

    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    points: np.ndarray

    @property
    def shape(self) -> tuple[int, int]:
        return self.x.shape

    @property
    def dx(self) -> float:
        if self.x.shape[1] < 2:
            return float("nan")
        return float(self.x[0, 1] - self.x[0, 0])

    @property
    def dy(self) -> float:
        if self.y.shape[0] < 2:
            return float("nan")
        return float(self.y[1, 0] - self.y[0, 0])


def make_xy_grid(
    fov_x: float,
    fov_y: float,
    nx: int,
    ny: int,
    z: float,
    center: tuple[float, float] = (0.0, 0.0),
) -> XYGrid:
    """Create a planar measurement grid.

    Args:
        fov_x: field of view in x [m]
        fov_y: field of view in y [m]
        nx: number of pixels along x
        ny: number of pixels along y
        z: constant measurement height [m]
        center: grid center (x0, y0) [m]

    Returns:
        XYGrid instance.
    """
    if nx < 2 or ny < 2:
        raise ValueError("nx and ny must be at least 2")
    cx, cy = center
    xs = np.linspace(cx - fov_x / 2.0, cx + fov_x / 2.0, nx)
    ys = np.linspace(cy - fov_y / 2.0, cy + fov_y / 2.0, ny)
    xx, yy = np.meshgrid(xs, ys, indexing="xy")
    zz = np.full_like(xx, z, dtype=float)
    pts = np.stack([xx, yy, zz], axis=-1)
    return XYGrid(x=xx, y=yy, z=zz, points=pts)
