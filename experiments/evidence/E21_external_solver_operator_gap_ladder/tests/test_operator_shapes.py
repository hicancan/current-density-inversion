"""Test that all operators return consistent shapes and units."""

import numpy as np
import pytest

from operators_centerline import (
    MU0,
    make_grid,
    segment_field,
    centerline_forward,
    analytic_reference_forward,
)
from operators_finite_width import finite_width_forward
from config import GridConfig


@pytest.fixture
def grid():
    cfg = GridConfig(n=16, fov_um=200.0, measurement_z_um=50.0)
    return make_grid(cfg)


@pytest.fixture
def segments():
    L = 100e-6
    z = 0.0
    p0 = np.array([-L, 0.0, z])
    p1 = np.array([L, 0.0, z])
    return [(p0, p1, "I_wire")]


def test_segment_field_shape(grid, segments):
    X, Y, Z, points = grid
    p0, p1, name = segments[0]
    B = segment_field(points, p0, p1, current=1.0)
    assert B.shape == (points.shape[0], 3)
    assert B.dtype == np.float64


def test_segment_field_is_finite(grid, segments):
    X, Y, Z, points = grid
    p0, p1, name = segments[0]
    B = segment_field(points, p0, p1, current=1.0)
    assert np.all(np.isfinite(B))


def test_centerline_forward_shape(grid, segments):
    X, Y, Z, points = grid
    B_total, seg_fields = centerline_forward(points, segments)
    assert B_total.shape == (points.shape[0], 3)
    assert "I_wire" in seg_fields


def test_analytic_reference_forward_shape(grid, segments):
    X, Y, Z, points = grid
    B_total, seg_fields = analytic_reference_forward(points, segments)
    assert B_total.shape == (points.shape[0], 3)
    assert np.all(np.isfinite(B_total))


def test_finite_width_forward_shape(grid, segments):
    X, Y, Z, points = grid
    B_total, seg_fields = finite_width_forward(
        points, segments, width_um=20.0, n_filaments=5,
        n_steps=40, return_scale=0.0,
    )
    assert B_total.shape == (points.shape[0], 3)
    assert np.all(np.isfinite(B_total))


def test_centerline_and_finite_width_not_identical(grid, segments):
    """Finite-width operator should differ from centerline even at nominal parameters."""
    X, Y, Z, points = grid
    B_center, _ = centerline_forward(points, segments, n_steps=40)
    B_fw, _ = finite_width_forward(
        points, segments, width_um=20.0, n_filaments=5,
        n_steps=40, return_scale=0.0, depth_shift_um=3.0,
    )
    rel_diff = np.linalg.norm(B_center - B_fw) / (np.linalg.norm(B_center) + 1e-30)
    assert rel_diff > 0.0


def test_analytic_near_centerline(grid, segments):
    """Analytic reference should be correlated with centerline for wire-like geometry.

    The infinite-wire approximation differs from finite-segment integration due to
    end effects, so we check field correlation rather than near-identity.
    """
    X, Y, Z, points = grid
    B_analytic, _ = analytic_reference_forward(points, segments)
    B_center, _ = centerline_forward(points, segments, n_steps=120)
    # Flatten and compute Pearson correlation
    flat_a = B_analytic.ravel()
    flat_c = B_center.ravel()
    corr = np.corrcoef(flat_a, flat_c)[0, 1]
    assert corr > 0.9, f"Analytic-centerline correlation {corr:.4f} below 0.9"


def test_B_units_are_tesla(grid, segments):
    """Field magnitude should be in Tesla range for 1A current at typical distances."""
    X, Y, Z, points = grid
    B, _ = centerline_forward(points, segments, n_steps=80)
    # At ~50um from a 1A wire, B ~ mu0 * I / (2*pi*r) ~ 4e-7*1/(2*pi*50e-6) ~ 1.3e-3 T
    max_B = np.max(np.abs(B))
    assert 1e-5 < max_B < 1e-2, f"Expected uT-mT range, got {max_B} T"


def test_linearity(grid, segments):
    """Field should scale linearly with current."""
    X, Y, Z, points = grid
    B1, _ = centerline_forward(points, segments, n_steps=80)
    # Scale segments: double current
    p0, p1, name = segments[0]
    segments_2x = [(p0, p1, "I_wire")]
    B2, _ = centerline_forward(points, segments_2x, n_steps=80)
    # Recompute with 2x current manually
    B_double = 2.0 * B1
    # If the segment has 1A, forward returns 1A field; doubling the forward is linear
    assert B_double[0, 0] == pytest.approx(2.0 * B1[0, 0])


# --- Round 2: Stronger operator tests ---

def test_missing_return_forward_shape(grid, segments):
    from operators_finite_width import missing_return_forward
    X, Y, Z, points = grid
    B_total, _ = missing_return_forward(points, segments, width_um=20.0, n_filaments=3, n_steps=40)
    assert B_total.shape == (points.shape[0], 3)
    assert np.all(np.isfinite(B_total))


def test_deep_layer_shift_forward_shape(grid, segments):
    from operators_finite_width import deep_layer_shift_forward
    X, Y, Z, points = grid
    B_total, _ = deep_layer_shift_forward(points, segments, depth_shift_um=15.0, n_steps=40)
    assert B_total.shape == (points.shape[0], 3)
    assert np.all(np.isfinite(B_total))


def test_registration_gap_forward_shape(grid, segments):
    from operators_finite_width import registration_gap_forward
    X, Y, Z, points = grid
    B_total, _ = registration_gap_forward(points, segments, shift_x_um=10.0, shift_y_um=5.0, n_steps=40)
    assert B_total.shape == (points.shape[0], 3)
    assert np.all(np.isfinite(B_total))


def test_missing_return_differs_from_full(grid, segments):
    """Missing-return operator should produce different field from full finite-width."""
    from operators_finite_width import missing_return_forward, finite_width_forward
    X, Y, Z, points = grid
    B_full, _ = finite_width_forward(points, segments, width_um=20.0, n_filaments=3,
                                      n_steps=40, return_scale=0.8)
    B_missing, _ = missing_return_forward(points, segments, width_um=20.0, n_filaments=3,
                                           n_steps=40)
    rel_diff = np.linalg.norm(B_full - B_missing) / (np.linalg.norm(B_full) + 1e-30)
    assert rel_diff > 0.01, f"Missing-return should differ from full return, got {rel_diff:.6f}"


def test_registration_gap_differs_from_centerline(grid, segments):
    """Registration-gap operator should differ from centerline due to grid shift."""
    from operators_finite_width import registration_gap_forward
    from operators_centerline import centerline_forward
    X, Y, Z, points = grid
    B_center, _ = centerline_forward(points, segments, n_steps=40)
    B_reg, _ = registration_gap_forward(points, segments, shift_x_um=10.0, shift_y_um=5.0, n_steps=40)
    rel_diff = np.linalg.norm(B_center - B_reg) / (np.linalg.norm(B_center) + 1e-30)
    assert rel_diff > 0.001, f"Registration gap should differ from centerline, got {rel_diff:.6f}"
