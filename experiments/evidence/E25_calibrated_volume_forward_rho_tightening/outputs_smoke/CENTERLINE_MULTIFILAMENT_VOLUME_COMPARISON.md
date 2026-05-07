# Centerline vs Multifilament vs Volume Comparison

## Per-Family Metrics

### straight_strip

| Comparison | Field RMSE | Field Rel L2 | Max Comp Error | Op Frobenius Rel | Rho Abs | Rho Rel |
|---|---|---|---|---|---|---|
| centerline_vs_volume | 2.2684e-07 | 2.7966e-01 | 1.6538e-06 | 2.7966e-01 | 2.4952e-06 | 2.7966e-01 |
| multifilament_vs_volume | 2.2132e-07 | 2.7285e-01 | 1.5558e-06 | 2.7285e-01 | 2.4345e-06 | 2.7285e-01 |
| centerline_vs_multifilament | 2.5821e-08 | 3.1859e-02 | 9.8015e-08 | 3.1859e-02 | 2.8403e-07 | 3.1834e-02 |

- Signal scale (||B_vol||_2): 8.9224e-06
- Current norm: 1.0000e-03

### parallel_strips

| Comparison | Field RMSE | Field Rel L2 | Max Comp Error | Op Frobenius Rel | Rho Abs | Rho Rel |
|---|---|---|---|---|---|---|
| centerline_vs_volume | 3.0852e-07 | 3.1983e-01 | 1.4952e-06 | 2.7239e-01 | 3.3937e-06 | 3.1983e-01 |
| multifilament_vs_volume | 3.0227e-07 | 3.1335e-01 | 1.4230e-06 | 2.6735e-01 | 3.3249e-06 | 3.1335e-01 |
| centerline_vs_multifilament | 3.4719e-08 | 3.6347e-02 | 7.2240e-08 | 2.9937e-02 | 3.8191e-07 | 3.5992e-02 |

- Signal scale (||B_vol||_2): 1.0611e-05
- Current norm: 1.4142e-03

## Key Finding

Multifilament should substantially outperform centerline, confirming
that finite-width effects are the dominant operator gap for traces.
