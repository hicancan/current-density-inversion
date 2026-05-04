# RUN_REPORT - E11 Chip-Like PDN Distribution

Claim: `C10_pdn_kcl_distribution_need`.

This run generated a four-layer artificial micro-PDN with top straps,
intermediate mesh, lower return grid, via stacks, distributed loads, VDD/GND
ports, edge resistance, solved KCL currents, current closure, and `Bxyz`
centerline Biot-Savart fields.

## Metrics

# Chip-Like PDN Metrics Table

| Metric | Value | Gate |
|---|---:|---|
| case count | 96 | - |
| family count | 4 | - |
| layer count | 4 | - |
| node count range | 35 to 37 | - |
| edge count range | 65 to 68 | - |
| max KCL residual | 4.913e-15 | True |
| max closure error | 7.391e-15 | True |
| max divB proxy residual | 0.003 | True |
| heldout accuracy | 1.000 | True |
| family-hidden accuracy | 1.000 | True |


## Boundary

This is generated-domain evidence. It does not validate real chip layouts,
CAD/Gerber/GDS imports, external FEM/FastHenry solves, frequency-dependent PDN
effects, or real QDM/NV measurements.

## Agent Audit Metadata

- Metrics file: `outputs/metrics.json`
- Schema version: `research-ssot-metrics-v1`
- Calibration source: No calibration rows used for threshold or model selection.
- Threshold source: none
- Model-selection source: not_applicable
- Audit date: 2026-05-04
