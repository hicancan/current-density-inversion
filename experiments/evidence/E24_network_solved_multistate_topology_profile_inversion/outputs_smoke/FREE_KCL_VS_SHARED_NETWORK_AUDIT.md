# Free KCL vs Shared Network Audit

## Aggregate

- Total rows: 128
- Truth self-fit mean residual (shared): 0.097908
- Truth self-fit mean residual (free): 0.097907
- Wrong fit mean residual (shared): 0.098019
- Wrong fit mean residual (free): 0.098029

## Key Finding

The free KCL model allows each excitation state to independently choose
nullspace current components. The shared network model ties all states
to one conductance vector, making it harder for wrong topologies to fit
multi-state data.
