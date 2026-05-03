# Finite-Width / Return-Current Stress

- input gap to clean centerline field: `0.181`
- surrogate model: `finite-width filaments plus weak return-current surrogate`

| model | overall L2 | L2 ratio | topology MSE | topology ratio | s1 L2 | via hit | via F1 | leakage | physical B clean | physical B obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 0.264 | 1.000 | 4.594e-01 | 1.000 | 0.513 | 0.907 | 0.991 | 0.021 | 0.228 | 0.140 |
| `unet_topology_soft_loss` | 0.291 | 1.102 | 2.441e-01 | 0.531 | 0.628 | 0.944 | 0.986 | 0.025 | 0.233 | 0.153 |
| `unet_topology_two_stage_refined` | 0.295 | 1.117 | 2.448e-01 | 0.533 | 0.716 | 0.944 | 0.874 | 0.025 | 0.234 | 0.153 |
