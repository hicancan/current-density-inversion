# E19 Metrics Schema

Schema version: `research-ssot-metrics-v1`

## Top-level fields

| Field | Type | Description |
|---|---|---|
| `evidence_id` | string | `E19_obghi_minimal_observable_topology_posterior` |
| `claim` | string | Primary claim `C10_pdn_kcl_distribution_need` |
| `all_acceptance_gates_passed` | bool | Aggregate gate status |
| `acceptance_gates` | dict | Per-gate pass/fail |
| `obghi` | dict | OBGHI aggregate metrics |
| `ridge_map_baseline` | dict | Ridge baseline metrics |
| `operator_diagnostics` | dict | Forward operator diagnostics |
| `leakage_audit` | dict | No-leakage protocol audit |
| `cannot_claim` | list | Cannot-claim boundary list |

## OBGHI metrics

| Field | Type | Description |
|---|---|---|
| `case_count` | int | Total cases |
| `top1_accuracy` | float | Top-1 hypothesis accuracy |
| `accepted_accuracy` | float | Accuracy among accepted cases |
| `accepted_risk` | float | Risk among accepted cases (1 - accuracy) |
| `reject_rate` | float | Fraction rejected |
| `need_next_measurement_rate` | float | Fraction needing more data |
| `brier_score` | float | Brier score across all hypotheses |
| `posterior_entropy` | float | Mean posterior entropy |
| `via_gap_angle_deg` | float | Via-gap subspace principal angle |
| `by_truth` | dict | Per-truth-class metrics |

## Acceptance gates

| Gate | Description |
|---|---|
| `posterior_rows_present` | At least one case processed |
| `topology_posterior_nontrivial` | Mean entropy > 0.05 |
| `accepted_risk_bounded` | Accepted risk <= 0.70 |
| `reject_or_need_next_available` | Reject + need_next > 2% |
| `via_gap_ambiguity_measured` | Via-gap angle >= 0 |
| `obghi_matches_or_beats_ridge_top1` | OBGHI top1 >= ridge top1 - 5% |
| `generated_domain_boundaries_recorded` | Always true |
