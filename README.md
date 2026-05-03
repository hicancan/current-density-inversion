# Magnetic System Identification SSOT

This repository is organized around a claim-centered research graph for
multilayer current-density inversion and magnetic system identification.

The source of truth is not an experiment number or a run log. The source of
truth is the graph under `research_graph/`:

- `claims.yml` records what is proposed, active, supported, limited, blocked,
  or retired.
- `nodes.yml` defines data distributions, physics constraints, solvers,
  observation models, representations, algorithms, protocols, and metrics.
- `experiments.yml` records evidence packages and planned evidence loops.
- `evidence_edges.yml` links evidence packages to claims with explicit scope,
  strength, and caveats.
- `open_questions.md` and `overclaim_guardrails.md` define what still cannot be
  claimed.

The research stance is deliberately conservative:

- generated, synthetic, and PyPEEC-domain results are never described as real
  QDM/NV/CAD validation;
- random split results never support strong generalization claims;
- hidden, held-out, external, or real rows are never used for tuning unless the
  protocol marks them as calibration rows;
- failure modes are preserved as claim boundaries and next required evidence.

## Repository Layout

```text
research_graph/      Claim graph SSOT and update log.
experiments/claims/  Claim-scoped experiment plans and evidence loops.
experiments/evidence/ Claim-graph evidence packages with runnable code.
outputs/by_claim/    Claim-scoped human-readable evidence summaries.
docs/protocols/      No-leakage and real-data validation protocols.
src/research_ssot/   Lightweight graph loader, validator, and renderers.
scripts/             CLI entry points for graph validation and reporting.
tests/               Integrity tests for the SSOT.
```

## Quick Start

```powershell
uv sync
uv run python scripts/validate_graph.py
uv run python scripts/render_claim_matrix.py
uv run python scripts/check_evidence_outputs.py
uv run python scripts/run_evidence.py --all --mode test --continue-on-fail
uv run pytest -q
```

## Working Rule

Before adding code or running a study, identify the affected claim and the
data, physics, forward, observation, representation, algorithm, protocol, and
metric nodes involved. If no claim exists, write a proposed claim first.

Every completed study must produce:

- machine-readable metrics where applicable;
- a human-readable output table or report;
- evidence edges that support, limit, contradict, require, or motivate claims;
- a claim-boundary update when failures or limitations appear.
