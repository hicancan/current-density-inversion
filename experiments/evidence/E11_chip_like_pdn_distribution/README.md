# E11 Chip-Like Multilayer PDN Distribution

Claim: `C10_pdn_kcl_distribution_need`.

This package generates a finite, generated-domain, chip-like multilayer PDN
distribution. It extends the E10 resistive graph loop from a toy path into a
four-layer micro-PDN with top power straps, intermediate mesh layers, a lower
return grid, via stacks, distributed loads, bumps/ports, edge resistance, KCL
solves, current closure checks, and centerline Biot-Savart `Bxyz` fields.

It remains generated evidence only. It cannot validate real chips, real
CAD/Gerber/GDS layouts, external FEM/FastHenry solves, or real QDM/NV data.

## Evidence Contract

- `configs/default.json`: deterministic generated-domain run settings.
- `src/run_all.py`: generator, KCL solver, forward field, gates, and exports.
- `outputs/metrics.json`: acceptance gates and scientific metrics.
- `outputs/RUN_REPORT.md`: human-readable audit report.
- `data/e11_dataset.json`: generated rows for downstream E12 learning runs.
- `data/e11_fields.npz`: generated `Bxyz` field arrays.

