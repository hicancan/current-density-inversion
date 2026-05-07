# H1/H2 Robust-Separability Phase Diagram

H1/H2 phase diagram over H2 via-conductance severity and sheet drift. Rows use the same robust Gamma definition with an explicit reduced phase nuisance budget.

## Interpretation Boundary

This is a generated-domain conditional separability audit. It asks when
H1_via and H2_model_gap become distinguishable after the same Gamma
subtractions used by E28. It does not validate real-chip H1/H2 recovery.

## Summary

- row_count: 32
- h1_h2_gram_positive_count: 0
- h1_h2_gram_positive_rate: 0.0000
- h1_h2_gram_max_gamma: -0.053700
- h1_h2_gram_min_gamma: -0.107236
- h1_h2_zero_noise_gram_positive_count: 9
- h1_h2_zero_noise_gram_positive_rate: 0.2812
- default_h2_via_factor: 0.82
- default_h2_sheet_jitter: 0.03
- default_h1_h2_gamma_gram: -0.094887
- default_h1_h2_zero_noise_gamma_gram: -0.013891
- default_h1_h2_required_eps_plus_rho_gram: 0.002866
- default_h1_h2_actual_eps_plus_rho_gram: 0.097753
- default_h1_h2_budget_gap_gram: 0.094887
- default_h1_h2_gram_positive: False
- max_h2_via_factor_with_h1_h2_gram_positive: None
- min_via_contrast_with_h1_h2_gram_positive: None
- gram_quotient_survival_rate: 1.0000

## Frontier by Sheet Jitter

| h2_sheet_jitter | max_h2_via_factor_positive | min_via_contrast_positive | positive_count | row_count |
|---:|---:|---:|---:|---:|
| 0.0000 | None | None | 0 | 8 |
| 0.0100 | None | None | 0 | 8 |
| 0.0300 | None | None | 0 | 8 |
| 0.0600 | None | None | 0 | 8 |

## Rows

| h2_via_factor | h2_sheet_jitter | gamma_raw | gamma_gram | zero_noise_gamma | budget_gap | delta_gram | gram_positive | gram_q_min | gram_q_pass |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.2000 | 0.0000 | -2.758813 | -0.053700 | 0.027297 | 0.053700 | 0.053980 | False | 0.452247 | True |
| 0.2000 | 0.0100 | -2.756594 | -0.055500 | 0.025497 | 0.055500 | 0.052192 | False | 0.453005 | True |
| 0.2000 | 0.0300 | -2.745873 | -0.058229 | 0.022768 | 0.058229 | 0.049486 | False | 0.454672 | True |
| 0.2000 | 0.0600 | -2.716161 | -0.059811 | 0.021186 | 0.059811 | 0.047939 | False | 0.457551 | True |
| 0.3500 | 0.0000 | -2.898779 | -0.080681 | 0.000316 | 0.080681 | 0.027020 | False | 0.474815 | True |
| 0.3500 | 0.0100 | -2.895285 | -0.082437 | -0.001441 | 0.082437 | 0.025275 | False | 0.475649 | True |
| 0.3500 | 0.0300 | -2.876785 | -0.083753 | -0.002757 | 0.083753 | 0.023983 | False | 0.477470 | True |
| 0.3500 | 0.0600 | -2.829637 | -0.079882 | 0.001114 | 0.079882 | 0.027889 | False | 0.480591 | True |
| 0.5000 | 0.0000 | -2.961162 | -0.092679 | -0.011683 | 0.092679 | 0.015030 | False | 0.484882 | True |
| 0.5000 | 0.0100 | -2.955929 | -0.094191 | -0.013194 | 0.094191 | 0.013530 | False | 0.485754 | True |
| 0.5000 | 0.0300 | -2.928246 | -0.092812 | -0.011815 | 0.092812 | 0.014933 | False | 0.487655 | True |
| 0.5000 | 0.0600 | -2.867649 | -0.083325 | -0.002329 | 0.083325 | 0.024455 | False | 0.490899 | True |
| 0.6500 | 0.0000 | -2.996569 | -0.099472 | -0.018476 | 0.097714 | 0.008241 | False | 0.490590 | True |
| 0.6500 | 0.0100 | -2.988558 | -0.100384 | -0.019388 | 0.097726 | 0.007341 | False | 0.491485 | True |
| 0.6500 | 0.0300 | -2.951137 | -0.095283 | -0.014287 | 0.095283 | 0.012466 | False | 0.493434 | True |
| 0.6500 | 0.0600 | -2.882313 | -0.082628 | -0.001632 | 0.082628 | 0.025156 | False | 0.496754 | True |
| 0.7500 | 0.0000 | -3.012751 | -0.102572 | -0.021576 | 0.097716 | 0.005144 | False | 0.493196 | True |
| 0.7500 | 0.0100 | -3.001805 | -0.102636 | -0.021639 | 0.097728 | 0.005092 | False | 0.494102 | True |
| 0.7500 | 0.0300 | -2.958588 | -0.095250 | -0.014254 | 0.095250 | 0.012502 | False | 0.496074 | True |
| 0.7500 | 0.0600 | -2.886777 | -0.081678 | -0.000682 | 0.081678 | 0.026109 | False | 0.497526 | True |
| 0.8200 | 0.0000 | -3.021853 | -0.104314 | -0.023318 | 0.097717 | 0.003403 | False | 0.494661 | True |
| 0.8200 | 0.0100 | -3.008044 | -0.103400 | -0.022404 | 0.097729 | 0.004329 | False | 0.495574 | True |
| 0.8200 | 0.0300 | -2.961621 | -0.094887 | -0.013891 | 0.094887 | 0.012866 | False | 0.497526 | True |
| 0.8200 | 0.0600 | -2.888596 | -0.080989 | 0.000008 | 0.080989 | 0.026799 | False | 0.497526 | True |
| 0.9000 | 0.0000 | -3.030607 | -0.105988 | -0.024992 | 0.097718 | 0.001730 | False | 0.496069 | True |
| 0.9000 | 0.0100 | -3.012480 | -0.103534 | -0.022538 | 0.097730 | 0.004196 | False | 0.496988 | True |
| 0.9000 | 0.0300 | -2.963628 | -0.094325 | -0.013329 | 0.094325 | 0.013429 | False | 0.497526 | True |
| 0.9000 | 0.0600 | -2.889851 | -0.080231 | 0.000766 | 0.080231 | 0.027558 | False | 0.497526 | True |
| 0.9700 | 0.0000 | -3.037136 | -0.107236 | -0.026239 | 0.097719 | 0.000483 | False | 0.497119 | True |
| 0.9700 | 0.0100 | -3.014288 | -0.103209 | -0.022213 | 0.097731 | 0.004522 | False | 0.497526 | True |
| 0.9700 | 0.0300 | -2.964498 | -0.093785 | -0.012789 | 0.093785 | 0.013970 | False | 0.497526 | True |
| 0.9700 | 0.0600 | -2.890466 | -0.079609 | 0.001387 | 0.079609 | 0.028181 | False | 0.497526 | True |

## Cannot Claim

- default H1_via versus H2_model_gap separability unless the default row has positive Gamma
- real-chip H1/H2 separation
- external-solver or real-data validation
- that sheet-drift and via-factor axes span all real model-gap mechanisms