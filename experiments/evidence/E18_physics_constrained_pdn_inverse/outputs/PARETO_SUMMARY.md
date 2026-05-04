# PARETO SUMMARY

New method: **graph_kcl_differentiable_inverse_scaled**

## vs ridge_scaled

  - ➖ no_via_fp: 0.000e+00 ≈ 0.000e+00
  - ✅ kcl_residual: 1.216e-15 vs 0.695279
  - ❌ current_relative_l2: 9.590102 vs 2.238138
  - ❌ layer_misallocation: 0.164399 vs 0.163659
  - ❌ via_f1: 0.273775 vs 0.411479
  - ❌ b_residual_rel: 0.400859 vs 0.002719
  - ❌ closure_error: 4.295514 vs 0.202007
  - **Dominates ridge_scaled**: NO

## vs graph_kcl_aware_scaled

  - ➖ current_relative_l2: 9.590102 ≈ 9.590102
  - ➖ layer_misallocation: 0.164399 ≈ 0.164399
  - ➖ via_f1: 0.273775 ≈ 0.273775
  - ➖ no_via_fp: 0.000e+00 ≈ 0.000e+00
  - ➖ b_residual_rel: 0.400859 ≈ 0.400859
  - ➖ kcl_residual: 1.216e-15 ≈ 4.460e-15
  - ➖ closure_error: 4.295514 ≈ 4.295514
  - **Dominates graph_kcl_aware_scaled**: YES

Generated-domain benchmark only. Cannot claim real validation.