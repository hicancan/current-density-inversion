# Research Graph Design

The research graph is the scientific source of truth.

## Files

- `claims.yml`: claim status, scope, boundaries, and next evidence.
- `nodes.yml`: data, physics, solver, observation, representation, algorithm,
  protocol, and metric nodes.
- `experiments.yml`: runnable evidence packages and their output contracts.
- `evidence_edges.yml`: machine-readable claim/evidence relations.
- `artifacts.yml`: tracked reports, metrics, protocols, and schemas.
- `open_questions.md`: unresolved scientific blockers.
- `overclaim_guardrails.md`: statements the repository must not make.
- `update_log.md`: auditable change history.

## Claim Gates

Supported and limited claims must have linked evidence. Generated-domain support
must include `cannot_claim` and limitations. Real validation claims cannot be
supported by synthetic, generated, or PyPEEC-domain evidence.

## Evidence Edges

Use edge relations conservatively:

- `supports`: evidence directly supports the scoped claim.
- `limits`: evidence narrows or bounds the claim.
- `contradicts`: evidence falsifies or conflicts with a claim.
- `requires`: evidence defines a required gate before claim support is possible.
- `motivates`: evidence motivates a next claim or evidence loop.

`limited_by` and `contradicted_by` in `claims.yml` must correspond to `limits`
and `contradicts` edges.

## Metrics

Each evidence metrics file must be a non-empty JSON object with:

- `schema_version: research-ssot-metrics-v1`
- a machine-readable acceptance gate;
- `leakage_audit`;
- enough paths or summaries for `RUN_REPORT.md` to be audited.

