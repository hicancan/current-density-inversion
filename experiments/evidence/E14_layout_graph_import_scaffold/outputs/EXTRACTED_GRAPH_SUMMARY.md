# EXTRACTED_GRAPH_SUMMARY.md - E14 Layout Graph Import Scaffold

## Overview

Processed 4 layout examples.
Total distinct layers found across all examples: 6.

## Per-Example Graph Extraction

### four_layer_pdn_like_layout

- Description: Four-layer PDN-like layout: two signal layers, power plane, ground plane, with via stacks and multiple ports
- Nodes: 27 (layer=4, port=6, junction=12, via=4, return_plane=1)
- Edges: 36 (trace=6, via_edge=8, return_candidate=3, layer_link=19)
- Layers: ['BOT', 'SIG1', 'SIG2', 'TOP']
- Via nodes: 4
- Return candidate edges: 3
- Connected: True
- Schema validates: True
- Hypothesis candidates: H0_nominal, H1_via_defect_or_extra_via, H2_return_bottleneck, H3_bend_width_artifact
- KCL proxy max residual: 1.099e+02

### no_via_hard_negative_layout

- Description: No-via hard negative: single signal trace with source and load on same layer, no vias present
- Nodes: 11 (layer=2, port=2, junction=6, return_plane=1)
- Edges: 15 (trace=5, return_candidate=1, layer_link=9)
- Layers: ['BOT', 'TOP']
- Via nodes: 0
- Return candidate edges: 1
- Connected: False
- Schema validates: True
- Hypothesis candidates: H0_nominal, H1_via_defect_or_extra_via, H2_return_bottleneck, H3_bend_width_artifact
- KCL proxy max residual: 4.972e+01

### return_bottleneck_layout

- Description: Return bottleneck: VDD has wide straps but return ground path is narrow, creating return asymmetry
- Nodes: 15 (layer=3, port=4, junction=6, via=1, return_plane=1)
- Edges: 19 (trace=3, via_edge=2, return_candidate=3, layer_link=11)
- Layers: ['BOT', 'SIG1', 'TOP']
- Via nodes: 1
- Return candidate edges: 3
- Connected: False
- Schema validates: True
- Hypothesis candidates: H0_nominal, H1_via_defect_or_extra_via, H2_return_bottleneck, H3_bend_width_artifact
- KCL proxy max residual: 1.025e+02

### simple_two_layer_layout

- Description: Simple two-layer layout: M1 signal trace with via to M2 return plane
- Nodes: 10 (layer=2, port=2, junction=4, via=1, return_plane=1)
- Edges: 13 (trace=2, via_edge=2, return_candidate=2, layer_link=7)
- Layers: ['M1', 'M2']
- Via nodes: 1
- Return candidate edges: 2
- Connected: True
- Schema validates: True
- Hypothesis candidates: H0_nominal, H1_via_defect_or_extra_via, H2_return_bottleneck, H3_bend_width_artifact
- KCL proxy max residual: 4.160e+01

## Hypothesis Candidate Summary

All 4 examples generate the complete set of 4 hypothesis candidates:
- H0_nominal: nominal layout
- H1_via_defect_or_extra_via: via perturbation
- H2_return_bottleneck: return path weakened
- H3_bend_width_artifact: trace width artifact

## Boundary

Generated scaffold only. No real CAD/Gerber/GDS import, no real QDM/NV
validation, no external solver validation. The layout examples are
hand-authored simplified JSON schemas for scaffold verification.