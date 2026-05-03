# Null-Via Hypothesis Gate On Frozen PyPEEC Stress

- enabled: `True`
- calibration split: `val_synthetic_null_via_stress`
- used for PyPEEC threshold selection: `False`
- used for PyPEEC calibration: `False`
- boundary: Frozen PyPEEC evaluation of a gate selected only on synthetic validation stress.

## Topology Model Summary

- no-via FP before/after: `1.000` / `0.605`
- via recall before/after: `0.910` / `0.630`
- via F1 before/after: `0.953` / `0.773`
- dense-via F1 before/after: `1.000` / `0.609`
- return-path FP before/after: `0.000` / `0.000`
- topology MSE before/after: `0.813` / `0.858`
- physical B PyPEEC before/after: `0.842` / `0.841`

## Model/Subset Trade-Offs

| model | subset | cases | FP before | FP after | recall before | recall after | F1 before | F1 after | topology before | topology after | B PyPEEC before | B PyPEEC after |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | `canonical` | 105 | 0.333 | 0.333 | 0.696 | 0.569 | 0.816 | 0.720 | 0.379 | 0.371 | 1.640 | 1.643 |
| `unet_no_topology` | `exp03_like` | 295 | 0.939 | 0.645 | 1.000 | 0.449 | 0.514 | 0.327 | 1.608 | 1.621 | 0.894 | 0.892 |
| `unet_no_topology` | `via` | 200 | 0.000 | 0.000 | 0.845 | 0.510 | 0.916 | 0.675 | 0.910 | 0.926 | 1.087 | 1.086 |
| `unet_no_topology` | `no_via` | 200 | 1.000 | 0.640 | 0.000 | 0.000 | 0.000 | 0.000 | 1.660 | 1.659 | 0.885 | 0.884 |
| `unet_no_topology` | `dense_via` | 32 | 0.000 | 0.000 | 1.000 | 0.438 | 1.000 | 0.609 | 1.450 | 1.462 | 0.904 | 0.901 |
| `unet_no_topology` | `return_path` | 100 | 0.000 | 0.000 | 0.700 | 0.580 | 0.824 | 0.734 | 0.353 | 0.345 | 1.807 | 1.811 |
| `unet_topology_soft_loss` | `canonical` | 105 | 0.333 | 0.000 | 0.824 | 0.745 | 0.898 | 0.854 | 0.292 | 0.313 | 1.776 | 1.780 |
| `unet_topology_soft_loss` | `exp03_like` | 295 | 0.949 | 0.614 | 1.000 | 0.510 | 0.512 | 0.372 | 0.998 | 1.051 | 0.752 | 0.750 |
| `unet_topology_soft_loss` | `via` | 200 | 0.000 | 0.000 | 0.910 | 0.630 | 0.953 | 0.773 | 0.613 | 0.662 | 1.045 | 1.045 |
| `unet_topology_soft_loss` | `no_via` | 200 | 1.000 | 0.605 | 0.000 | 0.000 | 0.000 | 0.000 | 1.013 | 1.053 | 0.736 | 0.735 |
| `unet_topology_soft_loss` | `dense_via` | 32 | 0.000 | 0.000 | 1.000 | 0.438 | 1.000 | 0.609 | 0.917 | 0.949 | 0.774 | 0.773 |
| `unet_topology_soft_loss` | `return_path` | 100 | 0.000 | 0.000 | 0.820 | 0.740 | 0.901 | 0.851 | 0.283 | 0.304 | 2.005 | 2.008 |
| `unet_topology_two_stage_refined` | `canonical` | 105 | 0.333 | 0.000 | 0.569 | 0.559 | 0.720 | 0.717 | 0.264 | 0.308 | 1.776 | 1.783 |
| `unet_topology_two_stage_refined` | `exp03_like` | 295 | 0.726 | 0.538 | 0.827 | 0.592 | 0.503 | 0.443 | 0.940 | 1.016 | 0.749 | 0.749 |
| `unet_topology_two_stage_refined` | `via` | 200 | 0.000 | 0.000 | 0.695 | 0.575 | 0.820 | 0.730 | 0.570 | 0.633 | 1.044 | 1.046 |
| `unet_topology_two_stage_refined` | `no_via` | 200 | 1.000 | 0.530 | 0.000 | 0.000 | 0.000 | 0.000 | 0.955 | 1.027 | 0.734 | 0.734 |
| `unet_topology_two_stage_refined` | `dense_via` | 32 | 0.000 | 0.000 | 0.906 | 0.625 | 0.951 | 0.769 | 0.853 | 0.914 | 0.772 | 0.772 |
| `unet_topology_two_stage_refined` | `return_path` | 100 | 0.000 | 0.000 | 0.570 | 0.560 | 0.726 | 0.718 | 0.257 | 0.298 | 2.005 | 2.013 |

## Rejection Reasons

| model | reason | count |
|---|---|---:|
| `unet_no_topology` | `artifact-zone residual` | 115 |
| `unet_no_topology` | `low hypothesis score` | 10 |
| `unet_topology_soft_loss` | `artifact-zone residual` | 120 |
| `unet_topology_soft_loss` | `low hypothesis score` | 3 |
| `unet_topology_two_stage_refined` | `artifact-zone residual` | 61 |
| `unet_topology_two_stage_refined` | `low hypothesis score` | 1 |

Interpretation: this is a frozen PyPEEC evaluation of a gate selected on synthetic validation stress. It reports the false-positive/recall trade-off and should not be described as PyPEEC-calibrated.
