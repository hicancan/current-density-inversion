# Observable Quotient Certificate

## Claim Boundary

This certificate is for the observable quotient:

- Q0_no_via = {H0_no_via}
- Q12_via_or_model_gap = {H1_via, H2_model_gap}
- Q3_return_path = {H3_return_path}

It is not a certificate for full four-hypothesis separability because
H1_via and H2_model_gap remain inside the robust margin radius.

## Selected Invariant

- selected_invariant: **gram**
- quotient_min_gamma: 0.451121
- quotient_positive_rate: 1.0000
- quotient_all_positive: True
- h1_h2_gamma: -0.128614
- h1_h2_unresolved: True

## Representation Summary

| representation | quotient_min_gamma | quotient_positive_rate | quotient_all_positive | H1/H2_gamma | H1/H2_unresolved |
|---|---:|---:|---:|---:|---:|
| raw | 1.182453 | 1.0000 | True | -3.459317 | True |
| projector | -0.926132 | 0.0000 | False | -1.720168 | True |
| gram | 0.451121 | 1.0000 | True | -0.128614 | True |
| differential | 1.678556 | 1.0000 | True | -4.691108 | True |

## Quotient Pair Margins

| pair | raw_gamma | projector_gamma | gram_gamma | differential_gamma |
|---|---:|---:|---:|---:|
| H0_no_via__H1_via | 3.878574 | -0.174875 | 0.460039 | 3.981282 |
| H0_no_via__H2_model_gap | 3.882924 | -0.174406 | 0.458399 | 3.955696 |
| H0_no_via__H3_return_path | 1.952630 | -0.926132 | 0.537166 | 1.678556 |
| H1_via__H3_return_path | 1.193015 | -0.288843 | 0.451154 | 1.771719 |
| H2_model_gap__H3_return_path | 1.182453 | -0.289570 | 0.451121 | 1.736765 |