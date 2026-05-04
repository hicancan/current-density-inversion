# Evidence Package Contract

Each runnable evidence package should be self-contained enough for an agent to
run, test, and audit without guessing hidden conventions.

## Required Files

- `README.md`
- `REPRODUCE.md`
- `METRICS_SCHEMA.md`
- `FAILURE_MODES.md`
- `requirements.txt`
- `configs/default.json` for runnable packages
- `tests/`
- `outputs/metrics.json` when evidence status is not `planned`

## Metrics Contract

`outputs/metrics.json` should include:

- `evidence_id`
- `claim_id`
- `status`
- `dataset`
- `split_roles`
- `acceptance_gates`
- `cannot_claim`
- `generated_at`

Legacy packages may not yet include every common field, but every non-planned
package must expose a recognized acceptance gate.

## Artifact Registration

Claim-supporting metrics and reports should be registered in
`research_graph/artifacts.yml` with path, claim, evidence, role, tracked state,
generation command, and calibration permission.

Ignored generated data should not be used to support a claim unless it can be
regenerated from a registered evidence package and its supporting tracked
metrics/report artifacts exist.

