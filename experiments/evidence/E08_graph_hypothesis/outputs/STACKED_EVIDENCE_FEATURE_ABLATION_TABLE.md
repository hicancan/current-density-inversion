# Exp08 P1 stacked evidence feature ablation

| feature policy | n features | repeats | heldout 4-way mean | heldout 4-way std | heldout H0 mean | heldout H1 mean | heldout H2 mean | heldout H3 mean | heldout H0 false-any mean | heldout objective mean | heldout objective std | alpha counts | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| h0_conservative_all_basis | 66 | 31 | 0.9958 | 0.0058 | 1.0000 | 0.9832 | 1.0000 | 1.0000 | 0.0000 | 3.7799 | 0.0280 |  | breakthrough_candidate |
| all_features | 396 | 31 | 0.9963 | 0.0036 | 0.9935 | 0.9916 | 1.0000 | 1.0000 | 0.0065 | 3.7564 | 0.0552 |  | breakthrough_candidate |
| no_return_bank | 330 | 31 | 0.9956 | 0.0038 | 0.9903 | 0.9923 | 1.0000 | 1.0000 | 0.0097 | 3.7404 | 0.0641 |  | breakthrough_candidate |
| no_distributed_via | 330 | 31 | 0.9956 | 0.0035 | 0.9903 | 0.9923 | 1.0000 | 1.0000 | 0.0097 | 3.7404 | 0.0628 |  | breakthrough_candidate |
| no_artifact_bank | 330 | 31 | 0.9950 | 0.0036 | 0.9877 | 0.9923 | 1.0000 | 1.0000 | 0.0123 | 3.7270 | 0.0665 |  | breakthrough_candidate |
| no_finite_width_sheet | 330 | 31 | 0.9795 | 0.0118 | 1.0000 | 0.9181 | 1.0000 | 1.0000 | 0.0000 | 3.7017 | 0.0566 |  | breakthrough_candidate |
| finite_width_all_evidence | 66 | 31 | 0.9927 | 0.0046 | 0.9787 | 0.9923 | 1.0000 | 1.0000 | 0.0213 | 3.6800 | 0.0833 |  | breakthrough_candidate |
| finite_width_h0_conservative_only | 11 | 31 | 0.9648 | 0.0435 | 0.9826 | 0.8768 | 1.0000 | 1.0000 | 0.0174 | 3.5615 | 0.2664 |  | h1_recall_limited |
| margin_residual_nbasis_only | 108 | 31 | 0.9342 | 0.0249 | 0.9994 | 0.7374 | 1.0000 | 1.0000 | 6.452e-04 | 3.4815 | 0.1188 |  | h1_recall_limited |
| scores_plus_margin | 180 | 31 | 0.9210 | 0.0194 | 1.0000 | 0.6839 | 1.0000 | 1.0000 | 0.0000 | 3.4206 | 0.0929 |  | h1_recall_limited |
| scores_only | 144 | 31 | 0.9116 | 0.0177 | 1.0000 | 0.6465 | 1.0000 | 1.0000 | 0.0000 | 3.3757 | 0.0850 |  | h1_recall_limited |
| pred_one_hot_only | 144 | 31 | 0.9773 | 0.0066 | 0.9103 | 0.9987 | 1.0000 | 1.0000 | 0.0897 | 3.3321 | 0.1423 |  | h0_safety_watch |
| scores_plus_residual | 180 | 31 | 0.8918 | 0.0173 | 0.7206 | 0.8465 | 1.0000 | 1.0000 | 0.2794 | 2.1631 | 0.3528 |  | h1_recall_limited |

All rows use fixed alpha=100 and repeated PyPEEC calibration/held-out splits. This ablation identifies whether the breakthrough comes from scores, margins, predicted one-hot outputs, or specific basis families.
