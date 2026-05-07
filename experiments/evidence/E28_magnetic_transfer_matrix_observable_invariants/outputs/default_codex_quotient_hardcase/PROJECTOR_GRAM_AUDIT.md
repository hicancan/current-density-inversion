# Projector and Gram Audit

## Pairwise Distances

| pair | proj_dist | gram_dist | min_angle_deg | raw_frob | raw_norm |
|---|---:|---:|---:|---:|---:|
| H0_no_via__H1_via | 1.530503 | 0.611498 | 0.69 | 7.601689 | 0.842189 |
| H0_no_via__H2_model_gap | 1.530629 | 0.609957 | 0.68 | 7.605664 | 0.843926 |
| H0_no_via__H3_return_path | 0.744630 | 0.700861 | 0.38 | 5.688897 | 0.406377 |
| H1_via__H2_model_gap | 0.019542 | 0.012866 | 0.06 | 0.077699 | 0.013614 |
| H1_via__H3_return_path | 1.416594 | 0.604771 | 1.61 | 4.743557 | 0.680938 |
| H2_model_gap__H3_return_path | 1.415524 | 0.604837 | 1.61 | 4.732620 | 0.682351 |

## Transfer Matrix Ranks

| hypothesis | shape | effective_rank |
|---|---:|---:|
| H0_no_via | [432, 6] | 6 |
| H1_via | [432, 6] | 6 |
| H2_model_gap | [432, 6] | 6 |
| H3_return_path | [432, 6] | 6 |

## Projector Properties

All projector matrices satisfy P^2 = P and P^T = P.

## Gram Properties

All whitened Gram matrices have unit diagonal.
Non-zero off-diagonals indicate correlation between port-state responses.