# Failure Modes - E20 Active OQCI (Round 3)

## Valid Disambiguation Utility <= 0

- add_state2_Bz: utility_valid=-0.300000
- add_h1.6_Bxyz: utility_valid=-0.500000
- add_h6.4_Bxyz: utility_valid=-0.500000
- add_h1.6_state2_Bz: utility_valid=-0.500000
- add_state2_Bxyz: utility_valid=-0.700000
- add_state4_Bz: utility_valid=-0.700000
- add_state4_Bxyz: utility_valid=-1.000000
- add_h1.6_state4_Bxyz: utility_valid=-1.500000

## Breakthrough Gates

- valid_disambiguation_rate_ge_0_50: **False**
- truth_in_consistent_set_rate_ge_0_90: **True**
- singleton_wrong_rate_eq_0: **True**
- empty_rate_le_0_10: **True**
- any_candidate_passes_all_four: **False**

## Best Coverage Pair

- candidate: add_h1.6_Bxyz @ epsilon_mult=1.5
- valid_disambiguation_rate: 0.0000
- singleton_correct: 0/18
- singleton_wrong: 0
- empty_rate: 0.0000
- truth_in_consistent_set_rate: 1.0000

## Cannot Claim Boundaries

- This evidence is generated-domain only
- No real QDM/NV, CAD/GDS, or external solver validation
- Multi-height/multi-state improvement does not transfer to real devices
- Hardware feasibility of active measurement is not assessed
- Empty-set discrimination is not treated as disambiguation

## Next Required Evidence

- Validate candidate recommendations on real QDM/NV multi-height data
- Cross-validate with external solver (COMSOL/FastHenry) held-out rows
- Test with imported CAD/GDS graph families
- If any candidate passes all 4 breakthrough gates, audit per-case at that epsilon
