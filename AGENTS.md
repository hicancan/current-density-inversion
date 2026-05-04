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

- Default to CPU for scripts, data processing, fitting, and evidence runs.
- Only target GPU when the task is explicitly: deep learning, CUDA/PyTorch
  acceleration, large matrix computation, or GPU-enabled simulation/rendering.
- Do not assume GPU is faster by default.
- GPU tasks use the WSL `quantum-dev` conda environment; entrypoint:
  `wsl -d Ubuntu -- bash -lc 'source ~/conda/etc/profile.d/conda.sh && conda activate quantum-dev && python <script.py>'`
- Never hard-code CUDA; GPU must remain optional with CPU fallback.

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
