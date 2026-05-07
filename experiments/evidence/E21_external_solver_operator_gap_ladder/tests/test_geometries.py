"""Test canonical geometry definitions."""

import numpy as np
import pytest

from geometries import (
    straight_wire,
    wire_loop,
    finite_width_trace,
    via_vertical_segment,
    return_path_pair,
    small_multilayer_route,
    build_all_geometries,
    GeometryConfig,
)


def test_straight_wire():
    cfg = GeometryConfig(name="straight_wire", wire_half_length_um=100.0, layer1_z_um=0.0)
    geom = straight_wire(cfg)
    assert geom.name == "straight_wire"
    assert len(geom.segments) == 1
    p0, p1, name = geom.segments[0]
    assert name == "I_wire"
    assert p0[2] == 0.0
    assert p1[2] == 0.0


def test_wire_loop():
    cfg = GeometryConfig(name="wire_loop", loop_radius_um=50.0, layer1_z_um=0.0)
    geom = wire_loop(cfg)
    assert geom.geom_type == "wire_loop"
    assert len(geom.segments) == 8
    for p0, p1, name in geom.segments:
        assert p0[2] == 0.0
        assert "I_loop" in name


def test_via_vertical():
    cfg = GeometryConfig(name="via_vertical_segment", via_height_um=50.0,
                         layer1_z_um=25.0, layer2_z_um=-25.0)
    geom = via_vertical_segment(cfg)
    assert len(geom.segments) == 1
    p0, p1, name = geom.segments[0]
    assert name == "I_via"
    assert p0[2] == pytest.approx(25e-6)
    assert p1[2] == pytest.approx(-25e-6)


def test_finite_width_trace():
    cfg = GeometryConfig(name="finite_width_trace", wire_half_length_um=100.0,
                         wire_width_um=20.0, layer1_z_um=0.0)
    geom = finite_width_trace(cfg)
    assert len(geom.segments) == 5
    offsets = [s[0][1] for s in geom.segments]
    assert min(offsets) < 0
    assert max(offsets) > 0


def test_return_path_pair():
    cfg = GeometryConfig(name="return_path_pair", wire_half_length_um=100.0,
                         layer1_z_um=25.0, ground_z_um=-75.0, return_spacing_um=80.0)
    geom = return_path_pair(cfg)
    assert len(geom.segments) == 2
    names = [s[2] for s in geom.segments]
    assert "I_signal" in names
    assert "I_return" in names
    z_vals = [s[0][2] for s in geom.segments]
    assert any(np.isclose(z, 25e-6) for z in z_vals)
    assert any(np.isclose(z, -75e-6) for z in z_vals)


def test_small_multilayer_route():
    cfg = GeometryConfig(name="small_multilayer_route", layer1_z_um=30.0,
                         layer2_z_um=-30.0)
    geom = small_multilayer_route(cfg)
    assert len(geom.segments) == 4
    names = [s[2] for s in geom.segments]
    assert "I_via_down" in names or "I_via_up" in names
    assert "I_L1_h" in names
    assert "I_L2_v" in names


def test_build_all_geometries():
    cfgs = [
        GeometryConfig(name="straight_wire", wire_half_length_um=100.0, layer1_z_um=0.0),
        GeometryConfig(name="wire_loop", loop_radius_um=50.0, layer1_z_um=0.0),
    ]
    geoms = build_all_geometries(cfgs)
    assert len(geoms) == 2
    assert geoms[0].geom_type == "straight_wire"
    assert geoms[1].geom_type == "wire_loop"
