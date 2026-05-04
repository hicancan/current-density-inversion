# Real PyPEEC Frozen Inference Subset Stress

| subset | cases | input gap | model | overall L2 | L2 ratio | topology MSE | topology ratio | s1 RMSE | via hit | via F1 | no-via FP | physical B PyPEEC |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `canonical` | 105 | 0.298 | `unet_no_topology` | 0.831 | 1.000 | 4.204e-01 | 1.000 | 0.050 | 0.931 | 0.856 | 0.333 | 1.642 |
| `canonical` | 105 | 0.298 | `unet_topology_soft_loss` | 0.843 | 1.015 | 2.625e-01 | 0.624 | 0.049 | 0.755 | 0.868 | 0.333 | 1.521 |
| `canonical` | 105 | 0.298 | `unet_topology_two_stage_refined` | 0.844 | 1.016 | 2.370e-01 | 0.564 | 0.050 | 0.804 | 0.696 | 0.333 | 1.518 |
| `exp03_like` | 295 | 0.188 | `unet_no_topology` | 0.796 | 1.000 | 1.631e+00 | 1.000 | 0.061 | 0.520 | 0.499 | 0.939 | 0.912 |
| `exp03_like` | 295 | 0.188 | `unet_topology_soft_loss` | 0.803 | 1.010 | 9.658e-01 | 0.592 | 0.060 | 0.551 | 0.508 | 0.964 | 0.735 |
| `exp03_like` | 295 | 0.188 | `unet_topology_two_stage_refined` | 0.799 | 1.004 | 9.200e-01 | 0.564 | 0.056 | 0.551 | 0.498 | 0.726 | 0.732 |
| `via` | 200 | 0.186 | `unet_no_topology` | 0.818 | 1.000 | 9.475e-01 | 1.000 | 0.073 | 0.730 | 0.922 | 0.000 | 1.123 |
| `via` | 200 | 0.186 | `unet_topology_soft_loss` | 0.822 | 1.005 | 6.006e-01 | 0.634 | 0.072 | 0.655 | 0.939 | 0.000 | 0.973 |
| `via` | 200 | 0.186 | `unet_topology_two_stage_refined` | 0.822 | 1.006 | 5.740e-01 | 0.606 | 0.073 | 0.680 | 0.806 | 0.000 | 0.969 |
| `no_via` | 200 | 0.199 | `unet_no_topology` | 0.792 | 1.000 | 1.680e+00 | 1.000 | 0.038 | 1.000 | 0.000 | 1.000 | 0.891 |
| `no_via` | 200 | 0.199 | `unet_topology_soft_loss` | 0.807 | 1.019 | 9.617e-01 | 0.573 | 0.036 | 1.000 | 0.000 | 1.000 | 0.711 |
| `no_via` | 200 | 0.199 | `unet_topology_two_stage_refined` | 0.800 | 1.011 | 9.074e-01 | 0.540 | 0.024 | 1.000 | 0.000 | 1.000 | 0.708 |
| `dense_via` | 32 | 0.173 | `unet_no_topology` | 0.852 | 1.000 | 1.456e+00 | 1.000 | 0.120 | 0.438 | 0.968 | 0.000 | 0.917 |
| `dense_via` | 32 | 0.173 | `unet_topology_soft_loss` | 0.864 | 1.014 | 9.347e-01 | 0.642 | 0.117 | 0.594 | 1.000 | 0.000 | 0.777 |
| `dense_via` | 32 | 0.173 | `unet_topology_two_stage_refined` | 0.862 | 1.012 | 8.977e-01 | 0.617 | 0.116 | 0.594 | 0.951 | 0.000 | 0.772 |
| `return_path` | 100 | 0.347 | `unet_no_topology` | 0.836 | 1.000 | 3.966e-01 | 1.000 | 0.051 | 0.930 | 0.857 | 0.000 | 1.821 |
| `return_path` | 100 | 0.347 | `unet_topology_soft_loss` | 0.850 | 1.016 | 2.536e-01 | 0.639 | 0.050 | 0.750 | 0.870 | 0.000 | 1.689 |
| `return_path` | 100 | 0.347 | `unet_topology_two_stage_refined` | 0.850 | 1.017 | 2.276e-01 | 0.574 | 0.051 | 0.800 | 0.693 | 0.000 | 1.686 |

Boundary: subset rows are descriptive diagnostics over the current exp07 mini distribution. They are not validation-selected thresholds and should not be treated as a broad PyPEEC distribution proof.
