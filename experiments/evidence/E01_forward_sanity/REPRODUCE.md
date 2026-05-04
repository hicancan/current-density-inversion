# Reproduce E01

## Run

```powershell
uv run --with-requirements requirements.txt python src/experiments/run_all.py --out outputs
```

## Tests

```powershell
uv run --with-requirements requirements.txt --with pytest pytest -q tests
```

## Determinism

This package uses deterministic canonical wire, loop, and via cases. Outputs
are generated-domain forward-sanity artifacts only.

