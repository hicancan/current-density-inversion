# Active Port Design Audit

## Boundary Control

- States: `6`
- Pair count: `28`
- Min delta: `1.002764534e-11`
- Min Gamma without nuisance: `-0.06399999999`
- Interpretation: even before nuisance subtraction, ordinary boundary diagonal
  ports do not reach the noise-plus-threshold budget for this local via-open
  family.

## Perimeter Boundary Upper Bound

- States: `87`
- Pair count: `28`
- Min delta: `7.771493398e-11`
- Min Gamma without nuisance: `-0.06399999992`
- Interpretation: even a top/bottom perimeter-node basis, treated
  optimistically without nuisance subtraction, does not create enough central
  via-open contrast.

## Dual Schur Design

- States: `8`
- Pair count: `28`
- Min delta: `0.2095795941`
- Min Gamma after nuisance: `0.1348041937`
- Interpretation: Schur-aligned endpoint excitation crosses the robust margin
  threshold for every candidate pair in this generated-domain family.

## Critical Current

- Dual critical amplitude: `16.09623992`
- Boundary optimistic critical amplitude: `3.191177882e+11`
- Perimeter boundary optimistic critical amplitude: `4.117612711e+10`
