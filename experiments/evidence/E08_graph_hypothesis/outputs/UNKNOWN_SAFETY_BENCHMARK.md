# Exp08 P2 unknown-safety benchmark

| signal | safety status | clean false reject | hidden reject | accepted clean | accepted hidden | accepted clean acc | accepted hidden acc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| margin_only | diagnostic_only | 0.2000 | 0.6354 | 80 | 35 | 0.9000 | 0.6000 |
| residual_only | diagnostic_only | 0.2000 | 0.2812 | 80 | 69 | 0.9250 | 0.4493 |
| margin_over_residual | diagnostic_only | 0.2000 | 0.6771 | 80 | 31 | 0.9125 | 0.5806 |
| registration_instability | fails_clean_reject_budget | 0.4700 | 0.3333 | 53 | 64 | 0.8868 | 0.4375 |
| prediction_disagreement | fails_clean_reject_budget | 1.0000 | 1.0000 | 0 | 0 | nan | nan |
| evidence_entropy | diagnostic_only | 0.2000 | 0.6354 | 80 | 35 | 0.9375 | 0.5714 |
| residual_gap_ambiguity | diagnostic_only | 0.2000 | 0.5208 | 80 | 46 | 0.8750 | 0.5000 |
| h0_h1_score_ambiguity | diagnostic_only | 0.2000 | 0.1458 | 80 | 82 | 0.8625 | 0.4634 |
| residual_score_disagreement | fails_clean_reject_budget | 0.2100 | 0.5938 | 79 | 39 | 0.8861 | 0.5641 |
| combined_unknown_score | usable_screen | 0.2000 | 0.6771 | 80 | 31 | 0.9375 | 0.7742 |
| combined_physical_unknown_score | diagnostic_only | 0.2000 | 0.6979 | 80 | 29 | 0.9000 | 0.6552 |

A usable screen must stay within the clean false-reject budget while rejecting many hidden mechanisms and preserving accepted-case accuracy. This is a safety diagnostic, not a deployed refusal policy.
