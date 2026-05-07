"""Test layout schema validation and parsing."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from layout_schema import load_layout, validate_layout, parse_layout


def test_simple_two_layer_validates():
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    errors = validate_layout(layout)
    assert len(errors) == 0


def test_four_layer_pdn_validates():
    layout = load_layout(ROOT / "examples" / "four_layer_pdn_layout.json")
    errors = validate_layout(layout)
    assert len(errors) == 0


def test_parse_simple():
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    parsed = parse_layout(layout)
    assert len(parsed["stackup"]) == 2
    assert len(parsed["layers"]) == 2
    assert len(parsed["ports"]) == 2
    assert len(parsed["traces"]) == 2
    assert len(parsed["vias"]) == 1
    assert len(parsed["return_planes"]) == 1


def test_parse_four_layer():
    layout = load_layout(ROOT / "examples" / "four_layer_pdn_layout.json")
    parsed = parse_layout(layout)
    assert len(parsed["stackup"]) == 4
    assert len(parsed["ports"]) == 4
    assert len(parsed["vias"]) == 6
    assert parsed["ports"][0]["role"] in ("source", "sink")


def test_invalid_via_same_layer():
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    layout["vias"][0]["from_layer"] = "M1"
    layout["vias"][0]["to_layer"] = "M1"
    errors = validate_layout(layout)
    assert len(errors) > 0


def test_invalid_port_layer():
    layout = load_layout(ROOT / "examples" / "simple_two_layer_layout.json")
    layout["ports"][0]["layer"] = "NONEXISTENT"
    errors = validate_layout(layout)
    assert len(errors) > 0
