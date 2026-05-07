# E28 Metrics Schema

Schema version: `research-ssot-metrics-v1`

## Top-level fields

| Field | Type | Description |
|---|---|---|
| evidence_id | string | E28_magnetic_transfer_matrix_observable_invariants |
| claim | string | Primary claim C02_single_plane_identifiability_boundary |
| status | string | passed / passed_with_limitations / failed_sanity |
| all_acceptance_gates_passed | bool | Aggregate gate status |
| engineering_gates | dict | Per-gate pass/fail |
| scientific_gates | dict | Per-gate pass/fail |
| transfer_matrix | dict | Transfer matrix diagnostics |
| invariants | dict | Invariant computation results |
| raw_vs_invariant | dict | Raw vs invariant margin comparison |
| nuisance_audit | dict | Nuisance radius audit |
| margins.observable_quotient | dict | Robust quotient certificate over Q0/Q12/Q3 |
| hardcase_gain_sweep | dict | Gain-only nuisance sweep for raw-fails/Gram-passes hard cases |
| consistent_set | dict | Consistent set analysis |
| leakage_audit | dict | No-leakage protocol audit |
| cannot_claim | list | Cannot-claim boundary list |

## Acceptance gates

| Gate | Description |
|---|---|
| transfer_matrix_computed | T_y computed for all hypotheses |
| invariants_computed | All three invariants computed |
| nuisance_stress_executed | Nuisance perturbation ladder ran |
| reports_written | All output files present |
| selected_invariant_is_not_raw | Best representation is an actual invariant, not raw field distance |
| selected_invariant_gamma_beats_raw_gamma | The selected invariant improves at least one robust margin over raw |
| selected_invariant_positive_gamma_rate_ge_0_30 | >= 30% pairs have positive selected-invariant margin |
| selected_invariant_critical_pair_positive_gamma_rate_ge_0_30 | >= 30% critical pairs positive for selected invariant |
| selected_invariant_rho_less_than_raw_rho | Selected invariant nuisance radius is smaller than raw |
| selected_invariant_nontrivial | Selected invariant has non-zero pairwise distance |
| observable_quotient_selected_invariant_all_positive | Selected invariant separates Q0/Q12/Q3 with positive robust margins |
| hard_h1_h2_reported_unresolved | H1/H2 is explicitly reported as unresolved |
| hardcase_gain_sweep_executed | Gain-only hard-case sweep ran |
| hardcase_gram_quotient_survives_when_raw_fails | Sweep found raw quotient failure with Gram quotient survival |
| generated_domain_boundary_explicit | Cannot-claim boundary recorded |
