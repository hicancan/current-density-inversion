from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import fftconvolve
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = Path(__file__).resolve().parent
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from current_inversion.evidence import (  # noqa: E402
    binary_auc,
    calibration_curve,
    generative_hypothesis_score,
    null_via_hypothesis_evidence,
    return_path_hypothesis,
    selective_risk_curve,
    summarize_evidence_rows,
    summarize_return_path_hypotheses,
)
from current_inversion.protocols import build_pypeec_heldout_split_protocol  # noqa: E402


CHANNELS = ["J1x", "J1y", "J2x", "J2y", "s1"]
MU0 = 4.0e-7 * np.pi


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_dataset_path(cfg: dict[str, Any]) -> Path:
    p = Path(cfg["dataset_path"])
    if not p.is_absolute():
        p = ROOT / p
    return p.resolve()


def resolve_root_path(path_value: str) -> Path:
    p = Path(path_value)
    if not p.is_absolute():
        p = ROOT / p
    return p.resolve()


def load_pypeec_operator_stress_bridge(cfg: dict[str, Any]) -> dict[str, Any]:
    """Load exp07 real PyPEEC metrics as a frozen operator-stress artifact."""
    bridge_cfg = cfg.get("pypeec_operator_stress_bridge", {})
    if not bool(bridge_cfg.get("enabled", False)):
        return {"enabled": False}

    metrics_path = resolve_root_path(str(bridge_cfg["metrics_path"]))
    if not metrics_path.exists():
        return {
            "enabled": True,
            "metrics_path": str(metrics_path),
            "artifact_available": False,
            "boundary": "exp07 metrics artifact is missing; no PyPEEC operator-stress bridge claim can be made.",
        }

    exp07 = json.loads(metrics_path.read_text(encoding="utf-8"))
    summary = exp07.get("summary", {})
    case_metrics = exp07.get("case_metrics", [])
    exp03_like_cases = set(summary.get("exp03_like_completed_cases", []))
    exp03_like_rows = [row for row in case_metrics if row.get("case") in exp03_like_cases]
    return {
        "enabled": True,
        "metrics_path": str(metrics_path),
        "artifact_available": True,
        "mode": "frozen_read_only_bridge",
        "calibration_split": "none",
        "used_for_training": False,
        "used_for_validation_thresholds": False,
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
        "case_shape_gaps": {
            row["case"]: float(row.get("pypeec_centerline_shape_rel_l2", float("nan")))
            for row in case_metrics
        },
        "case_raw_gaps": {
            row["case"]: float(row.get("pypeec_vs_center_rel_l2", float("nan")))
            for row in case_metrics
        },
        "boundary": (
            "This bridge reports real PyPEEC field-level operator mismatch from exp07. "
            "It is not a trained-model PyPEEC evaluation because the current exp07 "
            "cases are small solver-validation geometries, not the full exp03 dataset."
        ),
    }


def load_pypeec_frozen_inference_dataset(cfg: dict[str, Any]) -> dict[str, Any]:
    pcfg = cfg.get("pypeec_frozen_inference", {})
    if not bool(pcfg.get("enabled", False)):
        return {"enabled": False}

    dataset_path = resolve_root_path(str(pcfg["dataset_path"]))
    if not dataset_path.exists():
        return {
            "enabled": True,
            "dataset_path": str(dataset_path),
            "artifact_available": False,
        }

    data = np.load(dataset_path, allow_pickle=False)
    return {
        "enabled": True,
        "artifact_available": True,
        "dataset_path": str(dataset_path),
        "x": data["x"].astype(np.float32),
        "y": data["y"].astype(np.float32),
        "B_centerline": data["B_centerline"].astype(np.float32),
        "B_pypeec": data["B_pypeec"].astype(np.float32),
        "truth": data["truth"].astype(np.float32),
        "case_name": data["case_name"].astype(str),
        "case_type": data["case_type"].astype(str),
        "is_exp03_like": data["is_exp03_like"].astype(bool),
        "split": data["split"].astype(str),
        "metadata_json": str(data["metadata_json"]),
    }


def choose_device(name: str) -> torch.device:
    if name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(name)


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_dataset(path: Path) -> dict[str, Any]:
    d = np.load(path, allow_pickle=False)
    B_obs = d["B_obs"].astype(np.float32).transpose(0, 3, 1, 2)
    B_clean = d["B_clean"].astype(np.float32).transpose(0, 3, 1, 2)
    truth = d["truth"].astype(np.float32)
    split = d["split"].astype(str)
    return {
        "B_obs": B_obs,
        "B_clean": B_clean,
        "truth": truth,
        "split": split,
        "x": d["x"].astype(np.float32),
        "y": d["y"].astype(np.float32),
    }


def split_arrays(data: dict[str, Any], split_name: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mask = data["split"] == split_name
    return data["B_obs"][mask], data["truth"][mask], data["B_clean"][mask]


def channel_stats(a: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = a.mean(axis=(0, 2, 3), keepdims=True)
    std = a.std(axis=(0, 2, 3), keepdims=True) + 1e-8
    return mean.astype(np.float32), std.astype(np.float32)


def normalize(a: np.ndarray, stats: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
    mean, std = stats
    return ((a - mean) / std).astype(np.float32)


def denormalize(a: np.ndarray, stats: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
    mean, std = stats
    return (a * std + mean).astype(np.float32)


def denormalize_torch(a: torch.Tensor, mean: torch.Tensor, std: torch.Tensor) -> torch.Tensor:
    return a * std + mean


def gaussian_blur_fft_batch(x: np.ndarray, sigma_px: float) -> np.ndarray:
    if sigma_px <= 0:
        return x.astype(np.float32)
    h, w = x.shape[-2:]
    ky = np.fft.fftfreq(h)[:, None]
    kx = np.fft.fftfreq(w)[None, :]
    filt = np.exp(-2.0 * (np.pi**2) * (sigma_px**2) * (kx * kx + ky * ky)).astype(np.float32)
    blurred = np.fft.ifft2(np.fft.fft2(x, axes=(-2, -1)) * filt[None, None, :, :], axes=(-2, -1)).real
    return blurred.astype(np.float32)


def make_stress_inputs(x: np.ndarray, cfg: dict[str, Any], seed: int) -> dict[str, np.ndarray]:
    scfg = cfg.get("stress", {})
    if not scfg.get("enabled", False):
        return {}
    rng = np.random.default_rng(seed)
    out: dict[str, np.ndarray] = {}
    max_abs = float(np.max(np.abs(x)) + 1e-30)

    sigma = float(scfg.get("noise_relative_to_max_abs_B", 0.0)) * max_abs
    out["noise"] = (x + rng.normal(0.0, sigma, size=x.shape)).astype(np.float32)

    out["psf_blur"] = gaussian_blur_fft_batch(x, float(scfg.get("psf_sigma_px", 0.0)))

    h, w = x.shape[-2:]
    gx = np.linspace(-1.0, 1.0, w, dtype=np.float32)[None, None, None, :]
    gy = np.linspace(-1.0, 1.0, h, dtype=np.float32)[None, None, :, None]
    gain = 1.0 + float(scfg.get("tilt_gain_fraction", 0.0)) * (0.65 * gx - 0.35 * gy)
    out["tilt_gain"] = (x * gain).astype(np.float32)

    mix = np.asarray(scfg.get("channel_mixing_matrix", np.eye(x.shape[1])), dtype=np.float32)
    out["channel_mismatch"] = np.einsum("ij,njhw->nihw", mix, x).astype(np.float32)

    combo = gaussian_blur_fft_batch(out["channel_mismatch"], float(scfg.get("psf_sigma_px", 0.0)))
    combo = combo + rng.normal(0.0, sigma, size=combo.shape)
    out["combined"] = (combo * gain).astype(np.float32)
    return out


def make_operator_stress_inputs(
    truth: np.ndarray,
    b_clean: np.ndarray,
    data_x: np.ndarray,
    data_y: np.ndarray,
    cfg: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    ocfg = cfg.get("operator_stress", {})
    if not ocfg.get("enabled", False):
        return {}
    fw_forward = build_finite_width_return_forward_kernels(data_x, data_y, cfg)
    b_fw = raster_physical_forward(truth, fw_forward)
    return {
        "finite_width_return": {
            "B": b_fw.astype(np.float32),
            "input_gap_rel_l2_to_clean": rel_l2(b_fw, b_clean),
            "model": "finite-width filaments plus weak return-current surrogate",
        }
    }


def kernel_for_segment(x: np.ndarray, y: np.ndarray, z_src: float, sensor_z: float, dl: np.ndarray, dx: float) -> np.ndarray:
    """Biot-Savart linear-convolution kernel per raster-map density value."""
    n = len(x)
    offsets = (np.arange(-(n - 1), n, dtype=np.float64) * dx)
    ox, oy = np.meshgrid(offsets, offsets, indexing="xy")
    rz = np.full_like(ox, sensor_z - z_src)
    r = np.stack([ox, oy, rz], axis=-1)
    r2 = np.sum(r * r, axis=-1) + 1e-24
    r3 = r2 ** 1.5
    # Raster maps store current/dx, so one active cell has current = value * dx.
    cross = np.cross(dl.astype(np.float64), r)
    return (MU0 / (4.0 * np.pi) * dx * cross / r3[..., None]).astype(np.float32)


def kernel_for_segment_offset(
    x: np.ndarray,
    y: np.ndarray,
    z_src: float,
    sensor_z: float,
    dl: np.ndarray,
    dx: float,
    source_offset: np.ndarray,
) -> np.ndarray:
    """Convolution kernel for a source filament shifted within a finite trace."""
    n = len(x)
    offsets = (np.arange(-(n - 1), n, dtype=np.float64) * dx)
    ox, oy = np.meshgrid(offsets, offsets, indexing="xy")
    rz = np.full_like(ox, sensor_z - (z_src + float(source_offset[2])))
    r = np.stack([ox - float(source_offset[0]), oy - float(source_offset[1]), rz], axis=-1)
    r2 = np.sum(r * r, axis=-1) + 1e-24
    r3 = r2 ** 1.5
    cross = np.cross(dl.astype(np.float64), r)
    return (MU0 / (4.0 * np.pi) * dx * cross / r3[..., None]).astype(np.float32)


def build_physical_forward_kernels(x: np.ndarray, y: np.ndarray, cfg: dict[str, Any]) -> dict[str, Any]:
    pcfg = cfg["physical_forward"]
    dx = float(x[1] - x[0])
    z1 = float(pcfg["layer1_z_m"])
    z2 = float(pcfg["layer2_z_m"])
    sensor_z = float(pcfg.get("sensor_z_m", 0.0))
    kernels = np.stack(
        [
            kernel_for_segment(x, y, z1, sensor_z, np.array([dx, 0.0, 0.0]), dx),
            kernel_for_segment(x, y, z1, sensor_z, np.array([0.0, dx, 0.0]), dx),
            kernel_for_segment(x, y, z2, sensor_z, np.array([dx, 0.0, 0.0]), dx),
            kernel_for_segment(x, y, z2, sensor_z, np.array([0.0, dx, 0.0]), dx),
            kernel_for_segment(x, y, 0.5 * (z1 + z2), sensor_z, np.array([0.0, 0.0, z2 - z1]), dx),
        ],
        axis=0,
    )
    return {"kernels": kernels, "dx": dx, "layer1_z_m": z1, "layer2_z_m": z2, "sensor_z_m": sensor_z}


def finite_width_channel_kernel(
    x: np.ndarray,
    y: np.ndarray,
    z_src: float,
    sensor_z: float,
    dl: np.ndarray,
    dx: float,
    normal: np.ndarray,
    width_m: float,
    n_filaments: int,
    return_scale: float,
    ground_z_m: float,
) -> np.ndarray:
    offsets = np.linspace(-0.5, 0.5, int(n_filaments), dtype=np.float64) * float(width_m)
    acc = np.zeros((2 * len(x) - 1, 2 * len(y) - 1, 3), dtype=np.float32)
    for off in offsets:
        shift = normal.astype(np.float64) * off
        acc += kernel_for_segment_offset(x, y, z_src, sensor_z, dl / len(offsets), dx, shift)
        acc += kernel_for_segment_offset(
            x,
            y,
            ground_z_m,
            sensor_z,
            -return_scale * dl / len(offsets),
            dx,
            shift,
        )
    return acc.astype(np.float32)


def finite_width_via_kernel(
    x: np.ndarray,
    y: np.ndarray,
    z_src: float,
    sensor_z: float,
    dl: np.ndarray,
    dx: float,
    via_radius_m: float,
) -> np.ndarray:
    offsets = [
        np.array([0.0, 0.0, 0.0]),
        np.array([via_radius_m, 0.0, 0.0]),
        np.array([-via_radius_m, 0.0, 0.0]),
        np.array([0.0, via_radius_m, 0.0]),
        np.array([0.0, -via_radius_m, 0.0]),
    ]
    acc = np.zeros((2 * len(x) - 1, 2 * len(y) - 1, 3), dtype=np.float32)
    for off in offsets:
        acc += kernel_for_segment_offset(x, y, z_src, sensor_z, dl / len(offsets), dx, off)
    return acc.astype(np.float32)


def build_finite_width_return_forward_kernels(x: np.ndarray, y: np.ndarray, cfg: dict[str, Any]) -> dict[str, Any]:
    pcfg = cfg["physical_forward"]
    ocfg = cfg.get("operator_stress", {})
    dx = float(x[1] - x[0])
    z1 = float(pcfg["layer1_z_m"])
    z2 = float(pcfg["layer2_z_m"])
    sensor_z = float(pcfg.get("sensor_z_m", 0.0))
    width_m = float(ocfg.get("trace_width_m", 28e-6))
    via_radius_m = float(ocfg.get("via_radius_m", 18e-6))
    n_filaments = int(ocfg.get("n_width_filaments", 3))
    return_scale = float(ocfg.get("return_scale", 0.22))
    ground_z_m = float(ocfg.get("ground_z_m", -0.24e-3))
    kernels = np.stack(
        [
            finite_width_channel_kernel(x, y, z1, sensor_z, np.array([dx, 0.0, 0.0]), dx, np.array([0.0, 1.0, 0.0]), width_m, n_filaments, return_scale, ground_z_m),
            finite_width_channel_kernel(x, y, z1, sensor_z, np.array([0.0, dx, 0.0]), dx, np.array([1.0, 0.0, 0.0]), width_m, n_filaments, return_scale, ground_z_m),
            finite_width_channel_kernel(x, y, z2, sensor_z, np.array([dx, 0.0, 0.0]), dx, np.array([0.0, 1.0, 0.0]), width_m, n_filaments, return_scale, ground_z_m),
            finite_width_channel_kernel(x, y, z2, sensor_z, np.array([0.0, dx, 0.0]), dx, np.array([1.0, 0.0, 0.0]), width_m, n_filaments, return_scale, ground_z_m),
            finite_width_via_kernel(x, y, 0.5 * (z1 + z2), sensor_z, np.array([0.0, 0.0, z2 - z1]), dx, via_radius_m),
        ],
        axis=0,
    )
    return {"kernels": kernels, "dx": dx, "layer1_z_m": z1, "layer2_z_m": z2, "sensor_z_m": sensor_z}


def raster_physical_forward(y_map: np.ndarray, forward: dict[str, Any]) -> np.ndarray:
    kernels = forward["kernels"]
    n = y_map.shape[0]
    out = np.zeros((n, 3, y_map.shape[-2], y_map.shape[-1]), dtype=np.float32)
    for i in range(n):
        for ch in range(5):
            src = y_map[i, ch]
            if not np.any(src):
                continue
            for comp in range(3):
                out[i, comp] += fftconvolve(src, kernels[ch, :, :, comp], mode="same").astype(np.float32)
    return out


def raster_physical_adjoint(b_map: np.ndarray, forward: dict[str, Any]) -> np.ndarray:
    kernels = forward["kernels"]
    n = b_map.shape[0]
    out = np.zeros((n, 5, b_map.shape[-2], b_map.shape[-1]), dtype=np.float32)
    for i in range(n):
        for ch in range(5):
            acc = np.zeros(b_map.shape[-2:], dtype=np.float32)
            for comp in range(3):
                acc += fftconvolve(b_map[i, comp], kernels[ch, ::-1, ::-1, comp], mode="same").astype(np.float32)
            out[i, ch] = acc
    return out


def estimate_forward_lipschitz(forward: dict[str, Any], shape: tuple[int, int, int], n_iter: int = 8) -> float:
    rng = np.random.default_rng(12345)
    y = rng.normal(size=(1,) + shape).astype(np.float32)
    y /= np.linalg.norm(y) + 1e-30
    val = 1.0
    for _ in range(n_iter):
        ay = raster_physical_forward(y, forward)
        aty = raster_physical_adjoint(ay, forward)
        val = float(np.linalg.norm(aty))
        y = aty / (val + 1e-30)
    return max(val, 1e-30)


def physics_tikhonov_inverse(b_map: np.ndarray, forward: dict[str, Any], cfg: dict[str, Any]) -> np.ndarray:
    pcfg = cfg["physics_baseline"]
    lam = float(pcfg["tikhonov_lambda"])
    n_iter = int(pcfg["landweber_iterations"])
    lipschitz = float(forward.get("lipschitz", 1.0))
    step = float(pcfg.get("step_scale", 0.8)) / (lipschitz + lam)
    y = np.zeros((b_map.shape[0], 5, b_map.shape[-2], b_map.shape[-1]), dtype=np.float32)
    for _ in range(n_iter):
        residual = raster_physical_forward(y, forward) - b_map
        grad = raster_physical_adjoint(residual, forward) + lam * y
        y = (y - step * grad).astype(np.float32)
    return y


class ConvBlock(nn.Module):
    def __init__(self, in_ch: int, out_ch: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.GroupNorm(4 if out_ch >= 4 else 1, out_ch),
            nn.SiLU(),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.GroupNorm(4 if out_ch >= 4 else 1, out_ch),
            nn.SiLU(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class UNetLite(nn.Module):
    def __init__(self, in_ch: int = 3, out_ch: int = 5, base: int = 24):
        super().__init__()
        self.enc1 = ConvBlock(in_ch, base)
        self.enc2 = ConvBlock(base, base * 2)
        self.bottleneck = ConvBlock(base * 2, base * 4)
        self.dec2 = ConvBlock(base * 4 + base * 2, base * 2)
        self.dec1 = ConvBlock(base * 2 + base, base)
        self.out = nn.Conv2d(base, out_ch, 1)
        self.pool = nn.MaxPool2d(2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x1 = self.enc1(x)
        x2 = self.enc2(self.pool(x1))
        xb = self.bottleneck(self.pool(x2))
        u2 = torch.nn.functional.interpolate(xb, size=x2.shape[-2:], mode="bilinear", align_corners=False)
        d2 = self.dec2(torch.cat([u2, x2], dim=1))
        u1 = torch.nn.functional.interpolate(d2, size=x1.shape[-2:], mode="bilinear", align_corners=False)
        d1 = self.dec1(torch.cat([u1, x1], dim=1))
        return self.out(d1)


def divergence_torch(jx: torch.Tensor, jy: torch.Tensor) -> torch.Tensor:
    out = torch.zeros_like(jx)
    out[..., :, 1:-1] += 0.5 * (jx[..., :, 2:] - jx[..., :, :-2])
    out[..., 1:-1, :] += 0.5 * (jy[..., 2:, :] - jy[..., :-2, :])
    return out


def topology_residual_torch(y: torch.Tensor, mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    r1 = divergence_torch(y[:, 0], y[:, 1]) + y[:, 4]
    r2 = divergence_torch(y[:, 2], y[:, 3]) - y[:, 4]
    return r1 * mask, r2 * mask


def topology_loss_torch(y: torch.Tensor, mask: torch.Tensor, scale: torch.Tensor) -> torch.Tensor:
    r1, r2 = topology_residual_torch(y, mask)
    return (torch.mean(r1 * r1) + torch.mean(r2 * r2)) / scale


def train_unet(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_val: np.ndarray,
    y_val: np.ndarray,
    y_stats: tuple[np.ndarray, np.ndarray],
    cfg: dict[str, Any],
    device: torch.device,
    topology_lambda: float,
    epochs_override: int | None = None,
) -> tuple[UNetLite, list[dict[str, float]]]:
    tcfg = cfg["training"]
    model = UNetLite(base=int(tcfg["base_channels"])).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=float(tcfg["learning_rate"]), weight_decay=float(tcfg["weight_decay"]))
    ds = TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train))
    loader = DataLoader(ds, batch_size=int(tcfg["batch_size"]), shuffle=True)
    x_val_t = torch.from_numpy(x_val).to(device)
    y_val_t = torch.from_numpy(y_val).to(device)
    y_mean_t = torch.from_numpy(y_stats[0]).to(device)
    y_std_t = torch.from_numpy(y_stats[1]).to(device)
    mask = torch.zeros((1, y_train.shape[-2], y_train.shape[-1]), dtype=torch.float32, device=device)
    mask[..., 2:-2, 2:-2] = 1.0
    topo_scale = torch.tensor(float(np.mean(denormalize(y_train, y_stats) ** 2) + 1e-12), device=device)
    use_amp = bool(tcfg.get("amp", False)) and device.type == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
    hist: list[dict[str, float]] = []
    n_epochs = int(epochs_override if epochs_override is not None else tcfg["epochs"])
    for epoch in range(n_epochs):
        model.train()
        total = 0.0
        for xb, yb in loader:
            xb = xb.to(device)
            yb = yb.to(device)
            opt.zero_grad(set_to_none=True)
            with torch.amp.autocast(device_type="cuda", enabled=use_amp):
                pred = model(xb)
                loss_sup = torch.mean((pred - yb) ** 2)
                pred_phys = denormalize_torch(pred, y_mean_t, y_std_t)
                loss_topo = topology_loss_torch(pred_phys, mask, topo_scale)
                loss = loss_sup + float(topology_lambda) * loss_topo
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
            total += float(loss.detach().cpu()) * xb.shape[0]
        model.eval()
        with torch.no_grad():
            pred_val = model(x_val_t)
            val_mse = float(torch.mean((pred_val - y_val_t) ** 2).detach().cpu())
        hist.append({"epoch": epoch + 1, "train_loss": total / len(ds), "val_mse": val_mse})
    return model, hist


def predict_model(model: nn.Module, x: np.ndarray, device: torch.device, batch_size: int) -> np.ndarray:
    model.eval()
    outs = []
    with torch.no_grad():
        for i in range(0, len(x), batch_size):
            xb = torch.from_numpy(x[i : i + batch_size]).to(device)
            outs.append(model(xb).detach().cpu().numpy())
    return np.concatenate(outs, axis=0).astype(np.float32)


def fit_ridge_dual(x_train: np.ndarray, y_train: np.ndarray, lam: float) -> tuple[np.ndarray, np.ndarray, tuple[int, ...]]:
    x = x_train.reshape(x_train.shape[0], -1).astype(np.float64)
    y = y_train.reshape(y_train.shape[0], -1).astype(np.float64)
    x_mean = x.mean(axis=0, keepdims=True)
    x0 = x - x_mean
    gram = x0 @ x0.T + lam * np.eye(x0.shape[0])
    alpha = np.linalg.solve(gram, y)
    return alpha.astype(np.float32), x_mean.astype(np.float32), y_train.shape[1:]


def apply_ridge_dual(x: np.ndarray, x_train: np.ndarray, alpha: np.ndarray, x_mean: np.ndarray, out_shape: tuple[int, ...]) -> np.ndarray:
    xt = x_train.reshape(x_train.shape[0], -1).astype(np.float32) - x_mean
    xf = x.reshape(x.shape[0], -1).astype(np.float32) - x_mean
    pred = (xf @ xt.T) @ alpha
    return pred.reshape((x.shape[0],) + out_shape).astype(np.float32)


def fit_forward_proxy(y_train: np.ndarray, b_train: np.ndarray, lam: float) -> tuple[np.ndarray, np.ndarray, tuple[int, ...]]:
    return fit_ridge_dual(y_train, b_train, lam)


def apply_forward_proxy(y: np.ndarray, y_train: np.ndarray, proxy: tuple[np.ndarray, np.ndarray, tuple[int, ...]]) -> np.ndarray:
    alpha, y_mean, out_shape = proxy
    return apply_ridge_dual(y, y_train, alpha, y_mean, out_shape)


def divergence_np(jx: np.ndarray, jy: np.ndarray) -> np.ndarray:
    out = np.zeros_like(jx)
    out[..., :, 1:-1] += 0.5 * (jx[..., :, 2:] - jx[..., :, :-2])
    out[..., 1:-1, :] += 0.5 * (jy[..., 2:, :] - jy[..., :-2, :])
    return out


def posthoc_topology_projection(pred: np.ndarray) -> np.ndarray:
    out = pred.copy()
    d1 = divergence_np(out[:, 0], out[:, 1])
    d2 = divergence_np(out[:, 2], out[:, 3])
    out[:, 4] = 0.5 * (d2 - d1)
    return out


def rel_l2(pred: np.ndarray, truth: np.ndarray) -> float:
    return float(np.linalg.norm(pred - truth) / (np.linalg.norm(truth) + 1e-30))


def stable_channel_metrics(pred: np.ndarray, truth: np.ndarray) -> dict[str, Any]:
    """Channel metrics that remain meaningful when a truth channel is inactive."""
    truth_norms = [float(np.linalg.norm(truth[:, i])) for i in range(truth.shape[1])]
    pred_norms = [float(np.linalg.norm(pred[:, i])) for i in range(pred.shape[1])]
    global_norm = float(np.linalg.norm(truth))
    active_threshold = max(1e-8 * global_norm, 1e-12)
    max_truth = float(np.max(np.abs(truth))) + 1e-12
    rel = []
    active = []
    rmse_scale = []
    for i, nrm in enumerate(truth_norms):
        is_active = nrm > active_threshold
        active.append(bool(is_active))
        rel.append(float(np.linalg.norm(pred[:, i] - truth[:, i]) / nrm) if is_active else None)
        rmse_scale.append(float(np.sqrt(np.mean((pred[:, i] - truth[:, i]) ** 2)) / max_truth))
    return {
        "truth_channel_l2_norm": truth_norms,
        "pred_channel_l2_norm": pred_norms,
        "active_channel_mask": active,
        "active_channel_threshold": float(active_threshold),
        "per_channel_rel_l2": rel,
        "per_channel_rmse_current_scale": rmse_scale,
    }


def layer_leakage_proxy(pred: np.ndarray, truth: np.ndarray) -> float:
    p1 = np.sqrt(pred[:, 0] ** 2 + pred[:, 1] ** 2)
    p2 = np.sqrt(pred[:, 2] ** 2 + pred[:, 3] ** 2)
    t1 = np.sqrt(truth[:, 0] ** 2 + truth[:, 1] ** 2)
    t2 = np.sqrt(truth[:, 2] ** 2 + truth[:, 3] ** 2)
    th1 = np.percentile(t1, 55)
    th2 = np.percentile(t2, 55)
    m1 = t1 <= th1
    m2 = t2 <= th2
    if not np.any(m1):
        m1 = np.ones_like(t1, dtype=bool)
    if not np.any(m2):
        m2 = np.ones_like(t2, dtype=bool)
    leak = (np.mean(p1[m1] ** 2) + np.mean(p2[m2] ** 2)) / (np.mean(p1**2 + p2**2) + 1e-12)
    return float(leak)


def via_metrics(pred: np.ndarray, truth: np.ndarray) -> dict[str, float]:
    errs = []
    hits = 0
    truth_present = 0
    pred_present = 0
    presence_tp = 0
    false_positive = 0
    no_via = 0
    global_scale = float(np.max(np.abs(truth[:, 4])) + 1e-12)
    presence_threshold = 0.20 * global_scale
    for p, t in zip(pred[:, 4], truth[:, 4]):
        t_present = bool(np.max(np.abs(t)) > presence_threshold)
        p_present = bool(np.max(np.abs(p)) > presence_threshold)
        truth_present += int(t_present)
        pred_present += int(p_present)
        presence_tp += int(t_present and p_present)
        if not t_present:
            no_via += 1
            false_positive += int(p_present)
            continue
        py, px = np.unravel_index(int(np.argmax(np.abs(p))), p.shape)
        ty, tx = np.unravel_index(int(np.argmax(np.abs(t))), t.shape)
        e = float(((px - tx) ** 2 + (py - ty) ** 2) ** 0.5)
        errs.append(e)
        hits += e <= 2.0
    precision = presence_tp / max(pred_present, 1)
    recall = presence_tp / max(truth_present, 1)
    f1 = 2.0 * precision * recall / max(precision + recall, 1e-30)
    return {
        "via_loc_error_px_mean": float(np.mean(errs)) if errs else 0.0,
        "via_hit_rate_within_2px": float(hits / len(errs)) if errs else 1.0,
        "via_presence_precision": float(precision),
        "via_presence_recall": float(recall),
        "via_presence_f1": float(f1),
        "via_false_positive_rate_no_via": float(false_positive / max(no_via, 1)),
        "via_presence_threshold": float(presence_threshold),
    }


def via_score_maps_from_residual(pred: np.ndarray, b_obs: np.ndarray, forward: dict[str, Any]) -> np.ndarray:
    """Score via candidates from the magnetic residual after removing sheet current.

    This is a detector diagnostic, not a replacement for the reconstructed s1
    channel. The score is the absolute adjoint response of the vertical-via
    channel to B_obs - F(J1,J2,s=0).
    """
    sheet = pred.copy()
    sheet[:, 4] = 0.0
    residual = b_obs - raster_physical_forward(sheet, forward)
    return np.abs(raster_physical_adjoint(residual, forward)[:, 4]).astype(np.float32)


def signed_via_score_maps_from_residual(pred: np.ndarray, b_obs: np.ndarray, forward: dict[str, Any]) -> np.ndarray:
    sheet = pred.copy()
    sheet[:, 4] = 0.0
    residual = b_obs - raster_physical_forward(sheet, forward)
    return raster_physical_adjoint(residual, forward)[:, 4].astype(np.float32)


def raw_via_score_maps(b_obs: np.ndarray, forward: dict[str, Any]) -> np.ndarray:
    return np.abs(raster_physical_adjoint(b_obs, forward)[:, 4]).astype(np.float32)


def dog_score_maps(score_maps: np.ndarray, sigma_px: float) -> np.ndarray:
    if sigma_px <= 0:
        return np.maximum(score_maps, 0.0).astype(np.float32)
    blurred = gaussian_blur_fft_batch(score_maps[:, None], sigma_px)[:, 0]
    return np.maximum(score_maps - blurred, 0.0).astype(np.float32)


def calibrate_via_score_threshold(
    score_maps: np.ndarray,
    truth: np.ndarray,
    false_positive_quantile: float = 0.95,
    threshold_multiplier: float = 1.0,
) -> dict[str, float]:
    truth_scale = float(np.max(np.abs(truth[:, 4])) + 1e-12)
    truth_present = np.max(np.abs(truth[:, 4]).reshape(truth.shape[0], -1), axis=1) > 0.20 * truth_scale
    peaks = np.max(score_maps.reshape(score_maps.shape[0], -1), axis=1)
    pos = peaks[truth_present]
    neg = peaks[~truth_present]
    if len(pos) and len(neg):
        threshold = 0.5 * (float(np.median(pos)) + float(np.median(neg)))
    elif len(pos):
        threshold = 0.5 * float(np.median(pos))
    else:
        threshold = float(np.percentile(peaks, 95))
    if len(neg):
        fp_threshold = float(np.quantile(neg, false_positive_quantile))
        threshold = max(float(threshold), fp_threshold)
    threshold *= float(threshold_multiplier)
    return {
        "presence_threshold": float(threshold),
        "median_present_peak": float(np.median(pos)) if len(pos) else 0.0,
        "median_absent_peak": float(np.median(neg)) if len(neg) else 0.0,
        "false_positive_quantile": float(false_positive_quantile),
        "threshold_multiplier": float(threshold_multiplier),
        "score_separation_median_present_over_absent": float(
            (np.median(pos) if len(pos) else 0.0) / ((np.median(neg) if len(neg) else 0.0) + 1e-30)
        ),
    }


def via_detector_metrics(score_maps: np.ndarray, truth: np.ndarray, threshold: float) -> dict[str, float]:
    truth_scale = float(np.max(np.abs(truth[:, 4])) + 1e-12)
    truth_threshold = 0.20 * truth_scale
    errs = []
    hits = 0
    truth_present_count = 0
    pred_present_count = 0
    presence_tp = 0
    false_positive = 0
    no_via = 0
    peak_scores = []
    for score, target in zip(score_maps, truth[:, 4]):
        t_present = bool(np.max(np.abs(target)) > truth_threshold)
        peak = float(np.max(score))
        p_present = bool(peak > threshold)
        peak_scores.append(peak)
        truth_present_count += int(t_present)
        pred_present_count += int(p_present)
        presence_tp += int(t_present and p_present)
        if not t_present:
            no_via += 1
            false_positive += int(p_present)
            continue
        py, px = np.unravel_index(int(np.argmax(score)), score.shape)
        ty, tx = np.unravel_index(int(np.argmax(np.abs(target))), target.shape)
        err = float(((px - tx) ** 2 + (py - ty) ** 2) ** 0.5)
        errs.append(err)
        hits += err <= 2.0
    precision = presence_tp / max(pred_present_count, 1)
    recall = presence_tp / max(truth_present_count, 1)
    f1 = 2.0 * precision * recall / max(precision + recall, 1e-30)
    return {
        "via_loc_error_px_mean": float(np.mean(errs)) if errs else 0.0,
        "via_hit_rate_within_2px": float(hits / len(errs)) if errs else 1.0,
        "via_presence_precision": float(precision),
        "via_presence_recall": float(recall),
        "via_presence_f1": float(f1),
        "via_false_positive_rate_no_via": float(false_positive / max(no_via, 1)),
        "presence_threshold": float(threshold),
        "peak_score_median": float(np.median(peak_scores)) if peak_scores else 0.0,
    }


def build_via_detection_benchmark(
    calibration_truth: np.ndarray,
    calibration_b_obs: np.ndarray,
    calibration_preds: dict[str, np.ndarray],
    split_truth: dict[str, np.ndarray],
    split_b_obs: dict[str, np.ndarray],
    split_preds: dict[str, dict[str, np.ndarray]],
    forward: dict[str, Any],
    detector_cfg: dict[str, Any],
) -> dict[str, Any]:
    dog_sigma = float(detector_cfg.get("dog_sigma_px", 2.0))
    fp_quantile = float(detector_cfg.get("false_positive_quantile", 1.0))
    strict_multiplier = float(detector_cfg.get("strict_threshold_multiplier", 1.35))
    calibration_oracle_sheet = calibration_truth.copy()
    calibration_oracle_sheet[:, 4] = 0.0
    detector_calibration_scores = {
        "raw_adjoint": raw_via_score_maps(calibration_b_obs, forward),
        "oracle_sheet_residual": via_score_maps_from_residual(calibration_oracle_sheet, calibration_b_obs, forward),
    }
    for name, pred in calibration_preds.items():
        detector_calibration_scores[f"{name}_sheet_residual"] = via_score_maps_from_residual(pred, calibration_b_obs, forward)

    for name, score in list(detector_calibration_scores.items()):
        detector_calibration_scores[f"{name}_dog_fp_controlled"] = dog_score_maps(score, dog_sigma)

    thresholds = {
        name: calibrate_via_score_threshold(
            score,
            calibration_truth,
            false_positive_quantile=fp_quantile,
            threshold_multiplier=(strict_multiplier if name.endswith("_dog_fp_controlled") else 1.0),
        )
        for name, score in detector_calibration_scores.items()
    }

    out: dict[str, Any] = {
        "calibration_split": "val",
        "calibration": thresholds,
        "config": {
            "dog_sigma_px": dog_sigma,
            "false_positive_quantile": fp_quantile,
            "strict_threshold_multiplier": strict_multiplier,
        },
        "splits": {},
    }
    for split_name, truth in split_truth.items():
        b_obs = split_b_obs[split_name]
        oracle_sheet = truth.copy()
        oracle_sheet[:, 4] = 0.0
        score_maps = {
            "raw_adjoint": raw_via_score_maps(b_obs, forward),
            "oracle_sheet_residual": via_score_maps_from_residual(oracle_sheet, b_obs, forward),
        }
        for name, pred in split_preds[split_name].items():
            score_maps[f"{name}_sheet_residual"] = via_score_maps_from_residual(pred, b_obs, forward)
        for name, score in list(score_maps.items()):
            if f"{name}_dog_fp_controlled" in thresholds:
                score_maps[f"{name}_dog_fp_controlled"] = dog_score_maps(score, dog_sigma)
        out["splits"][split_name] = {
            name: via_detector_metrics(score, truth, thresholds[name]["presence_threshold"])
            for name, score in score_maps.items()
        }
    return out


def calibrate_two_stage_refiner(
    pred_calibration: np.ndarray,
    b_calibration: np.ndarray,
    truth_calibration: np.ndarray,
    forward: dict[str, Any],
    cfg: dict[str, Any],
    calibration_split: str = "val",
) -> dict[str, Any]:
    signed = signed_via_score_maps_from_residual(pred_calibration, b_calibration, forward)
    score = dog_score_maps(np.abs(signed), float(cfg.get("dog_sigma_px", 2.0)))
    threshold_info = calibrate_via_score_threshold(
        score,
        truth_calibration,
        false_positive_quantile=float(cfg.get("false_positive_quantile", 1.0)),
        threshold_multiplier=float(cfg.get("threshold_multiplier", 1.35)),
    )
    mask = score > threshold_info["presence_threshold"]
    if np.any(mask):
        denom = float(np.sum(signed[mask] * signed[mask]) + 1e-30)
        scale = float(np.sum(signed[mask] * truth_calibration[:, 4][mask]) / denom)
    else:
        denom = float(np.sum(signed * signed) + 1e-30)
        scale = float(np.sum(signed * truth_calibration[:, 4]) / denom)
    return {
        "calibration_split": calibration_split,
        "score_threshold": float(threshold_info["presence_threshold"]),
        "score_scale_to_s1": scale,
        "blend_with_prediction": float(cfg.get("blend_with_prediction", 0.65)),
        "max_abs_s1": float(np.max(np.abs(truth_calibration[:, 4])) + 1e-12),
        "dog_sigma_px": float(cfg.get("dog_sigma_px", 2.0)),
    }


def apply_two_stage_refinement(
    pred: np.ndarray,
    b_obs: np.ndarray,
    forward: dict[str, Any],
    refiner: dict[str, float],
) -> np.ndarray:
    signed = signed_via_score_maps_from_residual(pred, b_obs, forward)
    score = dog_score_maps(np.abs(signed), float(refiner["dog_sigma_px"]))
    sparse_candidate = np.zeros_like(pred[:, 4])
    active = score > float(refiner["score_threshold"])
    sparse_candidate[active] = float(refiner["score_scale_to_s1"]) * signed[active]
    clip = float(refiner["max_abs_s1"]) * 1.25
    sparse_candidate = np.clip(sparse_candidate, -clip, clip)
    out = pred.copy()
    blend = float(refiner["blend_with_prediction"])
    out[:, 4] = blend * out[:, 4] + (1.0 - blend) * sparse_candidate
    return out.astype(np.float32)


def topology_metrics(pred: np.ndarray) -> tuple[float, float]:
    mask = np.zeros(pred.shape[-2:], dtype=np.float32)
    mask[2:-2, 2:-2] = 1.0
    r1 = (divergence_np(pred[:, 0], pred[:, 1]) + pred[:, 4]) * mask[None]
    r2 = (divergence_np(pred[:, 2], pred[:, 3]) - pred[:, 4]) * mask[None]
    mse = float(np.mean(r1 * r1) + np.mean(r2 * r2))
    l1 = float(0.5 * (np.mean(np.abs(r1)) + np.mean(np.abs(r2))))
    return mse, l1


def evaluate_method(pred: np.ndarray, truth: np.ndarray, b_clean: np.ndarray, forward_proxy: tuple[np.ndarray, np.ndarray, tuple[int, ...]], y_train: np.ndarray) -> dict[str, Any]:
    topo_mse, topo_l1 = topology_metrics(pred)
    via = via_metrics(pred, truth)
    b_proxy = apply_forward_proxy(pred, y_train, forward_proxy)
    channel_metrics = stable_channel_metrics(pred, truth)
    return {
        "overall_rel_l2": rel_l2(pred, truth),
        **channel_metrics,
        "s1_rel_l2": rel_l2(pred[:, 4], truth[:, 4]),
        **via,
        "topology_mse": topo_mse,
        "topology_l1_mean": topo_l1,
        "layer_leakage_proxy": layer_leakage_proxy(pred, truth),
        "field_residual_proxy_rel_l2": rel_l2(b_proxy, b_clean),
    }


def evaluate_frozen_prediction(pred: np.ndarray, truth: np.ndarray, b_center: np.ndarray, b_pypeec: np.ndarray, forward: dict[str, Any]) -> dict[str, Any]:
    topo_mse, topo_l1 = topology_metrics(pred)
    channel_metrics = stable_channel_metrics(pred, truth)
    row = {
        "overall_rel_l2": rel_l2(pred, truth),
        **channel_metrics,
        "s1_rel_l2": rel_l2(pred[:, 4], truth[:, 4]),
        **via_metrics(pred, truth),
        "topology_mse": topo_mse,
        "topology_l1_mean": topo_l1,
        "layer_leakage_proxy": layer_leakage_proxy(pred, truth),
    }
    b_hat = raster_physical_forward(pred, forward)
    row["physical_reforward_rel_l2_to_bcenter"] = rel_l2(b_hat, b_center)
    row["physical_reforward_rel_l2_to_bpypeec"] = rel_l2(b_hat, b_pypeec)
    return row


def _pypeec_subset_masks(data: dict[str, Any], truth: np.ndarray) -> dict[str, np.ndarray]:
    names = np.asarray(data["case_name"]).astype(str)
    types = np.asarray(data["case_type"]).astype(str)
    is_exp03_like = np.asarray(data["is_exp03_like"], dtype=bool)
    has_via = np.max(np.abs(truth[:, 4]), axis=(1, 2)) > 1e-12
    return {
        "canonical": ~is_exp03_like,
        "exp03_like": is_exp03_like,
        "via": has_via,
        "no_via": ~has_via,
        "dense_via": np.char.find(types, "dense_via") >= 0,
        "return_path": (np.char.find(names, "return_path") >= 0) | (types == "return_path"),
    }


def _evaluate_pypeec_subset(
    mask: np.ndarray,
    data: dict[str, Any],
    preds: dict[str, np.ndarray],
    truth: np.ndarray,
    b_center: np.ndarray,
    b_pypeec: np.ndarray,
    forward: dict[str, Any],
) -> dict[str, Any]:
    methods = {
        name: evaluate_frozen_prediction(pred[mask], truth[mask], b_center[mask], b_pypeec[mask], forward)
        for name, pred in preds.items()
    }
    no = methods["unet_no_topology"]
    topo = methods["unet_topology_soft_loss"]
    refined = methods["unet_topology_two_stage_refined"]
    case_names = np.asarray(data["case_name"]).astype(str)[mask].tolist()
    return {
        "n_cases": int(np.sum(mask)),
        "case_name": case_names,
        "input_gap_rel_l2_pypeec_to_centerline": rel_l2(b_pypeec[mask], b_center[mask]),
        "methods": methods,
        "summary": {
            "topology_mse_ratio_topology_over_no_topology": topo["topology_mse"] / (no["topology_mse"] + 1e-30),
            "overall_l2_ratio_topology_over_no_topology": topo["overall_rel_l2"] / (no["overall_rel_l2"] + 1e-30),
            "refined_topology_mse_ratio_over_no_topology": refined["topology_mse"] / (no["topology_mse"] + 1e-30),
            "refined_over_topology_l2_ratio": refined["overall_rel_l2"] / (topo["overall_rel_l2"] + 1e-30),
        },
    }


def _via_presence_threshold_from_truth(truth: np.ndarray) -> float:
    return 0.20 * float(np.max(np.abs(truth[:, 4])) + 1e-12)


def _component_count(mask: np.ndarray) -> int:
    mask = np.asarray(mask, dtype=bool)
    seen = np.zeros_like(mask, dtype=bool)
    count = 0
    h, w = mask.shape
    for y in range(h):
        for x in range(w):
            if not mask[y, x] or seen[y, x]:
                continue
            count += 1
            stack = [(y, x)]
            seen[y, x] = True
            while stack:
                cy, cx = stack.pop()
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
    return int(count)


def _distance_to_mask_px(mask: np.ndarray, y: int, x: int) -> float | None:
    ys, xs = np.nonzero(np.asarray(mask, dtype=bool))
    if len(xs) == 0:
        return None
    return float(np.min(np.sqrt((xs - x) ** 2 + (ys - y) ** 2)))


def _diagnostic_masks(truth_case: np.ndarray) -> dict[str, np.ndarray]:
    top_x = np.abs(truth_case[0])
    top_y = np.abs(truth_case[1])
    bottom_x = np.abs(truth_case[2])
    bottom_y = np.abs(truth_case[3])
    sheet = np.sqrt(top_x**2 + top_y**2 + bottom_x**2 + bottom_y**2)
    threshold = max(float(np.max(sheet)) * 0.05, 1e-30)
    trace = sheet > threshold
    return_mask = np.sqrt(bottom_x**2 + bottom_y**2) > threshold
    x_active = (top_x + bottom_x) > threshold
    y_active = (top_y + bottom_y) > threshold
    y_near = y_active.copy()
    x_near = x_active.copy()
    for axis in [0, 1]:
        y_near |= np.roll(y_active, 1, axis=axis) | np.roll(y_active, -1, axis=axis)
        x_near |= np.roll(x_active, 1, axis=axis) | np.roll(x_active, -1, axis=axis)
    bend = (x_active & y_near) | (y_active & x_near)
    return {"trace": trace, "return": return_mask, "bend": bend}


def _case_topology_metrics(pred_case: np.ndarray) -> tuple[float, float]:
    return topology_metrics(pred_case[None])


def _case_layer_leakage(pred_case: np.ndarray, truth_case: np.ndarray) -> float:
    return layer_leakage_proxy(pred_case[None], truth_case[None])


def _finite_values(values: list[Any]) -> list[float]:
    finite: list[float] = []
    for value in values:
        if value is None:
            continue
        fvalue = float(value)
        if np.isfinite(fvalue):
            finite.append(fvalue)
    return finite


def _finite_mean(values: list[Any]) -> float | None:
    finite = _finite_values(values)
    if not finite:
        return None
    return float(np.mean(finite))


def _scalar_fit_residual(pred: np.ndarray, target: np.ndarray) -> tuple[float, float]:
    denom = float(np.sum(pred * pred)) + 1e-30
    scale = float(np.sum(pred * target) / denom)
    residual = rel_l2(scale * pred, target)
    return scale, residual


def _topology_residual_map(pred_case: np.ndarray) -> np.ndarray:
    r1 = divergence_np(pred_case[0][None], pred_case[1][None])[0] + pred_case[4]
    r2 = divergence_np(pred_case[2][None], pred_case[3][None])[0] - pred_case[4]
    return np.sqrt(0.5 * (r1 * r1 + r2 * r2))


def _classify_null_via_failure(
    false_positive: bool,
    distance_to_return_px: float | None,
    distance_to_bend_px: float | None,
    dog_score_peak_over_threshold: float,
    pypeec_centerline_gap: float,
) -> str:
    if not false_positive:
        return "no false positive"
    if distance_to_return_px is not None and distance_to_return_px <= 2.0:
        return "return-path induced residual"
    if distance_to_bend_px is not None and distance_to_bend_px <= 2.0:
        return "bend/corner induced residual"
    if dog_score_peak_over_threshold >= 1.0:
        return "detector threshold sensitivity"
    if pypeec_centerline_gap >= 0.15:
        return "operator mismatch"
    return "model hallucination"


def _summarize_diagnostic_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for model in sorted({str(row["model"]) for row in rows}):
        model_rows = [row for row in rows if row["model"] == model]
        mechanisms: dict[str, int] = {}
        detailed_mechanisms: dict[str, int] = {}
        for row in model_rows:
            key = str(row.get("failure_mode", "not classified"))
            mechanisms[key] = mechanisms.get(key, 0) + 1
            detailed_key = str(row.get("mechanism", key))
            detailed_mechanisms[detailed_key] = detailed_mechanisms.get(detailed_key, 0) + 1
        out[model] = {
            "n_cases": len(model_rows),
            "false_positive_rate": _finite_mean([float(row.get("false_positive", False)) for row in model_rows]),
            "mean_s1_peak_current_scale": _finite_mean([row.get("s1_peak_abs_current_scale") for row in model_rows]),
            "mean_physical_b_residual_to_pypeec": _finite_mean([row.get("physical_reforward_rel_l2_to_bpypeec") for row in model_rows]),
            "mean_physical_b_shape_residual_to_pypeec": _finite_mean([row.get("physical_reforward_shape_rel_l2_to_bpypeec") for row in model_rows]),
            "mean_topology_mse": _finite_mean([row.get("topology_mse") for row in model_rows]),
            "mean_layer_leakage_proxy": _finite_mean([row.get("layer_leakage_proxy") for row in model_rows]),
            "mean_layer_allocation_fraction_error": _finite_mean([row.get("layer_allocation_fraction_error") for row in model_rows]),
            "failure_mode_counts": mechanisms,
            "mechanism_counts": detailed_mechanisms,
        }
    return out


def _summarize_null_via_mechanisms(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    fp_rows = [row for row in rows if row.get("false_positive", False)]
    for model in sorted({str(row["model"]) for row in rows}):
        model_rows = [row for row in fp_rows if row["model"] == model]
        model_total = len(model_rows)
        mechanism_rows: dict[str, list[dict[str, Any]]] = {}
        for row in model_rows:
            mechanism = str(row.get("mechanism", row.get("failure_mode", "not classified")))
            mechanism_rows.setdefault(mechanism, []).append(row)
        summary[model] = {
            "n_false_positives": model_total,
            "mechanisms": {
                mechanism: {
                    "count": len(items),
                    "percentage_of_false_positives": float(len(items) / model_total) if model_total else None,
                    "mean_s1_peak_current_scale": _finite_mean([row.get("s1_peak_abs_current_scale") for row in items]),
                    "mean_topology_mse": _finite_mean([row.get("topology_mse") for row in items]),
                    "mean_physical_b_residual_to_pypeec": _finite_mean([row.get("physical_reforward_rel_l2_to_bpypeec") for row in items]),
                    "mean_pypeec_centerline_gap": _finite_mean([row.get("pypeec_centerline_gap_rel_l2") for row in items]),
                    "mean_distance_to_trace_px": _finite_mean([row.get("distance_to_trace_px") for row in items]),
                    "mean_distance_to_bend_px": _finite_mean([row.get("distance_to_bend_px") for row in items]),
                    "mean_distance_to_return_px": _finite_mean([row.get("distance_to_return_px") for row in items]),
                }
                for mechanism, items in sorted(mechanism_rows.items())
            },
        }
    return summary


def _classify_return_path_mechanism(row: dict[str, Any]) -> str:
    if row["layer_allocation_fraction_error"] >= 0.35:
        return "layer-allocation mismatch"
    if row.get("physical_reforward_shape_rel_l2_to_bpypeec", 0.0) >= 0.90:
        return "spatial-shape mismatch"
    if row.get("physical_reforward_amplitude_log_error_abs", 0.0) >= 0.40:
        return "amplitude mismatch"
    if row["excess_predicted_via_components"] > 0:
        return "return interpreted as extra via"
    if row["pypeec_centerline_gap_rel_l2"] >= 0.20:
        return "strong return operator gap"
    return "bounded/mixed"


def _summarize_return_path_mechanisms(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for model in sorted({str(row["model"]) for row in rows}):
        model_rows = [row for row in rows if row["model"] == model]
        model_total = len(model_rows)
        mechanism_rows: dict[str, list[dict[str, Any]]] = {}
        for row in model_rows:
            mechanism = str(row.get("mechanism", row.get("failure_mode", "not classified")))
            mechanism_rows.setdefault(mechanism, []).append(row)
        summary[model] = {
            "n_cases": model_total,
            "mechanisms": {
                mechanism: {
                    "count": len(items),
                    "percentage_of_cases": float(len(items) / model_total) if model_total else None,
                    "mean_raw_b_residual_to_pypeec": _finite_mean([row.get("physical_reforward_rel_l2_to_bpypeec") for row in items]),
                    "mean_shape_b_residual_to_pypeec": _finite_mean([row.get("physical_reforward_shape_rel_l2_to_bpypeec") for row in items]),
                    "mean_scalar_fit_to_pypeec": _finite_mean([row.get("physical_reforward_scalar_fit_to_bpypeec") for row in items]),
                    "mean_amplitude_log_error": _finite_mean([row.get("physical_reforward_amplitude_log_error_abs") for row in items]),
                    "mean_layer_allocation_fraction_error": _finite_mean([row.get("layer_allocation_fraction_error") for row in items]),
                    "mean_return_path_rel_l2": _finite_mean([row.get("return_path_rel_l2") for row in items]),
                    "mean_topology_mse": _finite_mean([row.get("topology_mse") for row in items]),
                }
                for mechanism, items in sorted(mechanism_rows.items())
            },
        }
    return summary


def build_pypeec_null_via_diagnostics(
    data: dict[str, Any],
    preds: dict[str, np.ndarray],
    truth: np.ndarray,
    b_center: np.ndarray,
    b_pypeec: np.ndarray,
    forward: dict[str, Any],
    two_stage_refiner: dict[str, Any],
) -> dict[str, Any]:
    masks = _pypeec_subset_masks(data, truth)
    no_via_mask = masks.get("no_via", np.zeros(truth.shape[0], dtype=bool))
    case_names = np.asarray(data["case_name"]).astype(str)
    case_types = np.asarray(data["case_type"]).astype(str)
    threshold = _via_presence_threshold_from_truth(truth)
    current_scale = float(np.max(np.abs(truth[:, 4])) + 1e-12)
    rows: list[dict[str, Any]] = []
    for model, pred in preds.items():
        b_hat = raster_physical_forward(pred, forward)
        signed_score = signed_via_score_maps_from_residual(pred, b_pypeec, forward)
        dog_score = dog_score_maps(np.abs(signed_score), float(two_stage_refiner["dog_sigma_px"]))
        score_threshold = float(two_stage_refiner["score_threshold"])
        for idx in np.where(no_via_mask)[0]:
            s1 = pred[idx, 4]
            peak_flat = int(np.argmax(np.abs(s1)))
            peak_y, peak_x = np.unravel_index(peak_flat, s1.shape)
            peak_abs = float(abs(s1[peak_y, peak_x]))
            fp_mask = np.abs(s1) > threshold
            topo_mse, topo_l1 = _case_topology_metrics(pred[idx])
            diag_masks = _diagnostic_masks(truth[idx])
            pypeec_gap = rel_l2(b_pypeec[idx], b_center[idx])
            dog_peak = float(np.max(dog_score[idx]))
            dist_return = _distance_to_mask_px(diag_masks["return"], int(peak_y), int(peak_x))
            dist_bend = _distance_to_mask_px(diag_masks["bend"], int(peak_y), int(peak_x))
            false_positive = bool(peak_abs > threshold)
            failure_mode = _classify_null_via_failure(
                false_positive,
                dist_return,
                dist_bend,
                dog_peak / (score_threshold + 1e-30),
                pypeec_gap,
            )
            rows.append(
                {
                    "case_index": int(idx),
                    "case_name": str(case_names[idx]),
                    "case_type": str(case_types[idx]),
                    "model": model,
                    "false_positive": false_positive,
                    "s1_peak_abs_current_scale": peak_abs / current_scale,
                    "s1_rms_current_scale": float(np.sqrt(np.mean(s1 * s1)) / current_scale),
                    "s1_abs_sum_current_scale": float(np.sum(np.abs(s1)) / current_scale),
                    "s1_peak_y": int(peak_y),
                    "s1_peak_x": int(peak_x),
                    "predicted_via_pixels": int(np.sum(fp_mask)),
                    "predicted_via_components": _component_count(fp_mask),
                    "trace_mask_present": bool(np.any(diag_masks["trace"])),
                    "bend_mask_present": bool(np.any(diag_masks["bend"])),
                    "return_mask_present": bool(np.any(diag_masks["return"])),
                    "distance_to_trace_px": _distance_to_mask_px(diag_masks["trace"], int(peak_y), int(peak_x)),
                    "distance_to_bend_px": dist_bend,
                    "distance_to_return_px": dist_return,
                    "topology_mse": topo_mse,
                    "topology_l1_mean": topo_l1,
                    "magnetic_residual_energy_ratio": float(np.mean((b_hat[idx] - b_pypeec[idx]) ** 2) / (np.mean(b_pypeec[idx] ** 2) + 1e-30)),
                    "physical_reforward_rel_l2_to_bpypeec": rel_l2(b_hat[idx], b_pypeec[idx]),
                    "pypeec_centerline_gap_rel_l2": pypeec_gap,
                    "layer_leakage_proxy": _case_layer_leakage(pred[idx], truth[idx]),
                    "residual_score_peak": float(np.max(np.abs(signed_score[idx]))),
                    "dog_residual_score_peak": dog_peak,
                    "dog_score_peak_over_threshold": dog_peak / (score_threshold + 1e-30),
                    "dog_score_components": _component_count(dog_score[idx] > score_threshold),
                    "failure_mode": failure_mode,
                    "mechanism": failure_mode,
                }
            )
    return {
        "n_cases": int(np.sum(no_via_mask)),
        "presence_threshold": threshold,
        "rows": rows,
        "summary": _summarize_diagnostic_rows(rows),
        "mechanism_summary": _summarize_null_via_mechanisms(rows),
        "boundary": "Diagnostic only. No PyPEEC no-via threshold is selected from these rows.",
    }


def _classify_return_path_row(row: dict[str, Any]) -> str:
    if row["physical_reforward_rel_l2_to_bpypeec"] >= 1.5:
        return "magnetic consistency failure"
    if row["layer_allocation_fraction_error"] >= 0.25:
        return "return-layer allocation mismatch"
    if row["excess_predicted_via_components"] > 0:
        return "return interpreted as extra via"
    if row["pypeec_centerline_gap_rel_l2"] >= 0.20:
        return "strong return operator gap"
    return "bounded"


def build_pypeec_return_path_diagnostics(
    data: dict[str, Any],
    preds: dict[str, np.ndarray],
    truth: np.ndarray,
    b_center: np.ndarray,
    b_pypeec: np.ndarray,
    forward: dict[str, Any],
) -> dict[str, Any]:
    masks = _pypeec_subset_masks(data, truth)
    return_mask = masks.get("return_path", np.zeros(truth.shape[0], dtype=bool))
    case_names = np.asarray(data["case_name"]).astype(str)
    case_types = np.asarray(data["case_type"]).astype(str)
    threshold = _via_presence_threshold_from_truth(truth)
    current_scale = float(np.max(np.abs(truth[:, 4])) + 1e-12)
    rows: list[dict[str, Any]] = []
    for idx in np.where(return_mask)[0]:
        truth_signal_energy = float(np.mean(truth[idx, 0] ** 2 + truth[idx, 1] ** 2))
        truth_return_energy = float(np.mean(truth[idx, 2] ** 2 + truth[idx, 3] ** 2))
        truth_return_fraction = truth_return_energy / (truth_signal_energy + truth_return_energy + 1e-30)
        true_via_components = _component_count(np.abs(truth[idx, 4]) > threshold)
        baseline_physical = None
        case_rows: list[dict[str, Any]] = []
        for model, pred in preds.items():
            b_hat = raster_physical_forward(pred[idx : idx + 1], forward)[0]
            scalar_fit, shape_residual = _scalar_fit_residual(b_hat, b_pypeec[idx])
            pred_signal_energy = float(np.mean(pred[idx, 0] ** 2 + pred[idx, 1] ** 2))
            pred_return_energy = float(np.mean(pred[idx, 2] ** 2 + pred[idx, 3] ** 2))
            pred_return_fraction = pred_return_energy / (pred_signal_energy + pred_return_energy + 1e-30)
            pred_components = _component_count(np.abs(pred[idx, 4]) > threshold)
            topo_mse, topo_l1 = _case_topology_metrics(pred[idx])
            row = {
                "case_index": int(idx),
                "case_name": str(case_names[idx]),
                "case_type": str(case_types[idx]),
                "model": model,
                "truth_signal_energy": truth_signal_energy,
                "truth_return_energy": truth_return_energy,
                "truth_return_fraction": truth_return_fraction,
                "pred_signal_energy": pred_signal_energy,
                "pred_return_energy": pred_return_energy,
                "pred_return_fraction": pred_return_fraction,
                "layer_allocation_fraction_error": abs(pred_return_fraction - truth_return_fraction),
                "signal_path_rel_l2": rel_l2(pred[idx, 0:2], truth[idx, 0:2]),
                "return_path_rel_l2": rel_l2(pred[idx, 2:4], truth[idx, 2:4]),
                "s1_peak_abs_current_scale": float(np.max(np.abs(pred[idx, 4])) / current_scale),
                "true_via_components": true_via_components,
                "predicted_via_components": pred_components,
                "excess_predicted_via_components": max(pred_components - true_via_components, 0),
                "topology_mse": topo_mse,
                "topology_l1_mean": topo_l1,
                "layer_leakage_proxy": _case_layer_leakage(pred[idx], truth[idx]),
                "physical_reforward_rel_l2_to_bcenter": rel_l2(b_hat, b_center[idx]),
                "physical_reforward_rel_l2_to_bpypeec": rel_l2(b_hat, b_pypeec[idx]),
                "physical_reforward_shape_rel_l2_to_bpypeec": shape_residual,
                "physical_reforward_scalar_fit_to_bpypeec": scalar_fit,
                "physical_reforward_amplitude_log_error_abs": float(abs(np.log(abs(scalar_fit) + 1e-30))),
                "pypeec_centerline_gap_rel_l2": rel_l2(b_pypeec[idx], b_center[idx]),
            }
            if model == "unet_no_topology":
                baseline_physical = row["physical_reforward_rel_l2_to_bpypeec"]
            case_rows.append(row)
        baseline_physical = float(baseline_physical if baseline_physical is not None else np.nan)
        for row in case_rows:
            row["physical_b_delta_vs_no_topology"] = row["physical_reforward_rel_l2_to_bpypeec"] - baseline_physical
            row["failure_mode"] = _classify_return_path_row(row)
            row["mechanism"] = _classify_return_path_mechanism(row)
            row.update(return_path_hypothesis(row))
            rows.append(row)
    return {
        "n_cases": int(np.sum(return_mask)),
        "rows": rows,
        "summary": _summarize_diagnostic_rows(rows),
        "mechanism_summary": _summarize_return_path_mechanisms(rows),
        "hypothesis_summary": summarize_return_path_hypotheses(rows),
        "boundary": "Diagnostic only. Return-path rows describe current allocation and magnetic consistency failures without changing model thresholds.",
    }


def evaluate_pypeec_frozen_inference(
    cfg: dict[str, Any],
    model_no: nn.Module,
    model_topo: nn.Module,
    x_stats: tuple[np.ndarray, np.ndarray],
    y_stats: tuple[np.ndarray, np.ndarray],
    device: torch.device,
    batch_size: int,
    two_stage_refiner: dict[str, Any],
    out: Path | None = None,
    null_via_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = load_pypeec_frozen_inference_dataset(cfg)
    if not data.get("enabled", False):
        return {"enabled": False}
    if not data.get("artifact_available", False):
        return {
            "enabled": True,
            "artifact_available": False,
            "dataset_path": data.get("dataset_path"),
        }

    b_pypeec = data["B_pypeec"].transpose(0, 3, 1, 2).astype(np.float32)
    b_center = data["B_centerline"].transpose(0, 3, 1, 2).astype(np.float32)
    truth = data["truth"].astype(np.float32)
    x_pypeec_n = normalize(b_pypeec, x_stats)
    pred_no = denormalize(predict_model(model_no, x_pypeec_n, device, batch_size), y_stats)
    pred_topo = denormalize(predict_model(model_topo, x_pypeec_n, device, batch_size), y_stats)
    forward = build_physical_forward_kernels(data["x"], data["y"], cfg)
    pred_topo_refined = apply_two_stage_refinement(pred_topo, b_pypeec, forward, two_stage_refiner)
    preds = {
        "unet_no_topology": pred_no,
        "unet_topology_soft_loss": pred_topo,
        "unet_topology_two_stage_refined": pred_topo_refined,
    }
    methods = {
        name: evaluate_frozen_prediction(pred, truth, b_center, b_pypeec, forward)
        for name, pred in preds.items()
    }
    subsets = {
        name: _evaluate_pypeec_subset(mask, data, preds, truth, b_center, b_pypeec, forward)
        for name, mask in _pypeec_subset_masks(data, truth).items()
        if bool(np.any(mask))
    }
    null_via_diagnostics = build_pypeec_null_via_diagnostics(
        data, preds, truth, b_center, b_pypeec, forward, two_stage_refiner
    )
    if out is not None:
        null_via_diagnostics["failure_figure_paths"] = plot_pypeec_null_via_failure_cases(
            data,
            preds,
            truth,
            b_center,
            b_pypeec,
            null_via_diagnostics,
            out,
        )
    return_path_diagnostics = build_pypeec_return_path_diagnostics(
        data, preds, truth, b_center, b_pypeec, forward
    )
    null_via_gate_eval = evaluate_pypeec_null_via_hypothesis_gate(
        data,
        preds,
        truth,
        b_center,
        b_pypeec,
        forward,
        two_stage_refiner,
        null_via_gate or {"enabled": False},
    )
    null_via_evidence = build_pypeec_null_via_hypothesis_evidence(
        data,
        preds,
        truth,
        b_pypeec,
        forward,
        two_stage_refiner,
        null_via_gate or {"enabled": False},
    )
    uncertainty_refusal = build_pypeec_uncertainty_refusal(null_via_evidence)
    generative_hypothesis = build_pypeec_generative_hypothesis_scoring(
        null_via_evidence,
        null_via_gate or {"enabled": False},
    )
    selective_risk = build_pypeec_selective_risk(generative_hypothesis)
    return_current_aware_generator = build_pypeec_return_current_aware_generator(
        data,
        truth,
        b_pypeec,
        forward,
    )
    heldout_split_protocol = build_pypeec_heldout_split_protocol(
        data["case_name"],
        data["case_type"],
        data["is_exp03_like"],
    )
    heldout_split_evaluation = build_pypeec_heldout_split_evaluation(
        heldout_split_protocol,
        data,
        preds,
        truth,
        b_center,
        b_pypeec,
        forward,
    )
    if out is not None and bool(null_via_gate_eval.get("enabled", False)):
        null_via_gate_eval["case_figure_paths"] = plot_null_via_gate_case_studies(
            data,
            pred_topo,
            truth,
            b_center,
            b_pypeec,
            forward,
            two_stage_refiner,
            null_via_gate_eval,
            out,
        )
    no = methods["unet_no_topology"]
    topo = methods["unet_topology_soft_loss"]
    refined = methods["unet_topology_two_stage_refined"]
    return {
        "enabled": True,
        "artifact_available": True,
        "dataset_path": data["dataset_path"],
        "split": "pypeec_test",
        "n_cases": int(truth.shape[0]),
        "n_exp03_like_cases": int(np.sum(data["is_exp03_like"])),
        "case_name": data["case_name"].tolist(),
        "case_type": data["case_type"].tolist(),
        "is_exp03_like": data["is_exp03_like"].astype(bool).tolist(),
        "input_gap_rel_l2_pypeec_to_centerline": rel_l2(b_pypeec, b_center),
        "used_for_training": False,
        "used_for_validation_thresholds": False,
        "used_for_calibration": False,
        "methods": methods,
        "subsets": subsets,
        "heldout_split_protocol": heldout_split_protocol,
        "null_via_diagnostics": null_via_diagnostics,
        "return_path_diagnostics": return_path_diagnostics,
        "null_via_hypothesis_gate": null_via_gate_eval,
        "null_via_hypothesis_evidence": null_via_evidence,
        "null_via_generative_hypothesis": generative_hypothesis,
        "selective_risk": selective_risk,
        "uncertainty_refusal": uncertainty_refusal,
        "return_current_aware_generator": return_current_aware_generator,
        "heldout_split_evaluation": heldout_split_evaluation,
        "summary": {
            "topology_mse_ratio_topology_over_no_topology": topo["topology_mse"] / (no["topology_mse"] + 1e-30),
            "overall_l2_ratio_topology_over_no_topology": topo["overall_rel_l2"] / (no["overall_rel_l2"] + 1e-30),
            "via_hit_delta_topology_minus_no_topology": topo["via_hit_rate_within_2px"] - no["via_hit_rate_within_2px"],
            "refined_over_topology_l2_ratio": refined["overall_rel_l2"] / (topo["overall_rel_l2"] + 1e-30),
        },
        "boundary": (
            "Frozen inference on the exp07 PyPEEC mini dataset. The models, "
            "normalization stats, detector thresholds, and two-stage refiner were "
            "trained/calibrated before this dataset is read."
        ),
    }


def attach_physical_reforward_metrics(rows: dict[str, dict[str, Any]], preds: dict[str, np.ndarray], b_clean: np.ndarray, b_obs: np.ndarray, forward: dict[str, Any]) -> None:
    for name, pred in preds.items():
        b_hat = raster_physical_forward(pred, forward)
        rows[name]["physical_reforward_rel_l2_to_bclean"] = rel_l2(b_hat, b_clean)
        rows[name]["physical_reforward_rel_l2_to_bobs"] = rel_l2(b_hat, b_obs)


def plot_training_curves(hist_no: list[dict[str, float]], hist_topo: list[dict[str, float]], out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4), constrained_layout=True)
    ax.plot([h["epoch"] for h in hist_no], [h["val_mse"] for h in hist_no], label="no-topology val MSE")
    ax.plot([h["epoch"] for h in hist_topo], [h["val_mse"] for h in hist_topo], label="topology val MSE")
    ax.set_xlabel("epoch")
    ax.set_ylabel("normalized supervised MSE")
    ax.set_title("U-Net-lite training curves")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.savefig(out / "01_training_curves.png", dpi=180)
    plt.close(fig)


def plot_prediction_comparison(x: np.ndarray, truth: np.ndarray, preds: dict[str, np.ndarray], out: Path) -> None:
    sample = 0
    rows = [("truth", truth), ("unet_no_topology", preds["unet_no_topology"]), ("unet_topology_soft_loss", preds["unet_topology_soft_loss"])]
    fig, axes = plt.subplots(len(rows), 5, figsize=(13, 7), constrained_layout=True)
    for r, (name, arr) in enumerate(rows):
        for c, ch in enumerate(CHANNELS):
            img = arr[sample, c]
            vmax = max(np.percentile(np.abs(img), 99), 1e-9)
            axes[r, c].imshow(img, origin="lower", cmap="coolwarm", vmin=-vmax, vmax=vmax)
            axes[r, c].set_title(f"{name} {ch}", fontsize=8)
            axes[r, c].set_xticks([])
            axes[r, c].set_yticks([])
    fig.savefig(out / "02_prediction_comparison.png", dpi=180)
    plt.close(fig)


def plot_metric_bars(metrics: dict[str, Any], out: Path) -> None:
    methods = ["zero", "ridge", "unet_no_topology", "unet_topology_soft_loss"]
    vals_l2 = [metrics["benchmark"]["test"][m]["overall_rel_l2"] for m in methods]
    vals_topo = [metrics["benchmark"]["test"][m]["topology_mse"] for m in methods]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    axes[0].bar(methods, vals_l2)
    axes[0].set_title("Test overall relative L2")
    axes[0].tick_params(axis="x", rotation=25)
    axes[1].bar(methods, vals_topo)
    axes[1].set_title("Test topology MSE")
    axes[1].tick_params(axis="x", rotation=25)
    axes[1].set_yscale("log")
    fig.savefig(out / "03_metric_bars.png", dpi=180)
    plt.close(fig)


def plot_lambda_pareto(metrics: dict[str, Any], out: Path) -> None:
    rows = metrics["lambda_sweep"]
    lambdas = [r["lambda"] for r in rows]
    l2 = [r["test"]["overall_rel_l2"] for r in rows]
    topo = [r["test"]["topology_mse"] for r in rows]
    ood_topo = [r["ood"]["topology_mse"] for r in rows]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    axes[0].plot(lambdas, l2, "o-", label="test overall L2")
    axes[0].set_xscale("symlog", linthresh=0.01)
    axes[0].set_xlabel("topology lambda")
    axes[0].set_ylabel("overall relative L2")
    axes[0].grid(alpha=0.3, which="both")
    axes[1].plot(lambdas, topo, "o-", label="test topology MSE")
    axes[1].plot(lambdas, ood_topo, "s--", label="OOD topology MSE")
    axes[1].set_xscale("symlog", linthresh=0.01)
    axes[1].set_yscale("log")
    axes[1].set_xlabel("topology lambda")
    axes[1].set_ylabel("topology MSE")
    axes[1].grid(alpha=0.3, which="both")
    axes[1].legend()
    fig.savefig(out / "04_lambda_pareto.png", dpi=180)
    plt.close(fig)


def _safe_filename(text: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in text)[:120]


def _plot_map(ax: Any, img: np.ndarray, title: str, cmap: str = "viridis", symmetric: bool = False) -> None:
    img = np.asarray(img)
    if symmetric:
        vmax = max(float(np.percentile(np.abs(img), 99)), 1e-9)
        vmin = -vmax
    else:
        vmin = float(np.percentile(img, 1))
        vmax = max(float(np.percentile(img, 99)), vmin + 1e-9)
    ax.imshow(img, origin="lower", cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_title(title, fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])


def plot_pypeec_null_via_failure_cases(
    data: dict[str, Any],
    preds: dict[str, np.ndarray],
    truth: np.ndarray,
    b_center: np.ndarray,
    b_pypeec: np.ndarray,
    diagnostics: dict[str, Any],
    out: Path,
    max_cases: int = 8,
) -> list[str]:
    rows = [row for row in diagnostics.get("rows", []) if row.get("false_positive", False)]
    if not rows:
        return []
    rows.sort(
        key=lambda row: (
            str(row.get("failure_mode", "")) == "bend/corner induced residual",
            float(row.get("s1_peak_abs_current_scale", 0.0)),
            float(row.get("physical_reforward_rel_l2_to_bpypeec", 0.0)),
        ),
        reverse=True,
    )
    selected: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        key = (str(row.get("case_name")), str(row.get("model")))
        if key in seen:
            continue
        seen.add(key)
        selected.append(row)
        if len(selected) >= max_cases:
            break

    fig_dir = out / "figures" / "pypeec_null_via_failures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    for old in fig_dir.glob("*.png"):
        old.unlink()

    case_names = np.asarray(data["case_name"]).astype(str)
    paths: list[str] = []
    for row in selected:
        idx = int(row["case_index"])
        model = str(row["model"])
        pred = preds[model][idx]
        diag_masks = _diagnostic_masks(truth[idx])
        b_mag = np.sqrt(np.sum(b_pypeec[idx] ** 2, axis=0))
        gap_mag = np.sqrt(np.sum((b_pypeec[idx] - b_center[idx]) ** 2, axis=0))
        topo = _topology_residual_map(pred)

        fig, axes = plt.subplots(2, 3, figsize=(10, 6), constrained_layout=True)
        _plot_map(axes[0, 0], b_mag, "PyPEEC |B|")
        _plot_map(axes[0, 1], gap_mag, "PyPEEC-centerline |gap|")
        _plot_map(axes[0, 2], truth[idx, 4], "truth s1", cmap="coolwarm", symmetric=True)
        _plot_map(axes[1, 0], pred[4], "predicted s1", cmap="coolwarm", symmetric=True)
        axes[1, 0].scatter([row["s1_peak_x"]], [row["s1_peak_y"]], s=45, facecolors="none", edgecolors="yellow", linewidths=1.5)
        _plot_map(axes[1, 1], topo, "topology residual")
        axes[1, 2].imshow(diag_masks["trace"], origin="lower", cmap="Greys", vmin=0, vmax=1)
        if np.any(diag_masks["bend"]):
            axes[1, 2].contour(diag_masks["bend"].astype(float), levels=[0.5], colors=["tab:red"], linewidths=1.0)
        if np.any(diag_masks["return"]):
            axes[1, 2].contour(diag_masks["return"].astype(float), levels=[0.5], colors=["tab:blue"], linewidths=1.0)
        axes[1, 2].scatter([row["s1_peak_x"]], [row["s1_peak_y"]], s=45, facecolors="none", edgecolors="yellow", linewidths=1.5)
        axes[1, 2].set_title("trace/bend/return overlay", fontsize=8)
        axes[1, 2].set_xticks([])
        axes[1, 2].set_yticks([])
        fig.suptitle(
            f"{case_names[idx]} / {model} / {row.get('failure_mode')} / s1 peak={row.get('s1_peak_abs_current_scale'):.3f}",
            fontsize=9,
        )
        rel_path = Path("figures") / "pypeec_null_via_failures" / f"{_safe_filename(case_names[idx])}__{_safe_filename(model)}.png"
        fig.savefig(out / rel_path, dpi=180)
        plt.close(fig)
        paths.append(str(rel_path).replace("\\", "/"))
    return paths


def plot_null_via_gate_case_studies(
    data: dict[str, Any],
    pred: np.ndarray,
    truth: np.ndarray,
    b_center: np.ndarray,
    b_pypeec: np.ndarray,
    forward: dict[str, Any],
    two_stage_refiner: dict[str, Any],
    gate_eval: dict[str, Any],
    out: Path,
) -> list[str]:
    if not bool(gate_eval.get("enabled", False)):
        return []
    params = gate_eval.get("selected_params", {})
    gated_pred, decisions = apply_null_via_gate(
        pred,
        b_pypeec,
        truth,
        forward,
        two_stage_refiner,
        {"selected_params": params},
    )
    case_names = np.asarray(data["case_name"]).astype(str)
    case_types = np.asarray(data["case_type"]).astype(str)
    decisions_by_idx = {int(row["case_index"]): row for row in decisions}
    candidates: list[tuple[str, int]] = []

    fp_filtered = [
        row for row in decisions
        if (not row["true_via"]) and row["candidate_present"] and (not row["accepted"])
    ]
    fp_filtered.sort(key=lambda row: float(row.get("s1_peak_abs_current_scale", 0.0)), reverse=True)
    if fp_filtered:
        candidates.append(("fp_filtered", int(fp_filtered[0]["case_index"])))

    true_via_rejected = [
        row for row in decisions
        if row["true_via"] and row["candidate_present"] and (not row["accepted"])
    ]
    true_via_rejected.sort(key=lambda row: float(row.get("s1_peak_abs_current_scale", 0.0)), reverse=True)
    if true_via_rejected:
        candidates.append(("true_via_rejected", int(true_via_rejected[0]["case_index"])))

    dense_rejected = [
        row for row in true_via_rejected
        if "dense_via" in str(case_types[int(row["case_index"])])
    ]
    if dense_rejected:
        candidates.append(("dense_via_weakened", int(dense_rejected[0]["case_index"])))

    return_rows = [
        row for row in decisions
        if "return_path" in str(case_types[int(row["case_index"])])
    ]
    return_rows.sort(key=lambda row: float(row.get("physical_b_improvement", 0.0)))
    if return_rows:
        candidates.append(("return_path_still_hard", int(return_rows[0]["case_index"])))

    seen: set[tuple[str, int]] = set()
    unique: list[tuple[str, int]] = []
    for label, idx in candidates:
        key = (label, idx)
        if key in seen:
            continue
        seen.add(key)
        unique.append((label, idx))

    fig_dir = out / "figures" / "null_via_gate_case_studies"
    fig_dir.mkdir(parents=True, exist_ok=True)
    for old in fig_dir.glob("*.png"):
        old.unlink()

    paths: list[str] = []
    for label, idx in unique:
        row = decisions_by_idx[idx]
        b_mag = np.sqrt(np.sum(b_pypeec[idx] ** 2, axis=0))
        gap_mag = np.sqrt(np.sum((b_pypeec[idx] - b_center[idx]) ** 2, axis=0))
        before = pred[idx]
        after = gated_pred[idx]
        b_after = raster_physical_forward(after[None], forward)[0]
        b_resid = np.sqrt(np.sum((b_after - b_pypeec[idx]) ** 2, axis=0))
        topo_before = _topology_residual_map(before)
        topo_after = _topology_residual_map(after)

        fig, axes = plt.subplots(2, 4, figsize=(13, 6), constrained_layout=True)
        _plot_map(axes[0, 0], b_mag, "PyPEEC |B|")
        _plot_map(axes[0, 1], gap_mag, "PyPEEC-centerline |gap|")
        _plot_map(axes[0, 2], truth[idx, 4], "truth s1", cmap="coolwarm", symmetric=True)
        _plot_map(axes[0, 3], before[4], "s1 before gate", cmap="coolwarm", symmetric=True)
        if row["candidate_present"]:
            axes[0, 3].scatter([row["s1_peak_x"]], [row["s1_peak_y"]], s=45, facecolors="none", edgecolors="yellow", linewidths=1.5)
        _plot_map(axes[1, 0], after[4], "s1 after gate", cmap="coolwarm", symmetric=True)
        if row["candidate_present"]:
            axes[1, 0].scatter([row["s1_peak_x"]], [row["s1_peak_y"]], s=45, facecolors="none", edgecolors="yellow", linewidths=1.5)
        _plot_map(axes[1, 1], topo_before, "topology residual before")
        _plot_map(axes[1, 2], topo_after, "topology residual after")
        _plot_map(axes[1, 3], b_resid, "after-gate |Bhat-PyPEEC|")
        fig.suptitle(
            f"{label}: {case_names[idx]} / {case_types[idx]} / accepted={row['accepted']} / reason={row['rejection_reason']}",
            fontsize=9,
        )
        rel_path = Path("figures") / "null_via_gate_case_studies" / f"{_safe_filename(label)}__{_safe_filename(case_names[idx])}.png"
        fig.savefig(out / rel_path, dpi=180)
        plt.close(fig)
        paths.append(str(rel_path).replace("\\", "/"))
    return paths


def _truth_via_present_mask(truth: np.ndarray) -> np.ndarray:
    threshold = _via_presence_threshold_from_truth(truth)
    return np.max(np.abs(truth[:, 4]).reshape(truth.shape[0], -1), axis=1) > threshold


def _bend_corner_residual_fields(truth: np.ndarray, b_obs: np.ndarray) -> np.ndarray:
    out = np.zeros_like(b_obs)
    for idx in range(truth.shape[0]):
        diag = _diagnostic_masks(truth[idx])
        mask = diag["bend"].astype(np.float32)
        if not np.any(mask):
            mask = diag["trace"].astype(np.float32)
        if not np.any(mask):
            continue
        smooth = gaussian_blur_fft_batch(mask[None, None], 1.2)[0, 0]
        gy, gx = np.gradient(smooth)
        pattern = np.stack([gx, gy, 0.5 * smooth], axis=0).astype(np.float32)
        pattern /= float(np.max(np.abs(pattern)) + 1e-30)
        amp = 0.08 * float(np.max(np.abs(b_obs[idx])) + 1e-30)
        out[idx] = amp * pattern
    return out.astype(np.float32)


def build_null_via_validation_stress(
    truth_val: np.ndarray,
    b_val: np.ndarray,
    data_x: np.ndarray,
    data_y: np.ndarray,
    cfg: dict[str, Any],
) -> dict[str, Any]:
    via_mask = _truth_via_present_mask(truth_val)
    no_via_mask = ~via_mask
    fw_forward = build_finite_width_return_forward_kernels(data_x, data_y, cfg)
    center_forward = build_physical_forward_kernels(data_x, data_y, cfg)
    b_fw = raster_physical_forward(truth_val, fw_forward)
    bend_residual = _bend_corner_residual_fields(truth_val, b_val)
    bend = (b_val + bend_residual).astype(np.float32)
    strong_bend = (b_val + 1.45 * bend_residual).astype(np.float32)
    return_like = (b_val + 0.85 * (b_fw - b_val)).astype(np.float32)
    operator_gap = b_fw.astype(np.float32)
    swapped = truth_val.copy()
    swapped[:, 0:2], swapped[:, 2:4] = truth_val[:, 2:4].copy(), truth_val[:, 0:2].copy()
    layer_ambiguous = (0.55 * b_val + 0.45 * raster_physical_forward(swapped, center_forward)).astype(np.float32)

    families: list[tuple[str, np.ndarray, np.ndarray, np.ndarray]] = [
        ("true_via_clean", b_val[via_mask], truth_val[via_mask], np.where(via_mask)[0]),
        ("true_via_bend_corner_stress", bend[via_mask], truth_val[via_mask], np.where(via_mask)[0]),
        ("true_via_near_bend_corner_strong_stress", strong_bend[via_mask], truth_val[via_mask], np.where(via_mask)[0]),
        ("true_via_return_path_stress", return_like[via_mask], truth_val[via_mask], np.where(via_mask)[0]),
        ("true_via_operator_gap_stress", operator_gap[via_mask], truth_val[via_mask], np.where(via_mask)[0]),
        ("true_via_layer_allocation_stress", layer_ambiguous[via_mask], truth_val[via_mask], np.where(via_mask)[0]),
        ("no_via_clean", b_val[no_via_mask], truth_val[no_via_mask], np.where(no_via_mask)[0]),
        ("synthetic_null_via_bend_corner_stress", bend[no_via_mask], truth_val[no_via_mask], np.where(no_via_mask)[0]),
        ("synthetic_null_via_strong_local_b_gap_stress", strong_bend[no_via_mask], truth_val[no_via_mask], np.where(no_via_mask)[0]),
        ("synthetic_null_via_return_path_stress", return_like[no_via_mask], truth_val[no_via_mask], np.where(no_via_mask)[0]),
        ("synthetic_null_via_operator_gap_stress", operator_gap[no_via_mask], truth_val[no_via_mask], np.where(no_via_mask)[0]),
        ("synthetic_null_via_layer_allocation_stress", layer_ambiguous[no_via_mask], truth_val[no_via_mask], np.where(no_via_mask)[0]),
    ]
    b_parts: list[np.ndarray] = []
    truth_parts: list[np.ndarray] = []
    family_labels: list[str] = []
    source_indices: list[int] = []
    rows: list[dict[str, Any]] = []
    for name, b_family, truth_family, idx_family in families:
        if len(b_family) == 0:
            continue
        b_parts.append(b_family)
        truth_parts.append(truth_family)
        family_labels.extend([name] * len(b_family))
        source_indices.extend([int(i) for i in idx_family])
        rows.append(
            {
                "family": name,
                "n_cases": int(len(b_family)),
                "n_via": int(np.sum(_truth_via_present_mask(truth_family))),
                "n_no_via": int(len(b_family) - np.sum(_truth_via_present_mask(truth_family))),
                "input_gap_rel_l2_to_val": rel_l2(b_family, b_val[idx_family]),
            }
        )
    return {
        "B": np.concatenate(b_parts, axis=0).astype(np.float32),
        "truth": np.concatenate(truth_parts, axis=0).astype(np.float32),
        "family": np.asarray(family_labels),
        "source_val_index": np.asarray(source_indices, dtype=np.int64),
        "family_rows": rows,
    }


def _gate_feature_rows(
    pred: np.ndarray,
    b_obs: np.ndarray,
    truth: np.ndarray,
    forward: dict[str, Any],
    two_stage_refiner: dict[str, Any],
) -> list[dict[str, Any]]:
    current_scale = float(np.max(np.abs(truth[:, 4])) + 1e-12)
    threshold = 0.20 * current_scale
    signed_score = signed_via_score_maps_from_residual(pred, b_obs, forward)
    dog_score = dog_score_maps(np.abs(signed_score), float(two_stage_refiner["dog_sigma_px"]))
    score_threshold = float(two_stage_refiner["score_threshold"])
    pred_zero = pred.copy()
    pred_zero[:, 4] = 0.0
    b_hat = raster_physical_forward(pred, forward)
    b_zero = raster_physical_forward(pred_zero, forward)
    rows: list[dict[str, Any]] = []
    for idx in range(pred.shape[0]):
        s1 = pred[idx, 4]
        peak_flat = int(np.argmax(np.abs(s1)))
        peak_y, peak_x = np.unravel_index(peak_flat, s1.shape)
        peak_abs = float(abs(s1[peak_y, peak_x]))
        candidate_mask = np.abs(s1) > threshold
        candidate_pixels = int(np.sum(candidate_mask))
        candidate_components = _component_count(candidate_mask)
        candidate = bool(peak_abs > threshold)
        true_via = bool(np.max(np.abs(truth[idx, 4])) > threshold)
        diag = _diagnostic_masks(truth[idx])
        topo_pred = _case_topology_metrics(pred[idx])[0]
        topo_zero = _case_topology_metrics(pred_zero[idx])[0]
        physical_pred = rel_l2(b_hat[idx], b_obs[idx])
        physical_zero = rel_l2(b_zero[idx], b_obs[idx])
        dist_bend = _distance_to_mask_px(diag["bend"], int(peak_y), int(peak_x))
        dist_return = _distance_to_mask_px(diag["return"], int(peak_y), int(peak_x))
        dist_trace = _distance_to_mask_px(diag["trace"], int(peak_y), int(peak_x))
        dog_peak_flat = int(np.argmax(dog_score[idx]))
        dog_y, dog_x = np.unravel_index(dog_peak_flat, dog_score[idx].shape)
        peak_alignment = float(np.sqrt((dog_y - peak_y) ** 2 + (dog_x - peak_x) ** 2))
        candidate_compactness = (
            float(1.0 / max(candidate_components, 1))
            if candidate_pixels > 0
            else 0.0
        )
        stability_proxy = float(1.0 / (1.0 + peak_alignment))
        rows.append(
            {
                "case_index": int(idx),
                "true_via": true_via,
                "candidate_present": candidate,
                "candidate_pixels": candidate_pixels,
                "candidate_components": candidate_components,
                "candidate_compactness": candidate_compactness,
                "stability_proxy": stability_proxy,
                "s1_dog_peak_alignment_px": peak_alignment,
                "s1_peak_abs_current_scale": peak_abs / current_scale,
                "s1_peak_y": int(peak_y),
                "s1_peak_x": int(peak_x),
                "topology_pred": float(topo_pred),
                "topology_zero_s1": float(topo_zero),
                "topology_improvement": float((topo_zero - topo_pred) / (abs(topo_zero) + 1e-30)),
                "physical_b_improvement": float(physical_zero - physical_pred),
                "physical_b_pred": physical_pred,
                "physical_b_zero_s1": physical_zero,
                "dog_score_peak_over_threshold": float(np.max(dog_score[idx]) / (score_threshold + 1e-30)),
                "distance_to_trace_px": dist_trace,
                "distance_to_bend_px": dist_bend,
                "distance_to_return_px": dist_return,
            }
        )
    return rows


def _null_via_gate_score(row: dict[str, Any], params: dict[str, Any]) -> float:
    weights = params["score_weights"]
    return float(
        weights["s1_peak"] * row["s1_peak_abs_current_scale"]
        + weights["topology_improvement"] * row["topology_improvement"]
        + weights["physical_b_improvement"] * row["physical_b_improvement"]
        + weights["dog_score"] * np.log1p(max(row["dog_score_peak_over_threshold"], 0.0))
    )


def _apply_null_via_gate_decisions(rows: list[dict[str, Any]], params: dict[str, Any]) -> list[dict[str, Any]]:
    decisions: list[dict[str, Any]] = []
    artifact_radius = float(params["artifact_radius_px"])
    return_radius = float(params["return_radius_px"])
    physical_override = float(params["artifact_physical_override"])
    score_threshold = float(params["score_threshold"])
    for row in rows:
        score = _null_via_gate_score(row, params)
        near_bend = row["distance_to_bend_px"] is not None and row["distance_to_bend_px"] <= artifact_radius
        near_return = row["distance_to_return_px"] is not None and row["distance_to_return_px"] <= return_radius
        artifact_zone = bool(near_bend or near_return)
        artifact_rejected = artifact_zone and row["physical_b_improvement"] < physical_override
        accepted = bool(row["candidate_present"] and score >= score_threshold and not artifact_rejected)
        reason = "accepted"
        if not row["candidate_present"]:
            reason = "no candidate"
        elif score < score_threshold:
            reason = "low hypothesis score"
        elif artifact_rejected:
            reason = "artifact-zone residual"
        decisions.append({**row, "gate_score": score, "artifact_zone": artifact_zone, "accepted": accepted, "rejection_reason": reason})
    return decisions


def _pred_from_gate_decisions(pred: np.ndarray, decisions: list[dict[str, Any]]) -> np.ndarray:
    out = pred.copy()
    for row in decisions:
        if not row["accepted"]:
            out[int(row["case_index"]), 4] = 0.0
    return out.astype(np.float32)


def _presence_metrics_from_decisions(decisions: list[dict[str, Any]]) -> dict[str, float]:
    truth_present = sum(1 for row in decisions if row["true_via"])
    pred_present = sum(1 for row in decisions if row["accepted"])
    tp = sum(1 for row in decisions if row["true_via"] and row["accepted"])
    no_via = sum(1 for row in decisions if not row["true_via"])
    fp = sum(1 for row in decisions if (not row["true_via"]) and row["accepted"])
    precision = tp / max(pred_present, 1)
    recall = tp / max(truth_present, 1)
    f1 = 2.0 * precision * recall / max(precision + recall, 1e-30)
    return {
        "via_presence_precision": float(precision),
        "via_presence_recall": float(recall),
        "via_presence_f1": float(f1),
        "via_false_positive_rate_no_via": float(fp / max(no_via, 1)),
        "truth_present": int(truth_present),
        "pred_present": int(pred_present),
        "true_positive": int(tp),
        "false_positive": int(fp),
        "no_via": int(no_via),
    }


def calibrate_null_via_hypothesis_gate(
    cfg: dict[str, Any],
    model_topo: nn.Module,
    x_stats: tuple[np.ndarray, np.ndarray],
    y_stats: tuple[np.ndarray, np.ndarray],
    device: torch.device,
    batch_size: int,
    truth_val: np.ndarray,
    b_val: np.ndarray,
    data_x: np.ndarray,
    data_y: np.ndarray,
    forward: dict[str, Any],
    two_stage_refiner: dict[str, Any],
) -> dict[str, Any]:
    gcfg = cfg.get("null_via_hypothesis_gate", {})
    if not bool(gcfg.get("enabled", True)):
        return {"enabled": False}
    stress = build_null_via_validation_stress(truth_val, b_val, data_x, data_y, cfg)
    pred = denormalize(
        predict_model(model_topo, normalize(stress["B"], x_stats), device, batch_size),
        y_stats,
    )
    rows = _gate_feature_rows(pred, stress["B"], stress["truth"], forward, two_stage_refiner)
    weights = {
        "s1_peak": float(gcfg.get("weight_s1_peak", 1.0)),
        "topology_improvement": float(gcfg.get("weight_topology_improvement", 0.8)),
        "physical_b_improvement": float(gcfg.get("weight_physical_b_improvement", 2.0)),
        "dog_score": float(gcfg.get("weight_dog_score", 0.08)),
    }
    base_params = {
        "score_weights": weights,
        "return_radius_px": float(gcfg.get("return_radius_px", 2.0)),
    }
    candidate_scores = []
    for row in rows:
        if row["candidate_present"]:
            candidate_scores.append(_null_via_gate_score(row, {**base_params, "score_threshold": 0.0, "artifact_radius_px": 0.0, "artifact_physical_override": 0.0}))
    if candidate_scores:
        quantiles = [float(q) for q in gcfg.get("score_quantiles", [0.0, 0.01, 0.02, 0.05, 0.15, 0.30, 0.45, 0.60, 0.75])]
        threshold_options = sorted(
            {
                float(np.min(candidate_scores) - 1e-9),
                *{float(np.quantile(candidate_scores, q)) for q in quantiles},
            }
        )
    else:
        threshold_options = [0.0]
    artifact_options = [float(x) for x in gcfg.get("artifact_radius_options_px", [0.0, 1.0, 2.0, 3.0])]
    override_options = [float(x) for x in gcfg.get("artifact_physical_override_options", [0.0, 0.01, 0.03, 0.05])]
    min_recall = float(gcfg.get("min_validation_recall", 0.70))
    grid: list[dict[str, Any]] = []
    best: dict[str, Any] | None = None
    for artifact_radius in artifact_options:
        for override in override_options:
            for score_threshold in threshold_options:
                params = {
                    **base_params,
                    "artifact_radius_px": artifact_radius,
                    "artifact_physical_override": override,
                    "score_threshold": score_threshold,
                }
                decisions = _apply_null_via_gate_decisions(rows, params)
                metrics = _presence_metrics_from_decisions(decisions)
                objective = (
                    metrics["via_presence_f1"]
                    - 0.75 * metrics["via_false_positive_rate_no_via"]
                    + 0.15 * metrics["via_presence_recall"]
                )
                if metrics["via_presence_recall"] < min_recall:
                    objective -= 1.0 + (min_recall - metrics["via_presence_recall"])
                entry = {
                    "params": params,
                    "validation": metrics,
                    "objective": float(objective),
                    "feasible_recall": bool(metrics["via_presence_recall"] >= min_recall),
                }
                grid.append(entry)
                if best is None:
                    best = entry
                elif entry["feasible_recall"] and not best["feasible_recall"]:
                    best = entry
                elif entry["feasible_recall"] and best["feasible_recall"]:
                    current_key = (
                        -entry["validation"]["via_false_positive_rate_no_via"],
                        entry["validation"]["via_presence_f1"],
                        entry["validation"]["via_presence_recall"],
                        entry["objective"],
                    )
                    best_key = (
                        -best["validation"]["via_false_positive_rate_no_via"],
                        best["validation"]["via_presence_f1"],
                        best["validation"]["via_presence_recall"],
                        best["objective"],
                    )
                    if current_key > best_key:
                        best = entry
                elif not entry["feasible_recall"] and not best["feasible_recall"]:
                    current_key = (
                        entry["validation"]["via_presence_recall"],
                        -entry["validation"]["via_false_positive_rate_no_via"],
                        entry["validation"]["via_presence_f1"],
                        entry["objective"],
                    )
                    best_key = (
                        best["validation"]["via_presence_recall"],
                        -best["validation"]["via_false_positive_rate_no_via"],
                        best["validation"]["via_presence_f1"],
                        best["objective"],
                    )
                    if current_key > best_key:
                        best = entry
    assert best is not None
    best_params = best["params"]
    best_decisions = _apply_null_via_gate_decisions(rows, best_params)
    filtered = _pred_from_gate_decisions(pred, best_decisions)
    before = via_metrics(pred, stress["truth"])
    after = via_metrics(filtered, stress["truth"])
    after.update(_presence_metrics_from_decisions(best_decisions))
    family_rows = []
    for family in sorted(set(stress["family"].tolist())):
        mask = stress["family"] == family
        family_decisions = [row for i, row in enumerate(best_decisions) if bool(mask[i])]
        before_family = via_metrics(pred[mask], stress["truth"][mask])
        filtered_family = filtered[mask]
        after_family = via_metrics(filtered_family, stress["truth"][mask])
        after_family.update(_presence_metrics_from_decisions(family_decisions))
        family_rows.append(
            {
                "family": str(family),
                "n_cases": int(np.sum(mask)),
                "input_gap_rel_l2_to_val": next((r["input_gap_rel_l2_to_val"] for r in stress["family_rows"] if r["family"] == family), 0.0),
                "before": before_family,
                "after": after_family,
            }
        )
    pareto_max = int(gcfg.get("pareto_max_points", 36))
    sorted_grid = sorted(
        grid,
        key=lambda r: (
            -r["validation"]["via_presence_recall"],
            r["validation"]["via_false_positive_rate_no_via"],
            -r["validation"]["via_presence_f1"],
            r["params"]["score_threshold"],
        ),
    )
    pareto_points: list[dict[str, Any]] = []
    seen_keys: set[tuple[float, float, float]] = set()
    for row in sorted_grid:
        key = (
            round(float(row["params"]["score_threshold"]), 10),
            round(float(row["params"]["artifact_radius_px"]), 4),
            round(float(row["params"]["artifact_physical_override"]), 4),
        )
        if key in seen_keys:
            continue
        seen_keys.add(key)
        pareto_points.append(
            {
                "params": row["params"],
                "validation": row["validation"],
                "objective": row["objective"],
                "feasible_recall": row.get("feasible_recall", False),
                "selected": row["params"] == best_params,
            }
        )
        if len(pareto_points) >= pareto_max:
            break
    return {
        "enabled": True,
        "calibration_split": "val_synthetic_null_via_stress",
        "used_for_training": False,
        "used_for_pypeec_threshold_selection": False,
        "used_for_pypeec_calibration": False,
        "model_used_for_calibration": "unet_topology_soft_loss",
        "selected_params": best_params,
        "validation_before": before,
        "validation_after": after,
        "validation_family_rows": family_rows,
        "pareto_points": pareto_points,
        "grid_search_rows": [
            {
                "score_threshold": row["params"]["score_threshold"],
                "artifact_radius_px": row["params"]["artifact_radius_px"],
                "artifact_physical_override": row["params"]["artifact_physical_override"],
                "objective": row["objective"],
                "feasible_recall": row.get("feasible_recall", False),
                **row["validation"],
            }
            for row in sorted(grid, key=lambda r: r["objective"], reverse=True)[:20]
        ],
        "boundary": "Gate parameters are selected only on synthetic validation stress generated from the validation split; PyPEEC cases are not used for threshold selection.",
    }


def apply_null_via_gate(
    pred: np.ndarray,
    b_obs: np.ndarray,
    truth: np.ndarray,
    forward: dict[str, Any],
    two_stage_refiner: dict[str, Any],
    gate: dict[str, Any],
) -> tuple[np.ndarray, list[dict[str, Any]]]:
    rows = _gate_feature_rows(pred, b_obs, truth, forward, two_stage_refiner)
    decisions = _apply_null_via_gate_decisions(rows, gate["selected_params"])
    return _pred_from_gate_decisions(pred, decisions), decisions


def _pypeec_gate_pareto_rows(
    data: dict[str, Any],
    pred: np.ndarray,
    truth: np.ndarray,
    b_center: np.ndarray,
    b_pypeec: np.ndarray,
    forward: dict[str, Any],
    two_stage_refiner: dict[str, Any],
    gate: dict[str, Any],
) -> list[dict[str, Any]]:
    masks = _pypeec_subset_masks(data, truth)
    rows: list[dict[str, Any]] = []
    seen_outcomes: set[tuple[float, float, float, float, float, float]] = set()
    before_all = evaluate_frozen_prediction(pred, truth, b_center, b_pypeec, forward)
    before_subsets = {
        name: evaluate_frozen_prediction(pred[mask], truth[mask], b_center[mask], b_pypeec[mask], forward)
        for name, mask in masks.items()
        if bool(np.any(mask))
    }
    seen: set[tuple[float, float, float]] = set()
    for rank, point in enumerate(gate.get("pareto_points", []), start=1):
        params = point.get("params", {})
        key = (
            round(float(params.get("score_threshold", 0.0)), 10),
            round(float(params.get("artifact_radius_px", 0.0)), 4),
            round(float(params.get("artifact_physical_override", 0.0)), 4),
        )
        if key in seen:
            continue
        seen.add(key)
        gated_pred, decisions = apply_null_via_gate(
            pred,
            b_pypeec,
            truth,
            forward,
            two_stage_refiner,
            {"selected_params": params},
        )
        after_all = evaluate_frozen_prediction(gated_pred, truth, b_center, b_pypeec, forward)
        no_via = evaluate_frozen_prediction(
            gated_pred[masks["no_via"]],
            truth[masks["no_via"]],
            b_center[masks["no_via"]],
            b_pypeec[masks["no_via"]],
            forward,
        )
        via = evaluate_frozen_prediction(
            gated_pred[masks["via"]],
            truth[masks["via"]],
            b_center[masks["via"]],
            b_pypeec[masks["via"]],
            forward,
        )
        dense = evaluate_frozen_prediction(
            gated_pred[masks["dense_via"]],
            truth[masks["dense_via"]],
            b_center[masks["dense_via"]],
            b_pypeec[masks["dense_via"]],
            forward,
        )
        return_path = evaluate_frozen_prediction(
            gated_pred[masks["return_path"]],
            truth[masks["return_path"]],
            b_center[masks["return_path"]],
            b_pypeec[masks["return_path"]],
            forward,
        )
        row_out = {
            "rank": rank,
            "selected": bool(point.get("selected", False)),
            "score_threshold": float(params.get("score_threshold", 0.0)),
            "artifact_radius_px": float(params.get("artifact_radius_px", 0.0)),
            "artifact_physical_override": float(params.get("artifact_physical_override", 0.0)),
            "validation_recall": point.get("validation", {}).get("via_presence_recall"),
            "validation_no_via_fp": point.get("validation", {}).get("via_false_positive_rate_no_via"),
            "validation_f1": point.get("validation", {}).get("via_presence_f1"),
            "validation_feasible_recall": bool(point.get("feasible_recall", False)),
            "pypeec_no_via_fp": no_via.get("via_false_positive_rate_no_via"),
            "pypeec_no_via_fp_before": before_subsets.get("no_via", {}).get("via_false_positive_rate_no_via"),
            "pypeec_via_recall": via.get("via_presence_recall"),
            "pypeec_via_recall_before": before_subsets.get("via", {}).get("via_presence_recall"),
            "pypeec_via_precision": via.get("via_presence_precision"),
            "pypeec_via_f1": via.get("via_presence_f1"),
            "pypeec_via_f1_before": before_subsets.get("via", {}).get("via_presence_f1"),
            "pypeec_dense_via_f1": dense.get("via_presence_f1"),
            "pypeec_dense_via_f1_before": before_subsets.get("dense_via", {}).get("via_presence_f1"),
            "pypeec_return_path_fp": return_path.get("via_false_positive_rate_no_via"),
            "pypeec_return_path_fp_before": before_subsets.get("return_path", {}).get("via_false_positive_rate_no_via"),
            "pypeec_topology_mse": after_all.get("topology_mse"),
            "pypeec_topology_mse_before": before_all.get("topology_mse"),
            "pypeec_physical_b": after_all.get("physical_reforward_rel_l2_to_bpypeec"),
            "pypeec_physical_b_before": before_all.get("physical_reforward_rel_l2_to_bpypeec"),
            "n_accepted": int(sum(1 for row in decisions if row["accepted"])),
            "n_rejected": int(sum(1 for row in decisions if row["candidate_present"] and not row["accepted"])),
        }
        outcome_key = (
            round(float(row_out["validation_recall"]), 4),
            round(float(row_out["validation_no_via_fp"]), 4),
            round(float(row_out["pypeec_no_via_fp"]), 4),
            round(float(row_out["pypeec_via_recall"]), 4),
            round(float(row_out["pypeec_dense_via_f1"]), 4),
            round(float(row_out["pypeec_physical_b"]), 4),
        )
        if outcome_key in seen_outcomes and not row_out["selected"]:
            continue
        seen_outcomes.add(outcome_key)
        rows.append(row_out)
    return rows


def evaluate_pypeec_null_via_hypothesis_gate(
    data: dict[str, Any],
    preds: dict[str, np.ndarray],
    truth: np.ndarray,
    b_center: np.ndarray,
    b_pypeec: np.ndarray,
    forward: dict[str, Any],
    two_stage_refiner: dict[str, Any],
    gate: dict[str, Any],
) -> dict[str, Any]:
    if not bool(gate.get("enabled", False)):
        return {"enabled": False}
    masks = _pypeec_subset_masks(data, truth)
    case_names = np.asarray(data["case_name"]).astype(str)
    case_types = np.asarray(data["case_type"]).astype(str)
    model_rows: dict[str, Any] = {}
    decision_rows: list[dict[str, Any]] = []
    for model, pred in preds.items():
        gated_pred, decisions = apply_null_via_gate(pred, b_pypeec, truth, forward, two_stage_refiner, gate)
        subsets: dict[str, Any] = {}
        for subset_name, mask in masks.items():
            if not bool(np.any(mask)):
                continue
            before = evaluate_frozen_prediction(pred[mask], truth[mask], b_center[mask], b_pypeec[mask], forward)
            after = evaluate_frozen_prediction(gated_pred[mask], truth[mask], b_center[mask], b_pypeec[mask], forward)
            subsets[subset_name] = {
                "n_cases": int(np.sum(mask)),
                "before": before,
                "after": after,
                "fp_delta_after_minus_before": after["via_false_positive_rate_no_via"] - before["via_false_positive_rate_no_via"],
                "recall_delta_after_minus_before": after["via_presence_recall"] - before["via_presence_recall"],
                "f1_delta_after_minus_before": after["via_presence_f1"] - before["via_presence_f1"],
            }
        before_all = evaluate_frozen_prediction(pred, truth, b_center, b_pypeec, forward)
        after_all = evaluate_frozen_prediction(gated_pred, truth, b_center, b_pypeec, forward)
        model_rows[model] = {
            "before": before_all,
            "after": after_all,
            "subsets": subsets,
            "n_accepted": int(sum(1 for row in decisions if row["accepted"])),
            "n_rejected": int(sum(1 for row in decisions if row["candidate_present"] and not row["accepted"])),
        }
        for row in decisions:
            idx = int(row["case_index"])
            decision_rows.append(
                {
                    "case_index": idx,
                    "case_name": str(case_names[idx]),
                    "case_type": str(case_types[idx]),
                    "model": model,
                    "true_via": bool(row["true_via"]),
                    "candidate_present": bool(row["candidate_present"]),
                    "accepted": bool(row["accepted"]),
                    "rejection_reason": str(row["rejection_reason"]),
                    "gate_score": row["gate_score"],
                    "artifact_zone": bool(row["artifact_zone"]),
                    "s1_peak_abs_current_scale": row["s1_peak_abs_current_scale"],
                    "topology_improvement": row["topology_improvement"],
                    "physical_b_improvement": row["physical_b_improvement"],
                    "distance_to_bend_px": row["distance_to_bend_px"],
                    "distance_to_return_px": row["distance_to_return_px"],
                }
            )
    topo_model = model_rows.get("unet_topology_soft_loss", {})
    topo_subsets = topo_model.get("subsets", {})
    summary = {
        "topology_model_no_via_fp_before": topo_subsets.get("no_via", {}).get("before", {}).get("via_false_positive_rate_no_via"),
        "topology_model_no_via_fp_after": topo_subsets.get("no_via", {}).get("after", {}).get("via_false_positive_rate_no_via"),
        "topology_model_via_recall_before": topo_subsets.get("via", {}).get("before", {}).get("via_presence_recall"),
        "topology_model_via_recall_after": topo_subsets.get("via", {}).get("after", {}).get("via_presence_recall"),
        "topology_model_via_f1_before": topo_subsets.get("via", {}).get("before", {}).get("via_presence_f1"),
        "topology_model_via_f1_after": topo_subsets.get("via", {}).get("after", {}).get("via_presence_f1"),
        "topology_model_dense_via_f1_before": topo_subsets.get("dense_via", {}).get("before", {}).get("via_presence_f1"),
        "topology_model_dense_via_f1_after": topo_subsets.get("dense_via", {}).get("after", {}).get("via_presence_f1"),
        "topology_model_return_path_fp_before": topo_subsets.get("return_path", {}).get("before", {}).get("via_false_positive_rate_no_via"),
        "topology_model_return_path_fp_after": topo_subsets.get("return_path", {}).get("after", {}).get("via_false_positive_rate_no_via"),
        "topology_model_topology_mse_before": topo_model.get("before", {}).get("topology_mse"),
        "topology_model_topology_mse_after": topo_model.get("after", {}).get("topology_mse"),
        "topology_model_physical_b_pypeec_before": topo_model.get("before", {}).get("physical_reforward_rel_l2_to_bpypeec"),
        "topology_model_physical_b_pypeec_after": topo_model.get("after", {}).get("physical_reforward_rel_l2_to_bpypeec"),
    }
    pareto_rows = _pypeec_gate_pareto_rows(
        data,
        preds["unet_topology_soft_loss"],
        truth,
        b_center,
        b_pypeec,
        forward,
        two_stage_refiner,
        gate,
    )
    return {
        "enabled": True,
        "calibration_split": gate.get("calibration_split"),
        "used_for_training": False,
        "used_for_pypeec_threshold_selection": False,
        "used_for_pypeec_calibration": False,
        "selected_params": gate.get("selected_params", {}),
        "models": model_rows,
        "decision_rows": decision_rows,
        "pareto_rows": pareto_rows,
        "summary": summary,
        "boundary": "Frozen PyPEEC evaluation of a gate selected only on synthetic validation stress.",
    }


def build_pypeec_null_via_hypothesis_evidence(
    data: dict[str, Any],
    preds: dict[str, np.ndarray],
    truth: np.ndarray,
    b_pypeec: np.ndarray,
    forward: dict[str, Any],
    two_stage_refiner: dict[str, Any],
    gate: dict[str, Any],
) -> dict[str, Any]:
    if not bool(gate.get("enabled", False)):
        return {"enabled": False}
    case_names = np.asarray(data["case_name"]).astype(str)
    case_types = np.asarray(data["case_type"]).astype(str)
    is_exp03_like = np.asarray(data["is_exp03_like"], dtype=bool)
    params = gate.get("selected_params", {})
    evidence_params = {
        "bend_radius_px": params.get("artifact_radius_px", 2.0),
        "return_radius_px": params.get("return_radius_px", 2.0),
    }
    rows: list[dict[str, Any]] = []
    for model, pred in preds.items():
        feature_rows = _gate_feature_rows(pred, b_pypeec, truth, forward, two_stage_refiner)
        gate_decisions = _apply_null_via_gate_decisions(feature_rows, params)
        for feature, gate_row in zip(feature_rows, gate_decisions):
            idx = int(feature["case_index"])
            evidence = null_via_hypothesis_evidence(feature, evidence_params)
            rows.append(
                {
                    "case_index": idx,
                    "case_name": str(case_names[idx]),
                    "case_type": str(case_types[idx]),
                    "is_exp03_like": bool(is_exp03_like[idx]),
                    "model": model,
                    **feature,
                    **evidence,
                    "selected_gate_score": gate_row.get("gate_score"),
                    "selected_gate_accepted": bool(gate_row.get("accepted", False)),
                    "selected_gate_rejection_reason": str(gate_row.get("rejection_reason", "")),
                    "used_for_pypeec_threshold_selection": False,
                    "used_for_pypeec_calibration": False,
                }
            )
    return {
        "enabled": True,
        "calibration_split": gate.get("calibration_split"),
        "used_for_training": False,
        "used_for_pypeec_threshold_selection": False,
        "used_for_pypeec_calibration": False,
        "rows": rows,
        "summary": summarize_evidence_rows(rows),
        "boundary": (
            "Evidence comparison is a frozen diagnostic over PyPEEC rows. "
            "It reports H1(true-via) versus H0(artifact/no-via) evidence and does not select a PyPEEC threshold."
        ),
    }


def build_pypeec_uncertainty_refusal(
    evidence: dict[str, Any],
) -> dict[str, Any]:
    if not bool(evidence.get("enabled", False)):
        return {"enabled": False}
    rows = evidence.get("rows", [])
    summary: dict[str, Any] = {}
    for model in sorted({str(row.get("model")) for row in rows}):
        model_rows = [row for row in rows if str(row.get("model")) == model]
        truth_via = [row for row in model_rows if row.get("true_via", False)]
        truth_no_via = [row for row in model_rows if not row.get("true_via", False)]
        high_via = [row for row in model_rows if row.get("decision") == "high_confidence_via"]
        no_via_high = [row for row in truth_no_via if row.get("decision") == "high_confidence_via"]
        via_refused = [row for row in truth_via if row.get("decision") != "high_confidence_via"]
        ambiguous = [
            row
            for row in model_rows
            if row.get("decision") in {"low_confidence_residual", "return_path_ambiguous", "needs_extra_observation"}
        ]
        summary[model] = {
            "n_rows": len(model_rows),
            "high_confidence_via_rate": len(high_via) / max(len(model_rows), 1),
            "no_via_high_confidence_false_alarm_rate": len(no_via_high) / max(len(truth_no_via), 1),
            "true_via_refusal_or_low_confidence_rate": len(via_refused) / max(len(truth_via), 1),
            "ambiguous_or_refusal_rate": len(ambiguous) / max(len(model_rows), 1),
            "mean_uncertainty_proxy": _finite_mean([row.get("uncertainty_proxy") for row in model_rows]),
        }
    return {
        "enabled": True,
        "rows": [
            {
                "case_index": int(row["case_index"]),
                "case_name": row.get("case_name"),
                "case_type": row.get("case_type"),
                "model": row.get("model"),
                "true_via": bool(row.get("true_via", False)),
                "decision": row.get("decision"),
                "uncertainty_proxy": row.get("uncertainty_proxy"),
                "evidence_margin_h1_minus_h0": row.get("evidence_margin_h1_minus_h0"),
                "return_path_evidence": row.get("return_path_evidence"),
                "selected_gate_accepted": bool(row.get("selected_gate_accepted", False)),
            }
            for row in rows
        ],
        "summary": summary,
        "boundary": (
            "Refusal labels are diagnostic confidence categories. They do not change the reported frozen model predictions "
            "or choose PyPEEC thresholds."
        ),
    }


def build_pypeec_generative_hypothesis_scoring(
    evidence: dict[str, Any],
    gate: dict[str, Any],
) -> dict[str, Any]:
    if not bool(evidence.get("enabled", False)):
        return {"enabled": False}
    params = gate.get("selected_params", {})
    score_params = {
        "bend_radius_px": params.get("artifact_radius_px", 2.0),
        "return_radius_px": params.get("return_radius_px", 2.0),
    }
    rows: list[dict[str, Any]] = []
    for row in evidence.get("rows", []):
        score = generative_hypothesis_score(row, score_params)
        out_row = {
            "case_index": int(row.get("case_index", -1)),
            "case_name": row.get("case_name"),
            "case_type": row.get("case_type"),
            "is_exp03_like": bool(row.get("is_exp03_like", False)),
            "model": row.get("model"),
            "true_via": bool(row.get("true_via", False)),
            "candidate_present": bool(row.get("candidate_present", False)),
            "s1_peak_abs_current_scale": row.get("s1_peak_abs_current_scale"),
            "topology_pred": row.get("topology_pred"),
            "topology_zero_s1": row.get("topology_zero_s1"),
            "physical_b_pred": row.get("physical_b_pred"),
            "physical_b_zero_s1": row.get("physical_b_zero_s1"),
            "distance_to_bend_px": row.get("distance_to_bend_px"),
            "distance_to_return_px": row.get("distance_to_return_px"),
            **score,
            "generative_abs_margin": abs(float(score["delta_evidence_h1_minus_h0"])),
            "used_for_pypeec_threshold_selection": False,
            "used_for_pypeec_calibration": False,
        }
        rows.append(out_row)
    summary: dict[str, Any] = {}
    calibration_rows: list[dict[str, Any]] = []
    for model in sorted({str(row.get("model")) for row in rows}):
        model_rows = [row for row in rows if str(row.get("model")) == model]
        scores = [float(row.get("delta_evidence_h1_minus_h0", 0.0)) for row in model_rows]
        labels = [bool(row.get("true_via", False)) for row in model_rows]
        favored_h1 = [row for row in model_rows if float(row.get("delta_evidence_h1_minus_h0", 0.0)) > 0.0]
        false_h1 = [row for row in favored_h1 if not row.get("true_via", False)]
        true_h1 = [row for row in favored_h1 if row.get("true_via", False)]
        true_via = [row for row in model_rows if row.get("true_via", False)]
        no_via = [row for row in model_rows if not row.get("true_via", False)]
        precision = len(true_h1) / max(len(favored_h1), 1)
        recall = len(true_h1) / max(len(true_via), 1)
        summary[model] = {
            "n_rows": len(model_rows),
            "auc_true_via_vs_no_via": binary_auc(labels, scores),
            "mean_delta_evidence_h1_minus_h0": _finite_mean(scores),
            "h1_favored_fraction": len(favored_h1) / max(len(model_rows), 1),
            "h1_precision": precision,
            "h1_recall": recall,
            "h1_f1": 2.0 * precision * recall / max(precision + recall, 1e-30),
            "no_via_h1_false_positive_rate": len(false_h1) / max(len(no_via), 1),
            "mean_generative_uncertainty": _finite_mean([row.get("generative_uncertainty_proxy") for row in model_rows]),
        }
        for cal_row in calibration_curve(
            model_rows,
            "delta_evidence_h1_minus_h0",
            "true_via",
            n_bins=6,
        ):
            calibration_rows.append({"model": model, **cal_row})
    return {
        "enabled": True,
        "calibration_split": evidence.get("calibration_split"),
        "used_for_training": False,
        "used_for_pypeec_threshold_selection": False,
        "used_for_pypeec_calibration": False,
        "rows": rows,
        "summary": summary,
        "calibration_rows": calibration_rows,
        "boundary": (
            "Generative hypothesis scoring compares explicit H1(with predicted s1) and H0(same prediction with s1 zeroed) "
            "re-forward energies. It is a frozen PyPEEC diagnostic and does not select thresholds."
        ),
    }


def build_pypeec_selective_risk(
    generative: dict[str, Any],
) -> dict[str, Any]:
    if not bool(generative.get("enabled", False)):
        return {"enabled": False}
    rows = generative.get("rows", [])
    curve_rows: list[dict[str, Any]] = []
    summary: dict[str, Any] = {}
    for model in sorted({str(row.get("model")) for row in rows}):
        model_rows = [row for row in rows if str(row.get("model")) == model]
        model_curve = selective_risk_curve(
            model_rows,
            "delta_evidence_h1_minus_h0",
            "true_via",
            "generative_abs_margin",
        )
        for row in model_curve:
            curve_rows.append({"model": model, **row})
        low_cov = next((row for row in model_curve if row["coverage"] >= 0.20), model_curve[0] if model_curve else {})
        full = model_curve[-1] if model_curve else {}
        summary[model] = {
            "n_rows": len(model_rows),
            "selective_risk_at_20pct_coverage": low_cov.get("selective_risk"),
            "selective_accuracy_at_20pct_coverage": low_cov.get("selective_accuracy"),
            "full_coverage_risk": full.get("selective_risk"),
            "full_coverage_accuracy": full.get("selective_accuracy"),
            "boundary": "Selective prediction reports risk only over accepted high-confidence rows; it does not change frozen predictions.",
        }
    return {
        "enabled": True,
        "rows": curve_rows,
        "summary": summary,
        "used_for_training": False,
        "used_for_pypeec_threshold_selection": False,
        "used_for_pypeec_calibration": False,
        "boundary": (
            "Risk-coverage diagnostic for refusing low-confidence via/no-via decisions using the absolute generative evidence margin."
        ),
    }


def build_pypeec_return_current_aware_generator(
    data: dict[str, Any],
    truth: np.ndarray,
    b_pypeec: np.ndarray,
    forward: dict[str, Any],
) -> dict[str, Any]:
    masks = _pypeec_subset_masks(data, truth)
    return_mask = masks.get("return_path", np.zeros(truth.shape[0], dtype=bool))
    case_names = np.asarray(data["case_name"]).astype(str)
    case_types = np.asarray(data["case_type"]).astype(str)
    rows: list[dict[str, Any]] = []
    for idx in np.where(return_mask)[0]:
        signal = np.zeros_like(truth[idx : idx + 1])
        return_current = np.zeros_like(truth[idx : idx + 1])
        signal[:, 0:2] = truth[idx : idx + 1, 0:2]
        signal[:, 4] = truth[idx : idx + 1, 4]
        return_current[:, 2:4] = truth[idx : idx + 1, 2:4]
        b_signal = raster_physical_forward(signal, forward)
        b_return = raster_physical_forward(return_current, forward)
        target = b_pypeec[idx : idx + 1]
        denom = float(np.sum(b_return * b_return) + 1e-30)
        alpha = float(np.sum((target - b_signal) * b_return) / denom)
        alpha_clipped = float(np.clip(alpha, -3.0, 3.0))
        b_centerline = raster_physical_forward(truth[idx : idx + 1], forward)
        b_alpha = b_signal + alpha_clipped * b_return
        center_resid = rel_l2(b_centerline, target)
        signal_only_resid = rel_l2(b_signal, target)
        return_fit_resid = rel_l2(b_alpha, target)
        scalar, shape_resid = _scalar_fit_residual(b_alpha, target)
        rows.append(
            {
                "case_index": int(idx),
                "case_name": str(case_names[idx]),
                "case_type": str(case_types[idx]),
                "alpha_return_fit": alpha_clipped,
                "alpha_return_unclipped": alpha,
                "centerline_truth_rel_l2_to_pypeec": center_resid,
                "signal_only_rel_l2_to_pypeec": signal_only_resid,
                "return_current_aware_rel_l2_to_pypeec": return_fit_resid,
                "return_current_aware_shape_rel_l2_to_pypeec": shape_resid,
                "return_current_aware_scalar_fit": scalar,
                "improvement_over_centerline": center_resid - return_fit_resid,
                "improvement_over_signal_only": signal_only_resid - return_fit_resid,
            }
        )
    summary = {
        "n_cases": len(rows),
        "mean_centerline_rel_l2": _finite_mean([row["centerline_truth_rel_l2_to_pypeec"] for row in rows]),
        "mean_return_current_aware_rel_l2": _finite_mean([row["return_current_aware_rel_l2_to_pypeec"] for row in rows]),
        "mean_improvement_over_centerline": _finite_mean([row["improvement_over_centerline"] for row in rows]),
        "median_alpha_return_fit": float(np.median([row["alpha_return_fit"] for row in rows])) if rows else float("nan"),
    }
    return {
        "enabled": True,
        "mode": "oracle_signal_plus_scalar_return_current_generator",
        "used_for_training": False,
        "used_for_threshold_selection": False,
        "used_for_model_prediction": False,
        "rows": rows,
        "summary": summary,
        "boundary": (
            "Oracle diagnostic only: it uses known return-current labels to test whether a signal-plus-return-current basis can "
            "explain PyPEEC return-path fields. It is not an inference model and does not alter predictions."
        ),
    }


def build_pypeec_heldout_split_evaluation(
    protocol: dict[str, Any],
    data: dict[str, Any],
    preds: dict[str, np.ndarray],
    truth: np.ndarray,
    b_center: np.ndarray,
    b_pypeec: np.ndarray,
    forward: dict[str, Any],
) -> dict[str, Any]:
    if not protocol.get("rows"):
        return {"enabled": False}
    roles = np.asarray([row.get("future_role") for row in protocol["rows"]], dtype=object)
    out_rows: list[dict[str, Any]] = []
    role_summary: dict[str, Any] = {}
    for role in sorted(set(str(r) for r in roles)):
        mask = roles == role
        if not bool(np.any(mask)):
            continue
        role_summary[role] = {"n_cases": int(np.sum(mask))}
        for model, pred in preds.items():
            metrics = evaluate_frozen_prediction(pred[mask], truth[mask], b_center[mask], b_pypeec[mask], forward)
            role_summary[role][model] = metrics
            out_rows.append(
                {
                    "future_role": role,
                    "model": model,
                    "n_cases": int(np.sum(mask)),
                    "overall_rel_l2": metrics.get("overall_rel_l2"),
                    "topology_mse": metrics.get("topology_mse"),
                    "via_recall": metrics.get("via_presence_recall"),
                    "via_f1": metrics.get("via_presence_f1"),
                    "no_via_fp": metrics.get("via_false_positive_rate_no_via"),
                    "physical_b_pypeec": metrics.get("physical_reforward_rel_l2_to_bpypeec"),
                }
            )
    return {
        "enabled": True,
        "current_protocol": "frozen_no_calibration_split_report",
        "used_for_current_training": False,
        "used_for_current_threshold_selection": False,
        "used_for_current_calibration": False,
        "rows": out_rows,
        "role_summary": role_summary,
        "boundary": (
            "Reports current frozen metrics by the reserved future calibration/test roles. No parameter is selected from these roles in this run."
        ),
    }


def write_metrics_table(metrics: dict[str, Any], out: Path) -> None:
    methods = [
        "zero",
        "ridge",
        "ridge_posthoc_topology",
        "physics_tikhonov",
        "physics_tikhonov_posthoc_topology",
        "unet_no_topology",
        "unet_topology_soft_loss",
        "unet_topology_two_stage_refined",
        "unet_topology_posthoc",
    ]
    header = "| model | test overall | OOD overall | test topo MSE | OOD topo MSE | s1 L2 | via hit | via F1 | leakage | fitted proxy | physical B |\n"
    sep = "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n"
    lines = [header, sep]
    for m in methods:
        test = metrics["benchmark"]["test"][m]
        ood = metrics["benchmark"]["ood"][m]
        lines.append(
            f"| `{m}` | {test['overall_rel_l2']:.3f} | {ood['overall_rel_l2']:.3f} | "
            f"{test['topology_mse']:.3e} | {ood['topology_mse']:.3e} | "
            f"{test['s1_rel_l2']:.3f} | {test['via_hit_rate_within_2px']:.3f} | "
            f"{test['via_presence_f1']:.3f} | {test['layer_leakage_proxy']:.3f} | "
            f"{test['field_residual_proxy_rel_l2']:.3f} | {test['physical_reforward_rel_l2_to_bclean']:.3f} |\n"
        )
    (out / "METRICS_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_channel_metrics_table(metrics: dict[str, Any], out: Path) -> None:
    methods = [
        "unet_no_topology",
        "unet_topology_soft_loss",
        "unet_topology_two_stage_refined",
        "unet_topology_posthoc",
    ]
    lines = [
        "| model | channel | active | truth norm | rel L2 | RMSE/current scale |\n",
        "|---|---|---:|---:|---:|---:|\n",
    ]
    for method in methods:
        row = metrics["benchmark"]["test"][method]
        for idx, ch in enumerate(CHANNELS):
            rel = row["per_channel_rel_l2"][idx]
            rel_text = "inactive" if rel is None else f"{rel:.3f}"
            lines.append(
                f"| `{method}` | `{ch}` | {str(row['active_channel_mask'][idx]).lower()} | "
                f"{row['truth_channel_l2_norm'][idx]:.3e} | {rel_text} | "
                f"{row['per_channel_rmse_current_scale'][idx]:.3e} |\n"
            )
    (out / "CHANNEL_METRICS_TABLE.md").write_text("".join(lines), encoding="utf-8")


def summarize_stress_benchmark(stress: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for case, methods in stress.items():
        no = methods["unet_no_topology"]
        topo = methods["unet_topology_soft_loss"]
        rows.append(
            {
                "case": case,
                "topology_mse_ratio": topo["topology_mse"] / (no["topology_mse"] + 1e-30),
                "overall_l2_ratio": topo["overall_rel_l2"] / (no["overall_rel_l2"] + 1e-30),
                "via_hit_delta": topo["via_hit_rate_within_2px"] - no["via_hit_rate_within_2px"],
            }
        )
    if not rows:
        return {"runs": []}
    topo = np.array([r["topology_mse_ratio"] for r in rows], dtype=float)
    l2 = np.array([r["overall_l2_ratio"] for r in rows], dtype=float)
    return {
        "runs": rows,
        "topology_mse_ratio_mean": float(np.mean(topo)),
        "topology_mse_ratio_max": float(np.max(topo)),
        "overall_l2_ratio_mean": float(np.mean(l2)),
        "overall_l2_ratio_max": float(np.max(l2)),
    }


def write_stress_metrics_table(metrics: dict[str, Any], out: Path) -> None:
    lines = [
        "| case | no-topo L2 | topo L2 | L2 ratio | no-topo topo MSE | topo topo MSE | topo ratio | no-topo via hit | topo via hit | no-topo physical B | topo physical B |\n",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for case, methods in metrics.get("stress_benchmark", {}).items():
        no = methods["unet_no_topology"]
        topo = methods["unet_topology_soft_loss"]
        lines.append(
            f"| `{case}` | {no['overall_rel_l2']:.3f} | {topo['overall_rel_l2']:.3f} | "
            f"{topo['overall_rel_l2'] / (no['overall_rel_l2'] + 1e-30):.3f} | "
            f"{no['topology_mse']:.3e} | {topo['topology_mse']:.3e} | "
            f"{topo['topology_mse'] / (no['topology_mse'] + 1e-30):.3f} | "
            f"{no['via_hit_rate_within_2px']:.3f} | {topo['via_hit_rate_within_2px']:.3f} | "
            f"{no['physical_reforward_rel_l2_to_bclean']:.3f} | {topo['physical_reforward_rel_l2_to_bclean']:.3f} |\n"
        )
    (out / "STRESS_METRICS_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_operator_stress_table(metrics: dict[str, Any], out: Path) -> None:
    case = metrics.get("stress_benchmark", {}).get("finite_width_return", {})
    stress_input = case.get("stress_input", {})
    methods = [
        "unet_no_topology",
        "unet_topology_soft_loss",
        "unet_topology_two_stage_refined",
    ]
    no = case.get("unet_no_topology", {})
    lines = [
        "# Finite-Width / Return-Current Stress\n\n",
        f"- input gap to clean centerline field: `{float(stress_input.get('input_gap_rel_l2_to_clean', float('nan'))):.3f}`\n",
        f"- surrogate model: `{stress_input.get('model', 'not reported')}`\n\n",
        "| model | overall L2 | L2 ratio | topology MSE | topology ratio | s1 L2 | via hit | via F1 | leakage | physical B clean | physical B obs |\n",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for name in methods:
        row = case.get(name, {})
        l2_ratio = row.get("overall_rel_l2", float("nan")) / (no.get("overall_rel_l2", float("nan")) + 1e-30)
        topo_ratio = row.get("topology_mse", float("nan")) / (no.get("topology_mse", float("nan")) + 1e-30)
        lines.append(
            f"| `{name}` | {row.get('overall_rel_l2', float('nan')):.3f} | {l2_ratio:.3f} | "
            f"{row.get('topology_mse', float('nan')):.3e} | {topo_ratio:.3f} | "
            f"{row.get('s1_rel_l2', float('nan')):.3f} | {row.get('via_hit_rate_within_2px', float('nan')):.3f} | "
            f"{row.get('via_presence_f1', float('nan')):.3f} | {row.get('layer_leakage_proxy', float('nan')):.3f} | "
            f"{row.get('physical_reforward_rel_l2_to_bclean', float('nan')):.3f} | "
            f"{row.get('physical_reforward_rel_l2_to_bobs', float('nan')):.3f} |\n"
        )
    (out / "OPERATOR_STRESS_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_operator_stress_table(metrics: dict[str, Any], out: Path) -> None:
    bridge = metrics.get("pypeec_operator_stress_bridge", {})
    lines = [
        "# Real PyPEEC Frozen Operator-Stress Bridge\n\n",
        f"- mode: `{bridge.get('mode', 'not enabled')}`\n",
        f"- artifact available: `{bridge.get('artifact_available', False)}`\n",
        f"- used for training: `{bridge.get('used_for_training', False)}`\n",
        f"- used for validation thresholds: `{bridge.get('used_for_validation_thresholds', False)}`\n",
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
        "\nBoundary: this table is a frozen exp07 artifact summary attached to exp04. "
        "It does not claim that the U-Net has already been evaluated on a full "
        "PyPEEC-generated exp03 dataset.\n"
    )
    (out / "PYPEEC_OPERATOR_STRESS_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_frozen_inference_table(metrics: dict[str, Any], out: Path) -> None:
    frozen = metrics.get("pypeec_frozen_inference", {})
    summary = frozen.get("summary", {})
    lines = [
        "# Real PyPEEC Frozen Inference Stress\n\n",
        f"- artifact available: `{frozen.get('artifact_available', False)}`\n",
        f"- split: `{frozen.get('split', 'not reported')}`\n",
        f"- cases: `{frozen.get('n_cases', 0)}`\n",
        f"- exp03-like cases: `{frozen.get('n_exp03_like_cases', 0)}`\n",
        f"- input gap PyPEEC vs centerline: `{float(frozen.get('input_gap_rel_l2_pypeec_to_centerline', float('nan'))):.6g}`\n",
        f"- topology/no-topology topology MSE ratio: `{float(summary.get('topology_mse_ratio_topology_over_no_topology', float('nan'))):.6g}`\n",
        f"- topology/no-topology overall L2 ratio: `{float(summary.get('overall_l2_ratio_topology_over_no_topology', float('nan'))):.6g}`\n",
        f"- used for training: `{frozen.get('used_for_training', False)}`\n",
        f"- used for validation thresholds: `{frozen.get('used_for_validation_thresholds', False)}`\n",
        f"- used for calibration: `{frozen.get('used_for_calibration', False)}`\n\n",
        "| model | overall L2 | L2 ratio | topology MSE | topology ratio | s1 L2 | via hit | via F1 | no-via FP | leakage | physical B center | physical B PyPEEC |\n",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    methods = frozen.get("methods", {})
    no = methods.get("unet_no_topology", {})
    for name in ["unet_no_topology", "unet_topology_soft_loss", "unet_topology_two_stage_refined"]:
        row = methods.get(name, {})
        l2_ratio = row.get("overall_rel_l2", float("nan")) / (no.get("overall_rel_l2", float("nan")) + 1e-30)
        topo_ratio = row.get("topology_mse", float("nan")) / (no.get("topology_mse", float("nan")) + 1e-30)
        lines.append(
            f"| `{name}` | {row.get('overall_rel_l2', float('nan')):.3f} | {l2_ratio:.3f} | "
            f"{row.get('topology_mse', float('nan')):.3e} | {topo_ratio:.3f} | "
            f"{row.get('s1_rel_l2', float('nan')):.3f} | {row.get('via_hit_rate_within_2px', float('nan')):.3f} | "
            f"{row.get('via_presence_f1', float('nan')):.3f} | {row.get('via_false_positive_rate_no_via', float('nan')):.3f} | "
            f"{row.get('layer_leakage_proxy', float('nan')):.3f} | "
            f"{row.get('physical_reforward_rel_l2_to_bcenter', float('nan')):.3f} | "
            f"{row.get('physical_reforward_rel_l2_to_bpypeec', float('nan')):.3f} |\n"
        )
    lines.append(
        "\nBoundary: this is frozen inference on the exp07 mini PyPEEC dataset. "
        "No PyPEEC samples are used for training, validation threshold selection, "
        "or calibration.\n"
    )
    (out / "PYPEEC_FROZEN_INFERENCE_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_frozen_inference_subset_table(metrics: dict[str, Any], out: Path) -> None:
    frozen = metrics.get("pypeec_frozen_inference", {})
    lines = [
        "# Real PyPEEC Frozen Inference Subset Stress\n\n",
        "| subset | cases | input gap | model | overall L2 | L2 ratio | topology MSE | topology ratio | s1 RMSE | via hit | via F1 | no-via FP | physical B PyPEEC |\n",
        "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for subset_name, subset in frozen.get("subsets", {}).items():
        methods = subset.get("methods", {})
        no = methods.get("unet_no_topology", {})
        for model_name in ["unet_no_topology", "unet_topology_soft_loss", "unet_topology_two_stage_refined"]:
            row = methods.get(model_name, {})
            l2_ratio = row.get("overall_rel_l2", float("nan")) / (no.get("overall_rel_l2", float("nan")) + 1e-30)
            topo_ratio = row.get("topology_mse", float("nan")) / (no.get("topology_mse", float("nan")) + 1e-30)
            s1_rmse = row.get("per_channel_rmse_current_scale", [float("nan")] * 5)[4]
            lines.append(
                f"| `{subset_name}` | {subset.get('n_cases', 0)} | "
                f"{subset.get('input_gap_rel_l2_pypeec_to_centerline', float('nan')):.3f} | "
                f"`{model_name}` | {row.get('overall_rel_l2', float('nan')):.3f} | {l2_ratio:.3f} | "
                f"{row.get('topology_mse', float('nan')):.3e} | {topo_ratio:.3f} | "
                f"{s1_rmse:.3f} | {row.get('via_hit_rate_within_2px', float('nan')):.3f} | "
                f"{row.get('via_presence_f1', float('nan')):.3f} | {row.get('via_false_positive_rate_no_via', float('nan')):.3f} | "
                f"{row.get('physical_reforward_rel_l2_to_bpypeec', float('nan')):.3f} |\n"
            )
    lines.append(
        "\nBoundary: subset rows are descriptive diagnostics over the current exp07 mini distribution. "
        "They are not validation-selected thresholds and should not be treated as a broad PyPEEC distribution proof.\n"
    )
    (out / "PYPEEC_FROZEN_INFERENCE_SUBSET_TABLE.md").write_text("".join(lines), encoding="utf-8")


def _md_value(value: Any, digits: int = 3) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return "yes" if value else "no"
    try:
        fvalue = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not np.isfinite(fvalue):
        return "n/a"
    if abs(fvalue) > 0.0 and (abs(fvalue) < 1e-3 or abs(fvalue) >= 1e4):
        return f"{fvalue:.3e}"
    return f"{fvalue:.{digits}f}"


def write_pypeec_null_via_diagnostics_table(metrics: dict[str, Any], out: Path) -> None:
    diag = metrics.get("pypeec_frozen_inference", {}).get("null_via_diagnostics", {})
    lines = [
        "# Real PyPEEC No-Via False-Positive Diagnostics\n\n",
        f"- no-via cases: `{diag.get('n_cases', 0)}`\n",
        f"- presence threshold: `{_md_value(diag.get('presence_threshold'), digits=6)}`\n",
        f"- boundary: {diag.get('boundary', 'diagnostic only')}\n\n",
        "## Summary\n\n",
        "| model | cases | FP rate | mean s1 peak | mean topology MSE | mean physical B PyPEEC | mean leakage | dominant failure modes |\n",
        "|---|---:|---:|---:|---:|---:|---:|---|\n",
    ]
    for model, row in diag.get("summary", {}).items():
        modes = row.get("failure_mode_counts", {})
        mode_text = ", ".join(f"{name}: {count}" for name, count in sorted(modes.items())) or "n/a"
        lines.append(
            f"| `{model}` | {row.get('n_cases', 0)} | {_md_value(row.get('false_positive_rate'))} | "
            f"{_md_value(row.get('mean_s1_peak_current_scale'))} | {_md_value(row.get('mean_topology_mse'))} | "
            f"{_md_value(row.get('mean_physical_b_residual_to_pypeec'))} | {_md_value(row.get('mean_layer_leakage_proxy'))} | "
            f"{mode_text} |\n"
        )
    lines.extend(
        [
            "\n## Per-Case Rows\n\n",
            "| case | type | model | FP | s1 peak | s1 rms | via px | comp | d trace | d bend | d return | topology MSE | B PyPEEC | gap | leakage | failure mode |\n",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|\n",
        ]
    )
    for row in diag.get("rows", []):
        lines.append(
            f"| `{row.get('case_name')}` | `{row.get('case_type')}` | `{row.get('model')}` | "
            f"{_md_value(row.get('false_positive'))} | {_md_value(row.get('s1_peak_abs_current_scale'))} | "
            f"{_md_value(row.get('s1_rms_current_scale'))} | {row.get('predicted_via_pixels', 0)} | "
            f"{row.get('predicted_via_components', 0)} | {_md_value(row.get('distance_to_trace_px'))} | "
            f"{_md_value(row.get('distance_to_bend_px'))} | {_md_value(row.get('distance_to_return_px'))} | "
            f"{_md_value(row.get('topology_mse'))} | {_md_value(row.get('physical_reforward_rel_l2_to_bpypeec'))} | "
            f"{_md_value(row.get('pypeec_centerline_gap_rel_l2'))} | {_md_value(row.get('layer_leakage_proxy'))} | "
            f"{row.get('failure_mode', 'not classified')} |\n"
        )
    lines.append(
        "\nInterpretation: these rows classify PyPEEC no-via false positives after inference. "
        "They do not tune a PyPEEC-specific detector threshold.\n"
    )
    (out / "PYPEEC_NULL_VIA_DIAGNOSTICS_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_null_via_mechanism_summary(metrics: dict[str, Any], out: Path) -> None:
    diag = metrics.get("pypeec_frozen_inference", {}).get("null_via_diagnostics", {})
    lines = [
        "# Real PyPEEC No-Via Mechanism Summary\n\n",
        "This table aggregates only false-positive no-via rows. It quantifies which mechanisms dominate the current PyPEEC mini stress failures without selecting any PyPEEC-specific threshold.\n\n",
        "| model | mechanism | count | % FP | mean s1 peak | mean topology MSE | mean B PyPEEC | mean gap | d trace | d bend | d return |\n",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for model, summary in diag.get("mechanism_summary", {}).items():
        mechanisms = summary.get("mechanisms", {})
        if not mechanisms:
            lines.append(f"| `{model}` | `no false positives` | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |\n")
            continue
        for mechanism, row in mechanisms.items():
            lines.append(
                f"| `{model}` | `{mechanism}` | {row.get('count', 0)} | "
                f"{_md_value(row.get('percentage_of_false_positives'))} | "
                f"{_md_value(row.get('mean_s1_peak_current_scale'))} | "
                f"{_md_value(row.get('mean_topology_mse'))} | "
                f"{_md_value(row.get('mean_physical_b_residual_to_pypeec'))} | "
                f"{_md_value(row.get('mean_pypeec_centerline_gap'))} | "
                f"{_md_value(row.get('mean_distance_to_trace_px'))} | "
                f"{_md_value(row.get('mean_distance_to_bend_px'))} | "
                f"{_md_value(row.get('mean_distance_to_return_px'))} |\n"
            )
    lines.append(
        "\nInterpretation: high bend/corner counts mean the dominant false-positive mechanism is local operator/geometric residual rather than random detector noise.\n"
    )
    (out / "PYPEEC_NULL_VIA_MECHANISM_SUMMARY.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_null_via_failure_cases(metrics: dict[str, Any], out: Path) -> None:
    diag = metrics.get("pypeec_frozen_inference", {}).get("null_via_diagnostics", {})
    rows = [row for row in diag.get("rows", []) if row.get("false_positive", False)]
    rows.sort(
        key=lambda row: (
            float(row.get("s1_peak_abs_current_scale", 0.0)),
            float(row.get("physical_reforward_rel_l2_to_bpypeec", 0.0)),
        ),
        reverse=True,
    )
    lines = [
        "# Real PyPEEC No-Via Failure Cases\n\n",
        "This is a diagnostic list of no-via cases where the frozen model predicts a nonzero via/source channel. "
        "It is used to identify mechanisms, not to select PyPEEC-specific thresholds.\n\n",
    ]
    if not rows:
        lines.append("No no-via false positives were found in the current PyPEEC mini distribution.\n")
    for row in rows[:30]:
        lines.extend(
            [
                f"## `{row.get('case_name')}` / `{row.get('model')}`\n\n",
                f"- case type: `{row.get('case_type')}`\n",
                f"- failure mode: `{row.get('failure_mode', 'not classified')}`\n",
                f"- s1 peak / rms current scale: `{_md_value(row.get('s1_peak_abs_current_scale'))}` / `{_md_value(row.get('s1_rms_current_scale'))}`\n",
                f"- peak location: `({row.get('s1_peak_y')}, {row.get('s1_peak_x')})`\n",
                f"- predicted via pixels / components: `{row.get('predicted_via_pixels', 0)}` / `{row.get('predicted_via_components', 0)}`\n",
                f"- distance to trace / bend / return: `{_md_value(row.get('distance_to_trace_px'))}` / `{_md_value(row.get('distance_to_bend_px'))}` / `{_md_value(row.get('distance_to_return_px'))}` px\n",
                f"- topology MSE / leakage: `{_md_value(row.get('topology_mse'))}` / `{_md_value(row.get('layer_leakage_proxy'))}`\n",
                f"- physical B residual to PyPEEC / PyPEEC-centerline gap: `{_md_value(row.get('physical_reforward_rel_l2_to_bpypeec'))}` / `{_md_value(row.get('pypeec_centerline_gap_rel_l2') )}`\n\n",
            ]
        )
    (out / "PYPEEC_NULL_VIA_FAILURE_CASES.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_return_path_diagnostics_table(metrics: dict[str, Any], out: Path) -> None:
    diag = metrics.get("pypeec_frozen_inference", {}).get("return_path_diagnostics", {})
    lines = [
        "# Real PyPEEC Return-Path Diagnostics\n\n",
        f"- return-path cases: `{diag.get('n_cases', 0)}`\n",
        f"- boundary: {diag.get('boundary', 'diagnostic only')}\n\n",
        "## Summary\n\n",
        "| model | cases | mean return allocation error | mean topology MSE | mean physical B PyPEEC | mean shape B PyPEEC | mean leakage | dominant failure modes | detailed mechanisms |\n",
        "|---|---:|---:|---:|---:|---:|---:|---|---|\n",
    ]
    for model, row in diag.get("summary", {}).items():
        modes = row.get("failure_mode_counts", {})
        mode_text = ", ".join(f"{name}: {count}" for name, count in sorted(modes.items())) or "n/a"
        lines.append(
            f"| `{model}` | {row.get('n_cases', 0)} | {_md_value(row.get('mean_layer_allocation_fraction_error'))} | "
            f"{_md_value(row.get('mean_topology_mse'))} | {_md_value(row.get('mean_physical_b_residual_to_pypeec'))} | "
            f"{_md_value(row.get('mean_physical_b_shape_residual_to_pypeec'))} | "
            f"{_md_value(row.get('mean_layer_leakage_proxy'))} | {mode_text} | "
            f"{', '.join(f'{name}: {count}' for name, count in sorted(row.get('mechanism_counts', {}).items())) or 'n/a'} |\n"
        )
    lines.extend(
        [
            "\n## Per-Case Rows\n\n",
            "| case | type | model | truth return frac | pred return frac | alloc err | signal L2 | return L2 | excess via comp | topology MSE | leakage | raw B | shape B | scalar fit | delta vs no-topo | gap | mechanism | failure mode |\n",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|\n",
        ]
    )
    for row in diag.get("rows", []):
        lines.append(
            f"| `{row.get('case_name')}` | `{row.get('case_type')}` | `{row.get('model')}` | "
            f"{_md_value(row.get('truth_return_fraction'))} | {_md_value(row.get('pred_return_fraction'))} | "
            f"{_md_value(row.get('layer_allocation_fraction_error'))} | {_md_value(row.get('signal_path_rel_l2'))} | "
            f"{_md_value(row.get('return_path_rel_l2'))} | {row.get('excess_predicted_via_components', 0)} | "
            f"{_md_value(row.get('topology_mse'))} | {_md_value(row.get('layer_leakage_proxy'))} | "
            f"{_md_value(row.get('physical_reforward_rel_l2_to_bpypeec'))} | "
            f"{_md_value(row.get('physical_reforward_shape_rel_l2_to_bpypeec'))} | "
            f"{_md_value(row.get('physical_reforward_scalar_fit_to_bpypeec'))} | "
            f"{_md_value(row.get('physical_b_delta_vs_no_topology'))} | "
            f"{_md_value(row.get('pypeec_centerline_gap_rel_l2'))} | {row.get('mechanism', 'not classified')} | "
            f"{row.get('failure_mode', 'not classified')} |\n"
        )
    lines.append(
        "\nInterpretation: return-path rows separate current allocation, topology residual, and magnetic consistency. "
        "A lower pixel-space L2 can still coincide with worse PyPEEC re-forward residual.\n"
    )
    (out / "PYPEEC_RETURN_PATH_DIAGNOSTICS_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_return_path_mechanism_summary(metrics: dict[str, Any], out: Path) -> None:
    diag = metrics.get("pypeec_frozen_inference", {}).get("return_path_diagnostics", {})
    lines = [
        "# Real PyPEEC Return-Path Mechanism Summary\n\n",
        "This table splits return-path magnetic consistency failures into amplitude, spatial-shape, layer-allocation, and mixed mechanisms. It is descriptive failure analysis, not a model update.\n\n",
        "| model | mechanism | count | % cases | raw B | shape B | scalar fit | amplitude log error | alloc err | return L2 | topology MSE |\n",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for model, summary in diag.get("mechanism_summary", {}).items():
        for mechanism, row in summary.get("mechanisms", {}).items():
            lines.append(
                f"| `{model}` | `{mechanism}` | {row.get('count', 0)} | "
                f"{_md_value(row.get('percentage_of_cases'))} | "
                f"{_md_value(row.get('mean_raw_b_residual_to_pypeec'))} | "
                f"{_md_value(row.get('mean_shape_b_residual_to_pypeec'))} | "
                f"{_md_value(row.get('mean_scalar_fit_to_pypeec'))} | "
                f"{_md_value(row.get('mean_amplitude_log_error'))} | "
                f"{_md_value(row.get('mean_layer_allocation_fraction_error'))} | "
                f"{_md_value(row.get('mean_return_path_rel_l2'))} | "
                f"{_md_value(row.get('mean_topology_mse'))} |\n"
            )
    lines.append(
        "\nInterpretation: raw B residual separates magnetic consistency from pixel-space current error; scalar-fitted shape residual distinguishes amplitude mismatch from spatial-shape mismatch.\n"
    )
    (out / "PYPEEC_RETURN_PATH_MECHANISM_SUMMARY.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_return_path_failure_modes(metrics: dict[str, Any], out: Path) -> None:
    diag = metrics.get("pypeec_frozen_inference", {}).get("return_path_diagnostics", {})
    rows = list(diag.get("rows", []))
    rows.sort(
        key=lambda row: (
            float(row.get("physical_reforward_rel_l2_to_bpypeec", 0.0)),
            float(row.get("layer_allocation_fraction_error", 0.0)),
        ),
        reverse=True,
    )
    lines = [
        "# Real PyPEEC Return-Path Failure Modes\n\n",
        "This report ranks return-path rows by PyPEEC magnetic residual and current-allocation error. "
        "It documents where return current remains an independent physical challenge for the current two-layer model.\n\n",
    ]
    for row in rows[:30]:
        lines.extend(
            [
                f"## `{row.get('case_name')}` / `{row.get('model')}`\n\n",
                f"- case type: `{row.get('case_type')}`\n",
                f"- failure mode: `{row.get('failure_mode', 'not classified')}`\n",
                f"- detailed mechanism: `{row.get('mechanism', 'not classified')}`\n",
                f"- truth/pred return fraction: `{_md_value(row.get('truth_return_fraction'))}` / `{_md_value(row.get('pred_return_fraction'))}`\n",
                f"- allocation error: `{_md_value(row.get('layer_allocation_fraction_error'))}`\n",
                f"- signal/return path L2: `{_md_value(row.get('signal_path_rel_l2'))}` / `{_md_value(row.get('return_path_rel_l2'))}`\n",
                f"- true/pred/excess via components: `{row.get('true_via_components', 0)}` / `{row.get('predicted_via_components', 0)}` / `{row.get('excess_predicted_via_components', 0)}`\n",
                f"- topology MSE / leakage: `{_md_value(row.get('topology_mse'))}` / `{_md_value(row.get('layer_leakage_proxy'))}`\n",
                f"- raw/shape physical B residual to PyPEEC: `{_md_value(row.get('physical_reforward_rel_l2_to_bpypeec'))}` / `{_md_value(row.get('physical_reforward_shape_rel_l2_to_bpypeec'))}`\n",
                f"- scalar fit to PyPEEC / delta vs no-topology: `{_md_value(row.get('physical_reforward_scalar_fit_to_bpypeec'))}` / `{_md_value(row.get('physical_b_delta_vs_no_topology'))}`\n\n",
            ]
        )
    (out / "PYPEEC_RETURN_PATH_FAILURE_MODES.md").write_text("".join(lines), encoding="utf-8")


def write_null_via_validation_stress_table(metrics: dict[str, Any], out: Path) -> None:
    gate = metrics.get("null_via_hypothesis_gate", {})
    lines = [
        "# Null-Via Synthetic Validation Stress\n\n",
        f"- enabled: `{gate.get('enabled', False)}`\n",
        f"- calibration split: `{gate.get('calibration_split', 'not reported')}`\n",
        f"- used for PyPEEC threshold selection: `{gate.get('used_for_pypeec_threshold_selection', True)}`\n",
        f"- boundary: {gate.get('boundary', 'not reported')}\n\n",
        "## Selected Gate\n\n",
        f"- score threshold: `{_md_value(gate.get('selected_params', {}).get('score_threshold'))}`\n",
        f"- artifact radius px: `{_md_value(gate.get('selected_params', {}).get('artifact_radius_px'))}`\n",
        f"- return radius px: `{_md_value(gate.get('selected_params', {}).get('return_radius_px'))}`\n",
        f"- artifact physical override: `{_md_value(gate.get('selected_params', {}).get('artifact_physical_override'))}`\n\n",
        "## Validation Before/After\n\n",
        "| split | precision | recall | F1 | no-via FP | pred present | TP | FP |\n",
        "|---|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for label, row in [("before", gate.get("validation_before", {})), ("after", gate.get("validation_after", {}))]:
        lines.append(
            f"| `{label}` | {_md_value(row.get('via_presence_precision'))} | {_md_value(row.get('via_presence_recall'))} | "
            f"{_md_value(row.get('via_presence_f1'))} | {_md_value(row.get('via_false_positive_rate_no_via'))} | "
            f"{row.get('pred_present', 'n/a')} | {row.get('true_positive', 'n/a')} | {row.get('false_positive', 'n/a')} |\n"
        )
    lines.extend(
        [
            "\n## Family Rows\n\n",
            "| family | cases | input gap | FP before | FP after | recall before | recall after | F1 before | F1 after |\n",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|\n",
        ]
    )
    for row in gate.get("validation_family_rows", []):
        before = row.get("before", {})
        after = row.get("after", {})
        lines.append(
            f"| `{row.get('family')}` | {row.get('n_cases', 0)} | {_md_value(row.get('input_gap_rel_l2_to_val'))} | "
            f"{_md_value(before.get('via_false_positive_rate_no_via'))} | {_md_value(after.get('via_false_positive_rate_no_via'))} | "
            f"{_md_value(before.get('via_presence_recall'))} | {_md_value(after.get('via_presence_recall'))} | "
            f"{_md_value(before.get('via_presence_f1'))} | {_md_value(after.get('via_presence_f1'))} |\n"
        )
    lines.append(
        "\nInterpretation: this table is the only place where the null-via gate parameters are selected. "
        "It uses synthetic validation stress, not PyPEEC test cases.\n"
    )
    (out / "NULL_VIA_VALIDATION_STRESS_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_null_via_hypothesis_gate_table(metrics: dict[str, Any], out: Path) -> None:
    gate = metrics.get("pypeec_frozen_inference", {}).get("null_via_hypothesis_gate", {})
    summary = gate.get("summary", {})
    lines = [
        "# Null-Via Hypothesis Gate On Frozen PyPEEC Stress\n\n",
        f"- enabled: `{gate.get('enabled', False)}`\n",
        f"- calibration split: `{gate.get('calibration_split', 'not reported')}`\n",
        f"- used for PyPEEC threshold selection: `{gate.get('used_for_pypeec_threshold_selection', True)}`\n",
        f"- used for PyPEEC calibration: `{gate.get('used_for_pypeec_calibration', True)}`\n",
        f"- boundary: {gate.get('boundary', 'not reported')}\n\n",
        "## Topology Model Summary\n\n",
        f"- no-via FP before/after: `{_md_value(summary.get('topology_model_no_via_fp_before'))}` / `{_md_value(summary.get('topology_model_no_via_fp_after'))}`\n",
        f"- via recall before/after: `{_md_value(summary.get('topology_model_via_recall_before'))}` / `{_md_value(summary.get('topology_model_via_recall_after'))}`\n",
        f"- via F1 before/after: `{_md_value(summary.get('topology_model_via_f1_before'))}` / `{_md_value(summary.get('topology_model_via_f1_after'))}`\n",
        f"- dense-via F1 before/after: `{_md_value(summary.get('topology_model_dense_via_f1_before'))}` / `{_md_value(summary.get('topology_model_dense_via_f1_after'))}`\n",
        f"- return-path FP before/after: `{_md_value(summary.get('topology_model_return_path_fp_before'))}` / `{_md_value(summary.get('topology_model_return_path_fp_after'))}`\n",
        f"- topology MSE before/after: `{_md_value(summary.get('topology_model_topology_mse_before'))}` / `{_md_value(summary.get('topology_model_topology_mse_after'))}`\n",
        f"- physical B PyPEEC before/after: `{_md_value(summary.get('topology_model_physical_b_pypeec_before'))}` / `{_md_value(summary.get('topology_model_physical_b_pypeec_after'))}`\n\n",
        "## Model/Subset Trade-Offs\n\n",
        "| model | subset | cases | FP before | FP after | recall before | recall after | F1 before | F1 after | topology before | topology after | B PyPEEC before | B PyPEEC after |\n",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for model, model_row in gate.get("models", {}).items():
        for subset_name, subset in model_row.get("subsets", {}).items():
            before = subset.get("before", {})
            after = subset.get("after", {})
            lines.append(
                f"| `{model}` | `{subset_name}` | {subset.get('n_cases', 0)} | "
                f"{_md_value(before.get('via_false_positive_rate_no_via'))} | {_md_value(after.get('via_false_positive_rate_no_via'))} | "
                f"{_md_value(before.get('via_presence_recall'))} | {_md_value(after.get('via_presence_recall'))} | "
                f"{_md_value(before.get('via_presence_f1'))} | {_md_value(after.get('via_presence_f1'))} | "
                f"{_md_value(before.get('topology_mse'))} | {_md_value(after.get('topology_mse'))} | "
                f"{_md_value(before.get('physical_reforward_rel_l2_to_bpypeec'))} | {_md_value(after.get('physical_reforward_rel_l2_to_bpypeec'))} |\n"
            )
    lines.extend(
        [
            "\n## Rejection Reasons\n\n",
            "| model | reason | count |\n",
            "|---|---|---:|\n",
        ]
    )
    reason_counts: dict[tuple[str, str], int] = {}
    for row in gate.get("decision_rows", []):
        if not row.get("candidate_present", False) or row.get("accepted", False):
            continue
        key = (str(row.get("model")), str(row.get("rejection_reason")))
        reason_counts[key] = reason_counts.get(key, 0) + 1
    for (model, reason), count in sorted(reason_counts.items()):
        lines.append(f"| `{model}` | `{reason}` | {count} |\n")
    lines.append(
        "\nInterpretation: this is a frozen PyPEEC evaluation of a gate selected on synthetic validation stress. "
        "It reports the false-positive/recall trade-off and should not be described as PyPEEC-calibrated.\n"
    )
    (out / "NULL_VIA_HYPOTHESIS_GATE_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_null_via_gate_pareto_table(metrics: dict[str, Any], out: Path) -> None:
    gate = metrics.get("pypeec_frozen_inference", {}).get("null_via_hypothesis_gate", {})
    rows = gate.get("pareto_rows", [])
    lines = [
        "# Null-Via Gate Pareto Table\n\n",
        f"- calibration split: `{gate.get('calibration_split', 'not reported')}`\n",
        f"- used for PyPEEC threshold selection: `{gate.get('used_for_pypeec_threshold_selection', True)}`\n",
        f"- used for PyPEEC calibration: `{gate.get('used_for_pypeec_calibration', True)}`\n\n",
        "Each row is a validation-defined operating point evaluated frozen on PyPEEC. "
        "Rows are for `unet_topology_soft_loss`; they are descriptive and are not used to select a PyPEEC threshold.\n\n",
        "| selected | score thr | artifact px | physical override | validation recall | validation FP | PyPEEC no-via FP | PyPEEC via recall | PyPEEC via F1 | PyPEEC dense F1 | PyPEEC return FP | topo MSE | physical B |\n",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for row in rows:
        lines.append(
            f"| {int(bool(row.get('selected', False)))} | {_md_value(row.get('score_threshold'))} | "
            f"{_md_value(row.get('artifact_radius_px'))} | {_md_value(row.get('artifact_physical_override'))} | "
            f"{_md_value(row.get('validation_recall'))} | "
            f"{_md_value(row.get('validation_no_via_fp'))} | {_md_value(row.get('pypeec_no_via_fp'))} | "
            f"{_md_value(row.get('pypeec_via_recall'))} | {_md_value(row.get('pypeec_via_f1'))} | "
            f"{_md_value(row.get('pypeec_dense_via_f1'))} | {_md_value(row.get('pypeec_return_path_fp'))} | "
            f"{_md_value(row.get('pypeec_topology_mse'))} | {_md_value(row.get('pypeec_physical_b'))} |\n"
        )
    lines.append(
        "\nInterpretation: the useful claim is the trade-off shape, not a single best PyPEEC point. "
        "The selected row is chosen before PyPEEC evaluation using synthetic validation stress only.\n"
    )
    (out / "NULL_VIA_GATE_PARETO_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_null_via_hypothesis_evidence_table(metrics: dict[str, Any], out: Path) -> None:
    evidence = metrics.get("pypeec_frozen_inference", {}).get("null_via_hypothesis_evidence", {})
    lines = [
        "# Null-Via Hypothesis Evidence Comparison\n\n",
        f"- enabled: `{evidence.get('enabled', False)}`\n",
        f"- calibration split: `{evidence.get('calibration_split', 'not reported')}`\n",
        f"- used for PyPEEC threshold selection: `{evidence.get('used_for_pypeec_threshold_selection', True)}`\n",
        f"- used for PyPEEC calibration: `{evidence.get('used_for_pypeec_calibration', True)}`\n",
        f"- boundary: {evidence.get('boundary', 'not reported')}\n\n",
        "## Summary\n\n",
        "| model | rows | high-conf via | probable artifact | ambiguous/refusal | mean uncertainty | decisions |\n",
        "|---|---:|---:|---:|---:|---:|---|\n",
    ]
    for model, row in evidence.get("summary", {}).items():
        counts = ", ".join(f"{name}: {count}" for name, count in sorted(row.get("decision_counts", {}).items()))
        lines.append(
            f"| `{model}` | {row.get('n_rows', 0)} | {_md_value(row.get('high_confidence_via_fraction'))} | "
            f"{_md_value(row.get('probable_artifact_fraction'))} | {_md_value(row.get('ambiguous_or_refusal_fraction'))} | "
            f"{_md_value(row.get('mean_uncertainty_proxy'))} | {counts or 'n/a'} |\n"
        )
    lines.extend(
        [
            "\n## Per-Case Evidence Rows\n\n",
            "| case | type | model | true via | candidate | H1 via | H0 artifact | margin | uncertainty | return evidence | bend prox | return prox | decision | selected gate |\n",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|\n",
        ]
    )
    rows = evidence.get("rows", [])
    rows = sorted(
        rows,
        key=lambda row: (
            str(row.get("model")),
            -float(row.get("uncertainty_proxy", 0.0)),
            str(row.get("case_name")),
        ),
    )
    for row in rows[:240]:
        lines.append(
            f"| `{row.get('case_name')}` | `{row.get('case_type')}` | `{row.get('model')}` | "
            f"{_md_value(row.get('true_via'))} | {_md_value(row.get('candidate_present'))} | "
            f"{_md_value(row.get('h1_true_via_evidence'))} | {_md_value(row.get('h0_artifact_evidence'))} | "
            f"{_md_value(row.get('evidence_margin_h1_minus_h0'))} | {_md_value(row.get('uncertainty_proxy'))} | "
            f"{_md_value(row.get('return_path_evidence'))} | {_md_value(row.get('bend_proximity'))} | "
            f"{_md_value(row.get('return_proximity'))} | `{row.get('decision')}` | "
            f"{_md_value(row.get('selected_gate_accepted'))} |\n"
        )
    lines.append(
        "\nInterpretation: these rows compare H1(true via/source-sink) against H0(artifact/no-via) evidence. "
        "They expose confidence and ambiguity; they do not tune PyPEEC thresholds.\n"
    )
    (out / "NULL_VIA_HYPOTHESIS_EVIDENCE_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_heldout_split_protocol(metrics: dict[str, Any], out: Path) -> None:
    protocol = metrics.get("pypeec_frozen_inference", {}).get("heldout_split_protocol", {})
    lines = [
        "# PyPEEC Held-Out Split Protocol\n\n",
        f"- protocol version: `{protocol.get('protocol_version', 'not reported')}`\n",
        f"- current protocol: `{protocol.get('current_protocol', 'not reported')}`\n",
        f"- used for current training: `{protocol.get('used_for_current_training', True)}`\n",
        f"- used for current threshold selection: `{protocol.get('used_for_current_threshold_selection', True)}`\n",
        f"- used for current calibration: `{protocol.get('used_for_current_calibration', True)}`\n",
        f"- boundary: {protocol.get('boundary', 'not reported')}\n\n",
        "## Family Summary\n\n",
        "| family | total | future calibration candidates | future held-out test |\n",
        "|---|---:|---:|---:|\n",
    ]
    for family, row in sorted(protocol.get("family_summary", {}).items()):
        lines.append(
            f"| `{family}` | {row.get('total', 0)} | {row.get('future_calibration_candidate', 0)} | "
            f"{row.get('future_heldout_test', 0)} |\n"
        )
    lines.extend(
        [
            "\n## Case Rows\n\n",
            "| idx | case | type | family | future role | score | adjustment | current threshold use |\n",
            "|---:|---|---|---|---|---:|---|---:|\n",
        ]
    )
    for row in protocol.get("rows", []):
        lines.append(
            f"| {row.get('case_index')} | `{row.get('case_name')}` | `{row.get('case_type')}` | "
            f"`{row.get('family')}` | `{row.get('future_role')}` | {_md_value(row.get('split_score'))} | "
            f"`{row.get('role_adjustment', 'none')}` | "
            f"{_md_value(row.get('used_for_current_threshold_selection'))} |\n"
        )
    lines.append(
        "\nInterpretation: this file reserves a future legal calibration/held-out protocol. "
        "The current PyPEEC results remain frozen no-calibration evaluation.\n"
    )
    (out / "PYPEEC_HELDOUT_SPLIT_PROTOCOL.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_return_path_hypothesis_table(metrics: dict[str, Any], out: Path) -> None:
    diag = metrics.get("pypeec_frozen_inference", {}).get("return_path_diagnostics", {})
    lines = [
        "# Return-Path Hypothesis Diagnostics\n\n",
        f"- cases: `{diag.get('n_cases', 0)}`\n",
        f"- boundary: {diag.get('boundary', 'not reported')}\n\n",
        "## Summary\n\n",
        "| model | rows | mean return-via margin | decisions |\n",
        "|---|---:|---:|---|\n",
    ]
    for model, row in diag.get("hypothesis_summary", {}).items():
        counts = ", ".join(f"{name}: {count}" for name, count in sorted(row.get("decision_counts", {}).items()))
        lines.append(
            f"| `{model}` | {row.get('n_rows', 0)} | {_md_value(row.get('mean_return_margin_minus_via'))} | "
            f"{counts or 'n/a'} |\n"
        )
    lines.extend(
        [
            "\n## Case Rows\n\n",
            "| case | model | via-like | return-like | return-via margin | decision | raw B | shape B | alloc err | return L2 | excess via |\n",
            "|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|\n",
        ]
    )
    for row in diag.get("rows", []):
        lines.append(
            f"| `{row.get('case_name')}` | `{row.get('model')}` | {_md_value(row.get('via_like_evidence'))} | "
            f"{_md_value(row.get('return_current_evidence'))} | {_md_value(row.get('return_margin_minus_via'))} | "
            f"`{row.get('hypothesis_decision')}` | {_md_value(row.get('physical_reforward_rel_l2_to_bpypeec'))} | "
            f"{_md_value(row.get('physical_reforward_shape_rel_l2_to_bpypeec'))} | "
            f"{_md_value(row.get('layer_allocation_fraction_error'))} | {_md_value(row.get('return_path_rel_l2'))} | "
            f"{row.get('excess_predicted_via_components', 0)} |\n"
        )
    lines.append(
        "\nInterpretation: this is a return-current versus via-like evidence table. "
        "It supports return-path-aware modeling decisions but does not alter current predictions.\n"
    )
    (out / "PYPEEC_RETURN_PATH_HYPOTHESIS_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_null_via_uncertainty_refusal_table(metrics: dict[str, Any], out: Path) -> None:
    refusal = metrics.get("pypeec_frozen_inference", {}).get("uncertainty_refusal", {})
    lines = [
        "# Null-Via Uncertainty And Refusal Diagnostics\n\n",
        f"- enabled: `{refusal.get('enabled', False)}`\n",
        f"- boundary: {refusal.get('boundary', 'not reported')}\n\n",
        "## Summary\n\n",
        "| model | rows | high-conf via rate | no-via high-conf false alarm | true-via refusal/low-conf | ambiguous/refusal | mean uncertainty |\n",
        "|---|---:|---:|---:|---:|---:|---:|\n",
    ]
    for model, row in refusal.get("summary", {}).items():
        lines.append(
            f"| `{model}` | {row.get('n_rows', 0)} | {_md_value(row.get('high_confidence_via_rate'))} | "
            f"{_md_value(row.get('no_via_high_confidence_false_alarm_rate'))} | "
            f"{_md_value(row.get('true_via_refusal_or_low_confidence_rate'))} | "
            f"{_md_value(row.get('ambiguous_or_refusal_rate'))} | {_md_value(row.get('mean_uncertainty_proxy'))} |\n"
        )
    lines.extend(
        [
            "\n## Highest-Uncertainty Rows\n\n",
            "| case | type | model | true via | decision | uncertainty | margin | return evidence | selected gate accepted |\n",
            "|---|---|---|---:|---|---:|---:|---:|---:|\n",
        ]
    )
    rows = sorted(
        refusal.get("rows", []),
        key=lambda row: float(row.get("uncertainty_proxy", 0.0)),
        reverse=True,
    )
    for row in rows[:120]:
        lines.append(
            f"| `{row.get('case_name')}` | `{row.get('case_type')}` | `{row.get('model')}` | "
            f"{_md_value(row.get('true_via'))} | `{row.get('decision')}` | {_md_value(row.get('uncertainty_proxy'))} | "
            f"{_md_value(row.get('evidence_margin_h1_minus_h0'))} | {_md_value(row.get('return_path_evidence'))} | "
            f"{_md_value(row.get('selected_gate_accepted'))} |\n"
        )
    lines.append(
        "\nInterpretation: refusal is a reporting layer for ambiguous residuals. It is meant to prevent overclaiming high-confidence via diagnosis from a single passive field.\n"
    )
    (out / "NULL_VIA_UNCERTAINTY_REFUSAL_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_null_via_generative_hypothesis_table(metrics: dict[str, Any], out: Path) -> None:
    gen = metrics.get("pypeec_frozen_inference", {}).get("null_via_generative_hypothesis", {})
    lines = [
        "# Null-Via Generative Hypothesis Scoring\n\n",
        f"- enabled: `{gen.get('enabled', False)}`\n",
        f"- used for PyPEEC threshold selection: `{gen.get('used_for_pypeec_threshold_selection', True)}`\n",
        f"- used for PyPEEC calibration: `{gen.get('used_for_pypeec_calibration', True)}`\n",
        f"- boundary: {gen.get('boundary', 'not reported')}\n\n",
        "Positive `Delta evidence H1-H0` means the explicit H1 model with predicted `s1` has lower energy than the H0 model with `s1=0`.\n\n",
        "## Summary\n\n",
        "| model | rows | AUC | mean DeltaE | H1 favored | H1 precision | H1 recall | H1 F1 | no-via H1 FP | mean uncertainty |\n",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for model, row in gen.get("summary", {}).items():
        lines.append(
            f"| `{model}` | {row.get('n_rows', 0)} | {_md_value(row.get('auc_true_via_vs_no_via'))} | "
            f"{_md_value(row.get('mean_delta_evidence_h1_minus_h0'))} | {_md_value(row.get('h1_favored_fraction'))} | "
            f"{_md_value(row.get('h1_precision'))} | {_md_value(row.get('h1_recall'))} | {_md_value(row.get('h1_f1'))} | "
            f"{_md_value(row.get('no_via_h1_false_positive_rate'))} | {_md_value(row.get('mean_generative_uncertainty'))} |\n"
        )
    lines.extend(
        [
            "\n## Calibration Rows\n\n",
            "| model | bin | n | score min | score max | score mean | observed true-via rate | observed no-via rate |\n",
            "|---|---:|---:|---:|---:|---:|---:|---:|\n",
        ]
    )
    for row in gen.get("calibration_rows", []):
        lines.append(
            f"| `{row.get('model')}` | {row.get('bin')} | {row.get('n')} | {_md_value(row.get('score_min'))} | "
            f"{_md_value(row.get('score_max'))} | {_md_value(row.get('score_mean'))} | "
            f"{_md_value(row.get('observed_true_via_rate'))} | {_md_value(row.get('observed_no_via_rate'))} |\n"
        )
    lines.extend(
        [
            "\n## Highest-Margin Rows\n\n",
            "| case | type | model | true via | candidate | DeltaE H1-H0 | E(H1) | E(H0) | physical gain | artifact prox | decision |\n",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|\n",
        ]
    )
    rows = sorted(
        gen.get("rows", []),
        key=lambda row: abs(float(row.get("delta_evidence_h1_minus_h0", 0.0))),
        reverse=True,
    )
    for row in rows[:180]:
        lines.append(
            f"| `{row.get('case_name')}` | `{row.get('case_type')}` | `{row.get('model')}` | "
            f"{_md_value(row.get('true_via'))} | {_md_value(row.get('candidate_present'))} | "
            f"{_md_value(row.get('delta_evidence_h1_minus_h0'))} | {_md_value(row.get('generative_energy_h1_with_s1'))} | "
            f"{_md_value(row.get('generative_energy_h0_zero_s1'))} | {_md_value(row.get('generative_physical_gain_h1_over_h0'))} | "
            f"{_md_value(row.get('generative_artifact_proximity'))} | `{row.get('generative_decision')}` |\n"
        )
    lines.append(
        "\nInterpretation: this is still diagnostic. It upgrades rule evidence into an explicit H1-vs-H0 re-forward energy comparison, but it does not claim a solved detector.\n"
    )
    (out / "NULL_VIA_GENERATIVE_HYPOTHESIS_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_return_current_aware_generator_table(metrics: dict[str, Any], out: Path) -> None:
    gen = metrics.get("pypeec_frozen_inference", {}).get("return_current_aware_generator", {})
    summary = gen.get("summary", {})
    lines = [
        "# Return-Current-Aware Generator Diagnostic\n\n",
        f"- enabled: `{gen.get('enabled', False)}`\n",
        f"- mode: `{gen.get('mode', 'not reported')}`\n",
        f"- used for model prediction: `{gen.get('used_for_model_prediction', True)}`\n",
        f"- boundary: {gen.get('boundary', 'not reported')}\n\n",
        "## Summary\n\n",
        f"- return-path cases: `{summary.get('n_cases', 0)}`\n",
        f"- mean centerline residual: `{_md_value(summary.get('mean_centerline_rel_l2'))}`\n",
        f"- mean return-current-aware residual: `{_md_value(summary.get('mean_return_current_aware_rel_l2'))}`\n",
        f"- mean improvement over centerline: `{_md_value(summary.get('mean_improvement_over_centerline'))}`\n",
        f"- median fitted return alpha: `{_md_value(summary.get('median_alpha_return_fit'))}`\n\n",
        "## Case Rows\n\n",
        "| case | type | alpha | centerline B | signal-only B | signal+alpha return B | shape B | scalar fit | improvement |\n",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for row in gen.get("rows", []):
        lines.append(
            f"| `{row.get('case_name')}` | `{row.get('case_type')}` | {_md_value(row.get('alpha_return_fit'))} | "
            f"{_md_value(row.get('centerline_truth_rel_l2_to_pypeec'))} | {_md_value(row.get('signal_only_rel_l2_to_pypeec'))} | "
            f"{_md_value(row.get('return_current_aware_rel_l2_to_pypeec'))} | "
            f"{_md_value(row.get('return_current_aware_shape_rel_l2_to_pypeec'))} | "
            f"{_md_value(row.get('return_current_aware_scalar_fit'))} | {_md_value(row.get('improvement_over_centerline'))} |\n"
        )
    lines.append(
        "\nInterpretation: this table asks whether an explicit `signal current + scalar return current` basis can explain PyPEEC return-path fields. It is an oracle diagnostic, not a deployed inference head.\n"
    )
    (out / "PYPEEC_RETURN_CURRENT_AWARE_GENERATOR_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_pypeec_heldout_split_evaluation_table(metrics: dict[str, Any], out: Path) -> None:
    evaluation = metrics.get("pypeec_frozen_inference", {}).get("heldout_split_evaluation", {})
    lines = [
        "# PyPEEC Held-Out Split Frozen Evaluation\n\n",
        f"- enabled: `{evaluation.get('enabled', False)}`\n",
        f"- current protocol: `{evaluation.get('current_protocol', 'not reported')}`\n",
        f"- used for current threshold selection: `{evaluation.get('used_for_current_threshold_selection', True)}`\n",
        f"- used for current calibration: `{evaluation.get('used_for_current_calibration', True)}`\n",
        f"- boundary: {evaluation.get('boundary', 'not reported')}\n\n",
        "| future role | model | cases | overall L2 | topology MSE | via recall | via F1 | no-via FP | physical B PyPEEC |\n",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for row in evaluation.get("rows", []):
        lines.append(
            f"| `{row.get('future_role')}` | `{row.get('model')}` | {row.get('n_cases', 0)} | "
            f"{_md_value(row.get('overall_rel_l2'))} | {_md_value(row.get('topology_mse'))} | "
            f"{_md_value(row.get('via_recall'))} | {_md_value(row.get('via_f1'))} | "
            f"{_md_value(row.get('no_via_fp'))} | {_md_value(row.get('physical_b_pypeec'))} |\n"
        )
    lines.append(
        "\nInterpretation: these are frozen metrics stratified by the reserved future split. They do not perform PyPEEC calibration in the current run.\n"
    )
    (out / "PYPEEC_HELDOUT_SPLIT_EVALUATION_TABLE.md").write_text("".join(lines), encoding="utf-8")


def write_null_via_selective_risk_table(metrics: dict[str, Any], out: Path) -> None:
    selective = metrics.get("pypeec_frozen_inference", {}).get("selective_risk", {})
    lines = [
        "# Null-Via Selective Risk-Coverage\n\n",
        f"- enabled: `{selective.get('enabled', False)}`\n",
        f"- used for PyPEEC threshold selection: `{selective.get('used_for_pypeec_threshold_selection', True)}`\n",
        f"- boundary: {selective.get('boundary', 'not reported')}\n\n",
        "## Summary\n\n",
        "| model | rows | risk @20% coverage | accuracy @20% coverage | full risk | full accuracy |\n",
        "|---|---:|---:|---:|---:|---:|\n",
    ]
    for model, row in selective.get("summary", {}).items():
        lines.append(
            f"| `{model}` | {row.get('n_rows', 0)} | {_md_value(row.get('selective_risk_at_20pct_coverage'))} | "
            f"{_md_value(row.get('selective_accuracy_at_20pct_coverage'))} | {_md_value(row.get('full_coverage_risk'))} | "
            f"{_md_value(row.get('full_coverage_accuracy'))} |\n"
        )
    lines.extend(
        [
            "\n## Risk-Coverage Rows\n\n",
            "| model | coverage | selected | risk | accuracy | via precision | via recall | no-via FP selected | mean confidence |\n",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|\n",
        ]
    )
    for row in selective.get("rows", []):
        lines.append(
            f"| `{row.get('model')}` | {_md_value(row.get('coverage'))} | {row.get('n_selected', 0)} | "
            f"{_md_value(row.get('selective_risk'))} | {_md_value(row.get('selective_accuracy'))} | "
            f"{_md_value(row.get('via_precision'))} | {_md_value(row.get('via_recall_within_selected'))} | "
            f"{_md_value(row.get('no_via_false_positive_rate_within_selected'))} | {_md_value(row.get('mean_confidence'))} |\n"
        )
    lines.append(
        "\nInterpretation: selective prediction is a refusal metric. A useful system must report both accuracy and coverage, not only high-confidence examples.\n"
    )
    (out / "NULL_VIA_SELECTIVE_RISK_TABLE.md").write_text("".join(lines), encoding="utf-8")


def plot_null_via_gate_pareto(metrics: dict[str, Any], out: Path) -> str | None:
    gate = metrics.get("pypeec_frozen_inference", {}).get("null_via_hypothesis_gate", {})
    rows = gate.get("pareto_rows", [])
    if not rows:
        return None
    fig_dir = out / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    fp = np.array([float(row.get("pypeec_no_via_fp", np.nan)) for row in rows], dtype=float)
    recall = np.array([float(row.get("pypeec_via_recall", np.nan)) for row in rows], dtype=float)
    dense = np.array([float(row.get("pypeec_dense_via_f1", np.nan)) for row in rows], dtype=float)
    valid = np.isfinite(fp) & np.isfinite(recall) & np.isfinite(dense)
    if not np.any(valid):
        return None
    fig, ax = plt.subplots(figsize=(6.5, 4.5), constrained_layout=True)
    scatter = ax.scatter(fp[valid], recall[valid], c=dense[valid], cmap="viridis", s=45, edgecolors="black", linewidths=0.3)
    for row in rows:
        if row.get("selected", False):
            ax.scatter(
                [float(row.get("pypeec_no_via_fp", np.nan))],
                [float(row.get("pypeec_via_recall", np.nan))],
                marker="*",
                s=180,
                c="tab:red",
                edgecolors="black",
                linewidths=0.6,
                label="selected",
            )
            break
    ax.set_xlabel("PyPEEC no-via false-positive rate")
    ax.set_ylabel("PyPEEC via recall")
    ax.set_title("Null-via gate frozen PyPEEC trade-off")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.grid(True, alpha=0.25)
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("dense-via F1")
    if any(row.get("selected", False) for row in rows):
        ax.legend(loc="lower left")
    rel_path = Path("figures") / "null_via_gate_pareto.png"
    fig.savefig(out / rel_path, dpi=180)
    plt.close(fig)
    return str(rel_path).replace("\\", "/")


def plot_null_via_generative_calibration(metrics: dict[str, Any], out: Path) -> str | None:
    gen = metrics.get("pypeec_frozen_inference", {}).get("null_via_generative_hypothesis", {})
    rows = gen.get("calibration_rows", [])
    if not rows:
        return None
    fig_dir = out / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 4.5), constrained_layout=True)
    for model in sorted({str(row.get("model")) for row in rows}):
        model_rows = [row for row in rows if str(row.get("model")) == model]
        x = [float(row.get("score_mean", np.nan)) for row in model_rows]
        y = [float(row.get("observed_true_via_rate", np.nan)) for row in model_rows]
        ax.plot(x, y, "o-", label=model)
    ax.set_xlabel("mean Delta evidence H1-H0")
    ax.set_ylabel("observed true-via rate")
    ax.set_title("Generative H0/H1 calibration diagnostic")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7)
    rel_path = Path("figures") / "null_via_generative_calibration.png"
    fig.savefig(out / rel_path, dpi=180)
    plt.close(fig)
    return str(rel_path).replace("\\", "/")


def plot_null_via_selective_risk(metrics: dict[str, Any], out: Path) -> str | None:
    selective = metrics.get("pypeec_frozen_inference", {}).get("selective_risk", {})
    rows = selective.get("rows", [])
    if not rows:
        return None
    fig_dir = out / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 4.5), constrained_layout=True)
    for model in sorted({str(row.get("model")) for row in rows}):
        model_rows = [row for row in rows if str(row.get("model")) == model]
        x = [float(row.get("coverage", np.nan)) for row in model_rows]
        y = [float(row.get("selective_risk", np.nan)) for row in model_rows]
        ax.plot(x, y, "o-", label=model)
    ax.set_xlabel("coverage")
    ax.set_ylabel("selective risk")
    ax.set_title("Null-via risk-coverage diagnostic")
    ax.set_xlim(0.0, 1.02)
    ax.set_ylim(bottom=0.0)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7)
    rel_path = Path("figures") / "null_via_selective_risk.png"
    fig.savefig(out / rel_path, dpi=180)
    plt.close(fig)
    return str(rel_path).replace("\\", "/")


def write_via_detector_table(metrics: dict[str, Any], out: Path) -> None:
    lines = [
        "| split | detector | loc error px | hit <=2px | precision | recall | F1 | false positive no-via | threshold |\n",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for split_name, rows in metrics.get("via_detection_benchmark", {}).get("splits", {}).items():
        for name, row in rows.items():
            lines.append(
                f"| `{split_name}` | `{name}` | {row['via_loc_error_px_mean']:.3f} | "
                f"{row['via_hit_rate_within_2px']:.3f} | {row['via_presence_precision']:.3f} | "
                f"{row['via_presence_recall']:.3f} | {row['via_presence_f1']:.3f} | "
                f"{row['via_false_positive_rate_no_via']:.3f} | {row['presence_threshold']:.3e} |\n"
            )
    (out / "VIA_DETECTOR_TABLE.md").write_text("".join(lines), encoding="utf-8")


def add_acceptance_gates(metrics: dict[str, Any], cfg: dict[str, Any]) -> None:
    test = metrics["benchmark"]["test"]
    ood = metrics["benchmark"]["ood"]
    gates_cfg = cfg["gates"]
    topo_ratio = test["unet_topology_soft_loss"]["topology_mse"] / (test["unet_no_topology"]["topology_mse"] + 1e-30)
    l2_ratio = test["unet_topology_soft_loss"]["overall_rel_l2"] / (test["unet_no_topology"]["overall_rel_l2"] + 1e-30)
    ood_topo_ratio = ood["unet_topology_soft_loss"]["topology_mse"] / (ood["unet_no_topology"]["topology_mse"] + 1e-30)
    multi = metrics.get("multi_seed_summary", {})
    multi_ratio = multi.get("topology_mse_ratio_mean", float("inf"))
    sweep = metrics.get("lambda_sweep_summary", {})
    sweep_topo_ratio = sweep.get("best_test_topology_ratio", float("inf"))
    sweep_l2_ratio = sweep.get("best_test_l2_ratio", float("inf"))
    stress = metrics.get("stress_summary", {})
    stress_topo_ratio = stress.get("topology_mse_ratio_mean", float("inf"))
    stress_l2_ratio = stress.get("overall_l2_ratio_max", float("inf"))
    via_det = metrics.get("via_detection_benchmark", {}).get("splits", {}).get("test", {})
    via_det_ood = metrics.get("via_detection_benchmark", {}).get("splits", {}).get("ood", {})
    raw_det = via_det.get("raw_adjoint", {})
    topo_det = via_det.get("unet_topology_soft_loss_sheet_residual", {})
    oracle_det = via_det.get("oracle_sheet_residual", {})
    ood_raw_det = via_det_ood.get("raw_adjoint", {})
    ood_topo_det = via_det_ood.get("unet_topology_soft_loss_sheet_residual", {})
    ood_topo_fp_det = via_det_ood.get("unet_topology_soft_loss_sheet_residual_dog_fp_controlled", {})
    finite_width_stress = metrics.get("stress_benchmark", {}).get("finite_width_return", {})
    finite_width_input_gap = finite_width_stress.get("stress_input", {}).get("input_gap_rel_l2_to_clean", float("nan"))
    pypeec_bridge = metrics.get("pypeec_operator_stress_bridge", {})
    pypeec_bridge_cfg = cfg.get("pypeec_operator_stress_bridge", {})
    pypeec_bridge_enabled = bool(pypeec_bridge_cfg.get("enabled", False))
    pypeec_bridge_gap = float(pypeec_bridge.get("exp03_like_shape_gap_median", float("nan")))
    pypeec_frozen = metrics.get("pypeec_frozen_inference", {})
    pypeec_frozen_cfg = cfg.get("pypeec_frozen_inference", {})
    pypeec_frozen_enabled = bool(pypeec_frozen_cfg.get("enabled", False))
    pypeec_frozen_summary = pypeec_frozen.get("summary", {})
    pypeec_null_diag = pypeec_frozen.get("null_via_diagnostics", {})
    pypeec_return_diag = pypeec_frozen.get("return_path_diagnostics", {})
    pypeec_heldout_protocol = pypeec_frozen.get("heldout_split_protocol", {})
    pypeec_heldout_evaluation = pypeec_frozen.get("heldout_split_evaluation", {})
    pypeec_hypothesis_evidence = pypeec_frozen.get("null_via_hypothesis_evidence", {})
    pypeec_generative_hypothesis = pypeec_frozen.get("null_via_generative_hypothesis", {})
    pypeec_selective_risk = pypeec_frozen.get("selective_risk", {})
    pypeec_uncertainty_refusal = pypeec_frozen.get("uncertainty_refusal", {})
    pypeec_return_generator = pypeec_frozen.get("return_current_aware_generator", {})
    null_gate_calibration = metrics.get("null_via_hypothesis_gate", {})
    null_gate_cfg = cfg.get("null_via_hypothesis_gate", {})
    null_gate_enabled = bool(null_gate_cfg.get("enabled", False))
    pypeec_null_gate = pypeec_frozen.get("null_via_hypothesis_gate", {})
    pypeec_frozen_values = []
    for row in pypeec_frozen.get("methods", {}).values():
        for key in [
            "overall_rel_l2",
            "topology_mse",
            "s1_rel_l2",
            "via_presence_f1",
            "via_hit_rate_within_2px",
            "via_false_positive_rate_no_via",
            "layer_leakage_proxy",
            "physical_reforward_rel_l2_to_bcenter",
            "physical_reforward_rel_l2_to_bpypeec",
        ]:
            pypeec_frozen_values.append(row.get(key, float("nan")))
    pypeec_subset_values = []
    for subset in pypeec_frozen.get("subsets", {}).values():
        for row in subset.get("methods", {}).values():
            for key in [
                "overall_rel_l2",
                "topology_mse",
                "s1_rel_l2",
                "via_presence_f1",
                "via_hit_rate_within_2px",
                "via_false_positive_rate_no_via",
                "physical_reforward_rel_l2_to_bpypeec",
            ]:
                pypeec_subset_values.append(row.get(key, float("nan")))
    pypeec_diag_values = []
    for diag in [pypeec_null_diag, pypeec_return_diag]:
        for row in diag.get("rows", []):
            for key in [
                "s1_peak_abs_current_scale",
                "topology_mse",
                "topology_l1_mean",
                "magnetic_residual_energy_ratio",
                "physical_reforward_rel_l2_to_bpypeec",
                "physical_reforward_shape_rel_l2_to_bpypeec",
                "physical_reforward_scalar_fit_to_bpypeec",
                "physical_reforward_amplitude_log_error_abs",
                "pypeec_centerline_gap_rel_l2",
                "layer_leakage_proxy",
                "layer_allocation_fraction_error",
                "signal_path_rel_l2",
                "return_path_rel_l2",
                "physical_b_delta_vs_no_topology",
                "via_like_evidence",
                "return_current_evidence",
                "return_margin_minus_via",
            ]:
                value = row.get(key)
                if value is not None:
                    pypeec_diag_values.append(value)
    pypeec_hypothesis_values = []
    for row in pypeec_hypothesis_evidence.get("rows", []):
        for key in [
            "h1_true_via_evidence",
            "h0_artifact_evidence",
            "return_path_evidence",
            "evidence_margin_h1_minus_h0",
            "uncertainty_proxy",
            "bend_proximity",
            "return_proximity",
            "trace_proximity",
            "selected_gate_score",
        ]:
            value = row.get(key)
            if value is not None:
                pypeec_hypothesis_values.append(value)
    pypeec_uncertainty_values = []
    for row in pypeec_uncertainty_refusal.get("summary", {}).values():
        for key in [
            "high_confidence_via_rate",
            "no_via_high_confidence_false_alarm_rate",
            "true_via_refusal_or_low_confidence_rate",
            "ambiguous_or_refusal_rate",
            "mean_uncertainty_proxy",
        ]:
            value = row.get(key)
            if value is not None:
                pypeec_uncertainty_values.append(value)
    pypeec_generative_values = []
    for row in pypeec_generative_hypothesis.get("rows", []):
        for key in [
            "generative_energy_h1_with_s1",
            "generative_energy_h0_zero_s1",
            "delta_evidence_h1_minus_h0",
            "generative_physical_gain_h1_over_h0",
            "generative_uncertainty_proxy",
            "generative_artifact_proximity",
        ]:
            value = row.get(key)
            if value is not None:
                pypeec_generative_values.append(value)
    for row in pypeec_generative_hypothesis.get("summary", {}).values():
        for key in [
            "auc_true_via_vs_no_via",
            "mean_delta_evidence_h1_minus_h0",
            "h1_favored_fraction",
            "h1_precision",
            "h1_recall",
            "h1_f1",
            "no_via_h1_false_positive_rate",
            "mean_generative_uncertainty",
        ]:
            value = row.get(key)
            if value is not None:
                pypeec_generative_values.append(value)
    pypeec_selective_values = []
    for row in pypeec_selective_risk.get("rows", []):
        for key in [
            "coverage",
            "selective_risk",
            "selective_accuracy",
            "via_precision",
            "via_recall_within_selected",
            "no_via_false_positive_rate_within_selected",
            "mean_confidence",
        ]:
            value = row.get(key)
            if value is not None:
                pypeec_selective_values.append(value)
    pypeec_return_generator_values = []
    for row in pypeec_return_generator.get("rows", []):
        for key in [
            "alpha_return_fit",
            "centerline_truth_rel_l2_to_pypeec",
            "signal_only_rel_l2_to_pypeec",
            "return_current_aware_rel_l2_to_pypeec",
            "return_current_aware_shape_rel_l2_to_pypeec",
            "return_current_aware_scalar_fit",
            "improvement_over_centerline",
        ]:
            value = row.get(key)
            if value is not None:
                pypeec_return_generator_values.append(value)
    pypeec_heldout_values = []
    for row in pypeec_heldout_evaluation.get("rows", []):
        for key in [
            "overall_rel_l2",
            "topology_mse",
            "via_recall",
            "via_f1",
            "no_via_fp",
            "physical_b_pypeec",
        ]:
            value = row.get(key)
            if value is not None:
                pypeec_heldout_values.append(value)
    null_gate_values = []
    for row in [null_gate_calibration.get("validation_before", {}), null_gate_calibration.get("validation_after", {})]:
        for key in ["via_presence_precision", "via_presence_recall", "via_presence_f1", "via_false_positive_rate_no_via"]:
            value = row.get(key)
            if value is not None:
                null_gate_values.append(value)
    for row in null_gate_calibration.get("validation_family_rows", []):
        for side in ["before", "after"]:
            for key in ["via_presence_precision", "via_presence_recall", "via_presence_f1", "via_false_positive_rate_no_via"]:
                value = row.get(side, {}).get(key)
                if value is not None:
                    null_gate_values.append(value)
        value = row.get("input_gap_rel_l2_to_val")
        if value is not None:
            null_gate_values.append(value)
    pypeec_null_gate_values = []
    for value in pypeec_null_gate.get("summary", {}).values():
        if value is not None:
            pypeec_null_gate_values.append(value)
    for model_row in pypeec_null_gate.get("models", {}).values():
        for side in ["before", "after"]:
            for key in [
                "overall_rel_l2",
                "topology_mse",
                "s1_rel_l2",
                "via_presence_precision",
                "via_presence_recall",
                "via_presence_f1",
                "via_false_positive_rate_no_via",
                "physical_reforward_rel_l2_to_bpypeec",
            ]:
                value = model_row.get(side, {}).get(key)
                if value is not None:
                    pypeec_null_gate_values.append(value)
        for subset in model_row.get("subsets", {}).values():
            for side in ["before", "after"]:
                for key in [
                    "overall_rel_l2",
                    "topology_mse",
                    "via_presence_recall",
                    "via_presence_f1",
                    "via_false_positive_rate_no_via",
                    "physical_reforward_rel_l2_to_bpypeec",
                ]:
                    value = subset.get(side, {}).get(key)
                    if value is not None:
                        pypeec_null_gate_values.append(value)
    for row in pypeec_null_gate.get("decision_rows", []):
        for key in [
            "gate_score",
            "s1_peak_abs_current_scale",
            "topology_improvement",
            "physical_b_improvement",
            "distance_to_bend_px",
            "distance_to_return_px",
        ]:
            value = row.get(key)
            if value is not None:
                pypeec_null_gate_values.append(value)
    for row in pypeec_null_gate.get("pareto_rows", []):
        for key in [
            "score_threshold",
            "artifact_radius_px",
            "artifact_physical_override",
            "validation_recall",
            "validation_no_via_fp",
            "validation_f1",
            "pypeec_no_via_fp",
            "pypeec_via_recall",
            "pypeec_via_precision",
            "pypeec_via_f1",
            "pypeec_dense_via_f1",
            "pypeec_return_path_fp",
            "pypeec_topology_mse",
            "pypeec_physical_b",
        ]:
            value = row.get(key)
            if value is not None:
                pypeec_null_gate_values.append(value)
    pypeec_required_models = [
        "unet_no_topology",
        "unet_topology_soft_loss",
        "unet_topology_two_stage_refined",
    ]
    finite_width_detail_values = []
    for method_name in ["unet_no_topology", "unet_topology_soft_loss", "unet_topology_two_stage_refined"]:
        row = finite_width_stress.get(method_name, {})
        for key in [
            "overall_rel_l2",
            "topology_mse",
            "s1_rel_l2",
            "via_presence_f1",
            "via_hit_rate_within_2px",
            "layer_leakage_proxy",
            "physical_reforward_rel_l2_to_bclean",
            "physical_reforward_rel_l2_to_bobs",
        ]:
            finite_width_detail_values.append(row.get(key, float("nan")))
    refined = test.get("unet_topology_two_stage_refined", {})
    robust_channel_values = []
    for split_name in ["test", "ood"]:
        for method_name in ["unet_no_topology", "unet_topology_soft_loss"]:
            robust_channel_values.extend(metrics["benchmark"][split_name][method_name]["per_channel_rmse_current_scale"])
    physical_values = []
    for split_name in ["test", "ood"]:
        for method_name, row in metrics["benchmark"][split_name].items():
            physical_values.append(row.get("physical_reforward_rel_l2_to_bclean", float("nan")))
    gates = {
        "dataset_splits_present": {
            "threshold": "train/val/test/ood all nonempty",
            "value": metrics["split_counts"],
            "pass": all(metrics["split_counts"].get(k, 0) > 0 for k in ["train", "val", "test", "ood"]),
        },
        "unet_no_topology_beats_zero": {
            "threshold": f"no-topology L2 < {gates_cfg['unet_beats_zero_l2_max']} * zero L2",
            "value": [test["unet_no_topology"]["overall_rel_l2"], test["zero"]["overall_rel_l2"]],
            "pass": test["unet_no_topology"]["overall_rel_l2"] < float(gates_cfg["unet_beats_zero_l2_max"]) * test["zero"]["overall_rel_l2"],
        },
        "topology_soft_reduces_test_topology_mse": {
            "threshold": f"ratio <= {gates_cfg['topology_mse_ratio_max']}",
            "value": topo_ratio,
            "pass": topo_ratio <= float(gates_cfg["topology_mse_ratio_max"]),
        },
        "topology_soft_l2_cost_is_bounded": {
            "threshold": f"ratio <= {gates_cfg['overall_l2_ratio_max']}",
            "value": l2_ratio,
            "pass": l2_ratio <= float(gates_cfg["overall_l2_ratio_max"]),
        },
        "topology_soft_reduces_ood_topology_mse": {
            "threshold": f"ratio <= {gates_cfg['ood_topology_mse_ratio_max']}",
            "value": ood_topo_ratio,
            "pass": ood_topo_ratio <= float(gates_cfg["ood_topology_mse_ratio_max"]),
        },
        "multi_seed_topology_mse_reduction_is_stable": {
            "threshold": f"mean ratio <= {gates_cfg['multi_seed_topology_mse_ratio_mean_max']}",
            "value": multi_ratio,
            "pass": multi_ratio <= float(gates_cfg["multi_seed_topology_mse_ratio_mean_max"]),
        },
        "lambda_sweep_finds_stronger_topology_tradeoff": {
            "threshold": "best topology ratio <= 0.5 and L2 ratio <= overall_l2_ratio_max",
            "value": [sweep_topo_ratio, sweep_l2_ratio],
            "pass": sweep_topo_ratio <= 0.5 and sweep_l2_ratio <= float(gates_cfg["overall_l2_ratio_max"]),
        },
        "robust_channel_metrics_are_finite": {
            "threshold": "all current-scale per-channel RMSE values are finite",
            "value": robust_channel_values,
            "pass": bool(np.all(np.isfinite(np.array(robust_channel_values, dtype=float)))),
        },
        "stress_topology_mse_reduction_is_stable": {
            "threshold": "stress mean topology ratio <= 0.95 and max L2 ratio <= overall_l2_ratio_max",
            "value": [stress_topo_ratio, stress_l2_ratio],
            "pass": stress_topo_ratio <= 0.95 and stress_l2_ratio <= float(gates_cfg["overall_l2_ratio_max"]),
        },
        "physical_reforward_metrics_are_finite": {
            "threshold": "all test/OOD physical re-forward residuals are finite",
            "value": physical_values,
            "pass": bool(np.all(np.isfinite(np.array(physical_values, dtype=float)))),
        },
        "physics_tikhonov_baseline_is_reported": {
            "threshold": "physics_tikhonov baseline exists on test and OOD",
            "value": ["physics_tikhonov" in test, "physics_tikhonov" in ood],
            "pass": "physics_tikhonov" in test and "physics_tikhonov" in ood,
        },
        "residual_via_detector_beats_raw_adjoint": {
            "threshold": "topology residual detector hit rate > raw hit rate and loc error < raw loc error",
            "value": [
                raw_det.get("via_hit_rate_within_2px", float("nan")),
                topo_det.get("via_hit_rate_within_2px", float("nan")),
                raw_det.get("via_loc_error_px_mean", float("nan")),
                topo_det.get("via_loc_error_px_mean", float("nan")),
            ],
            "pass": (
                topo_det.get("via_hit_rate_within_2px", -float("inf")) > raw_det.get("via_hit_rate_within_2px", float("inf"))
                and topo_det.get("via_loc_error_px_mean", float("inf")) < raw_det.get("via_loc_error_px_mean", -float("inf"))
            ),
        },
        "oracle_residual_detector_is_upper_bound": {
            "threshold": "oracle residual detector has high test hit rate",
            "value": oracle_det.get("via_hit_rate_within_2px", float("nan")),
            "pass": oracle_det.get("via_hit_rate_within_2px", 0.0) >= 0.95,
        },
        "fp_controlled_residual_detector_reduces_ood_false_positives": {
            "threshold": "DoG/strict topology residual detector has lower OOD no-via FP than the unfiltered residual detector and beats raw OOD hit rate",
            "value": [
                ood_topo_det.get("via_false_positive_rate_no_via", float("nan")),
                ood_topo_fp_det.get("via_false_positive_rate_no_via", float("nan")),
                ood_raw_det.get("via_hit_rate_within_2px", float("nan")),
                ood_topo_fp_det.get("via_hit_rate_within_2px", float("nan")),
            ],
            "pass": (
                ood_topo_fp_det.get("via_false_positive_rate_no_via", float("inf"))
                <= ood_topo_det.get("via_false_positive_rate_no_via", -float("inf"))
                and ood_topo_fp_det.get("via_hit_rate_within_2px", -float("inf"))
                > ood_raw_det.get("via_hit_rate_within_2px", float("inf"))
            ),
        },
        "finite_width_return_operator_stress_is_reported": {
            "threshold": "finite-width/return stress exists with measurable input gap > 2%",
            "value": finite_width_input_gap,
            "pass": bool(np.isfinite(finite_width_input_gap) and finite_width_input_gap > 0.02),
        },
        "finite_width_return_detail_metrics_are_finite": {
            "threshold": "finite-width/return row reports L2, topology, s1, via, leakage, and physical B metrics for all U-Net methods",
            "value": finite_width_detail_values,
            "pass": bool(np.all(np.isfinite(np.array(finite_width_detail_values, dtype=float)))),
        },
        "two_stage_refinement_is_reported_and_bounded": {
            "threshold": "two-stage refined model exists and test L2 <= overall_l2_ratio_max * topology-soft L2",
            "value": [
                "unet_topology_two_stage_refined" in test,
                refined.get("overall_rel_l2", float("nan")),
                test["unet_topology_soft_loss"]["overall_rel_l2"],
            ],
            "pass": (
                "unet_topology_two_stage_refined" in test
                and refined.get("overall_rel_l2", float("inf"))
                <= float(gates_cfg["overall_l2_ratio_max"]) * test["unet_topology_soft_loss"]["overall_rel_l2"]
            ),
        },
        "real_pypeec_operator_stress_bridge_is_reported": {
            "threshold": "exp07 real PyPEEC artifact exists, gates passed, and required cases completed",
            "value": {
                "enabled": pypeec_bridge_enabled,
                "artifact_available": pypeec_bridge.get("artifact_available", False),
                "exp07_all_gates_passed": pypeec_bridge.get("exp07_all_gates_passed", False),
                "n_cases_completed": pypeec_bridge.get("n_cases_completed", 0),
                "used_for_training": pypeec_bridge.get("used_for_training", True),
                "used_for_validation_thresholds": pypeec_bridge.get("used_for_validation_thresholds", True),
            },
            "pass": (
                (not pypeec_bridge_enabled)
                or (
                    bool(pypeec_bridge.get("artifact_available", False))
                    and bool(pypeec_bridge.get("exp07_all_gates_passed", False))
                    and int(pypeec_bridge.get("n_cases_completed", 0))
                    >= int(pypeec_bridge_cfg.get("required_cases_completed", 0))
                    and pypeec_bridge.get("used_for_training") is False
                    and pypeec_bridge.get("used_for_validation_thresholds") is False
                )
            ),
        },
        "real_pypeec_operator_stress_gap_is_material_and_bounded": {
            "threshold": "exp03-like PyPEEC shape gap is finite and between configured material/bounded limits",
            "value": pypeec_bridge_gap,
            "pass": (
                (not pypeec_bridge_enabled)
                or (
                    np.isfinite(pypeec_bridge_gap)
                    and pypeec_bridge_gap >= float(pypeec_bridge_cfg.get("min_exp03_like_shape_gap", 0.0))
                    and pypeec_bridge_gap <= float(pypeec_bridge_cfg.get("max_exp03_like_shape_gap", float("inf")))
                )
            ),
        },
        "real_pypeec_frozen_inference_is_reported": {
            "threshold": "PyPEEC mini dataset exists and frozen inference reports all three U-Net variants without leakage",
            "value": {
                "enabled": pypeec_frozen_enabled,
                "artifact_available": pypeec_frozen.get("artifact_available", False),
                "n_cases": pypeec_frozen.get("n_cases", 0),
                "used_for_training": pypeec_frozen.get("used_for_training", True),
                "used_for_validation_thresholds": pypeec_frozen.get("used_for_validation_thresholds", True),
                "used_for_calibration": pypeec_frozen.get("used_for_calibration", True),
                "methods": sorted(pypeec_frozen.get("methods", {}).keys()),
            },
            "pass": (
                (not pypeec_frozen_enabled)
                or (
                    bool(pypeec_frozen.get("artifact_available", False))
                    and int(pypeec_frozen.get("n_cases", 0)) >= int(pypeec_frozen_cfg.get("min_cases", 0))
                    and pypeec_frozen.get("used_for_training") is False
                    and pypeec_frozen.get("used_for_validation_thresholds") is False
                    and pypeec_frozen.get("used_for_calibration") is False
                    and all(
                        name in pypeec_frozen.get("methods", {})
                        for name in [
                            "unet_no_topology",
                            "unet_topology_soft_loss",
                            "unet_topology_two_stage_refined",
                        ]
                    )
                )
            ),
        },
        "real_pypeec_frozen_inference_metrics_are_finite": {
            "threshold": "all PyPEEC frozen inference core metrics are finite",
            "value": pypeec_frozen_values + pypeec_subset_values,
            "pass": (
                (not pypeec_frozen_enabled)
                or bool(np.all(np.isfinite(np.array(pypeec_frozen_values + pypeec_subset_values, dtype=float))))
            ),
        },
        "real_pypeec_frozen_inference_subsets_are_reported": {
            "threshold": "canonical, exp03-like, via, no-via, dense-via, and return-path subsets are reported",
            "value": {
                name: pypeec_frozen.get("subsets", {}).get(name, {}).get("n_cases", 0)
                for name in ["canonical", "exp03_like", "via", "no_via", "dense_via", "return_path"]
            },
            "pass": (
                (not pypeec_frozen_enabled)
                or all(
                    int(pypeec_frozen.get("subsets", {}).get(name, {}).get("n_cases", 0)) > 0
                    for name in ["canonical", "exp03_like", "via", "no_via", "dense_via", "return_path"]
                )
            ),
        },
        "real_pypeec_null_via_diagnostics_are_reported": {
            "threshold": "no-via diagnostic rows exist for every frozen U-Net variant without changing thresholds",
            "value": {
                "n_cases": pypeec_null_diag.get("n_cases", 0),
                "n_rows": len(pypeec_null_diag.get("rows", [])),
                "models": sorted(pypeec_null_diag.get("summary", {}).keys()),
                "boundary": pypeec_null_diag.get("boundary", ""),
            },
            "pass": (
                (not pypeec_frozen_enabled)
                or (
                    int(pypeec_null_diag.get("n_cases", 0)) > 0
                    and len(pypeec_null_diag.get("rows", []))
                    >= int(pypeec_null_diag.get("n_cases", 0)) * len(pypeec_required_models)
                    and all(model in pypeec_null_diag.get("summary", {}) for model in pypeec_required_models)
                    and "No PyPEEC no-via threshold" in str(pypeec_null_diag.get("boundary", ""))
                )
            ),
        },
        "real_pypeec_return_path_diagnostics_are_reported": {
            "threshold": "return-path diagnostic rows exist for every frozen U-Net variant without changing thresholds",
            "value": {
                "n_cases": pypeec_return_diag.get("n_cases", 0),
                "n_rows": len(pypeec_return_diag.get("rows", [])),
                "models": sorted(pypeec_return_diag.get("summary", {}).keys()),
                "boundary": pypeec_return_diag.get("boundary", ""),
            },
            "pass": (
                (not pypeec_frozen_enabled)
                or (
                    int(pypeec_return_diag.get("n_cases", 0)) > 0
                    and len(pypeec_return_diag.get("rows", []))
                    >= int(pypeec_return_diag.get("n_cases", 0)) * len(pypeec_required_models)
                    and all(model in pypeec_return_diag.get("summary", {}) for model in pypeec_required_models)
                    and "without changing model thresholds" in str(pypeec_return_diag.get("boundary", ""))
                )
            ),
        },
        "real_pypeec_failure_diagnostics_are_finite": {
            "threshold": "core no-via and return-path diagnostic values are finite",
            "value": pypeec_diag_values,
            "pass": (
                (not pypeec_frozen_enabled)
                or bool(np.all(np.isfinite(np.array(pypeec_diag_values, dtype=float))))
            ),
        },
        "real_pypeec_mechanism_summaries_are_reported": {
            "threshold": "no-via and return-path mechanism summaries plus no-via failure figures are present",
            "value": {
                "null_models": sorted(pypeec_null_diag.get("mechanism_summary", {}).keys()),
                "return_models": sorted(pypeec_return_diag.get("mechanism_summary", {}).keys()),
                "failure_figures": pypeec_null_diag.get("failure_figure_paths", []),
            },
            "pass": (
                (not pypeec_frozen_enabled)
                or (
                    all(model in pypeec_null_diag.get("mechanism_summary", {}) for model in pypeec_required_models)
                    and all(model in pypeec_return_diag.get("mechanism_summary", {}) for model in pypeec_required_models)
                    and len(pypeec_null_diag.get("failure_figure_paths", [])) > 0
                )
            ),
        },
        "null_via_hypothesis_gate_is_calibrated_without_pypeec": {
            "threshold": "null-via gate is selected on synthetic validation stress only; PyPEEC is not used for threshold selection",
            "value": {
                "enabled": null_gate_enabled,
                "gate_enabled": null_gate_calibration.get("enabled", False),
                "calibration_split": null_gate_calibration.get("calibration_split"),
                "used_for_pypeec_threshold_selection": null_gate_calibration.get("used_for_pypeec_threshold_selection", True),
                "used_for_pypeec_calibration": null_gate_calibration.get("used_for_pypeec_calibration", True),
                "families": [row.get("family") for row in null_gate_calibration.get("validation_family_rows", [])],
            },
            "pass": (
                (not null_gate_enabled)
                or (
                    bool(null_gate_calibration.get("enabled", False))
                    and null_gate_calibration.get("calibration_split") == "val_synthetic_null_via_stress"
                    and null_gate_calibration.get("used_for_pypeec_threshold_selection") is False
                    and null_gate_calibration.get("used_for_pypeec_calibration") is False
                    and "score_threshold" in null_gate_calibration.get("selected_params", {})
                    and {
                        "synthetic_null_via_bend_corner_stress",
                        "synthetic_null_via_return_path_stress",
                        "synthetic_null_via_operator_gap_stress",
                    }.issubset({str(row.get("family")) for row in null_gate_calibration.get("validation_family_rows", [])})
                )
            ),
        },
        "null_via_hypothesis_gate_validation_metrics_are_finite": {
            "threshold": "synthetic validation stress gate metrics are finite",
            "value": null_gate_values,
            "pass": (
                (not null_gate_enabled)
                or (
                    len(null_gate_values) > 0
                    and bool(np.all(np.isfinite(np.array(null_gate_values, dtype=float))))
                )
            ),
        },
        "real_pypeec_null_via_hypothesis_gate_is_reported": {
            "threshold": "frozen PyPEEC evaluation reports before/after null-via gate trade-offs without PyPEEC calibration",
            "value": {
                "enabled": pypeec_null_gate.get("enabled", False),
                "calibration_split": pypeec_null_gate.get("calibration_split"),
                "used_for_pypeec_threshold_selection": pypeec_null_gate.get("used_for_pypeec_threshold_selection", True),
                "used_for_pypeec_calibration": pypeec_null_gate.get("used_for_pypeec_calibration", True),
                "models": sorted(pypeec_null_gate.get("models", {}).keys()),
            },
            "pass": (
                (not (pypeec_frozen_enabled and null_gate_enabled))
                or (
                    bool(pypeec_null_gate.get("enabled", False))
                    and pypeec_null_gate.get("calibration_split") == "val_synthetic_null_via_stress"
                    and pypeec_null_gate.get("used_for_pypeec_threshold_selection") is False
                    and pypeec_null_gate.get("used_for_pypeec_calibration") is False
                    and all(model in pypeec_null_gate.get("models", {}) for model in pypeec_required_models)
                    and len(pypeec_null_gate.get("decision_rows", []))
                    >= int(pypeec_frozen.get("n_cases", 0)) * len(pypeec_required_models)
                )
            ),
        },
        "real_pypeec_null_via_hypothesis_gate_metrics_are_finite": {
            "threshold": "frozen PyPEEC null-via gate before/after metrics are finite",
            "value": pypeec_null_gate_values,
            "pass": (
                (not (pypeec_frozen_enabled and null_gate_enabled))
                or (
                    len(pypeec_null_gate_values) > 0
                    and bool(np.all(np.isfinite(np.array(pypeec_null_gate_values, dtype=float))))
                )
            ),
        },
        "real_pypeec_null_via_gate_pareto_is_reported": {
            "threshold": "frozen PyPEEC null-via gate Pareto rows include selected point and finite trade-off metrics",
            "value": {
                "n_pareto_rows": len(pypeec_null_gate.get("pareto_rows", [])),
                "selected_rows": sum(1 for row in pypeec_null_gate.get("pareto_rows", []) if row.get("selected", False)),
                "plot": pypeec_null_gate.get("pareto_plot_path"),
            },
            "pass": (
                (not (pypeec_frozen_enabled and null_gate_enabled))
                or (
                    len(pypeec_null_gate.get("pareto_rows", [])) >= 5
                    and any(row.get("selected", False) for row in pypeec_null_gate.get("pareto_rows", []))
                    and bool(pypeec_null_gate.get("pareto_plot_path"))
                )
            ),
        },
        "real_pypeec_null_via_gate_case_studies_are_reported": {
            "threshold": "before/after gate case-study figures exist for at least filtered FP or rejected true-via cases",
            "value": pypeec_null_gate.get("case_figure_paths", []),
            "pass": (
                (not (pypeec_frozen_enabled and null_gate_enabled))
                or len(pypeec_null_gate.get("case_figure_paths", [])) > 0
            ),
        },
        "real_pypeec_hypothesis_evidence_is_reported": {
            "threshold": "H1-via versus H0-artifact evidence rows exist for every frozen U-Net variant without PyPEEC calibration",
            "value": {
                "enabled": pypeec_hypothesis_evidence.get("enabled", False),
                "n_rows": len(pypeec_hypothesis_evidence.get("rows", [])),
                "models": sorted(pypeec_hypothesis_evidence.get("summary", {}).keys()),
                "used_for_pypeec_threshold_selection": pypeec_hypothesis_evidence.get("used_for_pypeec_threshold_selection", True),
            },
            "pass": (
                (not (pypeec_frozen_enabled and null_gate_enabled))
                or (
                    bool(pypeec_hypothesis_evidence.get("enabled", False))
                    and len(pypeec_hypothesis_evidence.get("rows", []))
                    >= int(pypeec_frozen.get("n_cases", 0)) * len(pypeec_required_models)
                    and all(model in pypeec_hypothesis_evidence.get("summary", {}) for model in pypeec_required_models)
                    and pypeec_hypothesis_evidence.get("used_for_pypeec_threshold_selection") is False
                    and bool(np.all(np.isfinite(np.array(pypeec_hypothesis_values, dtype=float))))
                )
            ),
        },
        "real_pypeec_heldout_split_protocol_is_reported": {
            "threshold": "future PyPEEC calibration/held-out split protocol is defined but unused by current metrics",
            "value": {
                "protocol": pypeec_heldout_protocol.get("protocol_version"),
                "n_rows": len(pypeec_heldout_protocol.get("rows", [])),
                "used_for_current_threshold_selection": pypeec_heldout_protocol.get("used_for_current_threshold_selection", True),
                "families": sorted(pypeec_heldout_protocol.get("family_summary", {}).keys()),
            },
            "pass": (
                (not pypeec_frozen_enabled)
                or (
                    len(pypeec_heldout_protocol.get("rows", [])) == int(pypeec_frozen.get("n_cases", -1))
                    and pypeec_heldout_protocol.get("used_for_current_training") is False
                    and pypeec_heldout_protocol.get("used_for_current_threshold_selection") is False
                    and pypeec_heldout_protocol.get("used_for_current_calibration") is False
                    and len(pypeec_heldout_protocol.get("family_summary", {})) >= 4
                )
            ),
        },
        "real_pypeec_return_path_hypothesis_is_reported": {
            "threshold": "return-path rows include via-like versus return-current evidence classifications",
            "value": {
                "models": sorted(pypeec_return_diag.get("hypothesis_summary", {}).keys()),
                "n_rows": len(pypeec_return_diag.get("rows", [])),
            },
            "pass": (
                (not pypeec_frozen_enabled)
                or (
                    all(model in pypeec_return_diag.get("hypothesis_summary", {}) for model in pypeec_required_models)
                    and all("hypothesis_decision" in row for row in pypeec_return_diag.get("rows", []))
                )
            ),
        },
        "real_pypeec_uncertainty_refusal_is_reported": {
            "threshold": "uncertainty/refusal diagnostics exist and are finite for every frozen U-Net variant",
            "value": {
                "enabled": pypeec_uncertainty_refusal.get("enabled", False),
                "models": sorted(pypeec_uncertainty_refusal.get("summary", {}).keys()),
            },
            "pass": (
                (not (pypeec_frozen_enabled and null_gate_enabled))
                or (
                    bool(pypeec_uncertainty_refusal.get("enabled", False))
                    and all(model in pypeec_uncertainty_refusal.get("summary", {}) for model in pypeec_required_models)
                    and len(pypeec_uncertainty_values) > 0
                    and bool(np.all(np.isfinite(np.array(pypeec_uncertainty_values, dtype=float))))
                )
            ),
        },
        "real_pypeec_generative_hypothesis_scoring_is_reported": {
            "threshold": "explicit H1(with s1) vs H0(s1=0) generative energy rows and calibration curve are reported",
            "value": {
                "enabled": pypeec_generative_hypothesis.get("enabled", False),
                "n_rows": len(pypeec_generative_hypothesis.get("rows", [])),
                "n_calibration_rows": len(pypeec_generative_hypothesis.get("calibration_rows", [])),
                "plot": pypeec_generative_hypothesis.get("calibration_plot_path"),
            },
            "pass": (
                (not (pypeec_frozen_enabled and null_gate_enabled))
                or (
                    bool(pypeec_generative_hypothesis.get("enabled", False))
                    and len(pypeec_generative_hypothesis.get("rows", []))
                    >= int(pypeec_frozen.get("n_cases", 0)) * len(pypeec_required_models)
                    and len(pypeec_generative_hypothesis.get("calibration_rows", [])) >= len(pypeec_required_models)
                    and bool(pypeec_generative_hypothesis.get("calibration_plot_path"))
                    and len(pypeec_generative_values) > 0
                    and bool(np.all(np.isfinite(np.array(pypeec_generative_values, dtype=float))))
                )
            ),
        },
        "real_pypeec_selective_risk_is_reported": {
            "threshold": "risk-coverage rows exist for every frozen U-Net variant",
            "value": {
                "enabled": pypeec_selective_risk.get("enabled", False),
                "n_rows": len(pypeec_selective_risk.get("rows", [])),
                "plot": pypeec_selective_risk.get("plot_path"),
            },
            "pass": (
                (not (pypeec_frozen_enabled and null_gate_enabled))
                or (
                    bool(pypeec_selective_risk.get("enabled", False))
                    and len(pypeec_selective_risk.get("rows", [])) >= len(pypeec_required_models) * 5
                    and bool(pypeec_selective_risk.get("plot_path"))
                    and len(pypeec_selective_values) > 0
                    and bool(np.all(np.isfinite(np.array(pypeec_selective_values, dtype=float))))
                )
            ),
        },
        "real_pypeec_return_current_generator_is_reported": {
            "threshold": "return-current-aware signal-plus-return generator diagnostic exists for return-path cases",
            "value": {
                "enabled": pypeec_return_generator.get("enabled", False),
                "mode": pypeec_return_generator.get("mode"),
                "n_cases": pypeec_return_generator.get("summary", {}).get("n_cases", 0),
            },
            "pass": (
                (not pypeec_frozen_enabled)
                or (
                    bool(pypeec_return_generator.get("enabled", False))
                    and int(pypeec_return_generator.get("summary", {}).get("n_cases", 0)) > 0
                    and pypeec_return_generator.get("used_for_model_prediction") is False
                    and len(pypeec_return_generator_values) > 0
                    and bool(np.all(np.isfinite(np.array(pypeec_return_generator_values, dtype=float))))
                )
            ),
        },
        "real_pypeec_heldout_split_evaluation_is_reported": {
            "threshold": "frozen metrics are stratified by reserved future calibration/held-out roles without using the roles for calibration",
            "value": {
                "enabled": pypeec_heldout_evaluation.get("enabled", False),
                "roles": sorted(pypeec_heldout_evaluation.get("role_summary", {}).keys()),
                "used_for_current_threshold_selection": pypeec_heldout_evaluation.get("used_for_current_threshold_selection", True),
            },
            "pass": (
                (not pypeec_frozen_enabled)
                or (
                    bool(pypeec_heldout_evaluation.get("enabled", False))
                    and {"future_calibration_candidate", "future_heldout_test"}.issubset(
                        set(pypeec_heldout_evaluation.get("role_summary", {}).keys())
                    )
                    and pypeec_heldout_evaluation.get("used_for_current_threshold_selection") is False
                    and pypeec_heldout_evaluation.get("used_for_current_calibration") is False
                    and len(pypeec_heldout_values) > 0
                    and bool(np.all(np.isfinite(np.array(pypeec_heldout_values, dtype=float))))
                )
            ),
        },
        "real_pypeec_frozen_inference_cost_is_bounded": {
            "threshold": "topology/no-topology ratios on PyPEEC mini stress remain below configured loose bounds",
            "value": [
                pypeec_frozen_summary.get("topology_mse_ratio_topology_over_no_topology", float("nan")),
                pypeec_frozen_summary.get("overall_l2_ratio_topology_over_no_topology", float("nan")),
                pypeec_frozen.get("subsets", {}).get("exp03_like", {}).get("summary", {}).get("topology_mse_ratio_topology_over_no_topology", float("nan")),
                pypeec_frozen.get("subsets", {}).get("exp03_like", {}).get("summary", {}).get("overall_l2_ratio_topology_over_no_topology", float("nan")),
            ],
            "pass": (
                (not pypeec_frozen_enabled)
                or (
                    np.isfinite(pypeec_frozen_summary.get("topology_mse_ratio_topology_over_no_topology", float("nan")))
                    and np.isfinite(pypeec_frozen_summary.get("overall_l2_ratio_topology_over_no_topology", float("nan")))
                    and np.isfinite(pypeec_frozen.get("subsets", {}).get("exp03_like", {}).get("summary", {}).get("topology_mse_ratio_topology_over_no_topology", float("nan")))
                    and np.isfinite(pypeec_frozen.get("subsets", {}).get("exp03_like", {}).get("summary", {}).get("overall_l2_ratio_topology_over_no_topology", float("nan")))
                    and pypeec_frozen_summary.get("topology_mse_ratio_topology_over_no_topology", float("inf"))
                    <= float(pypeec_frozen_cfg.get("max_topology_mse_ratio", float("inf")))
                    and pypeec_frozen_summary.get("overall_l2_ratio_topology_over_no_topology", float("inf"))
                    <= float(pypeec_frozen_cfg.get("max_overall_l2_ratio", float("inf")))
                    and pypeec_frozen.get("subsets", {}).get("exp03_like", {}).get("summary", {}).get("topology_mse_ratio_topology_over_no_topology", float("inf"))
                    <= float(pypeec_frozen_cfg.get("max_exp03_like_topology_mse_ratio", float("inf")))
                    and pypeec_frozen.get("subsets", {}).get("exp03_like", {}).get("summary", {}).get("overall_l2_ratio_topology_over_no_topology", float("inf"))
                    <= float(pypeec_frozen_cfg.get("max_exp03_like_overall_l2_ratio", float("inf")))
                )
            ),
        },
    }
    metrics["derived_ratios"] = {
        "test_topology_mse_ratio_topology_over_no_topology": topo_ratio,
        "test_overall_l2_ratio_topology_over_no_topology": l2_ratio,
        "ood_topology_mse_ratio_topology_over_no_topology": ood_topo_ratio,
    }
    metrics["acceptance_gates"] = gates
    metrics["all_acceptance_gates_passed"] = all(g["pass"] for g in gates.values())


def summarize_multi_seed(rows: list[dict[str, float]]) -> dict[str, Any]:
    keys = [
        "no_topology_l2",
        "topology_l2",
        "topology_mse_ratio",
        "overall_l2_ratio",
        "ood_topology_mse_ratio",
    ]
    out: dict[str, Any] = {"runs": rows}
    for k in keys:
        vals = np.array([r[k] for r in rows], dtype=float)
        out[f"{k}_mean"] = float(np.mean(vals))
        out[f"{k}_std"] = float(np.std(vals, ddof=0))
    return out


def write_run_report(metrics: dict[str, Any], out: Path) -> None:
    gates = "\n".join(
        f"- {name}: {'PASS' if gate['pass'] else 'FAIL'}; value={gate['value']}; threshold={gate['threshold']}"
        for name, gate in metrics["acceptance_gates"].items()
    )
    test = metrics["benchmark"]["test"]
    pypeec = metrics.get("pypeec_frozen_inference", {})
    null_summary = pypeec.get("null_via_diagnostics", {}).get("summary", {})
    return_summary = pypeec.get("return_path_diagnostics", {}).get("summary", {})
    null_gate_summary = pypeec.get("null_via_hypothesis_gate", {}).get("summary", {})
    evidence_summary = pypeec.get("null_via_hypothesis_evidence", {}).get("summary", {})
    generative_summary = pypeec.get("null_via_generative_hypothesis", {}).get("summary", {})
    selective_summary = pypeec.get("selective_risk", {}).get("summary", {})
    return_gen_summary = pypeec.get("return_current_aware_generator", {}).get("summary", {})
    refusal_summary = pypeec.get("uncertainty_refusal", {}).get("summary", {})
    report = f"""# exp04 Run Report

## Role

Full topology-aware inverse benchmark on the exp03 Biot-Savart two-layer via
dataset. This is the first benchmark that trains on `B_obs` and predicts
`J1x,J1y,J2x,J2y,s1` with U-Net-lite baselines.

## Gate Summary

Overall: {'PASS' if metrics['all_acceptance_gates_passed'] else 'FAIL'}

{gates}

## Key Test Metrics

- zero overall L2: `{test['zero']['overall_rel_l2']:.3f}`
- ridge overall L2: `{test['ridge']['overall_rel_l2']:.3f}`
- physics Tikhonov overall L2: `{test['physics_tikhonov']['overall_rel_l2']:.3f}`
- U-Net no-topology overall L2: `{test['unet_no_topology']['overall_rel_l2']:.3f}`
- U-Net topology overall L2: `{test['unet_topology_soft_loss']['overall_rel_l2']:.3f}`
- U-Net no-topology topology MSE: `{test['unet_no_topology']['topology_mse']:.3e}`
- U-Net topology topology MSE: `{test['unet_topology_soft_loss']['topology_mse']:.3e}`
- U-Net no-topology physical re-forward residual: `{test['unet_no_topology']['physical_reforward_rel_l2_to_bclean']:.3f}`
- U-Net topology physical re-forward residual: `{test['unet_topology_soft_loss']['physical_reforward_rel_l2_to_bclean']:.3f}`
- U-Net two-stage refined overall L2: `{test['unet_topology_two_stage_refined']['overall_rel_l2']:.3f}`
- U-Net two-stage refined via hit: `{test['unet_topology_two_stage_refined']['via_hit_rate_within_2px']:.3f}`
- lambda sweep best topology lambda: `{metrics['lambda_sweep_summary']['best_test_topology_lambda']}`
- lambda sweep best topology MSE ratio: `{metrics['lambda_sweep_summary']['best_test_topology_ratio']:.3f}`
- lambda sweep best L2 ratio: `{metrics['lambda_sweep_summary']['best_test_l2_ratio']:.3f}`
- multi-seed topology MSE ratio mean±std: `{metrics['multi_seed_summary']['topology_mse_ratio_mean']:.3f} ± {metrics['multi_seed_summary']['topology_mse_ratio_std']:.3f}`
- multi-seed OOD topology MSE ratio mean±std: `{metrics['multi_seed_summary']['ood_topology_mse_ratio_mean']:.3f} ± {metrics['multi_seed_summary']['ood_topology_mse_ratio_std']:.3f}`
- stress topology MSE ratio mean/max: `{metrics['stress_summary']['topology_mse_ratio_mean']:.3f} / {metrics['stress_summary']['topology_mse_ratio_max']:.3f}`
- stress L2 ratio mean/max: `{metrics['stress_summary']['overall_l2_ratio_mean']:.3f} / {metrics['stress_summary']['overall_l2_ratio_max']:.3f}`
- finite-width/return stress input gap: `{metrics['stress_benchmark']['finite_width_return']['stress_input']['input_gap_rel_l2_to_clean']:.3f}`
- real PyPEEC exp03-like shape gap: `{metrics.get('pypeec_operator_stress_bridge', {}).get('exp03_like_shape_gap_median', float('nan')):.3f}`
- real PyPEEC frozen inference topology ratio: `{metrics.get('pypeec_frozen_inference', {}).get('summary', {}).get('topology_mse_ratio_topology_over_no_topology', float('nan')):.3f}`
- real PyPEEC frozen inference L2 ratio: `{metrics.get('pypeec_frozen_inference', {}).get('summary', {}).get('overall_l2_ratio_topology_over_no_topology', float('nan')):.3f}`
- PyPEEC no-via FP rate, no-topology/topology: `{_md_value(null_summary.get('unet_no_topology', {}).get('false_positive_rate'))}` / `{_md_value(null_summary.get('unet_topology_soft_loss', {}).get('false_positive_rate'))}`
- PyPEEC return-path mean physical B residual, no-topology/topology: `{_md_value(return_summary.get('unet_no_topology', {}).get('mean_physical_b_residual_to_pypeec'))}` / `{_md_value(return_summary.get('unet_topology_soft_loss', {}).get('mean_physical_b_residual_to_pypeec'))}`
- null-via gate PyPEEC no-via FP before/after: `{_md_value(null_gate_summary.get('topology_model_no_via_fp_before'))}` / `{_md_value(null_gate_summary.get('topology_model_no_via_fp_after'))}`
- null-via gate PyPEEC via recall before/after: `{_md_value(null_gate_summary.get('topology_model_via_recall_before'))}` / `{_md_value(null_gate_summary.get('topology_model_via_recall_after'))}`
- null-via gate PyPEEC dense-via F1 before/after: `{_md_value(null_gate_summary.get('topology_model_dense_via_f1_before'))}` / `{_md_value(null_gate_summary.get('topology_model_dense_via_f1_after'))}`
- null-via gate PyPEEC physical B residual before/after: `{_md_value(null_gate_summary.get('topology_model_physical_b_pypeec_before'))}` / `{_md_value(null_gate_summary.get('topology_model_physical_b_pypeec_after'))}`
- null-via evidence high-confidence/ambiguous fractions, topology model: `{_md_value(evidence_summary.get('unet_topology_soft_loss', {}).get('high_confidence_via_fraction'))}` / `{_md_value(evidence_summary.get('unet_topology_soft_loss', {}).get('ambiguous_or_refusal_fraction'))}`
- generative H1/H0 evidence AUC / H1 recall, topology model: `{_md_value(generative_summary.get('unet_topology_soft_loss', {}).get('auc_true_via_vs_no_via'))}` / `{_md_value(generative_summary.get('unet_topology_soft_loss', {}).get('h1_recall'))}`
- selective risk at 20% / full coverage, topology model: `{_md_value(selective_summary.get('unet_topology_soft_loss', {}).get('selective_risk_at_20pct_coverage'))}` / `{_md_value(selective_summary.get('unet_topology_soft_loss', {}).get('full_coverage_risk'))}`
- return-current-aware generator mean improvement over centerline: `{_md_value(return_gen_summary.get('mean_improvement_over_centerline'))}`
- uncertainty/refusal no-via high-confidence false alarm, topology model: `{_md_value(refusal_summary.get('unet_topology_soft_loss', {}).get('no_via_high_confidence_false_alarm_rate'))}`
- via detector threshold calibration split: `{metrics['via_detection_benchmark']['calibration_split']}`
- two-stage refinement calibration split: `{metrics['two_stage_refiner']['calibration_split']}`
- robust channel metrics: see `outputs/CHANNEL_METRICS_TABLE.md`
- stress metrics: see `outputs/STRESS_METRICS_TABLE.md`
- finite-width/return stress details: see `outputs/OPERATOR_STRESS_TABLE.md`
- real PyPEEC frozen operator-stress bridge: see `outputs/PYPEEC_OPERATOR_STRESS_TABLE.md`
- real PyPEEC frozen inference stress: see `outputs/PYPEEC_FROZEN_INFERENCE_TABLE.md`
- real PyPEEC frozen inference subset stress: see `outputs/PYPEEC_FROZEN_INFERENCE_SUBSET_TABLE.md`
- real PyPEEC no-via false-positive diagnostics: see `outputs/PYPEEC_NULL_VIA_DIAGNOSTICS_TABLE.md`
- real PyPEEC no-via mechanism summary: see `outputs/PYPEEC_NULL_VIA_MECHANISM_SUMMARY.md`
- real PyPEEC no-via failure cases: see `outputs/PYPEEC_NULL_VIA_FAILURE_CASES.md`
- real PyPEEC no-via failure figures: see `outputs/figures/pypeec_null_via_failures/`
- real PyPEEC return-path diagnostics: see `outputs/PYPEEC_RETURN_PATH_DIAGNOSTICS_TABLE.md`
- real PyPEEC return-path mechanism summary: see `outputs/PYPEEC_RETURN_PATH_MECHANISM_SUMMARY.md`
- real PyPEEC return-path failure modes: see `outputs/PYPEEC_RETURN_PATH_FAILURE_MODES.md`
- synthetic null-via validation stress: see `outputs/NULL_VIA_VALIDATION_STRESS_TABLE.md`
- frozen PyPEEC null-via hypothesis gate trade-off: see `outputs/NULL_VIA_HYPOTHESIS_GATE_TABLE.md`
- frozen PyPEEC null-via gate Pareto curve: see `outputs/NULL_VIA_GATE_PARETO_TABLE.md` and `outputs/figures/null_via_gate_pareto.png`
- frozen PyPEEC null-via gate case studies: see `outputs/figures/null_via_gate_case_studies/`
- frozen PyPEEC H0/H1 null-via evidence comparison: see `outputs/NULL_VIA_HYPOTHESIS_EVIDENCE_TABLE.md`
- frozen PyPEEC generative H1/H0 scoring: see `outputs/NULL_VIA_GENERATIVE_HYPOTHESIS_TABLE.md` and `outputs/figures/null_via_generative_calibration.png`
- frozen PyPEEC selective risk-coverage: see `outputs/NULL_VIA_SELECTIVE_RISK_TABLE.md` and `outputs/figures/null_via_selective_risk.png`
- future PyPEEC calibration/held-out protocol: see `outputs/PYPEEC_HELDOUT_SPLIT_PROTOCOL.md`
- frozen PyPEEC held-out split stratification: see `outputs/PYPEEC_HELDOUT_SPLIT_EVALUATION_TABLE.md`
- return-path via-vs-return hypothesis diagnostics: see `outputs/PYPEEC_RETURN_PATH_HYPOTHESIS_TABLE.md`
- return-current-aware generator diagnostic: see `outputs/PYPEEC_RETURN_CURRENT_AWARE_GENERATOR_TABLE.md`
- null-via uncertainty/refusal diagnostics: see `outputs/NULL_VIA_UNCERTAINTY_REFUSAL_TABLE.md`
- residual via detector metrics: see `outputs/VIA_DETECTOR_TABLE.md`
- device: `{metrics['device']}`

## Boundary

This is still synthetic. The physical re-forward residual uses a rasterized
short-segment Biot-Savart operator, while the dataset fields are generated from
continuous line segments. It is therefore a real independent physics check but
not yet a finite-width/FEM/QDM validation.

The residual via detector is reported as a two-stage diagnostic. It scores via
candidates from `B_obs - F(J1,J2,s=0)` and should not be interpreted as an
additional reconstructed current map.

Via-detector thresholds and the two-stage refinement scale are selected on the
validation split and then frozen for test/OOD/stress reporting. The two-stage
baseline updates the `s1` channel after U-Net inference. It is reported to
measure whether the residual-via route is promising, not to claim a final
architecture.

The PyPEEC operator-stress bridge is imported from exp07 as a frozen read-only
artifact. It reports real-solver field gaps next to exp04 stress results, but it
is not used for training, validation threshold selection, or model calibration.

The PyPEEC frozen inference stress uses the same trained models and frozen
normalization/refinement settings on the exp07 mini PyPEEC dataset. It is a
small solver-validation stress set, not a broad PyPEEC-generated exp03
benchmark and not real QDM/FEM/FastHenry evidence.

The PyPEEC no-via and return-path diagnostic tables are failure analysis
artifacts. They document false-positive and return-current mechanisms without
selecting PyPEEC-specific thresholds, retraining models, or changing validation
calibration.

The null-via hypothesis gate is calibrated only on paired no-via/true-via
synthetic validation stress families that mimic bend/corner, strong local B-gap,
return-path, operator-gap, and layer-allocation ambiguity mechanisms. Its PyPEEC
rows are frozen before/after and Pareto evaluations and may reduce false
positives at a recall or physical-consistency cost; they should not be described
as PyPEEC-tuned thresholds.

The H0/H1 evidence comparison, uncertainty/refusal labels, return-path
hypothesis table, and PyPEEC held-out split protocol are diagnostic and protocol
artifacts. They move the task toward magnetic system identification, but they do
not change the frozen predictions or claim that no-via/return-path failures are
solved.

The generative H0/H1 score is an explicit re-forward ablation that compares the
same predicted sheet currents with and without the predicted `s1` channel. The
return-current-aware generator is an oracle return-path diagnostic using known
return-current labels. Both are evidence-building artifacts, not new trained
detectors or PyPEEC-calibrated inference models.
"""
    (out / "RUN_REPORT.md").write_text(report, encoding="utf-8")


def run(config_path: Path) -> dict[str, Any]:
    cfg = load_config(config_path)
    set_seed(int(cfg["seed"]))
    out = ROOT / "outputs"
    data_out = ROOT / "data"
    out.mkdir(exist_ok=True)
    data_out.mkdir(exist_ok=True)
    dataset_path = resolve_dataset_path(cfg)
    data = load_dataset(dataset_path)
    device = choose_device(cfg["device"])

    x_train, y_train_phys, b_train = split_arrays(data, "train")
    x_val, y_val_phys, _ = split_arrays(data, "val")
    x_test, y_test_phys, b_test = split_arrays(data, "test")
    x_ood, y_ood_phys, b_ood = split_arrays(data, "ood")
    physical_forward = build_physical_forward_kernels(data["x"], data["y"], cfg)
    physical_forward["lipschitz"] = estimate_forward_lipschitz(
        physical_forward,
        (y_train_phys.shape[1], y_train_phys.shape[2], y_train_phys.shape[3]),
    )

    x_stats = channel_stats(x_train)
    y_stats = channel_stats(y_train_phys)
    x_train_n = normalize(x_train, x_stats)
    x_val_n = normalize(x_val, x_stats)
    x_test_n = normalize(x_test, x_stats)
    x_ood_n = normalize(x_ood, x_stats)
    y_train_n = normalize(y_train_phys, y_stats)
    y_val_n = normalize(y_val_phys, y_stats)

    ridge_alpha, ridge_xmean, ridge_shape = fit_ridge_dual(x_train_n, y_train_phys, float(cfg["ridge"]["lambda"]))
    forward_proxy = fit_forward_proxy(y_train_phys, b_train, float(cfg["ridge"]["lambda"]))

    set_seed(int(cfg["seed"]))
    model_no, hist_no = train_unet(x_train_n, y_train_n, x_val_n, y_val_n, y_stats, cfg, device, topology_lambda=0.0)
    set_seed(int(cfg["seed"]))
    model_topo, hist_topo = train_unet(x_train_n, y_train_n, x_val_n, y_val_n, y_stats, cfg, device, topology_lambda=float(cfg["training"]["topology_lambda"]))

    pred_val_no_for_calibration = denormalize(
        predict_model(model_no, x_val_n, device, int(cfg["training"]["batch_size"])),
        y_stats,
    )
    pred_val_topo_for_calibration = denormalize(
        predict_model(model_topo, x_val_n, device, int(cfg["training"]["batch_size"])),
        y_stats,
    )
    two_stage_refiner = calibrate_two_stage_refiner(
        pred_val_topo_for_calibration,
        x_val,
        y_val_phys,
        physical_forward,
        cfg.get("two_stage_refinement", {}),
        calibration_split="val",
    )
    pred_val_refined_for_calibration = apply_two_stage_refinement(
        pred_val_topo_for_calibration,
        x_val,
        physical_forward,
        two_stage_refiner,
    )
    detector_calibration_preds: dict[str, np.ndarray] = {
        "unet_no_topology": pred_val_no_for_calibration,
        "unet_topology_soft_loss": pred_val_topo_for_calibration,
        "unet_topology_two_stage_refined": pred_val_refined_for_calibration,
    }
    detector_split_preds: dict[str, dict[str, np.ndarray]] = {}

    split_data = {
        "val": (x_val_n, x_val, y_val_phys, split_arrays(data, "val")[2]),
        "test": (x_test_n, x_test, y_test_phys, b_test),
        "ood": (x_ood_n, x_ood, y_ood_phys, b_ood),
    }
    benchmark: dict[str, dict[str, dict[str, Any]]] = {}
    saved_preds: dict[str, np.ndarray] = {}
    for split_name, (x_split_n, x_split_raw, y_split, b_split) in split_data.items():
        pred_zero = np.zeros_like(y_split)
        pred_ridge = apply_ridge_dual(x_split_n, x_train_n, ridge_alpha, ridge_xmean, ridge_shape)
        pred_ridge_proj = posthoc_topology_projection(pred_ridge)
        pred_phys = physics_tikhonov_inverse(x_split_raw, physical_forward, cfg)
        pred_phys_proj = posthoc_topology_projection(pred_phys)
        pred_no_n = predict_model(model_no, x_split_n, device, int(cfg["training"]["batch_size"]))
        pred_topo_n = predict_model(model_topo, x_split_n, device, int(cfg["training"]["batch_size"]))
        pred_no = denormalize(pred_no_n, y_stats)
        pred_topo = denormalize(pred_topo_n, y_stats)
        pred_topo_proj = posthoc_topology_projection(pred_topo)
        pred_topo_refined = apply_two_stage_refinement(pred_topo, x_split_raw, physical_forward, two_stage_refiner)
        preds = {
            "zero": pred_zero,
            "ridge": pred_ridge,
            "ridge_posthoc_topology": pred_ridge_proj,
            "physics_tikhonov": pred_phys,
            "physics_tikhonov_posthoc_topology": pred_phys_proj,
            "unet_no_topology": pred_no,
            "unet_topology_soft_loss": pred_topo,
            "unet_topology_two_stage_refined": pred_topo_refined,
            "unet_topology_posthoc": pred_topo_proj,
        }
        benchmark[split_name] = {
            name: evaluate_method(pred, y_split, b_split, forward_proxy, y_train_phys)
            for name, pred in preds.items()
        }
        attach_physical_reforward_metrics(benchmark[split_name], preds, b_split, x_split_raw, physical_forward)
        if split_name == "test":
            saved_preds = preds
        if split_name in {"test", "ood"}:
            detector_split_preds[split_name] = {
                "unet_no_topology": pred_no,
                "unet_topology_soft_loss": pred_topo,
                "unet_topology_two_stage_refined": pred_topo_refined,
            }

    stress_benchmark: dict[str, dict[str, dict[str, Any]]] = {}
    stress_inputs: dict[str, dict[str, Any]] = {
        name: {"B": arr, "input_gap_rel_l2_to_clean": rel_l2(arr, b_test), "model": "sensor-like input perturbation"}
        for name, arr in make_stress_inputs(x_test, cfg, int(cfg["seed"]) + 17).items()
    }
    stress_inputs.update(make_operator_stress_inputs(y_test_phys, b_test, data["x"], data["y"], cfg))
    for case, stress_info in stress_inputs.items():
        x_stress = stress_info["B"]
        x_stress_n = normalize(x_stress, x_stats)
        pred_no = denormalize(
            predict_model(model_no, x_stress_n, device, int(cfg["training"]["batch_size"])),
            y_stats,
        )
        pred_topo = denormalize(
            predict_model(model_topo, x_stress_n, device, int(cfg["training"]["batch_size"])),
            y_stats,
        )
        pred_topo_refined = apply_two_stage_refinement(pred_topo, x_stress, physical_forward, two_stage_refiner)
        stress_benchmark[case] = {
            "unet_no_topology": evaluate_method(pred_no, y_test_phys, b_test, forward_proxy, y_train_phys),
            "unet_topology_soft_loss": evaluate_method(pred_topo, y_test_phys, b_test, forward_proxy, y_train_phys),
            "unet_topology_two_stage_refined": evaluate_method(pred_topo_refined, y_test_phys, b_test, forward_proxy, y_train_phys),
        }
        attach_physical_reforward_metrics(
            stress_benchmark[case],
            {
                "unet_no_topology": pred_no,
                "unet_topology_soft_loss": pred_topo,
                "unet_topology_two_stage_refined": pred_topo_refined,
            },
            b_test,
            x_stress,
            physical_forward,
        )
        stress_benchmark[case]["stress_input"] = {
            key: (float(value) if isinstance(value, (np.floating, float)) else value)
            for key, value in stress_info.items()
            if key != "B"
        }
    stress_summary = summarize_stress_benchmark(stress_benchmark)

    analysis_cfg = cfg.get("analysis", {})
    lambda_sweep = []
    for lam in analysis_cfg.get("lambda_sweep", []):
        set_seed(int(cfg["seed"]))
        model_lam, _ = train_unet(
            x_train_n,
            y_train_n,
            x_val_n,
            y_val_n,
            y_stats,
            cfg,
            device,
            topology_lambda=float(lam),
            epochs_override=int(analysis_cfg.get("lambda_sweep_epochs", cfg["training"]["epochs"])),
        )
        pred_test = denormalize(
            predict_model(model_lam, x_test_n, device, int(cfg["training"]["batch_size"])),
            y_stats,
        )
        pred_ood = denormalize(
            predict_model(model_lam, x_ood_n, device, int(cfg["training"]["batch_size"])),
            y_stats,
        )
        lambda_sweep.append(
            {
                "lambda": float(lam),
                "test": evaluate_method(pred_test, y_test_phys, b_test, forward_proxy, y_train_phys),
                "ood": evaluate_method(pred_ood, y_ood_phys, b_ood, forward_proxy, y_train_phys),
            }
        )
    lambda0 = next((r for r in lambda_sweep if abs(r["lambda"]) < 1e-12), None)
    if lambda0 is None and lambda_sweep:
        lambda0 = lambda_sweep[0]
    if lambda0 is not None:
        best_topo = min(lambda_sweep, key=lambda r: r["test"]["topology_mse"])
        lambda_sweep_summary = {
            "reference_lambda": float(lambda0["lambda"]),
            "best_test_topology_lambda": float(best_topo["lambda"]),
            "best_test_topology_ratio": float(best_topo["test"]["topology_mse"] / (lambda0["test"]["topology_mse"] + 1e-30)),
            "best_test_l2_ratio": float(best_topo["test"]["overall_rel_l2"] / (lambda0["test"]["overall_rel_l2"] + 1e-30)),
        }
    else:
        lambda_sweep_summary = {}

    multi_seed_rows = []
    for seed in analysis_cfg.get("multi_seed", []):
        set_seed(int(seed))
        model_seed_no, _ = train_unet(
            x_train_n,
            y_train_n,
            x_val_n,
            y_val_n,
            y_stats,
            cfg,
            device,
            topology_lambda=0.0,
            epochs_override=int(analysis_cfg.get("multi_seed_epochs", cfg["training"]["epochs"])),
        )
        set_seed(int(seed))
        model_seed_topo, _ = train_unet(
            x_train_n,
            y_train_n,
            x_val_n,
            y_val_n,
            y_stats,
            cfg,
            device,
            topology_lambda=float(cfg["training"]["topology_lambda"]),
            epochs_override=int(analysis_cfg.get("multi_seed_epochs", cfg["training"]["epochs"])),
        )
        pred_no_test = denormalize(predict_model(model_seed_no, x_test_n, device, int(cfg["training"]["batch_size"])), y_stats)
        pred_topo_test = denormalize(predict_model(model_seed_topo, x_test_n, device, int(cfg["training"]["batch_size"])), y_stats)
        pred_no_ood = denormalize(predict_model(model_seed_no, x_ood_n, device, int(cfg["training"]["batch_size"])), y_stats)
        pred_topo_ood = denormalize(predict_model(model_seed_topo, x_ood_n, device, int(cfg["training"]["batch_size"])), y_stats)
        m_no = evaluate_method(pred_no_test, y_test_phys, b_test, forward_proxy, y_train_phys)
        m_topo = evaluate_method(pred_topo_test, y_test_phys, b_test, forward_proxy, y_train_phys)
        m_no_ood = evaluate_method(pred_no_ood, y_ood_phys, b_ood, forward_proxy, y_train_phys)
        m_topo_ood = evaluate_method(pred_topo_ood, y_ood_phys, b_ood, forward_proxy, y_train_phys)
        multi_seed_rows.append(
            {
                "seed": int(seed),
                "no_topology_l2": m_no["overall_rel_l2"],
                "topology_l2": m_topo["overall_rel_l2"],
                "topology_mse_ratio": m_topo["topology_mse"] / (m_no["topology_mse"] + 1e-30),
                "overall_l2_ratio": m_topo["overall_rel_l2"] / (m_no["overall_rel_l2"] + 1e-30),
                "ood_topology_mse_ratio": m_topo_ood["topology_mse"] / (m_no_ood["topology_mse"] + 1e-30),
            }
        )
    multi_seed_summary = summarize_multi_seed(multi_seed_rows) if multi_seed_rows else {}

    via_detection_benchmark = build_via_detection_benchmark(
        y_val_phys,
        x_val,
        detector_calibration_preds,
        {"test": y_test_phys, "ood": y_ood_phys},
        {"test": x_test, "ood": x_ood},
        detector_split_preds,
        physical_forward,
        cfg.get("via_detector", {}),
    )
    null_via_hypothesis_gate = calibrate_null_via_hypothesis_gate(
        cfg,
        model_topo,
        x_stats,
        y_stats,
        device,
        int(cfg["training"]["batch_size"]),
        y_val_phys,
        x_val,
        data["x"],
        data["y"],
        physical_forward,
        two_stage_refiner,
    )
    pypeec_frozen_inference = evaluate_pypeec_frozen_inference(
        cfg,
        model_no,
        model_topo,
        x_stats,
        y_stats,
        device,
        int(cfg["training"]["batch_size"]),
        two_stage_refiner,
        out,
        null_via_hypothesis_gate,
    )

    split_counts = {name: int(np.sum(data["split"] == name)) for name in ["train", "val", "test", "ood"]}
    metrics = {
        "experiment": "exp04-topology-aware-inverse-benchmark",
        "dataset_path": str(dataset_path),
        "device": str(device),
        "torch_version": torch.__version__,
        "cuda_available": bool(torch.cuda.is_available()),
        "cuda_device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "config": cfg,
        "split_counts": split_counts,
        "benchmark": benchmark,
        "history": {
            "unet_no_topology": hist_no,
            "unet_topology_soft_loss": hist_topo,
        },
        "lambda_sweep": lambda_sweep,
        "lambda_sweep_summary": lambda_sweep_summary,
        "multi_seed_summary": multi_seed_summary,
        "stress_benchmark": stress_benchmark,
        "stress_summary": stress_summary,
        "pypeec_operator_stress_bridge": load_pypeec_operator_stress_bridge(cfg),
        "pypeec_frozen_inference": pypeec_frozen_inference,
        "null_via_hypothesis_gate": null_via_hypothesis_gate,
        "via_detection_benchmark": via_detection_benchmark,
        "two_stage_refiner": two_stage_refiner,
        "notes": {
            "forward_residual": "field_residual_proxy_rel_l2 uses a fitted linear forward proxy from train truth maps to B_clean",
            "truth": "exp03 truth maps are raster labels; topology is evaluated as a consistency metric, not an exact discretization proof",
            "via_detector": "residual via detector is a candidate-localization diagnostic, not a replacement for the predicted s1 map",
            "operator_stress": "finite_width_return stress is generated by a finite-width/weak-return surrogate from truth maps; labels remain centerline truth",
            "pypeec_operator_stress_bridge": "exp07 real PyPEEC gaps are reported as a frozen read-only operator-stress bridge; they are not used for training or threshold calibration",
            "pypeec_frozen_inference": "exp07 real PyPEEC fields are used only for frozen inference with already trained/calibrated exp04 artifacts; no PyPEEC sample is used for training, threshold selection, or calibration",
            "calibration_boundary": "via detector thresholds and two-stage refinement are calibrated on validation data and frozen before test/OOD/stress reporting",
            "two_stage_refinement": "two-stage residual-via refinement is validation-calibrated and reported as a baseline, not as the final architecture",
            "null_via_hypothesis_gate": "null-via hypothesis gate parameters are selected on synthetic validation stress only, then frozen before PyPEEC evaluation",
        },
    }
    pareto_plot_path = plot_null_via_gate_pareto(metrics, out)
    if pareto_plot_path:
        metrics["pypeec_frozen_inference"]["null_via_hypothesis_gate"]["pareto_plot_path"] = pareto_plot_path
    gen_calibration_plot = plot_null_via_generative_calibration(metrics, out)
    if gen_calibration_plot:
        metrics["pypeec_frozen_inference"]["null_via_generative_hypothesis"]["calibration_plot_path"] = gen_calibration_plot
    selective_risk_plot = plot_null_via_selective_risk(metrics, out)
    if selective_risk_plot:
        metrics["pypeec_frozen_inference"]["selective_risk"]["plot_path"] = selective_risk_plot
    add_acceptance_gates(metrics, cfg)
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2, allow_nan=False), encoding="utf-8")
    write_run_report(metrics, out)
    plot_training_curves(hist_no, hist_topo, out)
    plot_prediction_comparison(x_test, y_test_phys, saved_preds, out)
    plot_metric_bars(metrics, out)
    plot_lambda_pareto(metrics, out)
    write_metrics_table(metrics, out)
    write_channel_metrics_table(metrics, out)
    write_stress_metrics_table(metrics, out)
    write_operator_stress_table(metrics, out)
    write_pypeec_operator_stress_table(metrics, out)
    write_pypeec_frozen_inference_table(metrics, out)
    write_pypeec_frozen_inference_subset_table(metrics, out)
    write_pypeec_null_via_diagnostics_table(metrics, out)
    write_pypeec_null_via_mechanism_summary(metrics, out)
    write_pypeec_null_via_failure_cases(metrics, out)
    write_pypeec_return_path_diagnostics_table(metrics, out)
    write_pypeec_return_path_mechanism_summary(metrics, out)
    write_pypeec_return_path_failure_modes(metrics, out)
    write_null_via_validation_stress_table(metrics, out)
    write_null_via_hypothesis_gate_table(metrics, out)
    write_null_via_gate_pareto_table(metrics, out)
    write_null_via_hypothesis_evidence_table(metrics, out)
    write_null_via_generative_hypothesis_table(metrics, out)
    write_null_via_selective_risk_table(metrics, out)
    write_pypeec_heldout_split_protocol(metrics, out)
    write_pypeec_heldout_split_evaluation_table(metrics, out)
    write_pypeec_return_path_hypothesis_table(metrics, out)
    write_pypeec_return_current_aware_generator_table(metrics, out)
    write_null_via_uncertainty_refusal_table(metrics, out)
    write_via_detector_table(metrics, out)
    np.savez_compressed(
        out / "predictions_test.npz",
        truth=y_test_phys,
        B_obs=x_test,
        **{f"pred_{k}": v for k, v in saved_preds.items()},
    )
    print(json.dumps({
        "all_acceptance_gates_passed": metrics["all_acceptance_gates_passed"],
        "device": metrics["device"],
        "test_l2_no_topology": benchmark["test"]["unet_no_topology"]["overall_rel_l2"],
        "test_l2_topology": benchmark["test"]["unet_topology_soft_loss"]["overall_rel_l2"],
        "test_topology_ratio": metrics["derived_ratios"]["test_topology_mse_ratio_topology_over_no_topology"],
    }, indent=2))
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "default.json")
    args = parser.parse_args()
    run(args.config)


if __name__ == "__main__":
    main()
