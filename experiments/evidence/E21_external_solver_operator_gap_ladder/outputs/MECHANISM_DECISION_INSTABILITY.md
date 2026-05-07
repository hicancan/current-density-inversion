# Mechanism-Level Decision Instability Report

H0/H1/H2/H3 hypothesis classification under operator swaps.

## Decoder trained on: analytic_reference

- Same-operator accuracy: 0.3750
- False via rate (H0→H1): 0.1250
- Return-path confusion (H3→H1): 0.1875

### Cross-Operator Accuracy

- On analytic_reference: 0.3750
- On centerline_biot_savart: 0.3750
- On finite_width_surrogate: 0.3750
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Cross/Same Accuracy Ratios

- analytic_reference_vs_centerline_biot_savart: 1.00x
- analytic_reference_vs_finite_width_surrogate: 1.00x
- analytic_reference_vs_missing_return_surrogate: 1.50x
- analytic_reference_vs_deep_layer_shift_surrogate: 1.50x
- analytic_reference_vs_registration_gap_surrogate: 1.50x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 11| 2| 0| 3|
| H1 | 3| 4| 1| 8|
| H2 | 7| 3| 0| 6|
| H3 | 3| 3| 1| 9|

## Decoder trained on: centerline_biot_savart

- Same-operator accuracy: 0.3750
- False via rate (H0→H1): 0.1250
- Return-path confusion (H3→H1): 0.1875

### Cross-Operator Accuracy

- On analytic_reference: 0.3750
- On centerline_biot_savart: 0.3750
- On finite_width_surrogate: 0.3750
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Cross/Same Accuracy Ratios

- centerline_biot_savart_vs_analytic_reference: 1.00x
- centerline_biot_savart_vs_finite_width_surrogate: 1.00x
- centerline_biot_savart_vs_missing_return_surrogate: 1.50x
- centerline_biot_savart_vs_deep_layer_shift_surrogate: 1.50x
- centerline_biot_savart_vs_registration_gap_surrogate: 1.50x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 11| 2| 0| 3|
| H1 | 3| 4| 1| 8|
| H2 | 7| 3| 0| 6|
| H3 | 3| 3| 1| 9|

## Decoder trained on: finite_width_surrogate

- Same-operator accuracy: 0.3750
- False via rate (H0→H1): 0.1250
- Return-path confusion (H3→H1): 0.1875

### Cross-Operator Accuracy

- On analytic_reference: 0.3750
- On centerline_biot_savart: 0.3750
- On finite_width_surrogate: 0.3750
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Cross/Same Accuracy Ratios

- finite_width_surrogate_vs_analytic_reference: 1.00x
- finite_width_surrogate_vs_centerline_biot_savart: 1.00x
- finite_width_surrogate_vs_missing_return_surrogate: 1.50x
- finite_width_surrogate_vs_deep_layer_shift_surrogate: 1.50x
- finite_width_surrogate_vs_registration_gap_surrogate: 1.50x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 11| 2| 0| 3|
| H1 | 3| 4| 1| 8|
| H2 | 7| 3| 0| 6|
| H3 | 3| 3| 1| 9|

## Decoder trained on: missing_return_surrogate

- Same-operator accuracy: 0.3438
- False via rate (H0→H1): 0.0625
- Return-path confusion (H3→H1): 0.0625

### Cross-Operator Accuracy

- On analytic_reference: 0.3750
- On centerline_biot_savart: 0.3750
- On finite_width_surrogate: 0.3750
- On missing_return_surrogate: 0.3438
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Cross/Same Accuracy Ratios

- missing_return_surrogate_vs_analytic_reference: 0.92x
- missing_return_surrogate_vs_centerline_biot_savart: 0.92x
- missing_return_surrogate_vs_finite_width_surrogate: 0.92x
- missing_return_surrogate_vs_deep_layer_shift_surrogate: 1.38x
- missing_return_surrogate_vs_registration_gap_surrogate: 1.38x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 12| 1| 0| 3|
| H1 | 6| 1| 0| 9|
| H2 | 11| 0| 0| 5|
| H3 | 6| 1| 0| 9|

## Decoder trained on: deep_layer_shift_surrogate

- Same-operator accuracy: 0.3750
- False via rate (H0→H1): 0.0625
- Return-path confusion (H3→H1): 0.1250

### Cross-Operator Accuracy

- On analytic_reference: 0.3750
- On centerline_biot_savart: 0.3750
- On finite_width_surrogate: 0.3750
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.3750
- On registration_gap_surrogate: 0.2500

### Cross/Same Accuracy Ratios

- deep_layer_shift_surrogate_vs_analytic_reference: 1.00x
- deep_layer_shift_surrogate_vs_centerline_biot_savart: 1.00x
- deep_layer_shift_surrogate_vs_finite_width_surrogate: 1.00x
- deep_layer_shift_surrogate_vs_missing_return_surrogate: 1.50x
- deep_layer_shift_surrogate_vs_registration_gap_surrogate: 1.50x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 13| 1| 0| 2|
| H1 | 5| 2| 1| 8|
| H2 | 10| 2| 0| 4|
| H3 | 5| 2| 0| 9|

## Decoder trained on: registration_gap_surrogate

- Same-operator accuracy: 0.3438
- False via rate (H0→H1): 0.0625
- Return-path confusion (H3→H1): 0.0625

### Cross-Operator Accuracy

- On analytic_reference: 0.3594
- On centerline_biot_savart: 0.3594
- On finite_width_surrogate: 0.3594
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.3438

### Cross/Same Accuracy Ratios

- registration_gap_surrogate_vs_analytic_reference: 0.96x
- registration_gap_surrogate_vs_centerline_biot_savart: 0.96x
- registration_gap_surrogate_vs_finite_width_surrogate: 0.96x
- registration_gap_surrogate_vs_missing_return_surrogate: 1.38x
- registration_gap_surrogate_vs_deep_layer_shift_surrogate: 1.38x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 12| 1| 0| 3|
| H1 | 6| 1| 0| 9|
| H2 | 11| 0| 0| 5|
| H3 | 6| 1| 0| 9|

