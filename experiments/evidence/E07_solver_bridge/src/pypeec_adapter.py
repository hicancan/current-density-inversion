"""Real PyPEEC API adapter for exp07.

This module intentionally has no proxy or fallback backend. A successful exp07
run must import the installed PyPEEC package and execute its public
``run_mesher_data`` and ``run_solver_data`` APIs.
"""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from geometry import CaseGeometry, Segment, SensorGrid
from reference_biot_savart import MU0


@dataclass(frozen=True)
class BackendResult:
    B_chw: np.ndarray
    metadata: dict[str, Any]


@dataclass(frozen=True)
class VoxelModel:
    geometry: dict[str, Any]
    problem: dict[str, Any]
    tolerance: dict[str, Any]
    index_counts: dict[str, int]
    n_total: int
    n_centerline_voxel: int
    pitch_m: tuple[float, float, float]
    center_m: tuple[float, float, float]
    cross_section_fill: bool


def detect_pypeec() -> dict[str, Any]:
    """Return an auditable snapshot of the real PyPEEC installation."""
    api_functions = [
        "run_mesher_data",
        "run_mesher_file",
        "run_solver_data",
        "run_solver_file",
        "run_arguments",
    ]
    spec = importlib.util.find_spec("pypeec")
    version = None
    import_error = None
    found_api: dict[str, bool] = {}
    if spec is not None:
        try:
            version = importlib.metadata.version("pypeec")
        except importlib.metadata.PackageNotFoundError:
            version = None
        try:
            import pypeec  # type: ignore

            found_api = {name: hasattr(pypeec, name) for name in api_functions}
        except Exception as exc:  # pragma: no cover - broken local installs only.
            import_error = repr(exc)
    optional_packages = {}
    for name in ["cupy", "mkl_fft", "pyfftw", "pydiso", "pyamg"]:
        opt_spec = importlib.util.find_spec(name)
        optional_packages[name] = {
            "available": opt_spec is not None,
            "origin": None if opt_spec is None else str(opt_spec.origin),
        }
    return {
        "python_module_available": spec is not None,
        "python_module_origin": None if spec is None else str(spec.origin),
        "python_package_version": version,
        "api_functions_checked": api_functions,
        "api_functions_found": found_api,
        "python_import_error": import_error,
        "optional_acceleration_packages": optional_packages,
    }


def require_real_pypeec() -> Any:
    detection = detect_pypeec()
    missing = [
        name
        for name in ["run_mesher_data", "run_solver_data"]
        if not detection["api_functions_found"].get(name, False)
    ]
    if (not detection["python_module_available"]) or missing or detection["python_import_error"]:
        raise RuntimeError(
            "Real PyPEEC is required for exp07, but the installed package is not usable. "
            f"detection={json.dumps(detection, sort_keys=True)}"
        )
    import pypeec  # type: ignore

    return pypeec


def _axis_centers(n: int, d: float, c: float) -> np.ndarray:
    return (np.arange(n, dtype=float) - (n - 1) / 2.0) * d + c


def _nearest(values: np.ndarray, value: float) -> int:
    return int(np.argmin(np.abs(values - value)))


def _voxel_index(ix: int, iy: int, iz: int, n: tuple[int, int, int]) -> int:
    nx, ny, _ = n
    return int(ix + nx * iy + nx * ny * iz)


def _unique_preserve_order(values: list[int]) -> list[int]:
    seen: set[int] = set()
    out: list[int] = []
    for value in values:
        if value not in seen:
            out.append(value)
            seen.add(value)
    return out


def _rasterize_segment(
    segment: Segment,
    xs: np.ndarray,
    ys: np.ndarray,
    zs: np.ndarray,
    n: tuple[int, int, int],
    step_m: float,
) -> list[int]:
    start = np.asarray(segment.start, dtype=float)
    end = np.asarray(segment.end, dtype=float)
    length = float(np.linalg.norm(end - start))
    if length <= 0:
        ix = _nearest(xs, float(start[0]))
        iy = _nearest(ys, float(start[1]))
        iz = _nearest(zs, float(start[2]))
        return [_voxel_index(ix, iy, iz, n)]
    n_sample = max(2, int(np.ceil(length / max(step_m, 1e-30))) + 1)
    out: list[int] = []
    for alpha in np.linspace(0.0, 1.0, n_sample):
        point = start + alpha * (end - start)
        ix = _nearest(xs, float(point[0]))
        iy = _nearest(ys, float(point[1]))
        iz = _nearest(zs, float(point[2]))
        out.append(_voxel_index(ix, iy, iz, n))
    return _unique_preserve_order(out)


def _segment_cross_section_axes(direction: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    direction = direction / (np.linalg.norm(direction) + 1e-30)
    z_axis = np.array([0.0, 0.0, 1.0])
    x_axis = np.array([1.0, 0.0, 0.0])
    seed = z_axis if abs(float(np.dot(direction, z_axis))) < 0.92 else x_axis
    u = np.cross(direction, seed)
    u = u / (np.linalg.norm(u) + 1e-30)
    v = np.cross(direction, u)
    v = v / (np.linalg.norm(v) + 1e-30)
    return u, v


def _half_cell_extent(axis: np.ndarray, pitch_m: tuple[float, float, float]) -> float:
    axis = np.asarray(axis, dtype=float)
    return 0.5 * float(np.dot(np.abs(axis), np.asarray(pitch_m, dtype=float)))


def _rasterize_segment_volume(
    segment: Segment,
    xs: np.ndarray,
    ys: np.ndarray,
    zs: np.ndarray,
    n: tuple[int, int, int],
    pitch_m: tuple[float, float, float],
) -> list[int]:
    """Rasterize a swept rectangular conductor volume onto intersecting voxels."""
    start = np.asarray(segment.start, dtype=float)
    end = np.asarray(segment.end, dtype=float)
    direction = end - start
    length = float(np.linalg.norm(direction))
    if length <= 0:
        return _rasterize_segment(segment, xs, ys, zs, n, step_m=min(pitch_m))

    tangent = direction / length
    width_axis, thickness_axis = _segment_cross_section_axes(tangent)
    half_along = _half_cell_extent(tangent, pitch_m)
    half_width = 0.5 * max(float(segment.width_m), 0.0) + _half_cell_extent(width_axis, pitch_m)
    half_thickness = 0.5 * max(float(segment.thickness_m), 0.0) + _half_cell_extent(thickness_axis, pitch_m)

    out: list[int] = []
    for iz, z in enumerate(zs):
        for iy, y in enumerate(ys):
            for ix, x in enumerate(xs):
                center = np.array([x, y, z], dtype=float)
                rel = center - start
                along = float(np.dot(rel, tangent))
                if along < -half_along or along > length + half_along:
                    continue
                along_clamped = min(max(along, 0.0), length)
                radial = rel - along_clamped * tangent
                w_coord = float(np.dot(radial, width_axis))
                t_coord = float(np.dot(radial, thickness_axis))
                if abs(w_coord) <= half_width and abs(t_coord) <= half_thickness:
                    out.append(_voxel_index(ix, iy, iz, n))
    return _unique_preserve_order(out)


def _build_tolerance(cfg: dict[str, Any]) -> dict[str, Any]:
    solver = cfg["pypeec"]["solver"]
    fft_library = str(solver.get("fft_library", "SciPy"))
    if fft_library == "CuPy" and importlib.util.find_spec("cupy") is None:
        raise RuntimeError(
            "exp07 requested PyPEEC FFT library 'CuPy', but CuPy is not importable in this Python environment."
        )
    return {
        "parallel_sweep": {"n_jobs": 0, "n_threads": None},
        "integral_simplify": float(solver["integral_simplify"]),
        "biot_savart": "face",
        "dense_options": {
            "method": "fft",
            "split": True,
            "fft_options": {
                "library": fft_library,
                "scipy_worker": 0,
                "fftw_thread": 0,
                "fftw_cache": True,
                "fftw_timeout": 100.0,
                "fftw_byte_align": 16,
            },
        },
        "factorization_options": {
            "schur": True,
            "library": "SuperLU",
            "pyamg_options": {"tol": 1.0e-6, "solver": "root", "krylov": None},
            "pardiso_options": {"thread_pardiso": 0, "thread_mkl": 0},
        },
        "solver_options": {
            "coupling": "direct",
            "status_options": {
                "ignore_status": False,
                "ignore_res": True,
                "rel_tol": 1.0e-3,
                "abs_tol": 1.0e-9,
            },
            "power_options": {
                "stop": True,
                "n_min": int(solver["power_n_min"]),
                "n_cmp": int(solver["power_n_cmp"]),
                "rel_tol": 1.0e-4,
                "abs_tol": 1.0e-10,
            },
            "direct_options": {
                "solver": "gmres",
                "rel_tol": float(solver["direct_rel_tol"]),
                "abs_tol": 1.0e-12,
                "n_inner": int(solver["direct_n_inner"]),
                "n_outer": int(solver["direct_n_outer"]),
            },
            "segregated_options": {
                "rel_tol": 1.0e-6,
                "abs_tol": 1.0e-12,
                "relax_electric": 1.0,
                "relax_magnetic": 1.0,
                "n_min": 2,
                "n_max": 10,
                "iter_electric_options": {
                    "solver": "gmres",
                    "rel_tol": 1.0e-6,
                    "abs_tol": 1.0e-12,
                    "n_inner": 10,
                    "n_outer": 10,
                },
                "iter_magnetic_options": {
                    "solver": "gmres",
                    "rel_tol": 1.0e-6,
                    "abs_tol": 1.0e-12,
                    "n_inner": 10,
                    "n_outer": 10,
                },
            },
        },
        "condition_options": {
            "check": False,
            "tolerance_electric": 1.0e15,
            "tolerance_magnetic": 1.0e15,
            "norm_options": {"t_accuracy": 2, "n_iter_max": 10},
        },
    }


def build_pypeec_model(case: CaseGeometry, grid: SensorGrid, cfg: dict[str, Any]) -> VoxelModel:
    p_cfg = cfg["pypeec"]
    nx = int(p_cfg["n_xy"])
    ny = int(p_cfg["n_xy"])
    nz = int(p_cfg["n_z"])
    dx = float(p_cfg["voxel_pitch_xy_m"])
    dy = float(p_cfg["voxel_pitch_xy_m"])
    dz = float(p_cfg["voxel_pitch_z_m"])
    center = (0.0, 0.0, -float(cfg["geometry"]["layer_gap_m"]))
    n = (nx, ny, nz)
    xs = _axis_centers(nx, dx, center[0])
    ys = _axis_centers(ny, dy, center[1])
    zs = _axis_centers(nz, dz, center[2])
    step_m = min(dx, dy, dz) * float(p_cfg["raster_step_fraction"])
    pitch_m = (dx, dy, dz)
    cross_section_fill = bool(p_cfg.get("cross_section_fill", True))

    centerline_order: list[int] = []
    conductor_order: list[int] = []
    for segment in case.segments:
        centerline_order.extend(_rasterize_segment(segment, xs, ys, zs, n, step_m=step_m))
        if cross_section_fill:
            conductor_order.extend(_rasterize_segment_volume(segment, xs, ys, zs, n, pitch_m))
        else:
            conductor_order.extend(_rasterize_segment(segment, xs, ys, zs, n, step_m=step_m))
    centerline_order = _unique_preserve_order(centerline_order)
    conductor_order = _unique_preserve_order(conductor_order)
    for idx in centerline_order:
        if idx not in conductor_order:
            conductor_order.append(idx)
    if len(conductor_order) < 2:
        raise RuntimeError(f"Case {case.name} rasterized to fewer than two conductor voxels.")
    if len(centerline_order) < 2:
        raise RuntimeError(f"Case {case.name} centerline rasterized to fewer than two voxels.")

    src = [centerline_order[0]]
    sink = [centerline_order[-1]]
    wire = [idx for idx in conductor_order if idx not in set(src + sink)]

    domain_index = {"wire": wire, "src": src, "sink": sink, "empty": []}
    geometry = {
        "mesh_type": "voxel",
        "data_voxelize": {
            "param": {"n": [nx, ny, nz], "d": [dx, dy, dz], "c": list(center)},
            "domain_index": domain_index,
        },
        "data_point": {
            "check_cloud": True,
            "filter_cloud": False,
            "pts_cloud": grid.points.astype(float).tolist(),
        },
        "data_resampling": {
            "use_reduce": False,
            "use_resample": False,
            "resampling_factor": [1, 1, 1],
        },
        "data_conflict": {
            "resolve_rules": True,
            "resolve_random": False,
            "conflict_rules": [],
        },
        "data_integrity": {
            "check_integrity": True,
            "domain_connected": {
                "conductor": {
                    "domain_group": [["wire"], ["src"], ["sink"]],
                    "connected": True,
                }
            },
            "domain_adjacent": {},
        },
    }

    current_a = float(cfg["currents"]["default_current_a"])
    material_val = {
        "copper": {
            "rho_re": float(p_cfg["rho_re_ohm_m"]),
            "rho_im": 0.0,
        },
        "empty": {"rho_re": 0.0, "rho_im": 0.0},
    }
    source_val = {
        "src": {
            "I_re": current_a,
            "I_im": 0.0,
            "Y_re": float(p_cfg["source_admittance_s"]),
            "Y_im": 0.0,
        },
        "sink": {
            "V_re": 0.0,
            "V_im": 0.0,
            "Z_re": float(p_cfg["sink_impedance_ohm"]),
            "Z_im": 0.0,
        },
        "empty": {"V_re": 0.0, "V_im": 0.0, "Z_re": 0.0, "Z_im": 0.0},
    }
    problem = {
        "material_def": {
            "copper": {
                "domain_list": ["src", "wire", "sink"],
                "material_type": "electric",
                "orientation_type": "isotropic",
                "var_type": "lumped",
            },
            "empty": {
                "domain_list": ["empty"],
                "material_type": "electric",
                "orientation_type": "isotropic",
                "var_type": "lumped",
            },
        },
        "source_def": {
            "src": {
                "domain_list": ["src"],
                "source_type": "current",
                "var_type": "lumped",
            },
            "sink": {
                "domain_list": ["sink"],
                "source_type": "voltage",
                "var_type": "lumped",
            },
            "empty": {
                "domain_list": ["empty"],
                "source_type": "voltage",
                "var_type": "lumped",
            },
        },
        "material_val": material_val,
        "source_val": source_val,
        "sweep_solver": {
            "sim_dc": {
                "init": None,
                "param": {
                    "freq": 0.0,
                    "material_val": material_val,
                    "source_val": source_val,
                },
            }
        },
    }

    return VoxelModel(
        geometry=geometry,
        problem=problem,
        tolerance=_build_tolerance(cfg),
        index_counts={name: len(values) for name, values in domain_index.items()},
        n_total=nx * ny * nz,
        n_centerline_voxel=len(centerline_order),
        pitch_m=pitch_m,
        center_m=center,
        cross_section_fill=cross_section_fill,
    )


def _as_complex(value: Any) -> complex:
    if isinstance(value, complex):
        return value
    if isinstance(value, dict) and "__complex__" in value:
        return complex(float(value["real"]), float(value["imag"]))
    return complex(value)


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, np.ndarray):
        return _json_safe(value.tolist())
    if isinstance(value, np.generic):
        return _json_safe(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return None
    if isinstance(value, complex):
        return {"real": float(value.real), "imag": float(value.imag)}
    return value


def _extract_solution_data(solution: dict[str, Any]) -> dict[str, Any]:
    return solution["data"] if "data" in solution else solution


def _extract_B_chw(solution: dict[str, Any], grid: SensorGrid) -> np.ndarray:
    data = _extract_solution_data(solution)
    field_values = data["data_sweep"]["sim_dc"]["field_values"]
    H_p = np.asarray(field_values["H_p"]["var"])
    if H_p.shape != (grid.points.shape[0], 3):
        raise RuntimeError(f"PyPEEC H_p shape {H_p.shape} does not match point cloud {grid.points.shape}.")
    B_flat = MU0 * np.real(H_p)
    return B_flat.reshape(grid.shape[0], grid.shape[1], 3).transpose(2, 0, 1)


def _solution_summary(solution: dict[str, Any]) -> dict[str, Any]:
    data = _extract_solution_data(solution)
    sweep = data["data_sweep"]["sim_dc"]
    source_values = sweep.get("source_values", {})
    terminal_summary: dict[str, Any] = {}
    for name, values in source_values.items():
        terminal_summary[name] = {
            "source_type": values.get("source_type"),
            "var_type": values.get("var_type"),
            "V_re": float(_as_complex(values.get("V", 0.0)).real),
            "I_re": float(_as_complex(values.get("I", 0.0)).real),
            "S_re": float(_as_complex(values.get("S", 0.0)).real),
        }
    conv = _json_safe(sweep.get("solver_convergence", {}))
    return {
        "solution_ok": bool(sweep.get("solution_ok", False)),
        "solver_ok": bool(sweep.get("solver_ok", False)),
        "condition_ok": bool(sweep.get("condition_ok", False)),
        "solver_status": _json_safe(sweep.get("solver_status")),
        "condition_status": _json_safe(sweep.get("condition_status")),
        "solver_convergence": conv,
        "source_values": terminal_summary,
    }


def run_real_pypeec_backend(
    case: CaseGeometry,
    grid: SensorGrid,
    cfg: dict[str, Any],
    work_dir: Path,
) -> BackendResult:
    """Execute real PyPEEC mesher and solver APIs for one canonical case."""
    pypeec = require_real_pypeec()
    work_dir.mkdir(parents=True, exist_ok=True)
    model = build_pypeec_model(case, grid, cfg)

    (work_dir / f"{case.name}_geometry.json").write_text(
        json.dumps(model.geometry, indent=2),
        encoding="utf-8",
    )
    (work_dir / f"{case.name}_problem.json").write_text(
        json.dumps(model.problem, indent=2),
        encoding="utf-8",
    )
    (work_dir / f"{case.name}_tolerance.json").write_text(
        json.dumps(model.tolerance, indent=2),
        encoding="utf-8",
    )

    data_voxel = pypeec.run_mesher_data(model.geometry)
    solution = pypeec.run_solver_data(data_voxel, model.problem, model.tolerance)
    B_chw = _extract_B_chw(solution, grid)
    summary = _solution_summary(solution)
    (work_dir / f"{case.name}_solution_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    metadata = {
        "backend": "real_pypeec_api",
        "pypeec_detection": detect_pypeec(),
        "api_calls": ["pypeec.run_mesher_data", "pypeec.run_solver_data"],
        "mesh_type": "voxel",
        "rasterization": "cross_section_voxel_fill" if model.cross_section_fill else "centerline_voxel_skeleton",
        "voxel_shape": model.geometry["data_voxelize"]["param"]["n"],
        "voxel_pitch_m": list(model.pitch_m),
        "voxel_center_m": list(model.center_m),
        "n_voxel_total": model.n_total,
        "n_voxel_centerline": model.n_centerline_voxel,
        "n_voxel_used": int(sum(model.index_counts.values())),
        "domain_index_counts": model.index_counts,
        "solution_summary": summary,
        "solver_acceleration": {
            "fft_library": model.tolerance["dense_options"]["fft_options"]["library"],
            "cupy_available": importlib.util.find_spec("cupy") is not None,
            "gpu_requested": model.tolerance["dense_options"]["fft_options"]["library"] == "CuPy",
        },
        "claim_boundary": "Real PyPEEC 5.x Python API executed; this is still solver cross-validation, not FEM/QDM/real-chip validation.",
    }
    return BackendResult(B_chw=B_chw, metadata=metadata)
