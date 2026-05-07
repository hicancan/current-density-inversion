# Agent Operating Rules

This repository is governed by a claim-centered Research Graph SSOT.

Before code work:

1. Read `research_graph/claims.yml`.
2. Read `research_graph/nodes.yml`.
3. Read `research_graph/experiments.yml`.
4. Read `research_graph/evidence_edges.yml`.
5. Read `research_graph/open_questions.md`.
6. Read `research_graph/overclaim_guardrails.md`.
7. Identify the affected claim.
8. Identify the involved data, physics, forward, observation, representation,
   algorithm, protocol, and metric nodes.

Rules:

- Do not open a study unless it is linked to a specific claim or unless the
  first output is a proposed new claim.
- Do not use held-out, hidden, external, or real data to tune thresholds,
  evidence weights, or model selection unless the protocol explicitly marks
  those rows as calibration data.
- Generated, synthetic, and PyPEEC-domain results cannot be described as real
  QDM/NV/CAD validation.
- Primary-label correctness cannot be described as mechanism-level
  explanation.
- PyPEEC cannot be described as ground-truth real physics.
- Failed studies must update claim boundaries, limitations, or open questions.

After code work:

1. Update `experiments.yml` with evidence metadata.
2. Update `evidence_edges.yml` with graph relations.
3. Update `claims.yml` if the claim status changes.
4. Update `open_questions.md` if limitations appear.
5. Update `overclaim_guardrails.md` if a new overclaim risk appears.
6. Update `update_log.md`.
7. Run `uv run python scripts/validate_graph.py` and tests where possible.

Agent-native audit commands:

- `uv run python scripts/audit_claim.py <claim-id>`
- `uv run python scripts/audit_evidence_package.py <evidence-id>`
- `uv run python scripts/prepare_agent_context.py --claim <claim-id>`
- `uv run python scripts/check_claim_gates.py`
- `uv run python scripts/check_metrics_schema.py`
- `uv run python scripts/check_no_leakage.py`
- `uv run python scripts/audit_old_new_experiment_coverage.py`
- `uv run python scripts/normalize_metrics_metadata.py` after full evidence
  runs that rewrite package metrics files

## Compute policy

- Select compute by the task itself. Use GPU when the workload is naturally
  GPU-accelerated and expected to be materially faster on GPU; otherwise use
  CPU.
- Prefer GPU for deep learning training/inference, CUDA/PyTorch/JAX/CuPy
  workloads, large dense or sparse matrix decompositions/solves, large batched
  forward/operator evaluations, and GPU-enabled simulation/rendering.
- Prefer CPU for small deterministic scripts, file/data plumbing, config work,
  graph bookkeeping, light fitting, short tests, and workloads where data
  transfer overhead likely dominates.
- If uncertain, run or design a small benchmark/scale estimate before choosing
  the expensive path. Do not assume GPU is faster by default.
- GPU tasks use Windows-native `uv` with the cu128 PyTorch index:
  `uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128`
- Never hard-code CUDA; GPU must remain optional with CPU fallback.
- CuPy/JAX GPU backends install via `uv pip install` in the project venv as needed.

## Core algorithm blueprint pool

External high-level algorithm blueprints live under:

- `docs/algorithm_blueprints/`

These documents are design inputs, not evidence. They do not support or upgrade
claims by themselves.

When a task asks for novel algorithmic progress, especially E18 or later
physics-constrained inversion work, read:

1. `docs/algorithm_blueprints/README.md`
2. the relevant phase document.

Current priority order:

1. Phase 1 OBGHI core algorithm
2. Phase 2 R-MF-CTAS only after OBGHI has runnable evidence
3. Phase 3 Q-R-MF-CTAS only when real/multi-height/NV observation data or
   observation-design work is available
4. Phase 4 EV-FAEDA only for industrial FA/EDA integration planning

Rules:

- Do not treat blueprint text as experimental evidence.
- Do not update claim status from blueprint text alone.
- Implement the smallest runnable algorithmic slice first.
- If blueprint theory conflicts with evidence metrics, evidence metrics win.
- Any implemented blueprint work must become a normal evidence package with
  metrics, RUN_REPORT, failure modes, cannot_claim, and research graph updates.

## Test entrypoint

- `uv run python -m pytest -q` (cross-platform); avoid bare `uv run pytest -q`.

---

Full run evidence must be recorded as full run only when the package
`run_command` or all equivalent stage commands completed. Test/smoke runs may
verify code paths, but must not be written as full-run evidence.

Final audit response must include:

- Claim affected
- Evidence added
- Metrics
- Failure modes
- Claim status change
- Cannot claim
- Next required evidence
- Tests run
- Files changed
