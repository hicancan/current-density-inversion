# Reproduce E10

## Run

```powershell
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs --data data
```

## Smoke

```powershell
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs --data data
```

## Tests

```powershell
uv run --with-requirements requirements.txt --with pytest pytest -q tests
```

## Leakage Boundary

No thresholds are selected on held-out rows. The H0/H1/H2/H3 scorer compares
frozen candidate graph families with the same generated family parameters and
reports split roles explicitly.

