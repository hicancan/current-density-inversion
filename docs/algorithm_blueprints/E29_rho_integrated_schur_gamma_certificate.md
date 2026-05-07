# E29 Rho-Integrated Schur Gamma Certificate

Status: top-level algorithm directive for Claude worker, not evidence.

Target evidence package:

```text
experiments/evidence/E29_rho_integrated_schur_gamma_certificate/
```

Affected claims:

- `C04_inverse_crime_and_operator_gap`
- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`
- `C13_calibration_protocol_reality`

Do not edit global research graph files.

## 0. Motivation

E25 produced a calibrated operator-radius budget. E27 will produce candidate
edge Schur signatures. E29 combines them into the actual certificate required
for a breakthrough:

```math
\Gamma > 0
```

after subtracting physically justified `rho`, noise, and acceptance thresholds.

This package is the auditing bridge: it should be conservative, boring, and
hard to fool.

## 1. Certificate Inputs

If E25 artifacts are available, read:

```text
outputs/rho_calibration_table.json
outputs/operator_error_budget.json
```

If not available, implement a small local copy of E25-style rho estimates and
mark it as local generated calibration.

For each candidate edge defect `q`, Schur signal:

```math
S_q(U)=\|W\Delta Y_q(U)\|_2.
```

Operator radius:

```math
\rho_q(U)
=
\rho_{\text{finite width}}
+\rho_{\text{height}}
+\rho_{\text{registration}}
+\rho_{\text{layer z}}
+\rho_{\text{background}}
```

or RSS if explicitly justified:

```math
\rho_q^{rss}
=
\left(\sum_j \rho_{q,j}^2\right)^{1/2}.
```

Gamma:

```math
\Gamma_q^{cons}
=
S_q-\epsilon-\tau-\rho_q^{cons}.
```

```math
\Gamma_q^{rss}
=
S_q-\epsilon-\tau-\rho_q^{rss}.
```

Both must be reported. Conservative gamma governs claims.

## 2. Required Stress Split

Separate:

```text
calibration geometries
evaluation geometries
```

Do not choose thresholds from evaluation rows. Calibration determines:

```text
epsilon_noise
tau
rho recommended values
```

Evaluation reports:

```text
positive_gamma_rate
wrong_accept_rate
truth_missing_rate
empty_rate
```

## 3. Certificate Decision Rule

Accept defect `q` only if:

```math
\Gamma_q^{cons}>0
```

and pairwise against alternatives:

```math
\Gamma_{qr}^{cons}
=
\|\Delta Y_q-\Delta Y_r\|
-\epsilon-\tau-\rho_q-\rho_r
>0.
```

Otherwise refuse:

```text
insufficient robust magnetic information
```

## 4. Required Ablations

Report all:

```text
no_rho_gamma
rss_rho_gamma
conservative_rho_gamma
E23_old_rho_gamma
E25_calibrated_rho_gamma
```

This tells us whether the bottleneck is physics signal or uncertainty budget.

## 5. Acceptance Gates

Engineering gates:

```text
package_runs_to_completion
rho_artifacts_loaded_or_recomputed
calibration_evaluation_split_enforced
conservative_and_rss_gamma_reported
pairwise_gamma_reported
ablation_table_reported
reports_written
generated_domain_boundary_explicit
```

Scientific gates:

```text
E25_rho_improves_gamma_over_E23_old_rho
positive_conservative_gamma_rate_ge_0_30
positive_rss_gamma_rate_ge_0_50
pairwise_conservative_gamma_rate_ge_0_20
truth_in_consistent_set_rate_ge_0_90
wrong_accept_rate_le_0_10
empty_rate_le_0_10
```

If conservative gates fail but RSS gates pass, report as promising but not
claim-supporting.

## 6. Required Outputs

Write:

```text
outputs/RUN_REPORT.md
outputs/RHO_INPUT_AUDIT.md
outputs/GAMMA_ABLATION_TABLE.md
outputs/CONSERVATIVE_GAMMA_CERTIFICATE.md
outputs/RSS_GAMMA_UPPER_BOUND.md
outputs/PAIRWISE_DEFECT_CERTIFICATE.md
outputs/CALIBRATION_EVALUATION_SPLIT_AUDIT.md
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

- rho sources and split discipline;
- no-rho, RSS-rho, conservative-rho, old-rho, calibrated-rho Gamma;
- pairwise defect certificate;
- whether E25 rho changes the E23/E24 conclusion;
- all gates;
- failure modes;
- cannot_claim;
- next required evidence;
- files changed.

