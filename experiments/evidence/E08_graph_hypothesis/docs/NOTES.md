# Notes

Exp08 intentionally keeps the first implementation linear and interpretable:

- each graph segment is a basis current;
- each hypothesis chooses a different basis library;
- ridge fitting estimates currents;
- score = normalized forward residual + complexity + extra-basis L1;
- H1/H0 score difference is used as via evidence.

The design is deliberately not a neural network. The point is to test whether the task representation should move from pixel regression to graph-level system identification.

Future extensions:

1. Replace synthetic graph generator with CAD/Gerber/GDS import.
2. Replace centerline basis with PyPEEC/FastHenry/FEM basis export.
3. Add multi-state current excitation.
4. Add Bayesian model evidence or AIC/BIC-style penalties.
5. Add GNN or differentiable graph optimizer after the physics-only baseline is established.

Current P0-P3 status:

- P0 is implemented as an exp07 metadata-to-graph bridge. It is intentionally
  approximate and shows a large centerline-to-PyPEEC performance drop.
- P1 is implemented as hidden-mechanism OOD stress. These cases are designed to
  fail when the hypothesis library is incomplete.
- P2 is implemented as `docs/GRAPH_CASE_SCHEMA.md` plus a JSON importer smoke
  test. This is an interface, not a Gerber parser.
- P3 is implemented as a synthetic two-state joint scorer. It is evidence that
  multi-state observations can help, not evidence that active hardware data is
  available.
