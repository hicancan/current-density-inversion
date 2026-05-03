from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt

# Allow running as `python src/run_all.py`.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from forward import (
    make_grid,
    standoff_plane,
    observation_points,
    make_two_layer_via_circuit,
    biot_savart_segments,
    bxy_energy,
    high_frequency_energy,
)
from sensor import observe_qdm_like, empirical_corr, apply_psf
from detection import dog_filter_B, crop_patch, matched_filter_score_map, peak_location, loc_error_um


def load_config():
    with open(ROOT / "configs" / "default.json", "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dirs():
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "data").mkdir(exist_ok=True)


def uT(B):
    return B * 1e6


def plot_b_component_grid(fields, titles, fname, component=2, cmap="coolwarm"):
    n = len(fields)
    fig, axes = plt.subplots(1, n, figsize=(4.2 * n, 3.6), constrained_layout=True)
    if n == 1:
        axes = [axes]
    vmax = max(np.percentile(np.abs(uT(F[..., component])), 99.0) for F in fields) + 1e-30
    for ax, F, title in zip(axes, fields, titles):
        im = ax.imshow(uT(F[..., component]), origin="lower", cmap=cmap, vmin=-vmax, vmax=vmax)
        ax.set_title(title)
        ax.set_xticks([]); ax.set_yticks([])
        fig.colorbar(im, ax=ax, shrink=0.78, label="µT")
    fig.savefig(ROOT / "outputs" / fname, dpi=180)
    plt.close(fig)


def plot_pipeline(B_true, B_blur, B_obs, conf, Z, fname):
    fig, axes = plt.subplots(2, 3, figsize=(12.5, 7.2), constrained_layout=True)
    fields = [(B_true, "true Bz"), (B_blur, "PSF-blurred Bz"), (B_obs, "observed Bz")]
    vmax = max(np.percentile(np.abs(uT(F[..., 2])), 99) for F, _ in fields) + 1e-30
    for ax, (F, title) in zip(axes[0], fields):
        im = ax.imshow(uT(F[..., 2]), origin="lower", cmap="coolwarm", vmin=-vmax, vmax=vmax)
        ax.set_title(title); ax.set_xticks([]); ax.set_yticks([])
        fig.colorbar(im, ax=ax, shrink=0.75, label="µT")
    im = axes[1, 0].imshow(conf, origin="lower", cmap="viridis", vmin=0, vmax=1)
    axes[1, 0].set_title("pixel confidence proxy"); axes[1, 0].set_xticks([]); axes[1, 0].set_yticks([])
    fig.colorbar(im, ax=axes[1, 0], shrink=0.75)
    im = axes[1, 1].imshow(Z * 1e6, origin="lower", cmap="magma")
    axes[1, 1].set_title("standoff z(x,y), µm"); axes[1, 1].set_xticks([]); axes[1, 1].set_yticks([])
    fig.colorbar(im, ax=axes[1, 1], shrink=0.75, label="µm")
    Bxy = np.sqrt(B_obs[..., 0] ** 2 + B_obs[..., 1] ** 2)
    im = axes[1, 2].imshow(uT(Bxy), origin="lower", cmap="inferno")
    axes[1, 2].set_title("observed |Bxy|"); axes[1, 2].set_xticks([]); axes[1, 2].set_yticks([])
    fig.colorbar(im, ax=axes[1, 2], shrink=0.75, label="µT")
    fig.savefig(ROOT / "outputs" / fname, dpi=180)
    plt.close(fig)


def plot_cov(target_corr, emp_corr, fname):
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.4), constrained_layout=True)
    for ax, mat, title in zip(axes, [target_corr, emp_corr], ["target corr", "empirical corr"]):
        im = ax.imshow(mat, cmap="coolwarm", vmin=-1, vmax=1)
        ax.set_title(title)
        ax.set_xticks([0,1,2]); ax.set_yticks([0,1,2])
        ax.set_xticklabels(["Bx", "By", "Bz"]); ax.set_yticklabels(["Bx", "By", "Bz"])
        for i in range(3):
            for j in range(3):
                ax.text(j, i, f"{mat[i,j]:.2f}", ha="center", va="center", fontsize=9)
        fig.colorbar(im, ax=ax, shrink=0.8)
    fig.savefig(ROOT / "outputs" / fname, dpi=180)
    plt.close(fig)


def plot_tilt_effect(B_const, B_tilt, diff, fname):
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.7), constrained_layout=True)
    arrs = [B_const[...,2], B_tilt[...,2], diff[...,2]]
    titles = ["constant-z Bz", "tilted-z Bz", "tilt mismatch ΔBz"]
    vmax = max(np.percentile(np.abs(uT(a)), 99) for a in arrs) + 1e-30
    for ax, arr, title in zip(axes, arrs, titles):
        im = ax.imshow(uT(arr), origin="lower", cmap="coolwarm", vmin=-vmax, vmax=vmax)
        ax.set_title(title); ax.set_xticks([]); ax.set_yticks([])
        fig.colorbar(im, ax=ax, shrink=0.75, label="µT")
    fig.savefig(ROOT / "outputs" / fname, dpi=180)
    plt.close(fig)


def plot_detection(raw_score, residual_score, dog_score, fname):
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.7), constrained_layout=True)
    maps = [(raw_score, "raw total field"), (residual_score, "oracle residual"), (dog_score, "DoG band-pass residual")]
    vmax = max(np.percentile(np.abs(M), 99) for M, _ in maps) + 1e-30
    for ax, (M, title) in zip(axes, maps):
        im = ax.imshow(M, origin="lower", cmap="viridis", vmin=np.percentile(M, 1), vmax=np.percentile(M, 99.5))
        ax.axhline(M.shape[0]//2, color="w", lw=0.5, alpha=0.5)
        ax.axvline(M.shape[1]//2, color="w", lw=0.5, alpha=0.5)
        ax.set_title(title); ax.set_xticks([]); ax.set_yticks([])
        fig.colorbar(im, ax=ax, shrink=0.75, label="score")
    fig.savefig(ROOT / "outputs" / fname, dpi=180)
    plt.close(fig)


def plot_bandpass_sweep(rows, fname):
    labels = [r["label"] for r in rows]
    raw = [r["raw_peak"] for r in rows]
    res = [r["residual_peak"] for r in rows]
    dog = [r["dog_peak"] for r in rows]
    tilt = [r["tilt_range_um"] for r in rows]
    x = np.arange(len(labels))
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.0), constrained_layout=True)
    axes[0].plot(x, raw, "o-", label="raw")
    axes[0].plot(x, res, "o-", label="residual")
    axes[0].plot(x, dog, "o-", label="DoG residual")
    axes[0].set_xticks(x); axes[0].set_xticklabels(labels, rotation=20, ha="right")
    axes[0].set_ylabel("matched-filter peak score")
    axes[0].set_title("via detection score under nonidealities")
    axes[0].legend()
    axes[1].bar(x, tilt)
    axes[1].set_xticks(x); axes[1].set_xticklabels(labels, rotation=20, ha="right")
    axes[1].set_ylabel("z range across FOV (µm)")
    axes[1].set_title("standoff tilt range")
    fig.savefig(ROOT / "outputs" / fname, dpi=180)
    plt.close(fig)


def nv_axes() -> np.ndarray:
    axes = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, -1.0, -1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, -1.0, 1.0],
        ],
        dtype=float,
    )
    return axes / np.linalg.norm(axes, axis=1, keepdims=True)


def project_nv_axes(B: np.ndarray, axes: np.ndarray) -> np.ndarray:
    return np.einsum("...c,ac->...a", B, axes)


def reconstruct_B_from_nv(projected: np.ndarray, axes: np.ndarray) -> np.ndarray:
    pinv = np.linalg.pinv(axes)
    return np.einsum("...a,ca->...c", projected, pinv)


def nv_projection_metrics(B_obs: np.ndarray, cfg: dict) -> dict:
    axes = nv_axes()
    projected = project_nv_axes(B_obs, axes)
    recon = reconstruct_B_from_nv(projected, axes)
    gains = np.asarray(cfg.get("nv_axis_gain_mismatch", [1.03, 0.97, 1.015, 0.985]), dtype=float)
    projected_gain_mismatch = projected * gains[None, None, :]
    recon_gain_mismatch = reconstruct_B_from_nv(projected_gain_mismatch, axes)
    one_axis_rank = int(np.linalg.matrix_rank(axes[:1]))
    four_axis_rank = int(np.linalg.matrix_rank(axes))
    cond = float(np.linalg.cond(axes))
    return {
        "axes": axes.tolist(),
        "projection_shape": list(projected.shape),
        "four_axis_rank": four_axis_rank,
        "single_axis_rank": one_axis_rank,
        "four_axis_condition_number": cond,
        "four_axis_reconstruction_rel_l2": float(np.linalg.norm(recon - B_obs) / (np.linalg.norm(B_obs) + 1e-30)),
        "axis_gain_mismatch": gains.tolist(),
        "axis_gain_mismatch_reconstruction_rel_l2": float(np.linalg.norm(recon_gain_mismatch - B_obs) / (np.linalg.norm(B_obs) + 1e-30)),
        "single_axis_rank_deficient": bool(one_axis_rank < 3),
    }


def add_acceptance_gates(metrics):
    full = next(r for r in metrics["case_metrics"] if r["label"] == "full")
    hard = next(r for r in metrics["case_metrics"] if r["label"] == "hard-full")
    gates = {
        "correlated_noise_matches_target_covariance": {
            "threshold": "mean absolute correlation error < 0.05",
            "value": metrics["summary"]["full_case_noise_corr_mean_abs_error_before_spatial_filter"],
            "pass": metrics["summary"]["full_case_noise_corr_mean_abs_error_before_spatial_filter"] < 0.05,
        },
        "psf_removes_high_frequency_energy": {
            "threshold": "full-case Bz high-frequency ratio < 0.25",
            "value": metrics["summary"]["full_case_psf_high_frequency_energy_ratio_Bz"],
            "pass": metrics["summary"]["full_case_psf_high_frequency_energy_ratio_Bz"] < 0.25,
        },
        "tilt_creates_measurable_forward_mismatch": {
            "threshold": "tilt range > 10 um and field mismatch > 1%",
            "value": [
                metrics["summary"]["full_case_tilt_range_um"],
                metrics["summary"]["full_case_constant_vs_tilted_field_rel_l2"],
            ],
            "pass": (
                metrics["summary"]["full_case_tilt_range_um"] > 10.0
                and metrics["summary"]["full_case_constant_vs_tilted_field_rel_l2"] > 0.01
            ),
        },
        "residual_detection_beats_raw_total_field": {
            "threshold": "full residual/raw peak ratio > 2 and residual loc error < raw loc error",
            "value": [
                metrics["summary"]["full_case_residual_vs_raw_peak_ratio"],
                full["raw_loc_error_um"],
                full["residual_loc_error_um"],
            ],
            "pass": (
                metrics["summary"]["full_case_residual_vs_raw_peak_ratio"] > 2.0
                and full["residual_loc_error_um"] < full["raw_loc_error_um"]
            ),
        },
        "hard_case_residual_still_localizes_reasonably": {
            "threshold": "hard-full residual loc error < 100 um",
            "value": hard["residual_loc_error_um"],
            "pass": hard["residual_loc_error_um"] < 100.0,
        },
        "nv_four_axis_projection_is_well_conditioned": {
            "threshold": "four-axis rank is 3, condition number < 2, reconstruction error < 1e-10",
            "value": [
                metrics["nv_projection"]["four_axis_rank"],
                metrics["nv_projection"]["four_axis_condition_number"],
                metrics["nv_projection"]["four_axis_reconstruction_rel_l2"],
            ],
            "pass": (
                metrics["nv_projection"]["four_axis_rank"] == 3
                and metrics["nv_projection"]["four_axis_condition_number"] < 2.0
                and metrics["nv_projection"]["four_axis_reconstruction_rel_l2"] < 1e-10
            ),
        },
        "single_nv_axis_is_rank_deficient": {
            "threshold": "single-axis rank < 3",
            "value": metrics["nv_projection"]["single_axis_rank"],
            "pass": metrics["nv_projection"]["single_axis_rank"] < 3,
        },
        "nv_axis_gain_mismatch_is_measurable": {
            "threshold": "gain-mismatch reconstruction relative L2 > 1%",
            "value": metrics["nv_projection"]["axis_gain_mismatch_reconstruction_rel_l2"],
            "pass": metrics["nv_projection"]["axis_gain_mismatch_reconstruction_rel_l2"] > 0.01,
        },
    }
    metrics["acceptance_gates"] = gates
    metrics["all_acceptance_gates_passed"] = all(g["pass"] for g in gates.values())


def write_run_report(metrics):
    gate_lines = "\n".join(
        f"- {name}: {'PASS' if gate['pass'] else 'FAIL'}; value={gate['value']}; threshold={gate['threshold']}"
        for name, gate in metrics["acceptance_gates"].items()
    )
    full = next(r for r in metrics["case_metrics"] if r["label"] == "full")
    report = f"""# exp05 Run Report

## Role

MVP-4 QDM-like sensor nonidealities. This experiment stress-tests standoff tilt,
PSF blur, correlated channel noise, spatial confidence, and via-scale band-pass
detection before these effects are mixed into learned inversion.

## Gate Summary

Overall: {'PASS' if metrics['all_acceptance_gates_passed'] else 'FAIL'}

{gate_lines}

## Key Results

- full-case tilt range: `{metrics['summary']['full_case_tilt_range_um']:.2f} um`
- full-case constant-vs-tilted field relative L2: `{metrics['summary']['full_case_constant_vs_tilted_field_rel_l2']:.3e}`
- full-case Bz high-frequency energy ratio after PSF: `{metrics['summary']['full_case_psf_high_frequency_energy_ratio_Bz']:.3f}`
- full-case raw via localization error: `{full['raw_loc_error_um']:.2f} um`
- full-case residual via localization error: `{full['residual_loc_error_um']:.2f} um`
- NV four-axis reconstruction relative L2: `{metrics['nv_projection']['four_axis_reconstruction_rel_l2']:.3e}`
- NV axis-gain mismatch reconstruction relative L2: `{metrics['nv_projection']['axis_gain_mismatch_reconstruction_rel_l2']:.3e}`

## Boundary

This is still a proxy, not an ODMR or NV-Hamiltonian simulator. The four-axis
NV projection check verifies vector-field observability under ideal calibrated
axes, and the axis-gain mismatch check quantifies one calibration risk. The
residual detector still uses oracle sheet-background subtraction.
"""
    (ROOT / "outputs" / "RUN_REPORT.md").write_text(report, encoding="utf-8")


def run_case(cfg, label, alpha_scale=1.0, noise_scale=1.0, psf_scale=1.0):
    rng = np.random.default_rng(cfg["seed"] + int(1000 * alpha_scale) + int(100 * noise_scale))
    X, Y, dx = make_grid(cfg["fov_m"], cfg["grid_n"])
    Z_tilt = standoff_plane(X, Y, cfg["standoff_m"], cfg["tilt_alpha"] * alpha_scale, cfg["tilt_beta"] * alpha_scale)
    Z_const = standoff_plane(X, Y, cfg["standoff_m"], 0.0, 0.0)
    obs_tilt = observation_points(X, Y, Z_tilt)
    obs_const = observation_points(X, Y, Z_const)
    l1, l2, via = make_two_layer_via_circuit(cfg["current_A"], cfg["layer1_depth_m"], cfg["layer2_depth_m"])
    nsub = cfg["segment_subdivisions"]

    B_l1_t = biot_savart_segments(l1, obs_tilt, nsub)
    B_l2_t = biot_savart_segments(l2, obs_tilt, nsub)
    B_via_t = biot_savart_segments(via, obs_tilt, nsub)
    B_true_t = B_l1_t + B_l2_t + B_via_t

    B_l1_c = biot_savart_segments(l1, obs_const, nsub)
    B_l2_c = biot_savart_segments(l2, obs_const, nsub)
    B_via_c = biot_savart_segments(via, obs_const, nsub)
    B_true_c = B_l1_c + B_l2_c + B_via_c

    sigmas_T = np.asarray(cfg["noise_sigma_uT"], dtype=float) * 1e-6 * noise_scale
    obs = observe_qdm_like(
        B_true_t,
        psf_sigma_px=cfg["psf_sigma_px"] * psf_scale,
        noise_sigma_T=sigmas_T,
        noise_corr=np.asarray(cfg["noise_corr"], dtype=float),
        spatial_corr_sigma_px=cfg["spatial_corr_sigma_px"],
        confidence_floor=cfg["confidence_floor"],
        confidence_percentile=cfg["confidence_percentile"],
        rng=rng,
    )
    # Sheet background receives the same deterministic PSF but no random noise, oracle style.
    B_sheet_blur = apply_psf(B_l1_t + B_l2_t, cfg["psf_sigma_px"] * psf_scale)
    B_via_blur = apply_psf(B_via_t, cfg["psf_sigma_px"] * psf_scale)
    residual_obs = obs["B_obs"] - B_sheet_blur

    center = (cfg["grid_n"] // 2, cfg["grid_n"] // 2)
    r = cfg["via_patch_radius_px"]
    T_patch = crop_patch(B_via_blur, center, r)
    T_patch_const = crop_patch(apply_psf(B_via_c, cfg["psf_sigma_px"] * psf_scale), center, r)

    raw_score = matched_filter_score_map(obs["B_obs"], T_patch)
    residual_score = matched_filter_score_map(residual_obs, T_patch)
    dog_residual = dog_filter_B(residual_obs, cfg["dog_sigma_small_px"], cfg["dog_sigma_large_px"])
    dog_template = crop_patch(dog_filter_B(B_via_blur, cfg["dog_sigma_small_px"], cfg["dog_sigma_large_px"]), center, r)
    dog_score = matched_filter_score_map(dog_residual, dog_template)
    # template mismatch: tilted data, constant-z template
    residual_score_const_template = matched_filter_score_map(residual_obs, T_patch_const)

    raw_loc = peak_location(raw_score, dx, cfg["fov_m"])
    res_loc = peak_location(residual_score, dx, cfg["fov_m"])
    dog_loc = peak_location(dog_score, dx, cfg["fov_m"])

    metrics = {
        "label": label,
        "tilt_range_um": float((np.max(Z_tilt) - np.min(Z_tilt)) * 1e6),
        "constant_vs_tilted_field_rel_l2": float(np.linalg.norm(B_true_t - B_true_c) / (np.linalg.norm(B_true_c) + 1e-30)),
        "psf_high_frequency_energy_ratio_Bz": float(high_frequency_energy(obs["B_blur"][...,2]) / (high_frequency_energy(B_true_t[...,2]) + 1e-30)),
        "via_to_sheet_Bxy_energy_ratio": float(bxy_energy(B_via_t) / (bxy_energy(B_l1_t + B_l2_t) + 1e-30)),
        "raw_peak": float(raw_loc[-1]),
        "residual_peak": float(res_loc[-1]),
        "dog_peak": float(dog_loc[-1]),
        "constant_template_residual_peak": float(np.max(residual_score_const_template)),
        "raw_loc_error_um": loc_error_um(raw_loc),
        "residual_loc_error_um": loc_error_um(res_loc),
        "dog_loc_error_um": loc_error_um(dog_loc),
    }
    data = {
        "X": X, "Y": Y, "Z_tilt": Z_tilt, "Z_const": Z_const,
        "B_true_tilt": B_true_t, "B_true_const": B_true_c,
        "B_l1_tilt": B_l1_t, "B_l2_tilt": B_l2_t, "B_via_tilt": B_via_t,
        "B_obs": obs["B_obs"], "B_blur": obs["B_blur"], "confidence": obs["confidence"],
        "noise": obs["noise"], "base_noise": obs["base_noise"],
        "residual_obs": residual_obs, "dog_residual": dog_residual,
        "raw_score": raw_score, "residual_score": residual_score, "dog_score": dog_score,
    }
    return metrics, data


def main():
    ensure_dirs()
    cfg = load_config()
    target_corr = np.asarray(cfg["noise_corr"], dtype=float)

    cases = [
        ("ideal-ish", 0.0, 0.15, 0.0),
        ("tilt-only", 1.0, 0.0, 0.0),
        ("psf+noise", 0.0, 1.0, 1.0),
        ("full", 1.0, 1.0, 1.0),
        ("hard-full", 1.5, 1.5, 1.2),
    ]
    rows = []
    saved_full = None
    for label, a, n, p in cases:
        metrics, data = run_case(cfg, label, a, n, p)
        rows.append(metrics)
        if label == "full":
            saved_full = data

    assert saved_full is not None
    emp_corr = empirical_corr(saved_full["base_noise"])
    corr_abs_err = float(np.mean(np.abs(emp_corr - target_corr)))
    full_metrics = [r for r in rows if r["label"] == "full"][0]
    full_metrics["noise_corr_mean_abs_error_before_spatial_filter"] = corr_abs_err

    # Plots.
    plot_pipeline(saved_full["B_true_tilt"], saved_full["B_blur"], saved_full["B_obs"], saved_full["confidence"], saved_full["Z_tilt"], "01_sensor_model_pipeline.png")
    plot_cov(target_corr, emp_corr, "02_noise_covariance.png")
    plot_tilt_effect(saved_full["B_true_const"], saved_full["B_true_tilt"], saved_full["B_true_tilt"] - saved_full["B_true_const"], "03_tilt_effect.png")
    plot_detection(saved_full["raw_score"], saved_full["residual_score"], saved_full["dog_score"], "04_via_detection.png")
    plot_bandpass_sweep(rows, "05_bandpass_and_standoff.png")

    metrics = {
        "experiment": "exp05-realistic-noise-and-standoff-tilt",
        "config": cfg,
        "case_metrics": rows,
        "nv_projection": nv_projection_metrics(saved_full["B_obs"], cfg),
        "summary": {
            "full_case_noise_corr_mean_abs_error_before_spatial_filter": corr_abs_err,
            "full_case_residual_vs_raw_peak_ratio": float(full_metrics["residual_peak"] / (abs(full_metrics["raw_peak"]) + 1e-30)),
            "full_case_dog_vs_residual_peak_ratio": float(full_metrics["dog_peak"] / (abs(full_metrics["residual_peak"]) + 1e-30)),
            "full_case_constant_template_peak_ratio": float(full_metrics["constant_template_residual_peak"] / (abs(full_metrics["residual_peak"]) + 1e-30)),
            "full_case_tilt_range_um": full_metrics["tilt_range_um"],
            "full_case_constant_vs_tilted_field_rel_l2": full_metrics["constant_vs_tilted_field_rel_l2"],
            "full_case_psf_high_frequency_energy_ratio_Bz": full_metrics["psf_high_frequency_energy_ratio_Bz"],
        }
    }
    add_acceptance_gates(metrics)
    with open(ROOT / "outputs" / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    write_run_report(metrics)
    np.savez_compressed(ROOT / "data" / "exp05_sensor_nonidealities.npz", **saved_full)
    print(json.dumps(metrics["summary"], indent=2))


if __name__ == "__main__":
    main()
