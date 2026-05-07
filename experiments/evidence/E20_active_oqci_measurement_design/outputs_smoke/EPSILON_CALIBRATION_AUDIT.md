# Epsilon Calibration Audit

Epsilon calibrated from truth residual quantiles on calibration split,
evaluated on held-out evaluation split.

## add_h1.6_Bxyz
  - fit_mode: ridge
  - lambda: 1e-04
  - calibration cases: 3
  - evaluation cases: 3

### Calibration

  - truth_residual_mean: 0.2611
  - truth_residual_median: 0.2577

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.2728 | 0.0000 | 0.6667 | 0.0000 | 0.0000 |
| q0.95 | 0.2747 | 0.0000 | 0.6667 | 0.0000 | 0.0000 |
| q0.99 | 0.2762 | 0.0000 | 0.6667 | 0.0000 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.2728 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.95 | 0.2747 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.99 | 0.2762 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |

## add_h6.4_Bz
  - fit_mode: ridge
  - lambda: 1e+00
  - calibration cases: 3
  - evaluation cases: 3

### Calibration

  - truth_residual_mean: 0.2206
  - truth_residual_median: 0.2202

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.2307 | 0.0000 | 0.6667 | 0.0000 | 0.0000 |
| q0.95 | 0.2320 | 0.0000 | 0.6667 | 0.0000 | 0.0000 |
| q0.99 | 0.2331 | 0.0000 | 0.6667 | 0.0000 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.2307 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.95 | 0.2320 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.99 | 0.2331 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |

## add_state2_Bz
  - fit_mode: ridge
  - lambda: 1e-04
  - calibration cases: 3
  - evaluation cases: 3

### Calibration

  - truth_residual_mean: 0.2837
  - truth_residual_median: 0.2791

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.2946 | 0.0000 | 0.6667 | 0.3333 | 0.0000 |
| q0.95 | 0.2965 | 0.0000 | 0.6667 | 0.3333 | 0.0000 |
| q0.99 | 0.2980 | 0.0000 | 0.6667 | 0.3333 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.2946 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.95 | 0.2965 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.99 | 0.2980 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |

## add_state4_Bxyz
  - fit_mode: ridge
  - lambda: 1e-04
  - calibration cases: 3
  - evaluation cases: 3

### Calibration

  - truth_residual_mean: 0.4258
  - truth_residual_median: 0.4211

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.4434 | 0.0000 | 0.6667 | 0.3333 | 0.0000 |
| q0.95 | 0.4462 | 0.0000 | 0.6667 | 0.3333 | 0.0000 |
| q0.99 | 0.4484 | 0.0000 | 0.6667 | 0.3333 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.4434 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.95 | 0.4462 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.99 | 0.4484 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |

## add_h1.6_state2_Bz
  - fit_mode: ridge
  - lambda: 1e-04
  - calibration cases: 3
  - evaluation cases: 3

### Calibration

  - truth_residual_mean: 0.3469
  - truth_residual_median: 0.3428

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.3587 | 0.0000 | 0.6667 | 0.3333 | 0.0000 |
| q0.95 | 0.3606 | 0.0000 | 0.6667 | 0.3333 | 0.0000 |
| q0.99 | 0.3622 | 0.0000 | 0.6667 | 0.3333 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.3587 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.95 | 0.3606 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.99 | 0.3622 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
