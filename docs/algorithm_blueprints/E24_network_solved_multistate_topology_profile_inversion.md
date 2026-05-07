# E24 Network-Solved Multi-State Topology Profile Inversion

Status: top-level algorithm directive for Claude worker, not evidence.

Target evidence package:

```text
experiments/evidence/E24_network_solved_multistate_topology_profile_inversion/
```

Affected claims:

- `C02_single_plane_identifiability_boundary`
- `C04_inverse_crime_and_operator_gap`
- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`

Do not edit global research graph files. This package is generated-domain only
until independently integrated and audited.

## 0. Why E24 Exists

E19/E19.2 showed that OQCI consistent sets remain ambiguous when hypothesis
current bases are too free. E20 showed that adding height/component/state rows
to the old linear basis leaves all pairwise deltas at zero. E21 showed that
classifier strength cannot overcome an operator gap larger than mechanism
margins. E23 produced the strongest positive signal, but Round 5 could not
certify robust margin:

```math
\Gamma_{hg}=\delta_{hg}-\tau-\epsilon-\rho_h-\rho_g < 0 .
```

The failure mode is now precise:

```text
KCL-compatible current spaces are still too expressive. Wrong hypotheses can
adjust state-specific nullspace currents to mimic the truth. A breakthrough
requires tying every excitation state to one shared physical network.
```

E24 therefore changes the inverse variable from arbitrary currents to a shared
conductance network.

## 1. Mathematical Object

For topology hypothesis `h`, define a directed circuit graph:

```math
G_h=(V_h,E_h),\qquad D_h\in\{-1,0,1\}^{|V_h|\times |E_h|}.
```

Each edge `e` has conductance:

```math
c_e = \exp(\theta_e),\qquad C_h(\theta)=\operatorname{diag}(c_e).
```

The weighted graph Laplacian is:

```math
L_h(\theta)=D_h C_h(\theta)D_h^T.
```

For excitation state `s`, port injection vector `b_s` obeys:

```math
\mathbf{1}^T b_s=0,\qquad \|b_s\|_1\le I_{\max}.
```

Network potentials solve:

```math
L_h(\theta)\phi_{h,s}=b_s,
```

with gauge fixed by one grounded node or by the Moore-Penrose solution:

```math
\phi_{h,s}=L_h(\theta)^\dagger b_s,\qquad \mathbf{1}^T\phi_{h,s}=0.
```

Edge currents are not free:

```math
i_{h,s}(\theta)
=C_h(\theta)D_h^T\phi_{h,s}.
```

They automatically satisfy KCL:

```math
D_h i_{h,s}(\theta)=b_s.
```

Magnetic observation:

```math
y_s=A_h(\xi)i_{h,s}(\theta)+\eta_s,
```

where `xi` denotes forward nuisance parameters: finite width, sensor height,
registration, layer z, blur, and background.

Stacked multi-state forward:

```math
F_h(U,\theta,\xi)
=
\begin{bmatrix}
A_h(\xi)i_{h,1}(\theta)\\
\vdots\\
A_h(\xi)i_{h,S}(\theta)
\end{bmatrix},
\qquad
U=[b_1,\ldots,b_S].
```

## 2. Core Breakthrough Hypothesis

The testable hypothesis is:

```text
There exist generated chip-like topologies and feasible port-state designs U
such that wrong topologies cannot use one shared conductance vector theta to
simultaneously fit all magnetic states, even when each wrong topology can fit
individual states or free KCL currents.
```

Formally, truth `h` and wrong topology `g` are profile-separated if:

```math
\delta^{profile}_{h\to g}(U)
=
\inf_{\theta_h,\theta_g,\xi_h,\xi_g}
\left\|
W\left[
F_h(U,\theta_h,\xi_h)-F_g(U,\theta_g,\xi_g)
\right]
\right\|_2
>0.
```

The nuisance variables must be bounded:

```math
\xi\in\Xi
=
\{|\Delta z|\le z_{\max},\|\Delta r\|\le r_{\max},
w\in[w_{\min},w_{\max}],\ldots\}.
```

If full nuisance profiling is too expensive, use a conservative two-level
certificate:

```math
\delta^{profile}_{hg}(U)
=
\inf_{\theta_h,\theta_g}
\|W[F_h(U,\theta_h,0)-F_g(U,\theta_g,0)]\|_2,
```

and subtract empirical nuisance radius:

```math
\Gamma_{hg}(U)
=
\delta^{profile}_{hg}(U)
-\epsilon_{\text{noise}}
-\rho_h(U)-\rho_g(U).
```

Round E24 succeeds only if the shared-network profile margin becomes positive
where the free-current margin was zero or negative.

## 3. Why Shared Conductance Can Break Degeneracy

Free KCL model:

```math
\mathcal{I}^{free}_{h,s}=i^0_{h,s}+N_h z_{h,s}.
```

Because `z_{h,s}` is independent for every state, the stacked manifold is:

```math
\mathcal{M}^{free}_h(U)
=
\prod_{s=1}^S A_h(i^0_{h,s}+N_h z_{h,s}).
```

This product is large. Wrong hypotheses can adapt separately per state.

Network-solved model:

```math
\mathcal{M}^{net}_h(U)
=
\{F_h(U,\theta,\xi):\theta\in\Theta_h,\xi\in\Xi_h\}.
```

The same `theta` explains every state. Thus:

```math
\dim \mathcal{M}^{net}_h(U)
\ll
\sum_s \dim \mathcal{I}^{free}_{h,s}.
```

The breakthrough mechanism is cross-state consistency:

```math
\exists \{i_s\}_{s=1}^S \text{ fitting }Y
\;\not\Rightarrow\;
\exists \theta \text{ such that } i_s=C(\theta)D^T L(\theta)^\dagger b_s
\;\forall s.
```

Claude must explicitly report the gap between:

```text
free_kcl_fit
per_state_network_fit
shared_network_fit
```

This is the decisive diagnostic.

## 4. Topology Hypotheses Must Truly Change the Graph

Do not implement H0/H1/H2/H3 as only edge-current scaling on one common graph.
Each hypothesis must change at least one of:

```text
D_h
E_h
port connectivity
via edge set
return path edge set
layer coupling
cycle space dimension
source-to-sink effective resistance
```

Minimum hypothesis set:

```text
H0: nominal no-defect / baseline topology
H1: via/vertical interconnect present or restored
H2: open/missing segment/model-gap topology
H3: alternative return-path or parasitic return topology
```

For each pair, report graph invariants:

```text
node_count
edge_count
component_count
cycle_rank = |E|-|V|+component_count
port_count
via_edge_count
return_edge_count
effective_resistance_matrix_between_ports
nullspace_dim = dim ker D_int
```

If hypotheses share all invariants and all edges, the package must fail fast:

```text
topology_not_changed = true
```

## 5. Profile Objective

For generated truth `Y`, fit topology `h` by:

```math
J_h(\theta)
=
\sum_{s=1}^S
\|W_s(y_s-A_h i_{h,s}(\theta))\|_2^2
\lambda_\theta \|\theta-\theta_0\|_2^2
\lambda_{\Delta}\|R\theta\|_2^2 .
```

Use log conductance `theta` to enforce positivity. `R` may be a graph smoothness
or edge-role prior.

Profile residual:

```math
r_h^{shared}(Y,U)=\min_\theta J_h(\theta)^{1/2}.
```

Free KCL lower bound:

```math
r_h^{free}(Y,U)
=
\min_{\{z_s\}}
\left[
\sum_s
\|W_s(y_s-A_h(i^0_{h,s}+N_h z_s))\|_2^2
\right]^{1/2}.
```

The key expected pattern for a successful E24 case is:

```math
r_g^{free}\approx r_h^{free}
\quad\text{but}\quad
r_g^{shared}\gg r_h^{shared}.
```

Define:

```math
\Delta^{shared}_{h,g}
= r_g^{shared}(Y_h,U)-r_h^{shared}(Y_h,U).
```

and normalized ratio:

```math
R^{shared}_{h,g}
= {r_g^{shared}+\epsilon \over r_h^{shared}+\epsilon}.
```

## 6. Accepted Set and Refusal

The network-profile accepted set is:

```math
\mathcal{C}_{net}(Y)
=
\{h:r_h^{shared}(Y,U)\le \tau_h\}.
```

Truth is safe only if:

```math
h^\star\in\mathcal{C}_{net}(Y)
```

and wrong topologies are rejected:

```math
\mathcal{C}_{net}(Y)\subseteq [h^\star].
```

Report:

```text
truth_in_consistent_set_rate
empty_rate
singleton_correct_rate
singleton_wrong_rate
multi_consistent_rate
accepted_accuracy
accepted_risk
```

Do not reward empty sets as disambiguation.

## 7. Robust Margin

Estimate operator/nuisance radius using at least the same stress classes as E23:

```text
finite_width
registration_gap
deep_layer_shift
sensor_height_error
noise
```

For topology `h`:

```math
\rho_h(U)
=
\max_{\xi\in\Xi}
\|W[F_h(U,\hat{\theta}_h,\xi)-F_h(U,\hat{\theta}_h,0)]\|_2 .
```

Pairwise robust profile margin:

```math
\Gamma^{profile}_{h,g}(U)
=
\delta^{profile}_{h,g}(U)
-\tau_g
-\epsilon_{\text{noise}}
-\rho_h(U)-\rho_g(U).
```

If computing `delta_profile` directly is hard, use truth-generated residual gap:

```math
\widetilde{\Gamma}_{h\to g}(U)
=
r_g^{shared}(Y_h,U)-r_h^{shared}(Y_h,U)
-\epsilon_{\text{noise}}
-\rho_h(U)-\rho_g(U).
```

Mark surrogate margins clearly.

## 8. Minimum Implementation Slice

Implement a self-contained generated package. Reuse local patterns, but keep all
edits under the E24 evidence package.

Minimum:

```text
layout_count >= 24
multiport_layout_count >= 16
state_count in {1,2,4}
hypothesis_count >= 4
operator_stress_count >= 4
```

Use CPU by default. No deep learning required.

Recommended modules:

```text
src/graphs.py
src/network_solve.py
src/forward.py
src/profile_fit.py
src/margins.py
src/run_all.py
tests/
configs/smoke.json
configs/default.json
```

## 9. Acceptance Gates

Engineering gates:

```text
package_runs_to_completion
all_layouts_parse
network_kcl_residual_below_tolerance
conductances_positive
topology_hypotheses_change_graph
multi_state_shared_theta_implemented
free_kcl_baseline_implemented
operator_stress_executed
reports_written
generated_domain_boundary_explicit
```

Scientific gates:

```text
shared_network_beats_free_kcl_wrong_topology
shared_network_reduces_consistent_set_size
truth_in_consistent_set_rate_ge_0_90
singleton_wrong_rate_eq_0
empty_rate_le_0_10
h1_h2_shared_profile_gap_positive_rate_ge_0_80
critical_pair_profile_gamma_positive_rate_ge_0_50
operator_stress_gamma_positive_rate_ge_0_30
```

If scientific gates fail, preserve the result as a boundary theorem.

## 10. Required Outputs

Write:

```text
outputs/RUN_REPORT.md
outputs/NETWORK_MODEL_DERIVATION.md
outputs/TOPOLOGY_GRAPH_INVARIANTS.md
outputs/FREE_KCL_VS_SHARED_NETWORK_AUDIT.md
outputs/PROFILE_RESIDUAL_MATRIX.md
outputs/CONSISTENT_SET_AUDIT.md
outputs/ROBUST_PROFILE_MARGIN_AUDIT.md
outputs/FAILURE_MODES.md
outputs/metrics.json
```

`NETWORK_MODEL_DERIVATION.md` must include the formulas from this directive in
the package's notation.

## 11. Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

If package-local requirements are not needed, create a minimal requirements
file and still use `uv run --with-requirements requirements.txt`.

## 12. Final Claude Report

Report:

- graph topology changes and invariants;
- KCL residuals and positivity checks;
- free KCL vs shared-network residuals;
- profile residual matrix;
- consistent-set metrics;
- H1/H2 and all critical pair profile margins;
- operator stress margins;
- all gates;
- failure modes;
- cannot_claim;
- next required evidence;
- files changed.

