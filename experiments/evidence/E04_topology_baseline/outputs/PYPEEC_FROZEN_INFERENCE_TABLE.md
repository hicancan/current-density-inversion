# Real PyPEEC Frozen Inference Stress

- artifact available: `True`
- split: `pypeec_test`
- cases: `400`
- exp03-like cases: `295`
- input gap PyPEEC vs centerline: `0.194978`
- topology/no-topology topology MSE ratio: `0.632436`
- topology/no-topology overall L2 ratio: `0.980681`
- used for training: `False`
- used for validation thresholds: `False`
- used for calibration: `False`

| model | overall L2 | L2 ratio | topology MSE | topology ratio | s1 L2 | via hit | via F1 | no-via FP | leakage | physical B center | physical B PyPEEC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unet_no_topology` | 0.813 | 1.000 | 1.285e+00 | 1.000 | 1.045 | 0.680 | 0.609 | 0.930 | 0.335 | 0.904 | 0.951 |
| `unet_topology_soft_loss` | 0.797 | 0.981 | 8.129e-01 | 0.632 | 1.013 | 0.610 | 0.639 | 0.940 | 0.350 | 0.806 | 0.842 |
| `unet_topology_two_stage_refined` | 0.795 | 0.977 | 7.625e-01 | 0.593 | 0.962 | 0.680 | 0.576 | 0.720 | 0.350 | 0.804 | 0.840 |

Boundary: this is frozen inference on the exp07 mini PyPEEC dataset. No PyPEEC samples are used for training, validation threshold selection, or calibration.
