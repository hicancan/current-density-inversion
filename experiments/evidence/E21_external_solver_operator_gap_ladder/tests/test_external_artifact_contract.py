"""Test external artifact contract and schema validation."""

import os
import tempfile

import numpy as np

from external_artifacts import (
    ExternalArtifactReport,
    SchemaValidationResult,
    validate_npz_schema,
    validate_comsol_artifact,
    validate_fasthenry_artifact,
)


def test_schema_validation_passes():
    data = {"Bx": np.ones(10), "By": np.ones(10), "Bz": np.ones(10)}
    result = validate_npz_schema(data, ["Bx", "By", "Bz"], ["metadata"])
    assert result.passed is True
    assert len(result.errors) == 0


def test_schema_validation_fails_missing():
    data = {"Bx": np.ones(10)}
    result = validate_npz_schema(data, ["Bx", "By", "Bz"], [])
    assert result.passed is False
    assert "By" in result.missing_required


def test_comsol_validation_none():
    result = validate_comsol_artifact(None)
    assert result.passed is False


def test_comsol_validation_valid():
    data = {"Bx": np.ones(10), "By": np.ones(10), "Bz": np.ones(10)}
    result = validate_comsol_artifact(data)
    assert result.passed is True


def test_fasthenry_validation_none():
    result = validate_fasthenry_artifact(None)
    assert result.passed is False


def test_external_artifact_report_blocked():
    report = ExternalArtifactReport.from_paths(comsol_path="", fasthenry_path="")
    assert report.status == "blocked"
    assert report.comsol_present is False
    assert report.fasthenry_present is False
    assert len(report.cannot_claim) > 0


def test_external_artifact_report_with_nonexistent_path():
    report = ExternalArtifactReport.from_paths(
        comsol_path="/nonexistent/path/file.npz",
        fasthenry_path="",
    )
    assert report.status == "blocked"
    assert report.comsol_present is False
