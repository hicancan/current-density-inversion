#!/usr/bin/env python3
"""exp06: anti-inverse-crime / multi-fidelity validation.

This experiment demonstrates why testing an inverse solver only on fields generated
by the same forward operator used in the solver can be misleading.

It uses a fast ideal line-current Biot-Savart operator as the low-fidelity model,
and a deliberately different high-fidelity surrogate that adds finite width,
return currents, depth offsets, PSF blur, and noise.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

MU0 = 4e-7 * np.pi
ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs" / "default.json"
OUTPUTS = ROOT / "outputs"
DATA = ROOT / "data"


@dataclass(frozen=True)
class Grid:
    X: np.ndarray
    Y: np.ndarray
    Z: np.ndarray
    points: np.ndarray
    n: int
    fov_m: float
    dx_m: float


def load_config(path: Path = CONFIG_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_root_path(path_value: str) -> Path:
    path = Path(path_value)
    if not path.is_absolute():
        path = ROOT / path
    return path.resolve()


def load_real_pypeec_bridge(cfg: dict) -> dict:
    """Read exp07 real PyPEEC metrics as a no-training fidelity bridge."""
    bridge_cfg = cfg.get("real_pypeec_bridge", {})
    if not bool(bridge_cfg.get("enabled", False)):
        return {"enabled": False}

    metrics_path = resolve_root_path(str(bridge_cfg["metrics_path"]))
    if not metrics_path.exists():
        return {
            "enabled": True,
            "metrics_path": str(metrics_path),
            "artifact_available": False,
            "boundary": "exp07 metrics artifact is missing; no PyPEEC bridge claim can be made.",
        }

    exp07 = json.loads(metrics_path.read_text(encoding="utf-8"))
    summary = exp07.get("summary", {})
    case_metrics = exp07.get("case_metrics", [])
    exp03_like_cases = set(summary.get("exp03_like_completed_cases", []))
    exp03_like_rows = [row for row in case_metrics if row.get("case") in exp03_like_cases]
    case_shape_gaps = {
        row["case"]: float(row.get("pypeec_centerline_shape_rel_l2", float("nan")))
        for row in case_metrics
    }
    case_raw_gaps = {
        row["case"]: float(row.get("pypeec_vs_center_rel_l2", float("nan")))
        for row in case_metrics
    }
    return {
        "enabled": True,
        "metrics_path": str(metrics_path),
        "artifact_available": True,
        "exp07_all_gates_passed": bool(exp07.get("all_acceptance_gates_passed", False)),
        "backend_mode": exp07.get("backend_mode_executed"),
        "pypeec_version": exp07.get("pypeec_detection", {}).get("python_package_version"),
        "n_cases_completed": int(exp07.get("n_cases_completed", 0)),
        "n_cases_requested": int(exp07.get("n_cases_requested", 0)),
        "exp03_like_cases": sorted(exp03_like_cases),
        "exp03_like_case_count": int(summary.get("exp03_like_case_count", len(exp03_like_rows))),
        "pypeec_centerline_gap_median": float(summary.get("pypeec_centerline_gap_median", float("nan"))),
        "pypeec_centerline_shape_gap_median": float(summary.get("pypeec_centerline_shape_gap_median", float("nan"))),
        "exp03_like_shape_gap_median": float(summary.get("exp03_like_shape_gap_median", float("nan"))),
        "max_terminal_current_rel_error": float(summary.get("max_terminal_current_rel_error", float("nan"))),
        "max_finest_step_convergence_shape_delta": float(
            summary.get("max_finest_step_convergence_shape_delta", float("nan"))
        ),
        "case_shape_gaps": case_shape_gaps,
        "case_raw_gaps": case_raw_gaps,
        "interpretation": (
            "Real PyPEEC is treated as an external solver fidelity bridge. "
            "The reported gaps are field-level operator mismatch signals; "
            "this exp06 run does not calibrate on PyPEEC samples."
        ),
    }


def make_grid(n: int, fov_um: float, measurement_z_um: float = 0.0) -> Grid:
    fov_m = fov_um * 1e-6
    coords = np.linspace(-fov_m / 2, fov_m / 2, n)
    X, Y = np.meshgrid(coords, coords, indexing="xy")
    Z = np.full_like(X, measurement_z_um * 1e-6)
    points = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
    dx = coords[1] - coords[0]
    return Grid(X=X, Y=Y, Z=Z, points=points, n=n, fov_m=fov_m, dx_m=dx)


def segment_field(
    points: np.ndarray,
    p0: Iterable[float],
    p1: Iterable[float],
    current: float = 1.0,
    n_steps: int = 80,
    eps: float = 1e-18,
) -> np.ndarray:
    """Numerically integrate Biot-Savart field for a finite straight segment.

    Parameters
    ----------
    points:
        Observation points, shape (N, 3), in meters.
    p0, p1:
        Segment endpoints in meters.
    current:
        Current in Ampere flowing from p0 to p1.
    n_steps:
        Number of midpoint quadrature samples along the segment.
    eps:
        Softening term to avoid division by zero in pathological tests.

    Returns
    -------
    B:
        Magnetic field at each observation point, shape (N, 3), in Tesla.
    """
    p0 = np.asarray(p0, dtype=float)
    p1 = np.asarray(p1, dtype=float)
    dl = (p1 - p0) / n_steps
    ts = (np.arange(n_steps) + 0.5) / n_steps
    mids = p0[None, :] + ts[:, None] * (p1 - p0)[None, :]

    B = np.zeros((points.shape[0], 3), dtype=float)
    for mid in mids:
        r = points - mid[None, :]
        r_norm = np.linalg.norm(r, axis=1)
        cross = np.cross(dl[None, :], r)
        B += cross / (r_norm[:, None] ** 3 + eps)
    return MU0 * current / (4 * np.pi) * B


def finite_width_wire_field(
    points: np.ndarray,
    p0: np.ndarray,
    p1: np.ndarray,
    current: float,
    width_m: float,
    n_filaments: int,
    n_steps: int = 80,
) -> np.ndarray:
    """Approximate a finite-width wire by parallel filaments across its width."""
    direction = p1 - p0
    dxy = direction[:2]
    norm = np.linalg.norm(dxy)
    if norm == 0:
        raise ValueError("wire direction cannot be vertical for finite_width_wire_field")
    tangent = dxy / norm
    normal_xy = np.array([-tangent[1], tangent[0]])
    offsets = np.linspace(-0.5, 0.5, n_filaments) * width_m
    B = np.zeros((points.shape[0], 3), dtype=float)
    for off in offsets:
        shift = np.array([normal_xy[0] * off, normal_xy[1] * off, 0.0])
        B += segment_field(points, p0 + shift, p1 + shift, current / n_filaments, n_steps=n_steps)
    return B


def psf_blur_field(field: np.ndarray, sigma_px: float) -> np.ndarray:
    """Apply per-component Gaussian PSF blur to field image, shape (n,n,3)."""
    if sigma_px <= 0:
        return field.copy()
    return np.stack([gaussian_filter(field[..., c], sigma=sigma_px, mode="nearest") for c in range(3)], axis=-1)


def build_basis_low(grid: Grid, cfg: dict) -> Tuple[np.ndarray, List[str]]:
    """Build low-fidelity basis fields for [I_L1, I_L2, I_via]."""
    g = cfg["geometry"]
    L = g["wire_half_length_um"] * 1e-6
    z1 = g["layer1_z_um"] * 1e-6
    z2 = g["layer2_z_um"] * 1e-6
    p_l1_a = np.array([-L, 0.0, z1])
    p_l1_b = np.array([ L, 0.0, z1])
    p_l2_a = np.array([0.0, -L, z2])
    p_l2_b = np.array([0.0,  L, z2])
    p_via_a = np.array([0.0, 0.0, z1])
    p_via_b = np.array([0.0, 0.0, z2])

    fields = [
        segment_field(grid.points, p_l1_a, p_l1_b, 1.0),
        segment_field(grid.points, p_l2_a, p_l2_b, 1.0),
        segment_field(grid.points, p_via_a, p_via_b, 1.0),
    ]
    basis = np.stack([f.reshape(grid.n, grid.n, 3) for f in fields], axis=0)
    return basis, ["I_layer1_horizontal", "I_layer2_vertical", "I_via"]


def build_basis_high_surrogate(grid: Grid, cfg: dict) -> Tuple[np.ndarray, List[str]]:
    """Build a high-fidelity surrogate basis different from the low operator."""
    g = cfg["geometry"]
    hf = cfg["high_fidelity_surrogate"]
    L = g["wire_half_length_um"] * 1e-6
    width = g["wire_width_um"] * 1e-6
    n_fil = int(hf["n_width_filaments"])
    return_scale = float(hf["return_current_scale"])
    z_ground = g["ground_z_um"] * 1e-6
    z1 = (g["layer1_z_um"] + hf["depth_shift_um"]["layer1"]) * 1e-6
    z2 = (g["layer2_z_um"] + hf["depth_shift_um"]["layer2"]) * 1e-6
    via_top = (g["layer1_z_um"] + hf["depth_shift_um"]["via_top"]) * 1e-6
    via_bottom = (g["layer2_z_um"] + hf["depth_shift_um"]["via_bottom"]) * 1e-6
    via_radius = g["via_radius_um"] * 1e-6

    p_l1_a = np.array([-L, 0.0, z1])
    p_l1_b = np.array([ L, 0.0, z1])
    p_l2_a = np.array([0.0, -L, z2])
    p_l2_b = np.array([0.0,  L, z2])
    p_l1_g_a = np.array([-L, 0.0, z_ground])
    p_l1_g_b = np.array([ L, 0.0, z_ground])
    p_l2_g_a = np.array([0.0, -L, z_ground])
    p_l2_g_b = np.array([0.0,  L, z_ground])

    # finite-width target wire plus simplified return current in ground plane
    B1 = finite_width_wire_field(grid.points, p_l1_a, p_l1_b, 1.0, width, n_fil)
    B1 += finite_width_wire_field(grid.points, p_l1_g_a, p_l1_g_b, -return_scale, width * 1.8, n_fil)

    B2 = finite_width_wire_field(grid.points, p_l2_a, p_l2_b, 1.0, width, n_fil)
    B2 += finite_width_wire_field(grid.points, p_l2_g_a, p_l2_g_b, -return_scale, width * 1.8, n_fil)

    # Via as a tiny cluster of vertical filaments rather than one ideal line.
    offsets = [
        (0.0, 0.0),
        (via_radius * 0.55, 0.0),
        (-via_radius * 0.55, 0.0),
        (0.0, via_radius * 0.55),
        (0.0, -via_radius * 0.55),
    ]
    Bv = np.zeros((grid.points.shape[0], 3), dtype=float)
    for ox, oy in offsets:
        Bv += segment_field(
            grid.points,
            np.array([ox, oy, via_top]),
            np.array([ox, oy, via_bottom]),
            1.0 / len(offsets),
        )
    # weak return path of vertical current spread over a larger loop-like column
    for ox, oy in [(2.5 * via_radius, 0), (-2.5 * via_radius, 0), (0, 2.5 * via_radius), (0, -2.5 * via_radius)]:
        Bv += segment_field(
            grid.points,
            np.array([ox, oy, via_bottom]),
            np.array([ox, oy, via_top]),
            0.08 / 4,
        )

    basis = np.stack([B1.reshape(grid.n, grid.n, 3), B2.reshape(grid.n, grid.n, 3), Bv.reshape(grid.n, grid.n, 3)], axis=0)
    basis = np.stack([psf_blur_field(b, float(hf["psf_sigma_px"])) for b in basis], axis=0)
    return basis, ["I_layer1_horizontal_high", "I_layer2_vertical_high", "I_via_high"]


def build_basis_medium_surrogate(grid: Grid, cfg: dict) -> Tuple[np.ndarray, List[str]]:
    """Intermediate surrogate: finite width and mild depth shift, no return plane."""
    g = cfg["geometry"]
    mf = cfg.get("medium_fidelity_surrogate", {})
    L = g["wire_half_length_um"] * 1e-6
    width = g["wire_width_um"] * 1e-6 * float(mf.get("width_scale", 1.0))
    n_fil = int(mf.get("n_width_filaments", 3))
    depth_shift_l1 = float(mf.get("depth_shift_um", {}).get("layer1", 2.0))
    depth_shift_l2 = float(mf.get("depth_shift_um", {}).get("layer2", -2.0))
    z1 = (g["layer1_z_um"] + depth_shift_l1) * 1e-6
    z2 = (g["layer2_z_um"] + depth_shift_l2) * 1e-6
    via_radius = g["via_radius_um"] * 1e-6 * 0.5

    p_l1_a = np.array([-L, 0.0, z1])
    p_l1_b = np.array([ L, 0.0, z1])
    p_l2_a = np.array([0.0, -L, z2])
    p_l2_b = np.array([0.0,  L, z2])

    B1 = finite_width_wire_field(grid.points, p_l1_a, p_l1_b, 1.0, width, n_fil)
    B2 = finite_width_wire_field(grid.points, p_l2_a, p_l2_b, 1.0, width, n_fil)
    Bv = np.zeros((grid.points.shape[0], 3), dtype=float)
    for ox, oy in [(0.0, 0.0), (via_radius, 0.0), (-via_radius, 0.0), (0.0, via_radius), (0.0, -via_radius)]:
        Bv += segment_field(
            grid.points,
            np.array([ox, oy, z1]),
            np.array([ox, oy, z2]),
            1.0 / 5.0,
        )

    basis = np.stack([B1.reshape(grid.n, grid.n, 3), B2.reshape(grid.n, grid.n, 3), Bv.reshape(grid.n, grid.n, 3)], axis=0)
    sigma = float(mf.get("psf_sigma_px", 0.0))
    basis = np.stack([psf_blur_field(b, sigma) for b in basis], axis=0)
    return basis, ["I_layer1_horizontal_medium", "I_layer2_vertical_medium", "I_via_medium"]


def flatten_basis(basis: np.ndarray) -> np.ndarray:
    return basis.reshape(basis.shape[0], -1)


def sample_currents(rng: np.random.Generator, n: int, max_abs_mA: float) -> np.ndarray:
    """Random target currents in Ampere.

    Values are deliberately mixed-sign to test sign and linearity.
    Via currents are slightly smaller on average but can be comparable.
    """
    max_a = max_abs_mA * 1e-3
    x = rng.uniform(-max_a, max_a, size=(n, 3))
    x[:, 2] *= 0.65
    return x


def synthesize_fields(currents: np.ndarray, basis: np.ndarray, noise_std_T: float = 0.0, rng=None) -> np.ndarray:
    """Create fields from basis, output shape (N, n, n, 3)."""
    flat_basis = flatten_basis(basis)
    fields_flat = currents @ flat_basis
    fields = fields_flat.reshape((currents.shape[0],) + basis.shape[1:])
    if noise_std_T > 0:
        if rng is None:
            rng = np.random.default_rng(0)
        fields = fields + rng.normal(scale=noise_std_T, size=fields.shape)
    return fields


def physics_decoder_from_low_basis(basis_low: np.ndarray, ridge: float = 1e-20) -> np.ndarray:
    """Return matrix P such that x_hat = y_flat @ P.T using low basis."""
    A = flatten_basis(basis_low)  # (3, d)
    gram = A @ A.T + ridge * np.eye(A.shape[0])
    return np.linalg.solve(gram, A)  # (3,d)


def predict_physics(fields: np.ndarray, decoder: np.ndarray) -> np.ndarray:
    y = fields.reshape(fields.shape[0], -1)
    return y @ decoder.T


def matched_features(fields: np.ndarray, basis_low: np.ndarray) -> np.ndarray:
    y = fields.reshape(fields.shape[0], -1)
    A = flatten_basis(basis_low)
    # Normalize features by basis energy for scale stability.
    denom = np.sum(A * A, axis=1)[None, :] + 1e-30
    return (y @ A.T) / denom


def fit_ridge(features: np.ndarray, targets: np.ndarray, lam: float) -> Tuple[np.ndarray, np.ndarray]:
    """Fit affine ridge: targets ≈ features @ W + b."""
    X = np.concatenate([features, np.ones((features.shape[0], 1))], axis=1)
    reg = lam * np.eye(X.shape[1])
    reg[-1, -1] = 0.0
    Wb = np.linalg.solve(X.T @ X + reg, X.T @ targets)
    return Wb[:-1, :], Wb[-1, :]


def apply_ridge(features: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    return features @ W + b[None, :]


def rel_l2(pred: np.ndarray, true: np.ndarray) -> float:
    return float(np.linalg.norm(pred - true) / (np.linalg.norm(true) + 1e-30))


def mae_mA(pred: np.ndarray, true: np.ndarray) -> float:
    return float(np.mean(np.abs(pred - true)) * 1e3)


def per_channel_rel_l2(pred: np.ndarray, true: np.ndarray) -> List[float]:
    return [float(np.linalg.norm(pred[:, i] - true[:, i]) / (np.linalg.norm(true[:, i]) + 1e-30)) for i in range(true.shape[1])]


def plot_field_triplet(path: Path, fields: Dict[str, np.ndarray], title: str, scale_uT: bool = True) -> None:
    n_rows = len(fields)
    fig, axes = plt.subplots(n_rows, 3, figsize=(10, 3.1 * n_rows), constrained_layout=True)
    if n_rows == 1:
        axes = axes[None, :]
    comps = ["Bx", "By", "Bz"]
    for r, (name, field) in enumerate(fields.items()):
        arr = field * (1e6 if scale_uT else 1.0)
        vmax = np.percentile(np.abs(arr), 99.5)
        vmax = max(vmax, 1e-12)
        for c in range(3):
            im = axes[r, c].imshow(arr[..., c], origin="lower", cmap="coolwarm", vmin=-vmax, vmax=vmax)
            axes[r, c].set_title(f"{name}: {comps[c]} ({'uT' if scale_uT else 'T'})")
            axes[r, c].set_xticks([])
            axes[r, c].set_yticks([])
            fig.colorbar(im, ax=axes[r, c], fraction=0.046, pad=0.04)
    fig.suptitle(title)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_error_bars(path: Path, metrics: Dict[str, float]) -> None:
    labels = ["Low test\n(same operator)", "High test\n(no adaptation)", "High test\n(400 cal)"]
    values = [
        metrics["low_test_rel_l2_physics_decoder"],
        metrics["high_test_rel_l2_physics_decoder"],
        metrics["high_test_rel_l2_calibrated_400"],
    ]
    fig, ax = plt.subplots(figsize=(7.5, 4.5), constrained_layout=True)
    ax.bar(labels, values)
    ax.set_ylabel("Relative L2 current error")
    ax.set_title("Inverse-crime gap: same-operator test is over-optimistic")
    ax.grid(axis="y", alpha=0.3)
    for i, v in enumerate(values):
        ax.text(i, v + max(values) * 0.03, f"{v:.3f}", ha="center")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_current_scatter(path: Path, true: np.ndarray, pred_before: np.ndarray, pred_after: np.ndarray) -> None:
    names = ["I_L1", "I_L2", "I_via"]
    fig, axes = plt.subplots(2, 3, figsize=(11, 6.5), constrained_layout=True)
    for j, name in enumerate(names):
        for row, pred, label in [(0, pred_before, "Before calibration"), (1, pred_after, "After calibration")]:
            ax = axes[row, j]
            ax.scatter(true[:, j] * 1e3, pred[:, j] * 1e3, s=8, alpha=0.35)
            mn = min(np.min(true[:, j]), np.min(pred[:, j])) * 1e3
            mx = max(np.max(true[:, j]), np.max(pred[:, j])) * 1e3
            ax.plot([mn, mx], [mn, mx], "k--", lw=1)
            ax.set_title(f"{label}: {name}")
            ax.set_xlabel("True (mA)")
            ax.set_ylabel("Pred (mA)")
            ax.grid(alpha=0.25)
    fig.suptitle("High-fidelity surrogate currents: prediction scatter")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_calibration_curve(path: Path, calib_sizes: List[int], errors: List[float], baseline_error: float, low_error: float) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 4.5), constrained_layout=True)
    ax.plot(calib_sizes, errors, marker="o", label="High-fidelity calibrated")
    ax.axhline(baseline_error, ls="--", color="tab:red", label="No adaptation")
    ax.axhline(low_error, ls=":", color="tab:green", label="Low same-operator test")
    ax.set_xscale("log")
    ax.set_xlabel("Number of high-fidelity calibration samples")
    ax.set_ylabel("High-test relative L2 current error")
    ax.set_title("Small high-fidelity calibration set reduces operator-mismatch error")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_fidelity_ladder(path: Path, metrics: Dict[str, object]) -> None:
    labels = ["low", "medium", "high"]
    decoder_errors = [
        metrics["low_test_rel_l2_physics_decoder"],
        metrics["medium_test_rel_l2_physics_decoder"],
        metrics["high_test_rel_l2_physics_decoder"],
    ]
    basis_gaps = [
        0.0,
        metrics["medium_basis_rel_difference_from_low"],
        metrics["operator_basis_rel_difference"],
    ]
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.0), constrained_layout=True)
    axes[0].plot(labels, decoder_errors, "o-")
    axes[0].set_ylabel("current relative L2")
    axes[0].set_title("Low-operator decoder across fidelity ladder")
    axes[0].grid(alpha=0.3)
    axes[1].plot(labels, basis_gaps, "o-", color="tab:orange")
    axes[1].set_ylabel("basis rel difference from low")
    axes[1].set_title("Forward-operator gap")
    axes[1].grid(alpha=0.3)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_residual_maps(path: Path, high_field: np.ndarray, low_recon_field: np.ndarray) -> None:
    residual = high_field - low_recon_field
    plot_field_triplet(
        path,
        {"high observation": high_field, "low-op reconstruction": low_recon_field, "residual": residual},
        "Residual map caused by forward-operator mismatch",
    )


def add_acceptance_gates(metrics: Dict[str, object]) -> None:
    bridge = metrics.get("real_pypeec_bridge", {})
    bridge_cfg = metrics.get("real_pypeec_bridge_config", {})
    bridge_enabled = bool(bridge_cfg.get("enabled", False))
    bridge_gap = float(bridge.get("exp03_like_shape_gap_median", float("nan"))) if bridge else float("nan")
    gates = {
        "same_operator_decoder_is_nearly_exact": {
            "threshold": "low-test relative L2 < 1e-10",
            "value": metrics["low_test_rel_l2_physics_decoder"],
            "pass": metrics["low_test_rel_l2_physics_decoder"] < 1e-10,
        },
        "operator_mismatch_creates_visible_gap": {
            "threshold": "high-test relative L2 > 0.05",
            "value": metrics["high_test_rel_l2_physics_decoder"],
            "pass": metrics["high_test_rel_l2_physics_decoder"] > 0.05,
        },
        "calibration_reduces_high_fidelity_error": {
            "threshold": "calibrated/high error ratio < 0.01",
            "value": metrics["calibration_improvement_ratio"],
            "pass": metrics["calibration_improvement_ratio"] < 0.01,
        },
        "high_operator_is_materially_different": {
            "threshold": "basis relative difference > 0.1",
            "value": metrics["operator_basis_rel_difference"],
            "pass": metrics["operator_basis_rel_difference"] > 0.1,
        },
        "fidelity_ladder_is_monotone": {
            "threshold": "low decoder error < medium decoder error < high decoder error",
            "value": [
                metrics["low_test_rel_l2_physics_decoder"],
                metrics["medium_test_rel_l2_physics_decoder"],
                metrics["high_test_rel_l2_physics_decoder"],
            ],
            "pass": (
                metrics["low_test_rel_l2_physics_decoder"] < metrics["medium_test_rel_l2_physics_decoder"]
                and metrics["medium_test_rel_l2_physics_decoder"] < metrics["high_test_rel_l2_physics_decoder"]
            ),
        },
        "medium_operator_gap_is_between_low_and_high": {
            "threshold": "0 < medium basis gap < high basis gap",
            "value": [
                metrics["medium_basis_rel_difference_from_low"],
                metrics["operator_basis_rel_difference"],
            ],
            "pass": (
                metrics["medium_basis_rel_difference_from_low"] > 0.0
                and metrics["medium_basis_rel_difference_from_low"] < metrics["operator_basis_rel_difference"]
            ),
        },
        "calibrated_error_is_small_enough_for_gate": {
            "threshold": "calibrated high-test relative L2 < 0.01",
            "value": metrics["high_test_rel_l2_calibrated_400"],
            "pass": metrics["high_test_rel_l2_calibrated_400"] < 0.01,
        },
        "real_pypeec_bridge_artifact_is_valid": {
            "threshold": "exp07 real PyPEEC artifact exists, gates passed, and required cases completed",
            "value": {
                "enabled": bridge_enabled,
                "artifact_available": bridge.get("artifact_available", False) if bridge else False,
                "exp07_all_gates_passed": bridge.get("exp07_all_gates_passed", False) if bridge else False,
                "n_cases_completed": bridge.get("n_cases_completed", 0) if bridge else 0,
            },
            "pass": (
                (not bridge_enabled)
                or (
                    bool(bridge.get("artifact_available", False))
                    and bool(bridge.get("exp07_all_gates_passed", False))
                    and int(bridge.get("n_cases_completed", 0)) >= int(bridge_cfg.get("required_cases_completed", 0))
                )
            ),
        },
        "real_pypeec_bridge_gap_is_material_and_bounded": {
            "threshold": "exp03-like PyPEEC shape gap is finite and between configured material/bounded limits",
            "value": bridge_gap,
            "pass": (
                (not bridge_enabled)
                or (
                    np.isfinite(bridge_gap)
                    and bridge_gap >= float(bridge_cfg.get("min_exp03_like_shape_gap", 0.0))
                    and bridge_gap <= float(bridge_cfg.get("max_exp03_like_shape_gap", float("inf")))
                )
            ),
        },
    }
    metrics["acceptance_gates"] = gates
    metrics["all_acceptance_gates_passed"] = all(g["pass"] for g in gates.values())


def write_run_report(metrics: Dict[str, object]) -> None:
    gate_lines = "\n".join(
        f"- {name}: {'PASS' if gate['pass'] else 'FAIL'}; value={gate['value']}; threshold={gate['threshold']}"
        for name, gate in metrics["acceptance_gates"].items()
    )
    report = f"""# exp06 Run Report

## Role

MVP-5 anti-inverse-crime and multi-fidelity validation. This experiment proves
that same-operator synthetic testing can be over-optimistic, and that a small
high-fidelity calibration set can close an operator-mismatch gap.

## Gate Summary

Overall: {'PASS' if metrics['all_acceptance_gates_passed'] else 'FAIL'}

{gate_lines}

## Key Results

- low same-operator relative L2: `{metrics['low_test_rel_l2_physics_decoder']:.3e}`
- medium surrogate relative L2 before calibration: `{metrics['medium_test_rel_l2_physics_decoder']:.3f}`
- high surrogate relative L2 before calibration: `{metrics['high_test_rel_l2_physics_decoder']:.3f}`
- high surrogate relative L2 after 400 calibration samples: `{metrics['high_test_rel_l2_calibrated_400']:.3e}`
- medium basis relative difference: `{metrics['medium_basis_rel_difference_from_low']:.3f}`
- operator basis relative difference: `{metrics['operator_basis_rel_difference']:.3f}`
- real PyPEEC exp03-like shape gap: `{metrics.get('real_pypeec_bridge', {}).get('exp03_like_shape_gap_median', float('nan')):.3f}`
- real PyPEEC bridge table: `outputs/PYPEEC_BRIDGE_TABLE.md`

## Boundary

The medium and high-fidelity operators are still surrogates, not
COMSOL/FastHenry/QDM data. The PyPEEC bridge imports a real-solver exp07 artifact
as a read-only fidelity level; it does not calibrate or train on PyPEEC samples.
Passing this gate only justifies moving to real multi-fidelity stress tests.
"""
    (OUTPUTS / "RUN_REPORT.md").write_text(report, encoding="utf-8")


def write_pypeec_bridge_table(metrics: Dict[str, object]) -> None:
    bridge = metrics.get("real_pypeec_bridge", {})
    lines = [
        "# Real PyPEEC Fidelity Bridge\n\n",
        f"- enabled: `{bridge.get('enabled', False)}`\n",
        f"- artifact available: `{bridge.get('artifact_available', False)}`\n",
        f"- backend: `{bridge.get('backend_mode', 'not reported')}`\n",
        f"- PyPEEC version: `{bridge.get('pypeec_version', 'not reported')}`\n",
        f"- cases completed: `{bridge.get('n_cases_completed', 0)}` / `{bridge.get('n_cases_requested', 0)}`\n",
        f"- exp03-like shape gap median: `{float(bridge.get('exp03_like_shape_gap_median', float('nan'))):.6g}`\n",
        f"- finest-step convergence shape delta: `{float(bridge.get('max_finest_step_convergence_shape_delta', float('nan'))):.6g}`\n\n",
        "| case | PyPEEC-vs-center raw gap | scalar-fitted shape gap |\n",
        "|---|---:|---:|\n",
    ]
    raw = bridge.get("case_raw_gaps", {})
    shape = bridge.get("case_shape_gaps", {})
    for case in sorted(shape):
        lines.append(f"| `{case}` | {float(raw.get(case, float('nan'))):.6g} | {float(shape[case]):.6g} |\n")
    lines.append(
        "\nBoundary: this table imports exp07 real PyPEEC field gaps as an external "
        "fidelity signal. It is not a PyPEEC-calibrated decoder and not a model "
        "robustness result.\n"
    )
    (OUTPUTS / "PYPEEC_BRIDGE_TABLE.md").write_text("".join(lines), encoding="utf-8")


def main() -> None:
    OUTPUTS.mkdir(exist_ok=True, parents=True)
    DATA.mkdir(exist_ok=True, parents=True)
    cfg = load_config()
    rng = np.random.default_rng(cfg["seed"])
    grid = make_grid(cfg["grid"]["n"], cfg["grid"]["fov_um"], cfg["grid"]["measurement_z_um"])

    basis_low, names_low = build_basis_low(grid, cfg)
    basis_medium, names_medium = build_basis_medium_surrogate(grid, cfg)
    basis_high, names_high = build_basis_high_surrogate(grid, cfg)

    cur_cfg = cfg["currents"]
    n_train_low = int(cur_cfg["n_train_low"])
    n_test_low = int(cur_cfg["n_test_low"])
    n_test_high = int(cur_cfg["n_test_high"])
    max_abs_mA = float(cur_cfg["max_abs_mA"])
    noise_std_T = cfg["high_fidelity_surrogate"]["noise_std_uT"] * 1e-6

    X_train_low = sample_currents(rng, n_train_low, max_abs_mA)
    X_test_low = sample_currents(rng, n_test_low, max_abs_mA)
    X_test_medium = sample_currents(rng, n_test_high, max_abs_mA)
    X_cal_pool = sample_currents(rng, max(cur_cfg["calibration_sizes"]), max_abs_mA)
    X_test_high = sample_currents(rng, n_test_high, max_abs_mA)

    Y_test_low = synthesize_fields(X_test_low, basis_low, noise_std_T=0.0, rng=rng)
    Y_test_medium = synthesize_fields(X_test_medium, basis_medium, noise_std_T=0.0, rng=rng)
    Y_cal_high = synthesize_fields(X_cal_pool, basis_high, noise_std_T=noise_std_T, rng=rng)
    Y_test_high = synthesize_fields(X_test_high, basis_high, noise_std_T=noise_std_T, rng=rng)

    decoder = physics_decoder_from_low_basis(basis_low, ridge=float(cfg["ridge"]["lambda_physics"]))
    pred_low = predict_physics(Y_test_low, decoder)
    pred_medium_physics = predict_physics(Y_test_medium, decoder)
    pred_high_physics = predict_physics(Y_test_high, decoder)

    # Domain adaptation with a few high-fidelity samples: ridge over matched-filter features.
    feat_cal = matched_features(Y_cal_high, basis_low)
    feat_high_test = matched_features(Y_test_high, basis_low)
    calib_sizes = list(map(int, cur_cfg["calibration_sizes"]))
    cal_errors = []
    cal_preds = {}
    for n_cal in calib_sizes:
        W, b = fit_ridge(feat_cal[:n_cal], X_cal_pool[:n_cal], lam=float(cfg["ridge"]["lambda_calibration"]))
        pred = apply_ridge(feat_high_test, W, b)
        cal_preds[n_cal] = pred
        cal_errors.append(rel_l2(pred, X_test_high))

    pred_high_cal = cal_preds[calib_sizes[-1]]

    # Operator mismatch for a representative sample.
    sample_x = np.array([[12e-3, -9e-3, 5e-3]])
    B_low_sample = synthesize_fields(sample_x, basis_low)[0]
    B_high_sample = synthesize_fields(sample_x, basis_high, noise_std_T=0.0)[0]
    plot_field_triplet(
        OUTPUTS / "01_operator_mismatch.png",
        {
            "low operator": B_low_sample,
            "high surrogate": B_high_sample,
            "high-low difference": B_high_sample - B_low_sample,
        },
        "Same current, different forward operators",
    )

    low_err = rel_l2(pred_low, X_test_low)
    medium_err = rel_l2(pred_medium_physics, X_test_medium)
    high_err = rel_l2(pred_high_physics, X_test_high)
    high_cal_err = rel_l2(pred_high_cal, X_test_high)

    # Reconstruct one high field with low model and physics decoder to visualize residual.
    idx = 0
    x_hat = pred_high_physics[idx:idx+1]
    B_low_recon = synthesize_fields(x_hat, basis_low)[0]
    plot_residual_maps(OUTPUTS / "05_residual_maps.png", Y_test_high[idx], B_low_recon)

    metrics = {
        "experiment": "exp06-anti-inverse-crime-multifidelity-validation",
        "n_train_low": n_train_low,
        "n_test_low": n_test_low,
        "n_test_high": n_test_high,
        "low_test_rel_l2_physics_decoder": low_err,
        "low_test_mae_mA_physics_decoder": mae_mA(pred_low, X_test_low),
        "medium_test_rel_l2_physics_decoder": medium_err,
        "medium_test_mae_mA_physics_decoder": mae_mA(pred_medium_physics, X_test_medium),
        "high_test_rel_l2_physics_decoder": high_err,
        "high_test_mae_mA_physics_decoder": mae_mA(pred_high_physics, X_test_high),
        "inverse_crime_gap_ratio_high_over_low": float(high_err / (low_err + 1e-30)),
        "high_test_rel_l2_calibrated_400": high_cal_err,
        "high_test_mae_mA_calibrated_400": mae_mA(pred_high_cal, X_test_high),
        "calibration_improvement_ratio": float(high_cal_err / (high_err + 1e-30)),
        "medium_basis_rel_difference_from_low": float(np.linalg.norm(basis_medium - basis_low) / (np.linalg.norm(basis_low) + 1e-30)),
        "operator_basis_rel_difference": float(np.linalg.norm(basis_high - basis_low) / (np.linalg.norm(basis_low) + 1e-30)),
        "sample_operator_mismatch_rel_l2": float(np.linalg.norm(B_high_sample - B_low_sample) / (np.linalg.norm(B_low_sample) + 1e-30)),
        "per_channel_rel_l2_high_before": per_channel_rel_l2(pred_high_physics, X_test_high),
        "per_channel_rel_l2_high_after": per_channel_rel_l2(pred_high_cal, X_test_high),
        "fidelity_ladder": [
            {"name": "low", "basis_rel_difference_from_low": 0.0, "decoder_rel_l2": low_err},
            {
                "name": "medium",
                "basis_rel_difference_from_low": float(np.linalg.norm(basis_medium - basis_low) / (np.linalg.norm(basis_low) + 1e-30)),
                "decoder_rel_l2": medium_err,
            },
            {
                "name": "high",
                "basis_rel_difference_from_low": float(np.linalg.norm(basis_high - basis_low) / (np.linalg.norm(basis_low) + 1e-30)),
                "decoder_rel_l2": high_err,
            },
        ],
        "real_pypeec_bridge": load_real_pypeec_bridge(cfg),
        "real_pypeec_bridge_config": cfg.get("real_pypeec_bridge", {}),
        "calibration_sizes": calib_sizes,
        "calibration_curve_rel_l2": cal_errors,
        "noise_std_uT_high_surrogate": cfg["high_fidelity_surrogate"]["noise_std_uT"],
        "return_current_scale_high_surrogate": cfg["high_fidelity_surrogate"]["return_current_scale"],
        "psf_sigma_px_high_surrogate": cfg["high_fidelity_surrogate"]["psf_sigma_px"],
    }
    add_acceptance_gates(metrics)

    (OUTPUTS / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    write_run_report(metrics)
    write_pypeec_bridge_table(metrics)

    plot_error_bars(OUTPUTS / "02_inverse_crime_gap.png", metrics)
    plot_current_scatter(OUTPUTS / "03_current_scatter.png", X_test_high, pred_high_physics, pred_high_cal)
    plot_calibration_curve(OUTPUTS / "04_calibration_curve.png", calib_sizes, cal_errors, high_err, low_err)
    plot_fidelity_ladder(OUTPUTS / "06_fidelity_ladder.png", metrics)

    np.savez_compressed(
        DATA / "exp06_multifidelity_examples.npz",
        basis_low=basis_low,
        basis_medium=basis_medium,
        basis_high=basis_high,
        names_low=np.array(names_low),
        names_medium=np.array(names_medium),
        names_high=np.array(names_high),
        X_test_low=X_test_low,
        X_test_medium=X_test_medium,
        X_test_high=X_test_high,
        pred_low=pred_low,
        pred_medium_physics=pred_medium_physics,
        pred_high_physics=pred_high_physics,
        pred_high_calibrated=pred_high_cal,
        sample_current=sample_x,
        B_low_sample=B_low_sample,
        B_high_sample=B_high_sample,
        grid_X=grid.X,
        grid_Y=grid.Y,
    )

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
