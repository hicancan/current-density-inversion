# Update Log

## 2026-05-03 - Initial claim graph

Claim affected:
- C01_forward_sanity
- C02_single_plane_identifiability_boundary
- C03_unet_topology_baseline_boundary
- C04_inverse_crime_and_operator_gap
- C05_pypeec_solver_bridge
- C06_graph_hypothesis_system_identification
- C07_stacked_evidence_calibration
- C08_ood_refusal_safety
- C09_fewshot_family_adaptation
- C10_pdn_kcl_distribution_need
- C11_mechanism_level_explanation
- C12_real_qdm_nv_validation
- C13_calibration_protocol_reality
- C14_unlabeled_family_adaptation

Change type:
- claim graph initialization
- evidence registration
- boundary registration

Files changed:
- research graph SSOT
- claim-scoped experiment plans
- claim-scoped output summaries
- validation and rendering scripts

Evidence:
- nine evidence packages registered from forward sanity through real-data
  intake gates.

Metrics:
- graph integrity is enforced by `scripts/validate_graph.py`.

Claim status before:
- no graph state.

Claim status after:
- claim-centered graph state initialized.

Cannot claim:
- real QDM/NV validation.
- real CAD/Gerber/GDS validation.
- deployment-safe via/no-via diagnosis.
- mechanism-level explanation for accepted hidden rows.

Next required evidence:
- implement `D08_pdn_kcl_circuit_graph` with KCL, current closure, return path,
  and held-out/few-shot protocols.

## 2026-05-03 - Runnable evidence packages

Claim affected:
- C01-C09
- C11-C13

Change type:
- runnable evidence implementation added
- no-leakage runtime commands registered
- evidence output gate check added

Files changed:
- `experiments/evidence/`
- `research_graph/experiments.yml`
- `scripts/run_evidence.py`
- `scripts/check_evidence_outputs.py`
- `tests/test_graph_integrity.py`

Evidence:
- Claim-graph evidence packages now contain runnable code, configs, tests, and
  local result artifacts.

Metrics:
- `scripts/check_evidence_outputs.py` checks registered metrics gates.
- `scripts/run_evidence.py --all --mode test --continue-on-fail` runs the
  evidence package test suites.

Claim status before:
- graph state initialized with evidence summaries only.

Claim status after:
- graph state initialized with runnable evidence packages.

Cannot claim:
- real QDM/NV validation.
- real CAD/Gerber/GDS validation.
- deployment-safe via/no-via diagnosis.

Next required evidence:
- implement and validate the PDN/KCL circuit-graph distribution.

## 2026-05-03 - Runtime verification pass

Claim affected:
- C01-C09
- C11-C13

Change type:
- runtime verification
- path repair

Files changed:
- `experiments/evidence/`
- `research_graph/experiments.yml`

Evidence:
- Evidence package unit tests pass across all registered runtime packages.
- Reproduction smoke entries were run for canonical forward, observability,
  two-layer topology, sensor observation stress, operator gap, solver quick
  bridge, graph hypothesis scoring, and real-data intake validation.

Metrics:
- All registered metrics gates pass.
- Graph hypothesis scoring reports `all_scientific_gates_passed`.

Claim status before:
- runnable evidence packages registered.

Claim status after:
- runnable evidence packages verified locally.

Cannot claim:
- real QDM/NV validation.
- full retraining of the image inverse benchmark during the smoke run.
- PDN/KCL distribution robustness.

Next required evidence:
- run the full image-inverse training package only when retraining is needed;
  current claim state uses the preserved gate artifacts and package tests.
