# Real Data Intake Gate

Claim: `C12_real_qdm_nv_validation`.

| Gate | Required before diagnosis |
|---|---|
| metadata schema | field units, component order, pixel pitch, standoff, pose, ports |
| measured array loader | finite values and explicit B-component layout |
| background subtraction | preserve original data and record reference source |
| component plots | polarity and coordinate-frame inspection |
| simple-wire sanity | known-current magnetic shape and sign checks |

Cannot claim: real QDM/NV validation until measured rows pass these gates.

