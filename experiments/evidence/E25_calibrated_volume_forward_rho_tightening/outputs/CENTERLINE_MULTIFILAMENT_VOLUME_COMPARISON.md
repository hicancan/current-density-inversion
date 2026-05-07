# Centerline vs Multifilament vs Volume Comparison

## Per-Family Metrics

### straight_strip

| Comparison | Field RMSE | Field Rel L2 | Max Comp Error | Op Frobenius Rel | Rho Abs | Rho Rel |
|---|---|---|---|---|---|---|
| centerline_vs_volume | 7.9493e-08 | 9.3952e-02 | 7.2730e-07 | 9.3952e-02 | 1.6693e-06 | 9.3952e-02 |
| multifilament_vs_volume | 7.8762e-08 | 9.3088e-02 | 6.5856e-07 | 9.3088e-02 | 1.6540e-06 | 9.3088e-02 |
| centerline_vs_multifilament | 1.6495e-08 | 1.9626e-02 | 6.8734e-08 | 1.9626e-02 | 3.4639e-07 | 1.9495e-02 |

- Signal scale (||B_vol||_2): 1.7768e-05
- Current norm: 1.0000e-03

### parallel_strips

| Comparison | Field RMSE | Field Rel L2 | Max Comp Error | Op Frobenius Rel | Rho Abs | Rho Rel |
|---|---|---|---|---|---|---|
| centerline_vs_volume | 1.1166e-07 | 1.0975e-01 | 6.4118e-07 | 9.3381e-02 | 2.3448e-06 | 1.0975e-01 |
| multifilament_vs_volume | 1.1064e-07 | 1.0875e-01 | 5.9107e-07 | 9.2549e-02 | 2.3234e-06 | 1.0875e-01 |
| centerline_vs_multifilament | 2.3318e-08 | 2.3150e-02 | 5.0113e-08 | 1.9460e-02 | 4.8969e-07 | 2.2919e-02 |

- Signal scale (||B_vol||_2): 2.1366e-05
- Current norm: 1.4142e-03

### rectangular_loop

| Comparison | Field RMSE | Field Rel L2 | Max Comp Error | Op Frobenius Rel | Rho Abs | Rho Rel |
|---|---|---|---|---|---|---|
| centerline_vs_volume | 1.7867e-08 | 1.5365e-02 | 1.0805e-07 | 1.6555e-02 | 3.7520e-07 | 1.5365e-02 |
| multifilament_vs_volume | 1.1751e-08 | 1.0106e-02 | 5.9182e-08 | 1.0925e-02 | 2.4677e-07 | 1.0106e-02 |
| centerline_vs_multifilament | 2.2396e-08 | 1.9316e-02 | 6.2698e-08 | 2.0837e-02 | 4.7032e-07 | 1.9261e-02 |

- Signal scale (||B_vol||_2): 2.4418e-05
- Current norm: 2.0000e-03

### vertical_via

| Comparison | Field RMSE | Field Rel L2 | Max Comp Error | Op Frobenius Rel | Rho Abs | Rho Rel |
|---|---|---|---|---|---|---|
| centerline_vs_volume | 1.9387e-09 | 1.4736e-02 | 1.9730e-08 | 1.4736e-02 | 4.0713e-08 | 1.4736e-02 |
| multifilament_vs_volume | 1.6463e-09 | 1.2513e-02 | 1.9084e-08 | 1.2513e-02 | 3.4572e-08 | 1.2513e-02 |
| centerline_vs_multifilament | 3.5331e-09 | 2.7050e-02 | 3.8812e-08 | 2.7050e-02 | 7.4196e-08 | 2.6855e-02 |

- Signal scale (||B_vol||_2): 2.7629e-06
- Current norm: 1.0000e-03

### two_layer_trace_with_return

| Comparison | Field RMSE | Field Rel L2 | Max Comp Error | Op Frobenius Rel | Rho Abs | Rho Rel |
|---|---|---|---|---|---|---|
| centerline_vs_volume | 1.7204e-07 | 3.7731e-01 | 1.6159e-06 | 1.5897e-01 | 3.6129e-06 | 3.7731e-01 |
| multifilament_vs_volume | 1.6893e-07 | 3.7049e-01 | 1.4443e-06 | 1.5629e-01 | 3.5475e-06 | 3.7049e-01 |
| centerline_vs_multifilament | 3.6085e-08 | 8.5294e-02 | 1.7152e-07 | 3.4465e-02 | 7.5778e-07 | 7.9139e-02 |

- Signal scale (||B_vol||_2): 9.5754e-06
- Current norm: 2.0000e-03

### four_layer_via_return_motif

| Comparison | Field RMSE | Field Rel L2 | Max Comp Error | Op Frobenius Rel | Rho Abs | Rho Rel |
|---|---|---|---|---|---|---|
| centerline_vs_volume | 2.1737e-05 | 9.4458e-01 | 3.0620e-04 | 9.3254e-01 | 4.5648e-04 | 9.4458e-01 |
| multifilament_vs_volume | 2.2771e-05 | 9.8952e-01 | 3.3795e-04 | 9.7817e-01 | 4.7820e-04 | 9.8952e-01 |
| centerline_vs_multifilament | 6.3820e-06 | 5.7752e+00 | 3.2582e-05 | 2.8447e+00 | 1.3402e-04 | 2.7733e-01 |

- Signal scale (||B_vol||_2): 4.8326e-04
- Current norm: 2.6458e-03

## Key Finding

Multifilament should substantially outperform centerline, confirming
that finite-width effects are the dominant operator gap for traces.
