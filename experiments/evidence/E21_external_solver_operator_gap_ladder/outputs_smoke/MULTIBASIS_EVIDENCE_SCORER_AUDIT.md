# Multi-Basis Evidence Scorer Audit

Per-hypothesis PCA subspace evidence: d_h(y)^2 = ||y - Q_h Q_h^T y||^2.

## Scorer trained on: analytic_reference

- k components: 2
- Energy retained: 0.9625
- Same-operator accuracy: 0.6000
- Cross-operator drop: 0.3500
- False via rate (H0->H1): 0.1000
- Return-path confusion (H3->H1): 0.1000

### Cross-Operator Accuracy

- On analytic_reference: 0.6000
- On centerline_biot_savart: 0.4250
- On finite_width_surrogate: 0.5500
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 7| 1| 2| 0|
| H1 | 1| 6| 2| 1|
| H2 | 0| 2| 6| 2|
| H3 | 3| 1| 1| 5|

### Confusion Matrix (cross: centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 4| 3| 1| 2|
| H1 | 2| 5| 0| 3|
| H2 | 2| 2| 5| 1|
| H3 | 1| 4| 2| 3|

### Confusion Matrix (cross: finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 1| 4| 2|
| H1 | 2| 6| 2| 0|
| H2 | 1| 1| 8| 0|
| H3 | 0| 2| 3| 5|

### Confusion Matrix (cross: missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|

### Confusion Matrix (cross: deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|

### Confusion Matrix (cross: registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|
## Scorer trained on: centerline_biot_savart

- k components: 2
- Energy retained: 0.9714
- Same-operator accuracy: 0.5000
- Cross-operator drop: 0.3250
- False via rate (H0->H1): 0.4000
- Return-path confusion (H3->H1): 0.3000

### Cross-Operator Accuracy

- On analytic_reference: 0.4250
- On centerline_biot_savart: 0.5000
- On finite_width_surrogate: 0.4750
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.1750
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 4| 4| 2| 0|
| H1 | 1| 6| 1| 2|
| H2 | 4| 0| 6| 0|
| H3 | 1| 3| 2| 4|

### Confusion Matrix (cross: analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 4| 3| 0|
| H1 | 0| 6| 2| 2|
| H2 | 2| 0| 6| 2|
| H3 | 1| 5| 2| 2|

### Confusion Matrix (cross: finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 2| 5| 0|
| H1 | 2| 5| 1| 2|
| H2 | 3| 0| 5| 2|
| H3 | 1| 2| 1| 6|

### Confusion Matrix (cross: missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|

### Confusion Matrix (cross: deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 7| 3|
| H1 | 0| 0| 6| 4|
| H2 | 0| 0| 3| 7|
| H3 | 0| 0| 6| 4|

### Confusion Matrix (cross: registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|
## Scorer trained on: finite_width_surrogate

- k components: 2
- Energy retained: 0.9734
- Same-operator accuracy: 0.6250
- Cross-operator drop: 0.3750
- False via rate (H0->H1): 0.2000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.4500
- On centerline_biot_savart: 0.4250
- On finite_width_surrogate: 0.6250
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 5| 2| 3| 0|
| H1 | 1| 5| 2| 2|
| H2 | 3| 0| 6| 1|
| H3 | 1| 0| 0| 9|

### Confusion Matrix (cross: analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 2| 4| 3| 1|
| H1 | 0| 7| 1| 2|
| H2 | 4| 1| 5| 0|
| H3 | 1| 5| 0| 4|

### Confusion Matrix (cross: centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 5| 4| 1| 0|
| H1 | 2| 3| 1| 4|
| H2 | 7| 0| 3| 0|
| H3 | 2| 0| 2| 6|

### Confusion Matrix (cross: missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|

### Confusion Matrix (cross: deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|

### Confusion Matrix (cross: registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|
## Scorer trained on: missing_return_surrogate

- k components: 2
- Energy retained: 0.9686
- Same-operator accuracy: 0.2500
- Cross-operator drop: 0.0000
- False via rate (H0->H1): 0.0000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.4500
- On centerline_biot_savart: 0.4250
- On finite_width_surrogate: 0.3500
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|

### Confusion Matrix (cross: analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 6| 1| 3| 0|
| H1 | 3| 2| 2| 3|
| H2 | 0| 3| 6| 1|
| H3 | 2| 3| 1| 4|

### Confusion Matrix (cross: centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 5| 4| 1| 0|
| H1 | 1| 2| 1| 6|
| H2 | 2| 3| 4| 1|
| H3 | 0| 2| 2| 6|

### Confusion Matrix (cross: finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 4| 2| 3| 1|
| H1 | 6| 1| 2| 1|
| H2 | 2| 3| 5| 0|
| H3 | 1| 4| 1| 4|

### Confusion Matrix (cross: deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|

### Confusion Matrix (cross: registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|
## Scorer trained on: deep_layer_shift_surrogate

- k components: 2
- Energy retained: 0.9614
- Same-operator accuracy: 0.2500
- Cross-operator drop: 0.0000
- False via rate (H0->H1): 0.0000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.5000
- On centerline_biot_savart: 0.4500
- On finite_width_surrogate: 0.5000
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 10| 0| 0| 0|
| H1 | 10| 0| 0| 0|
| H2 | 10| 0| 0| 0|
| H3 | 10| 0| 0| 0|

### Confusion Matrix (cross: analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 5| 2| 1| 2|
| H1 | 1| 4| 3| 2|
| H2 | 2| 1| 4| 3|
| H3 | 1| 1| 1| 7|

### Confusion Matrix (cross: centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 4| 3| 0| 3|
| H1 | 0| 3| 1| 6|
| H2 | 0| 5| 3| 2|
| H3 | 1| 1| 0| 8|

### Confusion Matrix (cross: finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 2| 2| 3| 3|
| H1 | 2| 4| 3| 1|
| H2 | 0| 4| 6| 0|
| H3 | 1| 0| 1| 8|

### Confusion Matrix (cross: missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 10| 0| 0| 0|
| H1 | 10| 0| 0| 0|
| H2 | 10| 0| 0| 0|
| H3 | 10| 0| 0| 0|

### Confusion Matrix (cross: registration_gap_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 10| 0| 0| 0|
| H1 | 10| 0| 0| 0|
| H2 | 10| 0| 0| 0|
| H3 | 10| 0| 0| 0|
## Scorer trained on: registration_gap_surrogate

- k components: 2
- Energy retained: 0.9461
- Same-operator accuracy: 0.2500
- Cross-operator drop: 0.0000
- False via rate (H0->H1): 0.0000
- Return-path confusion (H3->H1): 0.0000

### Cross-Operator Accuracy

- On analytic_reference: 0.4500
- On centerline_biot_savart: 0.4500
- On finite_width_surrogate: 0.5250
- On missing_return_surrogate: 0.2500
- On deep_layer_shift_surrogate: 0.2500
- On registration_gap_surrogate: 0.2500

### Confusion Matrix (same-operator)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|

### Confusion Matrix (cross: analytic_reference)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 3| 4| 3| 0|
| H1 | 1| 5| 1| 3|
| H2 | 2| 2| 5| 1|
| H3 | 3| 1| 1| 5|

### Confusion Matrix (cross: centerline_biot_savart)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 5| 3| 1| 1|
| H1 | 3| 3| 0| 4|
| H2 | 1| 3| 6| 0|
| H3 | 2| 2| 2| 4|

### Confusion Matrix (cross: finite_width_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 5| 0| 3| 2|
| H1 | 3| 4| 2| 1|
| H2 | 3| 0| 7| 0|
| H3 | 1| 3| 1| 5|

### Confusion Matrix (cross: missing_return_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|

### Confusion Matrix (cross: deep_layer_shift_surrogate)

| Truth \\ Pred | H0| H1| H2| H3|
|---|---:|---:|---:|---:|
| H0 | 0| 0| 10| 0|
| H1 | 0| 0| 10| 0|
| H2 | 0| 0| 10| 0|
| H3 | 0| 0| 10| 0|
