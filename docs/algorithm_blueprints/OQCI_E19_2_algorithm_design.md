# OQCI / E19.2 Algorithm Design

**Title:** Observable Quotient Current Inversion for Multilayer Magnetic Current Inference  
**Evidence package target:** `E19_2_observable_quotient_identifiability_audit`  
**Intended repository location:** `experiments/evidence/E19_2_observable_quotient_identifiability_audit/`  
**Status:** design document; not evidence until implemented, run, audited, and registered.

---

## 0. Executive Summary

E19 and E19.1 showed an important failure mode in the current-density-inversion project.

- E19 v0: posterior evidence collapsed toward `H1_via`.
- E19.1: after calibration, block priors, expanded bases, and residual diagnostics, posterior evidence collapsed toward `H3_return_path`.
- E19.1 engineering gates passed, but scientific gates mostly failed.
- The observed failure is not merely an accuracy problem. It is a warning that winner-take-all topology inference is the wrong target when the current observation family cannot distinguish competing internal states.

This document proposes a new algorithmic theory and implementation target:

> **Observable Quotient Current Inversion (OQCI)**

The central principle is:

> Do not infer a unique internal current state. Infer which current/topology claims are forced by the external magnetic data under the current experiment family, and which claims remain compatible with multiple internal explanations.

Instead of outputting a single winning hypothesis such as `H1_via` or `H3_return_path`, OQCI outputs:

1. the set of hypotheses consistent with the data;
2. intervals for physical claims over that set;
3. near-null / near-silent modes;
4. pairwise distinguishability distances;
5. resolution/rank diagnostics;
6. whether to accept, reject, or request a next measurement;
7. which next measurement would most reduce ambiguity.

The purpose of E19.2 is **not** to beat ridge accuracy. The purpose is to determine whether the H0/H1/H2/H3 claims are identifiable under single-height, single-state magnetic observations, and whether multi-height or multi-state observations shrink the observable equivalence classes.

---

## 1. Why E19.1 Is Not Enough

### 1.1 What E19.1 Established

E19.1 established that the current OBGHI implementation is runnable and auditable, but not scientifically successful as a discriminative topology posterior.

It revealed:

- high posterior confidence with low accuracy;
- broad `H3_return_path` basis dominance;
- failure to recover `H0_no_via`;
- collapse of `H2_model_gap`;
- insufficient reject / need-next decisions;
- case-specific via/gap angle degeneracy;
- ridge baseline outperforming the Bayesian topology posterior.

This is valuable negative evidence.

### 1.2 What E19.1 Did Not Prove

E19.1 did **not** conclusively prove that via/gap/return are physically indistinguishable under all single-height observations.

It proved a narrower statement:

> Under the current generated data, basis design, prior scaling, residual evidence, and decision rule, the E19.1 posterior model selection mechanism is not reliable and collapses toward `H3_return_path`.

The stronger physical claim requires an explicit identifiability audit:

- pairwise state construction;
- forward-distance comparison;
- approximate null-space extraction;
- claim interval computation;
- resolution spectrum;
- adversarial equivalent pairs;
- multi-height / multi-state comparison.

That is the role of E19.2.

---

## 2. Theoretical Shift

### 2.1 Old Target

The old target was:

```text
Given y, choose top hypothesis:
argmax_g p(g | y)
```

This is unsafe when posterior confidence is miscalibrated.

### 2.2 New Target

The new target is:

```text
Given y and noise epsilon, determine which physical claims L(z) are forced by data.
```

Let the internal state be:

```text
z = (J, g, theta, xi)
```

where:

- `J`: multilayer current vector;
- `g`: topology / mechanism hypothesis;
- `theta`: calibration parameters such as height, registration, PSF, gain;
- `xi`: model-gap / background / unmodeled residual state.

Let the experiment family be:

```text
E = {e_1, ..., e_N}
```

where each experiment can encode:

- sensor height;
- field component;
- scan window;
- load state;
- excitation state;
- sensor calibration;
- frequency/state if applicable.

The stacked forward map is:

```text
F_E(z) = [F_e1(z), ..., F_eN(z)]
```

With noise covariance `Sigma`, define the noise-weighted distance:

```text
d_E(z1, z2) =
|| Sigma^{-1/2} (F_E(z1) - F_E(z2)) ||_2
```

The noisy equivalence relation is:

```text
z1 ~_{E,epsilon} z2  iff  d_E(z1, z2) <= epsilon
```

The recoverable object is not `z`, but the equivalence class induced by the experiment family.

---

## 3. Consistent Set

Given observation `y`, define the consistent set:

```text
C_epsilon(y) =
{ z in A : || Sigma^{-1/2}(F_E(z) - y) ||_2 <= epsilon }
```

where `A` is the admissible physical state space.

In E19.2 generated-domain implementation, `A` is finite or low-dimensional and includes:

- H0 no-via candidates;
- H1 via candidates;
- H2 model-gap candidates;
- H3 return-path candidates;
- continuous current coefficients within each candidate subspace;
- bounded calibration/gap perturbations when enabled.

The algorithm should not immediately choose one member of `C_epsilon(y)`. It should ask:

> For a physical claim L(z), how much can L vary over all states compatible with the data?

Define the claim interval:

```text
I_L(y) =
[ min_{z in C_epsilon(y)} L(z),
  max_{z in C_epsilon(y)} L(z) ]
```

Examples:

- `L_H1(z) = 1` if any via explanation is active, else 0.
- `L_H2(z) = 1` if model-gap explanation is active, else 0.
- `L_H3(z) = 1` if return-path explanation is active, else 0.
- `L_layer3_current(z) = total current on layer 3`.
- `L_via_q(z) = current through candidate via q`.
- `L_gap_amp(z) = norm of model-gap coefficient`.

Interpretation:

- `[1, 1]`: data force the claim true.
- `[0, 0]`: data force the claim false.
- `[0, 1]`: claim is not identifiable under current experiment.
- narrow numeric interval: stable quantitative recovery.
- wide numeric interval: unstable or prior-dominated quantity.

---

## 4. Minimax Certainty Principle

For any estimator `L_hat(y)`, the unavoidable worst-case error is lower bounded by half the largest possible variation in `L` among states that are indistinguishable at the noise level:

```text
inf_{L_hat} sup_{z in A, ||F(z)-y|| <= epsilon}
|L_hat(y) - L(z)|
>=
1/2 sup_{z1,z2 in A, ||F(z1)-F(z2)|| <= 2epsilon}
|L(z1) - L(z2)|
```

This is the core scientific principle of OQCI.

The best algorithm is not necessarily the one that produces the sharpest-looking image. The best algorithm is the one that reports the irreducible uncertainty honestly.

---

## 5. Linearized Diagnostics

For a reference state `z0`, linearize:

```text
delta_y = D F_E(z0) delta_z + eta
```

Let:

```text
A_lin = Sigma^{-1/2} D F_E(z0)
```

Compute the SVD:

```text
A_lin = U S V^T
```

Then:

- large singular values correspond to observable directions;
- small singular values correspond to near-null directions;
- right singular vectors with `s_i <= tau_null` are near-silent internal perturbations;
- condition number gives stability;
- effective observable dimension is the number of singular values above threshold.

The approximate resolution operator is:

```text
R = A_lin^+ A_lin
```

or with Tikhonov:

```text
R_lambda = (A_lin^T A_lin + lambda I)^{-1} A_lin^T A_lin
```

If `R` is far from identity, only projected/smoothed components can be recovered.

E19.2 must report:

- singular spectrum;
- effective rank;
- near-null count;
- near-null example modes;
- pairwise projected subspace distances;
- resolution rank.

---

## 6. Pairwise Hypothesis Distinguishability

For hypothesis classes `Gi` and `Gj`, define:

```text
D_epsilon(Gi, Gj) =
min_{zi in Gi, zj in Gj}
|| Sigma^{-1/2} (F_E(zi) - F_E(zj)) ||_2
```

Interpretation:

- if `D_epsilon(Gi, Gj) <= epsilon`, then `Gi` and `Gj` are indistinguishable at noise level;
- if `D_epsilon(Gi, Gj) >> epsilon`, then they are distinguishable in principle.

For E19.2, compute pairwise distances among:

- H0 vs H1;
- H0 vs H2;
- H0 vs H3;
- H1 vs H2;
- H1 vs H3;
- H2 vs H3.

Also compute per-family distinguishability:

- no-via clean;
- single via;
- dense via cluster;
- model-gap registration;
- model-gap standoff;
- deep return loop.

E19.2 should not merely ask whether the classifier chose correctly. It should ask whether the true class was distinguishable from the alternatives in the first place.

---

## 7. OQCI Algorithm

### 7.1 Inputs

```text
config.json
case data or generator
operator bundle
hypothesis families
noise model
experiment family
claim definitions
epsilon policy
```

### 7.2 Outputs

```text
outputs/metrics.json
outputs/RUN_REPORT.md
outputs/CONSISTENT_HYPOTHESES.md
outputs/CLAIM_INTERVALS.md
outputs/PAIRWISE_DISTANCES.md
outputs/NEAR_NULL_MODES.md
outputs/RESOLUTION_AUDIT.md
outputs/ADVERSARIAL_PAIRS.md
outputs/NEXT_MEASUREMENT.md
```

### 7.3 Algorithm Steps

#### Step 1: Build experiment stack

For each experiment `e`:

```text
A_e = build_forward_operator(height, field_components, load_state, ...)
```

Stack:

```text
A_E = [A_e1; A_e2; ...; A_eN]
```

#### Step 2: Build hypothesis subspaces

For each hypothesis `g`:

```text
B_g = A_E H_g
```

where `H_g` is the current/gap/topology basis.

Do not use `B_g` for winner-take-all evidence first. Use it to evaluate distinguishability and consistency.

#### Step 3: Fit each hypothesis under fair residual objective

For each case and hypothesis `g`, solve:

```text
min_z || Sigma^{-1/2}(B_g z - y) ||_2^2 + alpha_g(z)
```

where `alpha_g` is only used for numerical stabilization and must be reported separately from data fit.

Report:

```text
data_residual_g
regularization_cost_g
effective_dof_g
coeff_norm_g
```

#### Step 4: Construct consistent hypothesis set

Given `epsilon`, define:

```text
G_consistent(y) =
{ g : min_z || Sigma^{-1/2}(B_g z - y) ||_2 <= epsilon }
```

Epsilon policies:

- known noise: `epsilon = sqrt(M) * sigma * c`;
- chi-square: `epsilon^2 = chi2_quantile(M, 0.95)`;
- empirical generated calibration: percentile of oracle residuals;
- sensitivity sweep: report results for multiple epsilon values.

#### Step 5: Compute claim intervals

For binary claims:

```text
I_Hi = [0, 1] if both Hi and non-Hi are consistent
I_Hi = [1, 1] if only Hi-compatible states are consistent
I_Hi = [0, 0] if no Hi-compatible state is consistent
```

For numeric claims:

Solve min/max constrained problems over consistent states, or approximate by sampling coefficients within residual threshold.

#### Step 6: Extract near-null modes

Use SVD or randomized SVD of `A_E H_all`, where `H_all` spans all admissible modes.

For each near-null vector:

- report singular value;
- report energy by block: graph / via / gap / return / residual;
- report field norm;
- report current norm;
- save vector to `.npz`.

#### Step 7: Decision rule

For a target claim `L`:

```text
if interval width <= tolerance and residual sanity passes:
    accept claim value/range
elif interval is wide but can be reduced by a feasible next experiment:
    need_next_measurement
else:
    reject / unidentifiable_under_current_protocol
```

Do not accept a topology solely because it has the best fit or highest posterior.

#### Step 8: Next measurement selection

For candidate next experiments `e_next`, estimate expected ambiguity reduction:

```text
score(e_next) =
current_interval_width - predicted_interval_width_after(e_next)
```

or:

```text
score(e_next) =
near_null_dimension_reduction
+ min_pairwise_distance_increase
+ resolution_rank_increase
- measurement_cost
```

Candidate next experiments:

- second sensor height;
- third sensor height;
- alternative load state;
- differential failing/golden observation;
- restricted high-resolution local scan;
- added field components if not already measured.

---

## 8. Multi-Height and Multi-State Extension

E19.2 should include two modes:

### Mode A: single-height audit

This reproduces the current setting and should likely show wide claim intervals and large near-null spaces.

### Mode B: synthetic multi-height audit

Add at least one additional height.

Compare:

```text
E_single = {height h1}
E_multi  = {height h1, height h2}
```

Report:

- pairwise distance increase;
- near-null dimension decrease;
- claim interval width reduction;
- resolution rank increase;
- ambiguity rate reduction.

If multi-height does not improve these metrics, report that honestly.

### Mode C: synthetic multi-state audit

Add alternate excitation/load state if the generator supports it.

Report the same metrics.

---

## 9. Scientific Gates

Engineering gates:

- package runs on smoke and default configs;
- metrics schema valid;
- reports written;
- no leakage flags present;
- operator columns nonzero;
- graph validation passes.

Scientific gates:

- `consistent_set_nonempty_rate >= 0.95`;
- `single_height_ambiguity_rate >= expected_min` for adversarial cases;
- `adversarial_pairs_detected_as_ambiguous >= 0.90`;
- `oracle_distinguishable_cases_have_tight_intervals >= 0.80`;
- `claim_interval_width_reduces_with_multi_height >= 0.20`;
- `near_null_dimension_decreases_with_multi_height > 0`;
- `no_wrong_high_confidence_accepts`: if a claim is false but indistinguishable, interval must be wide, not falsely tight.

Important:

The goal is not for all single-height claims to become identifiable. The goal is for the algorithm to correctly state when they are not identifiable.

---

## 10. Evidence Interpretation

Possible outcomes:

### Outcome 1: Single-height ambiguity, multi-height improvement

This is the ideal scientific result.

Interpretation:

> Single-height data cannot decide certain topology claims, but additional height or state measurements shrink the observable equivalence classes.

### Outcome 2: Single-height ambiguity, multi-height still ambiguous

Interpretation:

> The current hypothesis set and observation family remain insufficient. Need stronger experimental protocol or layout/external solver constraints.

### Outcome 3: Single-height claims all tight

Suspicious. Must check for prior leakage, too narrow admissible set, or generator/basis inverse crime.

### Outcome 4: Consistent sets empty

Indicates forward model mismatch, noise model error, or too strict epsilon.

---

## 11. Implementation File Structure

Recommended package:

```text
experiments/evidence/E19_2_observable_quotient_identifiability_audit/
  README.md
  requirements.txt
  configs/
    smoke.json
    default.json
    multi_height.json
  src/
    __init__.py
    config.py
    operators.py
    data.py
    hypotheses.py
    quotient.py
    intervals.py
    distances.py
    nullspace.py
    resolution.py
    next_measurement.py
    metrics.py
    reporting.py
    run_all.py
  tests/
    test_config.py
    test_consistent_set.py
    test_claim_intervals.py
    test_pairwise_distances.py
    test_nullspace.py
    test_adversarial_pairs.py
    test_run_outputs.py
  outputs/
    .gitkeep
  research_graph_patch/
    E19_2_research_graph_snippets.md
```

E19.2 may reuse E19.1 operators/data generators, but must not reuse the winner-take-all posterior decision as the core scientific output.

---

## 12. Minimal Generated Experiments

### 12.1 Oracle consistency test

Generate cases exactly from each hypothesis basis.

Expected:

- true hypothesis is consistent;
- alternatives may also be consistent if forward-equivalent;
- claim intervals reflect ambiguity.

### 12.2 Adversarial equivalent pair test

Construct pairs `(z1, z2)` such that:

```text
||F(z1) - F(z2)|| <= epsilon
```

but:

```text
L(z1) != L(z2)
```

Expected:

- OQCI outputs wide interval for `L`;
- OQCI does not falsely accept either claim.

### 12.3 Multi-height reduction test

Construct adversarial pair under one height. Add second height.

Expected:

- if second height separates them, pairwise distance increases;
- claim interval narrows;
- near-null dimension decreases.

### 12.4 Noise sensitivity sweep

Run epsilon sweep:

```text
epsilon in {0.5σ, 1σ, 2σ, 3σ}
```

Report how claim intervals change.

---

## 13. Relationship to E18/E19

E18 attempted physics-constrained current map optimization.

E19 attempted Bayesian topology posterior selection.

E19.2 changes the target:

```text
From: Which current/topology explanation wins?
To:  Which current/topology claims are identifiable under this experiment?
```

Therefore E19.2 should not be judged by top1 accuracy alone.

Correct metrics include:

- ambiguity detection;
- interval calibration;
- near-null extraction;
- distinguishability distance;
- next-measurement value;
- no hallucinated high-confidence claims.

---

## 14. Cannot Claim

E19.2 cannot claim:

- real QDM/NV validation;
- real CAD/Gerber/GDS validation;
- external FEM/FastHenry/COMSOL validation;
- universal via detection;
- real-board PDN robustness;
- mechanism-level correctness on real data;
- that generated-domain ambiguity necessarily holds for all real hardware.

E19.2 can claim only:

- generated-domain identifiability audit under specified operator/noise/experiment family;
- whether certain generated claims are or are not distinguishable under that protocol;
- whether additional synthetic measurements shrink the ambiguity.

---

## 15. Success Criteria

E19.2 is successful if it does all of the following:

1. shows when H0/H1/H2/H3 are indistinguishable under single-height data;
2. avoids wrong high-confidence accepts in adversarial cases;
3. produces explicit near-null modes;
4. computes meaningful claim intervals;
5. demonstrates whether multi-height or multi-state measurements reduce ambiguity;
6. preserves cannot-claim boundaries;
7. updates research graph as `limits` / `motivates` unless stronger evidence is truly present.

It does **not** need to solve all topology classification in single-height data.

The highest scientific success is not a pretty recovered current image. It is a rigorous statement of what the current experiment can and cannot force.
