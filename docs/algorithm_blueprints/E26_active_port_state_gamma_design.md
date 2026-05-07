# E26 Active Port-State Gamma Design

Status: top-level algorithm directive for Claude worker, not evidence.

Target evidence package:

```text
experiments/evidence/E26_active_port_state_gamma_design/
```

Affected claims:

- `C02_single_plane_identifiability_boundary`
- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`
- `C13_calibration_protocol_reality`

Do not edit global research graph files.

## 0. Why E26 Exists

E23 showed that port-feasible multi-state excitation can dramatically increase
H1/H2 distance in generated layouts. E24 will test whether shared-network
profile constraints create true topology separability. E26 asks a different
question:

```text
Which port states should be measured to maximize certified robust margin per
measurement cost?
```

This cannot be left to ad hoc state choices. The state design must optimize the
same certificate used for claims.

## 1. Feasible Port-State Set

Let `p` be the number of accessible ports. A port excitation is:

```math
b\in R^p,\qquad \mathbf{1}^T b=0.
```

Hardware constraints:

```math
\|b\|_1\le 2I_{\max},\qquad
|b_j|\le I_{\max,j},\qquad
b_j=0\text{ for inaccessible ports}.
```

Candidate set:

```math
\mathcal{U}_1
=
\{e_a-e_b: a,b\in\mathcal{P},a\ne b\}
\cup
\{\text{balanced multi-source/multi-sink patterns}\}.
```

A measurement design is:

```math
U=[b_1,\ldots,b_S].
```

Cost:

```math
c(U)=
\alpha S
+\beta\sum_s \|b_s\|_0
+\gamma\sum_s \|b_s\|_2^2
+c_{\text{switch}}(U).
```

## 2. Objective: Robust Profile Margin

For topology pair `(h,g)`, use a profile margin:

```math
\Gamma_{hg}(U)
=
\delta^{profile}_{hg}(U)
-\tau_g(U)
-\epsilon(U)
-\rho_h(U)-\rho_g(U).
```

If E24-style network solving is implemented locally:

```math
\delta^{profile}_{hg}(U)
=
\inf_{\theta_h,\theta_g}
\|W[F_h(U,\theta_h)-F_g(U,\theta_g)]\|_2.
```

If full profiling is too expensive, use a conservative proxy:

```math
\Gamma^{proxy}_{hg}(U)
=
\Delta r^{shared}_{h,g}(U)-\epsilon-\rho_h-\rho_g.
```

The minimax design:

```math
U^\star
=
\arg\max_{U\subset\mathcal{U}_1,|U|\le S_{\max}}
\min_{(h,g)\in\mathcal{P}_{crit}}
\Gamma_{hg}(U)
-c(U).
```

Critical pairs must include:

```text
via vs return
via vs open/model-gap
deep-layer route vs shallow return
nominal vs parasitic return
```

## 3. Greedy and Lookahead Algorithms

Greedy state selection:

```math
b_{k+1}
=
\arg\max_{b\in\mathcal{U}_1\setminus U_k}
\left[
\min_{(h,g)\in\mathcal{P}_{crit}}
\Gamma_{hg}(U_k\cup\{b\})
-
\min_{(h,g)\in\mathcal{P}_{crit}}
\Gamma_{hg}(U_k)
-
c(b)
\right].
```

Two-step lookahead:

```math
(b_{k+1},b_{k+2})
=
\arg\max_{b,b'}
\min_{(h,g)}
\Gamma_{hg}(U_k\cup\{b,b'\})
-c(b)-c(b').
```

Entropy or consistent-set utility for comparison:

```math
\Delta H(b)
=
H(\mathcal{C}(Y_U))-E_{Y_b|Y_U}H(\mathcal{C}(Y_U,Y_b)).
```

Do not let entropy replace robust margin; it is only a secondary comparison.

## 4. Identifiability Diagnostics

For every selected state, report how it changes:

```text
effective_resistance_between_ports
current_path_overlap
edge_current_correlation_between_hypotheses
profile_delta_by_pair
profile_gamma_by_pair
consistent_set_size
truth_missing_rate
wrong_accept_rate
```

Current-path overlap for topologies `h,g` under state `b`:

```math
\operatorname{overlap}_{hg}(b)
=
{|\langle i_h(b),i_g(b)\rangle|
\over
\|i_h(b)\|_2\|i_g(b)\|_2+\epsilon}.
```

A good state should reduce overlap for critical pairs.

## 5. Baselines

Compare:

```text
single_default_state
all_pairwise_port_states
random_states_fixed_seed
max_current_norm_states
max_effective_resistance_contrast_states
greedy_gamma_states
two_step_gamma_states
oracle_truth_margin_states
```

Oracle is allowed only as an upper-bound diagnostic and must be marked
nondeployable.

## 6. Sequential Refusal Policy

After each added state `k`, compute:

```math
\mathcal{C}_k(Y)
=
\{h:r_h(Y_{1:k})\le\tau_h\}.
```

Stop if:

```math
|\mathcal{C}_k|=1
\quad\text{and}\quad
\min_{g\ne \hat h}\Gamma_{\hat h g}(U_k)>0.
```

Refuse if:

```math
k=S_{\max}
\quad\text{and}\quad
\min_{h,g}\Gamma_{hg}(U_k)\le0.
```

Report expected state count:

```math
E[S_{\text{used}}].
```

## 7. Minimum Implementation Slice

Implement self-contained generated networks. It is acceptable to use a compact
E24-like network model locally, but keep package independent.

Minimum:

```text
layout_count >= 24
port_count range 3..8
candidate_state_count >= 12
max_selected_states >= 4
hypothesis_count >= 4
```

## 8. Acceptance Gates

Engineering gates:

```text
package_runs_to_completion
feasible_port_states_generated
state_constraints_satisfied
greedy_gamma_implemented
two_step_or_lookahead_implemented
baselines_implemented
sequential_refusal_reported
reports_written
generated_domain_boundary_explicit
```

Scientific gates:

```text
greedy_gamma_beats_random_by_0_10
greedy_gamma_beats_default
two_step_beats_greedy_or_ties
critical_pair_gamma_improves_with_states
wrong_accept_rate_decreases_with_states
truth_missing_rate_le_0_10
mean_states_used_le_smax
positive_gamma_rate_ge_0_50
```

If positive Gamma cannot be achieved, the worker must identify whether the
limiter is:

```text
state set too weak
network model too flexible
operator rho too large
topology hypotheses too similar
measurement noise too large
```

## 9. Required Outputs

Write:

```text
outputs/RUN_REPORT.md
outputs/PORT_STATE_FEASIBILITY_AUDIT.md
outputs/GREEDY_GAMMA_SELECTION.md
outputs/TWO_STEP_LOOKAHEAD_AUDIT.md
outputs/STATE_BASELINE_COMPARISON.md
outputs/SEQUENTIAL_REFUSAL_POLICY.md
outputs/CRITICAL_PAIR_STATE_DIAGNOSTICS.md
outputs/FAILURE_MODES.md
outputs/metrics.json
```

## 10. Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## 11. Final Claude Report

Report:

- feasible state set and constraints;
- selected greedy and two-step states;
- baseline comparison;
- critical pair Gamma trajectory as states are added;
- wrong-accept/truth-missing/consistent-set metrics;
- sequential refusal behavior;
- all gates;
- failure modes;
- cannot_claim;
- next required evidence;
- files changed.

