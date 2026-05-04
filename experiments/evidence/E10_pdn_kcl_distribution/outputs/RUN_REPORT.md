# RUN_REPORT - E10 PDN/KCL Distribution

Claim: `C10_pdn_kcl_distribution_need`.

This run implements the first generated PDN/KCL circuit-graph evidence loop:
resistive graph generation, nodal KCL solve, current closure, centerline
Biot-Savart forward fields, and H0/H1/H2/H3 generated hypothesis scoring.

## Metrics

# PDN/KCL Metrics Table

| Metric | Value | Gate |
|---|---:|---|
| max interior KCL residual | 7.147e-16 | True |
| max current closure error | 3.128e-15 | True |
| max divB proxy residual | 0.004 | True |
| heldout H0/H1/H2/H3 accuracy | 1.000 | True |

Cannot claim: real CAD/Gerber/GDS, real QDM/NV, or external FEM/FastHenry validation.


## Case Counts

# Case Counts Table

| Group | Count |
|---|---:|
| H0_nominal_pdn | 15 |
| H1_extra_via | 15 |
| H2_return_path_shift | 15 |
| H3_bend_artifact | 15 |
| split:calibration | 12 |
| split:heldout | 36 |
| split:train | 12 |


## Boundary

This evidence supports only a generated-domain PDN/KCL prototype. It cannot be
claimed as real CAD/Gerber/GDS, external FEM/FastHenry, or real QDM/NV
validation.

## Agent Audit Metadata

- Metrics file: `outputs/metrics.json`
- Schema version: `research-ssot-metrics-v1`
- Calibration source: No calibration rows used for threshold or model selection.
- Threshold source: none
- Model-selection source: not_applicable
- Audit date: 2026-05-04
