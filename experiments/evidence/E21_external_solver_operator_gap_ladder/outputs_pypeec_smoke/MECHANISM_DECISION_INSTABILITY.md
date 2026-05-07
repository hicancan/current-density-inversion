# Mechanism-Level Decision Instability Report

H0/H1/H2/H3 hypothesis classification under operator swaps.

## Decoder trained on: analytic_reference

- Same-operator accuracy: 0.4000
- False via rate (H0→H1): 0.4000
- Return-path confusion (H3→H1): 0.4000

### Cross-Operator Accuracy

- On analytic_reference: 0.4000
- On centerline_biot_savart: 0.4000
- On finite_width_surrogate: 0.4000
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Cross/Same Accuracy Ratios

- analytic_reference_vs_centerline_biot_savart: 1.00x
- analytic_reference_vs_finite_width_surrogate: 1.00x
- analytic_reference_vs_missing_return_surrogate: 1.60x
- analytic_reference_vs_deep_layer_shift_surrogate: 1.60x
- analytic_reference_vs_registration_gap_surrogate: 1.60x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 4| 3| 0|
| H1 | 1| 8| 1| 0|
| H2 | 2| 3| 5| 0|
| H3 | 1| 4| 5| 0|

## Decoder trained on: centerline_biot_savart

- Same-operator accuracy: 0.4000
- False via rate (H0→H1): 0.4000
- Return-path confusion (H3→H1): 0.4000

### Cross-Operator Accuracy

- On analytic_reference: 0.4000
- On centerline_biot_savart: 0.4000
- On finite_width_surrogate: 0.4000
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Cross/Same Accuracy Ratios

- centerline_biot_savart_vs_analytic_reference: 1.00x
- centerline_biot_savart_vs_finite_width_surrogate: 1.00x
- centerline_biot_savart_vs_missing_return_surrogate: 1.60x
- centerline_biot_savart_vs_deep_layer_shift_surrogate: 1.60x
- centerline_biot_savart_vs_registration_gap_surrogate: 1.60x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 4| 3| 0|
| H1 | 1| 8| 1| 0|
| H2 | 2| 3| 5| 0|
| H3 | 1| 4| 5| 0|

## Decoder trained on: finite_width_surrogate

- Same-operator accuracy: 0.4000
- False via rate (H0→H1): 0.4000
- Return-path confusion (H3→H1): 0.4000

### Cross-Operator Accuracy

- On analytic_reference: 0.4000
- On centerline_biot_savart: 0.4000
- On finite_width_surrogate: 0.4000
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Cross/Same Accuracy Ratios

- finite_width_surrogate_vs_analytic_reference: 1.00x
- finite_width_surrogate_vs_centerline_biot_savart: 1.00x
- finite_width_surrogate_vs_missing_return_surrogate: 1.60x
- finite_width_surrogate_vs_deep_layer_shift_surrogate: 1.60x
- finite_width_surrogate_vs_registration_gap_surrogate: 1.60x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 4| 3| 0|
| H1 | 1| 8| 1| 0|
| H2 | 2| 3| 5| 0|
| H3 | 1| 4| 5| 0|

## Decoder trained on: missing_return_surrogate

- Same-operator accuracy: 0.3000
- False via rate (H0→H1): 0.8000
- Return-path confusion (H3→H1): 0.7000

### Cross-Operator Accuracy

- On analytic_reference: 0.4250
- On centerline_biot_savart: 0.4250
- On finite_width_surrogate: 0.4250
- On missing_return_surrogate: 0.3000
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Cross/Same Accuracy Ratios

- missing_return_surrogate_vs_analytic_reference: 0.71x
- missing_return_surrogate_vs_centerline_biot_savart: 0.71x
- missing_return_surrogate_vs_finite_width_surrogate: 0.71x
- missing_return_surrogate_vs_deep_layer_shift_surrogate: 1.20x
- missing_return_surrogate_vs_registration_gap_surrogate: 1.20x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 8| 2| 0|
| H1 | 0| 8| 2| 0|
| H2 | 0| 6| 4| 0|
| H3 | 0| 7| 3| 0|

## Decoder trained on: deep_layer_shift_surrogate

- Same-operator accuracy: 0.4250
- False via rate (H0→H1): 0.4000
- Return-path confusion (H3→H1): 0.4000

### Cross-Operator Accuracy

- On analytic_reference: 0.4250
- On centerline_biot_savart: 0.4250
- On finite_width_surrogate: 0.4250
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.4250
- On registration_gap_surrogate: 0.2750

### Cross/Same Accuracy Ratios

- deep_layer_shift_surrogate_vs_analytic_reference: 1.00x
- deep_layer_shift_surrogate_vs_centerline_biot_savart: 1.00x
- deep_layer_shift_surrogate_vs_finite_width_surrogate: 1.00x
- deep_layer_shift_surrogate_vs_missing_return_surrogate: 1.70x
- deep_layer_shift_surrogate_vs_registration_gap_surrogate: 1.55x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 4| 3| 0|
| H1 | 0| 7| 3| 0|
| H2 | 1| 2| 7| 0|
| H3 | 0| 4| 6| 0|

## Decoder trained on: registration_gap_surrogate

- Same-operator accuracy: 0.2750
- False via rate (H0→H1): 0.8000
- Return-path confusion (H3→H1): 0.9000

### Cross-Operator Accuracy

- On analytic_reference: 0.4250
- On centerline_biot_savart: 0.4250
- On finite_width_surrogate: 0.4250
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2750

### Cross/Same Accuracy Ratios

- registration_gap_surrogate_vs_analytic_reference: 0.65x
- registration_gap_surrogate_vs_centerline_biot_savart: 0.65x
- registration_gap_surrogate_vs_finite_width_surrogate: 0.65x
- registration_gap_surrogate_vs_missing_return_surrogate: 1.10x
- registration_gap_surrogate_vs_deep_layer_shift_surrogate: 1.10x

### Confusion Matrix (same-operator)

| Truth \ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 8| 2| 0|
| H1 | 0| 8| 2| 0|
| H2 | 0| 7| 3| 0|
| H3 | 0| 9| 1| 0|

