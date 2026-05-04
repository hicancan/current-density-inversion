# Chip-Like PDN Evidence

Claim: `C10_pdn_kcl_distribution_need`

Evidence: `E11_chip_like_pdn_distribution`

## What Was Added

E11 adds a generated four-layer chip-like micro-PDN distribution with:

- top power straps;
- two intermediate mesh layers;
- lower return grid;
- via stacks;
- distributed loads;
- VDD/GND boundary ports;
- edge resistance;
- solved KCL edge currents;
- current closure;
- centerline Biot-Savart `Bxyz` fields;
- H0/H1/H2/H3 generated hypothesis rows.

## Metrics

- case count: 96
- family count: 4
- layer count: 4
- node count range: 35 to 37
- edge count range: 65 to 68
- max KCL residual: `4.913e-15`
- max current closure error: `7.391e-15`
- max divB proxy residual: `2.835e-03`
- held-out hypothesis accuracy: `1.000`
- family-hidden hypothesis accuracy: `1.000`
- all acceptance gates passed: `true`

## Failure Modes Covered

- disconnected or floating generated graph nodes;
- missing explicit return path;
- KCL residual above tolerance;
- VDD/GND current closure mismatch;
- divB proxy inconsistency;
- H0/H1/H2/H3 imbalance;
- generated hypothesis scoring failure on held-out rows.

## Claim Boundary

This strengthens generated-domain support for C10. It does not validate real
chip PDNs, real CAD/Gerber/GDS imports, external FEM/FastHenry solves,
frequency-dependent PDN behavior, or real QDM/NV measurements.

Next required evidence: import CAD/Gerber/GDS-like graph families and validate a
small subset against an independent external solver.

