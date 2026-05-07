# Epsilon Calibration Audit

Epsilon calibrated from truth residual quantiles on calibration split,
evaluated on held-out evaluation split.

## add_h1.6_Bxyz
  - fit_mode: ridge
  - lambda: 1e-02
  - calibration cases: 9
  - evaluation cases: 9

### Calibration

  - truth_residual_mean: 0.4689
  - truth_residual_median: 0.4406

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.5308 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.95 | 0.5371 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.99 | 0.5421 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.5308 | 0.2222 | 1.0000 | 0.0000 | 0.0000 |
| q0.95 | 0.5371 | 0.2222 | 1.0000 | 0.0000 | 0.0000 |
| q0.99 | 0.5421 | 0.2222 | 1.0000 | 0.0000 | 0.0000 |

## add_h1.6_Bz
  - fit_mode: ridge
  - lambda: 1e-01
  - calibration cases: 9
  - evaluation cases: 9

### Calibration

  - truth_residual_mean: 0.3670
  - truth_residual_median: 0.3620

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.3992 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.95 | 0.4016 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.99 | 0.4035 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.3992 | 0.1111 | 0.8889 | 0.0000 | 0.1111 |
| q0.95 | 0.4016 | 0.0000 | 0.8889 | 0.0000 | 0.1111 |
| q0.99 | 0.4035 | 0.0000 | 0.8889 | 0.0000 | 0.1111 |

## add_h6.4_Bxyz
  - fit_mode: ridge
  - lambda: 1e-04
  - calibration cases: 9
  - evaluation cases: 9

### Calibration

  - truth_residual_mean: 0.4439
  - truth_residual_median: 0.4366

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.4646 | 0.1111 | 0.8889 | 0.0000 | 0.0000 |
| q0.95 | 0.4696 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.99 | 0.4737 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.4646 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.95 | 0.4696 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| q0.99 | 0.4737 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |

## add_h6.4_Bz
  - fit_mode: ridge
  - lambda: 1e-01
  - calibration cases: 9
  - evaluation cases: 9

### Calibration

  - truth_residual_mean: 0.3630
  - truth_residual_median: 0.3613

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.3891 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.95 | 0.3905 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.99 | 0.3916 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.3891 | 0.0000 | 0.8889 | 0.0000 | 0.1111 |
| q0.95 | 0.3905 | 0.0000 | 0.8889 | 0.1111 | 0.0000 |
| q0.99 | 0.3916 | 0.0000 | 0.8889 | 0.1111 | 0.0000 |

## add_h12.8_Bz
  - fit_mode: ridge
  - lambda: 1e-01
  - calibration cases: 9
  - evaluation cases: 9

### Calibration

  - truth_residual_mean: 0.3630
  - truth_residual_median: 0.3611

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.3888 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.95 | 0.3902 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.99 | 0.3914 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.3888 | 0.0000 | 0.8889 | 0.0000 | 0.1111 |
| q0.95 | 0.3902 | 0.0000 | 0.8889 | 0.1111 | 0.0000 |
| q0.99 | 0.3914 | 0.0000 | 0.8889 | 0.1111 | 0.0000 |

## add_state2_Bz
  - fit_mode: ridge
  - lambda: 1e-04
  - calibration cases: 9
  - evaluation cases: 9

### Calibration

  - truth_residual_mean: 0.6129
  - truth_residual_median: 0.5966

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.6575 | 0.0000 | 0.8889 | 0.0000 | 0.1111 |
| q0.95 | 0.6669 | 0.0000 | 0.8889 | 0.0000 | 0.1111 |
| q0.99 | 0.6744 | 0.0000 | 0.8889 | 0.0000 | 0.1111 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.6575 | 0.1111 | 0.8889 | 0.0000 | 0.1111 |
| q0.95 | 0.6669 | 0.1111 | 0.8889 | 0.0000 | 0.1111 |
| q0.99 | 0.6744 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |

## add_state2_Bxyz
  - fit_mode: ridge
  - lambda: 1e-04
  - calibration cases: 9
  - evaluation cases: 9

### Calibration

  - truth_residual_mean: 0.6129
  - truth_residual_median: 0.5966

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.6575 | 0.0000 | 0.8889 | 0.0000 | 0.1111 |
| q0.95 | 0.6669 | 0.0000 | 0.8889 | 0.0000 | 0.1111 |
| q0.99 | 0.6744 | 0.0000 | 0.8889 | 0.0000 | 0.1111 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.6575 | 0.1111 | 0.8889 | 0.0000 | 0.1111 |
| q0.95 | 0.6669 | 0.1111 | 0.8889 | 0.0000 | 0.1111 |
| q0.99 | 0.6744 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |

## add_state4_Bz
  - fit_mode: ridge
  - lambda: 1e-04
  - calibration cases: 9
  - evaluation cases: 9

### Calibration

  - truth_residual_mean: 0.9442
  - truth_residual_median: 0.9563

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.9681 | 0.0000 | 0.8889 | 0.1111 | 0.0000 |
| q0.95 | 0.9785 | 0.0000 | 0.8889 | 0.1111 | 0.0000 |
| q0.99 | 0.9869 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.9681 | 0.2222 | 0.8889 | 0.0000 | 0.1111 |
| q0.95 | 0.9785 | 0.2222 | 0.8889 | 0.0000 | 0.0000 |
| q0.99 | 0.9869 | 0.1111 | 1.0000 | 0.0000 | 0.0000 |

## add_state4_Bxyz
  - fit_mode: ridge
  - lambda: 1e-04
  - calibration cases: 9
  - evaluation cases: 9

### Calibration

  - truth_residual_mean: 0.9442
  - truth_residual_median: 0.9563

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.9681 | 0.0000 | 0.8889 | 0.1111 | 0.0000 |
| q0.95 | 0.9785 | 0.0000 | 0.8889 | 0.1111 | 0.0000 |
| q0.99 | 0.9869 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.9681 | 0.2222 | 0.8889 | 0.0000 | 0.1111 |
| q0.95 | 0.9785 | 0.2222 | 0.8889 | 0.0000 | 0.0000 |
| q0.99 | 0.9869 | 0.1111 | 1.0000 | 0.0000 | 0.0000 |

## add_h1.6_state2_Bz
  - fit_mode: ridge
  - lambda: 1e-04
  - calibration cases: 9
  - evaluation cases: 9

### Calibration

  - truth_residual_mean: 0.7849
  - truth_residual_median: 0.7974

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.8462 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.95 | 0.8468 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.99 | 0.8472 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 0.8462 | 0.0000 | 0.6667 | 0.0000 | 0.3333 |
| q0.95 | 0.8468 | 0.0000 | 0.6667 | 0.0000 | 0.3333 |
| q0.99 | 0.8472 | 0.0000 | 0.6667 | 0.0000 | 0.3333 |

## add_h1.6_state4_Bxyz
  - fit_mode: ridge
  - lambda: 1e-04
  - calibration cases: 9
  - evaluation cases: 9

### Calibration

  - truth_residual_mean: 2.0460
  - truth_residual_median: 2.0319

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 2.1357 | 0.0000 | 0.8889 | 0.1111 | 0.0000 |
| q0.95 | 2.1536 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |
| q0.99 | 2.1679 | 0.0000 | 0.8889 | 0.0000 | 0.0000 |

### Evaluation

| quantile | epsilon | VDR | ticr | SWR | ER |
|---|---:|---:|---:|---:|---:|
| q0.90 | 2.1357 | 0.0000 | 0.7778 | 0.0000 | 0.2222 |
| q0.95 | 2.1536 | 0.0000 | 0.7778 | 0.0000 | 0.2222 |
| q0.99 | 2.1679 | 0.0000 | 0.7778 | 0.0000 | 0.2222 |
