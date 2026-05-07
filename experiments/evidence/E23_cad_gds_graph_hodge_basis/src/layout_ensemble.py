"""Parameterized generated PDN layout ensemble for E23 round 5.

Produces 40+ deterministic multi-port PDN-like layouts with fixed seed.
Varies: layers, ports, via/return placement, mesh density, geometry.
"""
from __future__ import annotations

import copy
import math
from typing import Any

import numpy as np


def generate_ensemble(
    n_layouts: int = 44,
    seed: int = 20260506,
) -> list[dict[str, Any]]:
    """Generate a deterministic ensemble of PDN-like layout dicts.

    Each layout follows the layout-graph-import-v1 schema used by layout_schema.py.
    Returns list of layout dicts with fixed random seed.
    """
    rng = np.random.RandomState(seed)
    layouts: list[dict] = []

    # Parameter ranges
    n_layers_options = [2, 3, 4, 5, 6]
    n_ports_options = [2, 4, 6, 8]  # sources + sinks, always balanced
    mesh_density_options = ["sparse", "medium", "dense"]
    x_extents = [3.0, 5.0, 8.0]
    y_extents = [1.0, 2.0, 3.0]
    via_density_options = ["few", "moderate", "many"]

    layer_names_pool = [
        ["TOP", "BOT"],
        ["TOP", "SIG1", "BOT"],
        ["TOP", "SIG1", "SIG2", "BOT"],
        ["TOP", "SIG1", "SIG2", "SIG3", "BOT"],
        ["TOP", "SIG1", "SIG2", "SIG3", "SIG4", "BOT"],
    ]

    for idx in range(n_layouts):
        nl = n_layers_options[idx % len(n_layers_options)]
        np_total = n_ports_options[idx % len(n_ports_options)]
        x_ext = x_extents[idx % len(x_extents)]
        y_ext = y_extents[idx % len(y_extents)]
        via_density = via_density_options[idx % len(via_density_options)]
        mesh_density = mesh_density_options[idx % len(mesh_density_options)]

        layer_names = layer_names_pool[nl - 2][:nl]

        # Stackup
        stackup = []
        layers = []
        z_top = 0.0
        for li, ln in enumerate(layer_names):
            z_bot = z_top - 3.0 - li * 8.0
            ltype = "power_strap" if li == 0 else ("return_grid" if li == nl - 1 else "mesh")
            stackup.append({
                "layer": ln, "z_top_um": z_top, "z_bottom_um": z_bot,
                "material": "copper", "conductivity_sm": 5.8e7,
            })
            layers.append({"name": ln, "type": ltype, "thickness_um": 3.0})
            z_top = z_bot

        # Ports: half sources on first layer, half sinks on last layer
        n_src = np_total // 2
        n_snk = np_total - n_src
        ports = []
        for i in range(n_src):
            y = -y_ext / 2 + (y_ext / (n_src + 1)) * (i + 1) if n_src > 1 else 0.0
            ports.append({
                "name": f"src_{i}", "layer": layer_names[0],
                "position_mm": {"x": 0.0, "y": y}, "net": "VDD", "role": "source",
            })
        for i in range(n_snk):
            y = -y_ext / 2 + (y_ext / (n_snk + 1)) * (i + 1) if n_snk > 1 else 0.0
            ports.append({
                "name": f"snk_{i}", "layer": layer_names[-1],
                "position_mm": {"x": x_ext, "y": y}, "net": "GND", "role": "sink",
            })

        # Traces: power straps on top, mesh on inner layers, return on bottom
        # Align trace endpoints to ensure via connectivity
        traces = []
        mesh_n = {"sparse": 1, "medium": 2, "dense": 3}[mesh_density]
        tw = 200.0 if nl <= 2 else 150.0
        via_x_positions = [x_ext * (k + 1) / (mesh_n + 1) for k in range(mesh_n)]

        for li, ln in enumerate(layer_names):
            if li == 0:  # top layer: power straps from sources
                for si in range(n_src):
                    sy = ports[si]["position_mm"]["y"]
                    traces.append({
                        "name": f"top_strap_{si}", "layer": ln,
                        "points_mm": [{"x": 0.0, "y": sy}, {"x": x_ext, "y": sy}],
                        "width_um": tw, "net": "VDD",
                    })
            elif li == nl - 1:  # bottom layer: return to sinks
                for si in range(n_snk):
                    sy = ports[n_src + si]["position_mm"]["y"]
                    traces.append({
                        "name": f"bot_return_{si}", "layer": ln,
                        "points_mm": [{"x": 0.0, "y": sy}, {"x": x_ext, "y": sy}],
                        "width_um": tw, "net": "GND",
                    })
            else:  # inner mesh layers
                for ti in range(min(mesh_n, len(via_x_positions))):
                    y = 0.0 if mesh_n == 1 else -y_ext/3 + (2*y_ext/3/(mesh_n-1))*ti if mesh_n > 1 else 0.0
                    x_start = via_x_positions[max(0, ti-1)] if ti > 0 else 0.5
                    x_end = via_x_positions[ti]
                    traces.append({
                        "name": f"{ln}_h_{ti}", "layer": ln,
                        "points_mm": [{"x": x_start, "y": y}, {"x": x_end, "y": y}],
                        "width_um": tw, "net": "VDD",
                    })

        # Vias: connect adjacent layers at trace endpoints to ensure connectivity
        vias = []
        n_via_per_level = {"few": 1, "moderate": 2, "many": 3}[via_density]
        for li in range(nl - 1):
            from_layer = layer_names[li]
            to_layer = layer_names[li + 1]
            # Get trace endpoints on from_layer
            from_traces = [t for t in traces if t["layer"] == from_layer]
            to_traces = [t for t in traces if t["layer"] == to_layer]
            for vi in range(min(n_via_per_level, len(from_traces), len(to_traces))):
                ft = from_traces[vi % len(from_traces)]
                tt = to_traces[vi % len(to_traces)]
                # Place via at the downstream end of from_trace
                fpts = ft["points_mm"]
                fx = fpts[-1]["x"]
                fy = fpts[-1]["y"]
                vias.append({
                    "name": f"via_{li}_{vi}",
                    "from_layer": from_layer,
                    "to_layer": to_layer,
                    "position_mm": {"x": fx, "y": fy},
                    "net": "VDD",
                })

        # Return planes
        return_planes = [{
            "name": "gnd_grid", "layer": layer_names[-1], "net": "GND",
            "outline_mm": [
                {"x": 0.0, "y": -y_ext - 0.5},
                {"x": x_ext + 0.5, "y": -y_ext - 0.5},
                {"x": x_ext + 0.5, "y": y_ext + 0.5},
                {"x": 0.0, "y": y_ext + 0.5},
            ],
        }]

        layout = {
            "schema": "layout-graph-import-v1",
            "description": f"Generated ensemble layout {idx}: {nl}L, {np_total}P, {via_density} vias, {mesh_density} mesh, {x_ext}x{y_ext}mm",
            "stackup": stackup,
            "layers": layers,
            "nets": [{"name": "VDD", "voltage": 1.0}, {"name": "GND", "voltage": 0.0}],
            "ports": ports,
            "traces": traces,
            "vias": vias,
            "return_planes": return_planes,
            "_ensemble_idx": idx,
            "_ensemble_meta": {
                "n_layers": nl, "n_ports": np_total, "n_sources": n_src, "n_sinks": n_snk,
                "via_density": via_density, "mesh_density": mesh_density,
                "x_extent": x_ext, "y_extent": y_ext,
            },
        }
        layouts.append(layout)

    return layouts


def is_multiport(layout: dict[str, Any]) -> bool:
    """Check if layout has enough ports for meaningful multi-state."""
    n_src = sum(1 for p in layout["ports"] if p.get("role") == "source")
    n_snk = sum(1 for p in layout["ports"] if p.get("role") == "sink")
    return (n_src + n_snk) > 2


def portfolio_summary(layouts: list[dict[str, Any]]) -> dict[str, Any]:
    """Summary statistics for a layout portfolio."""
    multiport = sum(1 for l in layouts if is_multiport(l))
    layers_counts = {}
    ports_counts = {}
    for l in layouts:
        nl = len(l["layers"])
        layers_counts[nl] = layers_counts.get(nl, 0) + 1
        np_ = len(l["ports"])
        ports_counts[np_] = ports_counts.get(np_, 0) + 1
    return {
        "total": len(layouts),
        "multiport": multiport,
        "layers_distribution": layers_counts,
        "ports_distribution": ports_counts,
    }
