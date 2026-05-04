# LAYOUT_GRAPH_IMPORT_SCAFFOLD.md - E14 supporting C10

Claim: `C10_pdn_kcl_distribution_need`.

## Evidence

`E14_layout_graph_import_scaffold` extracts PDN-relevant graph features from
simplified JSON/YAML layout schemas:

- Layer stack with depths and material conductivity
- Net/port graph with source, sink, and load roles
- Via candidates and return candidate edges
- KCL proxy residual for rough current conservation check
- Hypothesis candidates (H0 nominal, H1 via defect, H2 return bottleneck, H3 bend/width artifact)

## Metrics

- Example layouts: 4 (simple two-layer, four-layer PDN-like, no-via hard negative, return bottleneck)
- Total layers found: 4
- All examples generate all 4 hypothesis candidates
- KCL proxy values computed for all graphs

## Boundary

This is a generated scaffold. It does NOT validate:
- Real CAD/Gerber/GDS PDN import
- External FEM/FastHenry validation
- Real QDM/NV measurements
- Real PDN/KCL robustness
- The KCL proxy is not a real circuit solve

## Relation

- Supports C10: provides layout-derived graph with return candidates and KCL proxy
- Limits C10: scaffold only, not real CAD/Gerber/GDS or external solver validation
