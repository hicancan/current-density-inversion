"""Run E20 Active OQCI (Round 5): pairwise-margin active measurement design."""

from __future__ import annotations

import argparse
import json
import numpy as np
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from config import load_config
from operators import multi_height_operator_stack, operator_diagnostics
from data_adapter import generate_cases
from hypotheses import build_all_hypothesis_bases, HYPOTHESES
from oqci_core import (
    consistent_set_for_case, compute_epsilon_from_policy,
    run_consistent_set_analysis,
)
from intervals import aggregate_claim_intervals
from distances import pairwise_distinguishability
from nullspace import near_null_modes
from resolution import resolution_diagnostics
from candidates import build_candidate_pool, evaluate_candidate
from pairwise_margin import compute_pairwise_margins, compute_pairwise_margin_gain
from policies import (
    compare_acquisition_policies, greedy_two_step_design,
)
from utility import rank_candidates
from metrics import build_metrics
from reporting import (
    write_metrics_json, write_run_report, write_candidate_ranking,
    write_epsilon_sweep, write_epsilon_candidate_matrix,
    write_ambiguity_reduction, write_claim_intervals_before_after,
    write_near_null_before_after, write_next_measurement_policy,
    write_failure_modes,
    write_truth_coverage_audit, write_valid_disambiguation_matrix,
    write_breakthrough_gate_audit,
    write_regularized_consistent_set_audit, write_epsilon_calibration_audit,
    write_regularization_breakthrough_gate_audit,
    write_pairwise_margin_matrix_report, write_active_policy_comparison,
    write_two_step_active_design_audit, write_round5_pairwise_margin_gate_audit,
)

EVIDENCE_ID = "E20_active_oqci_measurement_design"
PRIMARY_CLAIM = "C10_pdn_kcl_distribution_need"
SECONDARY_CLAIMS = [
    "C02_single_plane_identifiability_boundary",
    "C04_inverse_crime_and_operator_gap",
    "C06_graph_hypothesis_system_identification",
    "C13_calibration_protocol_reality",
]


def main(argv: list[str] | None = None) -> dict:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    t0 = time.perf_counter()
    cfg = load_config(args.config)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    baseline_heights = [float(h) for h in cfg["sensor_heights_um"]]

    # 1. Build baseline operator (E0)
    bundle = multi_height_operator_stack(cfg)
    op_diag = operator_diagnostics(bundle)

    # 2. Build hypothesis bases
    bases = build_all_hypothesis_bases(bundle, cfg)

    # 3. Generate cases
    cases = generate_cases(bundle, cfg)

    # 4. Baseline OQCI
    sigma = float(cfg["noise_sigma"]); obs_dim = bundle.A.shape[0]
    eps_values = compute_epsilon_from_policy(sigma, obs_dim, cfg["epsilon_policy"])
    primary_eps = eps_values[0] if eps_values else 0.0

    baseline_oqci = run_consistent_set_analysis(cases, bundle, bases, cfg)
    per_case = []
    for case in cases:
        r = consistent_set_for_case(case, bundle, bases, primary_eps)
        per_case.append({"case_id": r.case_id, "truth": r.truth_hypothesis,
            "consistent_hypotheses": r.consistent_hypotheses,
            "non_consistent_hypotheses": r.non_consistent_hypotheses})
    baseline_oqci["per_case"] = per_case

    # 5. Baseline intervals, pairwise, nullspace, and margins
    all_results = [consistent_set_for_case(case, bundle, bases, primary_eps) for case in cases]
    baseline_intervals = aggregate_claim_intervals(all_results)
    baseline_pairwise_dists = pairwise_distinguishability(bases, bundle, cases)
    baseline_nullspace = near_null_modes(bundle, bases, float(cfg["nullspace_threshold"]))

    # Baseline pairwise margins
    eps_margin = sigma * np.sqrt(obs_dim)
    baseline_margins = compute_pairwise_margins(bases, bundle, eps_margin)

    # 6. Build candidate pool
    candidates = build_candidate_pool(cfg)
    print(f"Candidate pool: {len(candidates)} candidates")

    # 7. Evaluate each candidate
    candidate_results = []
    for i, cand in enumerate(candidates):
        print(f"  Evaluating {i+1}/{len(candidates)}: {cand.candidate_id} "
              f"(h={cand.height_um}, comp={cand.components}, states={cand.n_states}) ...")
        result = evaluate_candidate(
            cfg, all_results, baseline_heights,
            baseline_oqci, baseline_nullspace, baseline_pairwise_dists,
            cand,
        )
        # Recompute pairwise margin using actual baseline bases for proper comparison
        pm_gain = compute_pairwise_margin_gain(
            baseline_bases=bases,
            candidate_bases=build_all_hypothesis_bases(build_from_candidate(cfg, cand, baseline_heights), cfg),
            baseline_bundle=bundle,
            candidate_bundle=build_from_candidate(cfg, cand, baseline_heights),
            epsilon=eps_margin,
        )
        pm_gain["candidate_id"] = cand.candidate_id
        result["pairwise_margin"] = pm_gain
        candidate_results.append(result)

    # 8. Policy comparison
    policy_comparison = compare_acquisition_policies(
        bases, bundle, candidate_results, eps_margin)

    # 9. Two-step design
    two_step = greedy_two_step_design(
        bases, bundle, candidate_results, eps_margin)

    # 10. Rank candidates
    ranking = rank_candidates(
        baseline_oqci, baseline_nullspace, baseline_pairwise_dists,
        candidate_results, cfg["utility_weights"],
    )

    # 11. Resolution
    resolution = resolution_diagnostics(bundle)

    # 12. Build metrics
    elapsed = time.perf_counter() - t0
    metrics = build_metrics(
        cfg=cfg, baseline_oqci=baseline_oqci,
        baseline_nullspace=baseline_nullspace,
        baseline_pairwise=baseline_pairwise_dists,
        baseline_intervals=baseline_intervals,
        op_diag=op_diag, candidate_results=candidate_results,
        ranking=ranking, runtime_s=elapsed,
        evidence_id=EVIDENCE_ID, primary_claim=PRIMARY_CLAIM,
        secondary_claims=SECONDARY_CLAIMS,
    )
    # Round 5 additions
    metrics["baseline_pairwise_margins"] = baseline_margins
    metrics["policy_comparison"] = policy_comparison
    metrics["two_step_design"] = two_step
    metrics["resolution"] = resolution
    metrics["timestamp_utc"] = datetime.now(timezone.utc).isoformat()

    # 13. Write outputs
    write_metrics_json(metrics, out_dir)
    write_run_report(metrics, out_dir)
    write_candidate_ranking(ranking, out_dir)
    write_epsilon_sweep(candidate_results, out_dir)
    write_epsilon_candidate_matrix(candidate_results, out_dir)
    write_ambiguity_reduction(baseline_oqci, ranking, out_dir)
    write_claim_intervals_before_after(baseline_intervals, candidate_results, ranking, out_dir)
    write_near_null_before_after(baseline_nullspace, candidate_results, ranking, out_dir)
    write_next_measurement_policy(ranking, out_dir)
    write_failure_modes(metrics, ranking, out_dir)
    write_truth_coverage_audit(candidate_results, out_dir)
    write_valid_disambiguation_matrix(candidate_results, out_dir)
    write_breakthrough_gate_audit(candidate_results, metrics, out_dir)
    write_regularized_consistent_set_audit(candidate_results, out_dir)
    write_epsilon_calibration_audit(candidate_results, out_dir)
    write_regularization_breakthrough_gate_audit(metrics, candidate_results, out_dir)
    # Round 5 new reports
    write_pairwise_margin_matrix_report(baseline_margins, candidate_results, out_dir)
    write_active_policy_comparison(policy_comparison, out_dir)
    write_two_step_active_design_audit(two_step, candidate_results, out_dir)
    write_round5_pairwise_margin_gate_audit(metrics, two_step, policy_comparison, out_dir)

    # 14. Summary
    summary = {
        "evidence_id": EVIDENCE_ID,
        "case_count": len(cases),
        "candidate_count": len(candidates),
        "status": metrics["status"],
        "engineering_gates_passed": metrics["engineering_gates_passed"],
        "scientific_gates_passed": metrics["scientific_gates_passed"],
        "baseline_min_gamma": baseline_margins["summary"]["min_gamma"],
        "best_1step": two_step.get("best_1step_candidate", "none"),
        "min_gamma_after_1step": two_step.get("min_gamma_after_1step", 0.0),
        "pairwise_differs_from_vdr": policy_comparison.get("pairwise_differs_from_vdr", False),
        "baseline_ambiguity_rate": baseline_oqci["ambiguity_rate"],
        "best_candidate": ranking.get("best_global", "none"),
        "best_utility": ranking.get("best_utility", 0.0),
        "metrics_path": str(out_dir / "metrics.json"),
        "runtime_s": elapsed,
    }
    print(json.dumps(summary, indent=2))
    return metrics


def build_from_candidate(cfg, cand, baseline_heights):
    """Build the operator bundle for a candidate (for pairwise margin computation)."""
    from operators import build_candidate_operator, build_multi_state_operator
    from data_adapter import generate_cases as _gen

    n_states = cand.n_states
    if cand.height_um <= 0.01:
        bundle_ss = multi_height_operator_stack(cfg)
    else:
        bundle_ss = build_candidate_operator(
            cfg, baseline_heights, cand.height_um, cand.components)
    if n_states > 1:
        return build_multi_state_operator(bundle_ss, n_states)
    return bundle_ss


if __name__ == "__main__":
    main()
