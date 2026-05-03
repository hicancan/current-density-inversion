# Real Calibration Boundary

Claim: `C13_calibration_protocol_reality`.

Candidate calibration sources:

| Source | Can support |
|---|---|
| calibration coupon | known H0/H1/H2/H3 samples |
| known-good no-via region | H0 safety calibration |
| known-via coupon | H1 recall calibration |
| known-return structure | H2 return evidence calibration |
| known-artifact corner/bend | H3 artifact calibration |
| external solver subset | solver-domain calibration |
| simple-wire known structure | units, polarity, standoff sanity |

Cannot claim: generated few-shot rows are automatically realistic calibration
samples.

