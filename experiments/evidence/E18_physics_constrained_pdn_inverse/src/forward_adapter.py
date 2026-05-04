"""Forward operator adapter for E18.1.

Builds the Biot-Savart forward operator matrix A mapping
11*n*n current/via channels to 3*m*m sensor field values.

E18.1 FIX: via/source-sink channels (s12, s23, s34) now have nonzero
columns via a vertical-current kernel approximation.
"""
from __future__ import annotations
import numpy as np

MU0_OVER_4PI = 1e-7
LAYER_IDS = ["L1", "L2", "L3", "L4"]
VIA_PAIRS = [("L1", "L2"), ("L2", "L3"), ("L3", "L4")]


def grid_centers(cfg: dict):
    n = int(cfg["grid_size"])
    x0, x1, y0, y1 = cfg["in_plane_extent"]
    xs = np.linspace(x0 + (x1 - x0) / (2 * n), x1 - (x1 - x0) / (2 * n), n)
    ys = np.linspace(y0 + (y1 - y0) / (2 * n), y1 - (y1 - y0) / (2 * n), n)
    return xs, ys, xs[1] - xs[0], ys[1] - ys[0]


def sensor_grid(cfg: dict):
    m = int(cfg["sensor_grid_size"])
    x0, x1, y0, y1 = cfg["in_plane_extent"]
    xs = np.linspace(x0, x1, m)
    ys = np.linspace(y0, y1, m)
    xx, yy = np.meshgrid(xs, ys)
    zz = np.full_like(xx, float(cfg["sensor_z"]))
    return xx, yy, zz, np.stack([xx, yy, zz], axis=-1)


def build_forward_operator(cfg: dict):
    """Build the Biot-Savart forward operator A.

    Returns (A, via_base_index) where A is (3*m*m, 11*n*n) and
    via_base_index is 8*n*n (start of via channels).

    E18.1: Via columns are now nonzero. Each via source/sink channel
    is modelled as a vertical current segment between two layer depths.
    """
    n = int(cfg["grid_size"])
    m = int(cfg["sensor_grid_size"])
    depths = {l: float(cfg["layer_depths"][l]) for l in LAYER_IDS}
    xs, ys, dx, dy = grid_centers(cfg)
    dA = dx * dy
    pts = sensor_grid(cfg)[3].reshape(-1, 3)
    ns = len(pts)
    pl = n * n
    A = np.zeros((3 * ns, 11 * pl))

    # --- Sheet current columns (Jx, Jy per layer) ---
    for li, lid in enumerate(LAYER_IDS):
        z = depths[lid]
        for iy in range(n):
            py = ys[iy]
            for ix in range(n):
                px = xs[ix]
                r = pts - np.array([px, py, z])
                n3 = np.maximum(np.linalg.norm(r, axis=1) ** 3, 1e-18)
                f = MU0_OVER_4PI * dA / n3
                rz = r[:, 2]
                rx = r[:, 0]
                ry = r[:, 1]
                jc = li * 2 * pl + iy * n + ix
                jyc = jc + pl
                # Jx contribution: dB = mu0/(4pi) * (Jx_hat x r) / |r|^3 * dA
                A[0::3, jc] = 0.0
                A[1::3, jc] = -f * rz
                A[2::3, jc] = f * ry
                # Jy contribution
                A[0::3, jyc] = f * rz
                A[1::3, jyc] = 0.0
                A[2::3, jyc] = -f * rx

    # --- Via vertical-current columns (s12, s23, s34) ---
    # Model each via as a vertical current segment from z_top to z_bot.
    # dl = (0, 0, dz), dl x r = (-dz*ry, dz*rx, 0)
    # Bx += -mu0/(4pi) * I * dz * ry / |r|^3
    # By +=  mu0/(4pi) * I * dz * rx / |r|^3
    # Bz += 0
    for vi, (lid_top, lid_bot) in enumerate(VIA_PAIRS):
        z_top = depths[lid_top]
        z_bot = depths[lid_bot]
        dz = abs(z_bot - z_top)
        z_mid = 0.5 * (z_top + z_bot)
        col_base = 8 * pl + vi * pl
        for iy in range(n):
            py = ys[iy]
            for ix in range(n):
                px = xs[ix]
                col = col_base + iy * n + ix
                r = pts - np.array([px, py, z_mid])
                n3 = np.maximum(np.linalg.norm(r, axis=1) ** 3, 1e-18)
                f = MU0_OVER_4PI * dz / n3
                rx = r[:, 0]
                ry = r[:, 1]
                # Via vertical current: Bx, By only
                A[0::3, col] = -f * ry   # Bx
                A[1::3, col] = f * rx    # By
                # A[2::3, col] = 0.0  (already zero)

    return A, 8 * pl


def build_kcl_matrix(n: int, cfg: dict = None):
    """Build KCL constraint matrix coupling layers and vias.

    Real four-layer KCL:
        L1: div(J1) + s12 = 0
        L2: div(J2) - s12 + s23 = 0
        L3: div(J3) - s23 + s34 = 0
        L4: div(J4) - s34 = 0

    Returns D of shape (4*n*n, 11*n*n).

    E18.1 FIX: Uses Neumann boundary (non-periodic) by default and
    couples via source/sink channels into layer continuity.
    """
    pl = n * n
    D = np.zeros((4 * pl, 11 * pl))
    sc = float(n)
    boundary = "neumann"
    if cfg is not None:
        boundary = cfg.get("kcl_boundary", "neumann")

    for layer in range(4):
        base = layer * pl
        jxb = layer * 2 * pl
        jyb = jxb + pl
        for iy in range(n):
            for ix in range(n):
                row = base + iy * n + ix
                # dJx/dx
                if boundary == "periodic":
                    nx = (ix + 1) % n
                else:
                    nx = min(ix + 1, n - 1)
                D[row, jxb + iy * n + nx] += sc
                D[row, jxb + iy * n + ix] += -sc
                # dJy/dy
                if boundary == "periodic":
                    ny = (iy + 1) % n
                else:
                    ny = min(iy + 1, n - 1)
                D[row, jyb + ny * n + ix] += sc
                D[row, jyb + iy * n + ix] += -sc

        # Via coupling: source/sink terms
        # L1: div(J1) + s12 = 0  -> D[L1_row, s12_col] = +1
        # L2: div(J2) - s12 + s23 = 0 -> D[L2_row, s12_col] = -1, D[L2_row, s23_col] = +1
        # L3: div(J3) - s23 + s34 = 0 -> D[L3_row, s23_col] = -1, D[L3_row, s34_col] = +1
        # L4: div(J4) - s34 = 0  -> D[L4_row, s34_col] = -1
        via_scale = sc  # same scale as divergence
        for iy in range(n):
            for ix in range(n):
                row = base + iy * n + ix
                cell = iy * n + ix
                if layer == 0:
                    D[row, 8 * pl + 0 * pl + cell] += via_scale   # +s12
                elif layer == 1:
                    D[row, 8 * pl + 0 * pl + cell] += -via_scale  # -s12
                    D[row, 8 * pl + 1 * pl + cell] += via_scale   # +s23
                elif layer == 2:
                    D[row, 8 * pl + 1 * pl + cell] += -via_scale  # -s23
                    D[row, 8 * pl + 2 * pl + cell] += via_scale   # +s34
                elif layer == 3:
                    D[row, 8 * pl + 2 * pl + cell] += -via_scale  # -s34

    return D


# Keep old name for backward compat but use new implementation
def build_div_matrix(n: int):
    """Backward-compatible wrapper using new KCL matrix."""
    return build_kcl_matrix(n)


def forward_predict(A: np.ndarray, x: np.ndarray, field_shape: tuple):
    """Predict B field from current vector x."""
    return (A @ x).reshape(field_shape)


def operator_diagnostics(A: np.ndarray, cfg: dict) -> dict:
    """Compute forward operator diagnostics."""
    n = int(cfg["grid_size"])
    pl = n * n
    col_norms = np.linalg.norm(A, axis=0)

    groups = {}
    names = ["J1x", "J1y", "J2x", "J2y", "J3x", "J3y", "J4x", "J4y", "s12", "s23", "s34"]
    for gi, name in enumerate(names):
        start = gi * pl
        end = start + pl
        groups[name] = {
            "mean_norm": float(np.mean(col_norms[start:end])),
            "min_norm": float(np.min(col_norms[start:end])),
            "max_norm": float(np.max(col_norms[start:end])),
        }

    via_norms = col_norms[8 * pl:]
    sheet_norms = col_norms[:8 * pl]

    return {
        "column_norm_by_group": groups,
        "via_column_norm_min": float(np.min(via_norms)) if len(via_norms) > 0 else 0.0,
        "via_column_norm_mean": float(np.mean(via_norms)) if len(via_norms) > 0 else 0.0,
        "sheet_column_norm_mean": float(np.mean(sheet_norms)),
        "via_columns_nonzero": bool(np.min(via_norms) > 1e-20) if len(via_norms) > 0 else False,
        "total_columns": A.shape[1],
        "total_rows": A.shape[0],
    }


def kcl_diagnostics(D: np.ndarray, n: int) -> dict:
    """Compute KCL matrix diagnostics."""
    pl = n * n
    col_norms = np.linalg.norm(D, axis=0)
    via_col_norms = col_norms[8 * pl:]

    return {
        "via_coupling_nonzero": bool(np.min(np.abs(via_col_norms)) > 1e-20) if len(via_col_norms) > 0 else False,
        "via_coupling_column_norms": {
            "s12": float(np.mean(col_norms[8 * pl:9 * pl])),
            "s23": float(np.mean(col_norms[9 * pl:10 * pl])),
            "s34": float(np.mean(col_norms[10 * pl:11 * pl])),
        },
        "layer_rows_count": 4 * pl,
        "total_shape": list(D.shape),
    }


def scale_operator(A: np.ndarray, b: np.ndarray):
    """Column-normalize A and scale b for numerically stable inversion.

    Returns (A_scaled, b_scaled, col_norms, b_scale).
    To recover x from y: x = y / col_norms
    """
    col_norms = np.linalg.norm(A, axis=0)
    col_norms = np.maximum(col_norms, 1e-20)
    A_scaled = A / col_norms[None, :]
    b_scale = max(float(np.linalg.norm(b) / np.sqrt(len(b))), 1e-20)
    A_scaled = A_scaled / b_scale
    b_scaled = b / b_scale
    return A_scaled, b_scaled, col_norms, b_scale


def unscale_solution(y: np.ndarray, col_norms: np.ndarray) -> np.ndarray:
    """Recover physical solution from scaled solution."""
    return y / col_norms
