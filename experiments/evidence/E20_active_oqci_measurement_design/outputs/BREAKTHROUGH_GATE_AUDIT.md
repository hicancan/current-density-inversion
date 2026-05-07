# Breakthrough Gate Audit

All four breakthrough gates passed: **False**

## Gate Requirements

| gate | requirement | current best | passed |
|---|---:|---:|
| valid_disambiguation_rate >= 0.50 | >= 0.50 | 0.0000 | no |
| truth_in_consistent_set_rate >= 0.90 | >= 0.90 | 1.0000 | yes |
| singleton_wrong_rate == 0 | = 0.00 | 0.0000 | yes |
| empty_rate <= 0.10 | <= 0.10 | 0.0000 | yes |

## Interpretation

No (candidate, epsilon) pair passes all four breakthrough gates.
The current generated-domain OQCI framework does not yet produce
reliable valid disambiguation. The observed signal at tight epsilon
is dominated by empty sets or singleton-wrong classifications.

This is a stronger negative result: even with epsilon sweep and
multi-state excitation, the generated basis family cannot produce
valid disambiguation at a level meeting all breakthrough criteria.
