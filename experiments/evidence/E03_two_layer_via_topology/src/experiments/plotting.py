from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def save_bxyz_panels(B_list, titles, x_um, y_um, out_path: Path, scale: float = 1e6):
    comps = ["Bx", "By", "Bz"]
    fig, axes = plt.subplots(3, len(B_list), figsize=(4 * len(B_list), 9), constrained_layout=True)
    if len(B_list) == 1:
        axes = axes[:, None]
    for j, (B, title) in enumerate(zip(B_list, titles)):
        for i in range(3):
            im = axes[i, j].imshow(B[..., i] * scale, origin="lower", extent=[x_um[0], x_um[-1], y_um[0], y_um[-1]], cmap="coolwarm")
            axes[i, j].set_title(f"{title}: {comps[i]} (µT)")
            axes[i, j].set_xlabel("x (µm)")
            axes[i, j].set_ylabel("y (µm)")
            fig.colorbar(im, ax=axes[i, j], fraction=0.046, pad=0.04)
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def save_map_grid(maps, titles, x_um, y_um, out_path: Path, cmap="viridis"):
    n = len(maps)
    cols = min(n, 4)
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3.6 * rows), constrained_layout=True)
    axes = np.atleast_1d(axes).ravel()
    for ax, M, title in zip(axes, maps, titles):
        im = ax.imshow(M, origin="lower", extent=[x_um[0], x_um[-1], y_um[0], y_um[-1]], cmap=cmap)
        ax.set_title(title)
        ax.set_xlabel("x (µm)")
        ax.set_ylabel("y (µm)")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    for ax in axes[n:]:
        ax.axis("off")
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def save_line_plot(x, series, labels, xlabel, ylabel, title, out_path: Path, yscale=None):
    fig, ax = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
    for y, lab in zip(series, labels):
        ax.plot(x, y, marker="o", label=lab)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    if yscale:
        ax.set_yscale(yscale)
    ax.legend()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)
