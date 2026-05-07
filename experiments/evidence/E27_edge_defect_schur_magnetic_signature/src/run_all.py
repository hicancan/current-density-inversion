"""Run E27 Edge-Defect Schur Magnetic Signature Inversion evidence."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from baselines import (
    run_all_baselines,
    to_summary_dict,
    compute_pairwise_defect_delta,
    compute_pairwise_defect_gamma,
)
from config import load_config
from data import generate_cases, compute_sherman_morrison_validation_error
from metrics import (
    compute_design_improvement,
    compute_consistent_sets,
    per_family_edge_gamma,
    engineering_gates,
    scientific_gates,
    compute_pairwise_summary,
)
from operators import (
    build_operator,
    operator_diagnostics,
    build_candidate_defects,
    compute_edge_signal,
    solve_potential,
)
from reporting import write_outputs

EVIDENCE_ID = "E27_edge_defect_schur_magnetic_signature"
PRIMARY_CLAIM = "C06_graph_hypothesis_system_identification"
SECONDARY_CLAIMS = [
    "C02_single_plane_identifiability_boundary",
    "C10_pdn_kcl_distribution_need",
    "C13_calibration_protocol_reality",
]


def main(argv: list[str] | None = None) -> dict:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Path to config JSON")
    parser.add_argument("--out", required=True, help="Output directory")
    args = parser.parse_args(argv)

    t0 = time.perf_counter()
    cfg = load_config(args.config)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Build operator
    bundle = build_operator(cfg)
    op_diag = operator_diagnostics(bundle)

    # 2. Build candidate defects
    candidates = build_candidate_defects(bundle, cfg)

    # 3. Generate cases (truth defects with ground-truth signatures)
    cases = generate_cases(bundle, cfg, candidates)

    # 4. Validate Sherman-Morrison against direct solve
    sm_errors = []
    for case in cases[:min(10, len(cases))]:
        err = compute_sherman_morrison_validation_error(
            bundle, case.phi_baseline, case.truth_defect
        )
        sm_errors.append(err)

    # 5. Run all baselines (Schur + comparators)
    W = None  # Uniform weighting for generated domain
    baseline_results = run_all_baselines(bundle, candidates, cfg, W)

    # 6. Extract Schur result
    schur_result = None
    for br in baseline_results:
        if br.strategy == "schur_voltage_drop":
            schur_result = br
            break

    if schur_result is None:
        raise RuntimeError("Schur voltage-drop strategy not found in baseline results")

    # 7. Compute improvement over baselines
    improvement = compute_design_improvement(schur_result, baseline_results)

    # 8. Compute pairwise defect Gamma matrix
    pairwise_summary = compute_pairwise_summary(
        bundle, candidates, schur_result.states, cfg, W
    )

    # 9. Compute consistent-set metrics
    consistent = compute_consistent_sets(candidates, schur_result, cfg)

    # 10. Per-family edge Gamma
    per_family = per_family_edge_gamma(candidates, schur_result)

    # 11. Baseline summaries
    baseline_summaries = [to_summary_dict(br) for br in baseline_results]

    # 12. Compute acceptance gates
    eng_gates = engineering_gates(
        {
            "candidate_defect_count": len(candidates),
            "families": cfg["families"],
            "schur_state_count": len(schur_result.states),
            "baseline_strategy_count": len(baseline_results),
        },
        op_diag,
        sm_errors,
        len(cases),
    )

    # Compute pairwise-specific gate (positive pairwise gamma rate)
    sci_gates = scientific_gates(improvement, schur_result, consistent, per_family, pairwise_summary)

    eng_passed = all(eng_gates.values())
    sci_passed = all(sci_gates.values())

    if not eng_passed:
        status = "failed_sanity"
    elif not sci_passed:
        status = "passed_with_limitations"
    else:
        status = "passed"

    gates = {**eng_gates, **sci_gates}
    elapsed = time.perf_counter() - t0

    # 13. Build canonical metrics
    metrics = {
        "schema_version": "research-ssot-metrics-v1",
        "evidence_id": EVIDENCE_ID,
        "claim": PRIMARY_CLAIM,
        "secondary_claims": SECONDARY_CLAIMS,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "engineering_gates_passed": eng_passed,
        "scientific_gates_passed": sci_passed,
        "all_acceptance_gates_passed": eng_passed and sci_passed,
        "engineering_gates": eng_gates,
        "scientific_gates": sci_gates,
        "acceptance_gates": gates,
        "operator_diagnostics": op_diag,
        "config": {
            "grid_size": int(cfg["grid_size"]),
            "layer_count": int(cfg["layer_count"]),
            "noise_sigma": float(cfg["noise_sigma"]),
            "case_count_per_family": int(cfg["case_count_per_family"]),
            "families": list(cfg["families"]),
            "candidate_defect_families": list(cfg["candidate_defect_families"]),
            "schur_state_count": int(cfg["schur"]["state_count"]),
        },
        "sherman_morrison_max_error": float(max(sm_errors)) if sm_errors else 0.0,
        "sherman_morrison_mean_error": float(sum(sm_errors) / len(sm_errors)) if sm_errors else 0.0,
        "sherman_morrison_valid": bool(max(sm_errors) < 1e-8) if sm_errors else False,
        "candidate_edge_sensitivity": {
            "candidate_defect_count": len(candidates),
            "families_covered": len(set(d.family for d in candidates)),
            "mean_edge_signal": float(schur_result.mean_signal),
            "mean_edge_gamma": float(schur_result.mean_gamma),
            "positive_edge_gamma_rate": float(schur_result.positive_gamma_rate),
        },
        "schur_state_info": {
            "state_count": len(schur_result.states),
            "mean_signal": float(schur_result.mean_signal),
            "mean_gamma": float(schur_result.mean_gamma),
            "positive_gamma_rate": float(schur_result.positive_gamma_rate),
        },
        "signal_gamma_improvement": improvement,
        "baseline_summaries": baseline_summaries,
        "pairwise_gamma_summary": pairwise_summary,
        "per_family_edge_gamma": per_family,
        "consistent_set_metrics": consistent,
        "leakage_audit": {
            "generated_domain_only": True,
            "heldout_rows_used_for_tuning": False,
            "hidden_rows_used_for_tuning": False,
            "external_or_real_rows_used": False,
            "truth_visible_to_inference": False,
            "blueprint_text_used_as_evidence": False,
        },
        "run_audit": {
            "fresh_full_run_completed": True,
            "runtime_s": float(elapsed),
            "command": "python src/run_all.py --config <config> --out <out>",
        },
        "cannot_claim": [
            "real QDM/NV validation",
            "real CAD/Gerber/GDS validation",
            "external FEM/FastHenry/COMSOL validation",
            "real-board PDN/KCL robustness",
            "Schur minimax with hardware port constraints (current limits, pad positions)",
            "universal edge-defect detection",
            "finite-width conductor corrections (multifilament)",
            "multi-height sensor validation",
            "generated-domain evidence transfers to real hardware",
        ],
    }

    # 14. Write outputs
    write_outputs(
        out_dir, metrics, cases, candidates,
        schur_result, baseline_results, sm_errors,
        gates, pairwise_summary, consistent, per_family, bundle,
    )

    # 15. Print machine-readable summary
    print(json.dumps({
        "evidence_id": EVIDENCE_ID,
        "case_count": len(cases),
        "defect_count": len(candidates),
        "status": metrics["status"],
        "all_acceptance_gates_passed": metrics["all_acceptance_gates_passed"],
        "metrics_path": str(out_dir / "metrics.json"),
        "runtime_s": elapsed,
    }, indent=2))
    return metrics


if __name__ == "__main__":
    main()
