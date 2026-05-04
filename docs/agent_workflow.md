# Agent Workflow

This repository is an agent-first scientific operating system. A Codex/agent
should move through the graph rather than guessing the next experiment.

## Fixed Entry Sequence

1. Read `research_graph/claims.yml`, `nodes.yml`, `experiments.yml`,
   `evidence_edges.yml`, `open_questions.md`, and `overclaim_guardrails.md`.
2. Run `uv run python scripts/validate_graph.py`.
3. Run `uv run python scripts/agent_next.py` to identify the next claim-safe
   work item.
4. Identify affected claim, required nodes, metrics, cannot-claim boundaries,
   and tests before editing code.
5. After a study runs, update evidence metadata, evidence edges, artifacts,
   claim status or limitations, open questions, and update log as needed.
6. Run `uv run python scripts/check_evidence_outputs.py`,
   `uv run python scripts/validate_agent_readiness.py`, and relevant tests.

## Failure Handling

Failed studies are evidence. Do not hide them. If a gate fails, preserve the
metrics, update limitations or open questions, and avoid strengthening the
claim.

## Overclaim Boundary

Generated, synthetic, and PyPEEC-domain results cannot be described as real
CAD/Gerber/GDS, external FEM/FastHenry, or real QDM/NV validation unless those
nodes and protocols are explicitly present and passed.

