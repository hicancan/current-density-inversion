# Literature Reproduction Notes

All methods are textbook implementations, not paper reproductions:
- Fourier: standard Wiener deconvolution in 2D Fourier domain
- Tikhonov: Landweber iteration on L2-regularized objective
- L1-sparse: ISTA with L1 soft-thresholding on J directly
  (Exact L1-curl failed: proximal operator for L1 on curl(J) requires
   split-Bregman or dual methods beyond this baseline scope)
- Div-free: stream-function representation J=curl(psi*z_hat)

No novelty claims. Centerline Biot-Savart forward only.
