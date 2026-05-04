# RUN REPORT - E18 Physics-Constrained PDN Inverse

## Claim

Primary: `C10_pdn_kcl_distribution_need`
Secondary: `C06_graph_hypothesis_system_identification`, `C02_single_plane_identifiability_boundary`, `C04_inverse_crime_and_operator_gap`

## Algorithm Summary

graph_kcl_differentiable_inverse: Warm-started constrained ridge + L-BFGS-B
composite loss optimization (B-fidelity + KCL + via sparsity + prior) + KCL
post-projection. CPU-first, scipy-based.

## Dataset Summary

- 18 cases across 6 families
- 4-layer stack with 11 output channels
- Grid: 12x12, sensor: 14x14
- Families: nominal_via_chain, no_via_hard_negative, dense_via_cluster, return_grid_bottleneck, deep_layer_only, layer_misallocation_trap
- Scale: prototype (18 cases); 180-case expansion possible with seed sweep

## Baseline List

- naive_single_layer
- incorrect_two_layer
- ridge_least_squares
- graph_kcl_aware
- graph_kcl_differentiable_inverse

## Leaderboard (Top-line)

See UNIFIED_LEADERBOARD.md for full table.

## Win/Loss Summary

- vs naive_single_layer: 1W/1L/6T
- vs incorrect_two_layer: 1W/1L/6T
- vs ridge_least_squares: 1W/1L/6T
- vs graph_kcl_aware: 0W/1L/7T

## Acceptance Gates

| e18_dataset_generated_or_loaded | True |
| four_layer_11_channel_outputs_present | True |
| new_inverse_runs_to_completion | True |
| leaderboard_contains_required_baselines | True |
| same_split_comparison_documented | True |
| no_leakage_protocol_documented | True |
| physical_b_residual_reported | True |
| kcl_residual_reported | True |
| layer_misallocation_reported | True |
| via_metrics_reported | True |
| failure_cases_reported | True |
| cannot_claim_boundaries_documented | True |
| new_method_reduces_misallocation_vs_naive | True |
| new_method_reduces_misallocation_vs_incorrect_two_layer | True |
| new_method_matches_or_improves_vs_ridge | True |
| new_method_reduces_kcl_residual_vs_unconstrained | True |
| new_method_reports_tradeoff_vs_best_b_residual_baseline | True |

All gates passed: True

## Failure Cases

4 failure case(s) identified. See FAILURE_CASES.md.

## Runtime

Total experiment: 14.5s

## Cannot Claim

- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL validation
- real multilayer PCB/PDN recovery
- real hardware via-chain sensitivity
- generated benchmark transfers to real hardware
- graph/KCL/differentiable inverse universally outperforms all baselines
- L1-curl literature method has been beaten unless exact reproduction is implemented
- mechanism-level correctness without mechanism labels

## Next Required Evidence

- Expand to 180 cases (6 families x 3 variants x 10 seeds)
- Validate against Tikhonov/L1-curl baselines from E17
- External solver validation (COMSOL/FastHenry)
- Real QDM/NV measurement data
- Real CAD/Gerber/GDS layout import

## Conclusion

This is generated-domain prototype evidence for physics-constrained multilayer
PDN inverse. Results are prototype/generated-domain and cannot be written as
decisive SOTA or real validation.

## Metrics Reference

Full metrics: `outputs/metrics.json`
