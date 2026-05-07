# Decision Instability Report

## 1. Ridge Reconstruction Instability

Decoder trained on operator A_i, evaluated on fields from operator A_j.

### Same-Operator Errors

- analytic_reference: 9.4292e-01
- centerline_biot_savart: 9.4291e-01
- finite_width_surrogate: 9.4292e-01
- missing_return_surrogate: 9.3846e-01
- deep_layer_shift_surrogate: 9.0659e-01
- registration_gap_surrogate: 9.4312e-01

### Cross-Operator Errors

- decoder_analytic_reference_on_centerline_biot_savart: 9.4291e-01
- decoder_analytic_reference_on_finite_width_surrogate: 9.4292e-01
- decoder_analytic_reference_on_missing_return_surrogate: 9.4059e-01
- decoder_analytic_reference_on_deep_layer_shift_surrogate: 9.2669e-01
- decoder_analytic_reference_on_registration_gap_surrogate: 9.4330e-01
- decoder_centerline_biot_savart_on_analytic_reference: 9.4292e-01
- decoder_centerline_biot_savart_on_finite_width_surrogate: 9.4292e-01
- decoder_centerline_biot_savart_on_missing_return_surrogate: 9.4059e-01
- decoder_centerline_biot_savart_on_deep_layer_shift_surrogate: 9.2669e-01
- decoder_centerline_biot_savart_on_registration_gap_surrogate: 9.4330e-01
- decoder_finite_width_surrogate_on_analytic_reference: 9.4292e-01
- decoder_finite_width_surrogate_on_centerline_biot_savart: 9.4292e-01
- decoder_finite_width_surrogate_on_missing_return_surrogate: 9.4059e-01
- decoder_finite_width_surrogate_on_deep_layer_shift_surrogate: 9.2669e-01
- decoder_finite_width_surrogate_on_registration_gap_surrogate: 9.4330e-01
- decoder_missing_return_surrogate_on_analytic_reference: 9.4088e-01
- decoder_missing_return_surrogate_on_centerline_biot_savart: 9.4088e-01
- decoder_missing_return_surrogate_on_finite_width_surrogate: 9.4088e-01
- decoder_missing_return_surrogate_on_deep_layer_shift_surrogate: 9.2386e-01
- decoder_missing_return_surrogate_on_registration_gap_surrogate: 9.4128e-01
- decoder_deep_layer_shift_surrogate_on_analytic_reference: 9.2952e-01
- decoder_deep_layer_shift_surrogate_on_centerline_biot_savart: 9.2952e-01
- decoder_deep_layer_shift_surrogate_on_finite_width_surrogate: 9.2952e-01
- decoder_deep_layer_shift_surrogate_on_missing_return_surrogate: 9.2644e-01
- decoder_deep_layer_shift_surrogate_on_registration_gap_surrogate: 9.3008e-01
- decoder_registration_gap_surrogate_on_analytic_reference: 9.4329e-01
- decoder_registration_gap_surrogate_on_centerline_biot_savart: 9.4329e-01
- decoder_registration_gap_surrogate_on_finite_width_surrogate: 9.4329e-01
- decoder_registration_gap_surrogate_on_missing_return_surrogate: 9.4099e-01
- decoder_registration_gap_surrogate_on_deep_layer_shift_surrogate: 9.2726e-01

### Ridge Instability Ratios (cross / same)

| Swap | Same Err | Cross Err | Ratio |
|---|---:|---:|---:|
| decoder_analytic_reference_on_centerline_biot_savart | 9.4292e-01 | 9.4291e-01 | 1.0x |
| decoder_analytic_reference_on_finite_width_surrogate | 9.4292e-01 | 9.4292e-01 | 1.0x |
| decoder_analytic_reference_on_missing_return_surrogate | 9.4292e-01 | 9.4059e-01 | 1.0x |
| decoder_analytic_reference_on_deep_layer_shift_surrogate | 9.4292e-01 | 9.2669e-01 | 1.0x |
| decoder_analytic_reference_on_registration_gap_surrogate | 9.4292e-01 | 9.4330e-01 | 1.0x |
| decoder_centerline_biot_savart_on_analytic_reference | 9.4291e-01 | 9.4292e-01 | 1.0x |
| decoder_centerline_biot_savart_on_finite_width_surrogate | 9.4291e-01 | 9.4292e-01 | 1.0x |
| decoder_centerline_biot_savart_on_missing_return_surrogate | 9.4291e-01 | 9.4059e-01 | 1.0x |
| decoder_centerline_biot_savart_on_deep_layer_shift_surrogate | 9.4291e-01 | 9.2669e-01 | 1.0x |
| decoder_centerline_biot_savart_on_registration_gap_surrogate | 9.4291e-01 | 9.4330e-01 | 1.0x |
| decoder_finite_width_surrogate_on_analytic_reference | 9.4292e-01 | 9.4292e-01 | 1.0x |
| decoder_finite_width_surrogate_on_centerline_biot_savart | 9.4292e-01 | 9.4292e-01 | 1.0x |
| decoder_finite_width_surrogate_on_missing_return_surrogate | 9.4292e-01 | 9.4059e-01 | 1.0x |
| decoder_finite_width_surrogate_on_deep_layer_shift_surrogate | 9.4292e-01 | 9.2669e-01 | 1.0x |
| decoder_finite_width_surrogate_on_registration_gap_surrogate | 9.4292e-01 | 9.4330e-01 | 1.0x |
| decoder_missing_return_surrogate_on_analytic_reference | 9.3846e-01 | 9.4088e-01 | 1.0x |
| decoder_missing_return_surrogate_on_centerline_biot_savart | 9.3846e-01 | 9.4088e-01 | 1.0x |
| decoder_missing_return_surrogate_on_finite_width_surrogate | 9.3846e-01 | 9.4088e-01 | 1.0x |
| decoder_missing_return_surrogate_on_deep_layer_shift_surrogate | 9.3846e-01 | 9.2386e-01 | 1.0x |
| decoder_missing_return_surrogate_on_registration_gap_surrogate | 9.3846e-01 | 9.4128e-01 | 1.0x |
| decoder_deep_layer_shift_surrogate_on_analytic_reference | 9.0659e-01 | 9.2952e-01 | 1.0x |
| decoder_deep_layer_shift_surrogate_on_centerline_biot_savart | 9.0659e-01 | 9.2952e-01 | 1.0x |
| decoder_deep_layer_shift_surrogate_on_finite_width_surrogate | 9.0659e-01 | 9.2952e-01 | 1.0x |
| decoder_deep_layer_shift_surrogate_on_missing_return_surrogate | 9.0659e-01 | 9.2644e-01 | 1.0x |
| decoder_deep_layer_shift_surrogate_on_registration_gap_surrogate | 9.0659e-01 | 9.3008e-01 | 1.0x |
| decoder_registration_gap_surrogate_on_analytic_reference | 9.4312e-01 | 9.4329e-01 | 1.0x |
| decoder_registration_gap_surrogate_on_centerline_biot_savart | 9.4312e-01 | 9.4329e-01 | 1.0x |
| decoder_registration_gap_surrogate_on_finite_width_surrogate | 9.4312e-01 | 9.4329e-01 | 1.0x |
| decoder_registration_gap_surrogate_on_missing_return_surrogate | 9.4312e-01 | 9.4099e-01 | 1.0x |
| decoder_registration_gap_surrogate_on_deep_layer_shift_surrogate | 9.4312e-01 | 9.2726e-01 | 1.0x |

### Ridge Summary

Cross/same error ratio: min=1.0x, median=1.0x, max=1.0x across 30 operator swaps

## 2. Mechanism Decision Instability (Linear Classifier)

H0/H1/H2/H3 classification under operator swaps.

### Decoder: analytic_reference

- Same-operator accuracy: 0.3750
- False via rate (H0→H1): 0.1250
- Return-path confusion (H3→H1): 0.1875

#### Cross-Operator Accuracy

- analytic_reference: 0.3750
- centerline_biot_savart: 0.3750
- finite_width_surrogate: 0.3750
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Mechanism Instability Ratios (same / cross)

- analytic_reference_vs_centerline_biot_savart: 1.00x
- analytic_reference_vs_finite_width_surrogate: 1.00x
- analytic_reference_vs_missing_return_surrogate: 1.50x
- analytic_reference_vs_deep_layer_shift_surrogate: 1.50x
- analytic_reference_vs_registration_gap_surrogate: 1.50x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 11| 2| 0| 3|
| H1 | 3| 4| 1| 8|
| H2 | 7| 3| 0| 6|
| H3 | 3| 3| 1| 9|

### Decoder: centerline_biot_savart

- Same-operator accuracy: 0.3750
- False via rate (H0→H1): 0.1250
- Return-path confusion (H3→H1): 0.1875

#### Cross-Operator Accuracy

- analytic_reference: 0.3750
- centerline_biot_savart: 0.3750
- finite_width_surrogate: 0.3750
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Mechanism Instability Ratios (same / cross)

- centerline_biot_savart_vs_analytic_reference: 1.00x
- centerline_biot_savart_vs_finite_width_surrogate: 1.00x
- centerline_biot_savart_vs_missing_return_surrogate: 1.50x
- centerline_biot_savart_vs_deep_layer_shift_surrogate: 1.50x
- centerline_biot_savart_vs_registration_gap_surrogate: 1.50x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 11| 2| 0| 3|
| H1 | 3| 4| 1| 8|
| H2 | 7| 3| 0| 6|
| H3 | 3| 3| 1| 9|

### Decoder: finite_width_surrogate

- Same-operator accuracy: 0.3750
- False via rate (H0→H1): 0.1250
- Return-path confusion (H3→H1): 0.1875

#### Cross-Operator Accuracy

- analytic_reference: 0.3750
- centerline_biot_savart: 0.3750
- finite_width_surrogate: 0.3750
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Mechanism Instability Ratios (same / cross)

- finite_width_surrogate_vs_analytic_reference: 1.00x
- finite_width_surrogate_vs_centerline_biot_savart: 1.00x
- finite_width_surrogate_vs_missing_return_surrogate: 1.50x
- finite_width_surrogate_vs_deep_layer_shift_surrogate: 1.50x
- finite_width_surrogate_vs_registration_gap_surrogate: 1.50x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 11| 2| 0| 3|
| H1 | 3| 4| 1| 8|
| H2 | 7| 3| 0| 6|
| H3 | 3| 3| 1| 9|

### Decoder: missing_return_surrogate

- Same-operator accuracy: 0.3438
- False via rate (H0→H1): 0.0625
- Return-path confusion (H3→H1): 0.0625

#### Cross-Operator Accuracy

- analytic_reference: 0.3750
- centerline_biot_savart: 0.3750
- finite_width_surrogate: 0.3750
- missing_return_surrogate: 0.3438
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Mechanism Instability Ratios (same / cross)

- missing_return_surrogate_vs_analytic_reference: 0.92x
- missing_return_surrogate_vs_centerline_biot_savart: 0.92x
- missing_return_surrogate_vs_finite_width_surrogate: 0.92x
- missing_return_surrogate_vs_deep_layer_shift_surrogate: 1.38x
- missing_return_surrogate_vs_registration_gap_surrogate: 1.38x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 12| 1| 0| 3|
| H1 | 6| 1| 0| 9|
| H2 | 11| 0| 0| 5|
| H3 | 6| 1| 0| 9|

### Decoder: deep_layer_shift_surrogate

- Same-operator accuracy: 0.3750
- False via rate (H0→H1): 0.0625
- Return-path confusion (H3→H1): 0.1250

#### Cross-Operator Accuracy

- analytic_reference: 0.3750
- centerline_biot_savart: 0.3750
- finite_width_surrogate: 0.3750
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.3750
- registration_gap_surrogate: 0.2500

#### Mechanism Instability Ratios (same / cross)

- deep_layer_shift_surrogate_vs_analytic_reference: 1.00x
- deep_layer_shift_surrogate_vs_centerline_biot_savart: 1.00x
- deep_layer_shift_surrogate_vs_finite_width_surrogate: 1.00x
- deep_layer_shift_surrogate_vs_missing_return_surrogate: 1.50x
- deep_layer_shift_surrogate_vs_registration_gap_surrogate: 1.50x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 13| 1| 0| 2|
| H1 | 5| 2| 1| 8|
| H2 | 10| 2| 0| 4|
| H3 | 5| 2| 0| 9|

### Decoder: registration_gap_surrogate

- Same-operator accuracy: 0.3438
- False via rate (H0→H1): 0.0625
- Return-path confusion (H3→H1): 0.0625

#### Cross-Operator Accuracy

- analytic_reference: 0.3594
- centerline_biot_savart: 0.3594
- finite_width_surrogate: 0.3594
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.3438

#### Mechanism Instability Ratios (same / cross)

- registration_gap_surrogate_vs_analytic_reference: 0.96x
- registration_gap_surrogate_vs_centerline_biot_savart: 0.96x
- registration_gap_surrogate_vs_finite_width_surrogate: 0.96x
- registration_gap_surrogate_vs_missing_return_surrogate: 1.38x
- registration_gap_surrogate_vs_deep_layer_shift_surrogate: 1.38x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 12| 1| 0| 3|
| H1 | 6| 1| 0| 9|
| H2 | 11| 0| 0| 5|
| H3 | 6| 1| 0| 9|


## 3. Template Evidence Scorer Instability

Class-mean template scorer: score_h = min_alpha || y - alpha * T_h ||^2.

### Templates from: analytic_reference

- Same-operator accuracy: 0.2031
- False via rate (H0→H1): 0.3750
- Return-path confusion (H3→H1): 0.1250

#### Cross-Operator Accuracy

- analytic_reference: 0.2031
- centerline_biot_savart: 0.2656
- finite_width_surrogate: 0.2031
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Template Instability Ratios (same / cross)

- analytic_reference_vs_centerline_biot_savart: 0.76x
- analytic_reference_vs_finite_width_surrogate: 1.00x
- analytic_reference_vs_missing_return_surrogate: 0.81x
- analytic_reference_vs_deep_layer_shift_surrogate: 0.81x
- analytic_reference_vs_registration_gap_surrogate: 0.81x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 2| 6| 7| 1|
| H1 | 1| 5| 9| 1|
| H2 | 2| 7| 4| 3|
| H3 | 6| 2| 6| 2|

### Templates from: centerline_biot_savart

- Same-operator accuracy: 0.2031
- False via rate (H0→H1): 0.1875
- Return-path confusion (H3→H1): 0.5000

#### Cross-Operator Accuracy

- analytic_reference: 0.2188
- centerline_biot_savart: 0.2031
- finite_width_surrogate: 0.2031
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.3125
- registration_gap_surrogate: 0.2500

#### Template Instability Ratios (same / cross)

- centerline_biot_savart_vs_analytic_reference: 0.93x
- centerline_biot_savart_vs_finite_width_surrogate: 1.00x
- centerline_biot_savart_vs_missing_return_surrogate: 0.81x
- centerline_biot_savart_vs_deep_layer_shift_surrogate: 0.65x
- centerline_biot_savart_vs_registration_gap_surrogate: 0.81x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 4| 3| 8| 1|
| H1 | 5| 5| 5| 1|
| H2 | 6| 4| 4| 2|
| H3 | 2| 8| 6| 0|

### Templates from: finite_width_surrogate

- Same-operator accuracy: 0.2500
- False via rate (H0→H1): 0.1875
- Return-path confusion (H3→H1): 0.1875

#### Cross-Operator Accuracy

- analytic_reference: 0.2812
- centerline_biot_savart: 0.2500
- finite_width_surrogate: 0.2500
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Template Instability Ratios (same / cross)

- finite_width_surrogate_vs_analytic_reference: 0.89x
- finite_width_surrogate_vs_centerline_biot_savart: 1.00x
- finite_width_surrogate_vs_missing_return_surrogate: 1.00x
- finite_width_surrogate_vs_deep_layer_shift_surrogate: 1.00x
- finite_width_surrogate_vs_registration_gap_surrogate: 1.00x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 3| 7| 3|
| H1 | 1| 2| 6| 7|
| H2 | 1| 5| 3| 7|
| H3 | 5| 3| 0| 8|

### Templates from: missing_return_surrogate

- Same-operator accuracy: 0.4219
- False via rate (H0→H1): 0.1250
- Return-path confusion (H3→H1): 0.1875

#### Cross-Operator Accuracy

- analytic_reference: 0.2812
- centerline_biot_savart: 0.2031
- finite_width_surrogate: 0.2969
- missing_return_surrogate: 0.4219
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2656

#### Template Instability Ratios (same / cross)

- missing_return_surrogate_vs_analytic_reference: 1.50x
- missing_return_surrogate_vs_centerline_biot_savart: 2.08x
- missing_return_surrogate_vs_finite_width_surrogate: 1.42x
- missing_return_surrogate_vs_deep_layer_shift_surrogate: 1.69x
- missing_return_surrogate_vs_registration_gap_surrogate: 1.59x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 1| 2| 9| 4|
| H1 | 1| 6| 3| 6|
| H2 | 3| 2| 9| 2|
| H3 | 0| 3| 2| 11|

### Templates from: deep_layer_shift_surrogate

- Same-operator accuracy: 0.4062
- False via rate (H0→H1): 0.0000
- Return-path confusion (H3→H1): 0.2500

#### Cross-Operator Accuracy

- analytic_reference: 0.2188
- centerline_biot_savart: 0.2031
- finite_width_surrogate: 0.2031
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.4062
- registration_gap_surrogate: 0.2500

#### Template Instability Ratios (same / cross)

- deep_layer_shift_surrogate_vs_analytic_reference: 1.86x
- deep_layer_shift_surrogate_vs_centerline_biot_savart: 2.00x
- deep_layer_shift_surrogate_vs_finite_width_surrogate: 2.00x
- deep_layer_shift_surrogate_vs_missing_return_surrogate: 1.62x
- deep_layer_shift_surrogate_vs_registration_gap_surrogate: 1.62x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 8| 0| 3| 5|
| H1 | 7| 2| 3| 4|
| H2 | 6| 0| 7| 3|
| H3 | 2| 4| 1| 9|

### Templates from: registration_gap_surrogate

- Same-operator accuracy: 0.4375
- False via rate (H0→H1): 0.3125
- Return-path confusion (H3→H1): 0.3750

#### Cross-Operator Accuracy

- analytic_reference: 0.3750
- centerline_biot_savart: 0.2812
- finite_width_surrogate: 0.2188
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.4375

#### Template Instability Ratios (same / cross)

- registration_gap_surrogate_vs_analytic_reference: 1.17x
- registration_gap_surrogate_vs_centerline_biot_savart: 1.56x
- registration_gap_surrogate_vs_finite_width_surrogate: 2.00x
- registration_gap_surrogate_vs_missing_return_surrogate: 1.75x
- registration_gap_surrogate_vs_deep_layer_shift_surrogate: 1.75x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 6| 5| 3| 2|
| H1 | 4| 10| 1| 1|
| H2 | 3| 4| 8| 1|
| H3 | 4| 6| 2| 4|


## 4. Acceptance Gate Summary

| Gate | Result | Value |
|---|---|---|
| package_runs_to_completion | PASS | True |
| all_operators_same_shape | PASS | True |
| operator_gaps_nonzero | PASS | True |
| decision_stress_executed | PASS | True |
| external_artifact_contract_written | PASS | True |
| reports_written | PASS | True |
| no_fake_external_validation | PASS | blocked |
| generated_domain_boundary_explicit | PASS | True |
| decision_instability_ratio_gt_1_25 | PASS | 1.5 |
| template_same_operator_accuracy_ge_0_60 | FAIL | 0.2031 |
| template_cross_operator_drop_ge_0_20 | FAIL | 0 |
| ridge_same_operator_accuracy_ge_0_60 | FAIL | 0.3125 |
| ridge_cross_operator_drop_ge_0_20 | FAIL | 0.07812 |
| ridge_wrong_accept_rate_cross_le_0_10_at_refusal | FAIL | 0.75 |
| ridge_accepted_accuracy_cross_ge_0_80_at_refusal | FAIL | 0.25 |
| pyquant_external_solver_pipeline_completed | FAIL | False |
| multibasis_same_operator_accuracy_ge_0_60 | FAIL | 0.4062 |
| multibasis_cross_operator_drop_ge_0_20 | FAIL | 0.1562 |
| operator_shift_less_than_half_margin | FAIL | False |
| margin_refusal_wrong_accept_rate_le_0_10 | FAIL | 0.6094 |
| margin_refusal_accepted_accuracy_ge_0_80 | FAIL | 0.3906 |
| external_solver_used_in_metrics | FAIL | False |

