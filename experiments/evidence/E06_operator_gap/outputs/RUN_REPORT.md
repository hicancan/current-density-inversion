# exp06 Run Report

## Role

MVP-5 anti-inverse-crime and multi-fidelity validation. This experiment proves
that same-operator synthetic testing can be over-optimistic, and that a small
high-fidelity calibration set can close an operator-mismatch gap.

## Gate Summary

Overall: PASS

- same_operator_decoder_is_nearly_exact: PASS; value=6.752852958533825e-16; threshold=low-test relative L2 < 1e-10
- operator_mismatch_creates_visible_gap: PASS; value=0.19018385455618986; threshold=high-test relative L2 > 0.05
- calibration_reduces_high_fidelity_error: PASS; value=0.0011521496360987035; threshold=calibrated/high error ratio < 0.01
- high_operator_is_materially_different: PASS; value=0.20377775495190803; threshold=basis relative difference > 0.1
- fidelity_ladder_is_monotone: PASS; value=[6.752852958533825e-16, 0.01955411507516346, 0.19018385455618986]; threshold=low decoder error < medium decoder error < high decoder error
- medium_operator_gap_is_between_low_and_high: PASS; value=[0.015596892160326913, 0.20377775495190803]; threshold=0 < medium basis gap < high basis gap
- calibrated_error_is_small_enough_for_gate: PASS; value=0.0002191202588187629; threshold=calibrated high-test relative L2 < 0.01
- real_pypeec_bridge_artifact_is_valid: PASS; value={'enabled': True, 'artifact_available': True, 'exp07_all_gates_passed': True, 'n_cases_completed': 400}; threshold=exp07 real PyPEEC artifact exists, gates passed, and required cases completed
- real_pypeec_bridge_gap_is_material_and_bounded: PASS; value=0.1738886546065947; threshold=exp03-like PyPEEC shape gap is finite and between configured material/bounded limits

## Key Results

- low same-operator relative L2: `6.753e-16`
- medium surrogate relative L2 before calibration: `0.020`
- high surrogate relative L2 before calibration: `0.190`
- high surrogate relative L2 after 400 calibration samples: `2.191e-04`
- medium basis relative difference: `0.016`
- operator basis relative difference: `0.204`
- real PyPEEC exp03-like shape gap: `0.174`
- real PyPEEC bridge table: `outputs/PYPEEC_BRIDGE_TABLE.md`

## Boundary

The medium and high-fidelity operators are still surrogates, not
COMSOL/FastHenry/QDM data. The PyPEEC bridge imports a real-solver exp07 artifact
as a read-only fidelity level; it does not calibrate or train on PyPEEC samples.
Passing this gate only justifies moving to real multi-fidelity stress tests.

## Agent Audit Metadata

- Metrics file: `outputs/metrics.json`
- Schema version: `research-ssot-metrics-v1`
- Calibration source: No calibration rows used for threshold or model selection.
- Threshold source: none
- Model-selection source: not_applicable
- Audit date: 2026-05-04
