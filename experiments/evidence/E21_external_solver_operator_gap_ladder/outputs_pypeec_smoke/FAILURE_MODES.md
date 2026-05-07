# Failure Modes

## Blocked Validation Paths

- External solver (COMSOL/FastHenry/FEM) validation: BLOCKED — no artifact files loaded.
- PyPEEC operator: available (generated-domain evidence only).

## Known Limitations

- All operators are generated-domain; no real CAD/GDS or QDM/NV data.
- PyPEEC bridge is generated-domain higher-fidelity, not ground truth.
- Decision instability is measured on toy current prediction, not full hypothesis scoring.
