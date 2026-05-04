# Open Questions

## OQ01: Can the system-identification framework survive PDN/KCL-constrained circuit-graph distributions?

Status: active, generated chip-like and physics-learning closure passed.

`E10_pdn_kcl_distribution` now implements the first generated resistive
PDN/KCL graph prototype with VDD, GND, load, vias, junctions, return paths,
edge resistance, KCL, current closure, and magnetic forward fields. The open
`E11_chip_like_pdn_distribution` expands this into a generated four-layer
chip-like micro-PDN with top straps, intermediate meshes, lower return grid,
via stacks, distributed loads, balanced H0/H1/H2/H3 rows, and passing KCL,
closure, and divB gates. `E12_pdn_physics_learning` shows generated-domain
physics-learning closure: held-out label learning is above majority baseline
and physics-aware graph/KCL projection improves predicted-current KCL and
current closure over unconstrained current regression. The open question is now
whether this survives imported CAD/Gerber/GDS-like graph families, broader
return networks, inductive/frequency effects, and independent external-solver
held-out rows.

## OQ02: Can few-shot family calibration be made realistic?

Status: high priority.

The calibration source must be explicit: calibration coupon, known-good H0,
known-via H1, known-return H2, known-artifact H3, simulated family calibration,
real reference region, or simple-wire known structure.

## OQ03: Can accepted hidden cases be explained at mechanism level?

Status: high priority.

Primary-label correctness is not enough. Accepted rows must eventually be
audited for wrong-layer via, shifted via, corner shadow, finite-width nuisance,
return overlap, and unexplained mechanisms.

## OQ04: Can unlabeled family adaptation reduce calibration-label requirements?

Status: medium priority, E11/E12 provide a generated family-hidden target.

Candidate methods include feature normalization, pseudo-labels, cluster
alignment, high-confidence self-training, distance-manifold adaptation, and
conformal calibration.

`E12_pdn_physics_learning` is supervised generated-domain learning. It does not
answer OQ04, but the E11 family-hidden split now provides a concrete dataset
target for a future unlabeled adaptation loop.

## OQ05: Can external solvers validate generated and PyPEEC-domain conclusions?

Status: high priority.

Required evidence includes COMSOL, FastHenry, Ansys, or an equivalent trusted
solver on a small but auditable subset.

## OQ06: Can real QDM/NV data pass simple-wire and known-via sanity gates?

Status: blocked until data.

`E09_real_data_intake_gate` now passes the interface scaffold: metadata
validation, component order, units, background protocol, NPZ loader,
background subtraction, component plotting, and simple-wire sanity stub are
callable and machine-checked. No measured rows are present. No real via/no-via
diagnosis can be claimed before units, coordinate frame, standoff, background
subtraction, polarity, and simple-wire sanity pass on measured data.
