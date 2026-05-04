# E13 Observability Table

Generated-domain multi-height / multi-state / multi-component observability metrics.

| Heights | N States | Components | Eff Rank | Cond # | Margin | Via AUC | Layer Err (no prior) | Layer Err (w/ prior) | Return Conf |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| single | 1 | Bz | 10.7 | 2519.969 | 0.002 | 0.205 | 0.233 | 0.166 | 0.017 |
| single | 1 | Bxy | 10.7 | 1716.881 | 0.002 | 0.273 | 0.238 | 0.163 | 0.018 |
| single | 1 | Bxyz | 10.7 | 1600.389 | 0.002 | 0.268 | 0.237 | 0.164 | 0.018 |
| single | 2 | Bz | 10.7 | 2519.969 | 0.002 | 0.247 | 0.237 | 0.167 | 0.017 |
| single | 2 | Bxy | 10.7 | 1716.881 | 0.002 | 0.253 | 0.231 | 0.166 | 0.018 |
| single | 2 | Bxyz | 10.7 | 1600.389 | 0.002 | 0.223 | 0.236 | 0.166 | 0.018 |
| single | 4 | Bz | 10.7 | 2519.969 | 0.002 | 0.268 | 0.231 | 0.167 | 0.017 |
| single | 4 | Bxy | 10.7 | 1716.881 | 0.002 | 0.367 | 0.230 | 0.166 | 0.018 |
| single | 4 | Bxyz | 10.7 | 1600.389 | 0.002 | 0.270 | 0.231 | 0.169 | 0.018 |
| dual | 1 | Bz | 10.7 | 2771.491 | 0.001 | 0.237 | 0.239 | 0.166 | 0.017 |
| dual | 1 | Bxy | 10.7 | 1926.430 | 0.002 | 0.307 | 0.232 | 0.169 | 0.018 |
| dual | 1 | Bxyz | 10.7 | 1781.010 | 0.002 | 0.235 | 0.235 | 0.169 | 0.018 |
| dual | 2 | Bz | 10.7 | 2771.491 | 0.002 | 0.210 | 0.233 | 0.166 | 0.017 |
| dual | 2 | Bxy | 10.7 | 1926.430 | 0.002 | 0.163 | 0.231 | 0.167 | 0.018 |
| dual | 2 | Bxyz | 10.7 | 1781.010 | 0.002 | 0.347 | 0.232 | 0.168 | 0.018 |
| dual | 4 | Bz | 10.7 | 2771.491 | 0.002 | 0.287 | 0.233 | 0.166 | 0.017 |
| dual | 4 | Bxy | 10.7 | 1926.430 | 0.002 | 0.233 | 0.235 | 0.165 | 0.018 |
| dual | 4 | Bxyz | 10.7 | 1781.010 | 0.003 | 0.355 | 0.230 | 0.166 | 0.018 |
| triple | 1 | Bz | 10.7 | 2859.807 | 0.002 | 0.333 | 0.233 | 0.166 | 0.017 |
| triple | 1 | Bxy | 10.7 | 2031.235 | 0.002 | 0.240 | 0.235 | 0.165 | 0.018 |
| triple | 1 | Bxyz | 10.7 | 1869.056 | 0.002 | 0.233 | 0.240 | 0.168 | 0.018 |
| triple | 2 | Bz | 10.7 | 2859.807 | 0.002 | 0.383 | 0.231 | 0.166 | 0.017 |
| triple | 2 | Bxy | 10.7 | 2031.235 | 0.002 | 0.285 | 0.233 | 0.168 | 0.018 |
| triple | 2 | Bxyz | 10.7 | 1869.056 | 0.002 | 0.128 | 0.234 | 0.166 | 0.018 |
| triple | 4 | Bz | 10.7 | 2859.807 | 0.002 | 0.275 | 0.231 | 0.165 | 0.017 |
| triple | 4 | Bxy | 10.7 | 2031.235 | 0.002 | 0.282 | 0.235 | 0.164 | 0.018 |
| triple | 4 | Bxyz | 10.7 | 1869.056 | 0.002 | 0.258 | 0.235 | 0.167 | 0.018 |

## Acceptance Gates

| Gate | Status |
|---|---|
| multi_height_effective_rank_not_worse_than_single | PASS |
| multi_height_condition_improves_or_separability_improves | PASS |
| multi_state_hypothesis_margin_improves | PASS |
| Bxyz_not_worse_than_Bz_only | PASS |
| graph_prior_reduces_layer_misallocation | PASS |
| no_leakage_protocol_documented | PASS |

All gates passed: **True**

Case count: 40, Configurations evaluated: 27

All results are generated-domain only. Cannot claim real multilayer recovery or real QDM/NV validation.
