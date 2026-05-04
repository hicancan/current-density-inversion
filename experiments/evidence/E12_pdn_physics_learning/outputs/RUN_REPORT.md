# RUN_REPORT - E12 PDN Physics Learning

Claim: `C10_pdn_kcl_distribution_need`.

This run reads/generated E11 chip-like PDN rows and evaluates whether a CPU
baseline can improve label learning while also improving predicted-current KCL
and current closure. The physics-aware branch uses generated graph/KCL
projection; therefore the result is evidence for generated-domain physics
closure, not for real mechanism explanation.

## Metrics

# PDN Physics Learning Metrics Table

| Metric | Value | Gate |
|---|---:|---|
| heldout accuracy | 1.000 | True |
| majority heldout accuracy | 0.250 | - |
| family generalization gap | 0.250 | True |
| unconstrained max KCL residual | 0.016 | - |
| physics-aware max KCL residual | 3.830e-15 | True |
| unconstrained max closure error | 1.138e-13 | - |
| physics-aware max closure error | 7.046e-15 | True |
| physics-aware field RMSE | 0.000 | True |


## Boundary

This evidence cannot be claimed as real chip, CAD/Gerber/GDS, external solver,
real QDM/NV, or mechanism-level validation. Label correctness remains separate
from mechanism correctness.

## Agent Audit Metadata

- Metrics file: `outputs/metrics.json`
- Schema version: `research-ssot-metrics-v1`
- Calibration source: No calibration rows used for threshold or model selection.
- Threshold source: none
- Model-selection source: not_applicable
- Audit date: 2026-05-04
