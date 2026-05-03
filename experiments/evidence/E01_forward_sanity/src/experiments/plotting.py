"""Plot helpers for experiment outputs."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def component_heatmaps(
    x: np.ndarray,
    y: np.ndarray,
    B: np.ndarray,
    title: str,
    path: str | Path,
    unit_scale: float = 1.0e6,
    unit_label: str = "µT",
) -> None:
    """Save Bx/By/Bz heatmaps."""
    comps = ["Bx", "By", "Bz"]
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), constrained_layout=True)
    extent = [x.min() * 1e3, x.max() * 1e3, y.min() * 1e3, y.max() * 1e3]
    for idx, ax in enumerate(axes):
        data = B[..., idx] * unit_scale
        vmax = np.nanmax(np.abs(data))
        if vmax == 0 or not np.isfinite(vmax):
            vmax = 1.0
        im = ax.imshow(
            data,
            origin="lower",
            extent=extent,
            cmap="coolwarm",
            vmin=-vmax,
            vmax=vmax,
            interpolation="nearest",
        )
        ax.set_title(comps[idx])
        ax.set_xlabel("x [mm]")
        ax.set_ylabel("y [mm]")
        fig.colorbar(im, ax=ax, label=unit_label)
    fig.suptitle(title)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def line_plot(xs: np.ndarray, ys: list[np.ndarray], labels: list[str], title: str, xlabel: str, ylabel: str, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    for y, label in zip(ys, labels):
        ax.plot(xs, y, label=label)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.savefig(path, dpi=200)
    plt.close(fig)
