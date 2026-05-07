"""Reporting for E23 round 5."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any


def write_outputs(d: Path, m: dict, r: dict) -> None:
    d.mkdir(parents=True, exist_ok=True)
    _j(d / "metrics.json", m)
    _run(d / "RUN_REPORT.md", m)
    _margin(d / "ROBUST_MARGIN_MATRIX.md", m, r)
    _ens(d / "LAYOUT_ENSEMBLE_SCALING_AUDIT.md", m)
    _gr(d / "GREEDY_PORT_EXCITATION_AUDIT.md", m, r)
    _adv(d / "ADVERSARIAL_OPERATOR_STRESS_AUDIT.md", m)
    _ga(d / "ROUND5_ROBUST_CERTIFICATE_GATE_AUDIT.md", m)
    for fn in ["SVD_NULLSPACE_PROJECTION.md", "HODGE_BASIS_AUDIT.md",
               "KCL_CLOSURE_AUDIT.md", "FAILURE_MODES.md"]:
        _j(d / fn, m.get("kcl", {}))


def _j(p, o): p.write_text(json.dumps(o, indent=2, ensure_ascii=False), encoding="utf-8")


def _run(p, m):
    rm = m["robust_margin"]; adv = m["adversarial_stress"]
    L = [f"# E23 R5 Run\nStatus: {m['status']}\nLayouts: {m['layout']['layout_count']} mp={m['layout']['multiport_count']}",
         f"min_gamma_all={rm['min_gamma_all_pairs']:.4f} min_gamma_crit={rm['min_gamma_critical_pairs']:.4f}",
         f"H1/H2 gamma={rm['h1_h2_gamma_hardcase']:.4f} cert_rate={rm['certified_pair_rate']:.3f}",
         f"Adv worst gamma={adv['worst_gamma']:.4f} pos={adv['gamma_positive']}", "## Gates"]
    for g, ok in m["acceptance_gates"].items():
        L.append(f"- [{'PASS' if ok else 'FAIL'}] {g}")
    L.append(f"\nAll: {m['all_acceptance_gates_passed']}")
    p.write_text("\n".join(L), encoding="utf-8")


def _margin(p, m, r):
    rm = m["robust_margin"]
    oqci = (r.get("oqci_results", [{}]) or [{}])[0]
    margins = oqci.get("robust_margins", {}).get("margin_matrix", {})
    L = ["# E23 Robust Margin Matrix",
         f"min_gamma_all={rm['min_gamma_all_pairs']:.4f} min_gamma_crit={rm['min_gamma_critical_pairs']:.4f}",
         f"H1/H2 gamma={rm['h1_h2_gamma_hardcase']:.4f} cert_rate={rm['certified_pair_rate']:.3f}"]
    h1h2 = margins.get("H1_via_defect_vs_H2_return_bottleneck", {})
    if h1h2:
        L += [f"H1/H2 delta={h1h2.get('delta_pair',0):.4f} rho_h={h1h2.get('rho_h',0):.4f} rho_g={h1h2.get('rho_g',0):.4f}",
              f"H1/H2 gamma={h1h2.get('gamma_pair',0):.4f} positive={h1h2.get('gamma_positive',False)}"]
    p.write_text("\n".join(L), encoding="utf-8")


def _ens(p, m):
    p.write_text(f"# Ensemble Audit\nLayouts: {m['layout']['layout_count']}\nMultiport: {m['layout']['multiport_count']}\n", encoding="utf-8")


def _gr(p, m, r):
    oqci = (r.get("oqci_results", [{}]) or [{}])[0]
    ge = oqci.get("greedy_excitation", {})
    L = ["# Greedy Port Excitation",
         f"beats_default={ge.get('greedy_beats_default')} beats_random={ge.get('greedy_beats_random')}",
         f"default_gamma={ge.get('default_min_gamma',0):.4f} greedy_gamma={ge.get('greedy_min_gamma',0):.4f}",
         f"states={ge.get('states',[])}"]
    p.write_text("\n".join(L), encoding="utf-8")


def _adv(p, m):
    adv = m["adversarial_stress"]
    L = [f"# Adversarial Stress\nworst_gamma={adv['worst_gamma']:.4f} positive={adv['gamma_positive']}"]
    p.write_text("\n".join(L), encoding="utf-8")


def _ga(p, m):
    L = ["# R5 Gate Audit"]
    for g, ok in m["acceptance_gates"].items():
        L.append(f"- [{'PASS' if ok else 'FAIL'}] {g}")
    L.append(f"\nAll: {m['all_acceptance_gates_passed']}")
    p.write_text("\n".join(L), encoding="utf-8")
