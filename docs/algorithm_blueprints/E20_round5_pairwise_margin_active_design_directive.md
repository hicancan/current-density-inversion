# E20 Round 5 Directive: Pairwise-Margin Active Measurement Design

Status: implementation directive for Claude worker, not evidence.

Target worktree/session:

- worktree: `e20-active-oqci`
- previous session: `aa6a240a-8b3b-46fc-9229-1123e36dc61b`

## Mathematical Objective

Rounds 3-4 showed that residual-threshold OQCI can produce some clean
evaluation cases, but the valid disambiguation rate remains too low:

```text
best full-set regularized VDR = 0.167
calibrated evaluation VDR = 0.222
truth coverage can survive, but most cases remain multi-consistent
```

Round 5 must stop optimizing interval width or raw residual shrinkage. It must
optimize the pairwise robust margin that determines whether a future
measurement can actually separate hypotheses.

For a measurement candidate `c` and current measurement set `M`, define the
stacked manifold:

```math
\mathcal{M}_h(M)
=
\{a_h(M)+B_h(M)\theta:\theta\in\Theta_h\}.
```

Pairwise affine separation:

```math
\delta_{hg}(M)^2
=
\min_{\theta_h,\theta_g}
\|W_M[(a_h-a_g)+B_h\theta_h-B_g\theta_g]\|_2^2 .
```

Robust margin:

```math
\Gamma_{hg}(M)
=
\delta_{hg}(M)
-\tau_g(M)
-\epsilon(M)
-\rho_h(M)-\rho_g(M).
```

The next measurement should maximize:

```math
c^*
=
\arg\max_{c\in\mathcal{C}}
\left[
\min_{h\ne g}\Gamma_{hg}(M\cup\{c\})
-\min_{h\ne g}\Gamma_{hg}(M)
-\beta\,\mathrm{cost}(c)
\right].
```

This is the top-level first-principles acquisition criterion.

## Required Scope

Implement only inside:

```text
experiments/evidence/E20_active_oqci_measurement_design/
```

Do not edit global research graph files.

## Required Changes

### 1. Pairwise Margin Computation

For every candidate measurement protocol, compute:

```text
pair
delta_before
delta_after
gamma_before
gamma_after
gamma_gain
principal_angle_before
principal_angle_after
intersection_rank_before
intersection_rank_after
```

At minimum include pairs:

```text
H0/H1, H0/H2, H0/H3, H1/H2, H1/H3, H2/H3
```

Use the existing basis/forward operators. If affine offsets are unavailable,
use subspace principal-angle metrics and explicitly mark them as lower-grade.

### 2. Acquisition Policies

Compare:

```text
interval_width_policy
valid_disambiguation_utility_policy
pairwise_min_gamma_policy
critical_pair_gamma_policy
random_policy_fixed_seed
```

Critical pairs must include H1/H2 and any pair that has near-zero separation in
the baseline.

Report whether the policy selected by pairwise margin differs from the old
policy and why.

### 3. Sequential Two-Step Design

Run a two-step lookahead:

```math
(c_1,c_2)^*
=
\arg\max_{c_1,c_2}
\min_{h\ne g}\Gamma_{hg}(M\cup\{c_1,c_2\})
-\beta[\mathrm{cost}(c_1)+\mathrm{cost}(c_2)] .
```

Use greedy approximation if exhaustive search is too expensive.

Report:

```text
best_1step_candidate
best_2step_sequence
min_gamma_after_1step
min_gamma_after_2step
critical_gamma_after_1step
critical_gamma_after_2step
```

### 4. Decision Outcome Audit

Evaluate the chosen policies on generated evaluation cases using the Round 4
truth-coverage metrics:

```text
valid_disambiguation_rate
truth_in_consistent_set_rate
singleton_wrong_rate
empty_rate
accepted_accuracy
mean_consistent_set_size
```

A pairwise-margin policy is only useful if it improves actual OQCI outcomes.

### 5. Breakthrough Gates

Add:

```text
pairwise_margin_policy_improves_min_gamma
pairwise_margin_policy_improves_vdr_by_0_20
two_step_policy_min_gamma_positive
two_step_policy_truth_coverage_ge_0_90
two_step_policy_singleton_wrong_rate_eq_0
two_step_policy_empty_rate_le_0_10
critical_h1_h2_gamma_positive
```

If these fail, E20 should be reported as a formal negative result: active
measurement candidates in this simplified basis do not supply enough new
information.

## Required Outputs

Add:

```text
outputs/PAIRWISE_MARGIN_MATRIX.md
outputs/ACTIVE_POLICY_COMPARISON.md
outputs/TWO_STEP_ACTIVE_DESIGN_AUDIT.md
outputs/ROUND5_PAIRWISE_MARGIN_GATE_AUDIT.md
```

Update metrics JSON with all Round 5 keys.

## Required Commands

Run:

```powershell
uv run --with-requirements requirements.txt --with pytest python -m pytest -q tests
uv run --with-requirements requirements.txt python src/run_all.py --config configs/smoke.json --out outputs_smoke
uv run --with-requirements requirements.txt python src/run_all.py --config configs/default.json --out outputs
```

## Final Report

Report:

- pairwise margin matrix before/after;
- which policy chooses which measurement;
- one-step and two-step margin gains;
- actual truth-coverage outcomes;
- all Round 5 gates;
- failure modes;
- cannot_claim;
- next required evidence.

