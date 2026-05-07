# Directional Statistical Certificate

Directional matched-filter certificate: subtract noise and nuisance only along each hypothesis-separation direction, rather than using a full feature-space noise ball.

## Interpretation Boundary

This certificate uses the hypothesis-separation direction as a matched
filter. It subtracts directional noise and directional nuisance, not a
full feature-space noise ball. It is a generated-domain statistical
audit, not real-chip risk validation.

## Summary

- z_threshold: 3.0
- directional_tau: 0.01
- baseline_selected_quotient_min_gamma: 0.451121
- directional_gram_quotient_min_gamma: 0.532388
- directional_gram_quotient_improvement: 0.081268
- directional_gram_quotient_all_positive: True
- directional_gram_h1_h2_gamma: -0.056070
- directional_gram_h1_h2_positive: False
- directional_raw_h1_h2_gamma: -0.232757
- directional_raw_h1_h2_positive: False

## Feature Summary

| feature | positive_rate | quotient_min_gamma | quotient_all_positive | H1/H2_gamma | H1/H2_positive |
|---|---:|---:|---:|---:|---:|
| raw | 0.8333 | 4.400391 | True | -0.232757 | False |
| gram | 0.8333 | 0.532388 | True | -0.056070 | False |

## raw Rows

| pair | delta | z_noise | rho_hi | rho_hj | tau | gamma | positive |
|---|---:|---:|---:|---:|---:|---:|---:|
| H0_no_via__H1_via | 7.601689 | 0.054000 | 0.525146 | 0.158018 | 0.010000 | 6.854526 | True |
| H0_no_via__H2_model_gap | 7.605664 | 0.054000 | 0.525988 | 0.159180 | 0.010000 | 6.856495 | True |
| H0_no_via__H3_return_path | 5.688897 | 0.054000 | 0.591879 | 0.367562 | 0.010000 | 4.665456 | True |
| H1_via__H2_model_gap | 0.077699 | 0.054000 | 0.124814 | 0.121642 | 0.010000 | -0.232757 | False |
| H1_via__H3_return_path | 4.743557 | 0.054000 | 0.172909 | 0.096084 | 0.010000 | 4.410565 | True |
| H2_model_gap__H3_return_path | 4.732620 | 0.054000 | 0.170678 | 0.097552 | 0.010000 | 4.400391 | True |

## gram Rows

| pair | delta | z_noise | rho_hi | rho_hj | tau | gamma | positive |
|---|---:|---:|---:|---:|---:|---:|---:|
| H0_no_via__H1_via | 0.611498 | 0.041990 | 0.016748 | 0.007203 | 0.010000 | 0.535558 | True |
| H0_no_via__H2_model_gap | 0.609957 | 0.043168 | 0.016902 | 0.007499 | 0.010000 | 0.532388 | True |
| H0_no_via__H3_return_path | 0.700861 | 0.037789 | 0.022634 | 0.020119 | 0.010000 | 0.610318 | True |
| H1_via__H2_model_gap | 0.012866 | 0.045196 | 0.006885 | 0.006856 | 0.010000 | -0.056070 | False |
| H1_via__H3_return_path | 0.604771 | 0.023486 | 0.006838 | 0.011748 | 0.010000 | 0.552699 | True |
| H2_model_gap__H3_return_path | 0.604837 | 0.024519 | 0.006653 | 0.011586 | 0.010000 | 0.552078 | True |

## Cannot Claim

- full H1_via versus H2_model_gap separation unless hard-pair gamma is positive
- real-chip detection risk control
- replacement for external-solver or real-data validation
- that directional Gaussian assumptions cover all structured noise