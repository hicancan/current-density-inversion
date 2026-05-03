# Simple Wire Sanity Protocol

Before any exp08-style graph identification is attempted on real QDM/NV data,
Exp09 must pass a simple-wire sanity protocol.

## Required Checks

1. Load `B_meas` with explicit component order and units.
2. Confirm the array is finite after background handling.
3. Confirm pixel size and field-of-view are consistent with acquisition notes.
4. Record standoff and tilt, or explicitly mark them `unknown`.
5. Fit or compare a one-wire Biot-Savart forward model to verify:
   - sign convention;
   - rough amplitude scale;
   - trace orientation;
   - component ordering.
6. Repeat for a two-trace or return-path control if available.

## Required Report Columns

```text
case_id
field_shape
component_order
units
pixel_size_m
standoff_m_or_unknown
tilt_known
background_protocol
simple_wire_sign_ok
simple_wire_scale_rel_error
allowed_next_step
```

## Claim Boundary

Passing this protocol only means the real data are auditable enough for later
model evaluation. It does not prove via detection, return-path reconstruction,
or graph-system identification on real hardware.
