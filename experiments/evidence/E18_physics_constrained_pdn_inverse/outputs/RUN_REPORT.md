# RUN REPORT - E18.1 Physics-Constrained PDN Inverse

## E18 v1 Root-Cause Diagnosis

1. Via columns in A were all zeros (no vertical current kernel)
2. KCL matrix D did not couple via source/sink to layer divergence
3. Fixed ridge_alpha=0.01 with SI-scale A (~1e-7) caused near-zero solutions
4. b_residual/current_rmse/via_f1 did not distinguish methods
5. Leaderboard mixed runtime and scientific metrics

## E18.1 Fixes Applied

1. Via vertical-current kernel added to forward operator
2. KCL matrix now couples via s12/s23/s34 into layer continuity equations
3. Column-normalized (scaled) solvers for numerical stability
4. Oracle/zero sanity baselines for forward operator verification
5. Separated scientific leaderboard (avg rank) from runtime table
6. KCL-consistent truth projection in data generation
7. Ablation methods: no_projection, no_via_sparsity

## Operator Sanity

- via_forward_columns_nonzero: True
- via_column_norm_mean: 8.279e-07
- sheet_column_norm_mean: 5.300e-08

## KCL Matrix Sanity

- kcl_via_coupling_nonzero: True

## Oracle/Zero Sanity

- oracle b_residual_rel: 0.000e+00
- zero b_residual_rel: 1.000000
- ridge_scaled b_residual_rel: 0.002719
- ridge_scaled beats zero: True

## Acceptance Gates

| via_forward_columns_nonzero | True |
| kcl_matrix_via_coupling_nonzero | True |
| oracle_b_residual_near_zero | True |
| zero_b_residual_near_one | True |
| ridge_scaled_beats_zero_on_b_residual | True |
| method_predictions_not_identical | True |
| b_residual_distinguishes_methods | True |
| current_rmse_distinguishes_methods_or_explained | True |
| via_metrics_nontrivial_or_failure_recorded | True |
| new_method_reduces_kcl_vs_ridge_scaled | True |
| new_method_improves_or_matches_misalloc_vs_gka_scaled | True |
| new_method_does_not_destroy_b_residual_vs_gka_scaled | True |
| failure_cases_reported | True |

All gates passed: True
Status: passed

## Win/Loss Summary (Scientific Only)

- vs naive_single_layer: 3W/3L/1T
- vs incorrect_two_layer: 3W/3L/1T
- vs ridge_unscaled: 3W/2L/2T
- vs ridge_scaled: 1W/5L/1T
- vs graph_kcl_aware_unscaled: 2W/3L/2T
- vs graph_kcl_aware_scaled: 0W/0L/7T
- vs new_no_projection: 0W/0L/7T
- vs new_no_via_sparsity: 0W/0L/7T

## Failure Cases

1 failure case(s). See FAILURE_CASES.md.

## Total Runtime

48.1s (18 cases, 11 methods)

## Cannot Claim

- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external solver validation
- universally outperforms all baselines
- generated benchmark transfers to real hardware

## Metrics Reference

Full metrics: `outputs/metrics.json`
