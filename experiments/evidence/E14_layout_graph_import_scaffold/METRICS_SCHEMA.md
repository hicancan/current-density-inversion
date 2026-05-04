# METRICS_SCHEMA - E14 Layout Graph Import Scaffold

Schema: `research-ssot-metrics-v1`.

## Acceptance Gates

| Gate | Type | Description |
|---|---|---|
| schema_validates_all_examples | bool | All layout examples pass schema validation |
| graph_extraction_preserves_layers | bool | Extracted graph preserves layer information |
| via_candidates_extracted | bool | Via nodes are extracted from layout |
| return_candidates_extracted | bool | Return candidate edges are identified |
| kcl_graph_export_available | bool | KCL-residual–ready graph is exported |
| hypothesis_candidates_generated | bool | H0/H1/H2/H3 candidates generated for all examples |
| no_real_cad_claim | bool | No real CAD/Gerber/GDS claim is made |
| all_acceptance_gates_passed | bool | All above gates pass |

## Metrics File

`outputs/metrics.json` contains per-example breakdowns and aggregate gates.
