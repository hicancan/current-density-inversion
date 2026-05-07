# Raw vs Invariant Margin Table

## Nuisance Radii

| metric | rho_raw | rho_projector | rho_gram | rho_differential |
|---|---:|---:|---:|---:|
| aggregate | 1.072278 | 0.118377 | 0.050187 | 1.655915 |

## Nuisance Reduction Factors (rho_invariant / rho_raw)

| invariant | reduction_factor |
|---|---:|
| projector | 0.1104 |
| gram | 0.0468 |
| differential | 1.5443 |

## Pairwise Margins

| pair | delta_raw | gamma_raw | delta_proj | gamma_proj | delta_gram | gamma_gram | delta_diff | gamma_diff |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| H0_no_via__H1_via | 7.601689 | 3.394635 | 1.530503 | -0.218725 | 0.611498 | 0.439497 | 9.095643 | 3.250665 |
| H0_no_via__H2_model_gap | 7.605664 | 3.399115 | 1.530629 | -0.218126 | 0.609957 | 0.437823 | 9.070679 | 3.224879 |
| H0_no_via__H3_return_path | 5.688897 | 1.465131 | 0.744630 | -0.944651 | 0.700861 | 0.512414 | 6.881409 | 0.919668 |
| H1_via__H2_model_gap | 0.077699 | -3.880144 | 0.019542 | -1.780656 | 0.012866 | -0.145747 | 0.089140 | -5.308913 |
| H1_via__H3_return_path | 4.743557 | 0.768497 | 1.416594 | -0.324130 | 0.604771 | 0.429846 | 6.639836 | 1.125843 |
| H2_model_gap__H3_return_path | 4.732620 | 0.758066 | 1.415524 | -0.324726 | 0.604837 | 0.429779 | 6.605503 | 1.090688 |

**Bold** indicates positive Gamma (robustly distinguishable).

## Invariant Beats Raw

| invariant | beats_raw |
|---|---:|
| projector_beats_raw | True |
| gram_beats_raw | True |
| differential_beats_raw | True |