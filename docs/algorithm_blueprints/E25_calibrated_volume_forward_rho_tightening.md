# E25 Calibrated Volume Forward and Operator-Radius Tightening

Status: top-level algorithm directive for Claude worker, not evidence.

Target evidence package:

```text
experiments/evidence/E25_calibrated_volume_forward_rho_tightening/
```

Affected claims:

- `C04_inverse_crime_and_operator_gap`
- `C10_pdn_kcl_distribution_need`
- `C13_calibration_protocol_reality`

Do not edit global research graph files.

## 0. Why E25 Exists

E23 Round 5 failed robust certification because the perturbation radius
`rho` dominated hypothesis separation:

```math
\Gamma = \delta-\tau-\epsilon-\rho_h-\rho_g < 0 .
```

This may mean either:

```text
1. the physics really is too uncertain for magnetic topology diagnosis, or
2. the finite-width/operator stress ladder is too crude and over-conservative.
```

E25 must make `rho` a calibrated, decomposed, numerically justified quantity
rather than a black-box penalty.

## 1. Continuous Forward Model

For a conductor volume `V_e` carrying uniform current density along unit tangent
`t_e`, edge current `i_e`, and cross-section area `a_e`, the current density is:

```math
J_e(r')={i_e\over a_e}t_e,\qquad r'\in V_e.
```

The magnetic field at sensor point `r_m`:

```math
B_e(r_m)
=
{\mu_0\over4\pi}
\int_{V_e}
{J_e(r')\times(r_m-r')\over\|r_m-r'\|^3}\,dr'.
```

The volume forward matrix column is:

```math
A^{vol}_{m,e}
=
{\mu_0\over4\pi a_e}
\int_{V_e}
{t_e\times(r_m-r')\over\|r_m-r'\|^3}\,dr'.
```

Centerline approximation:

```math
A^{cl}_{m,e}
=
{\mu_0\over4\pi}
\int_{\ell_e}
{t_e(s)\times(r_m-r_e(s))\over\|r_m-r_e(s)\|^3}\,ds.
```

Finite-width quadrature approximation:

```math
A^{quad}_{m,e}
=
\sum_{q=1}^{Q}
\omega_q
{\mu_0\over4\pi a_e}
{t_e\times(r_m-r_{e,q})\over\|r_m-r_{e,q}\|^3}.
```

The convergence target is:

```math
\|A^{quad}_{Q}-A^{quad}_{2Q}\|_F/\|A^{quad}_{2Q}\|_F \to 0.
```

## 2. Operator Radius Definition

Let `A_0` be the model used by inversion and `A_*` a better calibrated forward
operator. For an admissible current family `\mathcal{I}_h(U)`:

```math
\rho_h(U)
=
\sup_{i\in\mathcal{I}_h(U),\|i\|_2\le R_h}
\|W(A_*-A_0)i\|_2 .
```

If `\mathcal{I}` is approximated by basis `Q_h`, then:

```math
\rho_h(U)
\approx
R_h \|W(A_*-A_0)Q_h\|_2 .
```

If using network-solved current samples `i_{h,s}(\theta_k)`, estimate:

```math
\rho_h(U)
=
\max_{k,s}
\|W(A_*-A_0)i_{h,s}(\theta_k)\|_2 .
```

E25 must report both worst-case and sample-based radii.

## 3. Nuisance Jacobian Radius

Let forward nuisance parameters be:

```math
\psi=(z_{\text{sensor}},\Delta x,\Delta y,\Delta z_{\text{layer}},
w,t,\sigma_{\text{psf}},\ldots).
```

First-order perturbation:

```math
A(\psi_0+\Delta\psi)i
\approx
A(\psi_0)i
+
\sum_j
{\partial A\over\partial\psi_j}i\,\Delta\psi_j.
```

With bounded box uncertainty `|\Delta\psi_j|\le a_j`:

```math
\rho^{box}_h
\le
\sum_j
a_j
\sup_{i\in\mathcal{I}_h}
\left\|
W{\partial A\over\partial\psi_j}i
\right\|_2.
```

With ellipsoid uncertainty `\Delta\psi^T\Lambda^{-1}\Delta\psi\le1`:

```math
\rho^{ellipsoid}_h
\le
\sup_i
\left[
\lambda_{\max}
\left(
G_i^T W^T W G_i \Lambda
\right)
\right]^{1/2},
```

where:

```math
G_i=
\left[
{\partial A\over\partial\psi_1}i,\ldots,
{\partial A\over\partial\psi_p}i
\right].
```

Use finite differences if analytic derivatives are too costly.

## 4. What Must Be Calibrated

At minimum decompose:

```text
rho_finite_width_centerline_to_volume
rho_multifilament_to_volume
rho_sensor_height
rho_registration_xy
rho_layer_z
rho_width_thickness
rho_psf_blur
rho_background_offset
rho_combined_conservative
rho_combined_rss
```

Report the radius as absolute and relative to signal scale:

```math
\rho_{\mathrm{rel}} = {\rho\over \|WAi\|_2+\epsilon}.
```

This is crucial because E23 Round 5 suggested finite-width surrogate
perturbations of 50-200% of nominal signal. E25 must decide whether that is
physically plausible or an artifact of the surrogate.

## 5. Canonical Validation Families

Use deterministic generated geometries:

```text
straight strip
parallel strips
rectangular loop
vertical via approximation
two-layer trace with return
four-layer via-return motif
```

For each, compare:

```text
analytic/reference where available
centerline
3-filament
5-filament
volume quadrature coarse
volume quadrature fine
```

Metrics:

```text
field_rmse
field_relative_l2
max_component_error
operator_frobenius_relative_error
rho_relative_by_current_family
quadrature_convergence_rate
```

## 6. Interface to E24/E26

E25 should write reusable JSON artifacts:

```text
outputs/rho_calibration_table.json
outputs/operator_error_budget.json
```

Each row:

```text
geometry_family
operator_pair
nuisance_name
absolute_radius
relative_radius
recommended_for_gamma
calibration_status
```

E24/E26 can later read this table, but E25 must be self-contained and runnable
alone.

## 7. Acceptance Gates

Engineering gates:

```text
package_runs_to_completion
canonical_geometries_generated
volume_quadrature_runs
quadrature_convergence_reported
rho_decomposition_reported
no_fake_external_solver_claim
reports_written
generated_domain_boundary_explicit
```

Scientific gates:

```text
volume_quadrature_relative_change_le_0_05
multifilament_beats_centerline_error
rho_finite_width_relative_below_centerline_surrogate
rho_combined_budget_finite
dominant_rho_source_identified
recommended_gamma_rho_available
```

If scientific gates fail, preserve the result as an operator-boundary finding.

## 8. Required Outputs

Write:

```text
outputs/RUN_REPORT.md
outputs/VOLUME_FORWARD_DERIVATION.md
outputs/QUADRATURE_CONVERGENCE_AUDIT.md
outputs/CENTERLINE_MULTIFILAMENT_VOLUME_COMPARISON.md
outputs/RHO_DECOMPOSITION_TABLE.md
outputs/NUISANCE_JACOBIAN_RADIUS_AUDIT.md
outputs/GAMMA_RHO_RECOMMENDATION.md
outputs/FAILURE_MODES.md
outputs/metrics.json
outputs/rho_calibration_table.json
outputs/operator_error_budget.json
```

## 9. Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## 10. Final Claude Report

Report:

- forward formulas implemented;
- quadrature convergence;
- centerline vs multifilament vs volume errors;
- rho decomposition;
- whether previous E23 rho was over-conservative or physically plausible;
- recommended rho for future Gamma certificates;
- all gates;
- failure modes;
- cannot_claim;
- next required evidence;
- files changed.

