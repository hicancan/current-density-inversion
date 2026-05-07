# Multi-Basis Evidence Scorer Audit

Per-hypothesis PCA subspace evidence: d_h(y)^2 = ||y - Q_h Q_h^T y||^2.

## Scorer trained on: analytic_reference

- k components: 2
- Energy retained: 0.9745
- Same-operator accuracy: 0.4062
- Cross-operator drop: 0.1562
- False via rate (H0->H1): 0.1250
- Return-path confusion (H3->H1): 0.5000

### Cross-Operator Accuracy

- On analytic_reference: 0.4062
- On centerline_biot_savart: 0.3906
- On finite_width_surrogate: 0.4688
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 8| 2| 6| 0|
| H1 | 6| 4| 2| 4|
| H2 | 2| 4| 9| 1|
| H3 | 3| 8| 0| 5|

### Confusion Matrix (cross: centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 9| 3| 4| 0|
| H1 | 6| 5| 1| 4|
| H2 | 9| 2| 4| 1|
| H3 | 1| 7| 1| 7|

### Confusion Matrix (cross: finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 7| 7| 0| 2|
| H1 | 4| 6| 0| 6|
| H2 | 4| 4| 8| 0|
| H3 | 0| 6| 1| 9|

### Confusion Matrix (cross: missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 16| 0| 0|
| H1 | 0| 16| 0| 0|
| H2 | 0| 16| 0| 0|
| H3 | 0| 16| 0| 0|

### Confusion Matrix (cross: deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 16| 0| 0|
| H1 | 0| 16| 0| 0|
| H2 | 0| 16| 0| 0|
| H3 | 0| 16| 0| 0|

### Confusion Matrix (cross: registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 16| 0| 0|
| H1 | 0| 16| 0| 0|
| H2 | 0| 16| 0| 0|
| H3 | 0| 16| 0| 0|
## Scorer trained on: centerline_biot_savart

- k components: 2
- Energy retained: 0.9536
- Same-operator accuracy: 0.5000
- Cross-operator drop: 0.2500
- False via rate (H0->H1): 0.2500
- Return-path confusion (H3->H1): 0.2500

### Cross-Operator Accuracy

- On analytic_reference: 0.5156
- On centerline_biot_savart: 0.5000
- On finite_width_surrogate: 0.6094
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 5| 4| 4| 3|
| H1 | 0| 10| 3| 3|
| H2 | 8| 0| 7| 1|
| H3 | 1| 4| 1| 10|

### Confusion Matrix (cross: analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 7| 4| 4| 1|
| H1 | 4| 6| 3| 3|
| H2 | 4| 0| 10| 2|
| H3 | 0| 5| 1| 10|

### Confusion Matrix (cross: finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 6| 2| 4| 4|
| H1 | 1| 8| 1| 6|
| H2 | 2| 1| 12| 1|
| H3 | 0| 1| 2| 13|

### Confusion Matrix (cross: missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 16| 0|
| H1 | 0| 0| 16| 0|
| H2 | 0| 0| 16| 0|
| H3 | 0| 0| 16| 0|

### Confusion Matrix (cross: deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 16| 0|
| H1 | 0| 0| 16| 0|
| H2 | 0| 0| 16| 0|
| H3 | 0| 0| 16| 0|

### Confusion Matrix (cross: registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 16| 0| 0|
| H1 | 0| 16| 0| 0|
| H2 | 0| 16| 0| 0|
| H3 | 0| 16| 0| 0|
## Scorer trained on: finite_width_surrogate

- k components: 2
- Energy retained: 0.9651
- Same-operator accuracy: 0.6562
- Cross-operator drop: 0.4062
- False via rate (H0->H1): 0.1250
- Return-path confusion (H3->H1): 0.1875

### Cross-Operator Accuracy

- On analytic_reference: 0.4688
- On centerline_biot_savart: 0.6250
- On finite_width_surrogate: 0.6562
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 8| 2| 5| 1|
| H1 | 1| 10| 1| 4|
| H2 | 2| 1| 13| 0|
| H3 | 0| 3| 2| 11|

### Confusion Matrix (cross: analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 6| 2| 8| 0|
| H1 | 4| 5| 3| 4|
| H2 | 3| 0| 10| 3|
| H3 | 0| 6| 1| 9|

### Confusion Matrix (cross: centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 9| 3| 2| 2|
| H1 | 0| 8| 4| 4|
| H2 | 1| 2| 13| 0|
| H3 | 1| 4| 1| 10|

### Confusion Matrix (cross: missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 16| 0|
| H1 | 0| 0| 16| 0|
| H2 | 0| 0| 16| 0|
| H3 | 0| 0| 16| 0|

### Confusion Matrix (cross: deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 16| 0|
| H1 | 0| 0| 16| 0|
| H2 | 0| 0| 16| 0|
| H3 | 0| 0| 16| 0|

### Confusion Matrix (cross: registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 16| 0|
| H1 | 0| 0| 16| 0|
| H2 | 0| 0| 16| 0|
| H3 | 0| 0| 16| 0|
## Scorer trained on: missing_return_surrogate

- k components: 2
- Energy retained: 0.9506
- Same-operator accuracy: 0.2500
- Cross-operator drop: 0.0000
- False via rate (H0->H1): 0.0000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.4531
- On centerline_biot_savart: 0.5156
- On finite_width_surrogate: 0.5781
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 16| 0|
| H1 | 0| 0| 16| 0|
| H2 | 0| 0| 16| 0|
| H3 | 0| 0| 16| 0|

### Confusion Matrix (cross: analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 8| 3| 4| 1|
| H1 | 4| 5| 4| 3|
| H2 | 4| 0| 8| 4|
| H3 | 1| 5| 2| 8|

### Confusion Matrix (cross: centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 7| 4| 3| 2|
| H1 | 1| 10| 1| 4|
| H2 | 6| 3| 7| 0|
| H3 | 0| 6| 1| 9|

### Confusion Matrix (cross: finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 6| 3| 6| 1|
| H1 | 5| 7| 1| 3|
| H2 | 2| 0| 13| 1|
| H3 | 2| 1| 2| 11|

### Confusion Matrix (cross: deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 16| 0|
| H1 | 0| 0| 16| 0|
| H2 | 0| 0| 16| 0|
| H3 | 0| 0| 16| 0|

### Confusion Matrix (cross: registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 16| 0| 0| 0|
| H1 | 16| 0| 0| 0|
| H2 | 16| 0| 0| 0|
| H3 | 16| 0| 0| 0|
## Scorer trained on: deep_layer_shift_surrogate

- k components: 2
- Energy retained: 0.9673
- Same-operator accuracy: 0.2500
- Cross-operator drop: 0.0000
- False via rate (H0->H1): 0.0000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.4375
- On centerline_biot_savart: 0.5156
- On finite_width_surrogate: 0.5938
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 16| 0|
| H1 | 0| 0| 16| 0|
| H2 | 0| 0| 16| 0|
| H3 | 0| 0| 16| 0|

### Confusion Matrix (cross: analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 7| 2| 6| 1|
| H1 | 4| 8| 3| 1|
| H2 | 3| 3| 9| 1|
| H3 | 0| 11| 1| 4|

### Confusion Matrix (cross: centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 9| 4| 2| 1|
| H1 | 3| 9| 2| 2|
| H2 | 2| 3| 11| 0|
| H3 | 1| 10| 1| 4|

### Confusion Matrix (cross: finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 9| 2| 5| 0|
| H1 | 4| 8| 2| 2|
| H2 | 2| 2| 12| 0|
| H3 | 1| 4| 2| 9|

### Confusion Matrix (cross: missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 16| 0|
| H1 | 0| 0| 16| 0|
| H2 | 0| 0| 16| 0|
| H3 | 0| 0| 16| 0|

### Confusion Matrix (cross: registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 16| 0|
| H1 | 0| 0| 16| 0|
| H2 | 0| 0| 16| 0|
| H3 | 0| 0| 16| 0|
## Scorer trained on: registration_gap_surrogate

- k components: 2
- Energy retained: 0.9680
- Same-operator accuracy: 0.2500
- Cross-operator drop: 0.0156
- False via rate (H0->H1): 0.0000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.3906
- On centerline_biot_savart: 0.4688
- On finite_width_surrogate: 0.5000
- On missing_return_surrogate: 0.2344
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 16| 0| 0| 0|
| H1 | 16| 0| 0| 0|
| H2 | 16| 0| 0| 0|
| H3 | 16| 0| 0| 0|

### Confusion Matrix (cross: analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 5| 6| 4| 1|
| H1 | 6| 9| 0| 1|
| H2 | 2| 6| 6| 2|
| H3 | 3| 7| 1| 5|

### Confusion Matrix (cross: centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 4| 7| 2| 3|
| H1 | 3| 9| 2| 2|
| H2 | 1| 2| 12| 1|
| H3 | 1| 9| 1| 5|

### Confusion Matrix (cross: finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 4| 5| 5| 2|
| H1 | 5| 6| 1| 4|
| H2 | 2| 3| 11| 0|
| H3 | 0| 4| 1| 11|

### Confusion Matrix (cross: missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 15| 0| 1| 0|
| H1 | 16| 0| 0| 0|
| H2 | 16| 0| 0| 0|
| H3 | 15| 0| 1| 0|

### Confusion Matrix (cross: deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 16| 0| 0| 0|
| H1 | 16| 0| 0| 0|
| H2 | 16| 0| 0| 0|
| H3 | 16| 0| 0| 0|
