# E20 Active OQCI Measurement Design

Status: design document only, not evidence.

Owner model: Codex designs and audits; Claude Code implements in an isolated
worktree with `--effort max`.

## Purpose

E19.2 showed that the current single-height generated protocol leaves every
H0/H1/H2/H3 case ambiguous under the OQCI consistent-set audit. E20 should not
try to win top-1 classification by a stronger posterior. It should attack the
information boundary directly:

```text
Given the current consistent set, which feasible next magnetic measurement most
shrinks the observable equivalence class for current claims?
```

This is the first top-level breakthrough target because it changes the
experiment family `E`, not only the estimator.

## Affected Claim

Primary:

- `C02_single_plane_identifiability_boundary`
- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`

Secondary:

- `C04_inverse_crime_and_operator_gap`
- `C13_calibration_protocol_reality`

## Involved Nodes

Data:

- `D11_chip_like_generated_pdn_family`

Physics:

- `P01_biot_savart_maxwell_forward`
- `P04_divJ_source_sink_consistency`
- `P05_kcl_node_conservation`
- `P07_current_closure_loop`
- `P08_return_path_completeness`

Forward:

- `F02_centerline_biot_savart`

Observation:

- `O01_ideal_Bxyz`
- `O02_Bz_only`
- `O03_Bxy`
- `O08_multi_height`
- `O09_multi_state_excitation`

Representation:

- `R08_hypothesis_set`
- `R09_posterior_candidate_set`
- `R10_multilayer_chip_like_pdn_graph`

Algorithm:

- `A04_hypothesis_scorer`
- `A12_bayesian_or_glrt_model_evidence`

Protocol:

- `S11_no_leakage_calibration_heldout`
- `S12_conformal_or_selective_risk_protocol`

Metrics:

- `M08_accepted_accuracy`
- `M09_accepted_risk`
- `M10_reject_rate`
- `M13_family_generalization_gap`

## First-Principles Formulation

Let `s` be an admissible generated current/topology state and `L(s)` be a
current claim, such as:

- `H1_via` is active;
- `H2_model_gap` is active;
- `H3_return_path` is active;
- total current on a deep layer exceeds a threshold;
- a via-chain segment carries nonzero current.

For an experiment family `E`:

```text
F_E(s) = [F_e1(s), ..., F_en(s)]
d_E(s1, s2) = || Sigma^{-1/2} (F_E(s1) - F_E(s2)) ||_2
```

The current consistent set is:

```text
C_epsilon(y; E) =
{ s in A : || Sigma^{-1/2} (F_E(s) - y) ||_2 <= epsilon }
```

The claim interval is:

```text
I_L(y; E) =
[ min_{s in C_epsilon(y; E)} L(s),
  max_{s in C_epsilon(y; E)} L(s) ]
```

E20 chooses a next measurement `e_next` from a candidate set `M`:

```text
e_next* =
argmax_e Utility(E + e)
```

where:

```text
Utility(E + e) =
  w1 * expected_claim_interval_width_reduction
+ w2 * near_null_dimension_reduction
+ w3 * min_pairwise_distance_increase
+ w4 * wrong_high_confidence_accept_reduction
- w5 * measurement_cost
```

The scientific target is not a prettier current map. The target is a measured
reduction in ambiguity.

## Candidate Measurements

The implementation should support a finite candidate pool:

1. additional height:
   - examples: `1.6um`, `3.2um`, `6.4um`, `12.8um`
2. component set:
   - `Bz`
   - `Bxy`
   - `Bxyz`
3. excitation/load state:
   - reuse or synthesize current injections/load states if available;
   - if E19.2 has no native multi-state generator, implement a minimal
     deterministic state perturbation over existing basis amplitudes.
4. local high-resolution rescan:
   - optional for the first slice;
   - may be represented as a measurement mask with lower noise or denser pixels
     over the most ambiguous region.

The first runnable slice should include at least height and component choices.
Multi-state can be a second engineering slice if needed.

## Algorithm Steps

1. Reuse or adapt E19.2 generated cases and hypothesis basis construction.
2. Build a baseline experiment family `E0`, normally the current single-height
   protocol.
3. Compute baseline OQCI metrics:
   - consistent-set nonempty rate;
   - ambiguity rate;
   - mean claim interval width;
   - near-null count;
   - effective rank;
   - pairwise distances.
4. For each candidate `e_next`:
   - stack `F_E0` with `F_e_next`;
   - recompute consistent sets and claim intervals;
   - recompute pairwise distances and near-null modes;
   - compute utility.
5. Rank candidate measurements.
6. Output:
   - best next measurement per case;
   - global best measurement class;
   - before/after ambiguity metrics;
   - failure cases where no candidate helps;
   - cannot-claim boundaries.

## Expected Evidence Package

Target package:

```text
experiments/evidence/E20_active_oqci_measurement_design/
```

Suggested files:

```text
README.md
DESIGN.md
requirements.txt
configs/
  smoke.json
  default.json
src/
  __init__.py
  config.py
  data_adapter.py
  operators.py
  oqci_core.py
  candidates.py
  utility.py
  reporting.py
  metrics.py
  run_all.py
tests/
  test_candidates.py
  test_utility.py
  test_oqci_reuse.py
  test_run_outputs.py
outputs/
  .gitkeep
research_graph_patch/
  snippets.md
```

Worker may reuse E19.2 source by copying a minimal subset into the E20 package
or importing carefully if package import paths are stable. Prefer local package
self-containment if that avoids brittle cross-package imports.

## Metrics and Gates

Required metrics:

```text
case_count
candidate_count
baseline_ambiguity_rate
best_ambiguity_rate
ambiguity_rate_reduction
baseline_mean_interval_width
best_mean_interval_width
claim_interval_width_reduction
baseline_near_null_count
best_near_null_count
near_null_count_reduction
baseline_effective_rank
best_effective_rank
effective_rank_gain
min_pairwise_distance_gain
wrong_high_confidence_accept_count
need_next_measurement_rate
best_candidate_distribution
```

Engineering gates:

- package runs in smoke and default configs;
- candidate pool is nonempty;
- baseline OQCI metrics are reproduced or close to E19.2;
- every candidate has utility metrics;
- reports are written;
- leakage audit is present;
- generated-domain boundary is recorded.

Scientific gates:

- `candidate_count >= 4`;
- `ambiguity_rate_reduction > 0` for at least one candidate, or a documented
  negative result if none helps;
- `claim_interval_width_reduction >= 0.10` for at least one target family, or a
  documented negative result;
- no wrong high-confidence accepts;
- best measurement is not selected solely by residual fit.

Scientific gates may fail. Failure is valuable if the package proves that a
candidate observation family still cannot break the ambiguity.

## Reports

Required outputs:

```text
outputs/metrics.json
outputs/RUN_REPORT.md
outputs/CANDIDATE_RANKING.md
outputs/AMBIGUITY_REDUCTION.md
outputs/CLAIM_INTERVALS_BEFORE_AFTER.md
outputs/NEAR_NULL_BEFORE_AFTER.md
outputs/NEXT_MEASUREMENT_POLICY.md
outputs/FAILURE_MODES.md
```

## Cannot Claim

E20 cannot claim:

- real QDM/NV validation;
- real CAD/GDS validation;
- hardware feasibility of active measurement;
- universal multilayer recovery;
- that generated multi-height improvements transfer to real devices;
- that no improvement means all physical measurement protocols are useless.

E20 can claim only:

- generated-domain measurement-candidate utility under the implemented basis,
  noise, and forward family;
- whether the tested candidate measurements shrink the OQCI ambiguity in that
  domain.

## Claude Worker Scope

Implement only the E20 package and proposed research graph snippets under:

```text
experiments/evidence/E20_active_oqci_measurement_design/
```

Do not edit global research graph SSOT files. Write proposed snippets instead.
Do not modify unrelated evidence packages except read-only inspection.

Run at minimum:

```powershell
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
```

If feasible, also run:

```powershell
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

Final worker report must include files changed, commands run, metrics, failure
modes, cannot_claim, and next required evidence.

