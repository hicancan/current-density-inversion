## Claim Graph

- Affected claim(s):
- Evidence package(s):
- Claim status change:
- Cannot claim:

## Evidence

- Full run command(s):
- Test/smoke command(s):
- Metrics file(s):
- RUN_REPORT file(s):
- Failure modes or blockers:

## Checks

- [ ] `uv run python scripts/validate_graph.py`
- [ ] `uv run python scripts/check_claim_gates.py`
- [ ] `uv run python scripts/check_metrics_schema.py`
- [ ] `uv run python scripts/check_no_leakage.py`
- [ ] `uv run python scripts/check_evidence_outputs.py`
- [ ] `uv run python scripts/audit_old_new_experiment_coverage.py`
- [ ] `uv run pytest -q`

## Boundary

Generated, synthetic, and PyPEEC-domain results are not real QDM/NV/CAD/FEM/FastHenry validation.

