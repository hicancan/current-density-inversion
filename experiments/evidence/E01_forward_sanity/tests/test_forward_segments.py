from __future__ import annotations

import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
for name in list(sys.modules):
    if name == "forward" or name.startswith("forward."):
        del sys.modules[name]
sys.path.insert(0, str(ROOT / "src"))

from forward.grid import make_xy_grid
from forward.segments import b_field_from_segments, make_straight_wire, make_vertical_via
from forward.analytic import infinite_wire_x_field


def test_current_reversal_symmetry() -> None:
    grid = make_xy_grid(1e-3, 1e-3, 31, 31, 100e-6)
    seg_pos = make_straight_wire(10e-3, 1e-3, axis="x")
    seg_neg = make_straight_wire(10e-3, -1e-3, axis="x")
    B_pos = b_field_from_segments(grid.points, seg_pos)
    B_neg = b_field_from_segments(grid.points, seg_neg)
    assert np.max(np.abs(B_pos + B_neg)) < 1e-18


def test_long_wire_matches_infinite_reference_trend() -> None:
    grid = make_xy_grid(1e-3, 1e-3, 61, 61, 100e-6)
    B_num = b_field_from_segments(grid.points, make_straight_wire(50e-3, 1e-3, axis="x"))
    B_ref = infinite_wire_x_field(grid.points, current=1e-3)
    mask = (np.abs(grid.y) > 60e-6) & (np.abs(grid.x) < 0.2e-3)
    rel = np.linalg.norm(B_num[mask] - B_ref[mask]) / np.linalg.norm(B_ref[mask])
    assert rel < 0.02


def test_vertical_via_has_negligible_bz() -> None:
    grid = make_xy_grid(1e-3, 1e-3, 61, 61, 100e-6)
    B = b_field_from_segments(grid.points, make_vertical_via(-50e-6, 50e-6, 1e-3))
    max_bxy = np.max(np.sqrt(B[..., 0] ** 2 + B[..., 1] ** 2))
    max_bz = np.max(np.abs(B[..., 2]))
    assert max_bz / max_bxy < 1e-10


def test_reference_outputs_pass_acceptance_gates() -> None:
    metrics_path = ROOT / "outputs" / "metrics.json"
    assert metrics_path.exists()
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert metrics["all_acceptance_gates_passed"] is True
    assert (ROOT / "outputs" / "RUN_REPORT.md").exists()
