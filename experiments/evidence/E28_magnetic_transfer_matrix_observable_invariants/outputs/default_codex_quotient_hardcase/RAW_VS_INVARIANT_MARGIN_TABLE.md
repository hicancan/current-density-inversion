# Raw vs Invariant Margin Table

## Nuisance Radii

| metric | rho_raw | rho_projector | rho_gram | rho_differential |
|---|---:|---:|---:|---:|
| aggregate | 0.798817 | 0.088068 | 0.037428 | 1.234101 |

## Nuisance Reduction Factors (rho_invariant / rho_raw)

| invariant | reduction_factor |
|---|---:|
| projector | 0.1102 |
| gram | 0.0469 |
| differential | 1.5449 |

## Pairwise Margins

| pair | delta_raw | gamma_raw | delta_proj | gamma_proj | delta_gram | gamma_gram | delta_diff | gamma_diff |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| H0_no_via__H1_via | 7.601689 | 3.878574 | 1.530503 | -0.174875 | 0.611498 | 0.460039 | 9.095643 | 3.981282 |
| H0_no_via__H2_model_gap | 7.605664 | 3.882924 | 1.530629 | -0.174406 | 0.609957 | 0.458399 | 9.070679 | 3.955696 |
| H0_no_via__H3_return_path | 5.688897 | 1.952630 | 0.744630 | -0.926132 | 0.700861 | 0.537166 | 6.881409 | 1.678556 |
| H1_via__H2_model_gap | 0.077699 | -3.459317 | 0.019542 | -1.720168 | 0.012866 | -0.128614 | 0.089140 | -4.691108 |
| H1_via__H3_return_path | 4.743557 | 1.193015 | 1.416594 | -0.288843 | 0.604771 | 0.451154 | 6.639836 | 1.771719 |
| H2_model_gap__H3_return_path | 4.732620 | 1.182453 | 1.415524 | -0.289570 | 0.604837 | 0.451121 | 6.605503 | 1.736765 |

**Bold** indicates positive Gamma (robustly distinguishable).

## Invariant Beats Raw

| invariant | beats_raw |
|---|---:|
| projector_beats_raw | True |
| gram_beats_raw | True |
| differential_beats_raw | True |