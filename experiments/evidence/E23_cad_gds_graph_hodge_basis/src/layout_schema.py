"""Layout schema validation and parsing for E23 Graph-Hodge basis."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_LAYOUT_FIELDS = [
    "schema", "stackup", "layers", "nets", "ports", "traces", "vias", "return_planes"
]


def load_layout(path: str | Path) -> dict[str, Any]:
    """Load a JSON layout file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_layout(layout: dict[str, Any]) -> list[str]:
    """Validate a layout dict. Returns list of error messages (empty = valid)."""
    errors: list[str] = []

    for field in REQUIRED_LAYOUT_FIELDS:
        if field not in layout:
            errors.append(f"Missing required field: {field}")

    if errors:
        return errors

    layer_names = {ly["name"] for ly in layout["layers"]}
    stackup_names = {s["layer"] for s in layout["stackup"]}

    for ly in layout["layers"]:
        if ly["name"] not in stackup_names:
            errors.append(f"Layer '{ly['name']}' not found in stackup")

    net_names = {n["name"] for n in layout["nets"]}

    for port in layout["ports"]:
        if port["layer"] not in layer_names:
            errors.append(f"Port '{port['name']}' references unknown layer '{port['layer']}'")
        if port["net"] not in net_names:
            errors.append(f"Port '{port['name']}' references unknown net '{port['net']}'")
        if port.get("role") not in ("source", "sink"):
            errors.append(f"Port '{port['name']}' has invalid role '{port.get('role')}'")

    for trace in layout["traces"]:
        if trace["layer"] not in layer_names:
            errors.append(f"Trace '{trace['name']}' references unknown layer '{trace['layer']}'")
        if trace["net"] not in net_names:
            errors.append(f"Trace '{trace['name']}' references unknown net '{trace['net']}'")

    for via in layout["vias"]:
        if via["from_layer"] not in layer_names:
            errors.append(f"Via '{via['name']}' from_layer '{via['from_layer']}' unknown")
        if via["to_layer"] not in layer_names:
            errors.append(f"Via '{via['name']}' to_layer '{via['to_layer']}' unknown")
        if via["from_layer"] == via["to_layer"]:
            errors.append(f"Via '{via['name']}' from_layer equals to_layer")

    return errors


def parse_layout(layout: dict[str, Any]) -> dict[str, Any]:
    """Parse layout dict into normalized internal representation."""
    stackup_map: dict[str, dict] = {}
    for s in layout["stackup"]:
        z_mid = (s["z_top_um"] + s["z_bottom_um"]) / 2.0
        thickness = abs(s["z_top_um"] - s["z_bottom_um"])
        stackup_map[s["layer"]] = {
            "z_top_um": s["z_top_um"],
            "z_bottom_um": s["z_bottom_um"],
            "z_mid_um": z_mid,
            "thickness_um": thickness,
            "material": s.get("material", "copper"),
            "conductivity_sm": s.get("conductivity_sm", 5.8e7),
        }

    layers = []
    for ly in layout["layers"]:
        layers.append({
            "name": ly["name"],
            "type": ly.get("type", "signal"),
            "thickness_um": ly.get("thickness_um", 2.0),
        })

    nets = {n["name"]: n for n in layout["nets"]}

    ports = []
    for p in layout["ports"]:
        ports.append({
            "name": p["name"],
            "layer": p["layer"],
            "position_mm": (p["position_mm"]["x"], p["position_mm"]["y"]),
            "net": p["net"],
            "role": p["role"],
        })

    traces = []
    for t in layout["traces"]:
        pts = [(pt["x"], pt["y"]) for pt in t["points_mm"]]
        traces.append({
            "name": t["name"],
            "layer": t["layer"],
            "points_mm": pts,
            "width_um": t.get("width_um", 100.0),
            "net": t["net"],
        })

    vias = []
    for v in layout["vias"]:
        vias.append({
            "name": v["name"],
            "from_layer": v["from_layer"],
            "to_layer": v["to_layer"],
            "position_mm": (v["position_mm"]["x"], v["position_mm"]["y"]),
            "net": v.get("net", "VDD"),
        })

    return_planes = []
    for rp in layout.get("return_planes", []):
        outline = [(pt["x"], pt["y"]) for pt in rp["outline_mm"]]
        return_planes.append({
            "name": rp["name"],
            "layer": rp["layer"],
            "net": rp.get("net", "GND"),
            "outline_mm": outline,
        })

    return {
        "stackup": stackup_map,
        "layers": layers,
        "nets": nets,
        "ports": ports,
        "traces": traces,
        "vias": vias,
        "return_planes": return_planes,
    }
