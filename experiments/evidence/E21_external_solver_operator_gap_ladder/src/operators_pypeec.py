"""PyPEEC operator interface and external artifact contract.

PyPEEC is an optional higher-fidelity solver bridge. This module provides:
1. A PyPEEC forward wrapper (if PyPEEC is installed).
2. Placeholder interfaces for COMSOL/FastHenry external artifacts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from config import GridConfig


@dataclass
class PyPEECStatus:
    available: bool = False
    version: str = ""
    error: str = ""
    backend: str = "none"


def detect_pypeec() -> PyPEECStatus:
    try:
        import pypeec  # noqa: F401
        return PyPEECStatus(
            available=True,
            version=getattr(pypeec, "__version__", "unknown"),
            backend="pypeec",
        )
    except ImportError as e:
        return PyPEECStatus(available=False, error=str(e))


def pypeec_forward(
    points: np.ndarray,
    geometry_segments: List[Tuple[np.ndarray, np.ndarray, str]],
    grid_cfg: GridConfig,
    frequency: float = 0.0,
) -> Tuple[Optional[np.ndarray], PyPEECStatus, str]:
    """Compute forward field using PyPEEC, if available.

    Attempts actual PyPEEC model creation and solve when the package is
    importable. Returns (B_total, status, boundary_note).
    B_total is None if PyPEEC is unavailable or fails.
    """
    status = detect_pypeec()
    if not status.available:
        return None, status, f"PyPEEC not installed; this operator is blocked. Error: {status.error}"

    boundary = (
        "PyPEEC forward computed on generated geometry. "
        "This is generated-domain higher-fidelity evidence, not real CAD/FEM/QDM validation. "
        f"PyPEEC version: {status.version}, backend: {status.backend}."
    )

    try:
        import pypeec
        result = _attempt_pypeec_solve(points, geometry_segments, pypeec, frequency)
        if result is None:
            return None, status, (
                "PyPEEC import succeeded but mesh/solve did not produce fields. "
                "Full PyPEEC pipeline (mesh, solve, field extraction) not yet integrated. "
                "This is a blocked/interface result. "
                + boundary
            )
        return result, status, boundary
    except Exception as e:
        return None, status, f"PyPEEC forward failed: {e}. {boundary}"


def _attempt_pypeec_solve(
    points: np.ndarray,
    segments: List,
    pypeec_module,
    frequency: float = 0.0,
) -> Optional[np.ndarray]:
    """Attempt to construct a trivial PyPEEC model and obtain fields.

    This is the smallest possible PyPEEC integration: create a line conductor,
    mesh it, solve DC, and extract B at observation points.
    """
    try:
        # Check for known PyPEEC API entrypoints
        has_mesh = hasattr(pypeec_module, 'Mesher') or hasattr(pypeec_module, 'mesher')
        has_solver = hasattr(pypeec_module, 'Solver') or hasattr(pypeec_module, 'solve')
        has_field = hasattr(pypeec_module, 'Fields') or hasattr(pypeec_module, 'compute_B')

        if not (has_mesh and has_solver):
            return None  # API surface not usable

        # Attempt minimal mesh from the first segment
        if not segments:
            return None

        # Build a simple conductor from the first segment
        p0, p1, _ = segments[0]
        try:
            # Try pypeec API — this is exploratory
            if hasattr(pypeec_module, 'StraightWire'):
                wire = pypeec_module.StraightWire(p0.tolist(), p1.tolist(), radius=1e-6)
            else:
                return None  # Unknown API shape

            if hasattr(pypeec_module, 'Mesher'):
                mesher = pypeec_module.Mesher(frequency=frequency)
                mesh = mesher.mesh([wire])
            else:
                return None

            if hasattr(pypeec_module, 'Solver'):
                solver = pypeec_module.Solver()
                solution = solver.solve(mesh)
            else:
                return None

            # Extract B at observation points
            if hasattr(solution, 'compute_B'):
                B = solution.compute_B(points)
                return np.asarray(B, dtype=float)
            if hasattr(pypeec_module, 'Fields'):
                B = pypeec_module.Fields.compute_B(solution, points)
                return np.asarray(B, dtype=float)

        except Exception:
            return None

    except Exception:
        return None

    return None


@dataclass
class ExternalArtifactContract:
    comsol_available: bool = False
    fasthenry_available: bool = False
    comsol_path: str = ""
    fasthenry_path: str = ""
    status: str = "blocked"
    boundary: str = ""

    @classmethod
    def check(cls, comsol_path: str = "", fasthenry_path: str = "") -> "ExternalArtifactContract":
        comsol_ok = False
        fh_ok = False
        boundary_parts = []

        import os
        if comsol_path and os.path.exists(comsol_path):
            comsol_ok = True
        if fasthenry_path and os.path.exists(fasthenry_path):
            fh_ok = True

        if not comsol_ok and not fh_ok:
            boundary_parts.append(
                "No COMSOL or FastHenry artifacts found. "
                "External solver validation is blocked until real artifact files are loaded. "
                "Cannot claim COMSOL/FastHenry/FEM validation."
            )
            status = "blocked"
        elif comsol_ok and not fh_ok:
            boundary_parts.append("COMSOL artifact present; FastHenry absent.")
            status = "partial"
        elif not comsol_ok and fh_ok:
            boundary_parts.append("FastHenry artifact present; COMSOL absent.")
            status = "partial"
        else:
            status = "full"

        return cls(
            comsol_available=comsol_ok,
            fasthenry_available=fh_ok,
            comsol_path=comsol_path,
            fasthenry_path=fasthenry_path,
            status=status,
            boundary=" ".join(boundary_parts),
        )


def ingest_comsol_artifact(path: str) -> Dict[str, Any]:
    """Placeholder COMSOL CSV/NPZ ingestion interface.

    Reads a COMSOL-exported field file if it exists. Returns a dict with
    status and any loaded data.
    """
    import os
    if not path or not os.path.exists(path):
        return {
            "status": "blocked",
            "artifact_present": False,
            "message": "COMSOL artifact not found. Cannot claim COMSOL/FEM validation.",
            "data": None,
        }

    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".npz":
            data = dict(np.load(path, allow_pickle=True))
        elif ext == ".csv":
            data = np.loadtxt(path, delimiter=",", skiprows=0)
        else:
            data = None
        return {
            "status": "loaded",
            "artifact_present": True,
            "message": f"COMSOL artifact loaded from {path}",
            "data_shape": str(data.shape) if hasattr(data, "shape") else "dict",
        }
    except Exception as e:
        return {
            "status": "error",
            "artifact_present": True,
            "message": f"COMSOL artifact load failed: {e}",
            "data": None,
        }


def ingest_fasthenry_artifact(path: str) -> Dict[str, Any]:
    """Placeholder FastHenry/Fasthenry-like exported currents/fields interface."""
    import os
    if not path or not os.path.exists(path):
        return {
            "status": "blocked",
            "artifact_present": False,
            "message": "FastHenry artifact not found. Cannot claim FastHenry validation.",
            "data": None,
        }
    try:
        data = np.loadtxt(path, delimiter=",", skiprows=0)
        return {
            "status": "loaded",
            "artifact_present": True,
            "message": f"FastHenry artifact loaded from {path}",
            "data_shape": str(data.shape),
        }
    except Exception as e:
        return {
            "status": "error",
            "artifact_present": True,
            "message": f"FastHenry artifact load failed: {e}",
            "data": None,
        }
