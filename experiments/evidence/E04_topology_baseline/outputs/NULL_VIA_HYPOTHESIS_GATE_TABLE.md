# Null-Via Hypothesis Gate On Frozen PyPEEC Stress

- enabled: `True`
- calibration split: `val_synthetic_null_via_stress`
- used for PyPEEC threshold selection: `False`
- used for PyPEEC calibration: `False`
- boundary: Frozen PyPEEC evaluation of a gate selected only on synthetic validation stress.

## Topology Model Summary

- no-via FP before/after: `1.000` / `0.610`
- via recall before/after: `0.885` / `0.490`
- via F1 before/after: `0.939` / `0.658`
- dense-via F1 before/after: `1.000` / `0.316`
- return-path FP before/after: `0.000` / `0.000`
- topology MSE before/after: `0.781` / `0.834`
- physical B PyPEEC before/after: `0.800` / `0.798`

## Model/Subset Trade-Offs

| model | subset | cases | FP before | FP after | recall before | recall after | F1 before | F1 after | topology before | topology after | B PyPEEC before | B PyPEEC after |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | `canonical` | 105 | 0.333 | 0.333 | 0.755 | 0.627 | 0.856 | 0.766 | 0.420 | 0.419 | 1.642 | 1.646 |
| `unet_no_topology` | `exp03_like` | 295 | 0.939 | 0.741 | 0.959 | 0.520 | 0.499 | 0.346 | 1.631 | 1.640 | 0.912 | 0.911 |
| `unet_no_topology` | `via` | 200 | 0.000 | 0.000 | 0.855 | 0.575 | 0.922 | 0.730 | 0.947 | 0.964 | 1.123 | 1.122 |
| `unet_no_topology` | `no_via` | 200 | 1.000 | 0.735 | 0.000 | 0.000 | 0.000 | 0.000 | 1.680 | 1.674 | 0.891 | 0.890 |
| `unet_no_topology` | `dense_via` | 32 | 0.000 | 0.000 | 0.938 | 0.625 | 0.968 | 0.769 | 1.456 | 1.483 | 0.917 | 0.915 |
| `unet_no_topology` | `return_path` | 100 | 0.000 | 0.000 | 0.750 | 0.630 | 0.857 | 0.773 | 0.397 | 0.395 | 1.821 | 1.826 |
| `unet_topology_soft_loss` | `canonical` | 105 | 0.333 | 0.000 | 0.775 | 0.696 | 0.868 | 0.821 | 0.262 | 0.286 | 1.521 | 1.524 |
| `unet_topology_soft_loss` | `exp03_like` | 295 | 0.964 | 0.619 | 1.000 | 0.276 | 0.508 | 0.219 | 0.966 | 1.029 | 0.735 | 0.733 |
| `unet_topology_soft_loss` | `via` | 200 | 0.000 | 0.000 | 0.885 | 0.490 | 0.939 | 0.658 | 0.601 | 0.672 | 0.973 | 0.970 |
| `unet_topology_soft_loss` | `no_via` | 200 | 1.000 | 0.610 | 0.000 | 0.000 | 0.000 | 0.000 | 0.962 | 0.995 | 0.711 | 0.709 |
| `unet_topology_soft_loss` | `dense_via` | 32 | 0.000 | 0.000 | 1.000 | 0.188 | 1.000 | 0.316 | 0.935 | 1.043 | 0.777 | 0.772 |
| `unet_topology_soft_loss` | `return_path` | 100 | 0.000 | 0.000 | 0.770 | 0.690 | 0.870 | 0.817 | 0.254 | 0.275 | 1.689 | 1.692 |
| `unet_topology_two_stage_refined` | `canonical` | 105 | 0.333 | 0.000 | 0.539 | 0.510 | 0.696 | 0.675 | 0.237 | 0.282 | 1.518 | 1.526 |
| `unet_topology_two_stage_refined` | `exp03_like` | 295 | 0.726 | 0.574 | 0.816 | 0.439 | 0.498 | 0.339 | 0.920 | 0.997 | 0.732 | 0.731 |
| `unet_topology_two_stage_refined` | `via` | 200 | 0.000 | 0.000 | 0.675 | 0.475 | 0.806 | 0.644 | 0.574 | 0.648 | 0.969 | 0.970 |
| `unet_topology_two_stage_refined` | `no_via` | 200 | 1.000 | 0.565 | 0.000 | 0.000 | 0.000 | 0.000 | 0.907 | 0.970 | 0.708 | 0.708 |
| `unet_topology_two_stage_refined` | `dense_via` | 32 | 0.000 | 0.000 | 0.906 | 0.375 | 0.951 | 0.545 | 0.898 | 1.004 | 0.772 | 0.771 |
| `unet_topology_two_stage_refined` | `return_path` | 100 | 0.000 | 0.000 | 0.530 | 0.500 | 0.693 | 0.667 | 0.228 | 0.271 | 1.686 | 1.695 |

## Rejection Reasons

| model | reason | count |
|---|---|---:|
| `unet_no_topology` | `artifact-zone residual` | 73 |
| `unet_no_topology` | `low hypothesis score` | 22 |
| `unet_topology_soft_loss` | `artifact-zone residual` | 145 |
| `unet_topology_soft_loss` | `low hypothesis score` | 3 |
| `unet_topology_two_stage_refined` | `artifact-zone residual` | 70 |
| `unet_topology_two_stage_refined` | `low hypothesis score` | 1 |

Interpretation: this is a frozen PyPEEC evaluation of a gate selected on synthetic validation stress. It reports the false-positive/recall trade-off and should not be described as PyPEEC-calibrated.
