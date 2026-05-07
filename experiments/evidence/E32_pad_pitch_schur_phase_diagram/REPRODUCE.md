# Reproduce E32

From this package directory:

```powershell
uv run python src/run_all.py --config configs/default.json --out outputs
uv run python -m pytest -q tests
```

Repository-level checks:

```powershell
uv run python scripts/validate_graph.py
uv run python -m pytest -q
```
