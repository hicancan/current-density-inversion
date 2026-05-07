# Failure Modes

Documented operator-boundary findings from E25.

## all_gates_passed
- Severity: info
- Description: All acceptance gates passed.
- Gate status: True

## four_layer_volume_overlap
- Severity: warning
- Description: four_layer_via_return_motif has overlapping conductor volumes at via-trace junctions. Quadrature diverges for this geometry (relative change up to 1515%). Recommend splitting conductors at junctions to avoid volume overlap. Affects worst-case rho estimate (drives combined conservative rho to 2.2x signal).
- Gate status: False

## quadrature_convergence_is_geometry_dependent
- Severity: info
- Description: Quadrature convergence to <5% is achieved for simple non-overlapping geometries (vertical_via best: 3.7e-6). For more complex geometries at moderate quadrature orders, relative changes of 8-13% are typical (straight_strip: 8.7%, two_layer: 13.1%). The median relative change across all 162 levels is 37.6%, driven by low-order and overlapping configurations.
- Gate status: True
