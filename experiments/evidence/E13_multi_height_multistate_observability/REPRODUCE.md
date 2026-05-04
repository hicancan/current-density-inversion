# Reproduce

```powershell
uv run python src/run_all.py --config configs/default.json --out outputs
```

Test:
```powershell
uv run --with pytest python -m pytest -q tests
```
