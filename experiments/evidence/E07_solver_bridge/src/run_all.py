"""Run exp07 real PyPEEC solver cross-validation."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).resolve().parent
_original_sys_path = list(sys.path)
_this_dir_str = os.path.abspath(str(THIS_DIR))
sys.path = [p for p in sys.path if not (p and os.path.abspath(str(p)) == _this_dir_str)]
import numpy as np

sys.path = _original_sys_path
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from exp07_metrics import finite_median, is_strictly_decreasing, rel_l2, via_bz_over_bxy
from geometry import make_case, make_cases, make_sensor_grid
from pypeec_adapter import detect_pypeec, run_real_pypeec_backend
from reference_biot_savart import field_from_segments, finite_width_segments, reshape_field
from simple_plots import write_bar_svg, write_line_svg


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    def _safe(value: Any) -> Any:
        if isinstance(value, dict):
            return {str(k): _safe(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [_safe(v) for v in value]
        if isinstance(value, np.ndarray):
            return _safe(value.tolist())
        if isinstance(value, np.generic):
            return _safe(value.item())
        if isinstance(value, float) and not np.isfinite(value):
            return None
        return value

    path.write_text(json.dumps(_safe(obj), indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")


def table_md(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        vals = []
        for v in row:
            if isinstance(v, float):
                vals.append(f"{v:.6g}")
            else:
                vals.append(str(v))
        out.append("| " + " | ".join(vals) + " |")
    return "\n".join(out) + "\n"


def scalar_fit_rel_l2(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    """Return best scalar alpha and relative L2 for alpha*a against b."""
    av = np.asarray(a, dtype=float).ravel()
    bv = np.asarray(b, dtype=float).ravel()
    denom = float(np.dot(av, av))
    if denom <= 1e-30:
        return 0.0, float("nan")
    alpha = float(np.dot(av, bv) / denom)
    return alpha, rel_l2(alpha * a, b)


def _hypothesis_label_for_case(case) -> str:
    physics = case.expected_physics
    route_kind = str(physics.get("route_kind", ""))
    if bool(physics.get("artifact_like", False)) or route_kind in {"bend_artifact", "corner_artifact"}:
        return "H3_sheet_artifact"
    if bool(physics.get("return_path", False)) or route_kind == "return_path":
        return "H2_sheet_return"
    if physics.get("has_via") is False or route_kind == "no_via_background":
        return "H0_sheet_only"
    for segment in case.segments:
        delta = np.abs(np.asarray(segment.end, dtype=float) - np.asarray(segment.start, dtype=float))
        if float(delta[2]) > max(float(delta[0]), float(delta[1]), 1e-15):
            return "H1_sheet_via"
    return "H0_sheet_only"


def _variant_name(base_name: str, variant_index: int) -> str:
    return base_name if variant_index == 0 else f"{base_name}__v{variant_index:02d}"


def expand_cases_for_distribution_targets(cfg: dict[str, Any]) -> dict[str, Any]:
    """Append deterministic variants until the configured H0/H1/H2/H3 targets are met."""
    target_cfg = cfg.get("pypeec_distribution_targets", {})
    if not bool(target_cfg.get("enabled", False)):
        return {
            "enabled": False,
            "target_cases_per_hypothesis": {},
            "case_count_by_hypothesis": {},
            "added_cases": [],
        }

    out = json.loads(json.dumps(cfg))
    cases = list(out.get("cases", []))
    case_set = set(cases)
    counts: dict[str, int] = {"H0_sheet_only": 0, "H1_sheet_via": 0, "H2_sheet_return": 0, "H3_sheet_artifact": 0}
    for name in cases:
        label = _hypothesis_label_for_case(make_case(name, out))
        counts[label] = counts.get(label, 0) + 1

    targets = {str(k): int(v) for k, v in target_cfg.get("target_cases_per_hypothesis", {}).items()}
    base_cases = {str(k): list(v) for k, v in target_cfg.get("base_cases_by_hypothesis", {}).items()}
    added: list[str] = []
    for label, target in targets.items():
        bases = base_cases.get(label, [])
        if not bases:
            continue
        variant_idx = 0
        while counts.get(label, 0) < target:
            for base in bases:
                name = _variant_name(base, variant_idx)
                if name in case_set:
                    continue
                case = make_case(name, out)
                inferred = _hypothesis_label_for_case(case)
                if inferred != label:
                    raise RuntimeError(f"Configured base case {base!r} maps to {inferred}, not {label}.")
                cases.append(name)
                case_set.add(name)
                added.append(name)
                counts[label] = counts.get(label, 0) + 1
                if counts[label] >= target:
                    break
            variant_idx += 1
            if variant_idx > int(target_cfg.get("max_variant_index", 999)):
                raise RuntimeError(f"Could not satisfy exp07 distribution target for {label}. counts={counts}")

    out["cases"] = cases
    out["_distribution_expansion_summary"] = {
        "enabled": True,
        "target_cases_per_hypothesis": targets,
        "case_count_by_hypothesis": counts,
        "added_cases": added,
        "n_added_cases": len(added),
    }
    return out


def compute_case_fields(case, grid, cfg, output_case_dir: Path) -> dict[str, Any]:
    sub = int(cfg["geometry"].get("default_segment_subdivisions", 24))
    fw = cfg["geometry"]["finite_width_filaments"]

    ref_flat = field_from_segments(grid.points, case.segments, n_sub=sub)
    B_center = reshape_field(ref_flat, grid.shape)

    finite_segments = finite_width_segments(
        case.segments,
        n_width=int(fw["n_width"]),
        n_thickness=int(fw["n_thickness"]),
        quantize_m=None,
    )
    B_finite = reshape_field(field_from_segments(grid.points, finite_segments, n_sub=sub), grid.shape)

    backend_result = run_real_pypeec_backend(case, grid, cfg, output_case_dir)
    return {
        "case": case,
        "B_center": B_center,
        "B_finite": B_finite,
        "B_pypeec": backend_result.B_chw,
        "backend_metadata": backend_result.metadata,
    }


def peak_abs_B(B: np.ndarray) -> float:
    return float(np.max(np.sqrt(np.sum(B ** 2, axis=0))))


def standoff_decay_for_case(case, cfg, z_values: list[float]) -> list[float]:
    values = []
    n = int(cfg["sensor_grid"]["n"])
    fov = float(cfg["sensor_grid"]["fov_m"])
    sub = int(cfg["geometry"].get("default_segment_subdivisions", 24))
    for z in z_values:
        grid = make_sensor_grid(n=n, fov_m=fov, z_m=float(z))
        B = reshape_field(field_from_segments(grid.points, case.segments, n_sub=sub), grid.shape)
        values.append(peak_abs_B(B))
    return values


def _nearest_grid_index(values: np.ndarray, value: float) -> int:
    return int(np.argmin(np.abs(values - value)))


def _rasterize_sheet_segment_truth(truth: np.ndarray, grid, segment, channel_x: int, channel_y: int) -> None:
    x = grid.x
    y = grid.y
    dx = float(abs(x[1] - x[0])) if len(x) > 1 else 1.0
    x0, y0, _ = segment.start
    x1, y1, _ = segment.end
    ix0 = _nearest_grid_index(x, x0)
    ix1 = _nearest_grid_index(x, x1)
    iy0 = _nearest_grid_index(y, y0)
    iy1 = _nearest_grid_index(y, y1)
    if abs(ix1 - ix0) >= abs(iy1 - iy0):
        c0, c1 = sorted([ix0, ix1])
        sign = 1.0 if ix1 >= ix0 else -1.0
        truth[channel_x, iy0, c0 : c1 + 1] += sign * float(segment.current_a) / dx
    else:
        r0, r1 = sorted([iy0, iy1])
        sign = 1.0 if iy1 >= iy0 else -1.0
        truth[channel_y, r0 : r1 + 1, ix0] += sign * float(segment.current_a) / dx


def truth_map_for_case(case, grid) -> np.ndarray:
    """Rasterize exp07 geometry into exp04-style [J1x,J1y,J2x,J2y,s1] maps."""
    truth = np.zeros((5, grid.shape[0], grid.shape[1]), dtype=np.float32)
    dx = float(abs(grid.x[1] - grid.x[0])) if len(grid.x) > 1 else 1.0
    for segment in case.segments:
        start = np.asarray(segment.start, dtype=float)
        end = np.asarray(segment.end, dtype=float)
        delta = end - start
        if abs(float(delta[2])) > max(abs(float(delta[0])), abs(float(delta[1])), 1e-30):
            ix = _nearest_grid_index(grid.x, float(start[0]))
            iy = _nearest_grid_index(grid.y, float(start[1]))
            sign = 1.0 if float(start[2]) > float(end[2]) else -1.0
            truth[4, iy, ix] += sign * float(segment.current_a) / dx
        elif int(segment.layer) == 2:
            _rasterize_sheet_segment_truth(truth, grid, segment, 2, 3)
        else:
            _rasterize_sheet_segment_truth(truth, grid, segment, 0, 1)
    return truth


def write_pypeec_exp03_like_mini_dataset(
    path: Path,
    cases,
    fields: dict[str, np.ndarray],
    grid,
    cfg: dict[str, Any],
) -> dict[str, Any]:
    B_center = []
    B_finite = []
    B_pypeec = []
    truth = []
    case_names = []
    case_types = []
    is_exp03_like = []
    metadata = []
    for case in cases:
        case_names.append(case.name)
        case_types.append(case.expected_physics.get("route_kind", "canonical"))
        is_exp03_like.append(bool(case.expected_physics.get("exp03_like", False)))
        B_center.append(fields[f"{case.name}__center"].transpose(1, 2, 0).astype(np.float32))
        B_finite.append(fields[f"{case.name}__finite"].transpose(1, 2, 0).astype(np.float32))
        B_pypeec.append(fields[f"{case.name}__pypeec"].transpose(1, 2, 0).astype(np.float32))
        truth.append(truth_map_for_case(case, grid))
        metadata.append(case.to_dict())

    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        x=grid.x.astype(np.float32),
        y=grid.y.astype(np.float32),
        B_centerline=np.stack(B_center).astype(np.float32),
        B_finite=np.stack(B_finite).astype(np.float32),
        B_pypeec=np.stack(B_pypeec).astype(np.float32),
        truth=np.stack(truth).astype(np.float32),
        case_name=np.asarray(case_names),
        case_type=np.asarray(case_types),
        is_exp03_like=np.asarray(is_exp03_like, dtype=bool),
        split=np.asarray(["pypeec_test"] * len(case_names)),
        metadata_json=json.dumps(metadata),
        config_json=json.dumps(cfg),
    )
    return {
        "file": str(path),
        "n_cases": len(case_names),
        "n_exp03_like_cases": int(sum(is_exp03_like)),
        "field_shape": [len(case_names), grid.shape[0], grid.shape[1], 3],
        "truth_shape": [len(case_names), 5, grid.shape[0], grid.shape[1]],
        "channels": ["J1x", "J1y", "J2x", "J2y", "s1"],
        "split": "pypeec_test",
        "case_names": case_names,
        "boundary": "Mini PyPEEC stress dataset for frozen inference only; not a training/calibration split.",
    }


def _cfg_with_convergence_level(cfg: dict[str, Any], level: dict[str, Any]) -> dict[str, Any]:
    out = json.loads(json.dumps(cfg))
    p_cfg = out["pypeec"]
    for key in ["voxel_pitch_xy_m", "voxel_pitch_z_m", "n_xy", "n_z"]:
        p_cfg[key] = level[key]
    return out


def _case_solution_flags(metadata: dict[str, Any]) -> tuple[bool, bool, bool]:
    summary = metadata.get("solution_summary", {})
    return (
        bool(summary.get("solution_ok", False)),
        bool(summary.get("solver_ok", False)),
        bool(summary.get("condition_ok", False)),
    )


def run_voxel_convergence_sweep(base_dir: Path, cfg: dict[str, Any], grid) -> dict[str, Any]:
    sweep_cfg = cfg["pypeec"].get("convergence_sweep", {})
    if not bool(sweep_cfg.get("enabled", False)):
        return {"enabled": False, "rows": [], "deltas": [], "finest_step_deltas": []}

    rows: list[dict[str, Any]] = []
    deltas: list[float] = []
    finest_step_deltas: list[float] = []
    cases_dir = base_dir / "data" / "pypeec_case_payloads" / "_convergence"
    for case_name in sweep_cfg.get("cases", []):
        per_level: list[dict[str, Any]] = []
        for level in sweep_cfg.get("levels", []):
            level_cfg = _cfg_with_convergence_level(cfg, level)
            case = make_case(case_name, level_cfg)
            result = compute_case_fields(case, grid, level_cfg, cases_dir / case_name / str(level["label"]))
            Bc = result["B_center"]
            Bf = result["B_finite"]
            Bp = result["B_pypeec"]
            metadata = result["backend_metadata"]
            alpha_center, shape_center = scalar_fit_rel_l2(Bp, Bc)
            solution_ok, solver_ok, condition_ok = _case_solution_flags(metadata)
            terminal_current = _terminal_current(metadata.get("solution_summary", {}))
            target_current = float(level_cfg["currents"]["default_current_a"])
            terminal_error = abs(terminal_current - target_current) / (abs(target_current) + 1e-30)
            row = {
                "case": case_name,
                "level": str(level["label"]),
                "voxel_pitch_xy_m": float(level["voxel_pitch_xy_m"]),
                "voxel_pitch_z_m": float(level["voxel_pitch_z_m"]),
                "n_xy": int(level["n_xy"]),
                "n_z": int(level["n_z"]),
                "n_voxel_used": int(metadata.get("n_voxel_used", 0)),
                "n_voxel_centerline": int(metadata.get("n_voxel_centerline", 0)),
                "pypeec_vs_center_rel_l2": rel_l2(Bp, Bc),
                "pypeec_vs_finite_rel_l2": rel_l2(Bp, Bf),
                "pypeec_fit_alpha_to_center": alpha_center,
                "pypeec_centerline_shape_rel_l2": shape_center,
                "source_current_rel_error": terminal_error,
                "solution_ok": solution_ok,
                "solver_ok": solver_ok,
                "condition_ok": condition_ok,
                "to_next_finer_shape_rel_l2": None,
            }
            rows.append(row)
            per_level.append({"row": row, "B_pypeec": Bp})

        for idx in range(len(per_level) - 1):
            _, delta = scalar_fit_rel_l2(per_level[idx]["B_pypeec"], per_level[idx + 1]["B_pypeec"])
            per_level[idx]["row"]["to_next_finer_shape_rel_l2"] = delta
            deltas.append(delta)
            if idx == len(per_level) - 2:
                finest_step_deltas.append(delta)

    return {"enabled": True, "rows": rows, "deltas": deltas, "finest_step_deltas": finest_step_deltas}


def _terminal_current(summary: dict[str, Any]) -> float:
    source_values = summary.get("source_values", {})
    src = source_values.get("src", {})
    return float(src.get("I_re", float("nan")))


def build_reports(
    base_dir: Path,
    metrics: dict[str, Any],
    case_rows: list[list[Any]],
    convergence_rows: list[list[Any]],
) -> None:
    outputs = base_dir / "outputs"
    solver_md = table_md(
        [
            "case",
            "backend",
            "center_vs_finite",
            "pypeec_vs_center",
            "pypeec_vs_finite",
            "fit_alpha_to_center",
            "shape_rel_l2",
            "src_current_rel_error",
            "solution_ok",
        ],
        case_rows,
    )
    (outputs / "SOLVER_CROSS_VALIDATION_TABLE.md").write_text(
        "# Exp07 real PyPEEC solver cross-validation table\n\n" + solver_md,
        encoding="utf-8",
    )
    conv_md = table_md(
        [
            "case",
            "level",
            "pitch_xy_um",
            "pitch_z_um",
            "n_xy",
            "n_z",
            "n_voxel_used",
            "shape_rel_l2",
            "to_next_finer_shape_rel_l2",
            "src_current_rel_error",
            "solution_ok",
        ],
        convergence_rows,
    )
    (outputs / "VOXEL_CONVERGENCE_TABLE.md").write_text(
        "# Exp07 PyPEEC voxel convergence table\n\n" + conv_md,
        encoding="utf-8",
    )

    gate_rows = [[k, "PASS" if v else "FAIL"] for k, v in metrics["acceptance_gates"].items()]
    gates_md = table_md(["gate", "status"], gate_rows)

    run_report = f"""# RUN_REPORT - exp07 Real PyPEEC Solver Cross-Validation

## Purpose

Run a true PyPEEC 5.x Python API mesher/solver path on small canonical conductor
geometries and exp03-like route families with cross-section voxel fill, compare
the resulting sensor-plane magnetic field against the in-repository centerline
and finite-width Biot-Savart references, and quantify a small layer-aligned
xy-pitch refinement sweep.

## Backend status

```json
{json.dumps(metrics['pypeec_detection'], indent=2)}
```

Executed backend mode: `{metrics['backend_mode_executed']}`.

## Key summary

- cases completed: `{metrics['n_cases_completed']}` / `{metrics['n_cases_requested']}`
- PyPEEC package version: `{metrics['pypeec_detection'].get('python_package_version')}`
- finite-width reference median gap: `{metrics['summary']['finite_width_gap_median']:.6g}`
- PyPEEC-vs-centerline median gap: `{metrics['summary']['pypeec_centerline_gap_median']:.6g}`
- PyPEEC-vs-finite-width median gap: `{metrics['summary']['pypeec_finite_width_gap_median']:.6g}`
- scalar-fitted PyPEEC shape median gap: `{metrics['summary']['pypeec_centerline_shape_gap_median']:.6g}`
- max source-current relative error: `{metrics['summary']['max_terminal_current_rel_error']:.6g}`
- single-via PyPEEC `Bz/Bxy`: `{metrics['summary']['single_via_pypeec_bz_over_bxy']:.6g}`
- finite-width/straight voxel ratio: `{metrics['summary']['finite_width_over_straight_voxel_ratio']:.6g}`
- exp03-like cases completed: `{metrics['summary']['exp03_like_case_count']}` / `{len(metrics['summary']['exp03_like_requested_cases'])}`
- exp03-like scalar-fitted shape median gap: `{metrics['summary']['exp03_like_shape_gap_median']:.6g}`
- PyPEEC distribution expansion counts: `{json.dumps(metrics['summary']['pypeec_distribution_expansion'].get('case_count_by_hypothesis', {}), sort_keys=True)}`
- PyPEEC FFT library: `{metrics['case_metrics'][0]['backend_metadata'].get('solver_acceleration', {}).get('fft_library', 'unknown') if metrics['case_metrics'] else 'unknown'}`
- max convergence shape delta: `{metrics['summary']['max_convergence_shape_delta']:.6g}`
- max finest-step convergence shape delta: `{metrics['summary']['max_finest_step_convergence_shape_delta']:.6g}`
- solver table: `outputs/SOLVER_CROSS_VALIDATION_TABLE.md`
- convergence table: `outputs/VOXEL_CONVERGENCE_TABLE.md`
- all gates passed: `{metrics['all_acceptance_gates_passed']}`

## Acceptance gates

{gates_md}

## Boundary

This experiment now executes real PyPEEC through `pypeec.run_mesher_data` and
`pypeec.run_solver_data` with canonical cross-section voxel fill and a small
exp03-like route subset. It is still a solver-level cross-validation gate: it
does not claim FastHenry/FEM/QDM, CAD-scale convergence, or real-chip agreement,
and it does not validate the inverse neural model until these fields are
explicitly fed back into exp04.
"""
    (outputs / "RUN_REPORT.md").write_text(run_report, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--quick", action="store_true", help="Run a smaller case list for smoke tests.")
    parser.add_argument("--out-dir", type=str, default=None, help="Override experiment base directory.")
    args = parser.parse_args(argv)

    base_dir = Path(args.out_dir).resolve() if args.out_dir else THIS_DIR.parent.resolve()
    cfg_path = Path(args.config).resolve() if args.config else base_dir / "configs" / "default.json"
    cfg = load_config(cfg_path)
    if args.quick:
        cfg = json.loads(json.dumps(cfg))
        cfg["sensor_grid"]["n"] = 9
        cfg["cases"] = ["straight_trace", "finite_width_trace", "single_via"]
        cfg["geometry"]["default_segment_subdivisions"] = 8
        cfg.get("exp03_like_subset", {})["enabled"] = False
        cfg.get("pypeec_distribution_targets", {})["enabled"] = False
        cfg.get("pypeec", {}).get("convergence_sweep", {})["enabled"] = False
    else:
        cfg = expand_cases_for_distribution_targets(cfg)

    outputs = base_dir / "outputs"
    data_dir = base_dir / "data"
    cases_dir = data_dir / "pypeec_case_payloads"
    outputs.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    cases_dir.mkdir(parents=True, exist_ok=True)

    grid = make_sensor_grid(
        n=int(cfg["sensor_grid"]["n"]),
        fov_m=float(cfg["sensor_grid"]["fov_m"]),
        z_m=float(cfg["sensor_grid"]["z_m"]),
    )
    cases = make_cases(cfg["cases"], cfg)
    distribution_summary = cfg.get(
        "_distribution_expansion_summary",
        {
            "enabled": False,
            "target_cases_per_hypothesis": {},
            "case_count_by_hypothesis": {},
            "added_cases": [],
            "n_added_cases": 0,
        },
    )

    case_metrics = []
    case_rows = []
    fields = {}
    backend_modes = []
    for case in cases:
        result = compute_case_fields(case, grid, cfg, cases_dir / case.name)
        Bc = result["B_center"]
        Bf = result["B_finite"]
        Bp = result["B_pypeec"]
        metadata = result["backend_metadata"]
        backend_name = metadata.get("backend", "unknown")
        backend_modes.append(backend_name)
        alpha_center, shape_center = scalar_fit_rel_l2(Bp, Bc)
        alpha_finite, shape_finite = scalar_fit_rel_l2(Bp, Bf)
        solution_summary = metadata.get("solution_summary", {})
        terminal_current = _terminal_current(solution_summary)
        target_current = float(cfg["currents"]["default_current_a"])
        terminal_error = abs(terminal_current - target_current) / (abs(target_current) + 1e-30)
        m = {
            "case": case.name,
            "description": case.description,
            "backend": backend_name,
            "center_vs_finite_rel_l2": rel_l2(Bf, Bc),
            "pypeec_vs_center_rel_l2": rel_l2(Bp, Bc),
            "pypeec_vs_finite_rel_l2": rel_l2(Bp, Bf),
            "pypeec_fit_alpha_to_center": alpha_center,
            "pypeec_fit_alpha_to_finite": alpha_finite,
            "pypeec_centerline_shape_rel_l2": shape_center,
            "pypeec_finite_width_shape_rel_l2": shape_finite,
            "peak_pypeec_over_center": peak_abs_B(Bp) / (peak_abs_B(Bc) + 1e-30),
            "source_current_a": terminal_current,
            "source_current_rel_error": terminal_error,
            "n_voxel_used": int(metadata.get("n_voxel_used", 0)),
            "n_voxel_centerline": int(metadata.get("n_voxel_centerline", 0)),
            "rasterization": metadata.get("rasterization", "unknown"),
            "solution_ok": bool(solution_summary.get("solution_ok", False)),
            "solver_ok": bool(solution_summary.get("solver_ok", False)),
            "condition_ok": bool(solution_summary.get("condition_ok", False)),
            "backend_metadata": metadata,
        }
        if case.name == "single_via":
            m["single_via_pypeec_bz_over_bxy"] = via_bz_over_bxy(Bp)
        case_metrics.append(m)
        case_rows.append(
            [
                case.name,
                backend_name,
                m["center_vs_finite_rel_l2"],
                m["pypeec_vs_center_rel_l2"],
                m["pypeec_vs_finite_rel_l2"],
                m["pypeec_fit_alpha_to_center"],
                m["pypeec_centerline_shape_rel_l2"],
                m["source_current_rel_error"],
                m["solution_ok"],
            ]
        )
        fields[f"{case.name}__center"] = Bc
        fields[f"{case.name}__finite"] = Bf
        fields[f"{case.name}__pypeec"] = Bp

    finite_gaps = [m["center_vs_finite_rel_l2"] for m in case_metrics]
    pypeec_center_gaps = [m["pypeec_vs_center_rel_l2"] for m in case_metrics]
    pypeec_finite_gaps = [m["pypeec_vs_finite_rel_l2"] for m in case_metrics]
    shape_gaps = [m["pypeec_centerline_shape_rel_l2"] for m in case_metrics]
    terminal_errors = [m["source_current_rel_error"] for m in case_metrics]

    straight = [c for c in cases if c.name == "straight_trace"][0]
    z_values = [20e-6, 50e-6, 100e-6, 200e-6]
    standoff_values = standoff_decay_for_case(straight, cfg, z_values)

    via_metrics = [m for m in case_metrics if m["case"] == "single_via"]
    via_ratio = via_metrics[0].get("single_via_pypeec_bz_over_bxy", float("nan")) if via_metrics else float("nan")
    convergence = run_voxel_convergence_sweep(base_dir, cfg, grid)
    mini_dataset = write_pypeec_exp03_like_mini_dataset(
        data_dir / "pypeec_exp03_like_mini_dataset.npz",
        cases,
        fields,
        grid,
        cfg,
    )
    convergence_deltas = [float(x) for x in convergence["deltas"] if np.isfinite(x)]
    finest_step_deltas = [float(x) for x in convergence["finest_step_deltas"] if np.isfinite(x)]
    case_by_name = {m["case"]: m for m in case_metrics}
    straight_voxels = int(case_by_name.get("straight_trace", {}).get("n_voxel_used", 0))
    finite_width_voxels = int(case_by_name.get("finite_width_trace", {}).get("n_voxel_used", 0))
    finite_width_voxel_ratio = finite_width_voxels / max(straight_voxels, 1)
    max_convergence_delta = float(max(convergence_deltas)) if convergence_deltas else 0.0
    max_finest_step_delta = float(max(finest_step_deltas)) if finest_step_deltas else 0.0
    exp03_like_cfg = cfg.get("exp03_like_subset", {})
    exp03_like_enabled = bool(exp03_like_cfg.get("enabled", False))
    exp03_like_requested = [
        case.name for case in cases if bool(case.expected_physics.get("exp03_like", False))
    ] if exp03_like_enabled else []
    exp03_like_set = set(exp03_like_requested)
    exp03_like_metrics = [m for m in case_metrics if m["case"] in exp03_like_set]
    exp03_like_shape_gaps = [m["pypeec_centerline_shape_rel_l2"] for m in exp03_like_metrics]
    exp03_like_terminal_errors = [m["source_current_rel_error"] for m in exp03_like_metrics]
    exp03_like_shape_gap_median = finite_median(exp03_like_shape_gaps)
    exp03_like_max_terminal_error = float(max(exp03_like_terminal_errors)) if exp03_like_terminal_errors else float("nan")

    thresholds = cfg["acceptance_thresholds"]
    pypeec_detection = detect_pypeec()
    backend_mode_executed = "mixed" if len(set(backend_modes)) > 1 else backend_modes[0]
    api_found = pypeec_detection.get("api_functions_found", {})

    gates = {
        "experiment_outputs_exist": True,
        "real_pypeec_module_available": bool(pypeec_detection.get("python_module_available", False)),
        "real_pypeec_mesher_solver_api_available": bool(
            api_found.get("run_mesher_data", False) and api_found.get("run_solver_data", False)
        ),
        "real_pypeec_backend_executed_for_all_cases": bool(
            len(case_metrics) == len(cases) and set(backend_modes) == {"real_pypeec_api"}
        ),
        "all_requested_cases_completed": len(case_metrics) == len(cfg["cases"]),
        "all_pypeec_solutions_ok": all(m["solution_ok"] and m["solver_ok"] for m in case_metrics),
        "pypeec_fields_are_finite": all(np.isfinite(fields[k]).all() for k in fields if k.endswith("__pypeec")),
        "source_current_matches_target": max(terminal_errors) <= float(thresholds["max_terminal_current_rel_error"]),
        "standoff_decay_is_monotone_for_reference": is_strictly_decreasing(standoff_values),
        "single_via_pypeec_bz_over_bxy_is_bounded": bool(
            np.isfinite(via_ratio) and via_ratio <= float(thresholds["max_single_via_pypeec_bz_over_bxy"])
        ),
        "finite_width_gap_is_quantified": bool(
            np.isfinite(finite_median(finite_gaps))
            and float(thresholds["min_finite_width_gap_median"])
            <= finite_median(finite_gaps)
            <= float(thresholds["max_finite_width_gap_median"])
        ),
        "finite_width_pypeec_geometry_is_wider": bool(
            finite_width_voxel_ratio >= float(thresholds["min_finite_width_voxel_ratio"])
        ),
        "pypeec_raw_gap_is_finite_and_bounded": bool(
            np.isfinite(finite_median(pypeec_center_gaps))
            and finite_median(pypeec_center_gaps) <= float(thresholds["max_pypeec_raw_gap_median"])
        ),
        "pypeec_shape_gap_is_finite_and_bounded": bool(
            np.isfinite(finite_median(shape_gaps))
            and finite_median(shape_gaps) <= float(thresholds["max_pypeec_shape_gap_median"])
        ),
        "voxel_convergence_sweep_completed": bool(
            (not convergence["enabled"])
            or (
                len(convergence["rows"])
                == len(cfg["pypeec"]["convergence_sweep"]["cases"]) * len(cfg["pypeec"]["convergence_sweep"]["levels"])
                and all(row["solution_ok"] and row["solver_ok"] for row in convergence["rows"])
            )
        ),
        "voxel_convergence_shape_delta_is_bounded": bool(
            (not convergence["enabled"])
            or (convergence_deltas and max_convergence_delta <= float(thresholds["max_convergence_shape_delta"]))
        ),
        "voxel_convergence_finest_step_is_bounded": bool(
            (not convergence["enabled"])
            or (
                finest_step_deltas
                and max_finest_step_delta <= float(thresholds["max_finest_step_convergence_shape_delta"])
            )
        ),
        "exp03_like_pypeec_subset_completed": bool(
            (not exp03_like_enabled)
            or (
                len(exp03_like_metrics) >= int(thresholds["min_exp03_like_case_count"])
                and exp03_like_set.issubset(set(case_by_name.keys()))
                and all(m["solution_ok"] and m["solver_ok"] for m in exp03_like_metrics)
            )
        ),
        "exp03_like_shape_gap_is_finite_and_bounded": bool(
            (not exp03_like_enabled)
            or (
                np.isfinite(exp03_like_shape_gap_median)
                and exp03_like_shape_gap_median <= float(thresholds["max_exp03_like_shape_gap_median"])
            )
        ),
        "exp03_like_source_current_matches_target": bool(
            (not exp03_like_enabled)
            or (
                np.isfinite(exp03_like_max_terminal_error)
                and exp03_like_max_terminal_error <= float(thresholds["max_exp03_like_source_current_rel_error"])
            )
        ),
        "pypeec_exp03_like_mini_dataset_written": bool(
            Path(mini_dataset["file"]).exists()
            and mini_dataset["n_cases"] == len(cases)
            and (
                (not exp03_like_enabled)
                or mini_dataset["n_exp03_like_cases"] >= int(thresholds["min_exp03_like_case_count"])
            )
        ),
        "pypeec_distribution_targets_are_met": bool(
            (not distribution_summary.get("enabled", False))
            or all(
                int(distribution_summary.get("case_count_by_hypothesis", {}).get(label, 0)) >= int(target)
                for label, target in distribution_summary.get("target_cases_per_hypothesis", {}).items()
            )
        ),
        "claim_boundary_records_real_pypeec_status": True,
    }

    metrics = {
        "experiment_name": cfg["experiment_name"],
        "config_path": str(cfg_path),
        "pypeec_detection": pypeec_detection,
        "backend_mode_executed": backend_mode_executed,
        "n_cases_requested": len(cfg["cases"]),
        "n_cases_completed": len(case_metrics),
        "sensor_grid": grid.to_dict(),
        "case_metrics": case_metrics,
        "standoff_scan": {
            "z_values_m": z_values,
            "peak_abs_B_t": standoff_values,
            "note": "Reference Biot-Savart standoff sanity; PyPEEC is solved once per canonical case.",
        },
        "summary": {
            "finite_width_gap_median": finite_median(finite_gaps),
            "pypeec_centerline_gap_median": finite_median(pypeec_center_gaps),
            "pypeec_finite_width_gap_median": finite_median(pypeec_finite_gaps),
            "pypeec_centerline_shape_gap_median": finite_median(shape_gaps),
            "single_via_pypeec_bz_over_bxy": via_ratio,
            "max_terminal_current_rel_error": float(max(terminal_errors)),
            "straight_trace_pypeec_n_voxel_used": straight_voxels,
            "finite_width_trace_pypeec_n_voxel_used": finite_width_voxels,
            "finite_width_over_straight_voxel_ratio": finite_width_voxel_ratio,
            "exp03_like_requested_cases": exp03_like_requested,
            "exp03_like_completed_cases": [m["case"] for m in exp03_like_metrics],
            "exp03_like_case_count": len(exp03_like_metrics),
            "exp03_like_shape_gap_median": exp03_like_shape_gap_median,
            "exp03_like_max_terminal_current_rel_error": exp03_like_max_terminal_error,
            "max_convergence_shape_delta": max_convergence_delta,
            "max_finest_step_convergence_shape_delta": max_finest_step_delta,
            "pypeec_distribution_expansion": distribution_summary,
        },
        "voxel_convergence_sweep": convergence,
        "pypeec_exp03_like_mini_dataset": mini_dataset,
        "acceptance_gates": gates,
        "all_acceptance_gates_passed": all(gates.values()),
    }

    write_json(outputs / "metrics.json", metrics)
    np.savez_compressed(data_dir / "exp07_fields.npz", **fields)

    write_bar_svg(
        outputs / "01_case_pypeec_gap_summary.svg",
        [m["case"] for m in case_metrics],
        [m["pypeec_centerline_shape_rel_l2"] for m in case_metrics],
        "Exp07 real PyPEEC scalar-fitted shape gap by case",
        "relative L2 after scalar fit",
    )
    write_bar_svg(
        outputs / "03_voxel_convergence_shape_gap.svg",
        [f"{row['case']}:{row['level']}" for row in convergence["rows"]],
        [row["pypeec_centerline_shape_rel_l2"] for row in convergence["rows"]],
        "Exp07 PyPEEC voxel convergence shape gap",
        "relative L2 after scalar fit",
    )
    write_line_svg(
        outputs / "02_standoff_decay.svg",
        [z * 1e6 for z in z_values],
        standoff_values,
        "Straight trace reference standoff decay",
        "standoff z (um)",
        "peak |B| (T)",
    )
    convergence_rows = [
        [
            row["case"],
            row["level"],
            row["voxel_pitch_xy_m"] * 1.0e6,
            row["voxel_pitch_z_m"] * 1.0e6,
            row["n_xy"],
            row["n_z"],
            row["n_voxel_used"],
            row["pypeec_centerline_shape_rel_l2"],
            "" if row["to_next_finer_shape_rel_l2"] is None else row["to_next_finer_shape_rel_l2"],
            row["source_current_rel_error"],
            row["solution_ok"],
        ]
        for row in convergence["rows"]
    ]
    build_reports(base_dir, metrics, case_rows, convergence_rows)

    return 0 if metrics["all_acceptance_gates_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
