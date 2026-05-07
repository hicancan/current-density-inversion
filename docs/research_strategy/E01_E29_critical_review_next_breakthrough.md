# E01-E29 Critical Review and Next Breakthrough Direction

Date: 2026-05-06

Status: strategic mathematical audit and next-direction design. This document is
not evidence and must not upgrade any claim by itself.

Affected claims:

- `C02_single_plane_identifiability_boundary`
- `C04_inverse_crime_and_operator_gap`
- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`
- `C12_real_qdm_nv_validation`
- `C13_calibration_protocol_reality`

Primary conclusion:

```text
No E01-E29 result is yet a claim-level major current-inversion breakthrough.

The strongest next breakthrough candidate is:

Robust transfer-operator observable-quotient inversion:
multi-state port-to-magnetic transfer matrices
+ Gram/quotient invariants
+ Graph-Hodge/KCL/network physical bases
+ calibrated E25-style operator radius
+ hard-case layout-ensemble certification
+ active port-state design against robust Gamma.
```

This direction should be continued as an audited E28 Round 2/3 program, not as a
new disconnected E unless the research object changes.

## Audit Stance

The review below does not assume worker code, tests, or acceptance gates are
scientifically correct. A gate can pass for implementation reasons while the
mathematical certificate remains invalid. The relevant question is:

```math
\text{Does the evidence force a current/topology claim after subtracting noise,
operator uncertainty, nuisance freedom, and calibration leakage risk?}
```

For a hypothesis pair \(h,g\), the minimum acceptable certificate is:

```math
\Gamma^\Phi_{hg}
=
\delta^\Phi_{hg}
-\epsilon^\Phi
-\rho^\Phi_h
-\rho^\Phi_g
-\tau^\Phi_g
>0,
```

where:

- \(\Phi\) is the reported representation or invariant;
- \(\delta^\Phi_{hg}\) is pairwise separability after profiling nuisance;
- \(\epsilon^\Phi\) is measurement/noise radius in that representation;
- \(\rho^\Phi_h,\rho^\Phi_g\) are operator/model-gap radii;
- \(\tau^\Phi_g\) is the wrong-hypothesis acceptance threshold.

A raw residual gap, top-1 accuracy, or positive uncalibrated distance is not a
breakthrough unless it survives this inequality on held-out hard cases.

## First-Principles Reduction

Let current state be:

```math
s=(J,g,\theta,\xi),
```

where \(J\) is current density, \(g\) is topology/mechanism, \(\theta\) is
calibration/sensor geometry, and \(\xi\) is structured model gap.

Magnetic observation under experiment family \(E\):

```math
y_E = F_E(J,g,\theta,\xi)+\eta.
```

For quasi-static magnetic imaging:

```math
B(r)= {\mu_0\over4\pi}\int_D
{J(r')\times(r-r')\over\|r-r'\|^3}\,dr',
```

and for a sheet current:

```math
\widehat{B_z}(k,z_0)
=
{\mu_0\over2} e^{-|k|(z_0-z_l)}
i(k_x\widehat{J_y}-k_y\widehat{J_x}).
```

Thus magnetic inversion is low-pass and depth-attenuated. If:

```math
\|\Sigma^{-1/2}(F_E(s_1)-F_E(s_2))\|_2\le\epsilon,
```

then no algorithm can reliably distinguish \(s_1\) and \(s_2\) under the current
experiment without adding information or restricting the state space correctly.

Therefore the recoverable object is an observable quotient:

```math
\mathcal{S}/\sim_{E,\epsilon},
\qquad
s_1\sim_{E,\epsilon}s_2
\iff
\|F_E(s_1)-F_E(s_2)\|_{\Sigma^{-1}}\le\epsilon.
```

This is why the project should not chase "full current image" as the primary
target. The correct target is:

```text
Which current mechanism claims are forced by magnetic data, and which remain
compatible with multiple mechanisms?
```

## What the E-Series Actually Shows

### E01-E07: Foundation and Operator Gap

E01 verifies canonical ideal Biot-Savart sanity. E02 establishes the
single-plane low-pass/identifiability boundary. E03-E04 show topology-aware
baselines and no-via/return-path failure modes. E05 gives QDM-like stressors
only as proxies. E06-E07 expose multi-fidelity and PyPEEC-domain operator gaps.

Useful conclusion:

```text
The forward and observation boundary is real; same-operator inverse success is
not enough.
```

Not a breakthrough:

```text
No real QDM/NV, no real CAD/GDS, and no external FEM/FastHenry/COMSOL
validation exists.
```

### E08-E13: Graph Hypotheses, Refusal, and Multi-State Signals

E08 supports graph hypothesis and refusal as a better frame than pixel
reconstruction. E09 is only a real-data intake scaffold. E10-E12 generate
PDN/KCL graph distributions and show generated-domain physics-learning closure.
E13 shows multi-height/multi-state can improve generated observability.

Useful conclusion:

```text
Graph/KCL priors and active states are plausible information levers.
```

Not a breakthrough:

```text
The priors are generated or scaffolded. Primary-label correctness is not
mechanism-level explanation. Calibration source remains unresolved.
```

### E14-E18: Layout Scaffold and Physics-Constrained Inverse

E14 creates a simplified layout graph scaffold. E15 creates a four-layer
generated benchmark. E16 gives differentiable Biot-Savart layers. E17 provides
regularized baselines. E18 shows KCL-constrained inversion can reduce KCL
residual to near zero but does not beat the best ridge baseline and still has
dense-via/deep-layer failures.

Useful conclusion:

```text
KCL correctness is necessary, but KCL residual reduction is not current
accuracy or mechanism correctness.
```

Not a breakthrough:

```text
Computation and regularization do not create missing magnetic information.
```

### E19 and E19.2: OBGHI/OQCI Boundary

E19 posterior selection collapses toward broad hypotheses and fails scientific
gates. E19.2 correctly changes the target to consistent sets and claim
intervals, showing single-height H0/H1/H2/H3 ambiguity under the implemented
generated basis.

Useful conclusion:

```text
OQCI is the right epistemic target: report ambiguity instead of falsely choosing
a topology.
```

Not a breakthrough:

```text
The current observation/basis still leaves broad consistent sets.
```

### E20: Active OQCI on the Old Basis

E20 Round 5 pairwise margins are effectively zero:

```text
all pairwise deltas ~ 0
principal angles 0 deg
min Gamma about -0.624
valid disambiguation remains low
```

Useful conclusion:

```text
Active measurement cannot rescue an over-flexible old basis if all hypotheses
share the same observable subspace.
```

Not a breakthrough:

```text
E20 is a formal negative result for that basis/candidate pool.
```

### E21: Operator Gap vs Mechanism Margin

E21 Round 5 reports:

```text
same-operator multibasis accuracy about 0.406
cross-operator accuracy about 0.25
interclass_delta_min about 2.07e-5
operator_shift_radius_max about 8.11e-2
gap_to_margin_ratio about 3915
external_solver_used_in_metrics = false
```

Useful conclusion:

```text
Operator uncertainty dwarfs mechanism margins in this route.
```

Not a breakthrough:

```text
Classifier/scorer improvements cannot overcome an operator gap thousands of
times larger than class separation.
```

### E23: Graph-Hodge Basis

E23 gives a real mathematical advance in representation:

```text
SVD-projected Graph-Hodge KCL residual ~ 1e-15
multi-state H1/H2 raw distance can rise from about 0.007 to about 0.680
```

But Round 5 robust margins fail:

```text
min_gamma_all_pairs about -5695
h1_h2_gamma_hardcase about -2918
certified_pair_rate = 0
```

Useful conclusion:

```text
Graph-Hodge/KCL basis is necessary infrastructure, but raw distance is not a
robust certificate.
```

Not a breakthrough:

```text
The perturbation radius dominates; no robust observable quotient is certified.
```

### E24: Shared Network Profile

E24's theory is strong: replace per-state free currents by one shared
conductance vector:

```math
i_{h,s}(\theta)=C_h(\theta)D_h^T L_h(\theta)^\dagger b_s.
```

But smoke evidence is negative:

```text
truth shared/free residuals ~ 0.097908 / 0.097907
wrong shared/free residuals ~ 0.098019 / 0.098029
all cases multi-consistent
Gamma ~ -0.25 for all tested pairs
```

Useful conclusion:

```text
Shared-network profiling alone did not create enough separation in the current
generated setup.
```

Not a breakthrough:

```text
Only smoke-level output exists, and the residual gaps are about 1e-4.
```

### E25: Calibrated Volume Forward and Rho

E25 is important support evidence because it decomposes operator radius:

```text
recommended rho becomes available
finite-width/volume/multifilament/nuisance budgets are explicit
```

However, the gates are over-lenient. The convergence gate uses:

```python
passed = best_relative_change <= gate
```

while the report also records worst and median. A single converged case can
pass the gate even if median convergence remains poor. The output also shows
large family-dependent rho, including severe four-layer via-return motifs.

Useful conclusion:

```text
E25 is required for future Gamma subtraction.
```

Not a breakthrough:

```text
E25 calibrates uncertainty; it does not by itself separate mechanisms.
```

### E26: Generic Active Port-State Gamma

E26 fails scientific gates:

```text
positive_gamma_rate = 0
greedy/two-step/random/default min gamma = -Infinity in metrics
mean_states_used = 0 in metrics despite intended S_max=4
```

Useful conclusion:

```text
Generic port-state optimization is not enough; state design must be tied to the
right invariant and hard pair.
```

Not a breakthrough:

```text
The metrics contain internal inconsistencies and should be treated as negative
until re-audited.
```

### E27: Edge Schur Signatures

E27 has an exact and valuable formula:

```math
\Delta i_{q,s}
=
{\alpha\,a_q^T\phi_s\over 1+\alpha a_q^T L^\dagger a_q}
\left[e_q-C D^T L^\dagger a_q\right].
```

Sherman-Morrison validation is excellent:

```text
max relative error ~ 1.9e-14
```

But generated magnetic signals are too small:

```text
mean edge signal ~ 0.00237
mean edge gamma ~ -0.0357
positive edge gamma rate = 0
positive pairwise gamma rate ~ 0.000287
truth_in_consistent_set_rate = 0
empty_rate = 1
```

Useful conclusion:

```text
Schur sensitivity is mathematically useful for state design and local
derivatives.
```

Not a breakthrough:

```text
Single-edge magnetic signatures are below calibrated uncertainty.
```

### E28: Transfer-Matrix Observable Invariants

E28 is the strongest positive candidate, not yet a proven breakthrough.

The core object is:

```math
T_{y,h}=A_h C_hD_h^T L_h^\dagger B,
```

the port-to-magnetic transfer matrix. Invariants include column-space
projector and whitened Gram:

```math
P_h=Q_hQ_h^T,
\qquad
\bar G_h=
\operatorname{diag}(G_h)^{-1/2}G_h\operatorname{diag}(G_h)^{-1/2},
\quad
G_h=T_{y,h}^TW^TWT_{y,h}.
```

Promising metrics:

```text
Gram nuisance radius ~ 0.050 vs raw ~ 1.072
Gram rho ratio ~ 0.0468
Gram positive Gamma rate 5/6
critical Gram Gamma rate 2/2
truth-in-consistent rate 1.0
singleton-wrong rate 0
```

Critical caveats:

```text
H1_via vs H2_model_gap remains negative:
  gamma_gram about -0.146
  gamma_raw about -3.88

Raw field already has positive Gamma for 5/6 pairs, so E28 has not yet shown
that Gram is uniquely needed on hard cases.

The reported best_invariant is wrong in the default output:
  projector positive Gamma rate = 0
  gram positive Gamma rate = 0.833
  best_invariant = projector

The code chooses the first max rate in insertion order, so ties with raw and
Gram can select projector even when projector fails.

Scientific gates take max over invariants, so they can pass while the named best
invariant is scientifically invalid.

Nuisance stress is still narrow: height/gain-style generated perturbations, not
full E25 finite-width/registration/PSF/layer-z/external-solver radius.

The layout family appears controlled and generated; no real CAD/GDS, external
solver, or real QDM/NV validation exists.
```

Useful conclusion:

```text
Transfer-matrix Gram invariants are the first genuinely promising mechanism for
shrinking nuisance radius while preserving topology signal.
```

Not yet a breakthrough:

```text
E28 must be re-run with corrected gates, hard-case sweeps, E25 rho, and layout
ensemble before it can be treated as a generated-domain breakthrough.
```

### E29: Rho-Integrated Schur Certificate

E29 is a conservative auditing bridge, and it fails:

```text
positive_conservative_gamma_rate = 0
positive_rss_gamma_rate = 0
pairwise_conservative_gamma_rate = 0
truth_missing_rate = 1
empty_rate = 0.4
calibration/evaluation split discipline = false
```

Useful conclusion:

```text
After rho subtraction, Schur-style local edge signals do not certify.
```

Not a breakthrough:

```text
Local rho was recomputed in E29 rather than cleanly imported from E25, and split
discipline already fails.
```

## Blueprint Review

### Phase 1 OBGHI

The OBGHI blueprint is conceptually correct:

```text
infer only in observable physical subspaces;
use Graph-Hodge/KCL bases;
return posterior/refusal instead of false unique current maps.
```

But the E19/E20 evidence shows that OBGHI with the old basis and residual
posterior is insufficient. The next OBGHI kernel should operate on transfer
operators and invariants, not on raw per-state magnetic images alone.

### Phase 2 R-MF-CTAS

R-MF-CTAS is the right scalable system architecture, but it is premature to
expand proposal/search machinery before the local certificate is correct.
Scaling a non-certified likelihood only creates faster wrong answers.

The immediate minimum slice should be:

```text
transfer-invariant OQCI certificate on generated layout ensembles.
```

Only after that passes should SMC/GNN/delayed-acceptance search matter.

### Phase 3 Q-R-MF-CTAS

The third-phase physics argument is correct:

```text
if the magnetic operator lacks information, only better observation or extra
modalities can change the Fisher information.
```

But real QDM/NV is currently blocked. Therefore Phase 3 should be treated as
the validation/observation escalation path, not the next software-only
breakthrough.

### Phase 4 EV-FAEDA

The industrial FA/EDA framework is the eventual product shape, but it is not
the next research breakthrough. It needs real layout, netlist, measurement,
and FA action data. Without a certified inversion kernel, it is integration
architecture rather than scientific progress.

## Next Breakthrough Direction

The next most likely major breakthrough is:

```text
Transfer-Operator Observable Quotient Current Inversion (T-OQCI)
```

or, in Chinese:

```text
端口-磁场传递算子可观测商反演
```

### Mathematical Core

For topology hypothesis \(h\), graph incidence \(D_h\), conductance
\(C_h(\theta)\), Laplacian:

```math
L_h(\theta)=D_hC_h(\theta)D_h^T.
```

For port-state matrix:

```math
B=[b_1,\ldots,b_S],
\qquad
\mathbf 1^Tb_s=0,
```

network current transfer is:

```math
T_{i,h}(\theta)
=
C_h(\theta)D_h^TL_h(\theta)^\dagger B.
```

Magnetic transfer:

```math
T_{y,h}(\theta,\psi)
=
A_h(\psi)T_{i,h}(\theta).
```

Observed transfer from measured states:

```math
\widehat T_y = YB^\dagger B
```

when state currents are known, or simply \(Y\) if all columns correspond to
known port excitations.

Define a nuisance group:

```math
\mathcal{N}=
\{\text{gain},\text{per-state scale},\text{state mixing},
\text{background},\text{height},\text{registration},\text{PSF},\text{layer z}\}.
```

The invariant \(\Phi\) should quotient the largest nuisance directions while
preserving topology response. The current leading invariant is the whitened
Gram:

```math
\Phi_G(T)=
\operatorname{diag}(T^TW^TWT)^{-1/2}
T^TW^TWT
\operatorname{diag}(T^TW^TWT)^{-1/2}.
```

The consistent set becomes:

```math
\mathcal C_\Phi(\widehat T_y)
=
\left\{
h:
\min_{\theta,\psi\in\Xi}
\|\Phi(\widehat T_y)-\Phi(T_{y,h}(\theta,\psi))\|_2
\le
\tau_h
\right\}.
```

Pairwise hard-case separation:

```math
\delta^\Phi_{hg}(U)
=
\inf_{\theta_h,\theta_g,\psi_h,\psi_g}
\|\Phi(T_{y,h}(\theta_h,\psi_h))
-\Phi(T_{y,g}(\theta_g,\psi_g))\|_2.
```

Robust certificate:

```math
\Gamma^\Phi_{hg}(U)
=
\delta^\Phi_{hg}(U)
-\epsilon^\Phi(U)
-\rho^\Phi_h(U)
-\rho^\Phi_g(U)
-\tau^\Phi_g(U).
```

Active state design:

```math
U^\star
=
\arg\max_{U\in\mathcal U, |U|\le S_{\max}}
\min_{(h,g)\in\mathcal P_{\rm crit}}
\Gamma^\Phi_{hg}(U)
-c(U).
```

The critical pair set must include:

```text
H0/H1, H0/H3, H1/H3, and especially H1/H2.
```

If H1/H2 remains negative, the system must not claim via-vs-model-gap recovery.
It may only claim a coarser quotient such as:

```text
{H1_via, H2_model_gap} vs {H0_no_via, H3_return_path}
```

provided that quotient has positive robust margin.

### Why This Is More Promising Than Other Routes

Pixel inversion is blocked by the Biot-Savart nullspace. Posterior selection on
raw images collapses under broad bases. Free-current OQCI and old-basis active
design have zero pairwise separation. Shared-network residual profiling did not
produce adequate gaps. Single-edge Schur signatures are below uncertainty.

E28 changes the object:

```text
from one magnetic image to the port-to-magnetic response operator.
```

That matters because topology affects how responses co-vary across states. A
Gram invariant can suppress nuisance amplitude/gain variation while preserving
the response geometry induced by the network. This is a real first-principles
lever:

```text
it changes the decision target and the nuisance quotient, not merely the
classifier.
```

### What Must Be Fixed Before Calling It a Breakthrough

The next directive must enforce these corrections.

1. Correct invariant selection.

   The best invariant must be chosen by a lexicographic scientific score:

   ```text
   critical hard-pair positive rate
   then all-pair positive rate
   then min Gamma
   then mean Gamma
   then nuisance radius
   ```

   A projector with zero positive Gamma cannot be called best.

2. Tighten scientific gates.

   Required E28 Round 2 gates:

   ```text
   best_invariant_name_matches_positive_gamma_metric
   best_invariant_min_gamma_reported
   gram_or_selected_invariant_positive_gamma_rate_ge_0_50_on_hard_eval
   h1_h2_boundary_characterized_not_hidden
   raw_easy_advantage_controlled
   selected_invariant_beats_raw_on_hard_pairs
   E25_rho_integrated
   calibration_eval_split_enforced
   layout_family_holdout_enforced
   ```

3. Use E25 rho correctly.

   Do not use only local height/gain stress. Subtract finite-width, volume,
   registration, PSF, layer-z, background, and sensor-height radii. The E25
   convergence gate should be treated skeptically because it passes on best
   relative change, not median or worst-case convergence.

4. Create hard-case sweeps.

   Sweep:

   ```text
   via conductance ratio
   open/model-gap severity
   return enhancement
   via-vs-gap similarity
   standoff
   layer depth
   port count
   state count
   SNR
   finite width
   registration
   ```

   Report phase diagrams:

   ```text
   gamma_gram(h,g) vs topology contrast and rho
   ```

5. Separate quotient claims.

   If H1/H2 remains unseparated, the valid claim is not "via detection." The
   valid claim may be:

   ```text
   a transfer-topology anomaly class is forced, but via vs model-gap remains
   unidentifiable.
   ```

6. Compare raw and invariant fairly.

   Because raw Gamma is already positive for 5/6 E28 pairs, the next run must
   demonstrate invariant value on cases where raw fails or is unstable.

7. Preserve no-leakage protocol.

   Thresholds, rho recommendations, and invariant selection must be determined
   on calibration layouts and evaluated on held-out layout families.

## Concrete Next Research Program

### Round A: E28 Audit Repair

Goal:

```text
Make the certificate mathematically honest.
```

Tasks:

- fix best-invariant selection;
- add gate that fails if reported best invariant has zero positive Gamma;
- split calibration/evaluation layouts;
- mark raw, Gram, projector, differential as separate decision rules;
- report all failures without collapsing them into a max-over-invariants pass.

Expected outcome:

```text
E28 becomes either a valid Gram-only candidate or a documented false positive.
```

### Round B: E28 Hard-Case Layout Ensemble

Goal:

```text
Determine whether Gram invariants survive outside easy contrast.
```

Minimum metrics:

```text
layout_count >= 80
family_holdout_count >= 4
hard_h1_h2_sweep_count >= 50
critical_pair_positive_gamma_rate
hard_eval_min_gamma
truth_in_consistent_set_rate
singleton_wrong_rate
empty_rate
raw_vs_gram_hardcase_delta
```

Pass condition:

```text
Gram or another declared invariant must produce positive Gamma on a meaningful
hard-case quotient after E25 rho subtraction and held-out evaluation.
```

### Round C: Active Gram-State Design

Goal:

```text
Choose port states to maximize the transfer-invariant robust margin, not raw
residual or generic Schur signal.
```

Use Schur voltage-drop states as candidates:

```math
b_q^\star
=
\arg\max_b
{|a_q^TL^\dagger b|\over 1+\alpha a_q^TL^\dagger a_q},
```

but score them by:

```math
\min_{h,g}\Gamma^G_{hg}(U).
```

Expected outcome:

```text
Generic E26 failure is replaced by invariant-targeted active design.
```

### Round D: CAD/External/Real Escalation

Only after generated hard-case Gamma is positive:

- import real or realistic CAD/GDS graph candidates;
- validate a small forward subset with external solver;
- run E09-style real simple-wire/known-via sanity gates if measured data exist;
- keep generated-domain claims separate from real claims.

## The Most Defensible Breakthrough Claim If Round A-C Pass

The valid generated-domain breakthrough claim would be:

```text
For a held-out generated class of multilayer PDN graphs, multi-state
port-to-magnetic transfer Gram invariants produce positive robust observable
quotient margins for specified topology-decision classes after calibrated
operator-radius subtraction, while raw magnetic images and old free-current
OQCI remain ambiguous or unstable.
```

This still cannot claim:

```text
real chip reverse analysis,
real QDM/NV validation,
real CAD/GDS validation,
universal via detection,
or H1/H2 mechanism separation if the H1/H2 Gamma remains negative.
```

## Final Decision

The next major-breakthrough attempt should not open a broad new direction. It
should concentrate on:

```text
E28 transfer-matrix Gram invariant
+ E25 calibrated rho
+ E23 Graph-Hodge/KCL basis
+ E24 shared-network transfer model
+ E27 Schur sensitivity only as active-state proposal
+ OQCI consistent-set/refusal semantics.
```

This is the smallest route that changes a first-principles object enough to
possibly shrink the magnetic equivalence class:

```text
not a better image,
not a stronger classifier,
but a robust invariant over the excitation-to-field operator.
```

If that route fails after hard-case rho-integrated evaluation, then the next
true breakthrough cannot be software-only. It must move to Phase 3:

```text
better observation physics: real multi-height/vector/NV/frequency/differential
measurements or external solver/real calibration data.
```

