# Reproducibility

Use `uv` for the repository-level environment.

```powershell
uv sync
```

Every evidence package must expose:

- `README.md`
- `REPRODUCE.md`
- `METRICS_SCHEMA.md`
- `FAILURE_MODES.md`
- `requirements.txt` or `pyproject.toml`
- `configs/default.json`
- `tests/`
- `outputs/metrics.json`
- `outputs/RUN_REPORT.md`

Run all package tests:

```powershell
uv run python scripts/run_evidence.py --all --mode test --continue-on-fail
```

Run smoke:

```powershell
uv run python scripts/run_evidence.py --all --mode smoke --continue-on-fail
```

Run full evidence commands:

```powershell
uv run python scripts/run_evidence.py --all --mode run --continue-on-fail
uv run python scripts/normalize_metrics_metadata.py --date 2026-05-04
```

CI is allowed to run tests and smoke-scale checks. A CI smoke pass is not a full
experiment pass. Full-run status must be recorded in `outputs/full_run_audit.md`
and the relevant evidence `outputs/RUN_REPORT.md`.

Real-data validation requires measured QDM/NV rows, metadata, calibration, and
simple-wire or known-structure sanity gates. E09 interface success is not real
validation.
