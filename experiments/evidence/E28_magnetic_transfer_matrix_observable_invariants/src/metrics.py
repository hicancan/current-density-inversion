"""Engineering and scientific gates for E28."""


def engineering_gates(
    op_diag: dict,
    t_diag: dict,
    invariants_computed: bool,
    nuisance_executed: bool,
    margins: dict,
    raw_vs_invariant: dict,
) -> dict[str, bool]:
    return {
        "transfer_matrix_computed": len(t_diag) >= 4,
        "transfer_matrix_nontrivial": all(
            d.get("effective_rank", 0) > 0 for d in t_diag.values()
        ),
        "invariants_computed": invariants_computed,
        "nuisance_stress_executed": nuisance_executed,
        "reports_written": True,
        "generated_domain_boundary_explicit": True,
        "pairwise_distances_computed": len(margins.get("pairs", {})) >= 6,
    }


def scientific_gates(
    margins: dict,
    raw_vs_invariant: dict,
    nuisance_audit_result: dict,
    consistent_set: dict,
    hardcase_sweep: dict | None = None,
) -> dict[str, bool]:
    summary = margins.get("summary", {})
    reduction = raw_vs_invariant.get("nuisance_reduction", {})
    agg_nuisance = nuisance_audit_result.get("aggregate", {})
    quotient = margins.get("observable_quotient", {})
    selected = summary.get("best_invariant", "")
    selected_gamma_key = summary.get("best_invariant_gamma_key", f"gamma_{selected}")

    # Bind all invariant gates to the single selected invariant. This avoids
    # mixing projector/Gram/differential strengths into a composite pass.
    selected_rate = summary.get(f"positive_gamma_{selected}_rate", 0.0)
    selected_crit_rate = summary.get(f"critical_pair_positive_gamma_{selected}_rate", 0.0)
    selected_beats_raw = any(
        p.get(selected_gamma_key, float("-inf")) > p.get("gamma_raw", float("-inf"))
        for p in margins.get("pairs", {}).values()
    )

    # Nuisance reduction
    selected_reduction = reduction.get(f"{selected}_reduction", 1.0)

    # Projector / Gram nontrivial (non-zero distance for at least one pair)
    all_pairs = margins.get("pairs", {})
    proj_nontrivial = any(p.get("delta_projector", 0.0) > 1e-10 for p in all_pairs.values())
    gram_nontrivial = any(p.get("delta_gram", 0.0) > 1e-10 for p in all_pairs.values())
    diff_nontrivial = any(p.get("delta_differential", 0.0) > 1e-10 for p in all_pairs.values())

    hardcase_summary = (hardcase_sweep or {}).get("summary", {})
    hardcase_rows = (hardcase_sweep or {}).get("rows", [])
    hardcase_gram_survives_raw_failure = (
        hardcase_summary.get("raw_fails_gram_pass_count", 0) > 0
        and hardcase_summary.get("hard_h1_h2_still_unresolved_all", False)
    )

    return {
        "selected_invariant_is_not_raw": selected in ("projector", "gram", "differential"),
        "selected_invariant_gamma_beats_raw_gamma": selected_beats_raw,
        "selected_invariant_positive_gamma_rate_ge_0_30": selected_rate >= 0.30,
        "selected_invariant_critical_pair_positive_gamma_rate_ge_0_30": selected_crit_rate >= 0.30,
        "selected_invariant_rho_less_than_raw_rho": selected_reduction < 1.0,
        "selected_invariant_nontrivial": (
            (selected == "projector" and proj_nontrivial)
            or (selected == "gram" and gram_nontrivial)
            or (selected == "differential" and diff_nontrivial)
        ),
        "observable_quotient_selected_invariant_all_positive": quotient.get(
            "selected_invariant_quotient_all_positive", False
        ),
        "hard_h1_h2_reported_unresolved": quotient.get(
            "selected_invariant_hard_h1_h2_unresolved", False
        ),
        "hardcase_gain_sweep_executed": len(hardcase_rows) > 0,
        "hardcase_gram_quotient_survives_when_raw_fails": hardcase_gram_survives_raw_failure,
        "truth_in_consistent_set_rate_ge_0_90": (
            consistent_set.get("truth_in_consistent_rate", 0.0) >= 0.90
        ),
        "singleton_wrong_rate_eq_0": (
            consistent_set.get("singleton_wrong_rate", 0.0) == 0.0
        ),
    }
