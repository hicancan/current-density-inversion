# E28 Failure Modes (Run-Specific)

## Observed Failure Modes

**Raw negative Gamma**: H1_via__H2_model_gap.
**Projector negative Gamma**: H0_no_via__H1_via, H0_no_via__H2_model_gap, H0_no_via__H3_return_path, H1_via__H2_model_gap, H1_via__H3_return_path, H2_model_gap__H3_return_path. Projector margin is negative for all pairs because projector epsilon 2.80 dominates projector deltas in units of [0, sqrt(k)].
**Gram negative Gamma**: H1_via__H2_model_gap. Typically H1_vs_H2 (very close hypotheses).
**Differential negative Gamma**: H1_via__H2_model_gap.
**H1/H2 unresolved by design**: the current certificate merges H1_via and H2_model_gap into one observable quotient class. This prevents a full four-hypothesis separability claim.
**High ambiguity**: 66.67% of cases have multiple consistent hypotheses.

## Gate Failures

All gates passed.