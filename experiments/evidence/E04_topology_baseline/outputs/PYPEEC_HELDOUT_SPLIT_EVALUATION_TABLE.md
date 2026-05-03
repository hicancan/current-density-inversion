# PyPEEC Held-Out Split Frozen Evaluation

- enabled: `True`
- current protocol: `frozen_no_calibration_split_report`
- used for current threshold selection: `False`
- used for current calibration: `False`
- boundary: Reports current frozen metrics by the reserved future calibration/test roles. No parameter is selected from these roles in this run.

| future role | model | cases | overall L2 | topology MSE | via recall | via F1 | no-via FP | physical B PyPEEC |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `future_calibration_candidate` | `unet_no_topology` | 115 | 0.838 | 1.340 | 0.905 | 0.671 | 0.962 | 0.957 |
| `future_calibration_candidate` | `unet_topology_soft_loss` | 115 | 0.799 | 0.831 | 0.952 | 0.694 | 0.962 | 0.839 |
| `future_calibration_candidate` | `unet_topology_two_stage_refined` | 115 | 0.796 | 0.775 | 0.794 | 0.654 | 0.769 | 0.837 |
| `future_heldout_test` | `unet_no_topology` | 285 | 0.803 | 1.263 | 0.818 | 0.582 | 0.919 | 0.949 |
| `future_heldout_test` | `unet_topology_soft_loss` | 285 | 0.797 | 0.806 | 0.891 | 0.615 | 0.932 | 0.844 |
| `future_heldout_test` | `unet_topology_two_stage_refined` | 285 | 0.794 | 0.758 | 0.650 | 0.539 | 0.703 | 0.842 |

Interpretation: these are frozen metrics stratified by the reserved future split. They do not perform PyPEEC calibration in the current run.
