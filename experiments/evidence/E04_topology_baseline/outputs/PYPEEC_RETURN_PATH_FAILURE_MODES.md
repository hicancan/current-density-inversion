# Real PyPEEC Return-Path Failure Modes

This report ranks return-path rows by PyPEEC magnetic residual and current-allocation error. It documents where return current remains an independent physical challenge for the current two-layer model.

## `trace_with_return_path__v31` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.087`
- allocation error: `0.413`
- signal/return path L2: `0.310` / `1.126`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.611` / `0.033`
- raw/shape physical B residual to PyPEEC: `3.380` / `0.553`
- scalar fit to PyPEEC / delta vs no-topology: `0.200` / `0.000`

## `trace_with_return_path__v06` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.060`
- allocation error: `0.440`
- signal/return path L2: `0.219` / `1.072`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.562` / `0.040`
- raw/shape physical B residual to PyPEEC: `3.376` / `0.550`
- scalar fit to PyPEEC / delta vs no-topology: `0.201` / `0.000`

## `trace_with_return_path__v30` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.075`
- allocation error: `0.425`
- signal/return path L2: `0.248` / `1.106`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.506` / `0.034`
- raw/shape physical B residual to PyPEEC: `3.370` / `0.556`
- scalar fit to PyPEEC / delta vs no-topology: `0.200` / `0.000`

## `trace_with_return_path__v06` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.053`
- allocation error: `0.447`
- signal/return path L2: `0.300` / `0.994`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.257` / `0.090`
- raw/shape physical B residual to PyPEEC: `3.173` / `0.553`
- scalar fit to PyPEEC / delta vs no-topology: `0.211` / `-0.203`

## `trace_with_return_path__v30` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.060`
- allocation error: `0.440`
- signal/return path L2: `0.293` / `1.019`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.259` / `0.049`
- raw/shape physical B residual to PyPEEC: `3.127` / `0.555`
- scalar fit to PyPEEC / delta vs no-topology: `0.213` / `-0.243`

## `trace_with_return_path__v06` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.053`
- allocation error: `0.447`
- signal/return path L2: `0.300` / `0.994`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.235` / `0.090`
- raw/shape physical B residual to PyPEEC: `3.126` / `0.544`
- scalar fit to PyPEEC / delta vs no-topology: `0.214` / `-0.250`

## `trace_with_return_path__v30` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.060`
- allocation error: `0.440`
- signal/return path L2: `0.293` / `1.019`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.273` / `0.049`
- raw/shape physical B residual to PyPEEC: `3.097` / `0.548`
- scalar fit to PyPEEC / delta vs no-topology: `0.215` / `-0.274`

## `trace_with_return_path__v31` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.056`
- allocation error: `0.444`
- signal/return path L2: `0.318` / `1.023`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.261` / `0.042`
- raw/shape physical B residual to PyPEEC: `3.088` / `0.552`
- scalar fit to PyPEEC / delta vs no-topology: `0.215` / `-0.293`

## `trace_with_return_path__v31` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.056`
- allocation error: `0.444`
- signal/return path L2: `0.318` / `1.023`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.237` / `0.042`
- raw/shape physical B residual to PyPEEC: `3.055` / `0.545`
- scalar fit to PyPEEC / delta vs no-topology: `0.218` / `-0.326`

## `trace_with_return_path__v78` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.097`
- allocation error: `0.403`
- signal/return path L2: `0.459` / `0.864`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.501` / `0.163`
- raw/shape physical B residual to PyPEEC: `2.925` / `0.451`
- scalar fit to PyPEEC / delta vs no-topology: `0.236` / `0.000`

## `trace_with_return_path__v79` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.068`
- allocation error: `0.432`
- signal/return path L2: `1.227` / `1.006`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.527` / `0.962`
- raw/shape physical B residual to PyPEEC: `2.920` / `0.533`
- scalar fit to PyPEEC / delta vs no-topology: `0.228` / `0.000`

## `trace_with_return_path__v29` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.067`
- allocation error: `0.433`
- signal/return path L2: `1.249` / `1.004`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.532` / `0.960`
- raw/shape physical B residual to PyPEEC: `2.911` / `0.534`
- scalar fit to PyPEEC / delta vs no-topology: `0.228` / `0.000`

## `trace_with_return_path__v52` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.131`
- allocation error: `0.369`
- signal/return path L2: `0.633` / `0.902`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.545` / `0.331`
- raw/shape physical B residual to PyPEEC: `2.879` / `0.468`
- scalar fit to PyPEEC / delta vs no-topology: `0.237` / `0.000`

## `trace_with_return_path__v53` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.134`
- allocation error: `0.366`
- signal/return path L2: `0.631` / `0.911`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.542` / `0.332`
- raw/shape physical B residual to PyPEEC: `2.864` / `0.460`
- scalar fit to PyPEEC / delta vs no-topology: `0.239` / `0.000`

## `trace_with_return_path__v28` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.070`
- allocation error: `0.430`
- signal/return path L2: `1.265` / `1.012`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.546` / `0.983`
- raw/shape physical B residual to PyPEEC: `2.850` / `0.538`
- scalar fit to PyPEEC / delta vs no-topology: `0.231` / `0.000`

## `trace_with_return_path__v48` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.121`
- allocation error: `0.379`
- signal/return path L2: `0.319` / `1.019`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.415` / `0.136`
- raw/shape physical B residual to PyPEEC: `2.572` / `0.488`
- scalar fit to PyPEEC / delta vs no-topology: `0.257` / `0.000`

## `trace_with_return_path__v99` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.137`
- allocation error: `0.363`
- signal/return path L2: `0.366` / `1.011`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.305` / `0.174`
- raw/shape physical B residual to PyPEEC: `2.490` / `0.485`
- scalar fit to PyPEEC / delta vs no-topology: `0.264` / `0.000`

## `trace_with_return_path__v53` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.109`
- allocation error: `0.391`
- signal/return path L2: `0.613` / `1.014`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.221` / `0.326`
- raw/shape physical B residual to PyPEEC: `2.485` / `0.465`
- scalar fit to PyPEEC / delta vs no-topology: `0.266` / `-0.379`

## `trace_with_return_path__v53` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.109`
- allocation error: `0.391`
- signal/return path L2: `0.613` / `1.014`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.202` / `0.326`
- raw/shape physical B residual to PyPEEC: `2.473` / `0.461`
- scalar fit to PyPEEC / delta vs no-topology: `0.268` / `-0.391`

## `trace_with_return_path__v52` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.101`
- allocation error: `0.399`
- signal/return path L2: `0.613` / `1.006`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.218` / `0.319`
- raw/shape physical B residual to PyPEEC: `2.471` / `0.476`
- scalar fit to PyPEEC / delta vs no-topology: `0.266` / `-0.408`

## `trace_with_return_path__v52` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.101`
- allocation error: `0.399`
- signal/return path L2: `0.613` / `1.006`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.203` / `0.319`
- raw/shape physical B residual to PyPEEC: `2.461` / `0.474`
- scalar fit to PyPEEC / delta vs no-topology: `0.267` / `-0.418`

## `trace_with_return_path__v09` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.132`
- allocation error: `0.368`
- signal/return path L2: `0.361` / `1.012`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.420` / `0.147`
- raw/shape physical B residual to PyPEEC: `2.424` / `0.483`
- scalar fit to PyPEEC / delta vs no-topology: `0.269` / `0.000`

## `trace_with_return_path__v78` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.083`
- allocation error: `0.417`
- signal/return path L2: `0.452` / `0.940`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.174` / `0.134`
- raw/shape physical B residual to PyPEEC: `2.322` / `0.467`
- scalar fit to PyPEEC / delta vs no-topology: `0.280` / `-0.603`

## `trace_with_return_path__v78` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.083`
- allocation error: `0.417`
- signal/return path L2: `0.452` / `0.940`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.177` / `0.134`
- raw/shape physical B residual to PyPEEC: `2.321` / `0.465`
- scalar fit to PyPEEC / delta vs no-topology: `0.280` / `-0.604`

## `trace_with_return_path__v02` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `amplitude mismatch`
- truth/pred return fraction: `0.500` / `0.217`
- allocation error: `0.283`
- signal/return path L2: `0.409` / `1.020`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.218` / `0.230`
- raw/shape physical B residual to PyPEEC: `2.299` / `0.486`
- scalar fit to PyPEEC / delta vs no-topology: `0.280` / `0.259`

## `trace_with_return_path__v82` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `amplitude mismatch`
- truth/pred return fraction: `0.500` / `0.217`
- allocation error: `0.283`
- signal/return path L2: `0.409` / `1.020`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.218` / `0.230`
- raw/shape physical B residual to PyPEEC: `2.299` / `0.486`
- scalar fit to PyPEEC / delta vs no-topology: `0.280` / `0.259`

## `trace_with_return_path__v04` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `amplitude mismatch`
- truth/pred return fraction: `0.500` / `0.211`
- allocation error: `0.289`
- signal/return path L2: `0.293` / `0.492`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.577` / `0.036`
- raw/shape physical B residual to PyPEEC: `2.293` / `0.285`
- scalar fit to PyPEEC / delta vs no-topology: `0.296` / `0.000`

## `trace_with_return_path__v02` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `amplitude mismatch`
- truth/pred return fraction: `0.500` / `0.217`
- allocation error: `0.283`
- signal/return path L2: `0.409` / `1.020`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.253` / `0.230`
- raw/shape physical B residual to PyPEEC: `2.293` / `0.484`
- scalar fit to PyPEEC / delta vs no-topology: `0.281` / `0.254`

## `trace_with_return_path__v82` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `amplitude mismatch`
- truth/pred return fraction: `0.500` / `0.217`
- allocation error: `0.283`
- signal/return path L2: `0.409` / `1.020`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.253` / `0.230`
- raw/shape physical B residual to PyPEEC: `2.293` / `0.484`
- scalar fit to PyPEEC / delta vs no-topology: `0.281` / `0.254`

## `trace_with_return_path__v32` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `amplitude mismatch`
- truth/pred return fraction: `0.500` / `0.189`
- allocation error: `0.311`
- signal/return path L2: `0.397` / `1.009`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.235` / `0.208`
- raw/shape physical B residual to PyPEEC: `2.282` / `0.487`
- scalar fit to PyPEEC / delta vs no-topology: `0.281` / `0.135`

