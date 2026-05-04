# PDN Physics Learning Evidence

Claim: `C10_pdn_kcl_distribution_need`

Evidence: `E12_pdn_physics_learning`

## What Was Tested

E12 reads the E11 generated chip-like PDN rows and compares CPU baselines:

- majority label baseline;
- residual/nearest-centroid scorer over `Bxyz` features;
- graph-agnostic ridge learner from `Bxyz` features to H0/H1/H2/H3 plus
  unconstrained edge-current regression;
- physics-aware learner that predicts a generated hypothesis and derives edge
  currents through graph/KCL projection.

Held-out and family-hidden rows are not used for feature scaling, fitting, or
model selection.

## Metrics

- E11 source rows: 96
- split roles: calibration 12, train 36, heldout 24, family-hidden 24
- majority held-out accuracy: `0.250`
- graph-agnostic held-out accuracy: `1.000`
- graph-agnostic family-hidden accuracy: `0.750`
- family generalization gap: `0.250`
- unconstrained max predicted KCL residual: `1.567e-02`
- physics-aware max predicted KCL residual: `3.830e-15`
- unconstrained max predicted closure error: `1.138e-13`
- physics-aware max predicted closure error: `7.046e-15`
- physics-aware field reconstruction RMSE: `2.166e-06`
- all acceptance gates passed: `true`

## Interpretation

The generated E11 rows support a limited physics-learning closure: label
learning is materially above the majority baseline, and the physics-aware graph
projection produces predicted currents with much better KCL and current closure
than unconstrained current regression.

## Claim Boundary

This cannot be claimed as real learned physics under real layouts. It does not
validate real chip PDNs, real CAD/Gerber/GDS imports, external FEM/FastHenry
solves, real QDM/NV data, or mechanism-level explanation. Label correctness is
not mechanism correctness.

