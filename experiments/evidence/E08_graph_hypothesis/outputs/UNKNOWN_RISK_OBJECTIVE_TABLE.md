# Exp08 P2 accepted-risk objective ranking

| signal | objective status | risk objective | clean false reject | hidden accept rate | accepted hidden risk | accepted clean acc | accepted hidden acc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| combined_unknown_score | diagnostic_only | 0.5974 | 0.2000 | 0.3229 | 0.2258 | 0.9375 | 0.7742 |
| combined_physical_unknown_score | diagnostic_only | 0.7938 | 0.2000 | 0.3021 | 0.3448 | 0.9000 | 0.6552 |
| margin_over_residual | diagnostic_only | 0.9846 | 0.2000 | 0.3229 | 0.4194 | 0.9125 | 0.5806 |
| margin_only | diagnostic_only | 1.0292 | 0.2000 | 0.3646 | 0.4000 | 0.9000 | 0.6000 |
| evidence_entropy | diagnostic_only | 1.0864 | 0.2000 | 0.3646 | 0.4286 | 0.9375 | 0.5714 |
| residual_score_disagreement | fails_clean_budget | 1.2142 | 0.2100 | 0.4062 | 0.4359 | 0.8861 | 0.5641 |
| residual_gap_ambiguity | diagnostic_only | 1.4584 | 0.2000 | 0.4792 | 0.5000 | 0.8750 | 0.5000 |
| residual_only | diagnostic_only | 2.0390 | 0.2000 | 0.7188 | 0.5507 | 0.9250 | 0.4493 |
| h0_h1_score_ambiguity | diagnostic_only | 2.2816 | 0.2000 | 0.8542 | 0.5366 | 0.8625 | 0.4634 |
| registration_instability | fails_clean_budget | 2.7684 | 0.4700 | 0.6667 | 0.5625 | 0.8868 | 0.4375 |
| prediction_disagreement | fails_clean_budget | nan | 1.0000 | 0.0000 | nan | nan | nan |

Rows rank fixed clean-thresholded unknown signals by accepted-hidden risk, hidden accept rate, and clean false-reject budget. Hidden rows are not used to choose thresholds; they only evaluate the frozen signals.
