# FAMILY BREAKDOWN

## nominal_via_chain

| Method | current_rmse | misalloc | via_f1 | kcl_res | b_res | closure |
|---|---:|---:|---:|---:|---:|---:|
| naive_single_layer | 0.018571 | 0.316092 | 0.000e+00 | 2.113e-13 | 1.000000 | 2.054e-12 |
| incorrect_two_layer | 0.018571 | 0.302396 | 0.000e+00 | 2.135e-13 | 1.000000 | 2.887e-12 |
| ridge_least_squares | 0.018571 | 0.176827 | 0.000e+00 | 2.462e-13 | 1.000000 | 5.591e-12 |
| graph_kcl_aware | 0.018571 | 0.170413 | 0.000e+00 | 8.011e-17 | 1.000000 | 5.591e-12 |
| graph_kcl_differentiable_inverse | 0.018571 | 0.170413 | 0.000e+00 | 3.935e-19 | 1.000000 | 5.591e-12 |

## no_via_hard_negative

| Method | current_rmse | misalloc | via_f1 | kcl_res | b_res | closure |
|---|---:|---:|---:|---:|---:|---:|
| naive_single_layer | 0.008124 | 0.316092 | 0.000e+00 | 1.120e-13 | 1.000000 | 5.886e-13 |
| incorrect_two_layer | 0.008124 | 0.308156 | 0.000e+00 | 1.126e-13 | 1.000000 | 7.999e-13 |
| ridge_least_squares | 0.008124 | 0.198030 | 0.000e+00 | 1.259e-13 | 1.000000 | 1.621e-12 |
| graph_kcl_aware | 0.008124 | 0.195485 | 0.000e+00 | 2.855e-17 | 1.000000 | 1.621e-12 |
| graph_kcl_differentiable_inverse | 0.008124 | 0.195485 | 0.000e+00 | 1.340e-19 | 1.000000 | 1.621e-12 |

## dense_via_cluster

| Method | current_rmse | misalloc | via_f1 | kcl_res | b_res | closure |
|---|---:|---:|---:|---:|---:|---:|
| naive_single_layer | 0.024676 | 0.316092 | 0.000e+00 | 1.893e-13 | 1.000000 | 1.727e-12 |
| incorrect_two_layer | 0.024676 | 0.301473 | 0.000e+00 | 1.906e-13 | 1.000000 | 2.348e-12 |
| ridge_least_squares | 0.024676 | 0.165374 | 0.000e+00 | 2.166e-13 | 1.000000 | 4.666e-12 |
| graph_kcl_aware | 0.024676 | 0.147759 | 0.000e+00 | 6.841e-17 | 1.000000 | 4.666e-12 |
| graph_kcl_differentiable_inverse | 0.024676 | 0.147759 | 0.000e+00 | 3.358e-19 | 1.000000 | 4.666e-12 |

## return_grid_bottleneck

| Method | current_rmse | misalloc | via_f1 | kcl_res | b_res | closure |
|---|---:|---:|---:|---:|---:|---:|
| naive_single_layer | 0.016288 | 0.312403 | 0.000e+00 | 1.138e-13 | 1.000000 | 5.646e-13 |
| incorrect_two_layer | 0.016288 | 0.305643 | 0.000e+00 | 1.150e-13 | 1.000000 | 7.769e-13 |
| ridge_least_squares | 0.016288 | 0.200315 | 0.000e+00 | 1.322e-13 | 1.000000 | 1.498e-12 |
| graph_kcl_aware | 0.016288 | 0.205272 | 0.000e+00 | 4.465e-17 | 1.000000 | 1.498e-12 |
| graph_kcl_differentiable_inverse | 0.016288 | 0.205272 | 0.000e+00 | 2.199e-19 | 1.000000 | 1.498e-12 |

## deep_layer_only

| Method | current_rmse | misalloc | via_f1 | kcl_res | b_res | closure |
|---|---:|---:|---:|---:|---:|---:|
| naive_single_layer | 0.006094 | 0.500000 | 0.000e+00 | 6.040e-14 | 1.000000 | 3.707e-12 |
| incorrect_two_layer | 0.006094 | 0.472855 | 0.000e+00 | 6.162e-14 | 1.000000 | 5.206e-12 |
| ridge_least_squares | 0.006094 | 0.437421 | 0.000e+00 | 7.559e-14 | 1.000000 | 1.022e-11 |
| graph_kcl_aware | 0.006094 | 0.423701 | 0.000e+00 | 2.839e-17 | 1.000000 | 1.022e-11 |
| graph_kcl_differentiable_inverse | 0.006094 | 0.423701 | 0.000e+00 | 1.423e-19 | 1.000000 | 1.022e-11 |

## layer_misallocation_trap

| Method | current_rmse | misalloc | via_f1 | kcl_res | b_res | closure |
|---|---:|---:|---:|---:|---:|---:|
| naive_single_layer | 0.005476 | 0.140449 | 0.000e+00 | 1.372e-13 | 1.000000 | 8.874e-13 |
| incorrect_two_layer | 0.005476 | 0.132470 | 0.000e+00 | 1.382e-13 | 1.000000 | 1.273e-12 |
| ridge_least_squares | 0.005476 | 0.134403 | 0.000e+00 | 1.567e-13 | 1.000000 | 2.485e-12 |
| graph_kcl_aware | 0.005476 | 0.134064 | 0.000e+00 | 4.512e-17 | 1.000000 | 2.485e-12 |
| graph_kcl_differentiable_inverse | 0.005476 | 0.134064 | 0.000e+00 | 2.167e-19 | 1.000000 | 2.485e-12 |

Generated-domain benchmark only. Cannot claim real validation.