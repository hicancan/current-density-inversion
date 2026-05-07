# Raw vs Invariant Margin Table

## Nuisance Radii

| metric | rho_raw | rho_projector | rho_gram | rho_differential |
|---|---:|---:|---:|---:|
| aggregate | 0.725007 | 0.103370 | 0.025795 | 1.281813 |

## Nuisance Reduction Factors (rho_invariant / rho_raw)

| invariant | reduction_factor |
|---|---:|
| projector | 0.1426 |
| gram | 0.0356 |
| differential | 1.7680 |

## Pairwise Margins

| pair | delta_raw | gamma_raw | delta_proj | gamma_proj | delta_gram | gamma_gram | delta_diff | gamma_diff |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| H0_no_via__H1_via | 5.912693 | 3.407664 | 1.376549 | 0.404458 | 0.368466 | 0.272577 | 6.657091 | 2.913884 |
| H0_no_via__H2_model_gap | 5.911385 | 3.406653 | 1.375390 | 0.403648 | 0.367847 | 0.271788 | 6.641341 | 2.898203 |
| H0_no_via__H3_return_path | 4.125876 | 1.677231 | 0.663612 | -0.286429 | 0.364758 | 0.260852 | 6.293627 | 2.605083 |
| H1_via__H2_model_gap | 0.071468 | -2.352246 | 0.013599 | -0.981974 | 0.010761 | -0.074340 | 0.082028 | -3.466764 |
| H1_via__H3_return_path | 4.104568 | 1.736941 | 1.325529 | 0.351658 | 0.197668 | 0.104720 | 5.137197 | 1.643000 |
| H2_model_gap__H3_return_path | 4.097023 | 1.729693 | 1.323438 | 0.349916 | 0.203893 | 0.110775 | 5.110020 | 1.615891 |

**Bold** indicates positive Gamma (robustly distinguishable).

## Invariant Beats Raw

| invariant | beats_raw |
|---|---:|
| projector_beats_raw | True |
| gram_beats_raw | True |
| differential_beats_raw | True |