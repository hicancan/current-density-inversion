# WIN/LOSS BY METRIC (Scientific Only)

New method: **graph_kcl_differentiable_inverse_scaled**

| vs Baseline | Wins | Losses | Ties | Win Metrics | Loss Metrics |
|---|---:|---:|---:|---|---|
| naive_single_layer | 3 | 3 | 1 | layer_misallocation, via_f1, kcl_residual | current_relative_l2, b_residual_rel, closure_error |
| incorrect_two_layer | 3 | 3 | 1 | layer_misallocation, via_f1, kcl_residual | current_relative_l2, b_residual_rel, closure_error |
| ridge_unscaled | 3 | 2 | 2 | layer_misallocation, via_f1, b_residual_rel | current_relative_l2, closure_error |
| ridge_scaled | 1 | 5 | 1 | kcl_residual | current_relative_l2, layer_misallocation, via_f1, b_residual_rel, closure_error |
| graph_kcl_aware_unscaled | 2 | 3 | 2 | via_f1, b_residual_rel | current_relative_l2, layer_misallocation, closure_error |
| graph_kcl_aware_scaled | 0 | 0 | 7 |  |  |
| new_no_projection | 0 | 0 | 7 |  |  |
| new_no_via_sparsity | 0 | 0 | 7 |  |  |

Generated-domain benchmark only. Cannot claim real validation.