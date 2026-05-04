# E19 OBGHI Minimal Observable Topology Posterior

This package is a smallest runnable evidence slice for **Observable Bayesian
Graph-Hodge Inversion (OBGHI)** in the current-density-inversion research graph.

It is designed to be copied to:

```text
experiments/evidence/E19_obghi_minimal_observable_topology_posterior/
```

## Scientific objective

E18 showed that hard physics-constrained inverse optimization can drive KCL
residuals very low while still failing on via detection, dense-via recall,
deep-layer allocation, and return-grid ambiguity.

E19 changes the question from:

```text
Which current map minimizes a penalty objective?
```

to:

```text
Which topology hypothesis has observable Bayesian support, and when should the
algorithm reject rather than make an over-confident topology claim?
```

## Hypotheses

The minimal OBGHI evidence package compares four topology/explanation families:

| ID | Meaning |
|---|---|
| `H0_no_via` | No cross-layer via explanation; graph-only current modes. |
| `H1_via` | Candidate vertical via/source-sink topology explanation. |
| `H2_model_gap` | Registration/standoff/PSF-like model-gap explanation in observation space. |
| `H3_return_path` | Return-loop or unmodeled return-path explanation. |

## What is implemented

- A deterministic generated four-layer sheet/via forward operator.
- Generated cases with known topology labels.
- Graph-Hodge-inspired low-dimensional current bases.
- Observable compression through singular-value/Fisher-energy filtering.
- Closed-form Gaussian Bayesian evidence for each topology.
- Posterior topology probabilities.
- Via-vs-gap principal-angle ambiguity diagnostic.
- Accept/reject/need-next-measurement decision rule.
- Ridge-map baseline for comparison.
- Machine-readable `metrics.json`.
- Human-readable `RUN_REPORT.md`, `POSTERIOR_TABLE.md`,
  `FAILURE_CASES.md`, and `ACCEPTANCE_GATES.md`.
- Pytest smoke tests for package integrity.

## Commands

```bash
cd experiments/evidence/E19_obghi_minimal_observable_topology_posterior
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
```

For a faster first check:

```bash
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
```

## Research-graph status

This ZIP intentionally does **not** mutate `research_graph/*.yml`.
After local execution, inspect the outputs and then apply the snippets in:

```text
research_graph_patch/E19_research_graph_snippets.md
```

Only apply them after the run is audited.

## Cannot claim

- Real QDM/NV validation.
- Real CAD/Gerber/GDS validation.
- External FEM/FastHenry/COMSOL validation.
- Real-board PDN/KCL robustness.
- Mechanism-level explanation on real data.
- Universal via detection.
- That blueprint text alone supports or upgrades a claim.
