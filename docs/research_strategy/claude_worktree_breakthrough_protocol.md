# Claude Worktree Breakthrough Protocol

Date: 2026-05-06

Status: operating protocol for future agent orchestration, not evidence.

This document records the preferred breakthrough workflow for this repository.
The scientific theme remains:

```text
magnetic field measurements -> current distribution / current mechanism inference
```

The protocol separates top-level scientific design from implementation.

## Non-Negotiable Execution Rule

Every Claude Code worker invocation must include:

```powershell
--effort max
```

Examples:

```powershell
claude --effort max -p --worktree e20-active-oqci "..."
claude --effort max -p --worktree e21-external-solver "..."
claude --effort max -p --verbose --output-format stream-json --include-partial-messages --worktree e22-real-qdm-gate "..."
```

Do not launch breakthrough workers with lower effort levels.

## Role Separation

Codex role:

- act as top-level mathematician, physicist, and algorithm architect;
- decide the scientific claim, mathematical target, physics assumptions,
  algorithm blueprint, metrics, and cannot-claim boundaries;
- write detailed design documents before implementation begins;
- launch Claude Code workers in isolated worktrees;
- audit worker outputs, diffs, reports, metrics, and tests;
- decide the next loop based on evidence and failure modes;
- integrate only audited results back into the main worktree.

Claude Code worker role:

- implement the assigned design in its own worktree;
- run package tests, smoke runs, or full evidence commands as instructed;
- preserve failure modes;
- return changed files, commands, metrics, failure modes, cannot-claim, and
  next required evidence;
- never upgrade claim status without explicit Codex review.

Codex should not directly implement breakthrough packages when the work can be
delegated to Claude Code workers. Codex should design, delegate, audit, and
iterate.

## Design-First Requirement

Before any Claude worker starts implementation, Codex must create or update a
detailed markdown design document in a suitable location, normally:

```text
docs/algorithm_blueprints/
docs/research_strategy/
experiments/evidence/<EID>/DESIGN.md
```

The design document must include:

- affected claim;
- involved data, physics, forward, observation, representation, algorithm,
  protocol, and metric nodes;
- first-principles motivation;
- mathematical formulation;
- algorithm steps;
- file/package structure;
- metrics and gates;
- expected failure modes;
- cannot-claim boundaries;
- test/smoke/full-run commands;
- required report artifacts;
- exact scope boundaries for the Claude worker.

Blueprint or strategy text is not evidence. It becomes evidence only after an
evidence package is implemented, run, audited, and registered in the research
graph.

## Parallelism Policy

Codex may run up to three top-level Claude worktree workers in parallel by
default. Use more only after the current three are audited and their merge risks
are understood.

Recommended three-way breakthrough split:

1. Active OQCI measurement design:
   `E20_active_oqci_measurement_design`
2. External-solver operator-gap ladder:
   `E21_external_solver_operator_gap_ladder`
3. Real QDM/NV or CAD/GDS grounding gate:
   `E22_real_qdm_nv_sanity_gate` or `E23_cad_gds_graph_hodge_basis`

Each worker must own a disjoint write scope. Research graph SSOT files should
normally be edited only by Codex after auditing worker outputs, or workers
should write proposed graph snippets under their evidence package.

## Worker Prompt Contract

Every worker prompt should include this contract:

```text
You are working in an isolated Claude Code worktree.
Use --effort max for this session.
Read AGENTS.md first.
Read research_graph/claims.yml, nodes.yml, experiments.yml,
evidence_edges.yml, open_questions.md, and overclaim_guardrails.md.
Follow the linked design document exactly.
Do not modify unrelated files.
Do not upgrade claim status.
Do not call generated, synthetic, or PyPEEC-domain results real QDM/NV,
real CAD/GDS, or external-solver validation.
Preserve failed studies and document limitations.
At the end, report:
- files changed;
- commands run;
- metrics;
- failure modes;
- claim status change, usually none;
- cannot_claim;
- next required evidence;
- any proposed research_graph snippets.
```

## Compute Policy for Workers

Claude workers should choose compute based on the workload, not habit.

- Use GPU when the task is naturally GPU-accelerated and expected to be
  materially faster: deep learning, CUDA/PyTorch/JAX/CuPy, large dense/sparse
  matrix decompositions or solves, large batched forward/operator evaluations,
  and GPU-enabled simulation/rendering.
- Use CPU for small deterministic scripts, file/data plumbing, graph metadata,
  lightweight fitting, short tests, and runs where data-transfer overhead
  likely dominates.
- If uncertain, run a small benchmark or estimate problem size first.
- GPU tasks use Windows-native `uv` with the cu128 PyTorch index:
  `uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128`
- CuPy/JAX GPU backends install via `uv pip install` in the project venv.
- Never hard-code CUDA; keep CPU fallback available and report which compute
  path was used.

## Worktree Commands

Important CLI rule:

```text
Use --worktree with a short worktree name, not an absolute path.
Keep the name ASCII and below the CLI limit, preferably under 40 characters.
```

Correct:

```powershell
claude --effort max -p --worktree e20-active-oqci --add-dir D:\code\github\hicancan\current-density-inversion\docs\algorithm_blueprints --output-format json "<task prompt>"
```

Incorrect:

```powershell
claude --effort max -p --worktree D:\code\github\hicancan\current-density-inversion\.claude\worktrees\e20-active-oqci "<task prompt>"
```

Interactive worker:

```powershell
claude --effort max --worktree e20-active-oqci
```

Non-interactive worker with JSON result:

```powershell
claude --effort max -p --worktree e20-active-oqci --output-format json "<task prompt>"
```

Streaming worker:

```powershell
claude --effort max -p --worktree e20-active-oqci --verbose --output-format stream-json --include-partial-messages "<task prompt>"
```

Resume worker:

```powershell
claude --effort max -p --resume <session_id> "<next audit or continuation prompt>"
```

## Audit Loop

After each worker finishes, Codex audits:

1. `git status --short`
2. `git diff`
3. changed files against the assigned scope
4. metrics and reports
5. failure-mode honesty
6. cannot-claim boundaries
7. required commands:

```powershell
uv run python scripts/validate_graph.py
uv run python -m pytest -q
```

For evidence packages, also run relevant package test/smoke/full commands and:

```powershell
uv run python scripts/check_claim_gates.py
uv run python scripts/check_metrics_schema.py
uv run python scripts/check_no_leakage.py
uv run python scripts/check_evidence_outputs.py
```

Codex then decides one of:

- continue same worker with a narrower correction prompt;
- launch a new worker on the next independent slice;
- integrate the worker result manually after audit;
- reject the worker result and preserve the failure as limitation or open
  question where appropriate.

## Breakthrough Targeting Rule

Every worker task must be tied to at least one first-principles breakthrough
lever:

1. observation information content;
2. admissible current space and physical prior;
3. forward/sensor/noise/model-gap realism;
4. identifiable current-claim target;
5. statistical certification and refusal;
6. scalable computation;
7. active next-measurement policy;
8. validation and transfer ladder.

If a proposed task does not change any of these levers, it is not a top-level
breakthrough task and should be deferred or reframed.

## Overclaim Boundaries

Claude worker output is not evidence until Codex audits it and the evidence
package is registered in the research graph.

Do not claim:

- worker success is scientific validation;
- strategy or blueprint text is evidence;
- generated-domain performance proves real QDM/NV or real CAD/GDS validation;
- PyPEEC is ground-truth real physics;
- a high-confidence topology posterior is mechanism-level correctness;
- a failed worker result should be hidden.
