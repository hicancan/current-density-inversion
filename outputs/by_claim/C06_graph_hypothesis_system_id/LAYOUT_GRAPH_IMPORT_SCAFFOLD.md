# LAYOUT_GRAPH_IMPORT_SCAFFOLD.md - E14 supporting C06

Claim: `C06_graph_hypothesis_system_identification`.

## Evidence

`E14_layout_graph_import_scaffold` implements a CAD/Gerber/GDS-like layout graph
import scaffold. Simplified JSON/YAML layout schemas are parsed into:

- Route graph (nodes: ports, junctions, vias, loads, layer nodes)
- Via candidate graph (edges: traces, vias, return candidates)
- Layer stack metadata
- Net/port graph with return candidates
- H0/H1/H2/H3 hypothesis candidates generated from the graph

## Metrics

- Schema validates all examples: True
- Graph extraction preserves layers: True
- Via candidates extracted: True
- Return candidates extracted: True
- KCL graph export available: True
- Hypothesis candidates generated: True

## Boundary

This is a generated scaffold. It does NOT validate:
- Real CAD/Gerber/GDS import
- Real QDM/NV graph inference
- External solver validation

## Relation

- Supports C06: demonstrates graph extraction pipeline from layout-like schema
- Limits C06: only a scaffold, not real CAD import
