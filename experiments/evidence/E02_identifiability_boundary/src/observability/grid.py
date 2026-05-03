"""Grid and spectral utility functions."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Grid2D:
    """Uniform 2D grid on a square field of view."""

    n: int
    fov_m: float

    @property
    def dx(self) -> float:
        return self.fov_m / self.n

    @property
    def extent_um(self) -> tuple[float, float, float, float]:
        half = self.fov_m * 0.5 * 1e6
        return (-half, half, -half, half)

    def coordinates(self) -> tuple[np.ndarray, np.ndarray]:
        x = (np.arange(self.n) - self.n / 2) * self.dx
        y = (np.arange(self.n) - self.n / 2) * self.dx
        return np.meshgrid(x, y, indexing="xy")

    def angular_frequencies(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        k = 2.0 * np.pi * np.fft.fftfreq(self.n, d=self.dx)
        kx, ky = np.meshgrid(k, k, indexing="xy")
        kmag = np.sqrt(kx**2 + ky**2)
        return kx, ky, kmag


def center_crop(arr: np.ndarray, n_crop: int) -> np.ndarray:
    """Center crop the last two dimensions of an array."""
    if arr.shape[-1] < n_crop or arr.shape[-2] < n_crop:
        raise ValueError("crop size exceeds array shape")
    y0 = (arr.shape[-2] - n_crop) // 2
    x0 = (arr.shape[-1] - n_crop) // 2
    return arr[..., y0 : y0 + n_crop, x0 : x0 + n_crop]
