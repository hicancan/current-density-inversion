# Metrics Schema - E18

## Schema Version

`research-ssot-metrics-v1`

## Required Fields

| Field | Type | Description |
|---|---|---|
| schema_version | string | Must be `research-ssot-metrics-v1` |
| evidence_id | string | `E18_physics_constrained_pdn_inverse` |
| claim_id | string | Primary claim ID |
| secondary_claims | list[string] | Secondary claim IDs |
| status | string | `passed`, `passed_with_limitations`, or `failed` |
| case_count | int | Number of benchmark cases |
| family_count | int | Number of families |
| method_names | list[string] | All method names |
| baseline_names | list[string] | Baseline-only names |
| leaderboard | list[dict] | Ranked leaderboard rows |
| aggregate_metrics | dict | Per-method aggregate metrics |
| family_metrics | dict | Per-method per-family metrics |
| improvement_ratios | dict | New method vs each baseline |
| acceptance_gates | dict | All acceptance gate results |
| all_acceptance_gates_passed | bool | Overall gate result |
| run_audit | dict | Run metadata |
| leakage_audit | dict | No-leakage audit |
| cannot_claim | list[string] | Explicit claim boundaries |

## Metric Definitions

| Metric | Range | Better |
|---|---|---|
| current_rmse | [0, ∞) | lower |
| current_relative_l2 | [0, 10] | lower |
| layer_wise_rmse | [0, 10] per layer | lower |
| layer_misallocation | [0, 1] | lower |
| via_precision | [0, 1] | higher |
| via_recall | [0, 1] | higher |
| via_f1 | [0, 1] | higher |
| no_via_false_positive | [0, ∞) | lower |
| physical_b_residual | [0, ∞) | lower |
| kcl_residual | [0, ∞) | lower |
| topology_residual | [0, ∞) | lower |
| current_closure_error | [0, ∞) | lower |
| b_residual_rel | [0, 10] | lower |
| runtime_s | [0, ∞) | lower |
