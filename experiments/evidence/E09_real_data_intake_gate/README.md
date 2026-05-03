# Exp09 Real QDM/NV Data Interface Stub

Exp09 is not a real-data validation claim yet. This folder is a conservative
interface scaffold for future QDM/NV magnetic-field cases. Its first job is to
make units, component order, background subtraction, sensor pose, and simple
wire sanity checks auditable before any exp08 graph-identification result is
reported on real data.

## Scope

Current scope:

- validate case metadata against a minimal schema;
- load a measured-field `.npz` array with explicit component order and finite
  values;
- plot `Bx/By/Bz` component maps for unit/polarity inspection;
- subtract a zero-current/reference background into a new `.npz` without
  changing the original data;
- compute first-pass simple-wire sanity metrics before any graph-identification
  claim is attempted;
- document the simple one-wire / two-wire sanity protocol required before
  via/no-via diagnosis.

Non-goals:

- no via/no-via diagnosis;
- no return-path reconstruction;
- no CAD/Gerber parser;
- no superiority claim over exp08;
- no real QDM/NV dataset is included.

## Usage

Validate the included metadata template:

```powershell
uv run --with-requirements experiments\evidence\E09_real_data_intake_gate\requirements.txt python experiments\evidence\E09_real_data_intake_gate\src\validate_real_case_metadata.py experiments\evidence\E09_real_data_intake_gate\examples\example_case_template.json
```

Load a future field file after replacing the template paths:

```powershell
uv run --with-requirements experiments\evidence\E09_real_data_intake_gate\requirements.txt python experiments\evidence\E09_real_data_intake_gate\src\load_qdm_npz_stub.py path\to\case.json
```

Plot component maps:

```powershell
uv run --with-requirements experiments\evidence\E09_real_data_intake_gate\requirements.txt python experiments\evidence\E09_real_data_intake_gate\src\plot_B_components.py path\to\case.json --out path\to\B_components.png
```

Subtract a reference/zero-current background configured in the case JSON:

```powershell
uv run --with-requirements experiments\evidence\E09_real_data_intake_gate\requirements.txt python experiments\evidence\E09_real_data_intake_gate\src\background_subtraction_stub.py path\to\case.json --out path\to\B_subtracted.npz
```

Run simple-wire sanity metrics:

```powershell
uv run --with-requirements experiments\evidence\E09_real_data_intake_gate\requirements.txt python experiments\evidence\E09_real_data_intake_gate\src\simple_wire_sanity_stub.py path\to\case.json
```

By default, the validator checks metadata only. Use `--strict-paths` when a real
case should have all referenced files present.

