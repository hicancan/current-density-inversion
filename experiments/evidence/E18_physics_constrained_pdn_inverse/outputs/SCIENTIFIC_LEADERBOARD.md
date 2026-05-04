# SCIENTIFIC LEADERBOARD

Ranked by average rank across scientific metrics (no runtime).

| Rank | Method | avg_rank | rel_l2 | misalloc | via_f1 | no_via_fp | b_res_rel | kcl_res | closure |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | ridge_scaled | 3.000000 | 2.238138 | 0.163659 | 0.411479 | 0.000e+00 | 0.002719 | 0.695279 | 0.202007 |
| 2 | graph_kcl_aware_unscaled | 4.285714 | 1.000000 | 0.160799 | 0.000e+00 | 0.000e+00 | 1.000000 | 7.000e-15 | 1.235e-10 |
| 3 | naive_single_layer | 5.000000 | 4.145790 | 0.326218 | 0.000e+00 | 0.000e+00 | 0.097962 | 1.186596 | 1.505415 |
| 4 | graph_kcl_aware_scaled | 5.000000 | 9.590102 | 0.164399 | 0.273775 | 0.000e+00 | 0.400859 | 4.460e-15 | 4.295514 |
| 5 | ridge_unscaled | 5.142857 | 1.000000 | 0.204068 | 0.000e+00 | 0.000e+00 | 1.000000 | 5.388e-11 | 5.826e-10 |
| 6 | graph_kcl_differentiable_inverse_scaled | 5.285714 | 9.590102 | 0.164399 | 0.273775 | 0.000e+00 | 0.400859 | 1.216e-15 | 4.295514 |
| 7 | incorrect_two_layer | 5.428571 | 8.907015 | 0.329004 | 0.000e+00 | 0.000e+00 | 0.017538 | 2.561636 | 0.782298 |
| 8 | new_no_via_sparsity | 5.857143 | 9.590102 | 0.164399 | 0.273775 | 0.000e+00 | 0.400859 | 1.198e-15 | 4.295514 |
| 9 | new_no_projection | 6.000000 | 9.590102 | 0.164399 | 0.273775 | 0.000e+00 | 0.400859 | 1.444e-13 | 4.295514 |

Generated-domain benchmark only. Cannot claim real validation.