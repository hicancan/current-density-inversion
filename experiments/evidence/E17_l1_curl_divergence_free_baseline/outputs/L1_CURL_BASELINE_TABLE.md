# Baseline Comparison Table

| Baseline | N | Fail | J RMSE(med) | B RMSE(med) | Div | Curl | Edge | Time(s) |
|---|---|---|---|---|---|---|---|---|
| div_free_iter=50 | 24 | 0 | 2.785922e+00 | 1.334097e-06 | 7.923469e-01 | 7.052277e-01 | 0.3054 | 2.199 |
| fourier_wiener_eps=0.001 | 24 | 0 | 1.491269e+00 | 4.342213e-07 | 2.904038e-11 | 6.861299e-13 | 0.1297 | 0.219 |
| fourier_wiener_eps=0.01 | 24 | 0 | 1.491269e+00 | 4.342213e-07 | 2.904038e-12 | 6.861299e-14 | 0.1297 | 0.222 |
| l1_sparse_lam=0.01_iter=50 | 24 | 0 | 1.491269e+00 | 4.342213e-07 | 0.000000e+00 | 0.000000e+00 | 0.0000 | 1.865 |
| l1_sparse_lam=0.1_iter=50 | 24 | 0 | 1.491269e+00 | 4.342213e-07 | 0.000000e+00 | 0.000000e+00 | 0.0000 | 1.867 |
| tikhonov_lam=1e-24_iter=50 | 24 | 0 | 1.386140e+00 | 1.256365e-07 | 2.871013e-01 | 2.481901e-01 | 0.3411 | 3.623 |

## Best per condition

| Condition | Best J | J RMSE | Best B | B RMSE |
|---|---|---|---|---|
| ood_noise=0.01 | tikhonov_lam=1e-24_iter=50 | 1.2894e+00 | tikhonov_lam=1e-24_iter=50 | 7.9129e-08 |
| ood_noise=0.02 | tikhonov_lam=1e-24_iter=50 | 1.3876e+00 | tikhonov_lam=1e-24_iter=50 | 9.6972e-08 |
| ood_noise=0.0 | tikhonov_lam=1e-24_iter=50 | 1.4536e+00 | tikhonov_lam=1e-24_iter=50 | 8.2178e-08 |
| test_noise=0.01 | tikhonov_lam=1e-24_iter=50 | 1.3266e+00 | tikhonov_lam=1e-24_iter=50 | 6.3529e-08 |
| test_noise=0.02 | tikhonov_lam=1e-24_iter=50 | 1.3179e+00 | tikhonov_lam=1e-24_iter=50 | 9.3898e-08 |
| test_noise=0.0 | tikhonov_lam=1e-24_iter=50 | 1.3611e+00 | tikhonov_lam=1e-24_iter=50 | 5.9876e-08 |
| train_noise=0.01 | tikhonov_lam=1e-24_iter=50 | 1.3846e+00 | tikhonov_lam=1e-24_iter=50 | 6.9768e-08 |
| train_noise=0.02 | tikhonov_lam=1e-24_iter=50 | 1.2532e+00 | tikhonov_lam=1e-24_iter=50 | 8.8318e-08 |
| train_noise=0.0 | tikhonov_lam=1e-24_iter=50 | 1.2948e+00 | tikhonov_lam=1e-24_iter=50 | 5.7948e-08 |
| val_noise=0.01 | tikhonov_lam=1e-24_iter=50 | 1.2784e+00 | tikhonov_lam=1e-24_iter=50 | 6.5600e-08 |
| val_noise=0.02 | tikhonov_lam=1e-24_iter=50 | 1.2473e+00 | tikhonov_lam=1e-24_iter=50 | 7.9790e-08 |
| val_noise=0.0 | tikhonov_lam=1e-24_iter=50 | 1.2394e+00 | tikhonov_lam=1e-24_iter=50 | 5.4664e-08 |
