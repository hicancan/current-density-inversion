# Regularization Breakthrough Gate Audit

All regularized gates passed: **False**

## Gate Requirements

| gate | requirement | current | passed |
|---|---:|---:|
| regularized VDR >= 0.50 | >= 0.50 | 0.3333 | no |
| regularized ticr >= 0.90 | >= 0.90 | 0.5000 | no |
| regularized SWR == 0 | == 0.00 | 0.0000 | yes |
| regularized ER <= 0.10 | <= 0.10 | 0.5000 | no |
| regularization beats OLS by 0.20 | >= 0.20 | — | yes |

## Calibration Evaluation Gate

calibration_eval_vdr_nondegenerate (VDR > 0 on eval split): **False**

## Best Regularized Coverage

- candidate: add_h6.4_Bz
- fit_mode: ridge
- lambda: 1e+00
- VDR: 0.3333
- OLS VDR: 0.0000
- ridge VDR: 0.3333
- reduced_ridge VDR: 0.3333
- regularization beats OLS: True
- singleton_wrong_rate: 0.0000
- empty_rate: 0.5000

## Interpretation

Regularized fitting does not yet pass all breakthrough gates.
