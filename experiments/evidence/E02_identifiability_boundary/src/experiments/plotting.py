"""Plot helpers for exp02."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def save_field_triplet(fields, titles, out_path: Path, extent_um=None, cmap="RdBu_r") -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.9), constrained_layout=True)
    vmax = max(float(np.max(np.abs(f))) for f in fields)
    for ax, field, title in zip(axes, fields, titles):
        im = ax.imshow(field, origin="lower", extent=extent_um, cmap=cmap, vmin=-vmax, vmax=vmax)
        ax.set_title(title)
        ax.set_xlabel("x (µm)")
        ax.set_ylabel("y (µm)")
        fig.colorbar(im, ax=ax, shrink=0.85)
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def save_current_comparison(truth, recon_a, recon_b, out_path: Path, extent_um=None, labels=("Truth", "Bxy", "Bz")) -> None:
    # Plot current magnitude, not vector arrows, to keep the figure readable.
    mags = [np.sqrt(jx**2 + jy**2) for jx, jy in [truth, recon_a, recon_b]]
    vmax = max(float(np.max(m)) for m in mags)
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.9), constrained_layout=True)
    for ax, mag, label in zip(axes, mags, labels):
        im = ax.imshow(mag, origin="lower", extent=extent_um, cmap="magma", vmin=0, vmax=vmax)
        ax.set_title(label)
        ax.set_xlabel("x (µm)")
        ax.set_ylabel("y (µm)")
        fig.colorbar(im, ax=ax, shrink=0.85)
    fig.savefig(out_path, dpi=180)
    plt.close(fig)
