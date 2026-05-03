# Failure Modes - exp07

## 1. PyPEEC Is Missing Or API-Incompatible

exp07 has no proxy fallback. If the installed `pypeec` package does not expose
`run_mesher_data` and `run_solver_data`, the experiment must fail.

## 2. Voxel Geometry Is Not Face-Connected

PyPEEC solves connected electric components. Diagonal or disconnected route
segments can create isolated voxel components and trigger solver errors. Canonical
cases therefore use Manhattan/face-connected paths.

The exp03-like cases are intentionally represented as single connected routes.
They approximate exp03 route families for solver validation; they are not a full
multi-source or branched benchmark distribution.

## 3. Current Source Misconfiguration

The current-source terminal includes an admittance parameter. A large source
admittance can shunt the intended current and shrink the magnetic field. exp07
sets `source_admittance_s = 0` and gates on the terminal current reported by
PyPEEC.

## 4. Centerline Reference Is Not Ground Truth

The internal Biot-Savart reference is a sanity reference, not a final high-fidelity
truth. Agreement with it is useful, but it does not prove agreement with
FastHenry/FEM/QDM or real hardware.

## 5. Coarse Voxels Can Hide Geometry Error

The current PyPEEC cases use small voxel grids to keep the solver fast. The
adapter now fills conductor cross-sections and runs a small layer-aligned xy
pitch sweep, but high agreement on canonical cases still does not guarantee
convergence for dense vias, wide conductors, ground returns, or package-scale
structures.

The current sweep intentionally keeps z pitch aligned to the two conductor
layers. A full 3D convergence study over larger CAD-like structures remains
missing.

## 6. Solver Validation Is Not Inverse-Model Validation

exp07 does not train or test the topology-aware inverse model. PyPEEC fields must
be explicitly routed back into exp04/exp06 before making inverse-model robustness
claims.
