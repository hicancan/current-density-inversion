# No-Leakage Calibration Protocol

## Rule

Held-out, hidden, external-solver, and real-measurement rows must not be used to
select thresholds, evidence weights, feature transforms, model banks, or
hyperparameters unless the protocol explicitly marks those rows as calibration
rows.

## Required Split Roles

Each study must label rows with one of these roles:

| Role | May tune? | May report final metric? | Notes |
|---|---:|---:|---|
| train | yes | no | Model fitting only. |
| calibration | yes | no | Thresholds, evidence fusion, conformal/refusal calibration. |
| validation | yes | no | Model selection when no separate calibration exists. |
| heldout | no | yes | Final in-scope reporting. |
| hidden | no | yes | Out-of-library safety stress only. |
| external | no | yes | External solver or external family stress. |
| real | no, unless separately split | yes | Must pass real-data sanity first. |

## Required Report Fields

- selected thresholds or evidence weights;
- the role used to select each parameter;
- held-out metrics after freezing selection;
- rejected-row rate and accepted-row risk;
- cannot-claim statement.

