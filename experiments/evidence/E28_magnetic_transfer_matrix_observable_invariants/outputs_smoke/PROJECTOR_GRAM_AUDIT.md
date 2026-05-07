# Projector and Gram Audit

## Pairwise Distances

| pair | proj_dist | gram_dist | min_angle_deg | raw_frob | raw_norm |
|---|---:|---:|---:|---:|---:|
| H0_no_via__H1_via | 1.376549 | 0.368466 | 0.79 | 5.912693 | 0.768846 |
| H0_no_via__H2_model_gap | 1.375390 | 0.367847 | 0.78 | 5.911385 | 0.770781 |
| H0_no_via__H3_return_path | 0.663612 | 0.364758 | 0.40 | 4.125876 | 0.312592 |
| H1_via__H2_model_gap | 0.013599 | 0.010761 | 0.07 | 0.071468 | 0.013102 |
| H1_via__H3_return_path | 1.325529 | 0.197668 | 1.82 | 4.104568 | 0.605950 |
| H2_model_gap__H3_return_path | 1.323438 | 0.203893 | 1.84 | 4.097023 | 0.608277 |

## Transfer Matrix Ranks

| hypothesis | shape | effective_rank |
|---|---:|---:|
| H0_no_via | [432, 4] | 4 |
| H1_via | [432, 4] | 4 |
| H2_model_gap | [432, 4] | 4 |
| H3_return_path | [432, 4] | 4 |

## Projector Properties

All projector matrices satisfy P^2 = P and P^T = P.

## Gram Properties

All whitened Gram matrices have unit diagonal.
Non-zero off-diagonals indicate correlation between port-state responses.