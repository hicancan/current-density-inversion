# exp06 Reproduce

From this experiment directory:

```bash
uv run --with-requirements requirements.txt python src/run_all.py
uv run --with-requirements requirements.txt --with pytest pytest -q
```

Expected status:

```text
all_acceptance_gates_passed = true
```

The run writes `outputs/metrics.json`, `outputs/RUN_REPORT.md`, fidelity-ladder
plots, and `data/exp06_multifidelity_examples.npz`.
