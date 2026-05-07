# E01-E29 Deep Replay and Next Major Breakthrough Direction

Date: 2026-05-06

Status: strategic audit and mathematical design. This document is not
experimental evidence. It must not support or upgrade any claim by itself.

Scope:

- replay E01-E29 with a skeptical audit stance;
- do not assume code, worker reports, or gates are scientifically correct;
- compare evidence against algorithm blueprints;
- identify the next most likely major current-inversion breakthrough;
- define the minimum certificate that would make that breakthrough defensible.

Primary verdict:

```text
The next most likely major breakthrough is not full current-map recovery and
not full H0/H1/H2/H3 classification.

The strongest route is a calibrated transfer-operator observable-quotient
certificate:

multi-state port-to-magnetic transfer matrix
+ Gram or related transfer invariant
+ Graph-Hodge / shared-network admissible current model
+ E25-style calibrated operator radius
+ family-heldout hard-case layout ensemble
+ active port-state design scored by robust invariant Gamma.
```

The valid breakthrough target is:

```text
positive robust margins for an observable quotient of topology/mechanism claims,
with unresolved intra-quotient pairs explicitly reported.
```

The current best positive evidence is E28. It supports only:

```text
Q0 = {H0_no_via}
Q12 = {H1_via, H2_model_gap}
Q3 = {H3_return_path}
```

It does not support:

```text
H1_via vs H2_model_gap separation,
full four-hypothesis separability,
real chip reverse analysis,
real QDM/NV validation,
real CAD/GDS validation,
or external solver validation.
```

## Audit Standard

The project is about magnetic field to current / current-mechanism inference.
The first-principles object is not an image, a classifier score, or a residual.
It is an equivalence class induced by the magnetic forward operator and the
available experiment family.

Let:

```math
s=(J,g,\theta,\xi)
```

where `J` is current density, `g` is topology or mechanism, `theta` is
calibration/sensor state, and `xi` is model gap / background / unmodeled
physics. For experiment family `E`,

```math
y_E=F_E(s)+\eta.
```

Two states are experimentally equivalent at noise level `epsilon` if:

```math
\|\Sigma^{-1/2}(F_E(s_1)-F_E(s_2))\|_2 \le \epsilon.
```

For any binary or numeric claim `L(s)`, the unavoidable minimax uncertainty is
bounded below by:

```math
\inf_{\hat L}
\sup_{\|F_E(s)-y\|\le\epsilon}
|\hat L(y)-L(s)|
\ge
{1\over2}
\sup_{\|F_E(s_1)-F_E(s_2)\|\le2\epsilon}
|L(s_1)-L(s_2)|.
```

Therefore any method that returns a single topology label while the claim
interval is wide is overclaiming.

The minimum acceptable pairwise certificate is:

```math
\Gamma^\Phi_{ab}
=
\delta^\Phi_{ab}
-\epsilon^\Phi
-\rho^\Phi_a
-\rho^\Phi_b
-\tau^\Phi
>0,
```

where:

- `a,b` are decision classes or quotient classes;
- `Phi` is the declared representation or invariant;
- `delta` is the calibrated pairwise distance after allowed nuisance/profile
  freedom;
- `epsilon` is the measurement/noise radius in the units of `Phi`;
- `rho` is operator/nuisance radius;
- `tau` is the acceptance threshold.

A result is not a breakthrough if it is only:

```text
top-1 accuracy,
KCL residual reduction,
raw residual gap,
positive uncalibrated distance,
same-operator reconstruction quality,
or a CI/test pass.
```

## Evidence Replay

### E01-E07: Foundation and Operator Gap

Useful result:

- E01 validates ideal canonical Biot-Savart sign, scale, and sanity.
- E02 establishes the single-plane low-pass / depth-attenuation boundary.
- E03/E04 expose no-via, via, return, finite-width, and topology baseline
  failure modes.
- E05 gives a QDM-like stress scaffold, not real ODMR/QDM validation.
- E06/E07 show that solver/operator gaps matter and PyPEEC is useful only as a
  generated-domain bridge.

Skeptical interpretation:

```text
These packages justify the research frame, but none closes the inverse problem.
They show that missing observation information and operator mismatch are real
constraints, not implementation inconvenience.
```

No major breakthrough:

- no external solver claim;
- no real data claim;
- no mechanism-level correctness;
- no evidence that pixel current maps are uniquely recoverable.

### E08-E14: Graph/Hypothesis Frame, Calibration, Layout Scaffold

Useful result:

- E08 makes graph/hypothesis scoring and refusal a better frame than pure pixel
  reconstruction.
- E09 adds real-data intake gates but no measured rows.
- E10/E11 build generated PDN/KCL and chip-like graph families.
- E12 shows generated-domain physics-aware graph projection improves KCL and
  current closure over unconstrained current regression.
- E13 shows multi-height/multi-state generated observations can improve rank
  and margins.
- E14 creates a simplified layout graph import scaffold.

Skeptical interpretation:

```text
Graph/KCL priors are necessary but not sufficient. They restrict the admissible
space, but if the hypothesis spaces remain too flexible or generated, they can
still explain the same magnetic data.
```

No major breakthrough:

- E12 label accuracy plus KCL consistency is not mechanism explanation.
- E14 is not real CAD/GDS import.
- E13 is generated-domain observation design, not hardware-feasible active
  measurement.

### E15-E18: Benchmark, Differentiable Forward, Physics-Constrained Inverse

Useful result:

- E15 creates a four-layer via-chain benchmark and exposes deep-layer
  attenuation.
- E16 gives differentiable Biot-Savart forward layers.
- E17 provides regularized baselines.
- E18 shows KCL-constrained optimization can drive KCL residual near zero.

Skeptical interpretation:

```text
KCL consistency is a constraint, not an information source. It can make currents
more physical, but it does not create magnetic distinguishability between
mechanisms that share an observable equivalence class.
```

No major breakthrough:

- E18 does not beat ridge_scaled in its own leaderboard.
- Dense-via recall and deep-layer misallocation remain failure modes.
- Same-operator differentiability does not close operator gap.

### E19 and E19.2: OBGHI Collapse and OQCI Target Correction

Useful result:

- E19 posterior selection collapsed toward broad hypotheses.
- E19.2 changed the target to consistent sets, claim intervals, near-null
  modes, and observable quotient reasoning.

Skeptical interpretation:

```text
E19.2 is theoretically correct: infer forced claims, not a single winner.
But the implemented basis/observation family still leaves broad ambiguity.
```

No major breakthrough:

- OQCI reports ambiguity; it does not resolve it by itself.
- The old basis is too flexible and leaves H0/H1/H2/H3 insufficiently
  separated under the tested protocol.

### E20: Active OQCI on the Old Basis

Provisional worker/worktree result:

- engineering gates pass;
- scientific gates fail;
- baseline ambiguity rate remains 1.0;
- best regularized valid disambiguation rate about 0.1667;
- best regularized truth-in-consistent-set rate about 0.3333;
- min Gamma after one-step/two-step remains about -0.624;
- critical H1/H2 Gamma remains non-positive.

Skeptical interpretation:

```text
Active measurements cannot rescue a representation whose hypothesis spaces
share the same observable subspace. Old-basis active design is a negative result.
```

Lesson:

```text
Measurement design must optimize the same robust certificate on a better
representation. It cannot be an add-on to a degenerate basis.
```

### E21: Operator Gap vs Mechanism Margin

Provisional worker/worktree result:

- external solver artifacts absent;
- PyPEEC not available in the default full output;
- centerline-vs-finite-width field relative RMSE about 0.409;
- interclass_delta_min about 2.07e-5;
- operator_shift_radius_max about 8.11e-2;
- gap_to_margin_ratio about 3915;
- stable_classification_possible_by_margin is false.

Skeptical interpretation:

```text
Operator uncertainty dwarfs the mechanism margin. Any claim that depends on a
smaller residual gap is not robust.
```

Lesson:

```text
Every future positive Gamma must subtract an operator radius. Otherwise it is
an inverse-crime artifact candidate.
```

### E23: Graph-Hodge Basis

Provisional worker/worktree result:

- KCL/projected basis properties look good.
- robust_margin min_gamma_all_pairs about -5695.
- H1/H2 hardcase Gamma about -2918.
- certified pair rate 0.
- adversarial worst_gamma about -7866.
- greedy excitation does not beat default/random.

Skeptical interpretation:

```text
Graph-Hodge admissible bases are structurally useful, but the current
certificate is dominated by uncertainty and/or basis flexibility. The basis is
not enough unless paired with a stronger observable object and calibrated rho.
```

Lesson:

```text
Use Graph-Hodge/KCL as admissible-state construction for E28-style transfer
operators, not as a standalone robust certificate yet.
```

### E24: Shared-Network Profile Inversion

Registered smoke result:

- engineering gates pass;
- scientific gates fail;
- consistent set truth-in rate 1.0 but multi-consistent rate 1.0;
- singleton correct rate 0;
- H1/H2 shared profile gap gate fails;
- critical-pair profile Gamma gate fails;
- operator-stress Gamma gate fails.

Skeptical interpretation:

```text
Shared conductance theta is the right physical idea, but the implemented
profile residual gaps are still too small or too easy to compensate. It does
not yet create a robust decision certificate.
```

Lesson:

```text
The network model should supply transfer matrices and nuisance-bounded
hypothesis manifolds for E28, not be judged by raw residual fit alone.
```

### E25: Calibrated Volume Forward and Rho

Registered result:

- package reports acceptance gates passing in metrics;
- volume/rho artifacts exist;
- failure modes report overlapping conductor volumes in the
  four_layer_via_return_motif;
- worst convergence behavior can be dominated by overlap and low-order
  quadrature;
- combined conservative rho can be comparable to or larger than signal.

Skeptical interpretation:

```text
E25 is not separability evidence. It is an error-budget instrument. The
scientific risk is that a "passing" rho package can still include geometry
artifacts, best-case convergence selection, or overly conservative radii.
```

Lesson:

```text
Future Gamma certificates need E25, but also need stricter rho artifact audits:
median/worst convergence, overlap detection, family-specific rho, and
calibration/evaluation split discipline.
```

### E26: Generic Active Port-State Gamma

Provisional worker/worktree result:

- engineering gates pass;
- scientific gates fail;
- aggregate min Gamma values include `-inf`;
- positive_gamma_rate is 0;
- greedy does not beat random/default;
- wrong_accept decreases gate fails.

Skeptical interpretation:

```text
Generic port-state optimization is not enough. If the score function degenerates
to -inf or does not target the final transfer-invariant certificate, it cannot
drive a breakthrough.
```

Lesson:

```text
Active design should be moved inside the E28 certificate: choose port states to
maximize held-out min Gamma of the selected invariant over quotient classes.
```

### E27: Schur Edge-Defect Signatures

Registered result:

- Sherman-Morrison validation is numerically excellent, max error about 1.9e-14.
- Mean edge Gamma about -0.0357.
- positive_edge_gamma_rate 0.
- Schur vs best other signal ratio about 0.557.
- pairwise positive Gamma rate about 2.87e-4.
- truth_in_consistent_set_rate 0 and singleton_wrong_rate 1 in the full output.

Skeptical interpretation:

```text
The derivation is useful, but the standalone magnetic edge-defect signal is too
small relative to noise/rho in this generated setup.
```

Lesson:

```text
Use Schur voltage-drop sensitivity to propose informative port states, not as
the primary certificate.
```

### E28: Transfer-Matrix Observable Invariants

Registered result after audit repair:

- engineering and scientific gates pass.
- selected invariant is Gram.
- Gram full-pair positive Gamma rate is 5/6.
- Gram quotient Q0/Q12/Q3 has all positive cross-quotient margins.
- selected-invariant quotient min Gamma is 0.4511206603.
- H1/H2 Gram Gamma is -0.1286141869 and explicitly unresolved.
- gain-only hardcase sweep has 3/5 rows where raw quotient fails but Gram
  quotient remains positive.
- consistent-set truth-in rate is 1.0, singleton_wrong_rate is 0, but
  ambiguity_rate remains 0.6667.

Skeptical interpretation:

```text
E28 is the first genuine positive candidate, but only for a quotient. It does
not prove full four-class recovery. Its default run is also not enough, because
raw already passes the easy quotient; the meaningful result is the hardcase
gain-nuisance regime where raw fails and Gram survives.
```

Lesson:

```text
The promising object is the transfer operator, not a single field image.
The promising claim is quotient separability, not complete current recovery.
```

### E29: Rho-Integrated Schur Gamma

Registered result:

- status partial;
- calibration_evaluation_split_enforced is false;
- positive conservative Gamma rate is 0;
- positive RSS Gamma rate is 0;
- pairwise conservative Gamma rate is 0;
- truth_missing_rate is 1.0;
- empty_rate is 0.4.

Skeptical interpretation:

```text
The E29 concept is correct, but the current result is negative and protocol
discipline fails. It confirms that Schur + rho is not yet a breakthrough.
```

Lesson:

```text
The rho-integrated certificate should be rebuilt around E28 transfer invariants,
not around standalone Schur edge signatures.
```

## Blueprint Audit

The blueprints are useful design inputs, but evidence metrics override them.

| Blueprint | Sound core idea | What evidence says | Keep / discard |
|---|---|---|---|
| OQCI/E19.2 | infer forced claims and intervals, not a winner | correct target, but old basis remains ambiguous | keep as decision semantics |
| E20 active OQCI | change experiment family | old-basis active design fails | keep only if scored by final Gamma |
| E21 operator gap | attack inverse crime | operator gap dwarfs margins | mandatory gate |
| E23 Graph-Hodge | restrict admissible currents by layout/KCL | KCL good, robust Gamma bad | keep as state/basis prior |
| E24 shared network | tie states by shared conductance | profile gaps too small in smoke | keep as transfer generator |
| E25 calibrated rho | decompose operator radius | needed but not separability evidence | integrate with stricter audit |
| E26 active ports | optimize port states | generic Gamma degenerates/fails | replace by E28-invariant objective |
| E27 Schur | exploit rank-one edge perturbation | formula correct, signal below uncertainty | use for state proposal only |
| E28 transfer invariants | quotient nuisance and compare response geometry | first positive quotient result | central route |
| E29 rho Schur | conservative Gamma bridge | split/gamma fail | rebuild around E28 |

## First-Principles Reason for the Next Direction

Static magnetic inversion is low-pass and depth-attenuated. In Fourier form for
sheet currents, the kernel contains:

```math
e^{-|k|z}.
```

Thus high spatial frequencies and deep-layer differences are exponentially
suppressed. No estimator can restore mechanism labels whose magnetic
differences sit below noise and operator uncertainty.

Changing from an image `y_s` to a transfer matrix

```math
T_y(h,U)=A_h C_h D_h^T L_h^\dagger U
```

changes the observable. It measures how the network maps accessible port states
to magnetic fields. Topology is often more visible in response geometry than in
one absolute field image.

The whitened Gram invariant:

```math
G_h = T_h^T W^T W T_h,
```

```math
\bar G_h =
\operatorname{diag}(G_h)^{-1/2}
G_h
\operatorname{diag}(G_h)^{-1/2}
```

compares correlations among measured response states. It suppresses per-state
amplitude scale and helps under sensor gain / current-scale nuisance. E28's
hardcase result is exactly this mechanism:

```text
raw quotient Gamma becomes negative under stronger gain nuisance,
while Gram quotient Gamma remains positive.
```

This is a real first-principles lever because it changes both:

```text
1. the experimental object: field image -> response operator;
2. the nuisance quotient: amplitude/gain directions -> invariant geometry.
```

## The Next Most Likely Major Breakthrough

Name:

```text
CTOQC: Calibrated Transfer-Operator Quotient Certificate
```

The target is not a new broad evidence package. It should be an E28-centered
Round 2/3 program, or a new E only if the package contract changes materially.

### Mathematical Target

Let `l` be a layout, `U_l` a feasible port-state design, and `Q_a,Q_b` quotient
classes of topology/mechanism hypotheses. For invariant `Phi`, define:

```math
\delta^\Phi_{ab}(l,U_l)
=
\inf_{h\in Q_a,g\in Q_b}
\|\Phi(T_h(l,U_l))-\Phi(T_g(l,U_l))\|.
```

Subtract calibrated uncertainty:

```math
\Gamma^\Phi_{ab}(l,U_l)
=
\delta^\Phi_{ab}(l,U_l)
-\epsilon^\Phi(l,U_l)
-\rho^\Phi_a(l,U_l)
-\rho^\Phi_b(l,U_l)
-\tau^\Phi.
```

The quotient certificate passes on evaluation layouts only if:

```math
\min_{l\in L_{eval}}
\min_{a<b}
\Gamma^\Phi_{ab}(l,U_l) > 0
```

or, for a refusal-safe protocol:

```math
\Pr_{l\in L_{eval}}
\left[
\min_{a<b}\Gamma^\Phi_{ab}(l,U_l)>0
\right]\ge p_{target}
```

with all non-certified layouts refused, not counted as correct.

The hard unresolved pair must be tracked:

```math
\Gamma^\Phi_{H1,H2}(l,U_l).
```

If it remains negative, the valid quotient is:

```text
{H0}, {H1,H2}, {H3}.
```

If it becomes positive only after extra observation physics, then and only then
can the claim move toward H1/H2 separation.

### Required Innovations

1. Family-heldout layout ensemble.

   Calibration layouts choose:

   ```text
   invariant, tau, epsilon policy, rho policy, port-state heuristic.
   ```

   Evaluation layouts only report:

   ```text
   Gamma, refusal, truth-in-set, singleton wrong, empty rate.
   ```

2. E25 rho integration with stricter gates.

   The certificate must subtract:

   ```text
   rho_gain
   rho_height
   rho_registration
   rho_layer_z
   rho_finite_width
   rho_background
   rho_psf
   ```

   E25 artifacts must be audited for:

   ```text
   overlap geometry,
   median and worst quadrature convergence,
   family-specific radius,
   calibration/evaluation split.
   ```

3. Raw-control hardcases.

   A real invariant breakthrough requires cases where:

   ```math
   \Gamma^{raw}_{ab}<0
   \quad\text{and}\quad
   \Gamma^{Gram}_{ab}>0.
   ```

   E28 already shows this for gain-only hardcases. The next step is to show it
   across layout families and calibrated rho.

4. Active states scored by transfer-invariant Gamma.

   Use Schur states as candidates:

   ```math
   b_q^\star=
   \arg\max_b
   {|a_q^T L^\dagger b|\over1+\alpha a_q^T L^\dagger a_q},
   ```

   but select final states by:

   ```math
   U^\star=
   \arg\max_U
   \min_{a<b}
   \Gamma^{Gram}_{ab}(U)-c(U).
   ```

   Do not optimize raw residual, entropy, current norm, or generic E26 Gamma
   unless they correlate with held-out invariant Gamma.

5. H1/H2 phase diagram.

   Sweep:

   ```text
   via conductance contrast,
   model-gap severity,
   standoff,
   registration,
   layer depth,
   finite width,
   port count,
   state count,
   SNR.
   ```

   Report:

   ```math
   \Gamma^{Gram}_{H1,H2}
   ```

   as a phase diagram. This decides whether H1/H2 is separable under static
   magnetic transfer measurements, or whether it belongs in the same quotient.

## Why Other Directions Are Less Likely Now

1. Pixel current inversion is blocked by nullspace and depth attenuation.
2. Stronger posterior selection already collapsed in E19.
3. Active measurement on the old basis failed in E20.
4. Operator gap dwarfs small mechanism margins in E21.
5. Graph-Hodge and shared-network constraints are useful but not enough alone.
6. Generic port-state design in E26 fails because the objective is not the final
   certificate.
7. Schur edge signatures in E27 are mathematically elegant but too weak as a
   standalone observable.
8. Rho-integrated Schur in E29 fails conservative Gamma and split discipline.

Thus the next breakthrough must combine the surviving pieces:

```text
E28 transfer invariant as the observable
+ E25 rho as the uncertainty budget
+ E23/E24 as admissible network physics
+ E27 as a state proposal mechanism
+ OQCI as the refusal/quotient semantics.
```

## Minimum Evidence Contract for the Next Run

A defensible next evidence package must include:

```text
layout_count >= 80
family_holdout_count >= 4
calibration_layouts disjoint from evaluation_layouts
state_count sweep in {2,4,6,8}
port_count sweep when available
gain/standoff/registration/finite-width rho
raw-vs-Gram hardcase control
H1/H2 phase diagram
E25 rho artifact audit
```

Required top-level metrics:

```text
selected_invariant
selected_invariant_chosen_on_calibration_only
eval_quotient_min_gamma
eval_quotient_positive_gamma_rate
eval_quotient_refusal_rate
eval_truth_in_consistent_set_rate
eval_singleton_wrong_rate
eval_empty_rate
raw_fail_gram_pass_count
H1_H2_gamma_quantiles
rho_breakdown_by_source
operator_gap_to_margin_ratio
```

Pass condition for a quotient breakthrough:

```text
On held-out generated layouts, after calibrated rho subtraction, Gram or a
preselected transfer invariant certifies positive robust margins for the
declared quotient classes, with zero wrong singleton accepts and explicit
refusal for non-certified layouts.
```

Pass condition for an H1/H2 breakthrough:

```text
Gamma_H1_H2 > 0 on held-out hardcases after rho subtraction and no leakage.
```

If H1/H2 remains negative, do not weaken the gate. The correct result is:

```text
H1 and H2 are one observable class under this protocol.
```

## If CTOQC Fails

If E28-centered CTOQC fails after calibrated rho, family holdout, and active
Gram-state design, then the next breakthrough is not software-only. It must
change observation physics:

```text
real multi-height vector QDM/NV,
differential golden-vs-failing measurements,
frequency/AC response,
magnetothermal joint observation,
or external-solver-calibrated layout priors.
```

Reason:

```text
If response-operator invariants cannot certify a quotient under calibrated
uncertainty, then the remaining ambiguity is physical under the current
experiment family.
```

## Final Recommendation

Continue with a single focused program:

```text
E28 Round 2/3: Calibrated Transfer-Operator Quotient Certificate.
```

Do not prioritize:

```text
new image reconstructions,
new top-1 classifiers,
generic active port search,
standalone Schur defect classification,
or uncalibrated raw residual profile fitting.
```

The next major breakthrough, if it comes, will be:

```text
a robust, rho-calibrated, family-heldout observable quotient theorem for
magnetic transfer operators.
```

That would be a real advance because it says exactly which current mechanism
claims are forced by magnetic measurements, and it refuses the rest.

