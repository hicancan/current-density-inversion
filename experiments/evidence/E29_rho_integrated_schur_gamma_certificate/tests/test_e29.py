"""Tests for E29 Rho-Integrated Schur Gamma Certificate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

_src = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(_src))

from rho_local import (
    compute_full_rho_decomposition,
    centerline_operator,
    volume_operator,
    finite_width_rho,
)
from schur_signal import (
    generate_candidate_defects,
    generate_defect_operator,
    compute_schur_signal,
    compute_all_schur_signals,
)
from gamma import (
    compute_gamma_ablations,
    compute_all_defect_gammas,
    compute_aggregate_rates,
    compute_thresholds_from_calibration,
)
from pairwise import (
    compute_pairwise_delta,
    compute_pairwise_gamma,
    compute_pairwise_rates,
)
from split_discipline import (
    split_geometries,
    split_audit,
)


def _make_tiny_geometry():
    """Create a minimal 2-edge geometry for fast tests."""
    edges = np.zeros((2, 2, 3), dtype=float)
    edges[0, 0] = [-5e-4, 0, 0]
    edges[0, 1] = [5e-4, 0, 0]
    edges[1, 0] = [0, -5e-4, 5e-5]
    edges[1, 1] = [0, 5e-4, 5e-5]
    widths = np.array([4e-5, 4e-5])
    thicknesses = np.array([1e-5, 1e-5])
    n = 5
    fov = 1.2e-3
    xs = np.linspace(-fov / 2, fov / 2, n)
    ys = np.linspace(-fov / 2, fov / 2, n)
    X, Y = np.meshgrid(xs, ys)
    points = np.column_stack([X.ravel(), Y.ravel(), np.full(n * n, 8e-5)])
    return edges, widths, thicknesses, points


class TestRhoLocal:
    def test_full_decomposition_runs(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        result = compute_full_rho_decomposition(points, edges, widths, thicknesses)
        assert "components" in result
        comps = result["components"]
        assert "rho_finite_width" in comps
        assert "rho_combined_conservative" in comps
        assert "rho_combined_rss" in comps

    def test_conservative_gte_rss(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        result = compute_full_rho_decomposition(points, edges, widths, thicknesses)
        cons = result["components"]["rho_combined_conservative"]["absolute_radius"]
        rss = result["components"]["rho_combined_rss"]["absolute_radius"]
        assert cons >= rss

    def test_finite_width_rho_nonnegative(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        abs_rho, rel_rho = finite_width_rho(points, edges, widths, thicknesses)
        assert abs_rho >= 0
        assert rel_rho >= 0

    def test_centerline_operator_shape(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        A_cl = centerline_operator(points, edges)
        assert A_cl.shape == (3 * points.shape[0], edges.shape[0])

    def test_volume_operator_shape(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        A_vol = volume_operator(points, edges, widths, thicknesses)
        assert A_vol.shape == (3 * points.shape[0], edges.shape[0])

    def test_e23_old_rho_larger_than_finite_width(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        result = compute_full_rho_decomposition(points, edges, widths, thicknesses)
        rho_fw = result["components"]["rho_finite_width"]["absolute_radius"]
        rho_e23 = result["components"]["rho_combined_e23_old"]["absolute_radius"]
        # E23 old should be ~2.5x finite_width
        assert rho_e23 >= rho_fw


class TestSchurSignal:
    def test_generate_defects(self):
        defects = generate_candidate_defects(n_edges=4, seed=42)
        assert len(defects) > 0
        assert all("defect_id" in d for d in defects)
        assert all("defect_type" in d for d in defects)
        assert all("affected_edges" in d for d in defects)

    def test_schur_signal_nonnegative(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        A = volume_operator(points, edges, widths, thicknesses)
        defects = generate_candidate_defects(edges.shape[0], seed=42)
        A_def = generate_defect_operator(
            A, edges, widths, thicknesses, defects[0],
        )
        current = np.array([1.0, -1.0])
        signal = compute_schur_signal(A, A_def, current)
        assert signal["signal_max"] >= 0
        assert signal["snr"] >= 0

    def test_via_absence_reduces_operator_norm(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        A = volume_operator(points, edges, widths, thicknesses)
        defect = {
            "defect_id": "test_via_absence",
            "defect_type": "via_absence",
            "affected_edges": [1],
            "perturbation_magnitude": 0.9,
        }
        A_def = generate_defect_operator(
            A, edges, widths, thicknesses, defect,
        )
        # Column 1 should be reduced
        assert np.linalg.norm(A_def[:, 1]) < np.linalg.norm(A[:, 1])

    def test_compute_all_schur_signals(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        A = volume_operator(points, edges, widths, thicknesses)
        defects = generate_candidate_defects(edges.shape[0], seed=42)[:4]
        current_samples = np.random.default_rng(42).standard_normal(
            (edges.shape[0], 5)
        )
        results = compute_all_schur_signals(
            A, edges, widths, thicknesses, defects, current_samples,
        )
        assert len(results) == len(defects)
        assert all("signal_max" in r for r in results)


class TestGamma:
    def test_gamma_ablations_all_keys(self):
        result = compute_gamma_ablations(
            schur_signal_max=1.0,
            rho_components={
                "rho_combined_conservative": {"absolute_radius": 0.3},
                "rho_combined_rss": {"absolute_radius": 0.2},
                "rho_combined_e23_old": {"absolute_radius": 0.5},
            },
            epsilon=0.1,
            tau=0.1,
        )
        assert "gamma_no_rho" in result
        assert "gamma_rss_rho" in result
        assert "gamma_conservative_rho" in result
        assert "gamma_e23_old_rho" in result
        assert "gamma_e25_calibrated_rho" in result
        assert result["conservative_pass"] == (result["gamma_conservative_rho"] > 0)

    def test_no_rho_gamma_largest(self):
        result = compute_gamma_ablations(
            schur_signal_max=1.0,
            rho_components={
                "rho_combined_conservative": {"absolute_radius": 0.3},
                "rho_combined_rss": {"absolute_radius": 0.2},
                "rho_combined_e23_old": {"absolute_radius": 0.5},
            },
            epsilon=0.1,
            tau=0.1,
        )
        assert result["gamma_no_rho"] >= result["gamma_conservative_rho"]
        assert result["gamma_no_rho"] >= result["gamma_rss_rho"]
        assert result["gamma_no_rho"] >= result["gamma_e23_old_rho"]

    def test_negative_gamma_fails(self):
        result = compute_gamma_ablations(
            schur_signal_max=0.01,
            rho_components={
                "rho_combined_conservative": {"absolute_radius": 1.0},
                "rho_combined_rss": {"absolute_radius": 0.5},
                "rho_combined_e23_old": {"absolute_radius": 2.0},
            },
            epsilon=0.1,
            tau=0.1,
        )
        assert not result["conservative_pass"]
        assert not result["rss_pass"]
        assert not result["e23_old_pass"]

    def test_aggregate_rates_in_range(self):
        dummy_gammas = [
            {
                "defect_id": "d0", "defect_type": "via_absence",
                "no_rho_pass": True, "rss_pass": True, "conservative_pass": True,
                "e23_old_pass": True, "e25_calibrated_pass": True,
            },
            {
                "defect_id": "d1", "defect_type": "return_path_gap",
                "no_rho_pass": True, "rss_pass": False, "conservative_pass": False,
                "e23_old_pass": False, "e25_calibrated_pass": False,
            },
        ]
        rates = compute_aggregate_rates(dummy_gammas)
        assert 0 <= rates["positive_conservative_rho_rate"] <= 1
        assert 0 <= rates["empty_rate"] <= 1


class TestPairwise:
    def test_pairwise_delta_nonnegative(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        A = volume_operator(points, edges, widths, thicknesses)
        defects = generate_candidate_defects(edges.shape[0], seed=42)[:2]
        rng = np.random.default_rng(42)
        A_q = generate_defect_operator(
            A, edges, widths, thicknesses, defects[0], rng,
        )
        A_r = generate_defect_operator(
            A, edges, widths, thicknesses, defects[1], rng,
        )
        current = np.array([1.0, -1.0])
        pair = compute_pairwise_delta(A, A_q, A_r, current)
        assert pair["pairwise_delta_max"] >= 0
        assert pair["pairwise_delta_max"] >= pair["pairwise_delta_min"]

    def test_same_defect_zero_delta(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        A = volume_operator(points, edges, widths, thicknesses)
        defect = generate_candidate_defects(edges.shape[0], seed=42)[0]
        rng = np.random.default_rng(42)
        A_d = generate_defect_operator(
            A, edges, widths, thicknesses, defect, rng,
        )
        current = np.array([1.0, -1.0])
        pair = compute_pairwise_delta(A, A_d, A_d, current)
        assert pair["pairwise_delta_max"] < 1e-10


class TestSplitDiscipline:
    def test_split_produces_both_sets(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        defects = generate_candidate_defects(edges.shape[0], seed=42)
        split_info = split_geometries(
            edges, widths, thicknesses, defects,
            calibration_fraction=0.5, seed=42,
        )
        assert split_info["calibration"]["n_defects"] > 0
        assert split_info["evaluation"]["n_defects"] > 0

    def test_split_audit_no_overlap(self):
        edges, widths, thicknesses, points = _make_tiny_geometry()
        defects = generate_candidate_defects(edges.shape[0], seed=42)
        split_info = split_geometries(
            edges, widths, thicknesses, defects,
            calibration_fraction=0.5, seed=42,
        )
        audit = split_audit(split_info)
        cal_ids = {d["defect_id"] for d in split_info["calibration"]["defects"]}
        eval_ids = {d["defect_id"] for d in split_info["evaluation"]["defects"]}
        assert cal_ids.isdisjoint(eval_ids)


class TestThresholds:
    def test_thresholds_from_calibration(self):
        schur = [
            {"defect_id": "d0", "signal_max": 1.0},
            {"defect_id": "d1", "signal_max": 2.0},
            {"defect_id": "d2", "signal_max": 0.5},
        ]
        thresholds = compute_thresholds_from_calibration(
            schur, noise_sigma=1e-12, obs_dim=100,
        )
        assert thresholds["epsilon"] > 0
        assert thresholds["tau"] > 0
        assert thresholds["calibration_defect_count"] == 3
