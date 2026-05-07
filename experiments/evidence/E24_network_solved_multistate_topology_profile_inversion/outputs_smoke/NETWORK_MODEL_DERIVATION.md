# E24 Network Model Derivation

## Mathematical Object

For topology hypothesis `h`, define a directed circuit graph:

    G_h = (V_h, E_h),  D_h in {-1,0,1}^{|V_h| x |E_h|}

Each edge `e` has conductance:

    c_e = exp(theta_e),  C_h(theta) = diag(c_e)

The weighted graph Laplacian:

    L_h(theta) = D_h C_h(theta) D_h^T

For excitation state `s`, port injection vector `b_s` obeys:

    1^T b_s = 0,  ||b_s||_1 <= I_max

Network potentials solve:

    L_h(theta) phi_{h,s} = b_s

with gauge fixed by sum(phi) = 0.

Edge currents are not free but determined by Ohm's law:

    i_{h,s}(theta) = C_h(theta) D_h^T phi_{h,s}

They automatically satisfy KCL: D_h i_{h,s}(theta) = b_s.

## Core Breakthrough Hypothesis

The same `theta` explains every state. Thus:

    dim M^{net}_h(U) << sum_s dim I^{free}_{h,s}

The breakthrough mechanism is cross-state consistency:

    exists {i_s}_{s=1}^S fitting Y
    => NOT => exists theta s.t. i_s = C(theta) D^T L(theta)^dagger b_s for all s

## Profile Objective

    J_h(theta) = sum_{s=1}^S ||W_s(y_s - A_h i_{h,s}(theta))||^2
                 + lambda_theta ||theta - theta_0||^2
                 + lambda_Delta ||R theta||^2

## Key Diagnostic

    free_kcl_fit    — each state independently chooses nullspace currents
    per_state_network_fit — each state gets its own conductance vector
    shared_network_fit    — one conductance vector for all states

Expected pattern: r_g^{free} ≈ r_h^{free} but r_g^{shared} >> r_h^{shared}.
