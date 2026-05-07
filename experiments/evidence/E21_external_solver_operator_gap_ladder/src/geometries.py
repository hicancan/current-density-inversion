"""Canonical geometry definitions for the operator-gap ladder.

Each geometry returns a list of (p0, p1, current_name) segments in SI units.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np

from config import GeometryConfig


@dataclass
class GeometryCase:
    name: str
    geom_type: str
    segments: List[Tuple[np.ndarray, np.ndarray, str]] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


def straight_wire(cfg: GeometryConfig) -> GeometryCase:
    L = cfg.wire_half_length_um * 1e-6
    z = cfg.layer1_z_um * 1e-6
    p0 = np.array([-L, 0.0, z])
    p1 = np.array([L, 0.0, z])
    return GeometryCase(
        name=cfg.name,
        geom_type="straight_wire",
        segments=[(p0, p1, "I_wire")],
        metadata={"length_um": 2 * cfg.wire_half_length_um, "z_um": cfg.layer1_z_um},
    )


def wire_loop(cfg: GeometryConfig) -> GeometryCase:
    R = cfg.loop_radius_um * 1e-6
    z = cfg.layer1_z_um * 1e-6
    n_sides = 8
    thetas = np.linspace(0, 2 * np.pi, n_sides + 1)
    segments = []
    for i in range(n_sides):
        t0, t1 = thetas[i], thetas[i + 1]
        p0 = np.array([R * np.cos(t0), R * np.sin(t0), z])
        p1 = np.array([R * np.cos(t1), R * np.sin(t1), z])
        segments.append((p0, p1, f"I_loop_{i}"))
    return GeometryCase(
        name=cfg.name,
        geom_type="wire_loop",
        segments=segments,
        metadata={"radius_um": cfg.loop_radius_um, "n_sides": n_sides, "z_um": cfg.layer1_z_um},
    )


def via_vertical_segment(cfg: GeometryConfig) -> GeometryCase:
    z1 = cfg.layer1_z_um * 1e-6
    z2 = cfg.layer2_z_um * 1e-6
    p0 = np.array([0.0, 0.0, z1])
    p1 = np.array([0.0, 0.0, z2])
    return GeometryCase(
        name=cfg.name,
        geom_type="via_vertical_segment",
        segments=[(p0, p1, "I_via")],
        metadata={"height_um": cfg.via_height_um, "radius_um": cfg.via_radius_um},
    )


def finite_width_trace(cfg: GeometryConfig) -> GeometryCase:
    """Represent a finite-width trace as multiple parallel filaments."""
    L = cfg.wire_half_length_um * 1e-6
    z = cfg.layer1_z_um * 1e-6
    width = cfg.wire_width_um * 1e-6
    n_fil = 5
    offsets = np.linspace(-width / 2, width / 2, n_fil)
    segments = []
    for i, off in enumerate(offsets):
        p0 = np.array([-L, off, z])
        p1 = np.array([L, off, z])
        segments.append((p0, p1, f"I_trace_fil_{i}"))
    return GeometryCase(
        name=cfg.name,
        geom_type="finite_width_trace",
        segments=segments,
        metadata={"length_um": 2 * cfg.wire_half_length_um, "width_um": cfg.wire_width_um, "n_filaments": n_fil},
    )


def return_path_pair(cfg: GeometryConfig) -> GeometryCase:
    L = cfg.wire_half_length_um * 1e-6
    z_signal = cfg.layer1_z_um * 1e-6
    z_return = cfg.ground_z_um * 1e-6
    spacing = cfg.return_spacing_um * 1e-6
    p_sig_a = np.array([-L, 0.0, z_signal])
    p_sig_b = np.array([L, 0.0, z_signal])
    p_ret_a = np.array([-L, spacing, z_return])
    p_ret_b = np.array([L, spacing, z_return])
    return GeometryCase(
        name=cfg.name,
        geom_type="return_path_pair",
        segments=[
            (p_sig_a, p_sig_b, "I_signal"),
            (p_ret_a, p_ret_b, "I_return"),
        ],
        metadata={
            "signal_z_um": cfg.layer1_z_um,
            "return_z_um": cfg.ground_z_um,
            "spacing_um": cfg.return_spacing_um,
        },
    )


def small_multilayer_route(cfg: GeometryConfig) -> GeometryCase:
    z1 = cfg.layer1_z_um * 1e-6
    z2 = cfg.layer2_z_um * 1e-6
    L = 80e-6
    segments = []
    segments.append((np.array([-L, 0.0, z1]), np.array([L, 0.0, z1]), "I_L1_h"))
    segments.append((np.array([0.0, -L, z2]), np.array([0.0, L, z2]), "I_L2_v"))
    segments.append((np.array([L, 0.0, z1]), np.array([L, 0.0, z2]), "I_via_down"))
    segments.append((np.array([0.0, L, z2]), np.array([0.0, L, z1]), "I_via_up"))
    return GeometryCase(
        name=cfg.name,
        geom_type="small_multilayer_route",
        segments=segments,
        metadata={"layer1_z_um": cfg.layer1_z_um, "layer2_z_um": cfg.layer2_z_um},
    )


GEOM_BUILDERS = {
    "straight_wire": straight_wire,
    "wire_loop": wire_loop,
    "finite_width_trace": finite_width_trace,
    "via_vertical_segment": via_vertical_segment,
    "return_path_pair": return_path_pair,
    "small_multilayer_route": small_multilayer_route,
}


def build_all_geometries(configs: List[GeometryConfig]) -> List[GeometryCase]:
    cases = []
    for cfg in configs:
        builder = GEOM_BUILDERS.get(cfg.name)
        if builder is None:
            raise ValueError(f"Unknown geometry: {cfg.name}")
        cases.append(builder(cfg))
    return cases


def total_segments(geom: GeometryCase) -> int:
    return len(geom.segments)
