# External Artifact Directory

Place COMSOL/FastHenry/FEM exported files here for external solver validation.

## Supported Formats

- `.npz` — Numpy archive with fields `Bx`, `By`, `Bz` (SI units, Tesla)
- `.csv` — Comma-separated field or current data

## COMSOL Convention

File: `comsol_export.npz`
Arrays: `Bx`, `By`, `Bz` of shape `(n, n)` in Tesla.

## FastHenry Convention

File: `fasthenry_export.npz` or `fasthenry_currents.csv`
Array: `currents` of shape `(n_segments,)` in Ampere.

## Without Artifacts

When no external artifacts are present, the package reports a valid
blocked/interface status. No fake validation is claimed.
