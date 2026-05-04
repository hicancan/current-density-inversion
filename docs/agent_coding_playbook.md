# Agent Coding Playbook

This repository is claim-centered. Start from the research graph, not from a
favorite script.

## Required Loop

1. Read `AGENTS.md`.
2. Read `research_graph/claims.yml`, `nodes.yml`, `experiments.yml`, and
   `evidence_edges.yml`.
3. Identify the affected claim and all involved data, physics, forward,
   observation, representation, algorithm, protocol, and metric nodes.
4. Inspect the linked evidence package with:

```powershell
uv run python scripts/audit_claim.py <claim-id>
uv run python scripts/audit_evidence_package.py <evidence-id>
uv run python scripts/prepare_agent_context.py --claim <claim-id>
```

5. Run the package test/smoke/full command through `scripts/run_evidence.py`.
6. Update metrics, RUN_REPORT, evidence edges, claim boundaries, open questions,
   guardrails, and `research_graph/update_log.md`.
7. Run the audit suite:

```powershell
uv run python scripts/validate_graph.py
uv run python scripts/check_claim_gates.py
uv run python scripts/check_metrics_schema.py
uv run python scripts/check_no_leakage.py
uv run python scripts/check_evidence_outputs.py
uv run python scripts/audit_old_new_experiment_coverage.py
uv run python -m pytest -q
```

## Status Rules

- `passed`: full run or equivalent stages completed and gates pass.
- `passed_interface`: interface/scaffold gates pass, but no real validation is
  implied.
- `partial`: useful evidence exists but a full run or gate is missing.
- `blocked`: external data, solver, license, or measured rows are missing.
- `supported_generated`: generated-domain support only and must include
  `cannot_claim` plus limitations.

Do not tune thresholds on hidden, held-out, external, real, or PyPEEC stress
rows unless the protocol explicitly marks them as calibration rows.
