# WIN/LOSS BY METRIC

New method: **graph_kcl_differentiable_inverse**

| vs Baseline | Wins | Losses | Ties | Win Metrics | Loss Metrics |
|---|---:|---:|---:|---|---|
| naive_single_layer | 1 | 1 | 6 | layer_misallocation | runtime_s |
| incorrect_two_layer | 1 | 1 | 6 | layer_misallocation | runtime_s |
| ridge_least_squares | 1 | 1 | 6 | layer_misallocation | runtime_s |
| graph_kcl_aware | 0 | 1 | 7 |  | runtime_s |

Generated-domain benchmark only. Cannot claim real validation.