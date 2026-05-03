# PDN/KCL Minimum Evidence Protocol

## Goal

Build the missing `D08_pdn_kcl_circuit_graph` evidence loop without turning it
into another route-like synthetic benchmark.

## Required Data Fields

- VDD and GND nodes;
- load nodes and port currents;
- via and junction nodes;
- multilayer metal-grid edges;
- return-path edges;
- edge resistance;
- optional capacitance/inductance metadata;
- per-edge current;
- per-node KCL residual;
- current-closure summary.

## Required Physics

- `P05_kcl_node_conservation`;
- `P06_kvl_or_resistive_network_consistency`;
- `P07_current_closure_loop`;
- `P08_return_path_completeness`;
- `P02_divB_zero`.

## Required Metrics

- `M04_kcl_residual`;
- `M05_divB_residual`;
- `M06_h0_false_any`;
- `M07_h1_recall`;
- `M08_accepted_accuracy`;
- `M09_accepted_risk`;
- `M12_calibration_cost`.

## Minimal Evidence Loop

1. Generate a small family of resistive PDN graphs.
2. Solve edge currents under KCL and current closure.
3. Forward the edge currents to `Bxyz`.
4. Build H0/H1/H2/H3 hypotheses with explicit return-path alternatives.
5. Evaluate family-heldout and few-shot calibration.
6. Report failures as limitations, not as discarded rows.

