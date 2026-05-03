# Data Directory

Use this directory for generated, external, and real-data artifacts only when a
claim-scoped evidence loop requires them.

Expected subdirectories:

- `generated/` for reproducible generated cases;
- `external/` for external solver exports;
- `raw/` for measured raw data that should not be modified in place.

Large arrays are ignored by default. Register their evidence role in
`research_graph/experiments.yml` before relying on them for a claim.

