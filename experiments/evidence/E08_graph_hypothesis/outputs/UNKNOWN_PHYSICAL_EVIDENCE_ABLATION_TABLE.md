# Exp08 P2 physical-evidence unknown/OOD ablation

| signal | clean threshold | clean false reject | hidden reject | accepted clean | accepted hidden | accepted clean acc | accepted hidden acc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| evidence_entropy | 0.5801 | 0.2000 | 0.6354 | 80 | 35 | 0.9375 | 0.5714 |
| residual_gap_ambiguity | 3.897e+03 | 0.2000 | 0.5208 | 80 | 46 | 0.8750 | 0.5000 |
| h0_h1_score_ambiguity | -3.066e-04 | 0.2000 | 0.1458 | 80 | 82 | 0.8625 | 0.4634 |
| residual_score_disagreement | 1.0000 | 0.2100 | 0.5938 | 79 | 39 | 0.8861 | 0.5641 |
| combined_physical_unknown_score | 1.5819 | 0.2000 | 0.6979 | 80 | 29 | 0.9000 | 0.6552 |

These signals use model-evidence entropy, residual ambiguity, H0/H1 score ambiguity, and residual-vs-score disagreement. Thresholds are still clean-validation only.
