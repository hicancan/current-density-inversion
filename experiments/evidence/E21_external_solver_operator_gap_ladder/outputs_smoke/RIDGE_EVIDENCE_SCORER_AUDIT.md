# Ridge Evidence Scorer Audit

Per-hypothesis ridge evidence: score_h = min_alpha ||y - alpha*T_h||^2 + lambda*alpha^2

## Scorer trained on: analytic_reference

- Best lambda: 1.0000e-04
- Same-operator accuracy: 0.2250
- False via rate (H0->H1): 0.0000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.2250
- On centerline_biot_savart: 0.3500
- On finite_width_surrogate: 0.3000
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Ridge Instability Ratios (same / cross)

- analytic_reference_vs_centerline_biot_savart: 0.64x
- analytic_reference_vs_finite_width_surrogate: 0.75x
- analytic_reference_vs_missing_return_surrogate: 0.90x
- analytic_reference_vs_deep_layer_shift_surrogate: 0.90x
- analytic_reference_vs_registration_gap_surrogate: 0.90x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 1| 0| 0| 9|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 0| 10|
| H3 | 2| 0| 0| 8|

### Confusion Matrix (cross-operator: templates on centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 1| 9|
| H1 | 0| 1| 1| 8|
| H2 | 0| 0| 4| 6|
| H3 | 0| 0| 1| 9|

### Confusion Matrix (cross-operator: templates on finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 1| 0| 9|
| H1 | 0| 1| 0| 9|
| H2 | 0| 0| 1| 9|
| H3 | 0| 0| 0| 10|

### Confusion Matrix (cross-operator: templates on missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 10|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 0| 10|
| H3 | 0| 0| 0| 10|

### Confusion Matrix (cross-operator: templates on deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 10|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 0| 10|
| H3 | 0| 0| 0| 10|

### Confusion Matrix (cross-operator: templates on registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 10|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 0| 10|
| H3 | 0| 0| 0| 10|
## Scorer trained on: centerline_biot_savart

- Best lambda: 1.0000e-04
- Same-operator accuracy: 0.2250
- False via rate (H0->H1): 0.5000
- Return-path confusion (H3->H1): 0.3000

### Cross-Operator Accuracy

- On analytic_reference: 0.1750
- On centerline_biot_savart: 0.2250
- On finite_width_surrogate: 0.1750
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Ridge Instability Ratios (same / cross)

- centerline_biot_savart_vs_analytic_reference: 1.29x
- centerline_biot_savart_vs_finite_width_surrogate: 1.29x
- centerline_biot_savart_vs_missing_return_surrogate: 0.90x
- centerline_biot_savart_vs_deep_layer_shift_surrogate: 0.90x
- centerline_biot_savart_vs_registration_gap_surrogate: 0.90x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 5| 5| 0| 0|
| H1 | 6| 4| 0| 0|
| H2 | 4| 6| 0| 0|
| H3 | 7| 3| 0| 0|

### Confusion Matrix (cross-operator: templates on analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 4| 0| 3|
| H1 | 6| 3| 0| 1|
| H2 | 3| 3| 0| 4|
| H3 | 6| 3| 0| 1|

### Confusion Matrix (cross-operator: templates on finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 5| 0| 2|
| H1 | 6| 2| 0| 2|
| H2 | 4| 3| 0| 3|
| H3 | 7| 1| 0| 2|

### Confusion Matrix (cross-operator: templates on missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 10| 0| 0|
| H1 | 0| 10| 0| 0|
| H2 | 0| 10| 0| 0|
| H3 | 0| 10| 0| 0|

### Confusion Matrix (cross-operator: templates on deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 10| 0| 0|
| H1 | 0| 10| 0| 0|
| H2 | 0| 10| 0| 0|
| H3 | 0| 10| 0| 0|

### Confusion Matrix (cross-operator: templates on registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 10| 0| 0|
| H1 | 0| 10| 0| 0|
| H2 | 0| 10| 0| 0|
| H3 | 0| 10| 0| 0|
## Scorer trained on: finite_width_surrogate

- Best lambda: 1.0000e-04
- Same-operator accuracy: 0.3000
- False via rate (H0->H1): 0.0000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.2000
- On centerline_biot_savart: 0.3250
- On finite_width_surrogate: 0.3000
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Ridge Instability Ratios (same / cross)

- finite_width_surrogate_vs_analytic_reference: 1.50x
- finite_width_surrogate_vs_centerline_biot_savart: 0.92x
- finite_width_surrogate_vs_missing_return_surrogate: 1.20x
- finite_width_surrogate_vs_deep_layer_shift_surrogate: 1.20x
- finite_width_surrogate_vs_registration_gap_surrogate: 1.20x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 1| 0| 1| 8|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 1| 9|
| H3 | 0| 0| 0| 10|

### Confusion Matrix (cross-operator: templates on analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 10|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 0| 10|
| H3 | 0| 0| 2| 8|

### Confusion Matrix (cross-operator: templates on centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 3| 7|
| H1 | 0| 0| 2| 8|
| H2 | 0| 0| 4| 6|
| H3 | 0| 0| 1| 9|

### Confusion Matrix (cross-operator: templates on missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 10|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 0| 10|
| H3 | 0| 0| 0| 10|

### Confusion Matrix (cross-operator: templates on deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 10|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 0| 10|
| H3 | 0| 0| 0| 10|

### Confusion Matrix (cross-operator: templates on registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 10|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 0| 10|
| H3 | 0| 0| 0| 10|
## Scorer trained on: missing_return_surrogate

- Best lambda: 1.0000e-04
- Same-operator accuracy: 0.3250
- False via rate (H0->H1): 0.6000
- Return-path confusion (H3->H1): 1.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.3250
- On centerline_biot_savart: 0.3000
- On finite_width_surrogate: 0.2000
- On missing_return_surrogate: 0.3250
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Ridge Instability Ratios (same / cross)

- missing_return_surrogate_vs_analytic_reference: 1.00x
- missing_return_surrogate_vs_centerline_biot_savart: 1.08x
- missing_return_surrogate_vs_finite_width_surrogate: 1.62x
- missing_return_surrogate_vs_deep_layer_shift_surrogate: 1.30x
- missing_return_surrogate_vs_registration_gap_surrogate: 1.30x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 4| 6| 0| 0|
| H1 | 1| 9| 0| 0|
| H2 | 2| 8| 0| 0|
| H3 | 0| 10| 0| 0|

### Confusion Matrix (cross-operator: templates on analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 4| 3| 0| 3|
| H1 | 1| 7| 0| 2|
| H2 | 0| 5| 0| 5|
| H3 | 4| 4| 0| 2|

### Confusion Matrix (cross-operator: templates on centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 4| 4| 0| 2|
| H1 | 1| 7| 0| 2|
| H2 | 4| 4| 0| 2|
| H3 | 5| 4| 0| 1|

### Confusion Matrix (cross-operator: templates on finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 5| 0| 2|
| H1 | 4| 4| 0| 2|
| H2 | 1| 5| 0| 4|
| H3 | 1| 8| 0| 1|

### Confusion Matrix (cross-operator: templates on deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 10| 0| 0| 0|
| H1 | 10| 0| 0| 0|
| H2 | 10| 0| 0| 0|
| H3 | 10| 0| 0| 0|

### Confusion Matrix (cross-operator: templates on registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 10| 0| 0|
| H1 | 0| 10| 0| 0|
| H2 | 0| 10| 0| 0|
| H3 | 0| 10| 0| 0|
## Scorer trained on: deep_layer_shift_surrogate

- Best lambda: 1.0000e-04
- Same-operator accuracy: 0.2500
- False via rate (H0->H1): 1.0000
- Return-path confusion (H3->H1): 1.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.1750
- On centerline_biot_savart: 0.2000
- On finite_width_surrogate: 0.2500
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Ridge Instability Ratios (same / cross)

- deep_layer_shift_surrogate_vs_analytic_reference: 1.43x
- deep_layer_shift_surrogate_vs_centerline_biot_savart: 1.25x
- deep_layer_shift_surrogate_vs_finite_width_surrogate: 1.00x
- deep_layer_shift_surrogate_vs_missing_return_surrogate: 1.00x
- deep_layer_shift_surrogate_vs_registration_gap_surrogate: 1.00x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 10| 0| 0|
| H1 | 0| 10| 0| 0|
| H2 | 0| 10| 0| 0|
| H3 | 0| 10| 0| 0|

### Confusion Matrix (cross-operator: templates on analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 0| 2| 5|
| H1 | 2| 0| 1| 7|
| H2 | 3| 0| 2| 5|
| H3 | 4| 0| 4| 2|

### Confusion Matrix (cross-operator: templates on centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 0| 4| 3|
| H1 | 1| 0| 5| 4|
| H2 | 4| 0| 2| 4|
| H3 | 5| 0| 2| 3|

### Confusion Matrix (cross-operator: templates on finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 2| 2| 1| 5|
| H1 | 2| 1| 3| 4|
| H2 | 4| 0| 1| 5|
| H3 | 1| 0| 3| 6|

### Confusion Matrix (cross-operator: templates on missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 10|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 0| 10|
| H3 | 0| 0| 0| 10|

### Confusion Matrix (cross-operator: templates on registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 10|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 0| 10|
| H3 | 0| 0| 0| 10|
## Scorer trained on: registration_gap_surrogate

- Best lambda: 1.0000e-03
- Same-operator accuracy: 0.2500
- False via rate (H0->H1): 0.0000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.2250
- On centerline_biot_savart: 0.1500
- On finite_width_surrogate: 0.3250
- On missing_return_surrogate: 0.3500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Ridge Instability Ratios (same / cross)

- registration_gap_surrogate_vs_analytic_reference: 1.11x
- registration_gap_surrogate_vs_centerline_biot_savart: 1.67x
- registration_gap_surrogate_vs_finite_width_surrogate: 0.77x
- registration_gap_surrogate_vs_missing_return_surrogate: 0.71x
- registration_gap_surrogate_vs_deep_layer_shift_surrogate: 1.00x

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 0| 10|
| H1 | 0| 0| 0| 10|
| H2 | 0| 0| 0| 10|
| H3 | 0| 0| 0| 10|

### Confusion Matrix (cross-operator: templates on analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 1| 2| 4|
| H1 | 0| 0| 1| 9|
| H2 | 3| 0| 0| 7|
| H3 | 2| 1| 1| 6|

### Confusion Matrix (cross-operator: templates on centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 2| 0| 2| 6|
| H1 | 0| 0| 2| 8|
| H2 | 4| 0| 0| 6|
| H3 | 3| 0| 3| 4|

### Confusion Matrix (cross-operator: templates on finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 2| 1| 2| 5|
| H1 | 0| 2| 3| 5|
| H2 | 3| 0| 0| 7|
| H3 | 0| 0| 1| 9|

### Confusion Matrix (cross-operator: templates on missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 4| 0| 0| 6|
| H1 | 1| 0| 0| 9|
| H2 | 1| 0| 0| 9|
| H3 | 0| 0| 0| 10|

### Confusion Matrix (cross-operator: templates on deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 10| 0| 0| 0|
| H1 | 10| 0| 0| 0|
| H2 | 10| 0| 0| 0|
| H3 | 10| 0| 0| 0|
