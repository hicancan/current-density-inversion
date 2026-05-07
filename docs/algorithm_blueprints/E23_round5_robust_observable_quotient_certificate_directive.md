# E23 Round 5 Directive: Robust Observable-Quotient Certificate

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e23-graph-hodge`
- previous session: `19e97ba9-2b0d-406e-95f9-f8c5eafb15d4`

## Mathematical Objective

Round 4 showed a strong generated-domain signal:

```text
H1/H2 1-state distance on four_layer_pdn: 0.006987
H1/H2 multi-state distance: 0.680306
finite-width/operator-stress gain remains about 0.67
port-feasible states provide the gain
```

Round 5 must convert this from a distance observation into a robust
observable-quotient certificate.

For hypothesis `h`, stacked observation `Y`, excitation design `U`, and
regularized manifold:

```math
\mathcal{M}_h(U)
= \{a_h(U)+B_h(U)\theta:\theta\in\Theta_h\},
```

define:

```math
d_h(Y)^2
=
\min_\theta
\|W(Y-a_h-B_h\theta)\|_2^2
+\lambda\|L_h\theta\|_2^2 .
```

For two hypotheses `h,g`, define affine pair separation:

```math
\delta_{hg}(U)^2
=
\min_{\theta_h,\theta_g}
\|W[(a_h-a_g)+B_h\theta_h-B_g\theta_g]\|_2^2 .
```

Let the empirical noise radius be `epsilon`, and let operator perturbation
radii be:

```math
\rho_h(U)
=
\max_{\Delta A\in\mathcal{D}}
\max_{i\in\mathcal{I}_h(U),\|i\|\le R_h}
\|W\Delta A i\|_2 .
```

The robust margin is:

```math
\Gamma_{hg}(U)
=
\delta_{hg}(U)
-\tau_g
-\epsilon
-\rho_h(U)-\rho_g(U).
```

Round 5 passes only if the hard H1/H2 pair has positive `Gamma` under
port-feasible excitation and finite-width/operator perturbation.

## Required Scope

Implement only inside:

```text
experiments/evidence/E23_cad_gds_graph_hodge_basis/
```

Do not edit global research graph files.

## Required Changes

### 1. Robust Margin Matrix

For every layout, operator, and protocol, compute all pairwise margins:

```text
H0/H1, H0/H2, H0/H3, H1/H2, H1/H3, H2/H3
```

Report:

```text
pair
delta_pair
tau_pair
epsilon_noise
rho_h
rho_g
gamma_pair
gamma_positive
wrong_accept
truth_missing
```

Use conservative defaults if no calibrated noise is present:

```text
epsilon_noise = tight_epsilon used by OQCI
tau_pair = acceptance threshold for the wrong hypothesis
rho_h,rho_g = maximum observed perturbation residual across stress ladder
```

The output must include:

```text
min_gamma_all_pairs
min_gamma_critical_pairs
h1_h2_gamma_hardcase
certified_pair_rate
certified_critical_pair_rate
```

### 2. Layout Ensemble Scaling

Round 4 had only two layouts, and the simple layout cannot benefit from
multi-state. Add a deterministic generated ensemble of multi-port PDN-like
graphs, still clearly marked generated-domain.

Minimum target:

```text
layout_ensemble_count >= 40
multiport_layout_count >= 30
seed fixed
```

Each layout should vary at least:

```text
number of ports
number of layers
via/return placement
mesh density
loop/cycle count
source/sink geometry
```

For every layout, compute:

```text
h1_h2_delta_1state
h1_h2_delta_multistate
h1_h2_gamma_1state
h1_h2_gamma_multistate
h1_h2_gamma_gain
h1_h2_wrong_accept_1state
h1_h2_wrong_accept_multistate
```

### 3. Port-Excitation Optimization

Implement a deterministic greedy excitation selector over feasible port states.

Feasible states satisfy:

```math
{\bf 1}^T b_s = 0,\qquad \|b_s\|_1 \le I_{\max},
```

and use only external ports, not internal via actuation.

Greedy objective:

```math
b_{k+1}
=
\arg\max_{b\in\mathcal{U}_1}
\min_{(h,g)\in\mathcal{P}_{crit}}
\Gamma_{hg}([b_1,\ldots,b_k,b])
-\alpha k .
```

Compare:

```text
baseline_default_states
greedy_margin_states
random_feasible_states_fixed_seed
ideal_internal_states
```

Report selected states and their port injection vectors.

### 4. Adversarial Perturbation Stress

The existing perturbation ladder is deterministic. Add a small adversarial or
randomized stress set:

```text
finite_width_scale in {0.5, 1.0, 2.0}
registration_sigma in {0.05, 0.10, 0.20}
deep_layer_shift in {25um, 50um, 100um}
sensor_height_error in {0, 25um, 50um}
noise_seed_count >= 10
```

Compute worst-case:

```text
rho_pair_worst
gamma_pair_worst
h1_h2_gamma_worst
wrong_accept_rate_worst
truth_missing_rate_worst
empty_rate_worst
```

### 5. Breakthrough Gates

Add these Round 5 gates:

```text
layout_ensemble_count_ge_40
multiport_layout_count_ge_30
h1_h2_hardcase_gamma_positive
h1_h2_gamma_positive_rate_ge_0_90
critical_pair_certified_rate_ge_0_80
greedy_port_states_beat_default
greedy_port_states_beat_random
adversarial_h1_h2_gamma_positive
adversarial_wrong_accept_rate_le_0_10
adversarial_truth_missing_rate_le_0_10
no_internal_actuation_needed
```

Do not call this real validation even if all gates pass.

## Required Outputs

Add:

```text
outputs/ROBUST_MARGIN_MATRIX.md
outputs/LAYOUT_ENSEMBLE_SCALING_AUDIT.md
outputs/GREEDY_PORT_EXCITATION_AUDIT.md
outputs/ADVERSARIAL_OPERATOR_STRESS_AUDIT.md
outputs/ROUND5_ROBUST_CERTIFICATE_GATE_AUDIT.md
```

Update metrics JSON with all Round 5 keys.

## Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## Final Report

Report:

- robust margin matrix summary;
- H1/H2 hardcase `delta`, `rho`, and `gamma`;
- layout ensemble pass/fail rates;
- greedy port-excitation states and improvement;
- adversarial perturbation worst-case metrics;
- all Round 5 gates;
- failure modes;
- cannot_claim;
- next required evidence.

