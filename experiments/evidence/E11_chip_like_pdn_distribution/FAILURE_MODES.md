# E11 Failure Modes

- Floating interior node or disconnected generated graph.
- Missing explicit return path from load-side current back to GND.
- KCL residual above numerical tolerance.
- Source current and sink current fail current-closure tolerance.
- `divB` proxy residual exceeds the generated-domain sanity threshold.
- H0/H1/H2/H3 rows are imbalanced or missing in held-out family slices.
- Matched generated hypothesis scorer fails on held-out generated rows.
- Results are overclaimed as real chip, real CAD/GDS, external solver, or real
  QDM/NV validation.

