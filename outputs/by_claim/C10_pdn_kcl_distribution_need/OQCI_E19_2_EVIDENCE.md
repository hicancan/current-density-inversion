# E19.2 OQCI Identifiability Audit Evidence

**Evidence package:** E19_2_observable_quotient_identifiability_audit
**Status:** passed (engineering gates), failed (scientific gates)
**Date:** 2026-05-05

## Summary

OQCI (Observable Quotient Current Inversion) changes the question from
"Which topology hypothesis wins?" to "Which topology claims are identifiable
under this experiment family?"

## Key Results

| Metric | Single-height (3.2um) |
|---|---|
| Cases | 72 |
| Consistent set non-empty rate | 1.00 |
| Ambiguity rate | 1.00 |
| Effective rank | 27 / 100 |
| Near-null modes | 50 |
| Ridge top1 accuracy | 33.3% |

All 72 cases have all 4 hypotheses (H0/H1/H2/H3) consistent at noise-level epsilon.
None of the topology claims are forced true or forced false by the data alone.

## Pairwise Distinguishability

| Pair | Full distance | Extra distance | Distinguishable? |
|---|---|---|---|
| H0 vs H1 | 0.00 | 3.28 | Yes |
| H0 vs H2 | 0.00 | 4.52 | Yes |
| H0 vs H3 | 0.00 | 2.04 | Yes |
| H1 vs H2 | 0.00 | 0.00 | **No** |
| H1 vs H3 | 0.00 | 0.00 | **No** |
| H2 vs H3 | 0.00 | 0.00 | **No** |

H1, H2, H3 share a subspace even beyond H0. Standard OLS residuals cannot
distinguish via from gap from return-path explanations.

## Interpretation

Under single-height ideal Biot-Savart magnetic observation, the H0/H1/H2/H3
topology claims are not identifiable. The evidence supports C02 (identifiability
boundary) and limits C10 and C06.

## Cannot Claim

- Real QDM/NV validation
- Real CAD/Gerber/GDS validation
- External FEM/FastHenry/COMSOL validation
- Universal via detection
- Real-board PDN robustness
