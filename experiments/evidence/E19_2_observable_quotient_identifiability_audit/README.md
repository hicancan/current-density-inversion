# E19.2 Observable Quotient Current Inversion

This package implements **Observable Quotient Current Inversion (OQCI)** for
the current-density-inversion research graph.

## Scientific objective

E19.1 showed that winner-take-all Bayesian topology posterior selection
produces miscalibrated confidence (95% top probability vs 22% accuracy) and
H3_return_path systematically dominates all cases.

E19.2 changes the question from:

```
Which topology hypothesis wins under Bayesian evidence?
```

to:

```
Which topology claims are identifiable under this experiment family?
When should the algorithm report ambiguity instead of forcing a decision?
```

OQCI outputs:
1. The consistent set of hypotheses at noise level ε
2. Claim intervals [0,0], [0,1], [1,1] for each topology claim
3. Pairwise distinguishability distances between hypotheses
4. Near-null modes (current patterns invisible to the sensor)
5. Resolution operator diagnostics
6. Whether to accept, reject, or request a next measurement
7. Which next measurement would most reduce ambiguity

## Hypotheses

| ID | Meaning |
|---|---|
| H0_no_via | No cross-layer via explanation |
| H1_via | Candidate via/source-sink topology explanation |
| H2_model_gap | Registration/standoff/PSF model-gap explanation |
| H3_return_path | Return-loop or unmodeled return-path explanation |

## Commands

```bash
cd experiments/evidence/E19_2_observable_quotient_identifiability_audit

# Smoke test (fast)
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke

# Full run
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs

# Multi-height comparison
uv run --with-requirements requirements.txt python src/run_all.py --config configs/multi_height.json --out outputs_multi

# Tests
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
```

## Cannot claim

- Real QDM/NV validation
- Real CAD/Gerber/GDS validation
- External FEM/FastHenry/COMSOL validation
- Universal via detection
- Real-board PDN robustness
- Mechanism-level explanation on real data
- That generated-domain ambiguity holds for all real hardware
