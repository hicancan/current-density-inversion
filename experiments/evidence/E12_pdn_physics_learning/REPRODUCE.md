# Reproduce E12

Run E11 first so the generated dataset exists:

```powershell
uv run python scripts/run_evidence.py E11_chip_like_pdn_distribution --mode smoke
```

Run E12:

```powershell
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

Package tests:

```powershell
uv run --with-requirements requirements.txt --with pytest pytest -q tests
```

Repository integration:

```powershell
uv run python scripts/run_evidence.py E12_pdn_physics_learning --mode smoke
uv run python scripts/check_evidence_outputs.py
uv run python scripts/validate_graph.py
```

GPU note: this smoke evidence uses closed-form CPU baselines. If a future run
scales to PyTorch training large enough to exceed reasonable CPU time, use the
WSL `quantum-dev` environment explicitly and record the command here.

