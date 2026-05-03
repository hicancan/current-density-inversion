from __future__ import annotations

import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
for prefix in ["forward", "geometry", "detection"]:
    for name in list(sys.modules):
        if name == prefix or name.startswith(prefix + "."):
            del sys.modules[name]
sys.path.insert(0, str(ROOT / "src"))

from forward.segments import make_grid, field_from_segments, group_field, rel_l2, Segment
from geometry.toy_circuit import build_two_layer_via_segments, finite_volume_route_maps
from detection.matched_filter import normalized_template_score, peak_location


def load_cfg():
    with open(ROOT / "configs" / "default.json", "r", encoding="utf-8") as f:
        return json.load(f)


def test_superposition_and_current_reversal():
    cfg = load_cfg()
    g, p = cfg["grid"], cfg["physics"]
    X, Y, Z = make_grid(g["fov_m"], 41, g["sensor_z_m"])
    segs = build_two_layer_via_segments(p["current_A"], p["layer1_z_m"], p["layer2_z_m"], p["via_x_m"], p["via_y_m"], p["left_port_x_m"], p["right_port_x_m"], p["route_y_m"])
    B = field_from_segments(X, Y, Z, segs, n_quad=40)
    Bsum = sum(group_field(X, Y, Z, segs, group, n_quad=40) for group in ["layer1", "layer2", "via"])
    assert rel_l2(B, Bsum) < 1e-12
    segs_neg = [Segment(s.p0, s.p1, -s.I_A, s.name, s.group) for s in segs]
    Bneg = field_from_segments(X, Y, Z, segs_neg, n_quad=40)
    assert np.max(np.abs(B + Bneg)) / (np.max(np.abs(B)) + 1e-30) < 1e-12


def test_via_bz_is_zero_for_vertical_segment():
    cfg = load_cfg()
    g, p = cfg["grid"], cfg["physics"]
    X, Y, Z = make_grid(g["fov_m"], 61, g["sensor_z_m"])
    via = Segment((0, 0, p["layer1_z_m"]), (0, 0, p["layer2_z_m"]), p["current_A"], "via", "via")
    B = field_from_segments(X, Y, Z, [via], n_quad=80)
    assert np.max(np.abs(B[..., 2])) < 1e-18
    assert np.max(np.sqrt(B[..., 0] ** 2 + B[..., 1] ** 2)) > 0


def test_topology_residual_cancels_internal_via():
    cfg = load_cfg()
    g, p = cfg["grid"], cfg["physics"]
    maps = finite_volume_route_maps(g["fov_m"], 65, p["current_A"], p["via_x_m"], p["via_y_m"], p["left_port_x_m"], p["right_port_x_m"], p["route_y_m"])
    inner = maps["inner_mask"]
    assert np.linalg.norm(maps["res1"][inner]) < 1e-12
    assert np.linalg.norm(maps["res2"][inner]) < 1e-12


def test_residual_template_localizes_via():
    cfg = load_cfg()
    g, p = cfg["grid"], cfg["physics"]
    X, Y, Z = make_grid(g["fov_m"], 65, g["sensor_z_m"])
    x, y = X[0, :], Y[:, 0]
    segs = build_two_layer_via_segments(p["current_A"], p["layer1_z_m"], p["layer2_z_m"], p["via_x_m"], p["via_y_m"], p["left_port_x_m"], p["right_port_x_m"], p["route_y_m"])
    B_total = field_from_segments(X, Y, Z, segs, n_quad=50)
    B_l1 = group_field(X, Y, Z, segs, "layer1", n_quad=50)
    B_l2 = group_field(X, Y, Z, segs, "layer2", n_quad=50)
    residual = B_total - B_l1 - B_l2
    templ = field_from_segments(X, Y, Z, [Segment((0, 0, p["layer1_z_m"]), (0, 0, p["layer2_z_m"]), p["current_A"], "via", "via")], n_quad=50)
    score = normalized_template_score(residual[..., :2], templ[..., :2])
    peak = peak_location(score, x, y)
    err = np.hypot(peak["x_m"] - p["via_x_m"], peak["y_m"] - p["via_y_m"])
    assert err <= (x[1] - x[0]) * 1.5


def test_reference_outputs_pass_acceptance_gates():
    metrics_path = ROOT / "outputs" / "metrics.json"
    assert metrics_path.exists()
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert metrics["all_acceptance_gates_passed"] is True
    stress = metrics["background_swamping_stress"]
    assert stress["residual_localization_error_m"] < stress["raw_localization_error_m"]
    bench = metrics["benchmark_dataset"]
    assert bench["truth_shape"][1] == 5
    assert all(bench["split_counts"][k] > 0 for k in ["train", "val", "test", "ood"])
    assert bench["truth_channel_l2_norms_by_split"]["test"]["J1y"] > 0
    assert bench["truth_channel_l2_norms_by_split"]["test"]["J2y"] > 0
    assert all(bench["route_kind_counts"]["test"][k] > 0 for k in ["straight", "l1_jog", "l2_jog", "both_jog", "multi_via", "no_via"])
    assert all(bench["route_kind_counts"]["ood"][k] > 0 for k in ["both_jog_background", "dense_via_background", "no_via_background"])
    assert bench["recoverability_summary"]["test"]["no_via_fraction"] > 0
    assert metrics["forward_realism_probe"]["median_rel_l2_gap"] > 0.01
    assert metrics["acceptance_gates"]["finite_width_return_surrogate_gap_is_quantified"]["pass"]
    assert (ROOT / bench["file"]).exists()
    assert (ROOT / "outputs" / "RUN_REPORT.md").exists()
