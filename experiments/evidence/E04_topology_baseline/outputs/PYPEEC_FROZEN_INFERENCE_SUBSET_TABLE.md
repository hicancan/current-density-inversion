# Real PyPEEC Frozen Inference Subset Stress

| subset | cases | input gap | model | overall L2 | L2 ratio | topology MSE | topology ratio | s1 RMSE | via hit | via F1 | no-via FP | physical B PyPEEC |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `canonical` | 105 | 0.298 | `unet_no_topology` | 0.830 | 1.000 | 3.785e-01 | 1.000 | 0.052 | 0.824 | 0.816 | 0.333 | 1.640 |
| `canonical` | 105 | 0.298 | `unet_topology_soft_loss` | 0.833 | 1.003 | 2.918e-01 | 0.771 | 0.049 | 0.696 | 0.898 | 0.333 | 1.776 |
| `canonical` | 105 | 0.298 | `unet_topology_two_stage_refined` | 0.833 | 1.003 | 2.642e-01 | 0.698 | 0.050 | 0.833 | 0.720 | 0.333 | 1.776 |
| `exp03_like` | 295 | 0.188 | `unet_no_topology` | 0.806 | 1.000 | 1.608e+00 | 1.000 | 0.061 | 0.531 | 0.514 | 0.939 | 0.894 |
| `exp03_like` | 295 | 0.188 | `unet_topology_soft_loss` | 0.782 | 0.971 | 9.984e-01 | 0.621 | 0.059 | 0.520 | 0.512 | 0.949 | 0.752 |
| `exp03_like` | 295 | 0.188 | `unet_topology_two_stage_refined` | 0.778 | 0.966 | 9.399e-01 | 0.584 | 0.055 | 0.520 | 0.503 | 0.726 | 0.749 |
| `via` | 200 | 0.186 | `unet_no_topology` | 0.817 | 1.000 | 9.104e-01 | 1.000 | 0.074 | 0.680 | 0.916 | 0.000 | 1.087 |
| `via` | 200 | 0.186 | `unet_topology_soft_loss` | 0.803 | 0.983 | 6.126e-01 | 0.673 | 0.072 | 0.610 | 0.953 | 0.000 | 1.045 |
| `via` | 200 | 0.186 | `unet_topology_two_stage_refined` | 0.803 | 0.983 | 5.704e-01 | 0.627 | 0.073 | 0.680 | 0.820 | 0.000 | 1.044 |
| `no_via` | 200 | 0.199 | `unet_no_topology` | 0.808 | 1.000 | 1.660e+00 | 1.000 | 0.038 | 1.000 | 0.000 | 1.000 | 0.885 |
| `no_via` | 200 | 0.199 | `unet_topology_soft_loss` | 0.791 | 0.978 | 1.013e+00 | 0.610 | 0.035 | 1.000 | 0.000 | 1.000 | 0.736 |
| `no_via` | 200 | 0.199 | `unet_topology_two_stage_refined` | 0.784 | 0.970 | 9.546e-01 | 0.575 | 0.023 | 1.000 | 0.000 | 1.000 | 0.734 |
| `dense_via` | 32 | 0.173 | `unet_no_topology` | 0.856 | 1.000 | 1.450e+00 | 1.000 | 0.118 | 0.500 | 1.000 | 0.000 | 0.904 |
| `dense_via` | 32 | 0.173 | `unet_topology_soft_loss` | 0.834 | 0.975 | 9.171e-01 | 0.633 | 0.117 | 0.562 | 1.000 | 0.000 | 0.774 |
| `dense_via` | 32 | 0.173 | `unet_topology_two_stage_refined` | 0.832 | 0.972 | 8.534e-01 | 0.589 | 0.116 | 0.562 | 0.951 | 0.000 | 0.772 |
| `return_path` | 100 | 0.347 | `unet_no_topology` | 0.836 | 1.000 | 3.530e-01 | 1.000 | 0.053 | 0.830 | 0.824 | 0.000 | 1.807 |
| `return_path` | 100 | 0.347 | `unet_topology_soft_loss` | 0.839 | 1.004 | 2.835e-01 | 0.803 | 0.050 | 0.700 | 0.901 | 0.000 | 2.005 |
| `return_path` | 100 | 0.347 | `unet_topology_two_stage_refined` | 0.839 | 1.004 | 2.567e-01 | 0.727 | 0.050 | 0.840 | 0.726 | 0.000 | 2.005 |

Boundary: subset rows are descriptive diagnostics over the current exp07 mini distribution. They are not validation-selected thresholds and should not be treated as a broad PyPEEC distribution proof.
