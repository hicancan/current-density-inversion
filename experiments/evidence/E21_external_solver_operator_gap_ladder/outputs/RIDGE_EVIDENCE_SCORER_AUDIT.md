# Ridge Evidence Scorer Audit

Per-hypothesis ridge evidence: score_h = min_alpha ||y - alpha*T_h||^2 + lambda*alpha^2

## Scorer trained on: analytic_reference

- Best lambda: 1.0000e-04
- Same-operator accuracy: 0.3125
- False via rate (H0->H1): 0.1250
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.3125
- On centerline_biot_savart: 0.2344
- On finite_width_surrogate: 0.2344
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Ridge Instability Ratios (same / cross)

- analytic_reference_vs_centerline_biot_savart: 1.33x
- analytic_reference_vs_finite_width_surrogate: 1.33x
- analytic_reference_vs_missing_return_surrogate: 1.25x
- analytic_reference_vs_deep_layer_shift_surrogate: 1.25x
- analytic_reference_vs_registration_gap_surrogate: 1.25x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 7| 2| 1| 6|
| H1 | 5| 1| 1| 9|
| H2 | 6| 1| 0| 9|
| H3 | 4| 0| 0| 12|

### Confusion Matrix (cross-operator: templates on centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 10| 1| 0| 5|
| H1 | 7| 1| 0| 8|
| H2 | 8| 2| 0| 6|
| H3 | 11| 1| 0| 4|

### Confusion Matrix (cross-operator: templates on finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 10| 4| 0| 2|
| H1 | 12| 2| 0| 2|
| H2 | 6| 4| 0| 6|
| H3 | 11| 1| 1| 3|

### Confusion Matrix (cross-operator: templates on missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 16| 0| 0| 0|
| H1 | 16| 0| 0| 0|
| H2 | 16| 0| 0| 0|
| H3 | 16| 0| 0| 0|

### Confusion Matrix (cross-operator: templates on deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 16| 0| 0| 0|
| H1 | 16| 0| 0| 0|
| H2 | 16| 0| 0| 0|
| H3 | 16| 0| 0| 0|

### Confusion Matrix (cross-operator: templates on registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 16| 0| 0| 0|
| H1 | 16| 0| 0| 0|
| H2 | 16| 0| 0| 0|
| H3 | 16| 0| 0| 0|
## Scorer trained on: centerline_biot_savart

- Best lambda: 1.0000e-04
- Same-operator accuracy: 0.2500
- False via rate (H0->H1): 0.0000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.2812
- On centerline_biot_savart: 0.2500
- On finite_width_surrogate: 0.2031
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Ridge Instability Ratios (same / cross)

- centerline_biot_savart_vs_analytic_reference: 0.89x
- centerline_biot_savart_vs_finite_width_surrogate: 1.23x
- centerline_biot_savart_vs_missing_return_surrogate: 1.00x
- centerline_biot_savart_vs_deep_layer_shift_surrogate: 1.00x
- centerline_biot_savart_vs_registration_gap_surrogate: 1.00x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 6|
| H1 | 0| 0| 9| 7|
| H2 | 0| 0| 8| 8|
| H3 | 1| 0| 7| 8|

### Confusion Matrix (cross-operator: templates on analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 8| 0| 3| 5|
| H1 | 6| 0| 4| 6|
| H2 | 4| 0| 8| 4|
| H3 | 6| 0| 8| 2|

### Confusion Matrix (cross-operator: templates on finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 8| 0| 2| 6|
| H1 | 12| 0| 1| 3|
| H2 | 7| 0| 4| 5|
| H3 | 10| 0| 5| 1|

### Confusion Matrix (cross-operator: templates on missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 16|
| H1 | 0| 0| 0| 16|
| H2 | 0| 0| 0| 16|
| H3 | 0| 0| 0| 16|

### Confusion Matrix (cross-operator: templates on deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 16|
| H1 | 0| 0| 0| 16|
| H2 | 0| 0| 0| 16|
| H3 | 0| 0| 0| 16|

### Confusion Matrix (cross-operator: templates on registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 16|
| H1 | 0| 0| 0| 16|
| H2 | 0| 0| 0| 16|
| H3 | 0| 0| 0| 16|
## Scorer trained on: finite_width_surrogate

- Best lambda: 1.0000e-04
- Same-operator accuracy: 0.2656
- False via rate (H0->H1): 0.0000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.2969
- On centerline_biot_savart: 0.2656
- On finite_width_surrogate: 0.2656
- On missing_return_surrogate: 0.1875
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2188

### Ridge Instability Ratios (same / cross)

- finite_width_surrogate_vs_analytic_reference: 0.89x
- finite_width_surrogate_vs_centerline_biot_savart: 1.00x
- finite_width_surrogate_vs_missing_return_surrogate: 1.42x
- finite_width_surrogate_vs_deep_layer_shift_surrogate: 1.06x
- finite_width_surrogate_vs_registration_gap_surrogate: 1.21x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 12| 0| 0| 4|
| H1 | 12| 0| 1| 3|
| H2 | 13| 0| 1| 2|
| H3 | 12| 0| 0| 4|

### Confusion Matrix (cross-operator: templates on analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 13| 1| 2| 0|
| H1 | 10| 2| 4| 0|
| H2 | 12| 0| 4| 0|
| H3 | 14| 0| 2| 0|

### Confusion Matrix (cross-operator: templates on centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 11| 0| 4| 1|
| H1 | 13| 1| 2| 0|
| H2 | 11| 0| 5| 0|
| H3 | 13| 0| 3| 0|

### Confusion Matrix (cross-operator: templates on missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 9| 0| 7| 0|
| H1 | 9| 0| 7| 0|
| H2 | 13| 0| 3| 0|
| H3 | 10| 0| 6| 0|

### Confusion Matrix (cross-operator: templates on deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 16| 0|
| H1 | 0| 0| 16| 0|
| H2 | 0| 0| 16| 0|
| H3 | 0| 0| 16| 0|

### Confusion Matrix (cross-operator: templates on registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 14| 2| 0|
| H1 | 0| 13| 3| 0|
| H2 | 0| 15| 1| 0|
| H3 | 0| 14| 2| 0|
## Scorer trained on: missing_return_surrogate

- Best lambda: 1.0000e-04
- Same-operator accuracy: 0.2969
- False via rate (H0->H1): 0.1250
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.2031
- On centerline_biot_savart: 0.2031
- On finite_width_surrogate: 0.2344
- On missing_return_surrogate: 0.2969
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2812

### Ridge Instability Ratios (same / cross)

- missing_return_surrogate_vs_analytic_reference: 1.46x
- missing_return_surrogate_vs_centerline_biot_savart: 1.46x
- missing_return_surrogate_vs_finite_width_surrogate: 1.27x
- missing_return_surrogate_vs_deep_layer_shift_surrogate: 1.19x
- missing_return_surrogate_vs_registration_gap_surrogate: 1.06x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 2| 0| 14|
| H1 | 1| 3| 0| 12|
| H2 | 0| 1| 0| 15|
| H3 | 0| 0| 0| 16|

### Confusion Matrix (cross-operator: templates on analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 7| 3| 6|
| H1 | 1| 4| 4| 7|
| H2 | 2| 7| 0| 7|
| H3 | 2| 5| 0| 9|

### Confusion Matrix (cross-operator: templates on centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 8| 2| 6|
| H1 | 3| 2| 4| 7|
| H2 | 2| 3| 1| 10|
| H3 | 2| 4| 0| 10|

### Confusion Matrix (cross-operator: templates on finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 1| 3| 2| 10|
| H1 | 3| 7| 1| 5|
| H2 | 7| 1| 0| 8|
| H3 | 4| 4| 1| 7|

### Confusion Matrix (cross-operator: templates on deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 16| 0| 0|
| H1 | 0| 16| 0| 0|
| H2 | 0| 16| 0| 0|
| H3 | 0| 16| 0| 0|

### Confusion Matrix (cross-operator: templates on registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 15| 1| 0| 0|
| H1 | 13| 3| 0| 0|
| H2 | 16| 0| 0| 0|
| H3 | 14| 2| 0| 0|
## Scorer trained on: deep_layer_shift_surrogate

- Best lambda: 1.0000e-04
- Same-operator accuracy: 0.2969
- False via rate (H0->H1): 0.7500
- Return-path confusion (H3->H1): 0.6250

### Cross-Operator Accuracy

- On analytic_reference: 0.3125
- On centerline_biot_savart: 0.2500
- On finite_width_surrogate: 0.2969
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2969
- On registration_gap_surrogate: 0.3281

### Ridge Instability Ratios (same / cross)

- deep_layer_shift_surrogate_vs_analytic_reference: 0.95x
- deep_layer_shift_surrogate_vs_centerline_biot_savart: 1.19x
- deep_layer_shift_surrogate_vs_finite_width_surrogate: 1.00x
- deep_layer_shift_surrogate_vs_missing_return_surrogate: 1.19x
- deep_layer_shift_surrogate_vs_registration_gap_surrogate: 0.90x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 12| 0| 4|
| H1 | 0| 13| 0| 3|
| H2 | 0| 14| 0| 2|
| H3 | 0| 10| 0| 6|

### Confusion Matrix (cross-operator: templates on analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 2| 8| 0| 6|
| H1 | 2| 10| 0| 4|
| H2 | 0| 7| 1| 8|
| H3 | 1| 7| 1| 7|

### Confusion Matrix (cross-operator: templates on centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 1| 9| 0| 6|
| H1 | 0| 5| 0| 11|
| H2 | 0| 4| 3| 9|
| H3 | 0| 8| 1| 7|

### Confusion Matrix (cross-operator: templates on finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 1| 6| 1| 8|
| H1 | 1| 9| 1| 5|
| H2 | 0| 2| 2| 12|
| H3 | 0| 8| 1| 7|

### Confusion Matrix (cross-operator: templates on missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 16|
| H1 | 0| 0| 0| 16|
| H2 | 0| 0| 0| 16|
| H3 | 0| 0| 0| 16|

### Confusion Matrix (cross-operator: templates on registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 12| 0| 0| 4|
| H1 | 12| 0| 0| 4|
| H2 | 11| 0| 0| 5|
| H3 | 7| 0| 0| 9|
## Scorer trained on: registration_gap_surrogate

- Best lambda: 1.0000e-04
- Same-operator accuracy: 0.3125
- False via rate (H0->H1): 0.5625
- Return-path confusion (H3->H1): 0.1875

### Cross-Operator Accuracy

- On analytic_reference: 0.2969
- On centerline_biot_savart: 0.2188
- On finite_width_surrogate: 0.2969
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.3125

### Ridge Instability Ratios (same / cross)

- registration_gap_surrogate_vs_analytic_reference: 1.05x
- registration_gap_surrogate_vs_centerline_biot_savart: 1.43x
- registration_gap_surrogate_vs_finite_width_surrogate: 1.05x
- registration_gap_surrogate_vs_missing_return_surrogate: 1.25x
- registration_gap_surrogate_vs_deep_layer_shift_surrogate: 1.25x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 9| 0| 7|
| H1 | 0| 7| 0| 9|
| H2 | 0| 6| 0| 10|
| H3 | 0| 3| 0| 13|

### Confusion Matrix (cross-operator: templates on analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 10| 0| 6|
| H1 | 0| 8| 1| 7|
| H2 | 0| 7| 0| 9|
| H3 | 0| 5| 0| 11|

### Confusion Matrix (cross-operator: templates on centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 12| 0| 4|
| H1 | 0| 5| 0| 11|
| H2 | 0| 5| 0| 11|
| H3 | 0| 7| 0| 9|

### Confusion Matrix (cross-operator: templates on finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 5| 0| 11|
| H1 | 0| 9| 0| 7|
| H2 | 0| 1| 0| 15|
| H3 | 0| 6| 0| 10|

### Confusion Matrix (cross-operator: templates on missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 16|
| H1 | 0| 0| 0| 16|
| H2 | 0| 0| 0| 16|
| H3 | 0| 0| 0| 16|

### Confusion Matrix (cross-operator: templates on deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 16| 0| 0|
| H1 | 0| 16| 0| 0|
| H2 | 0| 16| 0| 0|
| H3 | 0| 16| 0| 0|
