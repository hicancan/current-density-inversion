# Layer Misallocation Comparison Table

| Baseline | L1 RMSE | L2 RMSE | L3 RMSE | L4 RMSE | Mean Misalloc |
|---|---:|---:|---:|---:|---:|
| naive_single_layer (nominal_via_chain) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3161 |
| incorrect_two_layer (nominal_via_chain) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3024 |
| graph_kcl_aware (nominal_via_chain) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.1704 |
| ridge_least_squares (nominal_via_chain) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.1768 |

| naive_single_layer (no_via_hard_negative) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3161 |
| incorrect_two_layer (no_via_hard_negative) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3082 |
| graph_kcl_aware (no_via_hard_negative) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.1955 |
| ridge_least_squares (no_via_hard_negative) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.1980 |

| naive_single_layer (dense_via_cluster) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3161 |
| incorrect_two_layer (dense_via_cluster) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3015 |
| graph_kcl_aware (dense_via_cluster) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.1478 |
| ridge_least_squares (dense_via_cluster) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.1654 |

| naive_single_layer (return_grid_bottleneck) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3124 |
| incorrect_two_layer (return_grid_bottleneck) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3056 |
| graph_kcl_aware (return_grid_bottleneck) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.2053 |
| ridge_least_squares (return_grid_bottleneck) | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.2003 |

| naive_single_layer (deep_layer_only) | 10.0000 | 0.000e+00 | 1.0000 | 1.0000 | 0.5000 |
| incorrect_two_layer (deep_layer_only) | 10.0000 | 0.000e+00 | 1.0000 | 1.0000 | 0.4729 |
| graph_kcl_aware (deep_layer_only) | 10.0000 | 10.0000 | 1.0000 | 1.0000 | 0.4237 |
| ridge_least_squares (deep_layer_only) | 10.0000 | 10.0000 | 1.0000 | 1.0000 | 0.4374 |

| naive_single_layer (layer_misallocation_trap) | 1.0000 | 0.000e+00 | 0.000e+00 | 1.0000 | 0.1404 |
| incorrect_two_layer (layer_misallocation_trap) | 1.0000 | 0.000e+00 | 0.000e+00 | 1.0000 | 0.1325 |
| graph_kcl_aware (layer_misallocation_trap) | 1.0000 | 10.0000 | 10.0000 | 1.0000 | 0.1341 |
| ridge_least_squares (layer_misallocation_trap) | 1.0000 | 10.0000 | 10.0000 | 1.0000 | 0.1344 |

Generated four-layer via-chain benchmark.
