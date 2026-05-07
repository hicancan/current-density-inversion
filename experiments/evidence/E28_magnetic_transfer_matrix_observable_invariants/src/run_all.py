"""Run E28 Magnetic Transfer-Matrix Observable Invariants pipeline.

Computes transfer matrices for four topology hypotheses, extracts
nuisance-invariant representations, and compares raw vs invariant margins.
"""

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
from operators import (
    build_operator_and_graph,
    build_port_excitation,
    operator_diagnostics,
    OperatorBundle,
    PortExcitation,
)
from hypotheses import (
    HYPOTHESES,
    build_all_conductance_models,
    ConductanceModel,
)
from transfer_matrix import (
    compute_all_transfer_matrices,
    all_transfer_matrix_diagnostics,
)
from invariants import (
    compute_all_invariants,
    invariant_sanity_checks,
)
from distances import (
    compute_all_pairwise_distances,
    HYP_PAIRS,
    CRITICAL_PAIRS,
)
from nuisance import (
    nuisance_audit,
    nuisance_reduction_factor,
)
from margins import (
    compute_robust_margins,
    invariant_beats_raw,
    empirical_invariant_epsilon,
)
from hardcase import run_gain_hardcase_sweep
from data import (
    generate_transfer_cases,
    consistent_set_analysis,
)
from metrics import (
    engineering_gates,
    scientific_gates,
)
from reporting import (
    write_metrics_json,
    write_run_report,
    write_transfer_matrix_derivation,
    write_invariant_definitions,
    write_raw_vs_invariant_margin_table,
    write_projector_gram_audit,
    write_nuisance_invariance_audit,
    write_observable_quotient_certificate,
    write_hardcase_gain_sweep,
    write_consistent_set_audit,
    write_failure_modes,
)

EVIDENCE_ID = "E28_magnetic_transfer_matrix_observable_invariants"
PRIMARY_CLAIM = "C02_single_plane_identifiability_boundary"
SECONDARY_CLAIMS = [
    "C04_inverse_crime_and_operator_gap",
    "C06_graph_hypothesis_system_identification",
    "C10_pdn_kcl_distribution_need",
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

    # ── 1. Build operator bundle and graph ─────────────────────────────────
    n = int(cfg["grid_size"])
    layers = int(cfg["layer_count"])
    pitch = float(cfg["pixel_pitch_um"])
    dz = float(cfg["layer_spacing_um"])
    sensor_h = float(cfg["sensor_heights_um"][0])

    bundle = build_operator_and_graph(n, layers, pitch, dz, sensor_h)
    op_diag = operator_diagnostics(bundle)

    # ── 2. Build port excitation matrix ────────────────────────────────────
    ports = build_port_excitation(bundle, cfg)

    # ── 3. Build conductance models for each hypothesis ─────────────────────
    cond_models = build_all_conductance_models(bundle, cfg)

    # ── 4. Compute transfer matrices ───────────────────────────────────────
    T_matrices = compute_all_transfer_matrices(bundle, cond_models, ports)
    t_diag = all_transfer_matrix_diagnostics(T_matrices)

    # ── 5. Compute invariants ──────────────────────────────────────────────
    invariants = compute_all_invariants(T_matrices)
    sanity = invariant_sanity_checks(T_matrices, invariants)
    invariants_computed = all(sanity.values())

    # ── 6. Compute pairwise distances ──────────────────────────────────────
    pairwise_distances = compute_all_pairwise_distances(T_matrices)

    # ── 7. Nuisance audit ──────────────────────────────────────────────────
    nuisance_result = nuisance_audit(bundle, cfg, cond_models, ports, T_matrices)
    nuisance_executed = bool(nuisance_result.get("aggregate", {}))
    reduction = nuisance_reduction_factor(nuisance_result)

    # ── 8. Compute epsilon and tau ─────────────────────────────────────────
    sigma = float(cfg["noise_sigma"])
    tau_mult = float(cfg["tau_multiplier"])
    tau = float(cfg["invariant_eps_threshold"])

    # Empirical invariant-specific epsilon (in each invariant's own units)
    T_ref = T_matrices["H0_no_via"]
    eps_invariant = empirical_invariant_epsilon(T_ref, sigma, tau_mult, n_samples=20)

    # ── 9. Compute robust margins ──────────────────────────────────────────
    margins = compute_robust_margins(pairwise_distances, nuisance_result, eps_invariant, tau)

    # ── 10. Raw vs invariant comparison ────────────────────────────────────
    beats = invariant_beats_raw(margins)
    raw_vs_invariant = {
        "raw_nuisance_radius": nuisance_result["aggregate"]["rho_raw"],
        "projector_nuisance_radius": nuisance_result["aggregate"]["rho_projector"],
        "gram_nuisance_radius": nuisance_result["aggregate"]["rho_gram"],
        "differential_nuisance_radius": nuisance_result["aggregate"]["rho_differential"],
        "nuisance_reduction": reduction,
        "invariant_beats_raw": beats,
        "pairwise_margins": margins["pairs"],
        "margin_summary": margins["summary"],
        "observable_quotient": margins.get("observable_quotient", {}),
    }

    # ── 11. Consistent set analysis ────────────────────────────────────────
    cases = generate_transfer_cases(bundle, cond_models, ports, cfg)
    eps_cs = tau_mult * sigma * np.sqrt(float(T_matrices["H0_no_via"].size))
    consistent_set = consistent_set_analysis(cases, T_matrices, eps_cs)

    # ── 12. Gain hard-case sweep ────────────────────────────────────────────
    hardcase_gain_sweep = run_gain_hardcase_sweep(
        bundle, cfg, cond_models, ports, T_matrices,
        pairwise_distances, eps_invariant, tau,
    )

    # ── 13. Compute gates ──────────────────────────────────────────────────
    eng_gates = engineering_gates(
        op_diag, t_diag, invariants_computed, nuisance_executed,
        margins, raw_vs_invariant,
    )
    sci_gates = scientific_gates(
        margins, raw_vs_invariant, nuisance_result, consistent_set,
        hardcase_gain_sweep,
    )
    eng_passed = all(eng_gates.values())
    sci_passed = all(sci_gates.values())
    if not eng_passed:
        status = "failed_sanity"
    elif not sci_passed:
        status = "passed_with_limitations"
    else:
        status = "passed"

    elapsed = time.perf_counter() - t0

    # ── 14. Build metrics ─────────────────────────────────────────────────
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
        "acceptance_gates": {**eng_gates, **sci_gates},
        "operator_diagnostics": op_diag,
        "transfer_matrix": t_diag,
        "invariants": {
            "sanity_checks": sanity,
            "computed": invariants_computed,
        },
        "pairwise_distances": pairwise_distances,
        "nuisance_audit": {
            "per_hypothesis": nuisance_result.get("per_hypothesis", {}),
            "aggregate": nuisance_result["aggregate"],
            "perturbation_types": nuisance_result["perturbation_types"],
            "magnitudes": nuisance_result["magnitudes"],
            "reduction_factors": reduction,
        },
        "margins": margins,
        "raw_vs_invariant": raw_vs_invariant,
        "hardcase_gain_sweep": hardcase_gain_sweep,
        "consistent_set": consistent_set,
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
            "universal via detection",
            "real-board PDN robustness",
            "that invariants work for all real hardware",
            "that generated-domain margins hold for all observation protocols",
            "that transfer matrix approach replaces all existing methods",
            "that nuisance model captures all real-world perturbation families",
            "that H1_via and H2_model_gap are separable under the current generator",
            "full four-hypothesis robust separability",
        ],
    }

    # ── 15. Write outputs ──────────────────────────────────────────────────
    write_metrics_json(metrics, out_dir)
    write_run_report(metrics, out_dir)
    write_transfer_matrix_derivation(t_diag, op_diag, out_dir)
    write_invariant_definitions(out_dir)
    write_raw_vs_invariant_margin_table(pairwise_distances, margins, raw_vs_invariant, nuisance_result, out_dir)
    write_projector_gram_audit(pairwise_distances, T_matrices, out_dir)
    write_nuisance_invariance_audit(nuisance_result, out_dir)
    write_observable_quotient_certificate(metrics, out_dir)
    write_hardcase_gain_sweep(metrics, out_dir)
    write_consistent_set_audit(consistent_set, out_dir)
    write_failure_modes(metrics, out_dir)

    # ── 16. Summary ────────────────────────────────────────────────────────
    summary = {
        "evidence_id": EVIDENCE_ID,
        "n_cases": len(cases),
        "n_port_states": ports.n_states,
        "status": status,
        "engineering_gates_passed": eng_passed,
        "scientific_gates_passed": sci_passed,
        "best_invariant": margins["summary"].get("best_invariant", "none"),
        "positive_gamma_projector_rate": margins["summary"].get("positive_gamma_projector_rate", 0.0),
        "positive_gamma_gram_rate": margins["summary"].get("positive_gamma_gram_rate", 0.0),
        "observable_quotient_selected_invariant_all_positive": margins.get("observable_quotient", {}).get(
            "selected_invariant_quotient_all_positive", False
        ),
        "hardcase_raw_fails_gram_pass_count": hardcase_gain_sweep.get("summary", {}).get(
            "raw_fails_gram_pass_count", 0
        ),
        "consistent_set_nonempty_rate": consistent_set.get("consistent_set_nonempty_rate", 0.0),
        "truth_in_consistent_rate": consistent_set.get("truth_in_consistent_rate", 0.0),
        "metrics_path": str(out_dir / "metrics.json"),
        "runtime_s": elapsed,
    }
    print(json.dumps(summary, indent=2))
    return metrics


if __name__ == "__main__":
    main()
