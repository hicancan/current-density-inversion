# E19 Reproduction

## Prerequisites

- Python 3.10+
- `uv` package manager
- numpy, pytest

## Quick smoke test

```bash
cd experiments/evidence/E19_obghi_minimal_observable_topology_posterior
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
```

## Full run

```bash
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## Tests

```bash
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
```

## Expected outputs

- `outputs/metrics.json`
- `outputs/RUN_REPORT.md`
- `outputs/POSTERIOR_TABLE.md`
- `outputs/FAILURE_CASES.md`
- `outputs/ACCEPTANCE_GATES.md`

## Configuration

- `configs/default.json`: 12x12 grid, 4 layers, 72 cases (12 per family x 6 families)
- `configs/smoke.json`: 8x8 grid, 4 layers, 12 cases (3 per family x 4 families)
