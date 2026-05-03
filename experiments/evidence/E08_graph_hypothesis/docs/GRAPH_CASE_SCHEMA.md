# Exp08 Lightweight Graph Case Schema

This schema is the bridge between future layout importers and the exp08 graph
scorer. It is intentionally smaller than Gerber/GDS/ODB++: upstream code can
parse a real layout later and emit this graph/candidate representation.

## Required Top-Level Fields

```json
{
  "case_id": "example_case",
  "split": "external",
  "class_label": "true_via",
  "hypothesis_label": "H1_sheet_via",
  "b_obs": [[[0.0, 0.0, 0.0]]],
  "sheet_segments": [],
  "via_candidates": [],
  "return_candidates": [],
  "artifact_candidates": [],
  "truth_currents": {},
  "metadata": {}
}
```

`b_obs` must have shape `(H, W, 3)` and contain `Bx, By, Bz` in SI units.
`b_clean` is optional; if omitted, exp08 uses `b_obs` as the clean reference.

## Segment Fields

Each segment is a directed current basis:

```json
{
  "name": "edge_1",
  "layer": "L1",
  "kind": "edge",
  "prior_group": "sheet",
  "start": [-0.0003, 0.0, -0.00005],
  "end": [0.0003, 0.0, -0.00005]
}
```

Supported `prior_group` values in the current scorer:

- `sheet`
- `via`
- `return`
- `artifact`

The current implementation scores four hypotheses:

- `H0_sheet_only`: `sheet`
- `H1_sheet_via`: `sheet + via`
- `H2_sheet_return`: `sheet + return`
- `H3_sheet_artifact`: `sheet + artifact`

## Boundary

This schema is not a real CAD parser. It is the contract that a future
Gerber/GDS/ODB++ parser should target. A real layout import stage must still
handle pads, nets, ports, return planes, layer stack-up, copper width/thickness,
and candidate via constraints.
