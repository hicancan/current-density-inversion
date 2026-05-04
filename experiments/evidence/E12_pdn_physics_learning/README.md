# E12 PDN Physics Learning

Claim: `C10_pdn_kcl_distribution_need`.

This package asks whether generated E11 chip-like PDN data can support a
learning-oriented physics closure: `Bxyz`-derived hypothesis learning plus
predicted-current checks for KCL, current closure, and field reconstruction.

It trains CPU baselines:

- residual/hypothesis scorer baseline;
- graph-agnostic learner from `Bxyz` features to H0/H1/H2/H3 labels;
- physics-aware learner that predicts a hypothesis and derives currents through
  the E11 graph/KCL projection instead of unconstrained edge-current regression.

This evidence is generated-domain only. It cannot claim real chip validation,
real CAD/Gerber/GDS validation, external solver validation, real QDM/NV
validation, or mechanism-level explanation.

