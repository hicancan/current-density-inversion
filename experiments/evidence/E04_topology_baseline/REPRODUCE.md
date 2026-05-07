# exp04 Reproduce

Run from this directory.

CPU or Windows uv:

```powershell
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json
uv run --with-requirements requirements.txt --with pytest pytest -q
```

Windows GPU (cu128):

```powershell
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
uv run python src/run_all.py --config configs/default.json
```

Expected key outputs:

- `outputs/metrics.json`
- `outputs/RUN_REPORT.md`
- `outputs/METRICS_TABLE.md`
- `outputs/CHANNEL_METRICS_TABLE.md`
- `outputs/STRESS_METRICS_TABLE.md`
- `outputs/OPERATOR_STRESS_TABLE.md`
- `outputs/VIA_DETECTOR_TABLE.md`
- `outputs/04_lambda_pareto.png`
- `outputs/predictions_test.npz`

Expected gate state:

```text
all_acceptance_gates_passed = true
```

The default run trains the primary no-topology/topology pair, runs a shortened
lambda sweep, and runs paired shortened multi-seed checks. Reduce
`analysis.lambda_sweep` or `analysis.multi_seed` only for local smoke tests, not
for a reportable run.

