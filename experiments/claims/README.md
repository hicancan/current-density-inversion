# Claim-Scoped Experiment Plans

Each directory under this folder is owned by a claim. A study can write code,
metrics, or reports under a claim directory only after it maps the evidence loop
to the graph nodes in `research_graph/`.

## Claim Plan Format

Each claim plan should answer:

- affected claim;
- data nodes;
- physics nodes;
- forward solver nodes;
- observation nodes;
- representation nodes;
- algorithm nodes;
- protocol nodes;
- metric nodes;
- evidence outputs;
- failure modes to preserve;
- cannot-claim boundary;
- next required evidence.

