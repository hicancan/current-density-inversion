# Real QDM/NV Sanity Protocol

No real-data diagnosis claim can be made before the following gates pass.

## Required Metadata

- field units;
- component order;
- pixel pitch;
- sensor standoff;
- sensor pose and coordinate frame;
- current injection ports;
- background/reference path;
- sample geometry notes;
- measurement date and acquisition settings.

## Required Array Gates

- arrays are finite;
- component order is explicit;
- units are convertible to Tesla;
- background subtraction preserves the original field file;
- `Bx`, `By`, and `Bz` signs are inspected against a simple known structure.

## Required Simple-Structure Gates

At least one of:

- one-wire known-current sanity;
- two-wire differential-current sanity;
- known-via coupon;
- known-good no-via region.

## Cannot Claim Before Passing

- via/no-via diagnosis;
- return-path reconstruction;
- CAD/Gerber-guided inference;
- comparison to generated-domain calibrator metrics.

