# RUN REPORT - E19 OBGHI Minimal Observable Topology Posterior

## Claim affected

- Primary: `C10_pdn_kcl_distribution_need`
- Secondary: `C06_graph_hypothesis_system_identification`, `C02_single_plane_identifiability_boundary`, `C04_inverse_crime_and_operator_gap`

## Evidence added

Generated-domain minimal OBGHI evidence package implementing closed-form Gaussian Bayesian posterior topology inference over H0/H1/H2/H3 explanations on a four-layer generated sheet/via observation operator. 72 cases across 6 families (no-via clean, single via, dense via cluster, model gap registration, model gap standoff, return-path deep loop).

## Metrics

- case_count: 72
- OBGHI top1_accuracy: 0.3333
- OBGHI accepted_accuracy: 0.3455
- OBGHI accepted_risk: 0.6545
- OBGHI reject_rate: 0.0
- OBGHI need_next_measurement_rate: 0.2361
- OBGHI brier_score: 0.2465
- OBGHI mean_posterior_entropy: 0.7120
- OBGHI via_gap_angle_deg: 67.78
- Ridge-map top1_accuracy: 0.3333

By truth:
- H0_no_via (12 cases): top1=0.0, accept_rate=0.833, mean_true_posterior=0.056
- H1_via (24 cases): top1=1.0, accept_rate=0.792, mean_true_posterior=0.727
- H2_model_gap (24 cases): top1=0.0, accept_rate=0.75, mean_true_posterior=5.87e-07
- H3_return_path (12 cases): top1=0.0, accept_rate=0.667, mean_true_posterior=0.255

## Operator diagnostics

- A shape: `[432, 1584]` (3-channel field, 4 layers with Jx/Jy + 3 via pairs)
- via_columns_nonzero: `True`
- via_column_norm_min: `0.0103`
- via_column_norm_mean: `0.0179`
- sheet_column_norm_mean: `0.0245`
- condition_proxy: `94.5`

## Debugging priority audit

### Priority 1: Via forward columns are nonzero
PASS. All via Biot-Savart columns produce nonzero field contributions (min norm 0.0103).

### Priority 2: H1/H2/H3 posterior probabilities differ on generated families
PARTIALLY PASS. H1_via posterior (mean 0.727) and H3_return_path posterior (mean 0.255) differ. H2_model_gap posterior is effectively zero (mean 5.87e-07) even on model-gap truth cases. Root cause: the H2 gap basis uses simple Gaussian field-space patterns that do not match the gradient (registration) and Laplacian (standoff) model-gap data generation patterns. Additionally, the uniform prior variance for H2 (0.35) is applied to all blocks including the shared graph/residual basis, penalizing H2 relative to H0 (prior variance 1.0). The via-gap subspace principal angle is 67.8 degrees, confirming the subspaces are well-separated but the gap basis is too weak to compete.

### Priority 3: Accept/reject/need-next-measurement decisions are present
PASS. Accept=55, need_next_measurement=17, reject=0. No reject decisions occur because the reject criteria require top_p < 0.45 or via-gap ambiguity (neither triggers). The need-next-measurement decisions are driven by the accept threshold of 0.62.

### Priority 4: OBGHI top1/accepted risk against ridge-map baseline
PASS for comparison. OBGHI top1 (0.333) matches ridge baseline (0.333). Ridge baseline cannot distinguish H0/H2/H3 from H1 (confusion matrix shows all families classified as H1_via). This is not a bug but a deliberate limitation: the ridge baseline classifies by via/bottom energy ratios and cannot detect model gaps.

### Priority 5: Failures preserved as evidence boundaries
PASS. All 57 failure cases are documented in FAILURE_CASES.md with failure modes: accepted_wrong_topology (42 cases) and insufficient_posterior_separation (15 cases). No attempt was made to overfit gates.

## Acceptance gates

| gate | passed |
|---|---:|
| posterior_rows_present | True |
| topology_posterior_nontrivial | True |
| accepted_risk_bounded | **False** |
| reject_or_need_next_available | True |
| via_gap_ambiguity_measured | True |
| obghi_matches_or_beats_ridge_top1 | True |
| generated_domain_boundaries_recorded | True |

All gates passed: `False`

Gate failure: `accepted_risk_bounded` (0.655 > 0.45) because H1_via dominates all families. This is a legitimate generated-domain evidence boundary, not a gate-tuning problem.

## Failure modes

See `FAILURE_CASES.md`. Three systematic failure modes identified:

1. **H1_via dominates H0_no_via (no-via false-positive)**: The via basis has enough flexibility to fit no-via background fields better than H0, creating overconfident via predictions on clean no-via cases.

2. **H2_model_gap posterior collapses to zero**: The gap basis is fundamentally mismatched to the model-gap data generation. Gaussian field-space patterns cannot compete with current-based patterns under the Bayesian evidence framework at current prior variances.

3. **H1_via dominates H3_return_path**: The return-path basis (4 deep-layer loop modes) is too small to overcome the via basis flexibility. H3 has non-zero posterior (mean 0.255) but never wins.

## Claim status change

**None.** No claim status was upgraded from unrun code. C10 remains `supported_generated`, C06 remains `supported_generated`, C02 remains `supported`, C04 remains `supported_generated`. E19 is registered as generated-domain evidence with `passed_with_limitations` status.

## Cannot claim

- real QDM/NV validation
- real CAD/Gerber/GDS validation
- external FEM/FastHenry/COMSOL validation
- real-board PDN/KCL robustness
- mechanism-level explanation on real data
- universal via detection
- that H2_model_gap is resolved
- that the via-gap ambiguity is quantified sufficiently for deployment
- that OBGHI posterior probabilities are calibrated for real observations

## Next required evidence

1. Replace simple Gaussian gap basis with gradient/Laplacian/registration-matched basis patterns.
2. Add multi-height observation support (standoff variation as an observable discriminator).
3. Add multi-state excitation support (different current injection patterns).
4. Compare E19 failure slices against E18 physics-constrained inverse failure cases (dense-via recall, deep-layer misallocation).
5. Add per-block prior variances instead of uniform per-hypothesis prior variance.

## Tests run

- `uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests`: 5 passed (smoke config: 1.61s)
- `uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke`: passed_with_limitations (1.14s)
- `uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs`: passed_with_limitations (20.26s)

## Files changed

- `experiments/evidence/E19_obghi_minimal_observable_topology_posterior/` (all package files)
- `research_graph/experiments.yml` (E19 entry added)
- `research_graph/evidence_edges.yml` (E19 edges added)
- `research_graph/update_log.md` (this audit)
