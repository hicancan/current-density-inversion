# RUN_REPORT - E13 Multi-Height Multi-State Observability

Claims: `C02_single_plane_identifiability_boundary`, `C06_graph_hypothesis_system_identification`.

This run generated two-layer route/via/return current distributions and evaluated
observability metrics across multi-height, multi-state, multi-component, and
graph-prior configurations. All results are generated-domain evidence.

## Metrics Summary

- Case count: 40
- Configurations evaluated: 27
- All acceptance gates passed: **True**

## Observability Table

See `OBSERVABILITY_TABLE.md`.

## Identifiability Gain Table

See `IDENTIFIABILITY_GAIN_TABLE.md`.

## Boundary

This is generated-domain observability evidence. It cannot claim:
- Arbitrary real multilayer recovery
- Real QDM/NV validation
- Real CAD/Gerber/GDS validation
- External FEM/FastHenry validation
- Hardware-feasible active measurement
- Generated-domain improvement transfers to real measurement

## Agent Audit Metadata

- Metrics file: `outputs/metrics.json`
- Schema version: `research-ssot-metrics-v1`
- Calibration source: No calibration rows used for threshold or model selection.
- Threshold source: none
- Model-selection source: not_applicable
- Audit date: 2026-05-04
