"""Run all Stage-1 Biot-Savart forward sanity checks.

This script creates the required output figures and metrics JSON under outputs/.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

# Allow running as `python src/experiments/run_all.py` from project root.
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from forward.grid import make_xy_grid
from forward.segments import (
    b_field_from_segments,
    make_straight_wire,
    make_rect_loop,
    make_vertical_via,
)
from forward.analytic import infinite_wire_x_field
from experiments.plotting import component_heatmaps, line_plot, ensure_dir


def rel_l2(a: np.ndarray, b: np.ndarray, eps: float = 1e-30) -> float:
    return float(np.linalg.norm(a - b) / (np.linalg.norm(b) + eps))


def add_acceptance_gates(metrics: dict[str, object]) -> None:
    """Attach explicit pass/fail gates to make the sanity check auditable."""
    gates = {
        "finite_wire_matches_infinite_reference": {
            "threshold": "relative_l2 < 2e-3",
            "value": metrics["single_wire"]["infinite_wire_rel_l2_error_central_mask"],
            "pass": metrics["single_wire"]["infinite_wire_rel_l2_error_central_mask"] < 2e-3,
        },
        "current_reversal_is_antisymmetric": {
            "threshold": "max_abs_ratio < 1e-12",
            "value": metrics["single_wire"]["sign_reversal_max_abs_ratio"],
            "pass": metrics["single_wire"]["sign_reversal_max_abs_ratio"] < 1e-12,
        },
        "rect_loop_superposition_is_exact": {
            "threshold": "relative_l2 < 1e-12",
            "value": metrics["rect_loop"]["superposition_rel_l2_error"],
            "pass": metrics["rect_loop"]["superposition_rel_l2_error"] < 1e-12,
        },
        "vertical_via_has_no_bz": {
            "threshold": "Bz/Bxy < 1e-10",
            "value": metrics["single_via"]["Bz_over_Bxy_max_ratio"],
            "pass": metrics["single_via"]["Bz_over_Bxy_max_ratio"] < 1e-10,
        },
        "standoff_reduces_field_strength": {
            "threshold": "max |B| strictly decreases with h",
            "value": metrics["standoff_scan"]["max_abs_B_monotonic_decreasing"],
            "pass": bool(metrics["standoff_scan"]["max_abs_B_monotonic_decreasing"]),
        },
    }
    metrics["acceptance_gates"] = gates
    metrics["all_acceptance_gates_passed"] = all(g["pass"] for g in gates.values())


def write_run_report(out: Path, metrics: dict[str, object]) -> None:
    gates = metrics["acceptance_gates"]
    gate_lines = "\n".join(
        f"- {name}: {'PASS' if gate['pass'] else 'FAIL'}; value={gate['value']}; threshold={gate['threshold']}"
        for name, gate in gates.items()
    )
    report = f"""# exp01 Run Report

## Role

MVP-0 forward-operator sanity check. This experiment verifies signs, units,
linearity, analytic consistency, via field direction, and standoff scaling before
any inverse model or synthetic training data is trusted.

## Gate Summary

Overall: {'PASS' if metrics['all_acceptance_gates_passed'] else 'FAIL'}

{gate_lines}

## Key Metrics

- finite wire vs infinite-wire central relative L2: `{metrics['single_wire']['infinite_wire_rel_l2_error_central_mask']:.3e}`
- current reversal max-abs ratio: `{metrics['single_wire']['sign_reversal_max_abs_ratio']:.3e}`
- loop superposition relative L2: `{metrics['rect_loop']['superposition_rel_l2_error']:.3e}`
- via Bz/Bxy max ratio: `{metrics['single_via']['Bz_over_Bxy_max_ratio']:.3e}`

## Boundary

This is a free-space, centerline-current sanity test. It intentionally does not
claim finite-width, ground-plane, QDM, FEM, or multilayer inverse validity.
"""
    (out / "RUN_REPORT.md").write_text(report, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="outputs", help="output directory")
    parser.add_argument("--nx", type=int, default=161)
    parser.add_argument("--ny", type=int, default=161)
    args = parser.parse_args()

    out = ensure_dir(args.out)

    # Common grid: 2 mm FOV, source near z=0, measurement above source.
    fov = 2.0e-3
    h = 100.0e-6
    grid = make_xy_grid(fov_x=fov, fov_y=fov, nx=args.nx, ny=args.ny, z=h)
    I = 1.0e-3  # 1 mA

    metrics: dict[str, object] = {
        "units": {"length": "m", "current": "A", "magnetic_field": "T"},
        "grid": {"fov_m": fov, "nx": args.nx, "ny": args.ny, "z_m": h, "dx_m": grid.dx, "dy_m": grid.dy},
        "current_A": I,
    }

    # 1. Long straight wire along x.
    wire_len = 20.0e-3
    wire = make_straight_wire(length=wire_len, current=I, axis="x")
    B_wire = b_field_from_segments(grid.points, wire)
    component_heatmaps(grid.x, grid.y, B_wire, "Single long wire along +x, I=1 mA, h=100 µm", out / "01_single_wire_Bxyz.png")

    # Analytic infinite-wire comparison in central region away from finite ends.
    B_inf = infinite_wire_x_field(grid.points, current=I)
    # Mask out points too close to wire projection and keep central zone.
    mask = (np.abs(grid.y) > 40e-6) & (np.abs(grid.x) < 0.4e-3)
    wire_rel_err = rel_l2(B_wire[mask], B_inf[mask])
    sign_B = b_field_from_segments(grid.points, make_straight_wire(length=wire_len, current=-I, axis="x"))
    sign_symmetry = float(np.max(np.abs(B_wire + sign_B)) / (np.max(np.abs(B_wire)) + 1e-30))
    metrics["single_wire"] = {
        "finite_length_m": wire_len,
        "infinite_wire_rel_l2_error_central_mask": wire_rel_err,
        "sign_reversal_max_abs_ratio": sign_symmetry,
    }

    # Center line comparison for By and Bz.
    mid = args.ny // 2
    xs_mm = grid.x[mid, :] * 1e3
    # Use a slightly off-center y row to avoid y=0 singularity-like large-gradient comparison for Bz.
    row = args.ny // 2 + 12
    line_plot(
        xs_mm,
        [B_wire[row, :, 1] * 1e6, B_inf[row, :, 1] * 1e6, B_wire[row, :, 2] * 1e6, B_inf[row, :, 2] * 1e6],
        ["finite By", "infinite By", "finite Bz", "infinite Bz"],
        "Finite long wire vs infinite-wire reference",
        "x [mm]",
        "B [µT]",
        out / "02_wire_vs_infinite_reference.png",
    )

    # 2. Rectangular loop.
    loop = make_rect_loop(width=0.9e-3, height=0.6e-3, current=I, z=0.0)
    B_loop = b_field_from_segments(grid.points, loop)
    component_heatmaps(grid.x, grid.y, B_loop, "Rectangular loop, I=1 mA, h=100 µm", out / "03_rect_loop_Bxyz.png")
    # Superposition check: sum of segments individually equals multi-segment call.
    B_loop_manual = sum((b_field_from_segments(grid.points, [seg]) for seg in loop), start=np.zeros_like(grid.points))
    metrics["rect_loop"] = {
        "width_m": 0.9e-3,
        "height_m": 0.6e-3,
        "superposition_rel_l2_error": rel_l2(B_loop, B_loop_manual),
        "max_abs_B_T": float(np.max(np.abs(B_loop))),
    }

    # 3. Single vertical via.
    via = make_vertical_via(z0=-50e-6, z1=50e-6, current=I, xy=(0.0, 0.0))
    B_via = b_field_from_segments(grid.points, via)
    component_heatmaps(grid.x, grid.y, B_via, "Single vertical via, I=1 mA, z=-50..50 µm, h=100 µm", out / "04_single_via_Bxyz.png")
    via_Bxy = np.sqrt(B_via[..., 0] ** 2 + B_via[..., 1] ** 2)
    via_Bz = np.abs(B_via[..., 2])
    # Avoid exact center where finite segment line is below measurement plane; no singular, but use robust ratio.
    metrics["single_via"] = {
        "z0_m": -50e-6,
        "z1_m": 50e-6,
        "max_abs_Bxy_T": float(np.max(via_Bxy)),
        "max_abs_Bz_T": float(np.max(via_Bz)),
        "Bz_over_Bxy_max_ratio": float(np.max(via_Bz) / (np.max(via_Bxy) + 1e-30)),
    }

    # 4. Standoff scan.
    hs = np.array([10e-6, 25e-6, 50e-6, 100e-6, 250e-6, 500e-6])
    maxB = []
    meanB = []
    for hh in hs:
        g = make_xy_grid(fov_x=fov, fov_y=fov, nx=args.nx, ny=args.ny, z=hh)
        B = b_field_from_segments(g.points, wire)
        mag = np.linalg.norm(B, axis=-1)
        maxB.append(float(np.max(mag)))
        meanB.append(float(np.mean(mag)))
    maxB = np.array(maxB)
    meanB = np.array(meanB)
    line_plot(
        hs * 1e6,
        [maxB * 1e6, meanB * 1e6],
        ["max |B|", "mean |B|"],
        "Standoff scan for long straight wire",
        "standoff h [µm]",
        "B magnitude [µT]",
        out / "05_standoff_scan.png",
    )
    metrics["standoff_scan"] = {
        "h_m": hs.tolist(),
        "max_abs_B_T": maxB.tolist(),
        "mean_abs_B_T": meanB.tolist(),
        "max_abs_B_monotonic_decreasing": bool(np.all(np.diff(maxB) < 0)),
    }

    # Save representative arrays for reproducibility.
    np.savez_compressed(
        out / "fields_stage1_examples.npz",
        x=grid.x,
        y=grid.y,
        z=grid.z,
        B_wire=B_wire,
        B_loop=B_loop,
        B_via=B_via,
    )

    add_acceptance_gates(metrics)
    write_run_report(out, metrics)

    with open(out / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    print(f"\nSaved outputs to: {out.resolve()}")


if __name__ == "__main__":
    main()
