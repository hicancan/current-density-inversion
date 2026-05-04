# UNIFIED LEADERBOARD

| Rank | Method | current_rmse | layer_misalloc | via_f1 | no_via_fp | b_residual | kcl_residual | closure_error | runtime_s |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | naive_single_layer | 0.013205 | 0.316855 | 0.000e+00 | 0.000e+00 | 1.000000 | 1.373e-13 | 1.588e-12 | 0.019956 |
| 2 | incorrect_two_layer | 0.013205 | 0.303832 | 0.000e+00 | 0.000e+00 | 1.000000 | 1.386e-13 | 2.215e-12 | 0.053072 |
| 3 | ridge_least_squares | 0.013205 | 0.218728 | 0.000e+00 | 0.000e+00 | 1.000000 | 1.589e-13 | 4.347e-12 | 0.159555 |
| 4 | graph_kcl_aware | 0.013205 | 0.212783 | 0.000e+00 | 0.000e+00 | 1.000000 | 4.920e-17 | 4.347e-12 | 0.188564 |
| 5 | graph_kcl_differentiable_inverse | 0.013205 | 0.212783 | 0.000e+00 | 0.000e+00 | 1.000000 | 2.404e-19 | 4.347e-12 | 0.353978 |

Lower is better for all metrics except via_f1 (higher is better).

Generated-domain benchmark only. Cannot claim real validation.