# Design Rule Implications

E32 turns the E31 positive result into a stricter design-for-test condition.

Generated-domain rule for this graph family:

- Perimeter-only control is effectively impossible: min eta
  `2.48821324e-09`.
- Exact candidate-projection top pads preserve the E31-relevant Schur mode:
  min eta `0.4767196129`.
- Top+bottom local candidate pads nearly recover the local endpoint upper
  bound: min eta `0.9534392258`.
- Sparse top grids can collapse by orders of magnitude when their offsets miss
  the local extrema: stride-2 worst min eta
  `0.0003372396621`, stride-5+ worst min eta
  `4.754241203e-10`.

The next physical route is not a larger inverse model. It is a constrained
active-observation design: candidate-local DFT pads, local micro-bump access,
scanning probe injection, or another mechanism that places drive/return
degrees of freedom near the suspected via-open Schur mode.
