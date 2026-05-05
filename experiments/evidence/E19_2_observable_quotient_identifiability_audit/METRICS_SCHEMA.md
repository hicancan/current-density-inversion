# E19.2 Metrics Schema

Schema version: `research-ssot-metrics-v1`

## Top-level fields

| Field | Type | Description |
|---|---|---|
| evidence_id | string | E19_2_observable_quotient_identifiability_audit |
| claim | string | Primary claim C10_pdn_kcl_distribution_need |
| status | string | passed / passed_with_limitations / failed_sanity |
| all_acceptance_gates_passed | bool | Aggregate gate status |
| engineering_gates | dict | Per-gate pass/fail |
| scientific_gates | dict | Per-gate pass/fail |
| oqci | dict | OQCI aggregate metrics |
| ridge_baseline | dict | Ridge baseline metrics |
| operator_diagnostics | dict | Forward operator diagnostics |
| leakage_audit | dict | No-leakage protocol audit |
| cannot_claim | list | Cannot-claim boundary list |

## OQCI metrics

| Field | Type | Description |
|---|---|---|
| case_count | int | Total cases |
| consistent_set_nonempty_rate | float | Fraction where at least one hypothesis is consistent |
| single_height_ambiguity_rate | float | Fraction where multiple hypotheses are consistent |
| mean_claim_interval_width | float | Mean interval width across all claims |
| claim_interval_widths_by_truth | dict | Claim interval stats per truth class |
| pairwise_distances | dict | Per-pair distinguishability distance |
| near_null_count | int | Number of near-null modes |
| effective_rank | int | Effective observable rank |
| decision_counts | dict | accept/reject/need_next counts |

## Acceptance gates

| Gate | Description |
|---|---|
| consistent_set_nonempty | At least 95% of cases have non-empty consistent set |
| pairwise_distances_computed | All 6 hypothesis pairs have distances |
| near_null_modes_extracted | Near-null modes present |
| claim_intervals_valid | All intervals are subsets of [0,1] |
| reports_written | All output files present |
