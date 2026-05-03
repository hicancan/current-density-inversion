# exp03 Reproduce

Run from this directory:

```powershell
$env:PYTHONPATH='src'
uv run --with-requirements requirements.txt python src/experiments/run_all.py --config configs/default.json
uv run --with-requirements requirements.txt --with pytest pytest -q
```

Expected key outputs:

- `outputs/metrics.json`
- `outputs/RUN_REPORT.md`
- `outputs/08_benchmark_dataset_examples.png`
- `data/two_layer_via_benchmark.npz`

Expected gate state:

```text
all_acceptance_gates_passed = true
```
