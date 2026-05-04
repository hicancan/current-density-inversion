# Reproducing E18

## Prerequisites

- Python 3.10+
- uv package manager

## Full Run

```bash
uv run --with-requirements experiments/evidence/E18_physics_constrained_pdn_inverse/requirements.txt \
  python experiments/evidence/E18_physics_constrained_pdn_inverse/src/run_all.py \
  --config experiments/evidence/E18_physics_constrained_pdn_inverse/configs/default.json \
  --out experiments/evidence/E18_physics_constrained_pdn_inverse/outputs
```

## Tests

```bash
uv run --with-requirements experiments/evidence/E18_physics_constrained_pdn_inverse/requirements.txt \
  --with pytest python -m pytest -q \
  experiments/evidence/E18_physics_constrained_pdn_inverse/tests
```

## Expected Outputs

- `outputs/metrics.json` - Full metrics with acceptance gates
- `outputs/UNIFIED_LEADERBOARD.md` - Ranked method comparison
- `outputs/WIN_LOSS_BY_METRIC.md` - Per-metric win/loss table
- `outputs/FAMILY_BREAKDOWN.md` - Per-family metrics
- `outputs/FAILURE_CASES.md` - Identified failure modes
- `outputs/ALGORITHM_NOTES.md` - Algorithm details
- `outputs/RUN_REPORT.md` - Full run report

## Runtime

Expected: 30-120 seconds on a modern CPU (depends on L-BFGS-B convergence).
