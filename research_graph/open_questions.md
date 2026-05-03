# Open Questions

## OQ01: Can the system-identification framework survive PDN/KCL-constrained circuit-graph distributions?

Status: highest priority.

The current strongest missing data node is `D08_pdn_kcl_circuit_graph`. It must
include VDD, GND, load, vias, junctions, multilayer metal grids, return paths,
edge resistance, KCL, current closure, and optional KVL or resistive-network
consistency.

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

Status: medium priority.

Candidate methods include feature normalization, pseudo-labels, cluster
alignment, high-confidence self-training, distance-manifold adaptation, and
conformal calibration.

## OQ05: Can external solvers validate generated and PyPEEC-domain conclusions?

Status: high priority.

Required evidence includes COMSOL, FastHenry, Ansys, or an equivalent trusted
solver on a small but auditable subset.

## OQ06: Can real QDM/NV data pass simple-wire and known-via sanity gates?

Status: blocked until data.

No real via/no-via diagnosis can be claimed before units, coordinate frame,
standoff, background subtraction, polarity, and simple-wire sanity pass.

