# Decision Instability Report

## 1. Ridge Reconstruction Instability

Decoder trained on operator A_i, evaluated on fields from operator A_j.

### Same-Operator Errors

- analytic_reference: 9.9590e-01
- centerline_biot_savart: 9.9590e-01
- finite_width_surrogate: 9.9590e-01
- missing_return_surrogate: 9.9551e-01
- deep_layer_shift_surrogate: 9.9251e-01
- registration_gap_surrogate: 9.9593e-01

### Cross-Operator Errors

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

### Ridge Instability Ratios (cross / same)

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

### Ridge Summary

Cross/same error ratio: min=1.0x, median=1.0x, max=1.0x across 30 operator swaps

## 2. Mechanism Decision Instability (Linear Classifier)

H0/H1/H2/H3 classification under operator swaps.

### Decoder: analytic_reference

- Same-operator accuracy: 0.4000
- False via rate (H0→H1): 0.4000
- Return-path confusion (H3→H1): 0.4000

#### Cross-Operator Accuracy

- analytic_reference: 0.4000
- centerline_biot_savart: 0.4000
- finite_width_surrogate: 0.4000
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Mechanism Instability Ratios (same / cross)

- analytic_reference_vs_centerline_biot_savart: 1.00x
- analytic_reference_vs_finite_width_surrogate: 1.00x
- analytic_reference_vs_missing_return_surrogate: 1.60x
- analytic_reference_vs_deep_layer_shift_surrogate: 1.60x
- analytic_reference_vs_registration_gap_surrogate: 1.60x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 4| 3| 0|
| H1 | 1| 8| 1| 0|
| H2 | 2| 3| 5| 0|
| H3 | 1| 4| 5| 0|

### Decoder: centerline_biot_savart

- Same-operator accuracy: 0.4000
- False via rate (H0→H1): 0.4000
- Return-path confusion (H3→H1): 0.4000

#### Cross-Operator Accuracy

- analytic_reference: 0.4000
- centerline_biot_savart: 0.4000
- finite_width_surrogate: 0.4000
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Mechanism Instability Ratios (same / cross)

- centerline_biot_savart_vs_analytic_reference: 1.00x
- centerline_biot_savart_vs_finite_width_surrogate: 1.00x
- centerline_biot_savart_vs_missing_return_surrogate: 1.60x
- centerline_biot_savart_vs_deep_layer_shift_surrogate: 1.60x
- centerline_biot_savart_vs_registration_gap_surrogate: 1.60x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 4| 3| 0|
| H1 | 1| 8| 1| 0|
| H2 | 2| 3| 5| 0|
| H3 | 1| 4| 5| 0|

### Decoder: finite_width_surrogate

- Same-operator accuracy: 0.4000
- False via rate (H0→H1): 0.4000
- Return-path confusion (H3→H1): 0.4000

#### Cross-Operator Accuracy

- analytic_reference: 0.4000
- centerline_biot_savart: 0.4000
- finite_width_surrogate: 0.4000
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Mechanism Instability Ratios (same / cross)

- finite_width_surrogate_vs_analytic_reference: 1.00x
- finite_width_surrogate_vs_centerline_biot_savart: 1.00x
- finite_width_surrogate_vs_missing_return_surrogate: 1.60x
- finite_width_surrogate_vs_deep_layer_shift_surrogate: 1.60x
- finite_width_surrogate_vs_registration_gap_surrogate: 1.60x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 4| 3| 0|
| H1 | 1| 8| 1| 0|
| H2 | 2| 3| 5| 0|
| H3 | 1| 4| 5| 0|

### Decoder: missing_return_surrogate

- Same-operator accuracy: 0.3000
- False via rate (H0→H1): 0.8000
- Return-path confusion (H3→H1): 0.7000

#### Cross-Operator Accuracy

- analytic_reference: 0.4250
- centerline_biot_savart: 0.4250
- finite_width_surrogate: 0.4250
- missing_return_surrogate: 0.3000
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Mechanism Instability Ratios (same / cross)

- missing_return_surrogate_vs_analytic_reference: 0.71x
- missing_return_surrogate_vs_centerline_biot_savart: 0.71x
- missing_return_surrogate_vs_finite_width_surrogate: 0.71x
- missing_return_surrogate_vs_deep_layer_shift_surrogate: 1.20x
- missing_return_surrogate_vs_registration_gap_surrogate: 1.20x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 8| 2| 0|
| H1 | 0| 8| 2| 0|
| H2 | 0| 6| 4| 0|
| H3 | 0| 7| 3| 0|

### Decoder: deep_layer_shift_surrogate

- Same-operator accuracy: 0.4250
- False via rate (H0→H1): 0.4000
- Return-path confusion (H3→H1): 0.4000

#### Cross-Operator Accuracy

- analytic_reference: 0.4250
- centerline_biot_savart: 0.4250
- finite_width_surrogate: 0.4250
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.4250
- registration_gap_surrogate: 0.2750

#### Mechanism Instability Ratios (same / cross)

- deep_layer_shift_surrogate_vs_analytic_reference: 1.00x
- deep_layer_shift_surrogate_vs_centerline_biot_savart: 1.00x
- deep_layer_shift_surrogate_vs_finite_width_surrogate: 1.00x
- deep_layer_shift_surrogate_vs_missing_return_surrogate: 1.70x
- deep_layer_shift_surrogate_vs_registration_gap_surrogate: 1.55x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 4| 3| 0|
| H1 | 0| 7| 3| 0|
| H2 | 1| 2| 7| 0|
| H3 | 0| 4| 6| 0|

### Decoder: registration_gap_surrogate

- Same-operator accuracy: 0.2750
- False via rate (H0→H1): 0.8000
- Return-path confusion (H3→H1): 0.9000

#### Cross-Operator Accuracy

- analytic_reference: 0.4250
- centerline_biot_savart: 0.4250
- finite_width_surrogate: 0.4250
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2750

#### Mechanism Instability Ratios (same / cross)

- registration_gap_surrogate_vs_analytic_reference: 0.65x
- registration_gap_surrogate_vs_centerline_biot_savart: 0.65x
- registration_gap_surrogate_vs_finite_width_surrogate: 0.65x
- registration_gap_surrogate_vs_missing_return_surrogate: 1.10x
- registration_gap_surrogate_vs_deep_layer_shift_surrogate: 1.10x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 8| 2| 0|
| H1 | 0| 8| 2| 0|
| H2 | 0| 7| 3| 0|
| H3 | 0| 9| 1| 0|


## 3. Template Evidence Scorer Instability

Class-mean template scorer: score_h = min_alpha || y - alpha * T_h ||^2.

### Templates from: analytic_reference

- Same-operator accuracy: 0.3250
- False via rate (H0→H1): 0.3000
- Return-path confusion (H3→H1): 0.4000

#### Cross-Operator Accuracy

- analytic_reference: 0.3250
- centerline_biot_savart: 0.2750
- finite_width_surrogate: 0.4000
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Template Instability Ratios (same / cross)

- analytic_reference_vs_centerline_biot_savart: 1.18x
- analytic_reference_vs_finite_width_surrogate: 0.81x
- analytic_reference_vs_missing_return_surrogate: 1.30x
- analytic_reference_vs_deep_layer_shift_surrogate: 1.30x
- analytic_reference_vs_registration_gap_surrogate: 1.30x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 3| 1| 3|
| H1 | 1| 3| 5| 1|
| H2 | 2| 3| 3| 2|
| H3 | 1| 4| 1| 4|

### Templates from: centerline_biot_savart

- Same-operator accuracy: 0.3000
- False via rate (H0→H1): 0.1000
- Return-path confusion (H3→H1): 0.0000

#### Cross-Operator Accuracy

- analytic_reference: 0.2000
- centerline_biot_savart: 0.3000
- finite_width_surrogate: 0.3250
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Template Instability Ratios (same / cross)

- centerline_biot_savart_vs_analytic_reference: 1.50x
- centerline_biot_savart_vs_finite_width_surrogate: 0.92x
- centerline_biot_savart_vs_missing_return_surrogate: 1.20x
- centerline_biot_savart_vs_deep_layer_shift_surrogate: 1.20x
- centerline_biot_savart_vs_registration_gap_surrogate: 1.20x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 2| 1| 4| 3|
| H1 | 4| 3| 3| 0|
| H2 | 2| 0| 3| 5|
| H3 | 3| 0| 3| 4|

### Templates from: finite_width_surrogate

- Same-operator accuracy: 0.3000
- False via rate (H0→H1): 0.1000
- Return-path confusion (H3→H1): 0.5000

#### Cross-Operator Accuracy

- analytic_reference: 0.3750
- centerline_biot_savart: 0.2250
- finite_width_surrogate: 0.3000
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Template Instability Ratios (same / cross)

- finite_width_surrogate_vs_analytic_reference: 0.80x
- finite_width_surrogate_vs_centerline_biot_savart: 1.33x
- finite_width_surrogate_vs_missing_return_surrogate: 1.20x
- finite_width_surrogate_vs_deep_layer_shift_surrogate: 1.20x
- finite_width_surrogate_vs_registration_gap_surrogate: 1.20x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 1| 3| 3|
| H1 | 3| 3| 3| 1|
| H2 | 3| 4| 3| 0|
| H3 | 2| 5| 0| 3|

### Templates from: missing_return_surrogate

- Same-operator accuracy: 0.5250
- False via rate (H0→H1): 0.2000
- Return-path confusion (H3→H1): 0.2000

#### Cross-Operator Accuracy

- analytic_reference: 0.1750
- centerline_biot_savart: 0.2000
- finite_width_surrogate: 0.2500
- missing_return_surrogate: 0.5250
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.2500

#### Template Instability Ratios (same / cross)

- missing_return_surrogate_vs_analytic_reference: 3.00x
- missing_return_surrogate_vs_centerline_biot_savart: 2.62x
- missing_return_surrogate_vs_finite_width_surrogate: 2.10x
- missing_return_surrogate_vs_deep_layer_shift_surrogate: 2.10x
- missing_return_surrogate_vs_registration_gap_surrogate: 2.10x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 7| 2| 1| 0|
| H1 | 2| 6| 1| 1|
| H2 | 2| 2| 3| 3|
| H3 | 2| 2| 1| 5|

### Templates from: deep_layer_shift_surrogate

- Same-operator accuracy: 0.4750
- False via rate (H0→H1): 0.3000
- Return-path confusion (H3→H1): 0.4000

#### Cross-Operator Accuracy

- analytic_reference: 0.2000
- centerline_biot_savart: 0.1750
- finite_width_surrogate: 0.2250
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.4750
- registration_gap_surrogate: 0.2750

#### Template Instability Ratios (same / cross)

- deep_layer_shift_surrogate_vs_analytic_reference: 2.37x
- deep_layer_shift_surrogate_vs_centerline_biot_savart: 2.71x
- deep_layer_shift_surrogate_vs_finite_width_surrogate: 2.11x
- deep_layer_shift_surrogate_vs_missing_return_surrogate: 1.90x
- deep_layer_shift_surrogate_vs_registration_gap_surrogate: 1.73x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 5| 3| 2| 0|
| H1 | 2| 7| 0| 1|
| H2 | 1| 3| 2| 4|
| H3 | 0| 4| 1| 5|

### Templates from: registration_gap_surrogate

- Same-operator accuracy: 0.3000
- False via rate (H0→H1): 0.4000
- Return-path confusion (H3→H1): 0.0000

#### Cross-Operator Accuracy

- analytic_reference: 0.2250
- centerline_biot_savart: 0.2000
- finite_width_surrogate: 0.2500
- missing_return_surrogate: 0.2500
- deep_layer_shift_surrogate: 0.2500
- registration_gap_surrogate: 0.3000

#### Template Instability Ratios (same / cross)

- registration_gap_surrogate_vs_analytic_reference: 1.33x
- registration_gap_surrogate_vs_centerline_biot_savart: 1.50x
- registration_gap_surrogate_vs_finite_width_surrogate: 1.20x
- registration_gap_surrogate_vs_missing_return_surrogate: 1.20x
- registration_gap_surrogate_vs_deep_layer_shift_surrogate: 1.20x

#### Confusion Matrix

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 2| 4| 4| 0|
| H1 | 2| 2| 4| 2|
| H2 | 2| 3| 3| 2|
| H3 | 1| 0| 4| 5|


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
| decision_instability_ratio_gt_1_25 | PASS | 1.7 |
| template_same_operator_accuracy_ge_0_60 | FAIL | 0.325 |
| template_cross_operator_drop_ge_0_20 | FAIL | 0.075 |
| ridge_same_operator_accuracy_ge_0_60 | FAIL | 0.225 |
| ridge_cross_operator_drop_ge_0_20 | FAIL | -0.025 |
| ridge_wrong_accept_rate_cross_le_0_10_at_refusal | FAIL | 0.75 |
| ridge_accepted_accuracy_cross_ge_0_80_at_refusal | FAIL | 0.25 |
| pyquant_external_solver_pipeline_completed | FAIL | False |
| multibasis_same_operator_accuracy_ge_0_60 | PASS | 0.6 |
| multibasis_cross_operator_drop_ge_0_20 | PASS | 0.35 |
| operator_shift_less_than_half_margin | FAIL | False |
| margin_refusal_wrong_accept_rate_le_0_10 | FAIL | 0.575 |
| margin_refusal_accepted_accuracy_ge_0_80 | FAIL | 0.425 |
| external_solver_used_in_metrics | FAIL | False |

