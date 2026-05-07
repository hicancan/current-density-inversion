# Failure Modes

- Generated-domain centerline Biot-Savart/KCL evidence only.
- Pad sets are generated from the known candidate defect library; no hidden
  layout-family generalization is proven.
- The positive pad-Schur result uses top-surface candidate-projection pads. It
  does not prove that perimeter-only ports work.
- Real pad parasitics, contact resistance, finite conductor width, current
  limits, frequency dependence, external solver gaps, and real sensor nuisance
  are not validated.
- A positive pad-Schur Gamma is not real chip reverse analysis before CAD/GDS
  graph import, independent solver validation, and real QDM/NV sanity gates.

