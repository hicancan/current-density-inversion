# PyPEEC Held-Out Split Frozen Evaluation

- enabled: `True`
- current protocol: `frozen_no_calibration_split_report`
- used for current threshold selection: `False`
- used for current calibration: `False`
- boundary: Reports current frozen metrics by the reserved future calibration/test roles. No parameter is selected from these roles in this run.

| future role | model | cases | overall L2 | topology MSE | via recall | via F1 | no-via FP | physical B PyPEEC |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `future_calibration_candidate` | `unet_no_topology` | 115 | 0.828 | 1.369 | 0.921 | 0.674 | 0.981 | 0.982 |
| `future_calibration_candidate` | `unet_topology_soft_loss` | 115 | 0.832 | 0.811 | 0.952 | 0.698 | 0.942 | 0.821 |
| `future_calibration_candidate` | `unet_topology_two_stage_refined` | 115 | 0.829 | 0.775 | 0.683 | 0.597 | 0.731 | 0.817 |
| `future_heldout_test` | `unet_no_topology` | 285 | 0.797 | 1.291 | 0.825 | 0.587 | 0.912 | 0.962 |
| `future_heldout_test` | `unet_topology_soft_loss` | 285 | 0.808 | 0.769 | 0.854 | 0.591 | 0.959 | 0.791 |
| `future_heldout_test` | `unet_topology_two_stage_refined` | 285 | 0.806 | 0.727 | 0.672 | 0.549 | 0.716 | 0.788 |

Interpretation: these are frozen metrics stratified by the reserved future split. They do not perform PyPEEC calibration in the current run.
