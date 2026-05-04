# E18 Physics-Constrained PDN Inverse Evidence

## Claim: C04_inverse_crime_and_operator_gap

### Evidence summary

E18 uses the same Biot-Savart forward operator for both data generation and
inversion (same-operator benchmark). This is an explicit inverse crime
configuration that provides an upper bound on achievable accuracy.

### Key results

- B residual = 1.000 (relative L2) for all methods — same operator, no gap
- The unified leaderboard comparison is fair: all methods use the same
  forward operator and the same generated data
- Differences in current accuracy are due to regularization strategy, not
  operator mismatch

### Cannot claim

- Operator gap has been tested (it has not)
- External solver forward produces different results
- Real measurement noise, registration, or sensor calibration effects

### Metrics

See `experiments/evidence/E18_physics_constrained_pdn_inverse/outputs/metrics.json`
