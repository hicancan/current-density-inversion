"""Physical constants for E25 volume forward Biot-Savart computations.

All units SI.
"""
from __future__ import annotations

import math

MU0 = 4.0 * math.pi * 1.0e-7           # vacuum permeability [N/A²]
MU0_OVER_4PI = 1.0e-7                   # µ₀/(4π) [N/A²]
EPS = 1e-30                             # numerical floor
MIN_RHO = 1e-12                         # minimum perpendicular distance [m]
