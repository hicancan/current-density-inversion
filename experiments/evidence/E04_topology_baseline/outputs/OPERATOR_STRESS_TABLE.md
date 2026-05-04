# Finite-Width / Return-Current Stress

- input gap to clean centerline field: `0.181`
- surrogate model: `finite-width filaments plus weak return-current surrogate`

| model | overall L2 | L2 ratio | topology MSE | topology ratio | s1 L2 | via hit | via F1 | leakage | physical B clean | physical B obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 0.265 | 1.000 | 4.547e-01 | 1.000 | 0.525 | 0.953 | 0.991 | 0.022 | 0.229 | 0.143 |
| `unet_topology_soft_loss` | 0.311 | 1.173 | 2.587e-01 | 0.569 | 0.700 | 0.916 | 0.976 | 0.033 | 0.229 | 0.162 |
| `unet_topology_two_stage_refined` | 0.313 | 1.182 | 2.604e-01 | 0.573 | 0.756 | 0.916 | 0.856 | 0.033 | 0.229 | 0.161 |
