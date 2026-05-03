# Research Graph SSOT

The graph is the project control plane. It records the current research state,
claim boundaries, evidence relations, and next required evidence.

It is not a replacement for measurements, code, metrics, or plots. It is the
index that keeps those artifacts tied to claims and prevents unsupported
generalization.

## Node Layers

```text
Claim
  Data distribution
  Physics constraint
  Forward solver
  Observation model
  Representation
  Algorithm
  Protocol
  Metric
  Evidence
  Failure mode
  Boundary / Cannot-claim
```

## Required Update Events

Update this graph after any of these events:

- a new claim is proposed;
- a claim status changes;
- a data distribution, solver, observation model, algorithm, protocol, or
  metric is added;
- a study produces new results;
- a failure mode or overclaim risk is discovered;
- external solver evidence or real measurement evidence is added;
- the next best evidence loop changes.

No update is required for formatting-only or refactor-only changes that do not
alter claims, evidence, metrics, protocols, or data nodes.

