# Decision Instability Report

Decoder trained on operator A_i, evaluated on fields from operator A_j.

## Same-Operator Errors

- analytic_reference: 9.9590e-01
- centerline_biot_savart: 9.9590e-01
- finite_width_surrogate: 9.9590e-01
- missing_return_surrogate: 9.9551e-01
- deep_layer_shift_surrogate: 9.9251e-01
- registration_gap_surrogate: 9.9593e-01

## Cross-Operator Errors

- decoder_analytic_reference_on_centerline_biot_savart: 9.9590e-01
- decoder_analytic_reference_on_finite_width_surrogate: 9.9590e-01
- decoder_analytic_reference_on_missing_return_surrogate: 9.9571e-01
- decoder_analytic_reference_on_deep_layer_shift_surrogate: 9.9453e-01
- decoder_analytic_reference_on_registration_gap_surrogate: 9.9594e-01
- decoder_centerline_biot_savart_on_analytic_reference: 9.9590e-01
- decoder_centerline_biot_savart_on_finite_width_surrogate: 9.9590e-01
- decoder_centerline_biot_savart_on_missing_return_surrogate: 9.9571e-01
- decoder_centerline_biot_savart_on_deep_layer_shift_surrogate: 9.9453e-01
- decoder_centerline_biot_savart_on_registration_gap_surrogate: 9.9594e-01
- decoder_finite_width_surrogate_on_analytic_reference: 9.9590e-01
- decoder_finite_width_surrogate_on_centerline_biot_savart: 9.9590e-01
- decoder_finite_width_surrogate_on_missing_return_surrogate: 9.9571e-01
- decoder_finite_width_surrogate_on_deep_layer_shift_surrogate: 9.9453e-01
- decoder_finite_width_surrogate_on_registration_gap_surrogate: 9.9594e-01
- decoder_missing_return_surrogate_on_analytic_reference: 9.9571e-01
- decoder_missing_return_surrogate_on_centerline_biot_savart: 9.9571e-01
- decoder_missing_return_surrogate_on_finite_width_surrogate: 9.9571e-01
- decoder_missing_return_surrogate_on_deep_layer_shift_surrogate: 9.9427e-01
- decoder_missing_return_surrogate_on_registration_gap_surrogate: 9.9575e-01
- decoder_deep_layer_shift_surrogate_on_analytic_reference: 9.9455e-01
- decoder_deep_layer_shift_surrogate_on_centerline_biot_savart: 9.9455e-01
- decoder_deep_layer_shift_surrogate_on_finite_width_surrogate: 9.9455e-01
- decoder_deep_layer_shift_surrogate_on_missing_return_surrogate: 9.9428e-01
- decoder_deep_layer_shift_surrogate_on_registration_gap_surrogate: 9.9461e-01
- decoder_registration_gap_surrogate_on_analytic_reference: 9.9594e-01
- decoder_registration_gap_surrogate_on_centerline_biot_savart: 9.9594e-01
- decoder_registration_gap_surrogate_on_finite_width_surrogate: 9.9594e-01
- decoder_registration_gap_surrogate_on_missing_return_surrogate: 9.9575e-01
- decoder_registration_gap_surrogate_on_deep_layer_shift_surrogate: 9.9459e-01

## Instability Ratios (cross / same)

| Swap | Same Err | Cross Err | Ratio |
|---|---:|---:|---:|
| decoder_analytic_reference_on_centerline_biot_savart | 9.9590e-01 | 9.9590e-01 | 1.0x |
| decoder_analytic_reference_on_finite_width_surrogate | 9.9590e-01 | 9.9590e-01 | 1.0x |
| decoder_analytic_reference_on_missing_return_surrogate | 9.9590e-01 | 9.9571e-01 | 1.0x |
| decoder_analytic_reference_on_deep_layer_shift_surrogate | 9.9590e-01 | 9.9453e-01 | 1.0x |
| decoder_analytic_reference_on_registration_gap_surrogate | 9.9590e-01 | 9.9594e-01 | 1.0x |
| decoder_centerline_biot_savart_on_analytic_reference | 9.9590e-01 | 9.9590e-01 | 1.0x |
| decoder_centerline_biot_savart_on_finite_width_surrogate | 9.9590e-01 | 9.9590e-01 | 1.0x |
| decoder_centerline_biot_savart_on_missing_return_surrogate | 9.9590e-01 | 9.9571e-01 | 1.0x |
| decoder_centerline_biot_savart_on_deep_layer_shift_surrogate | 9.9590e-01 | 9.9453e-01 | 1.0x |
| decoder_centerline_biot_savart_on_registration_gap_surrogate | 9.9590e-01 | 9.9594e-01 | 1.0x |
| decoder_finite_width_surrogate_on_analytic_reference | 9.9590e-01 | 9.9590e-01 | 1.0x |
| decoder_finite_width_surrogate_on_centerline_biot_savart | 9.9590e-01 | 9.9590e-01 | 1.0x |
| decoder_finite_width_surrogate_on_missing_return_surrogate | 9.9590e-01 | 9.9571e-01 | 1.0x |
| decoder_finite_width_surrogate_on_deep_layer_shift_surrogate | 9.9590e-01 | 9.9453e-01 | 1.0x |
| decoder_finite_width_surrogate_on_registration_gap_surrogate | 9.9590e-01 | 9.9594e-01 | 1.0x |
| decoder_missing_return_surrogate_on_analytic_reference | 9.9551e-01 | 9.9571e-01 | 1.0x |
| decoder_missing_return_surrogate_on_centerline_biot_savart | 9.9551e-01 | 9.9571e-01 | 1.0x |
| decoder_missing_return_surrogate_on_finite_width_surrogate | 9.9551e-01 | 9.9571e-01 | 1.0x |
| decoder_missing_return_surrogate_on_deep_layer_shift_surrogate | 9.9551e-01 | 9.9427e-01 | 1.0x |
| decoder_missing_return_surrogate_on_registration_gap_surrogate | 9.9551e-01 | 9.9575e-01 | 1.0x |
| decoder_deep_layer_shift_surrogate_on_analytic_reference | 9.9251e-01 | 9.9455e-01 | 1.0x |
| decoder_deep_layer_shift_surrogate_on_centerline_biot_savart | 9.9251e-01 | 9.9455e-01 | 1.0x |
| decoder_deep_layer_shift_surrogate_on_finite_width_surrogate | 9.9251e-01 | 9.9455e-01 | 1.0x |
| decoder_deep_layer_shift_surrogate_on_missing_return_surrogate | 9.9251e-01 | 9.9428e-01 | 1.0x |
| decoder_deep_layer_shift_surrogate_on_registration_gap_surrogate | 9.9251e-01 | 9.9461e-01 | 1.0x |
| decoder_registration_gap_surrogate_on_analytic_reference | 9.9593e-01 | 9.9594e-01 | 1.0x |
| decoder_registration_gap_surrogate_on_centerline_biot_savart | 9.9593e-01 | 9.9594e-01 | 1.0x |
| decoder_registration_gap_surrogate_on_finite_width_surrogate | 9.9593e-01 | 9.9594e-01 | 1.0x |
| decoder_registration_gap_surrogate_on_missing_return_surrogate | 9.9593e-01 | 9.9575e-01 | 1.0x |
| decoder_registration_gap_surrogate_on_deep_layer_shift_surrogate | 9.9593e-01 | 9.9459e-01 | 1.0x |

## Summary

Cross/same error ratio: min=1.0x, median=1.0x, max=1.0x across 30 operator swaps
