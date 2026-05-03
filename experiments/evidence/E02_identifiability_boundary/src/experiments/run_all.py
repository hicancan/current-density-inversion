"""Run all observability and Bxy-vs-Bz experiments.

This script intentionally keeps the experiment self-contained so the folder can
be copied into a claim-scoped evidence package and reproduced.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys

# Matplotlib may otherwise try to write a cache under a non-writable home in
# some managed environments.
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-exp02")

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from observability.grid import Grid2D, center_crop
from observability.spectral import (
    streamfunction_current,
    forward_sheet_fft,
    inverse_bxy_fft,
    inverse_bz_fft,
    add_noise_like,
    relative_l2,
    attenuation_for_feature,
    recoverable_feature_size,
)
from experiments.plotting import save_field_triplet, save_current_comparison


def ensure_dirs() -> tuple[Path, Path]:
    outputs = ROOT / "outputs"
    data = ROOT / "data"
    outputs.mkdir(exist_ok=True)
    data.mkdir(exist_ok=True)
    return outputs, data


def plot_decay_curves(outputs: Path) -> dict:
    feature_um = np.logspace(np.log10(1.0), np.log10(5000.0), 500)
    feature_m = feature_um * 1e-6
    standoffs_um = [5, 10, 25, 50, 100, 250, 500]
    thresholds = [1e-1, 1e-2, 1e-3]

    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for z_um in standoffs_um:
        att = attenuation_for_feature(feature_m, z_um * 1e-6)
        ax.semilogx(feature_um, np.maximum(att, 1e-12), label=f"z={z_um} µm")
    for th in thresholds:
        ax.axhline(th, color="k", linestyle="--", linewidth=0.8, alpha=0.45)
        ax.text(feature_um[-1], th, f"  {th:g}", va="center", fontsize=8)
    ax.set_xlabel("feature size λ (µm), with k=2π/λ")
    ax.set_ylabel("field transfer |B(k)| / |J(k)| up to constant = exp(-kz)")
    ax.set_title("Near-field low-pass attenuation versus feature size")
    ax.set_ylim(1e-5, 1.05)
    ax.set_yscale("log")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(ncol=2, fontsize=8)
    fig.savefig(outputs / "01_standoff_feature_attenuation.png", dpi=180)
    plt.close(fig)

    table = {}
    for z_um in standoffs_um:
        table[f"z_{z_um}_um"] = {
            f"lambda_at_attenuation_{th:g}_um": recoverable_feature_size(z_um * 1e-6, th) * 1e6
            for th in thresholds
        }
    return table


def plot_recoverable_heatmap(outputs: Path) -> None:
    z_um = np.linspace(1, 500, 240)
    lam_um = np.logspace(np.log10(1), np.log10(5000), 260)
    Z, L = np.meshgrid(z_um, lam_um, indexing="ij")
    att = np.exp(-2 * np.pi * Z / L)
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    im = ax.pcolormesh(lam_um, z_um, np.log10(np.maximum(att, 1e-12)), shading="auto", cmap="viridis", vmin=-5, vmax=0)
    ax.set_xscale("log")
    ax.set_xlabel("feature size λ (µm)")
    ax.set_ylabel("standoff z (µm)")
    ax.set_title("Observability map: log10 exp(-2πz/λ)")
    cb = fig.colorbar(im, ax=ax)
    cb.set_label("log10 attenuation")
    cs = ax.contour(lam_um, z_um, att, levels=[1e-3, 1e-2, 1e-1], colors="white", linewidths=0.8)
    ax.clabel(cs, fmt="%.0e", fontsize=8)
    fig.savefig(outputs / "02_observability_heatmap.png", dpi=180)
    plt.close(fig)


def plot_inverse_gain(outputs: Path) -> None:
    lam_um = np.logspace(np.log10(2), np.log10(5000), 500)
    k = 2 * np.pi / (lam_um * 1e-6)
    standoffs_um = [10, 50, 100, 500]
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for z_um in standoffs_um:
        log10_gain = (k * z_um * 1e-6) / np.log(10)
        ax.semilogx(lam_um, np.minimum(log10_gain, 12), label=f"z={z_um} µm")
    ax.set_xlabel("feature size λ (µm)")
    ax.set_ylabel("log10 inverse amplification exp(kz)")
    ax.set_title("Why high spatial frequencies become unstable in inversion")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    fig.savefig(outputs / "03_inverse_amplification.png", dpi=180)
    plt.close(fig)


def full_field_inversion(outputs: Path, data: Path) -> dict:
    grid = Grid2D(n=128, fov_m=1.0e-3)
    jx, jy, psi = streamfunction_current(grid, seed=11)
    h = 50e-6
    bx, by, bz = forward_sheet_fft(jx, jy, grid, h)
    j_bxy = inverse_bxy_fft(bx, by, grid, h)
    j_bz = inverse_bz_fft(bz, grid, h)
    err_bxy = relative_l2(j_bxy, (jx, jy))
    err_bz = relative_l2(j_bz, (jx, jy))

    save_field_triplet(
        (bx * 1e6, by * 1e6, bz * 1e6),
        ("Bx (µT)", "By (µT)", "Bz (µT)"),
        outputs / "04_forward_Bxyz_from_sheet_current.png",
        extent_um=grid.extent_um,
    )
    save_current_comparison(
        (jx, jy),
        j_bxy,
        j_bz,
        outputs / "05_full_field_reconstruction_clean.png",
        extent_um=grid.extent_um,
        labels=("Truth |J|", f"Bxy inverse |J|\nrelL2={err_bxy:.2e}", f"Bz inverse |J|\nrelL2={err_bz:.2e}"),
    )

    np.savez_compressed(
        data / "full_field_streamfunction_example.npz",
        jx=jx,
        jy=jy,
        psi=psi,
        bx=bx,
        by=by,
        bz=bz,
        jx_bxy=j_bxy[0],
        jy_bxy=j_bxy[1],
        jx_bz=j_bz[0],
        jy_bz=j_bz[1],
    )
    return {"rel_l2_bxy_clean_full": err_bxy, "rel_l2_bz_clean_full": err_bz}


def finite_fov_experiment(outputs: Path, data: Path) -> dict:
    # Generate a localized source on a large domain and crop the field. The crop
    # contains the current source but not all long-range magnetic-field tails.
    large = Grid2D(n=256, fov_m=4.0e-3)
    crop_n = 128
    small = Grid2D(n=crop_n, fov_m=large.fov_m * crop_n / large.n)
    jx_large, jy_large, _ = streamfunction_current(large, seed=31)

    # Taper current to the center so the cropped truth is meaningful.
    x, y = large.coordinates()
    taper = np.exp(-((x / (0.70e-3)) ** 8 + (y / (0.70e-3)) ** 8))
    jx_large *= taper
    jy_large *= taper

    h = 50e-6
    bx_large, by_large, bz_large = forward_sheet_fft(jx_large, jy_large, large, h)

    jx_crop = center_crop(jx_large, crop_n)
    jy_crop = center_crop(jy_large, crop_n)
    bx_crop = center_crop(bx_large, crop_n)
    by_crop = center_crop(by_large, crop_n)
    bz_crop = center_crop(bz_large, crop_n)

    # Invert as if the crop were the whole measured world. Use a conservative
    # recovery bandwidth to avoid purely numerical high-k explosions.
    k_cut = 2 * np.pi / (8 * small.dx)
    j_bxy = inverse_bxy_fft(bx_crop, by_crop, small, h, k_cut_rad_per_m=k_cut)
    j_bz = inverse_bz_fft(bz_crop, small, h, k_cut_rad_per_m=k_cut)
    err_bxy = relative_l2(j_bxy, (jx_crop, jy_crop))
    err_bz = relative_l2(j_bz, (jx_crop, jy_crop))

    save_current_comparison(
        (jx_crop, jy_crop),
        j_bxy,
        j_bz,
        outputs / "06_finite_fov_truncation_bxy_vs_bz.png",
        extent_um=small.extent_um,
        labels=("Truth crop |J|", f"Bxy inverse crop\nrelL2={err_bxy:.3f}", f"Bz inverse crop\nrelL2={err_bz:.3f}"),
    )

    errmap_bxy = np.sqrt((j_bxy[0] - jx_crop) ** 2 + (j_bxy[1] - jy_crop) ** 2)
    errmap_bz = np.sqrt((j_bz[0] - jx_crop) ** 2 + (j_bz[1] - jy_crop) ** 2)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4), constrained_layout=True)
    vmax = max(float(np.max(errmap_bxy)), float(np.max(errmap_bz)))
    for ax, emap, title in zip(axes, [errmap_bxy, errmap_bz], ["Bxy error", "Bz error"]):
        im = ax.imshow(emap, origin="lower", extent=small.extent_um, cmap="inferno", vmin=0, vmax=vmax)
        ax.set_title(title)
        ax.set_xlabel("x (µm)")
        ax.set_ylabel("y (µm)")
        fig.colorbar(im, ax=ax, shrink=0.85)
    fig.savefig(outputs / "07_finite_fov_error_maps.png", dpi=180)
    plt.close(fig)

    np.savez_compressed(
        data / "finite_fov_crop_experiment.npz",
        jx_truth=jx_crop,
        jy_truth=jy_crop,
        bx=bx_crop,
        by=by_crop,
        bz=bz_crop,
        jx_bxy=j_bxy[0],
        jy_bxy=j_bxy[1],
        jx_bz=j_bz[0],
        jy_bz=j_bz[1],
    )
    return {"rel_l2_bxy_finite_fov": err_bxy, "rel_l2_bz_finite_fov": err_bz}


def noise_standoff_experiment(outputs: Path) -> dict:
    grid = Grid2D(n=128, fov_m=1.0e-3)
    jx, jy, _ = streamfunction_current(grid, seed=19)
    rng = np.random.default_rng(123)
    standoffs_um = np.array([10, 25, 50, 100, 200])
    noise_levels = np.array([0.0, 0.002, 0.005, 0.01, 0.02])
    err_bxy = np.zeros((len(standoffs_um), len(noise_levels)))
    err_bz = np.zeros_like(err_bxy)

    # Regularized recovery bandwidth: only invert spatial wavelengths >= 100 µm.
    # exp02 is about observability, so this bandwidth is intentionally explicit.
    k_cut = 2 * np.pi / (100e-6)
    for i, z_um in enumerate(standoffs_um):
        bx, by, bz = forward_sheet_fft(jx, jy, grid, z_um * 1e-6)
        for j, nl in enumerate(noise_levels):
            bx_n = add_noise_like(bx, nl, rng)
            by_n = add_noise_like(by, nl, rng)
            bz_n = add_noise_like(bz, nl, rng)
            j_bxy = inverse_bxy_fft(bx_n, by_n, grid, z_um * 1e-6, k_cut_rad_per_m=k_cut)
            j_bz = inverse_bz_fft(bz_n, grid, z_um * 1e-6, k_cut_rad_per_m=k_cut)
            err_bxy[i, j] = relative_l2(j_bxy, (jx, jy))
            err_bz[i, j] = relative_l2(j_bz, (jx, jy))

    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for j, nl in enumerate(noise_levels):
        ax.plot(standoffs_um, err_bxy[:, j], "o-", label=f"Bxy noise={nl:g}")
        ax.plot(standoffs_um, err_bz[:, j], "s--", label=f"Bz noise={nl:g}")
    ax.set_xlabel("standoff z (µm)")
    ax.set_ylabel("relative L2 reconstruction error")
    ax.set_title("Noise and standoff sensitivity under λ≥100 µm recovery bandwidth")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=7, ncol=2)
    fig.savefig(outputs / "08_noise_standoff_error_scan.png", dpi=180)
    plt.close(fig)

    return {
        "standoffs_um": standoffs_um.tolist(),
        "noise_levels_relative_to_max_field": noise_levels.tolist(),
        "regularized_recovery_min_wavelength_um": 100.0,
        "rel_l2_bxy_noise_scan": err_bxy.tolist(),
        "rel_l2_bz_noise_scan": err_bz.tolist(),
    }


def two_layer_single_plane_rank_gate(outputs: Path) -> dict:
    """Show why one measurement plane cannot unmix two unconstrained layers.

    For a divergence-free Fourier mode, every magnetic component receives the
    same modal direction from each layer, only scaled by exp(-k z_l). Therefore
    the two layer columns are collinear at each k. More components improve SNR
    but do not create independent layer labels by themselves.
    """
    feature_um = np.array([40.0, 80.0, 160.0, 320.0, 640.0])
    standoff_um = 50.0
    layer_depths_um = np.array([50.0, 130.0])
    total_z_um = standoff_um + layer_depths_um
    k = 2.0 * np.pi / (feature_um * 1e-6)
    shallow = np.exp(-k * total_z_um[0] * 1e-6)
    deep = np.exp(-k * total_z_um[1] * 1e-6)
    deep_to_shallow = deep / (shallow + 1e-30)

    # A scalar modal layer-unmixing matrix has one row and two layer columns.
    # Its smallest singular value is exactly zero.
    ranks = []
    smins = []
    smaxs = []
    for a, b in zip(shallow, deep):
        A = np.array([[a, b]], dtype=float)
        s = np.linalg.svd(A, compute_uv=False)
        ranks.append(int(np.linalg.matrix_rank(A, tol=1e-14)))
        smaxs.append(float(s[0]))
        smins.append(0.0)

    fig, ax = plt.subplots(figsize=(7.5, 4.5), constrained_layout=True)
    ax.semilogx(feature_um, deep_to_shallow, "o-")
    ax.set_xlabel("feature size lambda (um)")
    ax.set_ylabel("deep/shallow response amplitude")
    ax.set_title("Single-plane two-layer mixing: depth changes amplitude, not modal direction")
    ax.grid(True, which="both", alpha=0.3)
    fig.savefig(outputs / "09_two_layer_single_plane_rank_deficiency.png", dpi=180)
    plt.close(fig)

    return {
        "standoff_um": standoff_um,
        "layer_depths_um": layer_depths_um.tolist(),
        "feature_um": feature_um.tolist(),
        "deep_to_shallow_response_ratio": deep_to_shallow.tolist(),
        "rank_per_feature": ranks,
        "smallest_singular_value_per_feature": smins,
        "largest_singular_value_per_feature": smaxs,
        "single_plane_two_layer_rank_deficient": all(r == 1 for r in ranks),
        "interpretation": "single-plane Bxyz improves modal SNR but does not by itself identify layer labels without extra priors or measurements",
    }


def add_acceptance_gates(metrics: dict) -> None:
    gates = {
        "clean_full_field_bxy_inverse_is_self_consistent": {
            "threshold": "relative_l2 < 1e-4",
            "value": metrics["rel_l2_bxy_clean_full"],
            "pass": metrics["rel_l2_bxy_clean_full"] < 1e-4,
        },
        "clean_full_field_bz_inverse_is_self_consistent_except_dc": {
            "threshold": "relative_l2 < 1e-3",
            "value": metrics["rel_l2_bz_clean_full"],
            "pass": metrics["rel_l2_bz_clean_full"] < 1e-3,
        },
        "finite_fov_damages_bz_more_than_bxy": {
            "threshold": "Bz finite-FOV error > 5x Bxy finite-FOV error",
            "value": metrics["rel_l2_bz_finite_fov"] / (metrics["rel_l2_bxy_finite_fov"] + 1e-30),
            "pass": metrics["rel_l2_bz_finite_fov"] > 5.0 * metrics["rel_l2_bxy_finite_fov"],
        },
        "two_layer_single_plane_is_rank_deficient": {
            "threshold": "rank_per_feature all equal 1",
            "value": metrics["two_layer_single_plane_rank_gate"]["rank_per_feature"],
            "pass": metrics["two_layer_single_plane_rank_gate"]["single_plane_two_layer_rank_deficient"],
        },
    }
    metrics["acceptance_gates"] = gates
    metrics["all_acceptance_gates_passed"] = all(g["pass"] for g in gates.values())


def write_run_report(outputs: Path, metrics: dict) -> None:
    gates = "\n".join(
        f"- {name}: {'PASS' if gate['pass'] else 'FAIL'}; value={gate['value']}; threshold={gate['threshold']}"
        for name, gate in metrics["acceptance_gates"].items()
    )
    report = f"""# exp02 Run Report

## Role

MVP-1 observability calculator and single-layer Fourier inversion sanity check.
It defines recoverable spatial scales before any neural inverse model is trained.

## Gate Summary

Overall: {'PASS' if metrics['all_acceptance_gates_passed'] else 'FAIL'}

{gates}

## Key Results

- clean full-field Bxy inversion relative L2: `{metrics['rel_l2_bxy_clean_full']:.2e}`
- clean full-field Bz inversion relative L2: `{metrics['rel_l2_bz_clean_full']:.2e}`
- finite-FOV Bxy inversion relative L2: `{metrics['rel_l2_bxy_finite_fov']:.2e}`
- finite-FOV Bz inversion relative L2: `{metrics['rel_l2_bz_finite_fov']:.2e}`
- two-layer single-plane rank gate: `rank deficient`

## Boundary

The thin-sheet Fourier operator is an ideal free-space model. Multilayer
separation still requires topology, masks, multiple measurements, or other
priors; Bxyz alone on one plane does not label layers.
"""
    (outputs / "RUN_REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    outputs, data = ensure_dirs()
    metrics = {
        "experiment": "exp02-observability-and-bxy-vs-bz",
        "units": {
            "length": "m internally; figures use micrometres",
            "magnetic_field": "T internally; some figures use microtesla",
            "sheet_current": "A/m arbitrary scale in examples",
        },
        "notes": [
            "This experiment is a theoretical observability and single-layer Fourier inversion check, not a neural network experiment.",
            "Bxy and Bz inversions use the ideal thin-sheet free-space spectral model; real QDM sensor effects are intentionally left for later experiments.",
        ],
    }
    metrics["attenuation_threshold_table"] = plot_decay_curves(outputs)
    plot_recoverable_heatmap(outputs)
    plot_inverse_gain(outputs)
    metrics.update(full_field_inversion(outputs, data))
    metrics.update(finite_fov_experiment(outputs, data))
    metrics.update(noise_standoff_experiment(outputs))
    metrics["two_layer_single_plane_rank_gate"] = two_layer_single_plane_rank_gate(outputs)
    add_acceptance_gates(metrics)
    write_run_report(outputs, metrics)

    with open(outputs / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    print(f"\nOutputs written to: {outputs}")


if __name__ == "__main__":
    main()
