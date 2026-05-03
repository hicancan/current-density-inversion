# Strict No-Via Detector No-Leakage Protocol

## Purpose

The PyPEEC no-via false-positive diagnostics expose a real failure mode, but
the PyPEEC mini stress set must not be used to tune thresholds. This protocol
defines how a no-via confidence gate can be developed without leaking PyPEEC
test information into calibration.

## Current Frozen Boundary

Current PyPEEC frozen inference artifacts must keep these flags false:

- `used_for_training`
- `used_for_validation_thresholds`
- `used_for_calibration`

Current PyPEEC no-via and return-path tables are diagnostic only. They may be
used to describe failure mechanisms, select future experiment families, and
design held-out protocols. They must not be used to pick a detector threshold
that is then reported on the same PyPEEC cases as an unbiased frozen result.

The implemented null-via hypothesis gate follows the Stage 2 route below: it
selects parameters on synthetic validation stress only, freezes those parameters,
and then reports PyPEEC before/after plus Pareto trade-offs. PyPEEC cases are
not used for threshold selection or calibration.

The current H0/H1 evidence, uncertainty/refusal, and return-path hypothesis
tables are also frozen diagnostics. They may be used to explain ambiguity and
define future protocols, but they do not update predictions or choose a PyPEEC
operating point.

## Forbidden

- Do not lower or raise via-presence thresholds by inspecting PyPEEC test
  false positives.
- Do not tune bend/corner suppression radii on the current PyPEEC test cases.
- Do not tune return-path suppression rules on the current PyPEEC test cases.
- Do not select model checkpoints, lambdas, or post-processing blends by
  optimizing PyPEEC mini stress metrics.
- Do not report a PyPEEC result as frozen if any PyPEEC sample influenced the
  threshold, rule, calibration split, or checkpoint.

## Allowed Stage 1: Diagnosis Only

Allowed on the current PyPEEC mini stress set:

- classify false positives by mechanism;
- plot representative failures;
- report distances to trace, bend, return masks, and field-gap metrics;
- compare no-topology, topology, and two-stage rows without changing them;
- write claims that the failure is understood better, not solved.

## Allowed Stage 2: Synthetic Validation Stress

A no-via confidence gate may be tuned on synthetic validation-only stress
families that are generated without reading PyPEEC test labels or PyPEEC test
metrics:

- no-via bend/corner operator-gap stress;
- no-via finite-width mismatch stress;
- no-via return-path-like background stress;
- no-via correlated noise and PSF stress;
- no-via edge/FOV-boundary stress.
- matched true-via versions of the same stress families, so false-positive
  suppression cannot be selected without also measuring recall loss.

A valid detector rule can use validation-selected parameters such as:

- `s1` peak-to-background ratio;
- residual energy significance;
- topology improvement after introducing `s1`;
- physical re-forward degradation after introducing `s1`;
- distance-to-bend suppression;
- distance-to-return suppression;
- uncertainty or ensemble disagreement.

After selection, the entire rule must be frozen before PyPEEC evaluation.

The current evidence-comparison diagnostic may be reported under this stage
only if it keeps all PyPEEC current-use flags false and is described as
confidence/refusal evidence rather than a PyPEEC-calibrated detector.

## Allowed Stage 3: Held-Out PyPEEC Calibration

If PyPEEC samples are used for calibration, the dataset must be explicitly
split before looking at results:

- `pypeec_calibration`: allowed for threshold/rule selection;
- `pypeec_test`: held out until the final report.

The report must state:

- how many PyPEEC cases were used for calibration;
- which case families were included;
- which thresholds or rules were selected;
- that held-out test cases were not inspected during selection.

Metrics from a PyPEEC-calibrated protocol must not be mixed with frozen
no-calibration metrics. They should live in a separate table with
`used_for_calibration = true`.

The current `PYPEEC_HELDOUT_SPLIT_PROTOCOL.md` is a reserved future split only.
It does not license tuning on the current PyPEEC rows unless a later experiment
changes the protocol, separates calibration from held-out test, and reports
`used_for_calibration = true`.

## Null-Hypothesis Gate Template

A future no-via detector should compare at least two hypotheses:

- `H0`: no via/source-sink; residual is explained by sheet current,
  finite-width/centerline mismatch, bend/corner geometry, return path, or noise.
- `H1`: a true via/source-sink is required to explain the observation.

A conservative gate should keep a via candidate only when:

1. `s1` evidence is large relative to local background;
2. adding the via materially reduces topology residual;
3. adding the via does not materially worsen physical re-forward residual;
4. the peak is not inside a bend/corner or return-path artifact zone unless
   the physical evidence is strong;
5. uncertainty is low enough to make a hard decision.

## Reporting Standard

Every future no-via mitigation table must include:

- `used_for_training`;
- `used_for_validation_thresholds`;
- `used_for_calibration`;
- calibration split name;
- held-out split name;
- threshold/rule values;
- no-via false-positive rate;
- via recall/F1 trade-off;
- worst-case IDs.

## Current Claim Boundary

The current repository supports:

> PyPEEC no-via false positives can be diagnosed and are mostly associated with
> bend/corner-induced residuals in the current mini stress set.

> A null-via hypothesis gate can be selected without PyPEEC test leakage and
> evaluated as frozen PyPEEC before/after and Pareto trade-offs.

It does not yet support:

> PyPEEC no-via false positives are solved.
