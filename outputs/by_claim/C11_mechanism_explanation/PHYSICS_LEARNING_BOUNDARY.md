# Physics Learning Boundary

Claim: `C11_mechanism_level_explanation`

Evidence: `E12_pdn_physics_learning`

## Boundary Result

E12 improves generated-domain predicted-current KCL and current closure over an
unconstrained edge-current learner, but it does not add mechanism labels,
parameter-level audits, accepted-hidden audits, or real layout mechanisms.

Therefore E12 limits C11: it reinforces that physics consistency and label
accuracy must be reported separately from mechanism-level explanation.

## Cannot Claim

- accepted rows are mechanism-correct;
- primary-label correctness is sufficient explanation;
- KCL/current-closure consistency proves the diagnosed mechanism;
- generated E11 learning transfers to real CAD/GDS or real QDM/NV data.

## Next Required Evidence

Add mechanism labels and parameter-level audits for accepted generated and
hidden rows, then repeat the audit on externally solved or measured rows.

