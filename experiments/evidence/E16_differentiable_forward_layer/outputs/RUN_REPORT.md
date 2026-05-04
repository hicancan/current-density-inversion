# E16 Differentiable Biot-Savart Forward Layer -- Run Report

**Generated**: 2026-05-04T07:59:50Z
**Status**: passed
**All gates passed**: True

## Acceptance Gates

| Gate | Result |
|------|--------|
| `numpy_reference_passes` | PASS |
| `sheet_forward_sanity_passes` | PASS |
| `via_forward_sanity_passes` | PASS |
| `k0_handling_documented` | PASS |
| `padding_boundary_documented` | PASS |
| `torch_optional_path_does_not_break_cpu` | PASS |

## Key Metrics

| Metric | Value |
|--------|-------|
| Superposition error | 6.912e-16 |
| Antisymmetry error | 0.000e+00 |
| Standoff monotonic | True |
| Torch available | False |
| CUDA available | False |

## Cannot Claim

- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL agreement
- finite-width conductor agreement
- return-path completeness
- that differentiable forward guarantees better inverse
- that the forward layer is a substitute for external solver validation

Full results in `outputs/metrics.json`.

## Agent Audit Metadata

- Metrics file: `outputs/metrics.json`
- Schema version: `research-ssot-metrics-v1`
- Calibration source: No calibration rows used for threshold or model selection.
- Threshold source: none
- Model-selection source: not_applicable
- Audit date: 2026-05-04
