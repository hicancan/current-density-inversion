# Reproduce E11

Default smoke/run command:

```powershell
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs --data data
```

Package tests:

```powershell
uv run --with-requirements requirements.txt --with pytest pytest -q tests
```

Repository integration:

```powershell
uv run python scripts/run_evidence.py E11_chip_like_pdn_distribution --mode smoke
uv run python scripts/check_evidence_outputs.py
uv run python scripts/validate_graph.py
```

The run is CPU-only and deterministic. GPU is not used because this evidence is
graph generation plus linear solves, not deep learning or large matrix training.

