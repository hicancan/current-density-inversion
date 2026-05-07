"""Test end-to-end run for E23 round 5."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from layout_schema import load_layout, parse_layout
from graph_builder import build_graph, graph_summary
from incidence import build_incidence_matrix, build_source_vector
from hodge_basis import assemble_hodge_basis, validate_basis
from forward import build_centerline_operator
from oqci_adapter import run_oqci
from metrics import build_metrics
from layout_ensemble import generate_ensemble, portfolio_summary
from reporting import write_outputs


def _cfg():
    return {
        "seed": 20260506, "grid_size": 10, "sensor_z": 0.35,
        "source_current": 1.0, "kcl_residual_threshold": 1e-10,
        "current_closure_threshold": 1e-10, "basis_rank_tolerance": 1e-8,
        "oqci_epsilon": 0.1, "heights": [0.35, 0.70, 1.40],
        "hypotheses": ["H0_nominal", "H1_via_defect", "H2_return_bottleneck", "H3_bend_width_artifact"],
    }


def _run_layout(layout, cfg, name="test"):
    parsed = parse_layout(layout)
    graph = build_graph(parsed)
    D, no, eo = build_incidence_matrix(graph)
    q = build_source_vector(graph, no)
    hr = assemble_hodge_basis(graph, eo, D, q, cfg)
    v = validate_basis(hr, D, q, graph, cfg)
    A = build_centerline_operator(graph, eo, cfg["grid_size"], cfg["sensor_z"])
    oqci = run_oqci(graph, eo, D, hr, A, cfg)
    summary = graph_summary(graph)
    return {"layout_name": name, "summary": summary, "graph": graph, "valid": True,
            "hodge_result": hr, "validation": v, "oqci": oqci}


def test_ensemble_generates_44():
    layouts = generate_ensemble(n_layouts=44, seed=20260506)
    assert len(layouts) == 44
    s = portfolio_summary(layouts)
    assert s["total"] == 44
    assert s["multiport"] >= 30


def test_smoke_margin_matrix_present(tmp_path):
    layouts = generate_ensemble(n_layouts=2, seed=20260506)
    cfg = _cfg()
    results = [_run_layout(l, cfg, f"e{i}") for i, l in enumerate(layouts)]
    lps = [{"layout_name": r["layout_name"], "summary": r["summary"], "graph": r["graph"], "valid": r["valid"]} for r in results]
    m = build_metrics(lps, cfg, [r["hodge_result"] for r in results],
                      [r["oqci"] for r in results], [r["validation"] for r in results])
    assert "robust_margin" in m
    assert "min_gamma_all_pairs" in m["robust_margin"]
    assert "h1_h2_gamma_hardcase" in m["robust_margin"]


def test_round5_gates_present(tmp_path):
    layouts = generate_ensemble(n_layouts=2, seed=20260506)
    cfg = _cfg()
    results = [_run_layout(l, cfg, f"e{i}") for i, l in enumerate(layouts)]
    lps = [{"layout_name": r["layout_name"], "summary": r["summary"], "graph": r["graph"], "valid": r["valid"]} for r in results]
    m = build_metrics(lps, cfg, [r["hodge_result"] for r in results],
                      [r["oqci"] for r in results], [r["validation"] for r in results])
    for g in ["h1_h2_hardcase_gamma_positive", "h1_h2_gamma_positive_rate_ge_0_90",
              "critical_pair_certified_rate_ge_0_80", "greedy_port_states_beat_default",
              "greedy_port_states_beat_random", "adversarial_h1_h2_gamma_positive",
              "no_internal_actuation_needed"]:
        assert g in m["acceptance_gates"], f"Missing gate: {g}"


def test_robust_margin_outputs_written(tmp_path):
    layouts = generate_ensemble(n_layouts=1, seed=20260506)
    cfg = _cfg()
    r = _run_layout(layouts[0], cfg, "e0")
    lps = [{"layout_name": "e0", "summary": r["summary"], "graph": r["graph"], "valid": True}]
    m = build_metrics(lps, cfg, [r["hodge_result"]], [r["oqci"]], [r["validation"]])
    rd = {"layouts_processed": lps, "hodge_results": [r["hodge_result"]],
          "oqci_results": [r["oqci"]], "validation_results": [r["validation"]]}
    write_outputs(tmp_path, m, rd)
    for fname in ["ROBUST_MARGIN_MATRIX.md", "LAYOUT_ENSEMBLE_SCALING_AUDIT.md",
                  "GREEDY_PORT_EXCITATION_AUDIT.md", "ADVERSARIAL_OPERATOR_STRESS_AUDIT.md",
                  "ROUND5_ROBUST_CERTIFICATE_GATE_AUDIT.md"]:
        assert (tmp_path / fname).exists(), f"Missing: {fname}"


def test_greedy_excitation_present(tmp_path):
    layouts = generate_ensemble(n_layouts=1, seed=20260506)
    cfg = _cfg()
    r = _run_layout(layouts[0], cfg, "e0")
    ge = r["oqci"].get("greedy_excitation", {})
    assert "greedy_beats_default" in ge
    assert "states" in ge


def test_adversarial_stress_present(tmp_path):
    layouts = generate_ensemble(n_layouts=1, seed=20260506)
    cfg = _cfg()
    r = _run_layout(layouts[0], cfg, "e0")
    adv = r["oqci"].get("adversarial_stress", {})
    assert "worst_gamma" in adv
    assert "n_stress_configs" in adv
    assert adv["n_stress_configs"] > 0
