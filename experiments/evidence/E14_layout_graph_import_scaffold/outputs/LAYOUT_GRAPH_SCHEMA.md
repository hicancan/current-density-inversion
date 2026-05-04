# LAYOUT_GRAPH_SCHEMA.md - E14 Layout Graph Import Schema

## Layout Schema (input, simplified JSON/YAML)

```yaml
schema: layout-graph-import-v1
description: string
stackup:
  - layer: string (name)
    z_top_um: number (top Z coordinate in microns)
    z_bottom_um: number (bottom Z coordinate in microns)
    material: string
    conductivity_sm: number (S/m)
layers:
  - name: string
    type: signal|plane
    thickness_um: number
nets:
  - name: string
    voltage: number|null
ports:
  - name: string
    layer: string (layer name reference)
    position_mm: [x, y]
    net: string (net name reference)
    role: source|sink|load|passive
traces:
  - name: string
    layer: string
    points_mm: [[x1,y1], [x2,y2], ...]
    width_um: number
    net: string
vias:
  - name: string
    from_layer: string
    to_layer: string
    position_mm: [x, y]
    net: string
return_planes:
  - name: string
    layer: string
    net: string
    outline_mm: [[x1,y1], [x2,y2], ...]
```

## Output Graph Representation

### Node Kinds

| Kind | Description | Attributes |
|---|---|---|
| port | Input/output port (source, sink, load) | layer, net, position_mm, role |
| junction | Trace segment endpoint/corner | layer, net, position_mm |
| via | Layer-transition via | from_layer, to_layer, position_mm, net |
| layer | Abstract layer node | depth_um, thickness_um, type |
| return_plane | Return plane anchor | layer, net |

### Edge Kinds

| Kind | Description | Attributes |
|---|---|---|
| trace | Conductive trace segment | layer, width_um, length_mm, net, resistance_proxy |
| via_edge | Via-to-layer connection | net |
| return_candidate | Candidate return path | net |
| layer_link | Node-to-layer membership | - |

### Hypothesis Candidates

| Label | Description |
|---|---|
| H0_nominal | Layout graph as-is |
| H1_via_defect_or_extra_via | Via removed (if vias exist) or extra via added (if no vias) |
| H2_return_bottleneck | Return path resistance increased 10x |
| H3_bend_width_artifact | First trace edge width halved |

### KCL Proxy

A rough KCL residual is computed by treating each edge as having current
proportional to `1/resistance_proxy`. This is not a real circuit solve,
but a scaffold placeholder for the KCL residual gate.