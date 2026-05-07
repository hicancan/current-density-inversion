# E21 External-Solver Operator-Gap Ladder

Quantifies field-level and decision-level operator gaps across the solver ladder:
analytic reference, centerline Biot-Savart, finite-width surrogate, PyPEEC (if
available), and optional COMSOL/FastHenry external artifact ingestion.

## Quick Start

```powershell
# Smoke run
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke

# Default run
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs

# Tests
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
```

## Package Structure

- `configs/` — smoke and default JSON configs
- `src/` — implementation modules
- `tests/` — unit and integration tests
- `outputs/` — generated reports and metrics
- `external_artifacts/` — COMSOL/FastHenry artifact placeholder
- `research_graph_patch/` — proposed SSOT patches (do not write directly)
