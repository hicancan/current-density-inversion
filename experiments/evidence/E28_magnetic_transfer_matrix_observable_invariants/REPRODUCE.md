# E28 Reproduce

```bash
cd experiments/evidence/E28_magnetic_transfer_matrix_observable_invariants
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
```
