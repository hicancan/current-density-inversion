# Reproduce Exp08

## Environment

默认使用仓库通用的 `uv` 运行方式。

## Run

```bash
uv run --with-requirements requirements.txt python src/run_all.py
```

Optional custom paths:

```bash
uv run --with-requirements requirements.txt python src/run_all.py \
  --config configs/default.json \
  --outputs outputs \
  --data data
```

## Tests

```bash
uv run --with-requirements requirements.txt pytest -q
uv run --with-requirements requirements.txt python -m compileall src tests
```

## Determinism

The default configuration uses seed `20260430`. Thresholds and complexity penalties are selected only on the validation split and then frozen for test/OOD reporting.

## Leakage rules

- Test/OOD labels are never used for threshold selection.
- Complexity penalty is selected on validation only.
- Raw via template, sheet-residual template, and graph H1/H0 use the same validation-only threshold protocol.
- OOD has stronger noise/geometry/current shifts and optional hidden background return perturbations.
- Model-selection calibration rows are audit-only. They rank PyPEEC frozen
  trade-offs but do not change predictions or thresholds.
- The held-out PyPEEC model-selection pilot uses a deterministic
  calibration/held-out split on the current mini distribution. It is a protocol
  check, not broad external validation.
- Repeated PyPEEC split stability rows reshuffle calibration/held-out partitions
  within each true hypothesis. They estimate ranking variance but do not select
  or change the frozen bridge predictions.
- Unknown-safety thresholds target the configured clean false-reject budget and
  do not use hidden labels for threshold selection.
- Accepted-hidden risk is reported after thresholding; hidden rows still do not
  choose the threshold.
- Physical-evidence unknown signals use the same clean false-reject protocol.
- Active-design constraints are synthetic feasibility screens, not real
  hardware limits.

## Expected default results

The default smoke-scale run should report `all_scientific_gates_passed: true`.
Representative current values:

- test 4-way hypothesis accuracy: `1.000`
- OOD 4-way hypothesis accuracy: `0.880`
- OOD graph H1/H0 AUC: `0.969`
- OOD graph H1/H0 no-via false-positive rate: `0.000`
- exp07 centerline bridge 4-way accuracy: `1.000`
- exp07 PyPEEC bridge 4-way accuracy: about `0.695`
- hidden-mechanism stress 4-way accuracy: about `0.417`
- shifted-via accuracy after via-location marginalization: about `1.000`
- finite-width PyPEEC-aware basis bridge accuracy: about `0.810`
- combined PyPEEC-aware basis median PyPEEC residual: about `0.074`
- finite-width plus extra-count evidence PyPEEC accuracy: about `0.829`
- finite-width plus H0-conservative evidence PyPEEC no-via H0 accuracy: about `1.000`
- model-selection audit top row: `finite_width_sheet + h0_conservative`
  with objective about `0.666`, H0 acc `1.000`, H1 acc about `0.694`
- held-out PyPEEC split sizes: current protocol uses the 400-case bridge with
  H0/H1/H2/H3 each at `100` unique cases before calibration/held-out roles are
  assigned
- calibration-ranked held-out model-selection leader:
  `finite_width_sheet + extra_count`, held-out 4-way acc about `0.942`
- held-out H0/H1 trade-off best row:
  `finite_width_sheet + h0_conservative`, held-out H0/H1/4-way acc about
  `1.000` on this mini split
- repeated-split model-selection stability leader:
  `finite_width_sheet + h0_conservative`, top-1 selection rate `1.000`,
  heldout objective about `0.783 ± 0.019`, held-out H0 mean about `0.965`,
  held-out H1 mean about `0.677`
- PyPEEC distribution target coverage: H0 `100/100`, H1 `100/100`,
  H2 `100/100`, H3 `100/100`
- PyPEEC bridge after global registration search: about `0.724`
- hidden unknown rejection rate: about `1.000`
- clean OOD risk-coverage accuracy at 20% coverage: about `1.000`
- combined unknown detector hidden rejection at 20% clean false reject: about `0.677`
- combined unknown-safety accepted hidden accuracy: about `0.774`
- combined physical unknown score hidden rejection: about `0.698`; accepted
  hidden accuracy about `0.655`
- accepted-hidden risk: `combined_unknown_score` hidden accept rate about
  `0.323` with accepted hidden risk about `0.226`; `combined_physical_unknown_score`
  hidden accept rate about `0.302` with accepted hidden risk about `0.345`
- best joint two-state OOD accuracy: about `0.940`
- best label-free multi-state design policy: `h0_disambiguation`
- 80 µm translation stress base/global accuracy: about `0.594` / `1.000`
- 15/30 µm standoff stress base accuracy: about `0.406` / `0.312`;
  global xy registration does not recover it.
- 10/20 mrad tilt stress base accuracy: about `0.844` / `0.812`

Small numeric drift is acceptable if gates still pass and the validation-only
selection protocol is unchanged.
