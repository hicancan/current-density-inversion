# Volume Forward Derivation

## Continuous Model

For a conductor volume V_e with uniform current density J_e = (i_e / a_e) * t_e:

    B_e(r_m) = mu0/(4*pi) * int_{V_e} [J_e x (r_m - r')] / |r_m - r'|^3  dr'

## Discretization

The volume integral is factorized as:

1. **Along-segment integral** (0 to L): Gauss-Legendre quadrature, order n_seg.
2. **Cross-section integral** (width x thickness): Tensor-product Gauss-Legendre, orders n_w x n_t.

Total quadrature points per conductor: n_seg * n_w * n_t.

## Forward Matrix

    A^{vol}_{m,e} = mu0/(4*pi*a_e) * int_{V_e} [t_e x (r_m - r')] / |r_m - r'|^3  dr'

Each column is computed with unit current (i_e = 1 A) for linearity.

## Convergence

Convergence is verified by doubling all quadrature orders:

    ||A_Q - A_{{2Q}}||_F / ||A_{{2Q}}||_F  <=  0.05

The 0.05 threshold is the E25 scientific gate.
