# exp02 Run Report

## Role

MVP-1 observability calculator and single-layer Fourier inversion sanity check.
It defines recoverable spatial scales before any neural inverse model is trained.

## Gate Summary

Overall: PASS

- clean_full_field_bxy_inverse_is_self_consistent: PASS; value=7.636483302599897e-06; threshold=relative_l2 < 1e-4
- clean_full_field_bz_inverse_is_self_consistent_except_dc: PASS; value=4.5752510309098396e-05; threshold=relative_l2 < 1e-3
- finite_fov_damages_bz_more_than_bxy: PASS; value=10.282842479013027; threshold=Bz finite-FOV error > 5x Bxy finite-FOV error
- two_layer_single_plane_is_rank_deficient: PASS; value=[1, 1, 1, 1, 1]; threshold=rank_per_feature all equal 1

## Key Results

- clean full-field Bxy inversion relative L2: `7.64e-06`
- clean full-field Bz inversion relative L2: `4.58e-05`
- finite-FOV Bxy inversion relative L2: `5.06e-02`
- finite-FOV Bz inversion relative L2: `5.21e-01`
- two-layer single-plane rank gate: `rank deficient`

## Boundary

The thin-sheet Fourier operator is an ideal free-space model. Multilayer
separation still requires topology, masks, multiple measurements, or other
priors; Bxyz alone on one plane does not label layers.
