# E14 Layout Graph Import Scaffold

Evidence package for CAD/Gerber/GDS-like layout graph import scaffold.

Claims: `C06_graph_hypothesis_system_identification`, `C10_pdn_kcl_distribution_need`.

## Status

Generated scaffold. Not real CAD/Gerber/GDS validation.

## What it does

- Parses simplified JSON/YAML layout schemas
- Converts layout to route graph, via candidate graph, layer stack, net/port graph, return candidates
- Generates H0/H1/H2/H3 hypothesis candidates from extracted graph
- Produces metrics.json, graph summaries, and KCL proxy residuals

## Cannot claim

- Real CAD/Gerber/GDS validation
- Real QDM/NV validation
- External FEM/FastHenry validation
- Real layout import
