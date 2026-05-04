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
- `artifacts.yml` registers metrics, reports, and other evidence artifacts.
- `agent_queue.yml` records machine-readable next work items for Codex/agent
  execution.
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
docs/agent_workflow.md Agent-facing workflow for claim-safe research work.
src/research_ssot/   Lightweight graph loader, validator, and renderers.
scripts/             CLI entry points for graph validation and reporting.
tests/               Integrity tests for the SSOT.
```

## Quick Start

```powershell
uv sync
uv run python scripts/validate_graph.py
uv run python scripts/check_claim_gates.py
uv run python scripts/check_metrics_schema.py
uv run python scripts/check_no_leakage.py
uv run python scripts/render_claim_matrix.py
uv run python scripts/agent_next.py
uv run python scripts/check_evidence_outputs.py
uv run python scripts/audit_old_new_experiment_coverage.py
uv run python scripts/validate_agent_readiness.py
uv run python scripts/agent_audit.py
uv run python scripts/run_evidence.py E11_chip_like_pdn_distribution --mode smoke
uv run python scripts/run_evidence.py E12_pdn_physics_learning --mode smoke
uv run python scripts/run_evidence.py --all --mode test --continue-on-fail
uv run python -m pytest -q
```

Agent-native claim inspection:

```powershell
uv run python scripts/audit_claim.py C10_pdn_kcl_distribution_need
uv run python scripts/audit_evidence_package.py E08_graph_hypothesis_system_id
uv run python scripts/prepare_agent_context.py --claim C12_real_qdm_nv_validation
```

`scripts/run_evidence.py --all --mode smoke` is a runtime sanity sweep only.
It is not full-run evidence. Full-run status is recorded in
`outputs/full_run_audit.md` and in each evidence `outputs/RUN_REPORT.md`.
After a full run, run `uv run python scripts/normalize_metrics_metadata.py`
before the metrics/no-leakage audit because legacy evidence scripts rewrite
their own `metrics.json` files.

## Agent Loop

```powershell
uv run python scripts/validate_graph.py
uv run python scripts/agent_next.py
uv run python scripts/scaffold_evidence.py --claim <claim-id> --evidence <evidence-id>
uv run python scripts/run_evidence.py <evidence-id> --mode smoke
uv run python scripts/check_evidence_outputs.py
uv run python scripts/agent_audit.py
```

Current generated PDN loop:

```powershell
uv run python scripts/run_evidence.py E11_chip_like_pdn_distribution --mode smoke
uv run python scripts/run_evidence.py E12_pdn_physics_learning --mode smoke
```

E11/E12 are generated-domain only. They improve the PDN/KCL and learning
closure evidence, but they do not validate real chip layouts, external solvers,
or real QDM/NV measurements.

## Working Rule

Before adding code or running a study, identify the affected claim and the
data, physics, forward, observation, representation, algorithm, protocol, and
metric nodes involved. If no claim exists, write a proposed claim first.

Every completed study must produce:

- machine-readable metrics where applicable;
- a human-readable output table or report;
- evidence edges that support, limit, contradict, require, or motivate claims;
- a claim-boundary update when failures or limitations appear.
