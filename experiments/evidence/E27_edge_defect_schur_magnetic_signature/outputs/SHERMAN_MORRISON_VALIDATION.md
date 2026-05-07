# Sherman-Morrison Validation

- Tested 10 defect perturbations
- Max relative error: 1.909e-14
- Mean relative error: 7.075e-15
- Validation threshold: 1e-8
- Passed: True

The Sherman-Morrison perturbation formula matches direct Laplacian solve
to machine precision, confirming the closed-form edge-defect signature
is mathematically exact for the generated graph network.
