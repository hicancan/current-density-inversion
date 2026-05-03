"""Two-layer + via toy circuit geometry and finite-volume topology maps."""
from __future__ import annotations

import numpy as np
from forward.segments import Segment


def build_two_layer_via_segments(
    current_A: float,
    layer1_z_m: float,
    layer2_z_m: float,
    via_x_m: float,
    via_y_m: float,
    left_port_x_m: float,
    right_port_x_m: float,
    route_y_m: float,
) -> list[Segment]:
    """Build a minimal current path: L1 left -> via -> L2 right.

    Current direction:
    - layer 1: left port to via, +x direction
    - via: layer1 z down to layer2 z
    - layer 2: via to right port, +x direction
    """
    return [
        Segment((left_port_x_m, route_y_m, layer1_z_m), (via_x_m, via_y_m, layer1_z_m), current_A, "L1_trace", "layer1"),
        Segment((via_x_m, via_y_m, layer1_z_m), (via_x_m, via_y_m, layer2_z_m), current_A, "via_1_to_2", "via"),
        Segment((via_x_m, via_y_m, layer2_z_m), (right_port_x_m, route_y_m, layer2_z_m), current_A, "L2_trace", "layer2"),
    ]


def nearest_index(coords: np.ndarray, value: float) -> int:
    return int(np.argmin(np.abs(coords - value)))


def finite_volume_route_maps(
    fov_m: float,
    n: int,
    current: float,
    via_x_m: float,
    via_y_m: float,
    left_port_x_m: float,
    right_port_x_m: float,
    route_y_m: float,
):
    """Build simple finite-volume divergence and topology residual maps.

    The map is not used to generate fields; it is a discrete topology sanity check.
    Edge flux U is positive eastward.  A path on layer 1 ends at the via, and a
    path on layer 2 begins at the via.
    """
    x = np.linspace(-fov_m / 2, fov_m / 2, n)
    y = np.linspace(-fov_m / 2, fov_m / 2, n)
    dx = float(x[1] - x[0])
    iy = nearest_index(y, route_y_m)
    ix_v = nearest_index(x, via_x_m)
    ix_l = nearest_index(x, left_port_x_m)
    ix_r = nearest_index(x, right_port_x_m)

    # Edge fluxes U have shape (n, n+1), V has shape (n+1, n).
    U1 = np.zeros((n, n + 1), dtype=float)
    V1 = np.zeros((n + 1, n), dtype=float)
    U2 = np.zeros_like(U1)
    V2 = np.zeros_like(V1)

    # L1: left -> via. L2: via -> right.
    if ix_l < ix_v:
        U1[iy, ix_l + 1 : ix_v + 1] = current
    else:
        U1[iy, ix_v + 1 : ix_l + 1] = -current
    if ix_v < ix_r:
        U2[iy, ix_v + 1 : ix_r + 1] = current
    else:
        U2[iy, ix_r + 1 : ix_v + 1] = -current

    div1 = (U1[:, 1:] - U1[:, :-1] + V1[1:, :] - V1[:-1, :]) / dx
    div2 = (U2[:, 1:] - U2[:, :-1] + V2[1:, :] - V2[:-1, :]) / dx

    # s is positive from layer1 to layer2; convert edge current to divergence density.
    s = np.zeros((n, n), dtype=float)
    s[iy, ix_v] = current / dx
    res1 = div1 + s
    res2 = div2 - s

    inner = np.ones((n, n), dtype=bool)
    # Ignore port cells because current can enter/exit the measured FOV there.
    inner[iy, ix_l] = False
    inner[iy, ix_r] = False
    # Also ignore a one-cell outer border.
    inner[[0, -1], :] = False
    inner[:, [0, -1]] = False

    J1_vis = np.zeros((n, n), dtype=float)
    J2_vis = np.zeros((n, n), dtype=float)
    # Put a visual current magnitude on cells along the paths.
    c0, c1 = sorted([ix_l, ix_v])
    J1_vis[iy, c0 : c1 + 1] = current
    c0, c1 = sorted([ix_v, ix_r])
    J2_vis[iy, c0 : c1 + 1] = current

    return {
        "x": x,
        "y": y,
        "dx": dx,
        "via_index": (iy, ix_v),
        "left_index": (iy, ix_l),
        "right_index": (iy, ix_r),
        "J1_vis": J1_vis,
        "J2_vis": J2_vis,
        "div1": div1,
        "div2": div2,
        "s": s,
        "res1": res1,
        "res2": res2,
        "inner_mask": inner,
    }


def make_random_toy_segments(rng: np.random.Generator, fov_m: float, current_A: float, layer1_z: float, layer2_z: float):
    """Generate a random but simple L1-via-L2 horizontal route."""
    margin = 0.25 * fov_m
    x_v = rng.uniform(-0.2 * fov_m, 0.2 * fov_m)
    y_v = rng.uniform(-0.25 * fov_m, 0.25 * fov_m)
    left_x = -0.5 * fov_m + margin * rng.uniform(0.4, 1.0)
    right_x = 0.5 * fov_m - margin * rng.uniform(0.4, 1.0)
    I = current_A * rng.uniform(0.5, 1.5) * (1 if rng.random() > 0.15 else -1)
    return build_two_layer_via_segments(I, layer1_z, layer2_z, x_v, y_v, left_x, right_x, y_v), (x_v, y_v, I)
