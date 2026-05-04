# Full Run Audit

This file records required command execution for the current repository audit.
It distinguishes tests, smoke runs, preserved artifacts, fresh full runs,
partial evidence, blocked evidence, and interface-only scaffolds.

## Status After 2026-05-04 Final Command Sweep

| Evidence | Current status | Full-run interpretation |
|---|---|---|
| E01 | passed | Fresh full run completed in the all-evidence run command. |
| E02 | passed | Fresh full run completed in the all-evidence run command. |
| E03 | passed | Fresh full run completed in the all-evidence run command. |
| E04 | passed | Fresh full topology baseline/retraining/diagnostic command completed; claim boundaries still limit real/ mechanism claims. |
| E05 | passed | Fresh full run completed in the all-evidence run command. |
| E06 | passed | Fresh full run completed in the all-evidence run command. |
| E07 | passed | Fresh real PyPEEC API full run completed, including the 400-case target and exp03-like mini dataset. |
| E08 | passed | Fresh full graph-hypothesis/system-id command completed; C11 remains limited. |
| E09 | passed_interface | Interface scaffold gates pass; no measured real rows and no real validation claim. |
| E10 | passed | Fresh generated PDN/KCL prototype run completed. |
| E11 | passed | Fresh generated chip-like PDN run completed. |
| E12 | passed | Fresh generated PDN physics-learning run completed. |
| E13 | passed | Fresh full run completed; generated-domain multi-height/multi-state observability sweep across 27 configurations. |
| E14 | passed_scaffold | Fresh scaffold run completed; layout graph import generates H0/H1/H2/H3 candidates from 4 example layouts. |
| E15 | passed | Fresh full run completed; 4-layer via-chain benchmark with 18 cases, 11-channel output, 4 baselines. |
| E16 | passed | Fresh full run completed; FFT-domain differentiable Biot-Savart forward passes all 6 acceptance gates. |
| E17 | passed | Fresh full run completed; 144 runs across 4 regularized baselines x 3 noise x 2 standoff x 6 conditions. |

## Command Log (2026-05-04 Integration Sweep)

| Command | Result | Key output / consequence |
|---|---|---|
| `uv sync` | PASS | Dependency sync completed. |
| `uv run python scripts/validate_graph.py` | PASS after edge fixes | Graph validation finished with 0 error(s), 0 warning(s). |
| `uv run python scripts/check_claim_gates.py` | PASS after edge fixes | Claim gate check passed. |
| `uv run python scripts/check_metrics_schema.py` | FAIL after full run, then PASS after normalization | Full evidence scripts rewrote metrics and removed audit metadata; `scripts/normalize_metrics_metadata.py --date 2026-05-04` restored schema/no-leakage/RUN_REPORT metadata for 12 metrics files. |
| `uv run python scripts/check_no_leakage.py` | FAIL after full run, then PASS after normalization | Same metadata overwrite; final no-leakage check passed for 12 metrics files. |
| `uv run python scripts/check_evidence_outputs.py` | PASS | 12 metrics files checked; all registered gates true. |
| `uv run python scripts/audit_old_new_experiment_coverage.py` | PASS | Wrote `outputs/migration_coverage_matrix.md`. |
| `uv run pytest -q` | FAIL | Local Windows `uv` trampoline error: `uv trampoline failed to canonicalize script path`; this was not a pytest failure. |
| `uv run python -m pytest -q` | PASS | 11 repository tests passed. |
| `uv run python scripts/run_evidence.py --all --mode test --continue-on-fail` | PASS | E01-E12 package tests passed. |
| `uv run python scripts/run_evidence.py --all --mode smoke --continue-on-fail` | PASS | Smoke/runtime sweep completed in 715.6 s. |
| `uv run python scripts/run_evidence.py --all --mode run --continue-on-fail` | PASS | Full evidence sweep completed in 1703.9 s; E07 executed the real PyPEEC 400-case solver bridge. |
| `uv run python scripts/normalize_metrics_metadata.py --date 2026-05-04` | PASS | Restored `schema_version`, `leakage_audit`, and RUN_REPORT metrics references after full run. |
| `uv run python scripts/run_evidence.py --all --mode test --continue-on-fail` (2026-05-04) | PASS | All 17 evidence packages (E01-E17) test suites passed. |
| `uv run python scripts/run_evidence.py --all --mode smoke --continue-on-fail` (2026-05-04) | TIMEOUT (600s) | Smoke sweep progressing but timed out at E07 PyPEEC solver; test mode completed for all 17. |

## Cannot Claim From This Sweep

- Real QDM/NV validation; E09 has no measured rows.
- Real CAD/Gerber/GDS validation; E14 is a generated scaffold only.
- COMSOL/FastHenry/FEM validation; no independent external solver rows exist.
- PyPEEC as real ground truth; E07 is a generated-domain solver bridge.
- Mechanism-level explanation from primary-label or graph-label correctness; C11 remains limited.
- Multi-height/multi-state observability proves real multilayer recovery; E13 is generated-domain only.
- Layout graph import scaffold replaces CAD-derived graph candidates; E14 is scaffold only.
- Four-layer via-chain benchmark proves real hardware sensitivity; E15 is generated benchmark only.
- Differentiable forward layer validates against external solvers; E16 is generated-domain forward only.
- L1-curl/div-free baselines transfer to real measurements; E17 is generated-domain evaluation only.
- Generated-domain physics-aware graph/KCL projection proves real learned physics under imported layouts.
