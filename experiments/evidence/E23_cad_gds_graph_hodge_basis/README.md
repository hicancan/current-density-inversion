# E23 CAD/GDS-Derived Graph-Hodge Current Basis

Claim: `C06_graph_hypothesis_system_identification`, `C10_pdn_kcl_distribution_need`

Status: Generated-domain evidence. Not real CAD/GDS validation.

## What it does

Constructs a Graph-Hodge current basis from layout-derived graphs and uses it to constrain the admissible current space for magnetic-current inversion.

Pipeline:
1. Load layout examples (E14 simplified JSON layout schema)
2. Build graph objects (nodes, edges, layer stack, nets, ports, via/return candidates)
3. Construct node-edge incidence matrix D
4. Build Hodge basis blocks: port, loop, via, return, harmonic, gap, residual
5. Validate physical basis (KCL residual, current closure, basis rank, block dimensions)
6. Forward-project basis vectors through centerline Biot-Savart
7. Run minimal OQCI audit comparing unconstrained vs. graph-Hodge ambiguity

## Cannot claim

- Real CAD/GDS validation (no real layout files are imported)
- Real QDM/NV validation
- External solver validation (no COMSOL/FastHenry/FEM)
- Mechanism-level explanation from graph-prior correctness
- That graph-Hodge priors are safe without residual/gap modes

## Reproduce

```powershell
# Smoke run
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
# Default run
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
# Tests
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
```
