# E09 Real Data Intake Gate Run Report

This is an interface/scaffold run only. It validates metadata, component order,
units, background protocol, strict-path defaults, the NPZ loader stub, and the
simple-wire sanity utility. It does not load measured QDM/NV rows and cannot
support real via/no-via diagnosis.

Metrics file: `outputs/metrics.json`

| Gate | Pass |
|---|---|
| background_protocol_validation | True |
| background_subtraction_stub_callable | True |
| claim_boundary_real_data_interface_only | True |
| component_order_validation | True |
| metadata_template_valid | True |
| no_real_rows_present | True |
| npz_loader_stub_callable | True |
| simple_wire_sanity_stub_callable | True |
| strict_paths_default_off | True |
| units_validation | True |

## Claim Boundary

- C12_real_qdm_nv_validation remains blocked.
- No real rows are present.
- This run is `passed_interface`, not real validation.

## Agent Audit Metadata

- Metrics file: `outputs/metrics.json`
- Schema version: `research-ssot-metrics-v1`
- Calibration source: No measured rows present; interface scaffold only.
- Threshold source: none
- Model-selection source: not_applicable
- Audit date: 2026-05-04
