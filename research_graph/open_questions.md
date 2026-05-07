# Open Questions

## OQ07: Can the differentiable Biot-Savart forward layer be validated against independent external solvers?

Status: active, E16 numpy/torch forward passes generated-domain sanity gates.

`E16_differentiable_forward_layer` provides an FFT-domain differentiable
Biot-Savart forward with all 6 acceptance gates passing. The open question is
whether this forward agrees with COMSOL, FastHenry, or FEM on a small auditable
subset.

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

## OQ08: Can physics-constrained differentiable inverse overcome dense-via and deep-layer failure modes?

Status: active, E18 documents four failure modes.

`E18_physics_constrained_pdn_inverse` demonstrates KCL residual improvement
but identifies: (1) dense-via recall = 0 on cluster stress cases, (2) deep-layer
misallocation > 0.3, (3) return-grid ambiguity where new method has higher RMSE
than ridge, (4) aggregate KCL-RMSE tradeoff. Open question: can multi-height
observations (E13), improved via priors, or external-solver calibration
resolve these failure modes? Also: can the unified leaderboard be expanded
with Tikhonov/L1-curl baselines from E17 for complete comparison?

## OQ09: Can transfer-matrix Gram quotient certificates survive broader generated, external-solver, and real-calibrated nuisance?

Status: active, E28 provides first positive generated-domain quotient result.

`E28_magnetic_transfer_matrix_observable_invariants` shows that a whitened Gram
invariant of magnetic transfer matrices can certify the generated-domain
observable quotient Q0={H0_no_via}, Q12={H1_via,H2_model_gap}, Q3={H3_return_path}
with positive robust margins after noise, nuisance radius, and threshold
subtraction. The full run also finds a gain-only hard-case regime where raw
quotient margins fail but Gram quotient margins remain positive.

The E28 H1/H2 phase-diagram audit strengthens the boundary: across 32 controlled
H2 via-factor/sheet-jitter rows, no row has positive H1/H2 Gram Gamma under the
phase nuisance budget. The default row has Gamma -0.0948871365 and a budget gap
of 0.0948871365; it would need eps+rho <= 0.0028658462, while the observed
eps+rho is 0.0977529827. This argues against spending the next iteration on
default H1_via versus H2_model_gap splitting with the same observation/representation.

The E28 directional statistical certificate replaces full feature-space noise
ball subtraction with matched-filter directional noise/nuisance subtraction. It
tightens the generated-domain Gram quotient min Gamma from 0.4511206603 to
0.5323884196, but H1/H2 remains negative at -0.0560703448. This supports
directional Gamma as a sharper certificate for quotient decisions, while still
arguing that H1/H2 needs new physical information rather than only a tighter
statistical bound.

The open question is whether this survives (1) broader layout ensembles, (2)
external solver held-out transfer matrices, (3) real-calibrated gain/standoff/
registration nuisance, and (4) richer hypotheses that may separate H1_via from
H2_model_gap. E28 does not answer real-chip reverse analysis by itself.

## OQ10: Can dual-Schur local defect certificates become pad-feasible and survive real operator gaps?

Status: active, E30 provides a generated-domain local-access upper bound.

`E30_dual_schur_active_defect_certificate` shows that, for 8 generated central
via-open candidates, ordinary boundary diagonal ports remain below threshold
even without nuisance subtraction (min Gamma -0.06399999999), and an optimistic
top/bottom perimeter-boundary basis with 87 states also remains below threshold
(min Gamma -0.06399999992). Local dual Schur endpoint excitation yields positive
pairwise directional Gamma after noise, height/gain nuisance, and tau
subtraction (28/28 positive pairs; min Gamma 0.1348041937; truth pairwise
certified rate 1.0). The current-budget law reports dual critical amplitude
16.09623992 under the configured amplitude 50, whereas the boundary optimistic
critical amplitude is 3.191177882e11 and the perimeter-boundary optimistic
critical amplitude is 4.117612711e10.

The open question is whether this observability upper bound can be converted
into deployable evidence: pad-accessible active ports, broader/non-central
defect families, finite-width and registration rho, external-solver transfer
matrices, CAD/GDS-derived graph candidates, and eventually real QDM/NV sanity
gates. E30 does not prove real chip reverse analysis.

`E31_pad_schur_reachability_certificate` resolves the first generated-domain
version of the pad-feasibility question for the E30 central via-open family.
It proves the exact reachability ratio
`eta_e(P)=osc_P(L^+ d_e)/(d_e^T L^+ d_e)`, finds perimeter pads essentially
uncontrollable (min ratio 2.48821324e-09), and finds top candidate-projection
surface pads plus a reference pad reachable enough (min ratio 0.4767196129).
The theorem-selected pad pairs give 28/28 positive finite-difference magnetic
Gamma certificates after directional noise and height/gain nuisance
subtraction, with min Gamma 0.01963293336 and critical amplitude 38.26243887
under configured amplitude 50.

The open question is now narrower and more physical: can candidate-projection
surface pads be made realistic under pad pitch, current limits, contact
resistance, package parasitics, broader layouts, external-solver rho, and real
QDM/NV sanity gates? E31 still does not prove real chip reverse analysis.

`E32_pad_pitch_schur_phase_diagram` resolves the first generated-domain
pad-pitch version of that question for the same central via-open family. The
exact Schur reachability phase diagram shows candidate-projection top pads keep
min reachability 0.4767196129, top+bottom candidate pads reach 0.9534392258,
and perimeter pads remain near-null at 2.48821324e-09. Sparse regular-grid
offsets can collapse the same Schur mode by orders of magnitude: stride-2
worst min reachability is 3.37239662e-04, and stride-5+ worst min reachability
is 4.75424120e-10.

This sharpens the open question rather than closing it. The next physical
breakthrough must add contact resistance, voltage/current driver limits,
package return impedance, broader/non-central layout families, external-solver
rho, and eventually real QDM/NV sanity-gated rows. E32 does not add a fresh
magnetic Gamma certificate beyond E31 and does not prove real chip reverse
analysis.

## OQ11: Can certified observable current-subspace inversion replace unsupported full current maps?

Status: active, E33 provides a generated-domain Fourier/thin-sheet certificate.

`E33_certified_observable_current_subspace_inversion` reframes strict
current-density inversion as recovery of the Fisher-stable projection
`Pi_obs J` plus refusal of dark modes `(I-Pi_obs)J`. In the generated
Fourier/stream-function thin-sheet model, the Fisher eigenvalue of a current
mode is `lambda_i=phi_i^T A^T Sigma^-1 A phi_i`, with diagonal law
`lambda(q)=sum_h (q exp(-q h))^2/sigma^2`.

Under the E33 single-height protocol, only 8/144 current modes are
Fisher-stable, 136/144 are dark/refused, and the generated truth has
0.9228192454 dark-energy fraction. A full naive least-squares current inverse
hallucinates dark modes and has total RMSE 720.7362501, while the certified
projection has zero dark hallucination norm, stable-mode RMSE 0.1164511532,
and 3-sigma stable coefficient coverage 1.0. Adding a second height expands
the stable current subspace to 37 modes.

The open question is whether this projection/refusal certificate survives
non-diagonal graph/Hodge/CAD-like current bases, finite-width and registration
rho, external solver rows, real-calibrated QDM/NV nuisance, and eventually
measured data. E33 does not prove full current recovery or real chip reverse
analysis.
