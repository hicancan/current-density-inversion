# Margin Refusal Operator Gap Audit

Margin = score_second_best - score_best. Accept if margin >= 50th-percentile threshold.

## Scorer trained on: analytic_reference

- Margin threshold: 2.166364e-10
- Accepted rate (same-op): 0.0000
- Accepted accuracy (same-op): 0.0000

### Cross-Operator Margin Audit

| Test Op | Accept Rate | Accept Acc | Wrong Accept | Refusal Rate |
|---|---:|---:|---:|---:|
| analytic_reference | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| centerline_biot_savart | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| deep_layer_shift_surrogate | 1.0000 | 0.2500 | 0.7500 | 0.0000 |
| finite_width_surrogate | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| missing_return_surrogate | 1.0000 | 0.2500 | 0.7500 | 0.0000 |
| registration_gap_surrogate | 1.0000 | 0.2500 | 0.7500 | 0.0000 |

## Scorer trained on: centerline_biot_savart

- Margin threshold: 2.166364e-10
- Accepted rate (same-op): 0.0000
- Accepted accuracy (same-op): 0.0000

### Cross-Operator Margin Audit

| Test Op | Accept Rate | Accept Acc | Wrong Accept | Refusal Rate |
|---|---:|---:|---:|---:|
| analytic_reference | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| centerline_biot_savart | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| deep_layer_shift_surrogate | 1.0000 | 0.2500 | 0.7500 | 0.0000 |
| finite_width_surrogate | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| missing_return_surrogate | 1.0000 | 0.2500 | 0.7500 | 0.0000 |
| registration_gap_surrogate | 1.0000 | 0.2500 | 0.7500 | 0.0000 |

## Scorer trained on: finite_width_surrogate

- Margin threshold: 2.166364e-10
- Accepted rate (same-op): 0.0000
- Accepted accuracy (same-op): 0.0000

### Cross-Operator Margin Audit

| Test Op | Accept Rate | Accept Acc | Wrong Accept | Refusal Rate |
|---|---:|---:|---:|---:|
| analytic_reference | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| centerline_biot_savart | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| deep_layer_shift_surrogate | 1.0000 | 0.2500 | 0.7500 | 0.0000 |
| finite_width_surrogate | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| missing_return_surrogate | 0.1875 | 0.2500 | 0.7500 | 0.8125 |
| registration_gap_surrogate | 0.0000 | 0.0000 | 0.0000 | 1.0000 |

## Scorer trained on: missing_return_surrogate

- Margin threshold: 2.166364e-10
- Accepted rate (same-op): 1.0000
- Accepted accuracy (same-op): 0.2969

### Cross-Operator Margin Audit

| Test Op | Accept Rate | Accept Acc | Wrong Accept | Refusal Rate |
|---|---:|---:|---:|---:|
| analytic_reference | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| centerline_biot_savart | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| deep_layer_shift_surrogate | 1.0000 | 0.2500 | 0.7500 | 0.0000 |
| finite_width_surrogate | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| missing_return_surrogate | 1.0000 | 0.2969 | 0.7031 | 0.0000 |
| registration_gap_surrogate | 1.0000 | 0.2812 | 0.7188 | 0.0000 |

## Scorer trained on: deep_layer_shift_surrogate

- Margin threshold: 2.166364e-10
- Accepted rate (same-op): 1.0000
- Accepted accuracy (same-op): 0.2969

### Cross-Operator Margin Audit

| Test Op | Accept Rate | Accept Acc | Wrong Accept | Refusal Rate |
|---|---:|---:|---:|---:|
| analytic_reference | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| centerline_biot_savart | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| deep_layer_shift_surrogate | 1.0000 | 0.2969 | 0.7031 | 0.0000 |
| finite_width_surrogate | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| missing_return_surrogate | 1.0000 | 0.2500 | 0.7500 | 0.0000 |
| registration_gap_surrogate | 0.9688 | 0.3065 | 0.6935 | 0.0312 |

## Scorer trained on: registration_gap_surrogate

- Margin threshold: 2.166364e-10
- Accepted rate (same-op): 1.0000
- Accepted accuracy (same-op): 0.3125

### Cross-Operator Margin Audit

| Test Op | Accept Rate | Accept Acc | Wrong Accept | Refusal Rate |
|---|---:|---:|---:|---:|
| analytic_reference | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| centerline_biot_savart | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| deep_layer_shift_surrogate | 1.0000 | 0.2500 | 0.7500 | 0.0000 |
| finite_width_surrogate | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| missing_return_surrogate | 1.0000 | 0.2500 | 0.7500 | 0.0000 |
| registration_gap_surrogate | 1.0000 | 0.3125 | 0.6875 | 0.0000 |

