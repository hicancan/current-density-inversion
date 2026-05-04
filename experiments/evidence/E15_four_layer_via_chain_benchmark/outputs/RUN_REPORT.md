# RUN_REPORT - E15 Four-Layer Via-Chain Benchmark

## Claim

`C10_pdn_kcl_distribution_need` (secondary: `C02_single_plane_identifiability_boundary`, `C06_graph_hypothesis_system_identification`).

## Metrics

See `outputs/metrics.json` for full metrics.

## Acceptance Gates

| four_layer_dataset_generated | True |
| output_channels_match_11 | True |
| topology_residual_finite | True |
| kcl_residual_finite | True |
| graph_kcl_baseline_reduces_layer_misallocation_vs_naive | True |
| no_via_fp_reported | True |
| dense_via_metrics_reported | True |
| deep_layer_attenuation_reported | True |
| all_acceptance_gates_passed | True |

## Boundary

Generated benchmark only. No real PCB/chip, CAD, FEM, or QDM/NV validation.
