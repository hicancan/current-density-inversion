# Research Graph SSOT

The graph is the project control plane. It records the current research state,
claim boundaries, evidence relations, and next required evidence.

It is not a replacement for measurements, code, metrics, or plots. It is the
index that keeps those artifacts tied to claims and prevents unsupported
generalization.

Agent-facing additions:

- `artifacts.yml` registers metrics, reports, protocol files, and other
  claim-linked artifacts.
- `agent_queue.yml` records the next claim-safe work items for Codex/agent
  execution.
- `schemas/` stores minimal JSON Schemas for graph files; the Python validator
  remains the authoritative local checker.

Current generated PDN control path:

- `E10_pdn_kcl_distribution`: first runnable generated resistive PDN/KCL loop.
- `E11_chip_like_pdn_distribution`: four-layer chip-like generated PDN family.
- `E12_pdn_physics_learning`: CPU generated-domain physics-learning closure.

These evidence packages strengthen generated-domain claims only. They do not
upgrade any claim to real CAD/GDS, external solver, real chip, or real QDM/NV
validation.

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
- a metrics/report artifact is added, moved, or retired;
- the agent queue changes priority, status, or blocking conditions;
- a failure mode or overclaim risk is discovered;
- external solver evidence or real measurement evidence is added;
- the next best evidence loop changes.

No update is required for formatting-only or refactor-only changes that do not
alter claims, evidence, metrics, protocols, or data nodes.
