"""Canonical geometry contracts for exp07 real PyPEEC cross-validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Iterable
import math
import numpy as np


@dataclass(frozen=True)
class Segment:
    """Straight current-carrying conductor segment in SI units."""

    start: tuple[float, float, float]
    end: tuple[float, float, float]
    current_a: float
    width_m: float
    thickness_m: float
    layer: int
    tag: str

    def length(self) -> float:
        return float(np.linalg.norm(np.asarray(self.end) - np.asarray(self.start)))

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CaseGeometry:
    name: str
    description: str
    segments: tuple[Segment, ...]
    expected_physics: dict

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "segments": [s.to_dict() for s in self.segments],
            "expected_physics": self.expected_physics,
        }


@dataclass(frozen=True)
class SensorGrid:
    x: np.ndarray
    y: np.ndarray
    z: float

    @property
    def points(self) -> np.ndarray:
        xx, yy = np.meshgrid(self.x, self.y, indexing="xy")
        zz = np.full_like(xx, self.z, dtype=float)
        return np.stack([xx, yy, zz], axis=-1).reshape(-1, 3)

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.y), len(self.x))

    def to_dict(self) -> dict:
        return {
            "nx": int(len(self.x)),
            "ny": int(len(self.y)),
            "x_min_m": float(self.x.min()),
            "x_max_m": float(self.x.max()),
            "y_min_m": float(self.y.min()),
            "y_max_m": float(self.y.max()),
            "z_m": float(self.z),
        }


def make_sensor_grid(n: int = 49, fov_m: float = 1.2e-3, z_m: float = 80e-6) -> SensorGrid:
    half = 0.5 * fov_m
    axis = np.linspace(-half, half, int(n), dtype=float)
    return SensorGrid(x=axis, y=axis, z=float(z_m))


def _seg(
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    current: float,
    width: float,
    thickness: float,
    layer: int,
    tag: str,
) -> Segment:
    return Segment(start=start, end=end, current_a=float(current), width_m=float(width), thickness_m=float(thickness), layer=int(layer), tag=tag)


def _transform_xy(point: tuple[float, float, float], variant_index: int) -> tuple[float, float, float]:
    x, y, z = point
    scale = [0.84, 0.90, 0.96, 1.00][variant_index % 4]
    dx = [-36e-6, 0.0, 36e-6, -18e-6, 18e-6][variant_index % 5]
    dy = [30e-6, -30e-6, 0.0, 18e-6, -18e-6][(variant_index // 2) % 5]
    sx = -1.0 if (variant_index // 4) % 2 else 1.0
    sy = -1.0 if (variant_index // 8) % 2 else 1.0
    if (variant_index // 12) % 2:
        x, y = y, x
    return (sx * scale * x + dx, sy * scale * y + dy, z)


def _variant_case(base: CaseGeometry, name: str, variant_index: int) -> CaseGeometry:
    width_scale = [0.9, 1.0, 1.1][variant_index % 3]
    segments = tuple(
        replace(
            segment,
            start=_transform_xy(segment.start, variant_index),
            end=_transform_xy(segment.end, variant_index),
            width_m=float(segment.width_m) * width_scale,
            tag=f"{segment.tag}_v{variant_index:02d}",
        )
        for segment in base.segments
    )
    expected = dict(base.expected_physics)
    expected["variant_of"] = base.name
    expected["variant_index"] = int(variant_index)
    return CaseGeometry(
        name=name,
        description=f"{base.description} Deterministic exp07 geometry variant {variant_index:02d}.",
        segments=segments,
        expected_physics=expected,
    )


def make_case(name: str, cfg: dict) -> CaseGeometry:
    if "__v" in name:
        base_name, variant = name.rsplit("__v", 1)
        return _variant_case(make_case(base_name, cfg), name, int(variant))

    current = float(cfg["currents"]["default_current_a"])
    gap = float(cfg["geometry"]["layer_gap_m"])
    w = float(cfg["geometry"]["default_trace_width_m"])
    t = float(cfg["geometry"]["default_trace_thickness_m"])
    via_d = 2.0 * float(cfg["geometry"].get("default_via_radius_m", 0.5 * w))
    route = 0.42e-3
    sep = 0.12e-3

    if name == "straight_trace":
        segments = (
            _seg((-route, 0.0, 0.0), (route, 0.0, 0.0), current, w, t, 1, "top_x_trace"),
        )
        desc = "Single top-layer x-directed trace; checks sign and standoff decay."
        exp = {"standoff_decay": True, "dominant_components": ["By", "Bz"]}
    elif name == "finite_width_trace":
        segments = (
            _seg((-route, 0.0, 0.0), (route, 0.0, 0.0), current, 2.0 * w, 1.5 * t, 1, "wide_top_x_trace"),
        )
        desc = "Wider trace to expose centerline-vs-finite-width forward gap."
        exp = {"finite_width_gap_expected": True}
    elif name == "l_shape_trace":
        segments = (
            _seg((-route, -route, 0.0), (0.0, -route, 0.0), current, w, t, 1, "l_x_leg"),
            _seg((0.0, -route, 0.0), (0.0, route, 0.0), current, w, t, 1, "l_y_leg"),
        )
        desc = "Manhattan L-shape trace; checks corner and multi-direction current."
        exp = {"multi_direction": True}
    elif name == "parallel_traces":
        segments = (
            _seg((-route, -sep, 0.0), (route, -sep, 0.0), current, w, t, 1, "parallel_forward"),
            _seg((route, sep, 0.0), (-route, sep, 0.0), current, w, t, 1, "parallel_return"),
        )
        desc = "Two anti-parallel traces; checks cancellation and return-current effects."
        exp = {"return_current_like": True}
    elif name == "two_layer_crossing":
        segments = (
            _seg((-route, 0.0, 0.0), (route, 0.0, 0.0), current, w, t, 1, "top_x"),
            _seg((0.0, -route, -gap), (0.0, route, -gap), current, w, t, 2, "bottom_y"),
        )
        desc = "Orthogonal traces on two layers; checks layer/standoff mixing."
        exp = {"two_layer": True}
    elif name == "single_via":
        segments = (
            _seg((0.0, 0.0, -gap), (0.0, 0.0, 0.0), current, via_d, via_d, 0, "vertical_via"),
        )
        desc = "Single vertical via; Bz should be near zero in free-space Biot-Savart."
        exp = {"via_bz_over_bxy_should_be_small": True}
    elif name == "via_pair":
        segments = (
            _seg((-route, -sep, 0.0), (-sep, -sep, 0.0), current, w, t, 1, "top_left"),
            _seg((-sep, -sep, 0.0), (-sep, -sep, -gap), current, via_d, via_d, 0, "via_down"),
            _seg((-sep, -sep, -gap), (sep, -sep, -gap), current, w, t, 2, "bottom_x_bridge"),
            _seg((sep, -sep, -gap), (sep, sep, -gap), current, w, t, 2, "bottom_y_bridge"),
            _seg((sep, sep, -gap), (sep, sep, 0.0), current, via_d, via_d, 0, "via_up"),
            _seg((sep, sep, 0.0), (route, sep, 0.0), current, w, t, 1, "top_right"),
        )
        desc = "Two vias with a lower-layer bridge; checks source/sink-like vertical current signatures."
        exp = {"via_pair": True}
    elif name == "two_layer_route_with_via":
        segments = (
            _seg((-route, -1.5 * sep, 0.0), (-0.20e-3, -1.5 * sep, 0.0), current, w, t, 1, "l1_x_to_jog"),
            _seg((-0.20e-3, -1.5 * sep, 0.0), (-0.20e-3, 0.5 * sep, 0.0), current, w, t, 1, "l1_y_jog"),
            _seg((-0.20e-3, 0.5 * sep, 0.0), (-0.20e-3, 0.5 * sep, -gap), current, via_d, via_d, 0, "via_l1_to_l2"),
            _seg((-0.20e-3, 0.5 * sep, -gap), (route, 0.5 * sep, -gap), current, w, t, 2, "l2_x_exit"),
        )
        desc = "Exp03-like L1 jog, vertical via, and L2 exit route."
        exp = {"exp03_like": True, "route_kind": "l1_jog"}
    elif name == "multi_via_route":
        segments = (
            _seg((-route, -1.5 * sep, 0.0), (-0.28e-3, -1.5 * sep, 0.0), current, w, t, 1, "top_entry"),
            _seg((-0.28e-3, -1.5 * sep, 0.0), (-0.28e-3, -1.5 * sep, -gap), current, via_d, via_d, 0, "via_down_1"),
            _seg((-0.28e-3, -1.5 * sep, -gap), (0.0, -1.5 * sep, -gap), current, w, t, 2, "bottom_bridge_1"),
            _seg((0.0, -1.5 * sep, -gap), (0.0, -0.5 * sep, -gap), current, w, t, 2, "bottom_jog"),
            _seg((0.0, -0.5 * sep, -gap), (0.0, -0.5 * sep, 0.0), current, via_d, via_d, 0, "via_up_2"),
            _seg((0.0, -0.5 * sep, 0.0), (0.0, 1.5 * sep, 0.0), current, w, t, 1, "top_jog"),
            _seg((0.0, 1.5 * sep, 0.0), (0.0, 1.5 * sep, -gap), current, via_d, via_d, 0, "via_down_3"),
            _seg((0.0, 1.5 * sep, -gap), (route, 1.5 * sep, -gap), current, w, t, 2, "bottom_exit"),
        )
        desc = "Exp03-like continuous route with multiple layer transitions."
        exp = {"exp03_like": True, "route_kind": "multi_via"}
    elif name == "dense_via_background":
        segments = (
            _seg((-route, -2.0 * sep, 0.0), (-0.24e-3, -2.0 * sep, 0.0), current, 1.5 * w, t, 1, "wide_top_entry"),
            _seg((-0.24e-3, -2.0 * sep, 0.0), (-0.24e-3, -2.0 * sep, -gap), current, via_d, via_d, 0, "dense_via_down_1"),
            _seg((-0.24e-3, -2.0 * sep, -gap), (-0.08e-3, -2.0 * sep, -gap), current, w, t, 2, "dense_bottom_bridge_1"),
            _seg((-0.08e-3, -2.0 * sep, -gap), (-0.08e-3, -2.0 * sep, 0.0), current, via_d, via_d, 0, "dense_via_up_2"),
            _seg((-0.08e-3, -2.0 * sep, 0.0), (-0.08e-3, sep, 0.0), current, 1.5 * w, t, 1, "wide_top_jog"),
            _seg((-0.08e-3, sep, 0.0), (0.10e-3, sep, 0.0), current, 1.5 * w, t, 1, "wide_top_bridge"),
            _seg((0.10e-3, sep, 0.0), (0.10e-3, sep, -gap), current, via_d, via_d, 0, "dense_via_down_3"),
            _seg((0.10e-3, sep, -gap), (0.26e-3, sep, -gap), current, w, t, 2, "dense_bottom_bridge_2"),
            _seg((0.26e-3, sep, -gap), (0.26e-3, sep, 0.0), current, via_d, via_d, 0, "dense_via_up_4"),
            _seg((0.26e-3, sep, 0.0), (route, sep, 0.0), current, 1.5 * w, t, 1, "wide_top_exit"),
        )
        desc = "Exp03 OOD-inspired dense-via/background canonical route kept as a single connected path."
        exp = {"exp03_like": True, "route_kind": "dense_via_background"}
    elif name == "no_via_background":
        segments = (
            _seg((-route, 2.0 * sep, 0.0), (-0.12e-3, 2.0 * sep, 0.0), current, 1.5 * w, t, 1, "wide_top_entry"),
            _seg((-0.12e-3, 2.0 * sep, 0.0), (-0.12e-3, -sep, 0.0), current, 1.5 * w, t, 1, "wide_top_drop"),
            _seg((-0.12e-3, -sep, 0.0), (route, -sep, 0.0), current, 1.5 * w, t, 1, "wide_top_exit"),
        )
        desc = "Exp03-like no-via background control: a connected wide top-layer meander."
        exp = {"exp03_like": True, "route_kind": "no_via_background", "has_via": False}
    elif name == "bend_artifact_trace":
        segments = (
            _seg((-route, -sep, 0.0), (-0.16e-3, -sep, 0.0), current, 1.5 * w, t, 1, "artifact_main_entry"),
            _seg((-0.16e-3, -sep, 0.0), (-0.16e-3, 1.4 * sep, 0.0), current, 1.5 * w, t, 1, "corner_artifact_leg"),
            _seg((-0.16e-3, 1.4 * sep, 0.0), (0.10e-3, 1.4 * sep, 0.0), current, 1.5 * w, t, 1, "artifact_main_bridge"),
            _seg((0.10e-3, 1.4 * sep, 0.0), (0.10e-3, 0.15 * sep, 0.0), current, 1.5 * w, t, 1, "corner_artifact_return_leg"),
            _seg((0.10e-3, 0.15 * sep, 0.0), (route, 0.15 * sep, 0.0), current, 1.5 * w, t, 1, "artifact_main_exit"),
        )
        desc = "Exp03-like no-via hard negative with connected bend/corner artifact legs but no vertical via."
        exp = {
            "exp03_like": True,
            "route_kind": "bend_artifact",
            "has_via": False,
            "artifact_like": True,
            "artifact_mechanism": "bend_corner_induced_residual",
        }
    elif name == "trace_with_return_path":
        segments = (
            _seg((-route, 0.0, 0.0), (route, 0.0, 0.0), current, w, t, 1, "top_signal"),
            _seg((route, 0.0, 0.0), (route, 0.0, -gap), current, via_d, via_d, 0, "right_via_down"),
            _seg((route, 0.0, -gap), (-route, 0.0, -gap), current, 2.5 * w, 2.0 * t, 2, "lower_return"),
        )
        desc = "Connected signal trace with a lower return path; checks return-current cancellation."
        exp = {"return_path": True, "route_kind": "return_path"}
    else:
        raise ValueError(f"Unknown exp07 case: {name}")
    return CaseGeometry(name=name, description=desc, segments=segments, expected_physics=exp)


def make_cases(case_names: Iterable[str], cfg: dict) -> list[CaseGeometry]:
    return [make_case(name, cfg) for name in case_names]
