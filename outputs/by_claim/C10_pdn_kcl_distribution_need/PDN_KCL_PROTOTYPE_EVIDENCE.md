# PDN/KCL Prototype Evidence

Claim: `C10_pdn_kcl_distribution_need`.

Evidence package: `E10_pdn_kcl_distribution`.

## Result

The first generated PDN/KCL circuit-graph loop is runnable. It generates small
resistive graphs with VDD, GND, load, vias, junctions, return paths, edge
resistance, solved edge currents, current closure, centerline Biot-Savart
`Bxyz`, and matched generated H0/H1/H2/H3 hypothesis rows.

| Metric | Current result |
|---|---:|
| generated cases | 60 |
| max interior KCL residual | 7.147e-16 |
| max current closure error | 3.128e-15 |
| max divB proxy residual | 0.003842 |
| held-out H0/H1/H2/H3 accuracy | 1.000 |
| H0 false-any rate | 0.000 |
| H1 recall | 1.000 |

Metrics source:
`experiments/evidence/E10_pdn_kcl_distribution/outputs/metrics.json`.

## Claim Boundary

This supports a generated-domain PDN/KCL prototype only.

Cannot claim:

- real-board PDN/KCL robustness;
- real CAD/Gerber/GDS validation;
- external FEM/FastHenry validation;
- real QDM/NV validation;
- mechanism-level correctness under real layouts.

## Next Evidence

Expand the generator toward CAD/Gerber/GDS-like graph families and add
independent external-solver held-out rows.

