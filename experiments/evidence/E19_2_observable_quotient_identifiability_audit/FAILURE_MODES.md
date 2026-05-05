# E19.2 Failure Modes

See `outputs/FAILURE_CASES.md` for per-case failure documentation.

## Systematic failure modes

1. **Multiple consistent hypotheses (ambiguity)**: When noise-level forward distances between hypothesis subspaces are below epsilon, multiple hypotheses remain consistent. This is the expected behavior under single-height observation and is the primary scientific output.

2. **Empty consistent set**: Occurs when the forward model, noise model, or admissible state space is mismatched. Indicates either too-strict epsilon or genuine model mismatch.

3. **Unresolved adversarial pairs**: When D(Gi, Gj) < epsilon, the hypotheses are fundamentally indistinguishable under the current experiment family.

4. **Wide claim intervals persist under multi-height**: If adding a second sensor height does not narrow intervals, the hypotheses remain indistinguishable.
