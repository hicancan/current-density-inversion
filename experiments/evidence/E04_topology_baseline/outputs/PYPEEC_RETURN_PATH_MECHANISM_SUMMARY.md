# Real PyPEEC Return-Path Mechanism Summary

This table splits return-path magnetic consistency failures into amplitude, spatial-shape, layer-allocation, and mixed mechanisms. It is descriptive failure analysis, not a model update.

| model | mechanism | count | % cases | raw B | shape B | scalar fit | amplitude log error | alloc err | return L2 | topology MSE |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | `amplitude mismatch` | 68 | 0.680 | 1.521 | 0.528 | 0.384 | 0.976 | 0.230 | 0.980 | 0.405 |
| `unet_no_topology` | `layer-allocation mismatch` | 32 | 0.320 | 2.312 | 0.470 | 0.287 | 1.262 | 0.398 | 0.995 | 0.379 |
| `unet_topology_soft_loss` | `amplitude mismatch` | 70 | 0.700 | 1.492 | 0.559 | 0.398 | 0.949 | 0.206 | 1.000 | 0.276 |
| `unet_topology_soft_loss` | `layer-allocation mismatch` | 25 | 0.250 | 2.220 | 0.466 | 0.292 | 1.237 | 0.407 | 0.977 | 0.208 |
| `unet_topology_soft_loss` | `spatial-shape mismatch` | 2 | 0.020 | 1.487 | 0.918 | 0.253 | 1.377 | 0.301 | 1.051 | 0.230 |
| `unet_topology_soft_loss` | `strong return operator gap` | 3 | 0.030 | 0.715 | 0.637 | 0.703 | 0.353 | 0.083 | 1.066 | 0.125 |
| `unet_topology_two_stage_refined` | `amplitude mismatch` | 70 | 0.700 | 1.495 | 0.559 | 0.398 | 0.950 | 0.206 | 1.000 | 0.244 |
| `unet_topology_two_stage_refined` | `layer-allocation mismatch` | 25 | 0.250 | 2.210 | 0.461 | 0.293 | 1.233 | 0.407 | 0.977 | 0.198 |
| `unet_topology_two_stage_refined` | `spatial-shape mismatch` | 2 | 0.020 | 1.481 | 0.918 | 0.255 | 1.370 | 0.301 | 1.051 | 0.227 |
| `unet_topology_two_stage_refined` | `strong return operator gap` | 3 | 0.030 | 0.712 | 0.635 | 0.706 | 0.348 | 0.083 | 1.066 | 0.101 |

Interpretation: raw B residual separates magnetic consistency from pixel-space current error; scalar-fitted shape residual distinguishes amplitude mismatch from spatial-shape mismatch.
