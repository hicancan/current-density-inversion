# OOD Refusal Evidence

Claim: `C08_ood_refusal_safety`.

| Evidence | Result | Boundary |
|---|---|---|
| feature-distance refusal | Screens generated hidden/out-of-library stress more safely than confidence alone. | Generated hidden stress only. |
| near-boundary hidden rows | Harder rows are partly rejected and must be audited when accepted. | Primary-label correctness is insufficient. |
| hidden severity curve | Refusal can be tracked as severity varies. | Not real unknown safety. |
| accepted-hidden risk | Accepted hidden risk is a primary endpoint. | Hidden rejection rate alone is not enough. |

Cannot claim: deployment-safe unknown detection.

