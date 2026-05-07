# E23 CAD/GDS-Derived Graph-Hodge Current Basis

Status: design document only, not evidence.

Owner model: Codex designs and audits; Claude Code implements in an isolated
worktree with `--effort max`.

## Purpose

Pixel current inversion is too unconstrained. E14 introduced a layout graph
import scaffold, but the core breakthrough is not merely parsing layout-like
data. The breakthrough is to transform layout/PDN structure into a physically
admissible current basis:

```text
layout graph -> ports/nets/vias/returns -> Graph-Hodge current basis ->
magnetic forward operator -> OQCI claim intervals
```

E23 should create a first runnable CAD/GDS-like Graph-Hodge basis pipeline that
restricts the inverse problem to current modes that respect graph topology,
KCL, ports, vias, return paths, and residual off-graph explanations.

This changes the admissible current space `A`, one of the fundamental levers
for magnetic-current inversion.

## Affected Claim

Primary:

- `C06_graph_hypothesis_system_identification`
- `C10_pdn_kcl_distribution_need`

Secondary:

- `C02_single_plane_identifiability_boundary`
- `C04_inverse_crime_and_operator_gap`
- `C11_mechanism_level_explanation`

## Involved Nodes

Data:

- `D09_cad_gerber_gds_like`
- `D11_chip_like_generated_pdn_family`

Physics:

- `P01_biot_savart_maxwell_forward`
- `P04_divJ_source_sink_consistency`
- `P05_kcl_node_conservation`
- `P06_kvl_or_resistive_network_consistency`
- `P07_current_closure_loop`
- `P08_return_path_completeness`

Forward:

- `F02_centerline_biot_savart`
- optional future: `F05_comsol_fem`, `F06_fasthenry`

Observation:

- `O01_ideal_Bxyz`
- `O08_multi_height`
- `O09_multi_state_excitation`

Representation:

- `R04_route_graph`
- `R06_pdn_circuit_graph`
- `R08_hypothesis_set`
- `R09_posterior_candidate_set`
- `R10_multilayer_chip_like_pdn_graph`

Algorithm:

- `A04_hypothesis_scorer`
- `A08_differentiable_forward_optimization`
- `A12_bayesian_or_glrt_model_evidence`
- `A14_pdn_physics_aware_learner`

Protocol:

- `S03_family_heldout`
- `S11_no_leakage_calibration_heldout`
- `S12_conformal_or_selective_risk_protocol`

Metrics:

- `M01_field_l2_or_rmse`
- `M03_topology_residual`
- `M04_kcl_residual`
- `M08_accepted_accuracy`
- `M09_accepted_risk`
- `M10_reject_rate`
- `M13_family_generalization_gap`
- `M16_predicted_kcl_residual`
- `M17_predicted_current_closure_error`

## First-Principles Formulation

Let a layout-derived graph be:

```text
G = (V, E, L, N, P)
```

where:

- `V` are junctions, ports, via endpoints, and load nodes;
- `E` are trace, plane, via, return, and residual candidate edges;
- `L` maps edges and nodes to physical layers and coordinates;
- `N` maps graph elements to nets;
- `P` defines ports, known excitations, and boundary conditions.

Let `D` be the node-edge incidence matrix. KCL requires:

```text
D i = q
```

where `q` is source/sink injection. For homogeneous interior nodes:

```text
D_interior i = 0
```

The admissible current basis should decompose into:

```text
H = [H_port, H_loop, H_via, H_return, H_harmonic, H_gap, H_residual]
```

with:

- `H_port`: source-to-sink port currents;
- `H_loop`: cycle-space currents with zero divergence;
- `H_via`: candidate vertical transfer modes;
- `H_return`: explicit return-path modes;
- `H_harmonic`: boundary or hole modes;
- `H_gap`: structured model-gap modes;
- `H_residual`: low-rank off-layout unknown current modes.

The magnetic forward under a measurement family is:

```text
B = A H
```

OQCI then asks which claims are forced over the low-dimensional coefficient
space, rather than over unconstrained pixels.

## Algorithm Steps

1. Import or reuse layout-like examples:
   - start from E14 simplified JSON/YAML layout schema;
   - optionally add a minimal GDS/Gerber-like adapter only if it can be done
     cleanly without overclaiming real CAD validation.
2. Build graph objects:
   - nodes;
   - directed edges;
   - layer stack;
   - nets;
   - ports;
   - via candidates;
   - return candidates.
3. Construct incidence matrix `D`.
4. Build basis blocks:
   - port basis by solving `D i = q`;
   - loop basis from nullspace of `D`;
   - via basis from candidate cross-layer edges;
   - return basis from designated return net paths;
   - residual/gap basis from coarse off-layout patterns.
5. Validate physical basis:
   - KCL residual;
   - current closure;
   - layer and net consistency;
   - basis rank and block dimensions.
6. Forward project basis to magnetic fields.
7. Run a minimal OQCI audit:
   - compare unconstrained pixel/ridge baseline versus graph-Hodge basis;
   - report ambiguity and claim intervals;
   - report when graph prior overconstrains or hides mechanisms.
8. Write reports and proposed graph snippets.

## Expected Evidence Package

Target package:

```text
experiments/evidence/E23_cad_gds_graph_hodge_basis/
```

Suggested files:

```text
README.md
DESIGN.md
requirements.txt
configs/
  smoke.json
  default.json
examples/
  simple_two_layer_layout.json
  four_layer_pdn_layout.json
src/
  __init__.py
  config.py
  layout_schema.py
  graph_builder.py
  incidence.py
  hodge_basis.py
  forward.py
  oqci_adapter.py
  metrics.py
  reporting.py
  run_all.py
tests/
  test_layout_schema.py
  test_incidence.py
  test_hodge_basis.py
  test_kcl_closure.py
  test_run_outputs.py
outputs/
  .gitkeep
research_graph_patch/
  snippets.md
```

## Metrics and Gates

Required metrics:

```text
layout_count
graph_node_count
graph_edge_count
layer_count
net_count
port_count
via_candidate_count
return_candidate_count
basis_total_dim
basis_port_dim
basis_loop_dim
basis_via_dim
basis_return_dim
basis_residual_dim
max_kcl_residual
max_current_closure_error
basis_rank
operator_rank
graph_prior_ambiguity_rate
unconstrained_ambiguity_rate
ambiguity_rate_delta
wrong_high_confidence_accept_count
```

Engineering gates:

- all example layouts parse;
- incidence matrix shape is valid;
- basis blocks have expected dimensions;
- KCL residual is below tolerance for constrained blocks;
- current closure is reported;
- reports are written;
- cannot-claim boundaries are present.

Scientific gates:

- graph-Hodge basis reduces admissible dimension relative to pixels;
- basis does not collapse to zero or rank-deficient triviality;
- at least one claim interval changes under graph prior, or a negative result
  is documented;
- no wrong high-confidence accepts;
- residual basis is present so missing paths can be represented.

## Reports

Required outputs:

```text
outputs/metrics.json
outputs/RUN_REPORT.md
outputs/GRAPH_IMPORT_SUMMARY.md
outputs/HODGE_BASIS_AUDIT.md
outputs/KCL_CLOSURE_AUDIT.md
outputs/OQCI_GRAPH_PRIOR_AUDIT.md
outputs/FAILURE_MODES.md
```

## Cannot Claim

E23 cannot claim:

- real CAD/GDS validation unless real layout files are imported and audited;
- real QDM/NV validation;
- external solver validation;
- mechanism-level explanation from graph-prior correctness;
- that graph-Hodge priors are safe without residual/gap modes.

E23 can claim only:

- generated or simplified layout-derived Graph-Hodge basis construction;
- KCL/closure/basis-rank properties for those examples;
- generated-domain OQCI effects of the graph prior.

## Claude Worker Scope

Implement only:

```text
experiments/evidence/E23_cad_gds_graph_hodge_basis/
```

Do not edit global research graph SSOT files. Put proposed snippets under
`research_graph_patch/snippets.md`.

Run at minimum:

```powershell
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
```

If feasible:

```powershell
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

Final worker report must include files changed, commands run, metrics, failure
modes, cannot_claim, and next required evidence.

