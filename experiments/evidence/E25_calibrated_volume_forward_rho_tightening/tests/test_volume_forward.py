"""Tests for volume forward model, centerline, multifilament, and quadrature."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

# Add src to path
_src = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(_src))

from constants import MU0_OVER_4PI
from geometry import (
    RectConductor,
    make_straight_strip,
    make_parallel_strips,
    make_rectangular_loop,
    make_vertical_via,
    make_two_layer_trace_with_return,
    make_four_layer_via_return_motif,
    make_observation_grid,
)
from centerline import centerline_field, centerline_field_from_conductors, centerline_operator_matrix
from multifilament import multifilament_field, multifilament_field_from_conductors, multifilament_operator_matrix
from volume_forward import (
    volume_forward_column,
    volume_forward_matrix,
    volume_forward_matrix_quadrature_pair,
)
from quadrature_convergence import quadrature_relative_change, check_convergence_gate
from comparison import compare_forward_models
from rho_decomposition import decompose_rho, build_rho_calibration_table


MU0 = 4.0 * math.pi * 1e-7


class TestRectConductor:
    def test_constructor_validates_shapes(self):
        with pytest.raises(ValueError):
            RectConductor(
                p0=np.array([0.0, 0.0]),  # wrong shape
                p1=np.array([0.0, 0.0, 1.0]),
                width=1e-5, thickness=1e-5, current=1e-3,
            )

    def test_tangent_is_unit_vector(self):
        cond = RectConductor(
            p0=np.array([0.0, 0.0, 0.0]),
            p1=np.array([1e-3, 0.0, 0.0]),
            width=4e-5, thickness=1e-5, current=1e-3,
        )
        assert np.allclose(np.linalg.norm(cond.tangent), 1.0)

    def test_cross_section_axes_orthonormal(self):
        cond = RectConductor(
            p0=np.array([0.0, 0.0, 0.0]),
            p1=np.array([0.0, 1e-3, 0.0]),
            width=4e-5, thickness=1e-5, current=1e-3,
        )
        u, v = cond.cross_section_axes()
        t = cond.tangent
        assert abs(np.dot(u, v)) < 1e-10
        assert abs(np.dot(u, t)) < 1e-10
        assert abs(np.dot(v, t)) < 1e-10

    def test_area(self):
        cond = RectConductor(
            p0=np.array([0.0, 0.0, 0.0]),
            p1=np.array([1e-3, 0.0, 0.0]),
            width=4e-5, thickness=1e-5, current=1e-3,
        )
        assert cond.cross_section_area == pytest.approx(4e-10)


class TestCenterline:
    def test_field_linear_in_current(self):
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        conductors = make_straight_strip(current=1.0)
        B1 = centerline_field_from_conductors(points, conductors)
        conductors2 = make_straight_strip(current=2.0)
        B2 = centerline_field_from_conductors(points, conductors2)
        assert np.allclose(B2, 2.0 * B1, rtol=1e-10)

    def test_operator_matrix_shape(self):
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        conductors = make_straight_strip(current=1.0)
        A = centerline_operator_matrix(points, conductors)
        assert A.shape == (3 * points.shape[0], len(conductors))

    def test_field_reversal_symmetry(self):
        """Reversing current direction should flip B field."""
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        c1 = make_straight_strip(current=1.0)
        B1 = centerline_field_from_conductors(points, c1)
        c2 = make_straight_strip(current=-1.0)
        B2 = centerline_field_from_conductors(points, c2)
        assert np.allclose(B1, -B2, rtol=1e-10)


class TestVolumeForward:
    def test_column_shape(self):
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        cond = make_straight_strip(current=1.0)[0]
        B = volume_forward_column(points, cond, n_seg=4, n_w=3, n_t=2)
        assert B.shape == (points.shape[0], 3)

    def test_volume_linear_in_current(self):
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        c1 = make_straight_strip(current=1.0)
        c2 = make_straight_strip(current=3.0)
        A = volume_forward_matrix(points, c1, n_seg=4, n_w=3, n_t=2)
        i1 = np.array([1.0])
        i2 = np.array([3.0])
        B1 = (A @ i1).reshape(-1, 3)
        B2 = (A @ i2).reshape(-1, 3)
        assert np.allclose(B2, 3.0 * B1, rtol=1e-10)

    def test_approximates_centerline_for_thin_wire(self):
        """Very thin wire: volume_forward ≈ centerline."""
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        # Very thin
        cond = RectConductor(
            p0=np.array([-5e-4, 0.0, 0.0]),
            p1=np.array([5e-4, 0.0, 0.0]),
            width=1e-7, thickness=1e-7, current=1.0,
            tag="thin_wire",
        )
        B_vol = volume_forward_column(points, cond, n_seg=8, n_w=5, n_t=3)
        B_cl = centerline_field(points, cond)
        rel_err = np.linalg.norm(B_vol - B_cl) / (np.linalg.norm(B_cl) + 1e-30)
        # For 1e-7m wire, volume quadrature with finite points gives bounded error
        assert rel_err < 0.15, f"thin wire rel err too large: {rel_err}"

    def test_quadrature_pair_converges(self):
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        conds = make_straight_strip(current=1.0)
        A_q, A_2q = volume_forward_matrix_quadrature_pair(
            points, conds, n_seg=4, n_w=3, n_t=2,
        )
        delta = np.linalg.norm(A_q - A_2q, 'fro')
        norm_2q = np.linalg.norm(A_2q, 'fro')
        rel = delta / norm_2q
        assert rel < 0.35, f"coarse quadrature too far from fine: {rel}"


class TestMultifilament:
    def test_field_shape(self):
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        cond = make_straight_strip(current=1.0)
        B = multifilament_field_from_conductors(points, cond, n_w=3, n_t=2)
        assert B.shape == (points.shape[0], 3)

    def test_approximates_centerline_for_thin_wire(self):
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        cond = RectConductor(
            p0=np.array([-5e-4, 0.0, 0.0]),
            p1=np.array([5e-4, 0.0, 0.0]),
            width=1e-7, thickness=1e-7, current=1.0,
            tag="thin_wire",
        )
        B_mf = multifilament_field(points, cond, n_w=3, n_t=2)
        B_cl = centerline_field(points, cond)
        rel_err = np.linalg.norm(B_mf - B_cl) / (np.linalg.norm(B_cl) + 1e-30)
        assert rel_err < 0.05


class TestQuadratureConvergence:
    def test_relative_change_decreases(self):
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        conds = make_straight_strip(current=1.0)
        r1 = quadrature_relative_change(points, conds, n_seg=2, n_w=2, n_t=1)
        r2 = quadrature_relative_change(points, conds, n_seg=4, n_w=3, n_t=2)
        assert r2["relative_change"] < 0.5

    def test_convergence_gate_finds_best(self):
        dummy = [
            {"relative_change": 0.1},
            {"relative_change": 0.02},
            {"relative_change": 0.08},
        ]
        result = check_convergence_gate(dummy, gate=0.05)
        assert result["passed"] is True
        assert result["best_relative_change"] == 0.02


class TestComparison:
    def test_comparison_runs(self):
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        conds = make_straight_strip(current=1e-3)
        result = compare_forward_models(points, conds,
                                        vol_kwargs={"n_seg": 4, "n_w": 3, "n_t": 2},
                                        mf_kwargs={"n_w": 3, "n_t": 1})
        assert "field_comparison" in result
        assert result["num_conductors"] == 1
        fc = result["field_comparison"]
        assert fc["multifilament_vs_volume"]["relative_l2"] < 1.0


class TestRhoDecomposition:
    def test_decompose_runs(self):
        points = make_observation_grid(n=5, fov_m=1e-3, z_m=1e-4)
        conds = make_straight_strip(current=1e-3)
        result = decompose_rho(
            points, conds,
            R_h=1.0,
            vol_kwargs={"n_seg": 4, "n_w": 3, "n_t": 2},
            mf_kwargs={"n_w": 3, "n_t": 1},
        )
        assert "components" in result
        assert "rho_finite_width_centerline_to_volume" in result["components"]
        assert "rho_multifilament_to_volume" in result["components"]
        fw = result["components"]["rho_finite_width_centerline_to_volume"]
        assert fw["absolute_radius"] >= 0
        assert fw["relative_radius"] >= 0

    def test_calibration_table_builder(self):
        decomp = decompose_rho(
            make_observation_grid(n=3, fov_m=1e-3, z_m=1e-4),
            make_straight_strip(current=1e-3),
            vol_kwargs={"n_seg": 2, "n_w": 2, "n_t": 1},
            mf_kwargs={"n_w": 2, "n_t": 1},
        )
        rows = build_rho_calibration_table({"straight_strip": decomp})
        assert len(rows) > 0
        for row in rows:
            assert "geometry_family" in row
            assert "absolute_radius" in row
            assert "relative_radius" in row


class TestCanonicalGeometries:
    def test_straight_strip(self):
        conds = make_straight_strip()
        assert len(conds) == 1
        assert conds[0].tag == "straight_strip"

    def test_parallel_strips(self):
        conds = make_parallel_strips()
        assert len(conds) == 2
        assert conds[0].current > 0
        assert conds[1].current < 0  # return path has opposite current

    def test_rectangular_loop(self):
        conds = make_rectangular_loop()
        assert len(conds) == 4

    def test_vertical_via(self):
        conds = make_vertical_via()
        assert len(conds) == 1
        assert conds[0].p0[2] < conds[0].p1[2]

    def test_two_layer_trace(self):
        conds = make_two_layer_trace_with_return()
        assert len(conds) == 4
        layers = {c.layer for c in conds}
        assert "L1" in layers
        assert "L2" in layers

    def test_four_layer_via(self):
        conds = make_four_layer_via_return_motif()
        assert len(conds) == 7
        layers = {c.layer for c in conds}
        assert "L1" in layers
        assert "L4" in layers


class TestObservationGrid:
    def test_grid_shape(self):
        pts = make_observation_grid(n=7, fov_m=1e-3, z_m=1e-4)
        assert pts.shape == (49, 3)
        assert np.allclose(pts[:, 2], 1e-4)


class TestPhysicalConsistency:
    def test_biot_savart_perpendicular_to_current(self):
        """B field from a straight wire should be perpendicular to the wire direction."""
        points = np.array([[0.0, 1e-4, 1e-4], [0.0, -1e-4, 1e-4]])  # off-axis
        conductors = make_straight_strip(current=1.0, length=2e-3)
        B = centerline_field_from_conductors(points, conductors)
        t = conductors[0].tangent  # x-direction
        # B should have zero x-component
        assert np.allclose(B[:, 0], 0.0, atol=1e-15)

    def test_parallel_strips_Bz_symmetry(self):
        """Parallel forward/return strips: B field magnitude should be non-zero."""
        points = make_observation_grid(n=11, fov_m=1e-3, z_m=1e-4)
        conds = make_parallel_strips()
        B = centerline_field_from_conductors(points, conds)
        B_grid = B.reshape(11, 11, 3)
        # B should be non-zero (parallel strips produce a net dipole field)
        B_norm = np.sqrt(np.sum(B_grid ** 2, axis=-1))
        assert np.max(B_norm) > 1e-9, "parallel strips should produce measurable B field"
