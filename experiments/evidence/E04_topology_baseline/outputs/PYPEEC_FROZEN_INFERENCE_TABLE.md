# Real PyPEEC Frozen Inference Stress

- artifact available: `True`
- split: `pypeec_test`
- cases: `400`
- exp03-like cases: `295`
- input gap PyPEEC vs centerline: `0.194978`
- topology/no-topology topology MSE ratio: `0.594694`
- topology/no-topology overall L2 ratio: `1.01129`
- used for training: `False`
- used for validation thresholds: `False`
- used for calibration: `False`

| model | overall L2 | L2 ratio | topology MSE | topology ratio | s1 L2 | via hit | via F1 | no-via FP | leakage | physical B center | physical B PyPEEC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 0.806 | 1.000 | 1.314e+00 | 1.000 | 1.042 | 0.730 | 0.614 | 0.930 | 0.322 | 0.920 | 0.968 |
| `unet_topology_soft_loss` | 0.815 | 1.011 | 7.811e-01 | 0.595 | 1.020 | 0.655 | 0.623 | 0.955 | 0.380 | 0.766 | 0.800 |
| `unet_topology_two_stage_refined` | 0.812 | 1.008 | 7.407e-01 | 0.564 | 0.969 | 0.680 | 0.564 | 0.720 | 0.380 | 0.762 | 0.796 |

Boundary: this is frozen inference on the exp07 mini PyPEEC dataset. No PyPEEC samples are used for training, validation threshold selection, or calibration.
