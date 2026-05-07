# E27 Edge-Defect Schur Magnetic Signature Inversion

Status: top-level algorithm directive for Claude worker, not evidence.

Target evidence package:

```text
experiments/evidence/E27_edge_defect_schur_magnetic_signature/
```

Affected claims:

- `C02_single_plane_identifiability_boundary`
- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`
- `C13_calibration_protocol_reality`

Do not edit global research graph files.

## 0. Motivation from E24/E25/E26

E24 implemented shared-conductance network profile inversion, but smoke margins
remain negative. The H1/H2 profile gaps are only `~1e-4`, while robust penalties
are much larger. E26 showed active port selection fails when it treats states
as generic port pairs rather than optimizing candidate-defect sensitivity. E25
showed the operator radius can be calibrated and decomposed, so future Gamma
certificates should use physically justified `rho`.

The next breakthrough attempt must exploit the exact perturbation structure of
network topology changes. A via, open, missing return, or parasitic return is
not an arbitrary new topology: it is an edge insertion, deletion, or conductance
change. Those have closed-form first-order and rank-one formulas.

## 1. Base Network and Candidate Edge Perturbation

Let the baseline graph have incidence matrix:

```math
D\in\mathbb{R}^{|V|\times |E|},
\qquad
C=\operatorname{diag}(c_e),
\qquad
L=DC D^T.
```

For port state `b_s`:

```math
L\phi_s=b_s,\qquad i_s=C D^T\phi_s.
```

Consider a candidate defect edge `q` with incidence vector:

```math
a_q=e_u-e_v.
```

Adding or changing conductance by `\alpha` gives:

```math
L_\alpha=L+\alpha a_q a_q^T.
```

For an open/removal of existing edge `q`, use negative perturbation:

```math
\alpha=-c_q
```

when the resulting Laplacian remains connected after gauge fixing.

The perturbed potential is:

```math
\phi_s(\alpha)
=
(L+\alpha a_q a_q^T)^\dagger b_s.
```

With a grounded or projected Laplacian inverse `G=L^\dagger`, the
Sherman-Morrison formula gives:

```math
\phi_s(\alpha)
=
\phi_s
-
{\alpha\,G a_q\,a_q^T\phi_s
\over
1+\alpha\,a_q^T G a_q}.
```

Define candidate-edge voltage drop:

```math
v_{q,s}=a_q^T\phi_s.
```

Define effective resistance across candidate endpoints:

```math
R_q=a_q^T G a_q.
```

Then:

```math
\Delta\phi_s
=
\phi_s(\alpha)-\phi_s
=
-
{\alpha\,v_{q,s}\over 1+\alpha R_q}
G a_q.
```

This formula is the core of E27.

## 2. Current Perturbation Signature

Existing-edge current perturbation:

```math
\Delta i_s^{old}
=
C D^T\Delta\phi_s
=
-
{\alpha\,v_{q,s}\over 1+\alpha R_q}
C D^T G a_q.
```

New candidate-edge current:

```math
i_{q,s}^{new}(\alpha)
=
\alpha a_q^T\phi_s(\alpha)
=
{\alpha\,v_{q,s}\over 1+\alpha R_q}.
```

Therefore the full edge-current perturbation is:

```math
\Delta i_{q,s}
=
{\alpha\,v_{q,s}\over 1+\alpha R_q}
\left[
e_q - C D^T G a_q
\right],
```

where `e_q` is included only if the candidate edge is represented in the
augmented edge set.

The magnetic perturbation signature:

```math
\Delta y_{q,s}
=
A\,\Delta i_{q,s}.
```

Stacking states:

```math
\Delta Y_q(U)
=
\begin{bmatrix}
\Delta y_{q,1}\\
\vdots\\
\Delta y_{q,S}
\end{bmatrix}.
```

The expected signal energy is:

```math
S_q(U)
=
\|W\Delta Y_q(U)\|_2.
```

The robust edge-defect certificate is:

```math
\Gamma_q(U)
=
S_q(U)-\epsilon-\rho_q(U)-\tau.
```

E27 succeeds only if candidate defects have positive `Gamma_q` under generated
conditions and calibrated E25-style `rho`.

## 3. State Design from Schur Sensitivity

Because:

```math
\Delta y_{q,s}
\propto
{v_{q,s}\over 1+\alpha R_q},
```

a good port state maximizes endpoint voltage drop across the candidate edge:

```math
b^\star_q
=
\arg\max_{b\in\mathcal{U}_1}
{|a_q^T L^\dagger b|\over 1+\alpha a_q^T L^\dagger a_q}.
```

For multiple critical candidate defects `Q_crit`, use minimax:

```math
U^\star
=
\arg\max_U
\min_{q\in Q_{crit}}
\Gamma_q(U)-c(U).
```

Compare against generic E26 greedy-gamma states. The expected breakthrough is
not more states; it is states targeted to candidate-edge voltage drops.

## 4. Pairwise Defect Discrimination

Two candidate defects `q` and `r` are distinguishable if:

```math
\Delta_{qr}(U)
=
\|W[\Delta Y_q(U)-\Delta Y_r(U)]\|_2
```

exceeds uncertainty:

```math
\Gamma_{qr}(U)
=
\Delta_{qr}(U)
-\epsilon
-\rho_q(U)-\rho_r(U)
-\tau
>0.
```

Report:

```text
edge_signal_energy
edge_gamma
pairwise_defect_delta
pairwise_defect_gamma
positive_edge_gamma_rate
positive_pairwise_gamma_rate
```

## 5. Candidate Families

Minimum candidate defects:

```text
via insertion
via removal/open
return-path insertion
return-path removal
local open segment
parasitic short/bridge
deep-layer alternate return
```

Each candidate must specify:

```text
edge endpoints
layer ids
edge role
alpha range
effective resistance R_q
baseline voltage drop distribution over states
```

## 6. Forward Model

Use an edge-segment Biot-Savart forward, not a coarse grid-cell current map.
At minimum:

```math
B_e(r_m)
=
{\mu_0 I_e\over4\pi}
\int_0^1
{t_e\times(r_m-r_e(t))\over\|r_m-r_e(t)\|^3}
\ell_e\,dt.
```

Use quadrature along each segment. Optionally add finite-width approximation
using E25-style multifilament.

## 7. Baselines

Compare:

```text
generic random port states
E26 greedy-gamma states
max current norm states
max effective resistance contrast states
Schur voltage-drop states
Schur minimax states
oracle best states
```

Oracle is a nondeployable upper bound.

## 8. Acceptance Gates

Engineering gates:

```text
package_runs_to_completion
laplacian_solve_valid
sherman_morrison_matches_direct_solve
candidate_edge_families_generated
edge_segment_forward_runs
schur_state_design_implemented
baselines_implemented
reports_written
generated_domain_boundary_explicit
```

Scientific gates:

```text
schur_states_beat_random_signal_by_2x
schur_states_beat_e26_generic_gamma
positive_edge_gamma_rate_ge_0_50
positive_pairwise_defect_gamma_rate_ge_0_30
via_return_pair_gamma_positive_rate_ge_0_50
truth_in_consistent_set_rate_ge_0_90
singleton_wrong_rate_eq_0
empty_rate_le_0_10
```

If all scientific gates fail, preserve as a negative theorem: candidate-edge
magnetic signatures are below calibrated uncertainty for the generated setup.

## 9. Required Outputs

Write:

```text
outputs/RUN_REPORT.md
outputs/SCHUR_DERIVATION.md
outputs/SHERMAN_MORRISON_VALIDATION.md
outputs/CANDIDATE_EDGE_SENSITIVITY_TABLE.md
outputs/SCHUR_STATE_DESIGN_AUDIT.md
outputs/EDGE_DEFECT_SIGNATURES.md
outputs/PAIRWISE_DEFECT_GAMMA_MATRIX.md
outputs/CONSISTENT_SET_AUDIT.md
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

- Schur/Sherman-Morrison validation error;
- candidate edge sensitivity statistics;
- selected Schur states;
- signal and Gamma improvement over baselines;
- pairwise defect Gamma matrix;
- consistent-set metrics;
- all gates;
- failure modes;
- cannot_claim;
- next required evidence;
- files changed.

