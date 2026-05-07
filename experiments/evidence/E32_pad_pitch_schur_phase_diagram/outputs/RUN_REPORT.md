# E32 RUN REPORT - Pad-Pitch Schur Phase Diagram

Generated: 2026-05-06T16:10:10.496289+00:00

E32 is generated-domain reachability evidence. It proves pad-set active-mode
limits for the E31 graph family; it is not magnetic finite-difference evidence
and not real CAD/GDS, external-solver, QDM/NV, or real chip validation.

## Status

- Status: `passed`
- Engineering gates passed: `True`
- Scientific gates passed: `True`
- All acceptance gates passed: `True`
- Metrics file: `outputs/metrics.json`

## Main Result

- Candidate defects: `8`
- Candidate exact top-pad min reachability: `0.4767196129`
- Top full-surface min reachability: `0.4767196129`
- Top+bottom candidate min reachability: `0.9534392258`
- Perimeter min reachability: `2.48821324e-09`
- Stride-2 worst min reachability: `0.0003372396621`
- Stride-5+ worst min reachability: `4.754241203e-10`
- Candidate/stride-2 worst current multiplier: `1413.592962`
- Candidate/stride-5+ worst current multiplier: `1002724920`

## Acceptance Gates

| gate | passed |
|---|---:|
| package_runs_to_completion | True |
| e31_theorem_operator_reused | True |
| candidate_defects_generated | True |
| phase_diagram_has_rows | True |
| regular_grid_offsets_enumerated | True |
| local_patch_designs_enumerated | True |
| reports_written | True |
| generated_domain_boundary_explicit | True |
| no_external_or_real_data_used | True |
| candidate_exact_reachability_floor_ge_configured_gate | True |
| top_full_surface_does_not_beat_candidate_exact_floor | True |
| top_bottom_candidate_floor_ge_configured_gate | True |
| perimeter_floor_le_1e_minus_6 | True |
| stride2_worst_floor_le_sparse_failure_gate | True |
| stride5plus_worst_floor_le_1e_minus_6 | True |

## Cannot Claim

- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL validation
- real chip reverse analysis
- a fresh magnetic Gamma certificate beyond E31
- that sparse grid failure holds for all possible real layouts or defect families
- that candidate-projection pads are physically available on a real chip
- contact resistance, package parasitic, frequency-dependent, or finite-width robustness
- arbitrary current recovery outside the configured central via-open candidate set

## Next Required Evidence

- Run the E31 finite-difference magnetic Gamma certificate only on the E32-selected physically plausible local pad designs.
- Add explicit contact resistance, voltage/current driver limits, and package return impedance to the pad model.
- Repeat the pad-pitch phase diagram over non-central and broader generated layout families.
- Move the same reachability audit to CAD/GDS-derived graph candidates and independent solver rows.
- Only after real simple-wire and known-via sanity gates, evaluate QDM/NV measured rows.
