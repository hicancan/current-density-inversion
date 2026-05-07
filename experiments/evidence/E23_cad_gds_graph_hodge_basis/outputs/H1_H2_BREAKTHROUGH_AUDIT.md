# E23 H1/H2 Breakthrough Audit

## Degeneracy Status Across Rounds

| Round | Protocol | H1/H2 Distance | Wrong Accepts |
|-------|----------|---------------|---------------|
| R1 | 1s1h | ~0.007 | 2 |
| R2 | 3-height | ~0.007 | 2 |
| R3 | multi-state | 0.736487 | 2 |
| R3 | ms+mh | 0.710205 | 2 |

## Did Multi-State Break the Degeneracy?
- YES: multi-state + multi-height pushed H1/H2 distance >= 0.20
- This is the breakthrough signal: different excitation states
  stress graph topology differently, making via vs return
  perturbations distinguishable in B-field space.

## Next Steps
- If breakthrough: validate with external solver (COMSOL/FastHenry)
- If no breakthrough: consider finite-width forward (F03),
  different hypothesis perturbation models, or real CAD/GDS
  topologies where via and return paths differ in geometry, not
  just in edge-type labels.