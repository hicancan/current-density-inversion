# Real PyPEEC Return-Path Mechanism Summary

This table splits return-path magnetic consistency failures into amplitude, spatial-shape, layer-allocation, and mixed mechanisms. It is descriptive failure analysis, not a model update.

| model | mechanism | count | % cases | raw B | shape B | scalar fit | amplitude log error | alloc err | return L2 | topology MSE |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | `amplitude mismatch` | 56 | 0.560 | 1.427 | 0.582 | 0.396 | 0.946 | 0.242 | 0.956 | 0.395 |
| `unet_no_topology` | `layer-allocation mismatch` | 42 | 0.420 | 2.234 | 0.483 | 0.287 | 1.251 | 0.420 | 0.986 | 0.294 |
| `unet_no_topology` | `spatial-shape mismatch` | 2 | 0.020 | 1.868 | 0.909 | 0.204 | 1.591 | 0.063 | 1.029 | 0.408 |
| `unet_topology_soft_loss` | `amplitude mismatch` | 46 | 0.460 | 1.627 | 0.568 | 0.368 | 1.022 | 0.223 | 1.062 | 0.307 |
| `unet_topology_soft_loss` | `layer-allocation mismatch` | 54 | 0.540 | 2.286 | 0.449 | 0.294 | 1.246 | 0.399 | 0.966 | 0.263 |
| `unet_topology_two_stage_refined` | `amplitude mismatch` | 46 | 0.460 | 1.629 | 0.569 | 0.368 | 1.023 | 0.223 | 1.062 | 0.288 |
| `unet_topology_two_stage_refined` | `layer-allocation mismatch` | 54 | 0.540 | 2.287 | 0.449 | 0.294 | 1.246 | 0.399 | 0.966 | 0.230 |

Interpretation: raw B residual separates magnetic consistency from pixel-space current error; scalar-fitted shape residual distinguishes amplitude mismatch from spatial-shape mismatch.
