# Failure Modes

- The positive certificate uses generated-domain centerline Biot-Savart and KCL
  graph physics inherited from E28.
- Dual Schur excitation injects current at the candidate via endpoints. This is
  an observability upper bound and is not automatically pad-feasible.
- The default candidate set is central via-open defects only. It does not prove
  via-short, return-path, dense-cluster, H1/H2 model-gap, or arbitrary current
  recovery.
- Nuisance is limited to E28-style height jitter and gain variation. Finite
  conductor width, registration, inductive/frequency effects, and external
  solver gaps remain open.
- A positive generated-domain pairwise Gamma does not imply real chip reverse
  analysis before CAD/GDS-derived graphs, external-solver transfer matrices,
  and real QDM/NV sanity gates exist.

