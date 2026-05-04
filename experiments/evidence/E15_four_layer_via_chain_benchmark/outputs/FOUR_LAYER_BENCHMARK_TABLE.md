# Four-Layer Via-Chain Benchmark Table

| Baseline | Mean L2 RMSE | Mean L3 RMSE | Mean L4 RMSE | Mean Topo Res | Mean KCL Res | Mean B Res | Mean Misalloc |
|---|---:|---:|---:|---:|---:|---:|---:|
| naive_single_layer | 0.6667 | 0.8333 | 1.0000 | 1.373e-13 | 1.373e-13 | 1.0000 | 0.3169 |
| incorrect_two_layer | 0.6667 | 0.8333 | 1.0000 | 1.386e-13 | 1.386e-13 | 1.0000 | 0.3038 |
| graph_kcl_aware | 4.0000 | 2.5000 | 1.0000 | 4.920e-17 | 4.920e-17 | 1.0000 | 0.2128 |
| ridge_least_squares | 4.0000 | 2.5000 | 1.0000 | 1.589e-13 | 1.589e-13 | 1.0000 | 0.2187 |

Generated four-layer via-chain benchmark.
