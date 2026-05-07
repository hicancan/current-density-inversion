# E27 Edge-Defect Schur Magnetic Signature Inversion

Generated-domain evidence for edge-defect magnetic signature detectability using
Sherman-Morrison perturbation and Schur-optimal state design.

## Status

See `outputs/RUN_REPORT.md` after running.

## Quick start

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```
