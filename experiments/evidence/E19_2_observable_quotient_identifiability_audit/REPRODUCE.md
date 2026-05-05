# E19.2 Reproduce

```bash
cd experiments/evidence/E19_2_observable_quotient_identifiability_audit
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
uv run --with-requirements requirements.txt python src/run_all.py --config configs/multi_height.json --out outputs_multi
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
```
