# E27 Failure Modes

Generated at runtime; see `outputs/FAILURE_MODES.md` for results.

## Pre-registered failure modes

1. **Low edge Gamma**: Candidate defects with magnetic signatures below calibrated uncertainty.
2. **Pairwise non-separable**: Defect pairs whose signatures are too similar to distinguish.
3. **High empty rate**: Defects with no observable signature above noise.
4. **Singleton wrong**: Only one defect passes acceptance, but it is not the ground truth.
5. **Schur signal ratio < 2x**: Schur-designed states fail to provide significant signal improvement over random baselines.

## Inherent limitations

- Generated graph network is a simplified planar model.
- Edge-segment Biot-Savart uses midpoint quadrature; finite-width corrections not applied.
- Schur state design uses random search; real port constraints require combinatorial optimization.
- Operator perturbation rho is scalar; per-defect decomposition would give tighter bounds.
- Deep-layer defects have exponentially attenuated signals.
