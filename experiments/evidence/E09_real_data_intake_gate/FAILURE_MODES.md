# Failure Modes

## 1. Metadata can pass before data exists

The included example validates schema shape only. It cannot be treated as a
measured-data validation result.

## 2. Unit and polarity ambiguity

Future real rows must make units, component order, coordinate frame, and current
polarity explicit before any graph-identification claim.

## 3. Background subtraction can leak

Background/reference files must be preserved and recorded. Hidden or held-out
real rows cannot be used for calibration unless the protocol explicitly marks
them as calibration rows.

