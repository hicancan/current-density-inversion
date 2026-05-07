# Gamma Rho Recommendation

## E23 Rho Assessment

- Verdict: E23 rho was OVER-CONSERVATIVE: finite-width gap is small (median rel 0.26). The E23 surrogate inflated rho substantially. Recalibration with E25 volume quadrature reduces rho.

## Recommended Rho for Future Gamma Certificates

- Recommended absolute rho: 3.4613e-03
- Recommended relative rho: 3.6676e-01
- Dominant source: straight_strip/rho_combined_conservative

## Usage

Future rounds (E24, E26) should use these calibrated rho values as the
operator perturbation term in the robust Gamma margin:

    Gamma = delta - tau - epsilon - rho_h - rho_g

The conservative (sum) estimate provides a safe upper bound.
The RSS estimate is appropriate if nuisance sources are independent.

## Rationale

E25 decomposes rho into physically justified components with numerical
convergence verification. This replaces the black-box E23 finite-width
surrogate with calibrated, auditable operator radii.
