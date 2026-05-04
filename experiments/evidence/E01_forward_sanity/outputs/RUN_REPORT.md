# exp01 Run Report

## Role

MVP-0 forward-operator sanity check. This experiment verifies signs, units,
linearity, analytic consistency, via field direction, and standoff scaling before
any inverse model or synthetic training data is trusted.

## Gate Summary

Overall: PASS

- finite_wire_matches_infinite_reference: PASS; value=0.000905331408941824; threshold=relative_l2 < 2e-3
- current_reversal_is_antisymmetric: PASS; value=0.0; threshold=max_abs_ratio < 1e-12
- rect_loop_superposition_is_exact: PASS; value=0.0; threshold=relative_l2 < 1e-12
- vertical_via_has_no_bz: PASS; value=0.0; threshold=Bz/Bxy < 1e-10
- standoff_reduces_field_strength: PASS; value=True; threshold=max |B| strictly decreases with h

## Key Metrics

- finite wire vs infinite-wire central relative L2: `9.053e-04`
- current reversal max-abs ratio: `0.000e+00`
- loop superposition relative L2: `0.000e+00`
- via Bz/Bxy max ratio: `0.000e+00`

## Boundary

This is a free-space, centerline-current sanity test. It intentionally does not
claim finite-width, ground-plane, QDM, FEM, or multilayer inverse validity.

## Agent Audit Metadata

- Metrics file: `outputs/metrics.json`
- Schema version: `research-ssot-metrics-v1`
- Calibration source: No calibration rows used for threshold or model selection.
- Threshold source: none
- Model-selection source: not_applicable
- Audit date: 2026-05-04
