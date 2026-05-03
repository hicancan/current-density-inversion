# Exp08 P2 accepted-hidden risk endpoint

| signal | risk status | clean false reject | hidden reject | hidden accept rate | accepted clean | accepted hidden | accepted clean acc | accepted hidden acc | accepted hidden risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| prediction_disagreement | fails_clean_budget | 1.0000 | 1.0000 | 0.0000 | 0 | 0 | nan | nan | nan |
| combined_physical_unknown_score | rejects_many_but_accepted_hidden_risky | 0.2000 | 0.6979 | 0.3021 | 80 | 29 | 0.9000 | 0.6552 | 0.3448 |
| combined_unknown_score | rejects_many_but_accepted_hidden_risky | 0.2000 | 0.6771 | 0.3229 | 80 | 31 | 0.9375 | 0.7742 | 0.2258 |
| margin_over_residual | rejects_many_but_accepted_hidden_risky | 0.2000 | 0.6771 | 0.3229 | 80 | 31 | 0.9125 | 0.5806 | 0.4194 |
| margin_only | diagnostic_only | 0.2000 | 0.6354 | 0.3646 | 80 | 35 | 0.9000 | 0.6000 | 0.4000 |
| evidence_entropy | diagnostic_only | 0.2000 | 0.6354 | 0.3646 | 80 | 35 | 0.9375 | 0.5714 | 0.4286 |
| residual_score_disagreement | fails_clean_budget | 0.2100 | 0.5938 | 0.4062 | 79 | 39 | 0.8861 | 0.5641 | 0.4359 |
| residual_gap_ambiguity | diagnostic_only | 0.2000 | 0.5208 | 0.4792 | 80 | 46 | 0.8750 | 0.5000 | 0.5000 |
| registration_instability | fails_clean_budget | 0.4700 | 0.3333 | 0.6667 | 53 | 64 | 0.8868 | 0.4375 | 0.5625 |
| residual_only | diagnostic_only | 0.2000 | 0.2812 | 0.7188 | 80 | 69 | 0.9250 | 0.4493 | 0.5507 |
| h0_h1_score_ambiguity | diagnostic_only | 0.2000 | 0.1458 | 0.8542 | 80 | 82 | 0.8625 | 0.4634 | 0.5366 |

The primary safety question is not only how many hidden mechanisms are rejected, but how risky the hidden mechanisms are after they are accepted. Thresholds are still selected from clean rows only.
