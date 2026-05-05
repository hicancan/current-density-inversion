# E19.2 OQCI Identifiability Audit Evidence (Corrected)

**Evidence package:** E19_2_observable_quotient_identifiability_audit
**Status:** passed_with_limitations (engineering gates pass, scientific gates fail)
**Date:** 2026-05-05 (corrected)

## Summary

OQCI (Observable Quotient Current Inversion) is a *generated-domain admissible basis
family* identifiability audit. It does **not** constitute an absolute physical theorem
about all possible observation protocols.

## Key Results

| Metric | Single-height (3.2um) |
|---|---|
| Cases | 72 |
| all_acceptance_gates_passed | **False** (eng only) |
| Consistent set non-empty rate | 1.00 |
| Ambiguity rate | 1.00 |
| Effective rank | 27 / 100 |
| Near-null modes | 50 |

## Epsilon Sensitivity Sweep

| Multiplier | Epsilon | Nonempty | Ambiguous | Empty |
|---|---:|---:|---:|---:|
| 0.5 sigma | 0.187 | 0.00 | 0.00 | 1.00 |
| 1.0 sigma | 0.374 | 0.85 | 0.71 | 0.15 |
| 1.5 sigma | 0.561 | 1.00 | 1.00 | 0.00 |
| 2.0 sigma | 0.748 | 1.00 | 1.00 | 0.00 |
| 2.5 sigma | 0.935 | 1.00 | 1.00 | 0.00 |
| 3.0 sigma | 1.122 | 1.00 | 1.00 | 0.00 |

**Interpretation:** At tight epsilon (0.5sigma) all consistent sets are empty — no
hypothesis fits within pure noise. At 1.0sigma, some discriminating power emerges
(~15% empty, ~71% ambiguous). At 1.5sigma+, all cases become fully ambiguous.
This transition zone demonstrates that the ambiguity is epsilon-dependent.

## Non-Degenerate Pairwise Distinguishability

Unit-energy principal angle distances are zero (all subspaces share H0 common
core). Claim-activated distances (min coefficient norm = 0.1 on hypothesis-specific
blocks):

| Pair | Claim-Activated Distance | Per-Case Fitted Mean |
|---|---|---:|
| H0 vs H1 | 0.000 (no specific blocks in H0) | 0.241 |
| H0 vs H2 | 0.000 (no specific blocks in H0) | 0.168 |
| H0 vs H3 | 0.000 (no specific blocks in H0) | 0.225 |
| H1 vs H2 | **0.014** | 0.222 |
| H1 vs H3 | **0.001** (near-zero) | 0.095 |
| H2 vs H3 | **0.017** | 0.211 |

H1_vs_H3 has the smallest claim-activated distance (0.001) and smallest per-case
fitted mean (0.095) — via and return-path fitted predictions are nearly identical.

## Scope & Limitations

This evidence is scoped to the generated-domain admissible basis family under
ideal free-space Biot-Savart forward. It does **not** prove an absolute physical
identifiability theorem. It demonstrates that under the **current** experiment
family and basis construction, H0/H1/H2/H3 topology claims are not forced by data.

## Cannot Claim

- Real QDM/NV validation
- Real CAD/Gerber/GDS validation
- External FEM/FastHenry/COMSOL validation
- Universal via detection
- Real-board PDN robustness
- An absolute physical identifiability theorem
