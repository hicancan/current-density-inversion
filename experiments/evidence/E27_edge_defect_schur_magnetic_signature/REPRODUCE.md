# E27 Reproduction

## Prerequisites

- Python 3.11+
- `uv` package manager

## Quick smoke test

```powershell
cd experiments/evidence/E27_edge_defect_schur_magnetic_signature
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
```

## Full run

```powershell
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## Tests

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
```

## Dependencies

- numpy >= 1.24
- scipy >= 1.10
