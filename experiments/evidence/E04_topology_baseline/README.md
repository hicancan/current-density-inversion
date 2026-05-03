# exp04-topology-aware-inverse-benchmark

## Role

This experiment is the active `exp04` full benchmark.

The previous linear topology-loss mechanism experiment has been archived under
`experiments/archived/exp04-topology-soft-loss-network`. This active `exp04`
uses the `exp03` Biot-Savart benchmark dataset:

```text
../E03_two_layer_via_topology/data/two_layer_via_benchmark.npz
```

The inverse task is:

```text
B_obs[Bx,By,Bz] -> J1x,J1y,J2x,J2y,s1
```

## Baselines

- `zero`
- `ridge`
- `ridge_posthoc_topology`
- `physics_tikhonov`
- `physics_tikhonov_posthoc_topology`
- `unet_no_topology`
- `unet_topology_soft_loss`
- `unet_topology_two_stage_refined`
- `unet_topology_posthoc`
- residual-via detector diagnostics from raw adjoint, oracle sheet residual,
  no-topology sheet residual, topology-soft sheet residual, and DoG/strict
  false-positive-controlled variants

## Outputs

- `outputs/metrics.json`
- `outputs/RUN_REPORT.md`
- `outputs/01_training_curves.png`
- `outputs/02_prediction_comparison.png`
- `outputs/03_metric_bars.png`
- `outputs/04_lambda_pareto.png`
- `outputs/METRICS_TABLE.md`
- `outputs/CHANNEL_METRICS_TABLE.md`
- `outputs/STRESS_METRICS_TABLE.md`
- `outputs/OPERATOR_STRESS_TABLE.md`
- `outputs/PYPEEC_OPERATOR_STRESS_TABLE.md`
- `outputs/PYPEEC_FROZEN_INFERENCE_TABLE.md`
- `outputs/PYPEEC_FROZEN_INFERENCE_SUBSET_TABLE.md`
- `outputs/PYPEEC_NULL_VIA_DIAGNOSTICS_TABLE.md`
- `outputs/PYPEEC_NULL_VIA_MECHANISM_SUMMARY.md`
- `outputs/PYPEEC_NULL_VIA_FAILURE_CASES.md`
- `outputs/PYPEEC_RETURN_PATH_DIAGNOSTICS_TABLE.md`
- `outputs/PYPEEC_RETURN_PATH_MECHANISM_SUMMARY.md`
- `outputs/PYPEEC_RETURN_PATH_FAILURE_MODES.md`
- `outputs/NULL_VIA_VALIDATION_STRESS_TABLE.md`
- `outputs/NULL_VIA_HYPOTHESIS_GATE_TABLE.md`
- `outputs/NULL_VIA_GATE_PARETO_TABLE.md`
- `outputs/NULL_VIA_HYPOTHESIS_EVIDENCE_TABLE.md`
- `outputs/NULL_VIA_UNCERTAINTY_REFUSAL_TABLE.md`
- `outputs/PYPEEC_HELDOUT_SPLIT_PROTOCOL.md`
- `outputs/PYPEEC_RETURN_PATH_HYPOTHESIS_TABLE.md`
- `outputs/figures/pypeec_null_via_failures/*.png`
- `outputs/figures/null_via_gate_pareto.png`
- `outputs/figures/null_via_gate_case_studies/*.png`
- `outputs/VIA_DETECTOR_TABLE.md`
- `outputs/predictions_test.npz`
- `STRICT_DETECTOR_NO_LEAKAGE_PROTOCOL.md`

## Evidence Scope

This benchmark is intentionally stricter than the archived linear mechanism
experiment:

- the main pair compares U-Net-lite with and without topology loss on the same
  `exp03` Biot-Savart train/val/test/OOD splits;
- the metric table reports reconstruction, topology residual, via localization,
  layer-leakage proxy, fitted forward-proxy residual, and independent raster
  Biot-Savart re-forward residual side by side;
- the physics-only Tikhonov/Landweber baseline solves against the same raster
  Biot-Savart operator without using supervised labels at inference time;
- the channel table reports active-channel relative L2 plus current-scale RMSE,
  so zero-energy channels cannot create misleading relative-error blowups;
- the lambda sweep checks whether a stronger topology-consistency Pareto point
  exists beyond the default training setting;
- the multi-seed summary checks that topology residual reduction is not a
  one-seed artifact.
- the stress table evaluates the trained models without retraining on input
  noise, PSF blur, standoff-like gain tilt, channel mixing, and a combined case.
- the operator stress table row evaluates a finite-width/weak-return surrogate
  input generated from the same truth maps, so centerline-trained models face a
  measurable forward-operator mismatch.
- the PyPEEC operator-stress bridge imports the frozen exp07 real-solver
  artifact and reports canonical + exp03-like PyPEEC field gaps next to exp04
  stress results. It is read-only and is not used for training, validation
  threshold selection, or calibration.
- the PyPEEC frozen inference stress reads exp07's
  `pypeec_exp03_like_mini_dataset.npz`, applies the already-trained U-Net
  variants with frozen normalization and two-stage settings, and reports model
  metrics on real PyPEEC fields. It now includes subset diagnostics for
  canonical, exp03-like, via, no-via, dense-via, and return-path subsets. It is
  still a mini solver-validation distribution, not a broad CAD/PyPEEC dataset.
- the PyPEEC no-via diagnostics split out false-positive mechanisms by case and
  model, including predicted `s1` energy, peak location, distance to trace/bend
  or return masks, topology residual, magnetic residual, leakage, and a
  mechanism label. Mechanism summaries and representative figures explain the
  current FP problem; they do not tune a PyPEEC threshold.
- the PyPEEC return-path diagnostics split current allocation from magnetic
  consistency by reporting signal/return energy fractions, return-path L2,
  topology residual, leakage, PyPEEC physical re-forward residual, and
  failure-mode labels. The mechanism summary separates raw magnetic residual,
  scalar-fitted shape residual, amplitude scale, and layer allocation. These
  reports document return current as an independent physical challenge rather
  than treating it as solved by topology loss.
- `STRICT_DETECTOR_NO_LEAKAGE_PROTOCOL.md` defines how future no-via confidence
  gates may be calibrated without using the current PyPEEC test cases for
  threshold selection.
- the null-via hypothesis gate is calibrated on validation-only synthetic stress
  families that include paired no-via and true-via bend/corner, return-path, and
  operator-gap residuals, plus stronger bend and layer-allocation ambiguity
  cases, then frozen before evaluation on PyPEEC. It reports no-via false
  positive, via recall/F1, dense-via F1, return-path false positive, topology
  MSE, and PyPEEC physical-B residual before/after the gate. It also reports a
  frozen PyPEEC Pareto table/plot and before/after case-study figures so the
  FP/recall trade-off is auditable. It is a no-leakage prototype for rejecting
  low-confidence via candidates, not a final detector.
- the H0/H1 evidence table reframes each candidate as true-via evidence versus
  artifact/no-via evidence, then reports uncertainty/refusal labels. This is a
  system-identification diagnostic and does not rewrite the frozen PyPEEC
  predictions.
- the generative H0/H1 evidence table explicitly compares a re-forwarded H1
  model that keeps predicted `s1` against an H0 model that removes `s1`. It
  reports `Delta evidence H1-H0`, calibration rows, and a calibration plot,
  while still selecting no PyPEEC threshold.
- the held-out split protocol defines how a future larger PyPEEC dataset could
  be separated into calibration and test roles, and the held-out evaluation
  table reports current frozen metrics by those reserved roles. The current
  exp04 outputs do not use PyPEEC rows for calibration or threshold selection.
- the return-path hypothesis table distinguishes via-like excess-source
  evidence from return-current mismatch evidence, making return path a separate
  physical mechanism rather than a generic detector error.
- the return-current-aware generator table is an oracle diagnostic that tests
  whether a signal-current plus scalar return-current basis can better explain
  PyPEEC return-path fields. It uses known labels and is not an inference
  model.
- the selective risk table reports coverage versus via/no-via decision risk
  for confidence-based refusal. It frames refusal as a measurable operating
  curve rather than a vague warning label.
- the via detector table separates dense `s1` reconstruction from candidate
  localization, exposing when raw-field via detection is background-swamped and
  when residual detection is useful. DoG/strict variants explicitly test
  no-via false-positive control on the OOD split. Detector thresholds are
  selected on validation data and then frozen for test/OOD reporting.
- the two-stage refinement baseline calibrates residual-adjoint via scores on
  validation data and updates the `s1` channel after U-Net inference. It is
  included to measure the promise and side effects of a residual-via route
  before building a full architecture.

## Run

```powershell
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json
uv run --with-requirements requirements.txt --with pytest pytest -q
```

For the local WSL CUDA environment:

```powershell
wsl -d Ubuntu -- bash -lc 'cd /mnt/d/code/github/hicancan/magnetic-system-identification-ssot/experiments/evidence/E04_topology_baseline && source ~/conda/etc/profile.d/conda.sh && conda activate quantum-dev && python src/run_all.py --config configs/default.json'
```

## Boundary

This is still a synthetic benchmark. It proves whether topology-aware learning
helps on the exp03 Biot-Savart dataset, not on real QDM/FEM data. The residual
via detector is diagnostic and does not replace the reconstructed `s1` map. The
finite-width/return row is a surrogate operator mismatch, not COMSOL/FastHenry.
The PyPEEC mini stress reports frozen model inference on exp07 real-solver
fields, but it is not yet a full PyPEEC-generated exp03 dataset evaluation.
The no-via and return-path diagnostic tables are failure-analysis artifacts;
they do not claim that PyPEEC no-via false positives or return-path magnetic
consistency have been solved. Any future detector mitigation must follow the
strict no-leakage protocol before it can be reported as an unbiased PyPEEC test.
The null-via hypothesis gate follows that protocol by selecting parameters only
from synthetic validation stress and freezing them before PyPEEC evaluation; any
improvement must be reported with its recall and physical-consistency trade-off.
The H0/H1 evidence, generative H1/H0 re-forward scoring, uncertainty/refusal,
selective-risk, held-out split, and return-path/return-current tables are
diagnostic/protocol artifacts. They move the benchmark toward magnetic system
identification but do not claim that via diagnosis or return-current inference
is solved.


