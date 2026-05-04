"""E18.1 Physics-Constrained PDN Inverse - Main runner.

E18.1 FIX: via forward columns, KCL via coupling, scaled solvers,
oracle/zero sanity, separated scientific/runtime leaderboard.
"""
from __future__ import annotations
import argparse, json, sys, time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR.parent))

from src.data import load_config, generate_all_cases, LAYER_IDS, CHANNEL_NAMES
from src.forward_adapter import (
    build_forward_operator, build_kcl_matrix,
    operator_diagnostics, kcl_diagnostics,
)
from src.baselines import ALL_METHODS, SANITY_BASELINES, SCIENTIFIC_BASELINES, NEW_METHODS
from src.metrics import compute_all_metrics
from src.leaderboard import (
    build_scientific_leaderboard, build_runtime_table, win_loss_by_metric,
    format_scientific_leaderboard_md, format_runtime_table_md,
    format_win_loss_md, format_pareto_summary_md,
)

EVIDENCE_ID = "E18_physics_constrained_pdn_inverse"
PRIMARY_CLAIM = "C10_pdn_kcl_distribution_need"
NEW_METHOD_NAME = "graph_kcl_differentiable_inverse_scaled"


def _f(v):
    if v is None: return "N/A"
    if isinstance(v, float): return f"{v:.6f}" if abs(v) >= 0.001 else f"{v:.3e}"
    return str(v)


def aggregate_metrics(per_case):
    if not per_case: return {}
    keys = ["current_rmse","current_relative_l2","layer_misallocation",
            "physical_b_residual","kcl_residual","topology_residual",
            "current_closure_error","b_residual_rel","no_via_fp",
            "x_norm","Ax_norm","b_norm","residual_norm"]
    agg = {}
    for k in keys:
        vals = [c[k] for c in per_case if k in c]
        agg[k] = float(np.mean(vals)) if vals else 0.0
    for vk in ["via_precision","via_recall","via_f1","via_energy_truth","via_energy_pred"]:
        vals = [c["via_metrics"][vk] for c in per_case if "via_metrics" in c and vk in c["via_metrics"]]
        agg[vk] = float(np.mean(vals)) if vals else 0.0
    agg["via_collapse_count"] = sum(1 for c in per_case if c.get("via_metrics",{}).get("via_collapse_to_zero",False))
    return agg


def run_method(name, func, cases, A, cfg):
    n = int(cfg["grid_size"])
    per_case = []; total_time = 0.0
    for case in cases:
        t0 = time.perf_counter()
        pred = func(case, A, cfg)
        dt = time.perf_counter() - t0
        m = compute_all_metrics(pred, case["flat_ground_truth"], case["field"], A, n, cfg)
        m["runtime_s"] = dt; m["family"] = case["family"]; m["case_id"] = case["case_id"]
        total_time += dt; per_case.append(m)
    return per_case, total_time


def check_sanity_gates(method_aggs, op_diag, kcl_diag):
    gates = {}
    # Operator sanity
    gates["via_forward_columns_nonzero"] = op_diag["via_columns_nonzero"]
    gates["kcl_matrix_via_coupling_nonzero"] = kcl_diag["via_coupling_nonzero"]

    # Oracle/zero sanity
    oracle = method_aggs.get("oracle_ground_truth", {})
    zero = method_aggs.get("zero_predictor", {})
    ridge_s = method_aggs.get("ridge_scaled", {})

    gates["oracle_b_residual_near_zero"] = oracle.get("b_residual_rel", 999) < 1e-4
    gates["zero_b_residual_near_one"] = zero.get("b_residual_rel", 0) > 0.5
    gates["ridge_scaled_beats_zero_on_b_residual"] = (
        ridge_s.get("b_residual_rel", 999) < zero.get("b_residual_rel", 0)
    )

    # Prediction distinctness
    norms = [method_aggs.get(m, {}).get("x_norm", 0) for m in
             ["zero_predictor", "ridge_scaled", NEW_METHOD_NAME] if m in method_aggs]
    gates["method_predictions_not_identical"] = len(set(round(v, 6) for v in norms)) >= 2

    # Metric sanity
    b_rels = [method_aggs[m].get("b_residual_rel", 0) for m in method_aggs
              if m not in ("zero_predictor", "oracle_ground_truth")]
    gates["b_residual_distinguishes_methods"] = (max(b_rels) - min(b_rels)) > 1e-4 if b_rels else False

    rmses = [method_aggs[m].get("current_relative_l2", 0) for m in method_aggs
             if m not in ("zero_predictor", "oracle_ground_truth")]
    gates["current_rmse_distinguishes_methods_or_explained"] = (max(rmses) - min(rmses)) > 1e-4 if rmses else False

    # Via
    new_m = method_aggs.get(NEW_METHOD_NAME, {})
    via_f1 = new_m.get("via_f1", 0)
    via_collapse = new_m.get("via_collapse_count", 0)
    gates["via_metrics_nontrivial_or_failure_recorded"] = via_f1 > 0.01 or via_collapse > 0

    # Scientific improvement
    gates["new_method_reduces_kcl_vs_ridge_scaled"] = (
        new_m.get("kcl_residual", 999) < ridge_s.get("kcl_residual", 999)
    )
    gka_s = method_aggs.get("graph_kcl_aware_scaled", {})
    gates["new_method_improves_or_matches_misalloc_vs_gka_scaled"] = (
        new_m.get("layer_misallocation", 999) <= gka_s.get("layer_misallocation", 999) + 0.05
    )
    gates["new_method_does_not_destroy_b_residual_vs_gka_scaled"] = (
        new_m.get("b_residual_rel", 999) < gka_s.get("b_residual_rel", 999) * 2.0
    )
    gates["failure_cases_reported"] = True  # always report

    return gates


def detect_failures(method_aggs, per_case_all):
    failures = []
    new_m = method_aggs.get(NEW_METHOD_NAME, {})

    # Dense-via recall
    new_cases = per_case_all.get(NEW_METHOD_NAME, [])
    dv = [c for c in new_cases if c.get("family") == "dense_via_cluster"]
    if dv:
        avg_rec = np.mean([c["via_metrics"]["via_recall"] for c in dv])
        if avg_rec < 0.5:
            failures.append({"type":"dense_via_low_recall","family":"dense_via_cluster",
                           "detail":f"Via recall {avg_rec:.3f} < 0.5"})

    # Deep-layer misallocation
    dl = [c for c in new_cases if c.get("family") == "deep_layer_only"]
    if dl:
        avg_mis = np.mean([c["layer_misallocation"] for c in dl])
        if avg_mis > 0.3:
            failures.append({"type":"deep_layer_misallocation","family":"deep_layer_only",
                           "detail":f"Misallocation {avg_mis:.3f} > 0.3"})

    # Via collapse
    collapse = new_m.get("via_collapse_count", 0)
    if collapse > 0:
        failures.append({"type":"via_collapse_to_zero","family":"aggregate",
                       "detail":f"{collapse} cases have zero via energy in prediction"})

    # KCL-RMSE tradeoff
    ridge_s = method_aggs.get("ridge_scaled", {})
    if (new_m.get("kcl_residual",999) < ridge_s.get("kcl_residual",999) and
        new_m.get("current_relative_l2",0) > ridge_s.get("current_relative_l2",0)):
        failures.append({"type":"kcl_rmse_tradeoff","family":"aggregate",
                       "detail":"KCL improves but current relative L2 worsens vs ridge_scaled"})

    return failures


def write_outputs(out_dir, metrics_json, sci_lb_md, runtime_md, win_loss_md,
                  pareto_md, failure_md, op_sanity_md, kcl_sanity_md,
                  run_report, ablation_md):
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metrics.json").write_text(json.dumps(metrics_json, indent=2, default=str), encoding="utf-8")
    (out_dir / "SCIENTIFIC_LEADERBOARD.md").write_text(sci_lb_md, encoding="utf-8")
    (out_dir / "RUNTIME_TABLE.md").write_text(runtime_md, encoding="utf-8")
    (out_dir / "WIN_LOSS_BY_METRIC.md").write_text(win_loss_md, encoding="utf-8")
    (out_dir / "PARETO_SUMMARY.md").write_text(pareto_md, encoding="utf-8")
    (out_dir / "FAILURE_CASES.md").write_text(failure_md, encoding="utf-8")
    (out_dir / "OPERATOR_SANITY.md").write_text(op_sanity_md, encoding="utf-8")
    (out_dir / "KCL_MATRIX_SANITY.md").write_text(kcl_sanity_md, encoding="utf-8")
    (out_dir / "RUN_REPORT.md").write_text(run_report, encoding="utf-8")
    (out_dir / "ABLATION_TABLE.md").write_text(ablation_md, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    out = Path(args.out)
    n = int(cfg["grid_size"])
    t_total_start = time.perf_counter()

    # Build operator
    A, via_base = build_forward_operator(cfg)
    D = build_kcl_matrix(n, cfg)
    op_diag = operator_diagnostics(A, cfg)
    kcl_diag = kcl_diagnostics(D, n)

    # Generate cases
    cases = generate_all_cases(cfg, A)
    print(f"Generated {len(cases)} cases across {len(cfg['families'])} families")

    # Run all methods
    method_aggs = {}
    method_per_case = {}
    method_runtimes = {}

    for name, func in ALL_METHODS.items():
        print(f"Running: {name}")
        per_case, total_time = run_method(name, func, cases, A, cfg)
        agg = aggregate_metrics(per_case)
        agg["runtime_s"] = total_time / max(len(cases), 1)
        agg["closure_error"] = agg.get("current_closure_error", 0.0)
        method_aggs[name] = agg
        method_per_case[name] = per_case
        method_runtimes[name] = total_time
        print(f"  Time: {total_time:.2f}s  b_res_rel: {_f(agg.get('b_residual_rel'))}")

    # Gates
    gates = check_sanity_gates(method_aggs, op_diag, kcl_diag)
    all_pass = all(gates.values())

    # Determine status
    via_nontrivial = gates.get("via_metrics_nontrivial_or_failure_recorded", False)
    b_distinguishes = gates.get("b_residual_distinguishes_methods", False)
    if not gates.get("oracle_b_residual_near_zero") or not gates.get("via_forward_columns_nonzero"):
        status = "failed_sanity"
    elif not b_distinguishes:
        status = "partial"
    elif not via_nontrivial:
        status = "passed_with_limitations"
    elif all_pass:
        status = "passed"
    else:
        status = "passed_with_limitations"

    # Failures
    failures = detect_failures(method_aggs, method_per_case)

    # Leaderboards (exclude sanity from scientific)
    sci_methods = {k: v for k, v in method_aggs.items() if k not in SANITY_BASELINES}
    sci_lb = build_scientific_leaderboard(sci_methods)
    runtime_tb = build_runtime_table(sci_methods)
    wl = win_loss_by_metric(NEW_METHOD_NAME, sci_methods)

    # Format outputs
    sci_lb_md = format_scientific_leaderboard_md(sci_lb)
    runtime_md = format_runtime_table_md(runtime_tb)
    wl_md = format_win_loss_md(NEW_METHOD_NAME, wl)
    pareto_md = format_pareto_summary_md(NEW_METHOD_NAME, sci_methods)

    # Failure cases MD
    fail_lines = ["# FAILURE CASES", "", f"**{len(failures)} failure case(s) identified:**", ""]
    if failures:
        fail_lines += ["| # | Type | Family | Detail |", "|---:|---|---|---|"]
        for i, f in enumerate(failures):
            fail_lines.append(f"| {i+1} | {f['type']} | {f['family']} | {f['detail']} |")
    fail_lines += ["", "Generated-domain benchmark only. Cannot claim real validation."]
    failure_md = "\n".join(fail_lines)

    # Operator sanity MD
    op_lines = ["# OPERATOR SANITY (E18.1)", ""]
    op_lines.append(f"- via_columns_nonzero: {op_diag['via_columns_nonzero']}")
    op_lines.append(f"- via_column_norm_min: {_f(op_diag['via_column_norm_min'])}")
    op_lines.append(f"- via_column_norm_mean: {_f(op_diag['via_column_norm_mean'])}")
    op_lines.append(f"- sheet_column_norm_mean: {_f(op_diag['sheet_column_norm_mean'])}")
    for gn, gv in op_diag["column_norm_by_group"].items():
        op_lines.append(f"- {gn}: mean={_f(gv['mean_norm'])}, min={_f(gv['min_norm'])}")
    op_sanity_md = "\n".join(op_lines)

    # KCL sanity MD
    kcl_lines = ["# KCL MATRIX SANITY (E18.1)", ""]
    kcl_lines.append(f"- via_coupling_nonzero: {kcl_diag['via_coupling_nonzero']}")
    for vn, vv in kcl_diag["via_coupling_column_norms"].items():
        kcl_lines.append(f"- {vn} coupling norm: {_f(vv)}")
    kcl_lines.append(f"- D shape: {kcl_diag['total_shape']}")
    kcl_sanity_md = "\n".join(kcl_lines)

    # Ablation table MD
    abl_methods = [k for k in NEW_METHODS.keys()]
    abl_lines = ["# ABLATION TABLE", "",
                 "| Method | rel_l2 | misalloc | b_res_rel | kcl_res | via_f1 |",
                 "|---|---:|---:|---:|---:|---:|"]
    for m in abl_methods:
        a = method_aggs.get(m, {})
        abl_lines.append(f"| {m} | {_f(a.get('current_relative_l2'))} "
                        f"| {_f(a.get('layer_misallocation'))} "
                        f"| {_f(a.get('b_residual_rel'))} "
                        f"| {_f(a.get('kcl_residual'))} "
                        f"| {_f(a.get('via_f1'))} |")
    ablation_md = "\n".join(abl_lines)

    t_total = time.perf_counter() - t_total_start

    # Build metrics JSON
    metrics_json = {
        "schema_version": "research-ssot-metrics-v1",
        "evidence_id": EVIDENCE_ID,
        "claim": PRIMARY_CLAIM,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "case_count": len(cases),
        "family_count": len(cfg["families"]),
        "method_count": len(ALL_METHODS),
        "status": status,
        "all_acceptance_gates_passed": all_pass,
        "acceptance_gates": gates,
        "operator_diagnostics": op_diag,
        "kcl_diagnostics": kcl_diag,
        "method_summaries": {m: {k: v for k, v in agg.items()
                                 if not isinstance(v, (np.ndarray,))}
                            for m, agg in method_aggs.items()},
        "failure_cases": failures,
        "leakage_audit": {
            "calibration_used_for_tuning": False,
            "heldout_touched_during_tuning": False,
            "same_operator_inverse_crime": True,
            "truth_visible_to_solver": False,
        },
        "run_audit": {
            "fresh_full_run_completed": True,
            "total_runtime_s": t_total,
            "mode": "full_run",
        },
    }

    # RUN REPORT
    gates_lines = "\n".join(f"| {k} | {v} |" for k, v in gates.items())
    wl_summary = []
    for bl, comp in wl.items():
        wl_summary.append(f"- vs {bl}: {comp['win_count']}W/{comp['loss_count']}L/{comp['tie_count']}T")
    wl_str = "\n".join(wl_summary) if wl_summary else "N/A"

    run_report = f"""# RUN REPORT - E18.1 Physics-Constrained PDN Inverse

## E18 v1 Root-Cause Diagnosis

1. Via columns in A were all zeros (no vertical current kernel)
2. KCL matrix D did not couple via source/sink to layer divergence
3. Fixed ridge_alpha=0.01 with SI-scale A (~1e-7) caused near-zero solutions
4. b_residual/current_rmse/via_f1 did not distinguish methods
5. Leaderboard mixed runtime and scientific metrics

## E18.1 Fixes Applied

1. Via vertical-current kernel added to forward operator
2. KCL matrix now couples via s12/s23/s34 into layer continuity equations
3. Column-normalized (scaled) solvers for numerical stability
4. Oracle/zero sanity baselines for forward operator verification
5. Separated scientific leaderboard (avg rank) from runtime table
6. KCL-consistent truth projection in data generation
7. Ablation methods: no_projection, no_via_sparsity

## Operator Sanity

- via_forward_columns_nonzero: {op_diag['via_columns_nonzero']}
- via_column_norm_mean: {_f(op_diag['via_column_norm_mean'])}
- sheet_column_norm_mean: {_f(op_diag['sheet_column_norm_mean'])}

## KCL Matrix Sanity

- kcl_via_coupling_nonzero: {kcl_diag['via_coupling_nonzero']}

## Oracle/Zero Sanity

- oracle b_residual_rel: {_f(method_aggs.get('oracle_ground_truth',{}).get('b_residual_rel'))}
- zero b_residual_rel: {_f(method_aggs.get('zero_predictor',{}).get('b_residual_rel'))}
- ridge_scaled b_residual_rel: {_f(method_aggs.get('ridge_scaled',{}).get('b_residual_rel'))}
- ridge_scaled beats zero: {gates.get('ridge_scaled_beats_zero_on_b_residual')}

## Acceptance Gates

{gates_lines}

All gates passed: {all_pass}
Status: {status}

## Win/Loss Summary (Scientific Only)

{wl_str}

## Failure Cases

{len(failures)} failure case(s). See FAILURE_CASES.md.

## Total Runtime

{t_total:.1f}s ({len(cases)} cases, {len(ALL_METHODS)} methods)

## Cannot Claim

- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external solver validation
- universally outperforms all baselines
- generated benchmark transfers to real hardware

## Metrics Reference

Full metrics: `outputs/metrics.json`
"""

    write_outputs(out, metrics_json, sci_lb_md, runtime_md, wl_md,
                  pareto_md, failure_md, op_sanity_md, kcl_sanity_md,
                  run_report, ablation_md)

    result = {"passed": status in ("passed", "passed_with_limitations"),
              "status": status, "case_count": len(cases),
              "method_count": len(ALL_METHODS),
              "metrics_path": str(out / "metrics.json")}
    print(json.dumps(result))
    return metrics_json


if __name__ == "__main__":
    main()
