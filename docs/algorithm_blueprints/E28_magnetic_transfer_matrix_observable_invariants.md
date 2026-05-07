# E28 Magnetic Transfer-Matrix Observable Invariants

Status: top-level algorithm directive for Claude worker, not evidence.

Target evidence package:

```text
experiments/evidence/E28_magnetic_transfer_matrix_observable_invariants/
```

Affected claims:

- `C02_single_plane_identifiability_boundary`
- `C04_inverse_crime_and_operator_gap`
- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`

Do not edit global research graph files.

## 0. Motivation

E24/E26 optimized raw profile residuals and state-level Gamma. The remaining
issue is scale and forward-model nuisance: global current scale, sensor gain,
background, and common-mode operator errors can dominate small topology
signals.

E28 changes the object from individual magnetic images to the magnetic transfer
matrix induced by port excitations. The goal is to find topology-sensitive
invariants that cancel nuisance directions.

## 1. Linear Network Response

For fixed topology and conductance:

```math
i_s=C D^T L^\dagger b_s.
```

Let `B=[b_1,\ldots,b_S]`. The edge-current transfer matrix is:

```math
T_i
=
C D^T L^\dagger B.
```

Magnetic transfer matrix:

```math
T_y
=
A T_i
=
A C D^T L^\dagger B.
```

Observed stacked data `Y` under known port-state matrix `B` estimates `T_y`.

If `B` spans the accessible port subspace:

```math
T_y \approx Y B^\dagger B
```

or simply `T_y=Y` when columns are measured states.

## 2. Nuisance-Invariant Representations

### 2.1 Column-Space Projector

Topology can alter the subspace spanned by magnetic responses:

```math
\mathcal{S}_h=\operatorname{col}(T_{y,h}).
```

Use the orthogonal projector:

```math
P_h=Q_h Q_h^T,\qquad Q_h=\operatorname{orth}(W T_{y,h}).
```

Projector distance:

```math
d_P(h,g)
=
\|P_h-P_g\|_F/\sqrt{2}.
```

This is invariant to invertible mixing of measured states and global scale.

### 2.2 Whitened Gram Matrix

Response covariance:

```math
G_h=T_{y,h}^T W^T W T_{y,h}.
```

Normalize:

```math
\bar{G}_h
=
{\operatorname{diag}(G_h)^{-1/2}G_h\operatorname{diag}(G_h)^{-1/2}}.
```

Distance:

```math
d_G(h,g)=\|\bar{G}_h-\bar{G}_g\|_F.
```

This cancels per-state amplitude scale.

### 2.3 Differential Common-Mode Cancellation

For a reference state `s0`:

```math
\Delta y_s=y_s-y_{s0}.
```

Or pairwise:

```math
\Delta y_{ab}=y_a-y_b.
```

If forward nuisance is approximately common-mode:

```math
\Delta(Ai)\approx A\Delta i+\Delta A(i_a-i_b),
```

and `i_a-i_b` can be smaller or more localized than absolute currents.

## 3. Robust Invariant Margin

For invariant `\Phi(Y)`:

```math
\delta^\Phi_{hg}
=
\|\Phi(T_{y,h})-\Phi(T_{y,g})\|.
```

Empirical nuisance radius:

```math
\rho^\Phi_h
=
\max_{\xi\in\Xi}
\|\Phi(T_{y,h}(\xi))-\Phi(T_{y,h}(0))\|.
```

Robust invariant margin:

```math
\Gamma^\Phi_{hg}
=
\delta^\Phi_{hg}
-\epsilon^\Phi
-\rho^\Phi_h
-\rho^\Phi_g
-\tau^\Phi.
```

E28 succeeds if any invariant produces positive margin where raw field Gamma
does not.

## 4. Required Comparisons

Compare representations:

```text
raw stacked field
normalized raw field
differential field
column-space projector
whitened Gram matrix
principal-angle spectrum
Schur edge signature projection if E27-like candidates are available
```

For each:

```text
pairwise_delta
rho
gamma
positive_gamma_rate
critical_pair_positive_gamma_rate
via_return_gamma
```

## 5. Acceptance Gates

Engineering gates:

```text
package_runs_to_completion
transfer_matrix_computed
invariants_computed
nuisance_stress_executed
reports_written
generated_domain_boundary_explicit
```

Scientific gates:

```text
best_invariant_gamma_beats_raw_gamma
best_invariant_positive_gamma_rate_ge_0_30
critical_pair_positive_gamma_rate_ge_0_30
invariant_rho_less_than_raw_rho
projector_or_gram_nontrivial
truth_in_consistent_set_rate_ge_0_90
singleton_wrong_rate_eq_0
```

## 6. Required Outputs

Write:

```text
outputs/RUN_REPORT.md
outputs/TRANSFER_MATRIX_DERIVATION.md
outputs/INVARIANT_DEFINITIONS.md
outputs/RAW_VS_INVARIANT_MARGIN_TABLE.md
outputs/PROJECTOR_GRAM_AUDIT.md
outputs/NUISANCE_INVARIANCE_AUDIT.md
outputs/CONSISTENT_SET_AUDIT.md
outputs/FAILURE_MODES.md
outputs/metrics.json
```

## 7. Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## 8. Final Claude Report

Report:

- transfer matrix construction;
- invariant definitions and sanity checks;
- raw vs invariant margins;
- nuisance radius reduction;
- critical pair results;
- all gates;
- failure modes;
- cannot_claim;
- next required evidence;
- files changed.

