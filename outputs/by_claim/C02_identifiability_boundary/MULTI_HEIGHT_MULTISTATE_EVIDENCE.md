# E13 Multi-Height Multi-State Observability Evidence

Claim: `C02_single_plane_identifiability_boundary`.

## Summary

Generated-domain evidence shows that multi-height and multi-state observations improve
the identifiability of multilayer current inversion:

- **Effective rank**: not worse across heights (stable at ~10).
- **Multi-state gain**: hypothesis margin improves ~24% from 1 to 4 excitation states.
- **Multi-height**: condition number degrades slightly (173→198) but separability margin holds.
- **Bxyz vs Bz**: Bxyz is not worse than Bz alone (within 0.5%).
- **Graph prior**: reduces layer misallocation by ~1.4x.

## Evidence Package

- `experiments/evidence/E13_multi_height_multistate_observability/`
- `experiments/evidence/E13_multi_height_multistate_observability/outputs/metrics.json`
- `experiments/evidence/E13_multi_height_multistate_observability/outputs/OBSERVABILITY_TABLE.md`
- `experiments/evidence/E13_multi_height_multistate_observability/outputs/IDENTIFIABILITY_GAIN_TABLE.md`

## Boundary

This is generated-domain evidence only. It cannot claim:
- Arbitrary real multilayer recovery
- Real QDM/NV validation
- Hardware-feasible active measurement
