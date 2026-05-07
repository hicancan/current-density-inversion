# E23 H1/H2 Breakthrough Audit

## Degeneracy Status Across Rounds

| Round | Protocol | H1/H2 Distance | Wrong Accepts |
|-------|----------|---------------|---------------|
| R1 | 1s1h | ~0.007 | 2 |
| R2 | 3-height | ~0.007 | 2 |
| R3 | multi-state | 0.154270 | 0 |
| R3 | ms+mh | 0.154233 | 0 |

## Did Multi-State Break the Degeneracy?
- NO: multi-state did not break the H1/H2 degeneracy
- Via and return perturbations produce nearly identical B-fields
  even under stacked multi-state + multi-height observations.
- This is a stronger identifiability boundary:
  centerline Biot-Savart forward + resistive KCL graph
  fundamentally cannot distinguish via from return topology
  with the current hypothesis perturbation model.

## Next Steps
- If breakthrough: validate with external solver (COMSOL/FastHenry)
- If no breakthrough: consider finite-width forward (F03),
  different hypothesis perturbation models, or real CAD/GDS
  topologies where via and return paths differ in geometry, not
  just in edge-type labels.