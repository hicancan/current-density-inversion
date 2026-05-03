# Stacked Evidence Calibration

Claim: `C07_stacked_evidence_calibration`.

| Evidence | Result | Boundary |
|---|---|---|
| stacked evidence fusion | Legal calibration/held-out fusion improves H0/H1/H2/H3 diagnosis in generated PyPEEC-domain rows. | Calibration is required. |
| feature ablation | Improvements come from evidence fusion, not one scalar threshold. | Feature sources are still generated-domain evidence. |
| group heldout | Variant-heldout is stronger than pure family leaveout. | Family generalization remains limited. |
| selective risk reporting | Refusal remains part of the system design. | Low-coverage accuracy is not full-coverage deployment. |

Cannot claim: no-calibration deployment or real-world calibration transfer.

