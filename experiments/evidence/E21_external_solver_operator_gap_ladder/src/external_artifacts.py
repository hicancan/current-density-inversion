"""External artifact interface contract and validation.

Provides schema validation and contract checking for COMSOL/FastHenry
external solver artifacts. When artifacts are absent, returns a valid
blocked/interface status, not a crash.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np


EXPECTED_COMSOL_SCHEMA = {
    "type": "object",
    "required_fields": ["Bx", "By", "Bz"],
    "optional_fields": ["x", "y", "z", "metadata", "units"],
}

EXPECTED_FASTHENRY_SCHEMA = {
    "type": "object",
    "required_fields": ["currents"],
    "optional_fields": ["segments", "nodes", "frequency", "metadata"],
}


@dataclass
class SchemaValidationResult:
    passed: bool
    errors: List[str]
    warnings: List[str]
    missing_required: List[str]


def validate_npz_schema(
    data: Dict[str, Any],
    required_fields: List[str],
    optional_fields: List[str],
) -> SchemaValidationResult:
    errors = []
    warnings = []
    missing = []
    for f in required_fields:
        if f not in data:
            errors.append(f"Missing required field: {f}")
            missing.append(f)
    for f in optional_fields:
        if f not in data:
            warnings.append(f"Optional field '{f}' not present")
    return SchemaValidationResult(
        passed=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        missing_required=missing,
    )


def validate_comsol_artifact(data: Optional[Dict[str, Any]]) -> SchemaValidationResult:
    if data is None:
        return SchemaValidationResult(
            passed=False,
            errors=["COMSOL artifact data is None"],
            warnings=[],
            missing_required=["Bx", "By", "Bz"],
        )
    return validate_npz_schema(
        data,
        EXPECTED_COMSOL_SCHEMA["required_fields"],
        EXPECTED_COMSOL_SCHEMA["optional_fields"],
    )


def validate_fasthenry_artifact(data: Optional[Dict[str, Any]]) -> SchemaValidationResult:
    if data is None:
        return SchemaValidationResult(
            passed=False,
            errors=["FastHenry artifact data is None"],
            warnings=[],
            missing_required=["currents"],
        )
    return validate_npz_schema(
        data,
        EXPECTED_FASTHENRY_SCHEMA["required_fields"],
        EXPECTED_FASTHENRY_SCHEMA["optional_fields"],
    )


@dataclass
class ExternalArtifactReport:
    comsol_present: bool = False
    fasthenry_present: bool = False
    comsol_validation: Optional[SchemaValidationResult] = None
    fasthenry_validation: Optional[SchemaValidationResult] = None
    status: str = "blocked"
    cannot_claim: List[str] = None

    def __post_init__(self):
        if self.cannot_claim is None:
            self.cannot_claim = []

    @classmethod
    def from_paths(cls, comsol_path: str = "", fasthenry_path: str = "") -> "ExternalArtifactReport":
        import os

        report = cls()
        if comsol_path and os.path.exists(comsol_path):
            try:
                ext = os.path.splitext(comsol_path)[1].lower()
                if ext == ".npz":
                    data = dict(np.load(comsol_path, allow_pickle=True))
                else:
                    data = {"Bx": None, "By": None, "Bz": None}
                report.comsol_present = True
                report.comsol_validation = validate_comsol_artifact(data)
            except Exception as e:
                report.comsol_validation = SchemaValidationResult(
                    passed=False, errors=[str(e)], warnings=[], missing_required=["Bx", "By", "Bz"]
                )
        else:
            report.comsol_validation = SchemaValidationResult(
                passed=False,
                errors=["COMSOL artifact not found at configured path"],
                warnings=[],
                missing_required=["Bx", "By", "Bz"],
            )

        if fasthenry_path and os.path.exists(fasthenry_path):
            try:
                ext = os.path.splitext(fasthenry_path)[1].lower()
                if ext == ".npz":
                    data = dict(np.load(fasthenry_path, allow_pickle=True))
                else:
                    data = {"currents": None}
                report.fasthenry_present = True
                report.fasthenry_validation = validate_fasthenry_artifact(data)
            except Exception as e:
                report.fasthenry_validation = SchemaValidationResult(
                    passed=False, errors=[str(e)], warnings=[], missing_required=["currents"]
                )
        else:
            report.fasthenry_validation = SchemaValidationResult(
                passed=False,
                errors=["FastHenry artifact not found at configured path"],
                warnings=[],
                missing_required=["currents"],
            )

        if report.comsol_present or report.fasthenry_present:
            report.status = "partial" if not (report.comsol_present and report.fasthenry_present) else "full"
        else:
            report.status = "blocked"
            report.cannot_claim = [
                "COMSOL/FastHenry/FEM validation — no external artifacts loaded",
                "External solver agreement — blocked until real artifact files are present",
            ]

        return report
