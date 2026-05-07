# E28 Magnetic Transfer-Matrix Observable Invariants

This package implements magnetic transfer-matrix observable invariants for
topology discrimination under forward-model nuisance.

## Scientific objective

Change the observation object from individual magnetic field images to the
**magnetic transfer matrix** induced by port excitations. Compute
nuisance-invariant representations of the transfer matrix and demonstrate
that invariant margins exceed raw field margins for critical topology pairs.

## Hypotheses

| ID | Meaning |
|---|---|
| H0_no_via | No cross-layer via conduction |
| H1_via | Candidate via/source-sink topology |
| H2_model_gap | Registration/standoff/PSF model-gap |
| H3_return_path | Return-loop or unmodeled return path |

## Invariant Representations

1. **Column-space projector** — invariant to invertible mixing and global scale
2. **Whitened Gram matrix** — cancels per-state amplitude scale
3. **Differential common-mode cancellation** — subtracts reference state

## Commands

```bash
cd experiments/evidence/E28_magnetic_transfer_matrix_observable_invariants

# Smoke test (fast)
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke

# Full run
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs

# Tests
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
```

## Cannot claim

- Real QDM/NV validation
- Real CAD/Gerber/GDS validation
- External FEM/FastHenry/COMSOL validation
- Universal via detection
- Real-board PDN robustness
- That invariants work for all real hardware
- That generated-domain margins hold for all observation protocols
