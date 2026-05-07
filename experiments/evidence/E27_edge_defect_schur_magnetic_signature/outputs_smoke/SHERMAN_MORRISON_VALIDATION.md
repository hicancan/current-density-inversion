# Sherman-Morrison Validation

- Tested 8 defect perturbations
- Max relative error: 2.150e-14
- Mean relative error: 7.178e-15
- Validation threshold: 1e-8
- Passed: True

The Sherman-Morrison perturbation formula matches direct Laplacian solve
to machine precision, confirming the closed-form edge-defect signature
is mathematically exact for the generated graph network.
