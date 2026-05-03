# Exp08 P3 disciplined model-bank allowed-basis table

| hypothesis | allowed evidence/basis | restricted basis | reason |
| --- | --- | --- | --- |
| H0_sheet_only | sheet + finite_width_sheet | return_bank / artifact_bank / distributed_via | Protect no-via against residual-only over-explanation. |
| H1_sheet_via | sheet + finite_width_sheet + compact/distributed via | artifact_bank unless explicitly diagnosed | Keep true-via evidence separate from bend/corner artifacts. |
| H2_sheet_return | sheet + finite_width_sheet + return_bank | distributed_via as a first explanation | Return-current mismatch is a physical nuisance, not a via by default. |
| H3_sheet_artifact | sheet + finite_width_sheet + artifact_bank | return_bank unless route metadata supports it | Bend/corner residuals should compete with via, not silently become via. |
| unknown/refusal | all evidence families as diagnostic scores | label-changing calibration on PyPEEC frozen rows | Reject or defer when model evidence is not identifiable. |

This table states the model-bank discipline explicitly: richer bases must compete as hypotheses and should not be silently admitted to every class.
