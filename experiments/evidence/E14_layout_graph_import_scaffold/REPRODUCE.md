# REPRODUCE - E14 Layout Graph Import Scaffold

## Run

```
uv run python src/run_all.py
```

Outputs are written to `outputs/`.

## Test

```
uv run python -m pytest -q tests/
```

## Requirements

Standard library only (json, pathlib, math, copy).

## Config

Edit `configs/default.json` to adjust thresholds.
