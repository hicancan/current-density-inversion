# BiotSavartForwardLayer API

## Constructor: BiotSavartForwardLayer(nx, ny, dx, dy)

## Methods: sheet_to_B, via_to_Bxy, multilayer_sum_B, sheet_to_B_torch

## Transfer Functions (dz=z_obs-z_source):
- T_Bx_Jy = (mu0/2)*sign(dz)*exp(-k*|dz|) for k>0, = (mu0/2)*sign(dz) for k=0
- T_By_Jx = -(mu0/2)*sign(dz)*exp(-k*|dz|) for k>0, = -(mu0/2)*sign(dz) for k=0
- T_Bz = (i*mu0/2)*exp(-k*|dz|)*(kx*Jy-ky*Jx)/k for k>0, = 0 for k=0

## Known Limitations: periodic BC (use padding_factor>=2), thin-sheet, no material effects.
