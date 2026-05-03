# Exp08 P3 unknown/OOD detector ablation

| signal | clean threshold | clean false reject | hidden reject | accepted clean | accepted hidden | accepted clean acc | accepted hidden acc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| margin_only | -4.869e-04 | 0.2000 | 0.6354 | 80 | 35 | 0.9000 | 0.6000 |
| residual_only | 0.1921 | 0.2000 | 0.2812 | 80 | 69 | 0.9250 | 0.4493 |
| margin_over_residual | -0.0049 | 0.2000 | 0.6771 | 80 | 31 | 0.9125 | 0.5806 |
| registration_instability | 3.394e-04 | 0.4700 | 0.3333 | 53 | 64 | 0.8868 | 0.4375 |
| prediction_disagreement | 0.0000 | 1.0000 | 1.0000 | 0 | 0 | nan | nan |
| evidence_entropy | 0.5801 | 0.2000 | 0.6354 | 80 | 35 | 0.9375 | 0.5714 |
| residual_gap_ambiguity | 3.897e+03 | 0.2000 | 0.5208 | 80 | 46 | 0.8750 | 0.5000 |
| h0_h1_score_ambiguity | -3.066e-04 | 0.2000 | 0.1458 | 80 | 82 | 0.8625 | 0.4634 |
| residual_score_disagreement | 1.0000 | 0.2100 | 0.5938 | 79 | 39 | 0.8861 | 0.5641 |
| combined_unknown_score | 1.1972 | 0.2000 | 0.6771 | 80 | 31 | 0.9375 | 0.7742 |
| combined_physical_unknown_score | 1.5819 | 0.2000 | 0.6979 | 80 | 29 | 0.9000 | 0.6552 |

Thresholds target the configured clean false-reject rate on clean OOD rows. Hidden rows are never used to select thresholds.
