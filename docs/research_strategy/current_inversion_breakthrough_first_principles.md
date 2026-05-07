# Magnetic-Field-to-Current Inversion Breakthrough Directions from First Principles

Date: 2026-05-06

Status: strategic design input, not evidence.

This document is a first-principles analysis of the research direction:

```text
magnetic field measurements -> current distribution / current mechanism inference
```

It does not add experimental evidence, does not upgrade any claim, and must not
be cited as validation. It is a strategy document for deciding which future
evidence packages are worth building.

## Scope

Affected research-graph claims:

- `C02_single_plane_identifiability_boundary`
- `C04_inverse_crime_and_operator_gap`
- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`
- `C12_real_qdm_nv_validation`
- `C13_calibration_protocol_reality`

Main involved nodes:

- Data: `D09_cad_gerber_gds_like`, `D10_real_qdm_nv`,
  `D11_chip_like_generated_pdn_family`
- Physics: `P01_biot_savart_maxwell_forward`, `P05_kcl_node_conservation`,
  `P06_kvl_or_resistive_network_consistency`, `P07_current_closure_loop`,
  `P08_return_path_completeness`, `P09_finite_width_material_thickness`
- Forward: `F02_centerline_biot_savart`, `F04_pypeec`, `F05_comsol_fem`,
  `F06_fasthenry`, `F07_real_measurement`
- Observation: `O04_qdm_nv_projection`, `O08_multi_height`,
  `O09_multi_state_excitation`, `O10_magneto_thermal`,
  `O11_ac_frequency_dependent`
- Representation: `R04_route_graph`, `R06_pdn_circuit_graph`,
  `R08_hypothesis_set`, `R09_posterior_candidate_set`,
  `R10_multilayer_chip_like_pdn_graph`
- Algorithm: `A08_differentiable_forward_optimization`,
  `A09_gnn_on_graph`, `A10_diffusion_or_gflownet_candidate_generator`,
  `A11_conformal_prediction`, `A12_bayesian_or_glrt_model_evidence`,
  `A14_pdn_physics_aware_learner`
- Protocol: `S05_solver_heldout`, `S10_real_heldout`,
  `S11_no_leakage_calibration_heldout`, `S12_conformal_or_selective_risk_protocol`
- Metrics: `M08_accepted_accuracy`, `M09_accepted_risk`,
  `M10_reject_rate`, `M11_mechanism_level_correctness`,
  `M13_family_generalization_gap`, `M15_real_sanity_pass_fail`,
  `M16_predicted_kcl_residual`, `M17_predicted_current_closure_error`

## Executive Conclusion

The breakthrough space is broad in implementation, but narrow in first
principles.

For magnetic-field-to-current inversion, a real breakthrough can only come from
changing at least one of these fundamental levers:

1. the observation operator and information content;
2. the admissible current space and physical prior;
3. the forward/sensor/noise/model-gap description;
4. the recovered target, from full current state to identifiable current claims;
5. the statistical decision and certification rule;
6. the computational method used to solve the resulting inverse problem;
7. the active experiment policy that chooses the next measurement;
8. the validation and transfer ladder that separates real evidence from inverse
   crime.

This is not a list of fashionable methods. It follows from the structure of the
inverse problem itself. Any proposal that does not alter one of these levers can
only repackage the same information and cannot beat the fundamental
identifiability boundary.

The strongest repository direction is therefore:

```text
multi-height / multi-state / vector magnetic observations
+ Graph-Hodge / PDN physical basis
+ OQCI / OBGHI identifiability certification
+ Bayesian or selective-risk refusal
+ active next-measurement design
+ external-solver and real QDM/NV validation ladder
```

The target is not merely a sharper current image. The target is a system that
answers:

```text
Which current claims are forced by the measured magnetic field?
Which claims remain compatible with multiple internal mechanisms?
What next measurement would most reduce that ambiguity?
```

## First-Principles Formulation

Let the unknown physical state be

```text
s = (J, g, theta, xi)
```

where:

- `J` is the current distribution;
- `g` is topology or mechanism, such as no-via, via, gap, return path, or
  off-layout residual path;
- `theta` contains calibration parameters, such as standoff, gain, registration,
  layer depth, PSF, NV axis, and background;
- `xi` is model gap or unmodeled nuisance.

The measured data are

```text
y = O_m(A_theta J, theta) + U_gap xi + epsilon
```

where:

- `A_theta` is the Maxwell / Biot-Savart electromagnetic forward operator;
- `O_m` is the measurement operator for protocol `m`;
- `U_gap` captures structured mismatch;
- `epsilon` is noise.

In quasi-static magnetic imaging, the forward operator is smoothing. In Fourier
language, high spatial frequencies are strongly attenuated with sensor standoff.
For a sheet-current idealization this appears as an exponential depth factor of
the form:

```text
high-|k| information decays roughly like exp(-|k| h)
```

This one fact drives most of the difficulty. Deep, fine, or compensating current
modes can become nearly invisible.

Define the experiment-family forward map:

```text
F_E(s) = [F_e1(s), F_e2(s), ..., F_en(s)]
```

with noise-weighted distance:

```text
d_E(s1, s2) =
|| Sigma^{-1/2} (F_E(s1) - F_E(s2)) ||_2
```

If:

```text
d_E(s1, s2) <= epsilon
```

then `s1` and `s2` are indistinguishable under the current experiment family and
noise level. No estimator can reliably decide between them without additional
assumptions or measurements.

Therefore the recoverable object is not necessarily `J`. The recoverable object
is the quotient induced by the experiment:

```text
state space / magnetic indistinguishability
```

or, more practically, intervals over physical claims:

```text
I_L(y) = [min L(s), max L(s)] over all states s consistent with y.
```

A breakthrough either changes this quotient, restricts the admissible states
correctly, estimates the quotient more honestly, computes it at scale, or
validates it against independent reality.

## What Counts as a Breakthrough

A result is scientifically meaningful if it does at least one of the following:

1. enlarges the magnetic information content;
2. reduces the admissible current space using correct physical constraints;
3. improves the forward/sensor model enough to reduce false mechanisms;
4. proves which current claims are identifiable or unidentifiable;
5. gives calibrated uncertainty, refusal, or next-measurement decisions;
6. solves a previously intractable constrained inverse problem at useful scale;
7. transfers from generated/same-operator data to external solver or real
   measured data.

Improving a leaderboard metric on the same generated operator is useful
engineering. It is not, by itself, a fundamental breakthrough.

## Breakthrough Class 1: Observation and Information Content

First question:

```text
Does the measured magnetic field contain enough information?
```

If the answer is no, no downstream algorithm can make the missing information
appear. This is the highest-leverage class.

Possible directions:

- reduce standoff and PSF;
- measure all available vector components, not only `Bz`;
- collect multi-height scans;
- collect multiple excitation or load states;
- use differential failing/golden measurements;
- use AC, phase, or frequency-dependent magnetic response;
- improve SNR, dynamic range, drift control, and background subtraction;
- use QDM/NV near-field imaging where appropriate;
- add local high-resolution rescans driven by posterior ambiguity.

Why this can break the problem open:

- It changes `F_E`.
- It can increase pairwise distances between previously compatible states.
- It can reduce near-null dimension.
- It can shrink claim intervals.

Repository implication:

`E13` showed generated-domain multi-state benefits, while `E19.2` showed that
the current single-height setting remains fundamentally ambiguous for
H0/H1/H2/H3. The next observation-side breakthrough package should not only
report accuracy. It should report:

- pairwise hypothesis distances;
- near-null count;
- claim interval width;
- ambiguity rate;
- predicted next-measurement utility.

Important boundary:

Even NV/QDM does not abolish Biot-Savart smoothing. It can move the practical
cutoff by improving standoff, sensitivity, and vector information. Deep or
screened modes can remain below noise.

Literature touchpoints:

- QDM imaging has been used for IC activity fingerprinting and vector magnetic
  measurements in different active states:
  <https://arxiv.org/abs/2004.03707>.
- QDM has been demonstrated for 2D current distributions in an 8 nm flip-chip IC
  and 3D current paths in multilayer PCB structures:
  <https://arxiv.org/abs/2202.08135>.
- QDM current sensing has continued into wafer-level circuit examples:
  <https://arxiv.org/abs/2506.17742>.

## Breakthrough Class 2: Admissible Current Space and Physical Priors

Second question:

```text
Which current distributions are physically allowed?
```

The full pixel-current space is far too large. Many current maps fit the same
magnetic field but violate circuit physics, layout constraints, or port
conditions. A correct prior can turn an impossible inverse problem into a
decidable restricted problem.

Possible directions:

- KCL node conservation;
- KVL or resistive network consistency;
- current closure and return-path completeness;
- known ports, supply domains, package pins, load states, and boundary currents;
- layer stack, conductor width, thickness, material, and vias;
- CAD/GDS/Gerber graph constraints;
- Graph-Hodge decomposition into gradient, curl, harmonic, port, via, return,
  and residual modes;
- sparse or structured basis banks for expected failure mechanisms;
- explicit off-layout residual basis so the model can refuse instead of forcing
  a wrong in-layout explanation.

Why this can break the problem open:

- It changes the admissible set `A`.
- It removes physically impossible null-space directions.
- It can turn broad image reconstruction into low-dimensional mechanism
  inference.

Repository implication:

This is the direction represented by `C06`, `C10`, E10-E12, E14, E15, E18, and
E19. It remains generated-domain until real CAD/GDS parsing and external solver
rows exist.

Critical risk:

A wrong or incomplete physical prior can make the result more confident and
less true. For example, forcing KCL on an incomplete return-path graph can
project real current into the wrong topology. Therefore any strong prior must
be paired with residual modes, model-gap diagnostics, and refusal.

## Breakthrough Class 3: Forward, Sensor, Noise, and Model-Gap Realism

Third question:

```text
Is the forward/sensor model close enough to the real measurement chain?
```

If the model is wrong, inversion will explain model error as current structure.
This is how via false positives, return-path hallucinations, and gap-collapse
failures arise.

Possible directions:

- finite-width and finite-thickness conductor forward models;
- material and conductivity modeling;
- substrate, package, shielding, and stackup effects;
- frequency-dependent current redistribution, skin/proximity effects, and
  inductive coupling;
- external solver validation with COMSOL, FastHenry, Ansys, FEM, or equivalent;
- PyPEEC as generated-domain bridge, not real ground truth;
- QDM/NV sensor chain: axis projection, ODMR response, PSF, standoff, drift,
  registration, gain, background, line-shape uncertainty;
- structured model-gap bases for registration, standoff, PSF, background, and
  missing return paths.

Why this can break the problem open:

- It changes the actual likelihood `p(y | s)`.
- It prevents wrong physical mechanisms from absorbing sensor artifacts.
- It allows generated results to be stress-tested against independent physics.

Repository implication:

`F05_comsol_fem` and `F06_fasthenry` are missing. `C04` already documents
operator-gap risk. A major near-term breakthrough would be a small, auditable
external-solver benchmark that quantifies where the current generated operators
agree or fail.

## Breakthrough Class 4: Identifiability Target and Observable Quotient

Fourth question:

```text
What exactly are we trying to recover?
```

Trying to recover full internal current state is usually too strong. The correct
target is:

```text
the set of current claims forced by magnetic data under a stated protocol.
```

Possible directions:

- observable subspace extraction;
- near-null mode analysis;
- resolution operator analysis;
- pairwise hypothesis distinguishability;
- consistent-set inference;
- claim intervals;
- OQCI-style quotient recovery;
- OBGHI-style observable Bayesian Graph-Hodge posterior;
- explicit unidentifiability certificates.

Why this can break the problem open:

- It changes the scientific output from a false unique answer to a certified
  identifiable claim.
- It turns failure into useful knowledge.
- It prevents wrong high-confidence decisions.

Repository implication:

`E19.2` is the strongest current evidence for this direction. It showed that the
single-height protocol cannot disambiguate H0/H1/H2/H3 in the generated audit.
That is not a failure of the project. It is a correct identification of the
problem boundary.

The next step is not only to improve top-1 accuracy. The next step is to shrink
claim intervals by changing observation design or admissible physics, and to
report when that does not happen.

## Breakthrough Class 5: Statistical Decision, Certification, and Refusal

Fifth question:

```text
When should the system answer, and when should it refuse?
```

Current inversion often fails by returning a clean-looking current map even when
the data do not justify it. A scientific system must be allowed to say:

```text
unidentifiable under current protocol
```

or:

```text
need next measurement
```

Possible directions:

- Bayesian model evidence;
- posterior over current claims rather than only current pixels;
- conformal or selective-risk control;
- accepted-risk and reject-rate reporting;
- calibration/held-out separation;
- hidden/out-of-library stress;
- mechanism-level correctness audits;
- posterior predictive checks;
- decision utility rather than pure reconstruction error.

Why this can break the problem open:

- It changes the decision rule, not necessarily the forward information.
- It prevents overclaiming.
- It can make a system useful in practice before full recovery is possible.

Repository implication:

`C07`, `C08`, `C11`, `C13`, and `C14` touch this class. The key is to avoid
treating primary-label accuracy as mechanism-level truth. Accepted hidden cases
need parameter-level audits.

## Breakthrough Class 6: Computation and Scalable Algorithms

Sixth question:

```text
Can the physically correct inverse problem be solved at useful scale?
```

Computation is not the deepest information lever, but it is required once the
right problem is defined. A mathematically correct OQCI/OBGHI system can become
intractable if hypothesis sets, graph bases, external solvers, or posterior
sampling are too large.

Possible directions:

- differentiable Biot-Savart and differentiable sensor operators;
- sparse, TV, curl, divergence-free, and Graph-Hodge regularization;
- constrained optimization over KCL/KVL graphs;
- warm-started solvers and continuation methods;
- GNN proposal models over CAD/PDN graphs;
- diffusion, GFlowNet, MCMC, SMC, or delayed-acceptance candidate generation;
- amortized inference for local posterior approximation;
- randomized SVD and low-rank updates for observable subspaces;
- GPU acceleration only where large matrix, deep learning, or CUDA workloads
  justify it.

Why this can break the problem open:

- It makes the right physics/statistics usable.
- It can enable posterior or consistent-set computation that would otherwise be
  too expensive.

Boundary:

Computation alone cannot create information. A faster or larger neural network
is not a first-principles breakthrough unless it is paired with better
observation, better physics, better target definition, or better certification.

Repository implication:

`E16`, `E17`, `E18`, and `A14` are computation-side progress. E18 also shows the
risk: KCL improvement did not automatically mean current-RMSE improvement.

## Breakthrough Class 7: Active Experiment and Next-Measurement Policy

Seventh question:

```text
Given the current ambiguity, what should be measured next?
```

Active measurement is formally part of observation design, but it deserves its
own class because it changes the workflow from passive reconstruction to
closed-loop discovery.

Possible directions:

- choose the next sensor height;
- choose vector channel or ODMR protocol;
- choose local high-resolution scan region;
- choose load or excitation state;
- choose frequency or phase measurement;
- choose failing/golden differential experiment;
- choose whether to ask for CAD, external solve, or calibration coupon;
- choose when additional measurement is not worth the cost.

Why this can break the problem open:

- It directly attacks the current consistent-set width.
- It converts uncertainty into an experimental design objective.
- It is the natural operational form of OQCI.

Repository implication:

The likely next high-value package is an active OQCI package:

```text
E20_active_oqci_measurement_design
```

It should report expected ambiguity reduction, not only accuracy.

## Breakthrough Class 8: Validation and Transfer Ladder

Eighth question:

```text
Does the claimed breakthrough survive outside the data-generation loop?
```

This class is not a new mathematical inversion operator, but it is a scientific
breakthrough lever. Without it, same-operator success can be inverse crime.

Possible ladder:

1. analytic wire/loop/via sanity;
2. independent numerical solver on small cases;
3. generated PyPEEC-domain bridge;
4. COMSOL/FastHenry/FEM held-out subset;
5. simple measured wire;
6. known-via or known-return coupon;
7. real PCB/package/chip current path;
8. real held-out QDM/NV rows with metadata and sanity gates.

Why this can break the problem open:

- It separates real robustness from generated-domain performance.
- It exposes operator gaps and calibration gaps.
- It converts an algorithm into a physical measurement system.

Repository implication:

`C12` remains blocked until measured rows exist. `E09` is an interface scaffold,
not real validation. This is one of the most important limitations in the
current graph.

## Completeness Analysis

The taxonomy above is complete at the level of first-principles levers under the
following scope:

```text
Goal: infer current distributions or current mechanisms from magnetic-field
measurements under Maxwell/quasi-static electromagnetic physics.
```

Formal argument:

Any inversion system can be described by:

```text
state space        S
experiment family  E
forward map        F_E : S -> Y
noise/model gap    Sigma, U_gap, theta
prior/constraint   P(S) or admissible set A
target             L(S)
decision rule      delta(Y)
computation        approximate solver for delta
validation domain  D_valid
```

A proposed breakthrough must change at least one of these objects.

Mapping:

- Change `E` or the sensor: Class 1 or Class 7.
- Change `A` or `P(S)`: Class 2.
- Change `F_E`, `Sigma`, `theta`, or `U_gap`: Class 3.
- Change `L(S)` from full-state recovery to identifiable claim recovery:
  Class 4.
- Change `delta(Y)`, uncertainty, risk, or refusal: Class 5.
- Change the solver for the same mathematical problem: Class 6.
- Change `D_valid` or independent evidence: Class 8.

If a proposal changes none of these, then it uses the same data, same operator,
same admissible state space, same target, same decision rule, same computation,
and same validation domain. It cannot be a distinct first-principles
breakthrough.

This does not mean every implementation has been enumerated. It means every
implementation must enter through one or more of these gates.

## Stress Test Against Common "New Directions"

The table below checks whether apparent missing directions are actually outside
the taxonomy.

| Proposed direction | First-principles category |
| --- | --- |
| Larger U-Net, transformer, diffusion model | Class 2 if it changes learned prior; Class 6 if it only computes faster |
| GNN over CAD/GDS | Class 2 and Class 6 |
| QDM/NV hardware | Class 1 and Class 3 |
| Multi-height scans | Class 1 and Class 7 |
| Multi-state current injection | Class 1 and Class 7 |
| Frequency-domain / AC response | Class 1 and Class 3 |
| Thermal or electrical side-channel | Class 1 if treated as extra observation; outside pure magnetic-only scope if it becomes dominant |
| FEM/FastHenry/COMSOL | Class 3 and Class 8 |
| PyPEEC | Class 3 and Class 8 only within generated-domain limits |
| Sparse/TV/Hodge regularization | Class 2 and Class 6 |
| Bayesian inference | Class 5; also Class 4 if the target is claim intervals |
| Conformal or selective prediction | Class 5 |
| Active learning | Class 7 |
| Calibration coupons | Class 3, Class 5, and Class 8 |
| Human expert review | Class 2 if it adds priors; Class 8 if it validates mechanisms |
| LLM/agent orchestration | Class 6 operationally; not a physics breakthrough by itself |
| Destructive delayering, microscopy, X-ray | Outside magnetic-field-only inversion; auxiliary validation or multi-modal observation if included |
| Full netlist reverse engineering | Outside what magnetic current inversion alone can guarantee |

The taxonomy therefore appears exhaustive for magnetic-field-to-current
inversion, but not for all possible chip reverse-engineering workflows.

## What Would Falsify This Taxonomy?

To falsify the taxonomy, one would need a method that:

1. uses the same magnetic data;
2. uses the same forward and sensor model;
3. uses the same admissible current space;
4. estimates the same target;
5. uses the same loss and decision rule;
6. uses no new computational approximation that changes tractability;
7. uses no new validation domain;
8. yet reliably distinguishes states that are noise-indistinguishable under the
   forward map.

That would contradict the standard inverse-problem and information-theoretic
boundary. It is not a plausible research path.

A more realistic objection is not that there is a ninth lever, but that a future
technology combines several existing levers in a new way. For example:

```text
NV vector imaging + active load states + CAD graph prior + Bayesian claim
intervals + external-solver calibration
```

This is a new system architecture, but it is still a combination of the listed
first-principles levers.

## Recommended Repository Research Program

The next breakthrough sequence should be:

### E20: Active OQCI Measurement Design

Goal:

```text
Use OQCI consistent sets to choose height, state, vector channel, or local
rescan that maximally shrinks claim intervals.
```

Primary metrics:

- ambiguity-rate reduction;
- pairwise-distance increase;
- near-null-count decrease;
- claim-interval-width reduction;
- no wrong high-confidence accepts;
- measurement-cost-normalized utility.

Claim target:

- `C02_single_plane_identifiability_boundary`
- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`

### E21: External-Solver Operator Gap Ladder

Goal:

```text
Validate a small, auditable subset against COMSOL/FastHenry/FEM or equivalent.
```

Primary metrics:

- field residual between solvers;
- current mechanism disagreement;
- hypothesis-rank instability under solver swap;
- calibration parameters needed to align solver and measurement.

Claim target:

- `C04_inverse_crime_and_operator_gap`
- `C10_pdn_kcl_distribution_need`

### E22: Real QDM/NV Simple-Wire and Known-Via Gate

Goal:

```text
Move from interface scaffold to measured rows with units, metadata, polarity,
background, standoff, and simple current sanity.
```

Primary metrics:

- `M15_real_sanity_pass_fail`;
- sign/polarity agreement;
- standoff fit;
- current scale agreement;
- background subtraction stability.

Claim target:

- `C12_real_qdm_nv_validation`
- `C13_calibration_protocol_reality`

### E23: CAD/GDS Graph-Hodge Basis

Goal:

```text
Replace hand-authored generated graph scaffolds with real or realistic layout
graph-derived current bases.
```

Primary metrics:

- graph import validity;
- KCL/KVL/current-closure residuals;
- candidate coverage;
- return-path completeness;
- hypothesis ambiguity before/after layout prior.

Claim target:

- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`

### E24: Scalable Posterior Candidate Search

Goal:

```text
Make OQCI/OBGHI tractable on large graph candidate spaces.
```

Primary metrics:

- candidate recall under oracle inclusion;
- posterior or consistent-set approximation error;
- runtime and memory;
- accepted-risk stability;
- evidence ranking stability under solver/fidelity changes.

Claim target:

- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`

## Final Position

The major breakthrough path is not:

```text
better image-to-image current reconstruction on the same observation.
```

The major breakthrough path is:

```text
magnetic observation design
+ physical current-space restriction
+ forward/sensor calibration
+ observable-quotient identifiability
+ certified decision/refusal
+ scalable inference
+ real validation.
```

At first-principles level, this traverses the full space of ways to improve
magnetic-field-to-current inversion. Future ideas should be evaluated by asking
which lever they change and whether that change actually shrinks the magnetic
equivalence class for the current claim of interest.

