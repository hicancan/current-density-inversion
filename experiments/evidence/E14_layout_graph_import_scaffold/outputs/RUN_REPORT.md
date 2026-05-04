# RUN_REPORT - E14 Layout Graph Import Scaffold

Claims: `C06_graph_hypothesis_system_identification`, `C10_pdn_kcl_distribution_need`.

This run implements a CAD/Gerber/GDS-like layout graph importer scaffold.
It converts simplified JSON/YAML layout schemas into route graph, via
candidate graph, layer stack, net/port graph, and return candidates.
It also generates H0/H1/H2/H3 hypothesis candidates from the extracted graph.

## Metrics

# Layout Graph Import Metrics Table

| Metric | Value | Gate |
|---|---|---|
| schema validates all examples | True | True |
| graph extraction preserves layers | True | True |
| via candidates extracted | True | True |
| return candidates extracted | True | True |
| KCL graph export available | True | True |
| hypothesis candidates generated | True | True |
| no real CAD claim | True | True |
| all acceptance gates passed | True | True |

## Per-Example Summary

| Example | Nodes | Edges | Vias | Return Edges | Layers | Connected | Schema |
|---|---|---|---|---|---|---|---|
| four_layer_pdn_like_layout | 27 | 36 | 4 | 3 | 4 | True | True |
| no_via_hard_negative_layout | 11 | 15 | 0 | 1 | 2 | False | True |
| return_bottleneck_layout | 15 | 19 | 1 | 3 | 3 | False | True |
| simple_two_layer_layout | 10 | 13 | 1 | 2 | 2 | True | True |

Disconnected examples (no_via_hard_negative_layout, return_bottleneck_layout) are
intentional stress cases, not parser failures. The disconnected graph reflects
the physical topology of a signal trace on one layer with a separate return plane
on another, without bridging vias -- this is the deliberate "hard negative" and
"return bottleneck" design.

## Hypothesis Candidates Generated

For each example, the following candidates are generated:
- H0_nominal: layout graph as-is
- H1_via_defect_or_extra_via: one via removed or extra via added
- H2_return_bottleneck: return path weakened
- H3_bend_width_artifact: trace width halved

## Boundary

This is a generated scaffold only. It does not validate real CAD/Gerber/GDS
imports, real QDM/NV measurements, external FEM/FastHenry solves, or real
layout-derived hypothesis diagnosis. The layout schema is simplified and
the example layouts are hand-authored for scaffold verification.

## Agent Audit Metadata

- Metrics file: `outputs/metrics.json`
- Schema version: `research-ssot-metrics-v1`
- Calibration source: No calibration rows used.
- Threshold source: none
- Model-selection source: not_applicable
- Audit date: 2026-05-04
