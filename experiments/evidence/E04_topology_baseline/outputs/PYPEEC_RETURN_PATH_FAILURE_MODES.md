# Real PyPEEC Return-Path Failure Modes

This report ranks return-path rows by PyPEEC magnetic residual and current-allocation error. It documents where return current remains an independent physical challenge for the current two-layer model.

## `trace_with_return_path__v30` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.081`
- allocation error: `0.419`
- signal/return path L2: `0.226` / `0.979`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.283` / `0.044`
- raw/shape physical B residual to PyPEEC: `3.487` / `0.553`
- scalar fit to PyPEEC / delta vs no-topology: `0.195` / `0.784`

## `trace_with_return_path__v30` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.081`
- allocation error: `0.419`
- signal/return path L2: `0.226` / `0.979`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.265` / `0.044`
- raw/shape physical B residual to PyPEEC: `3.476` / `0.551`
- scalar fit to PyPEEC / delta vs no-topology: `0.196` / `0.773`

## `trace_with_return_path__v06` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.070`
- allocation error: `0.430`
- signal/return path L2: `0.268` / `0.947`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.236` / `0.091`
- raw/shape physical B residual to PyPEEC: `3.440` / `0.551`
- scalar fit to PyPEEC / delta vs no-topology: `0.197` / `0.801`

## `trace_with_return_path__v06` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.070`
- allocation error: `0.430`
- signal/return path L2: `0.268` / `0.947`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.197` / `0.091`
- raw/shape physical B residual to PyPEEC: `3.416` / `0.548`
- scalar fit to PyPEEC / delta vs no-topology: `0.199` / `0.778`

## `trace_with_return_path__v31` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.078`
- allocation error: `0.422`
- signal/return path L2: `0.258` / `0.987`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.228` / `0.037`
- raw/shape physical B residual to PyPEEC: `3.320` / `0.548`
- scalar fit to PyPEEC / delta vs no-topology: `0.203` / `0.688`

## `trace_with_return_path__v31` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.078`
- allocation error: `0.422`
- signal/return path L2: `0.258` / `0.987`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.195` / `0.037`
- raw/shape physical B residual to PyPEEC: `3.304` / `0.547`
- scalar fit to PyPEEC / delta vs no-topology: `0.204` / `0.671`

## `trace_with_return_path__v99` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.065`
- allocation error: `0.435`
- signal/return path L2: `0.241` / `0.982`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.227` / `0.075`
- raw/shape physical B residual to PyPEEC: `3.209` / `0.502`
- scalar fit to PyPEEC / delta vs no-topology: `0.214` / `0.753`

## `trace_with_return_path__v99` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.065`
- allocation error: `0.435`
- signal/return path L2: `0.241` / `0.982`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.230` / `0.075`
- raw/shape physical B residual to PyPEEC: `3.207` / `0.501`
- scalar fit to PyPEEC / delta vs no-topology: `0.215` / `0.751`

## `trace_with_return_path__v48` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.066`
- allocation error: `0.434`
- signal/return path L2: `0.283` / `0.985`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.347` / `0.075`
- raw/shape physical B residual to PyPEEC: `3.005` / `0.500`
- scalar fit to PyPEEC / delta vs no-topology: `0.226` / `0.546`

## `trace_with_return_path__v48` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.066`
- allocation error: `0.434`
- signal/return path L2: `0.283` / `0.985`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.286` / `0.075`
- raw/shape physical B residual to PyPEEC: `2.995` / `0.497`
- scalar fit to PyPEEC / delta vs no-topology: `0.227` / `0.536`

## `trace_with_return_path__v09` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.071`
- allocation error: `0.429`
- signal/return path L2: `0.304` / `0.978`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.281` / `0.075`
- raw/shape physical B residual to PyPEEC: `2.980` / `0.501`
- scalar fit to PyPEEC / delta vs no-topology: `0.228` / `0.660`

## `trace_with_return_path__v02` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.079`
- allocation error: `0.421`
- signal/return path L2: `0.297` / `0.954`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.218` / `0.076`
- raw/shape physical B residual to PyPEEC: `2.973` / `0.515`
- scalar fit to PyPEEC / delta vs no-topology: `0.226` / `1.003`

## `trace_with_return_path__v82` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.079`
- allocation error: `0.421`
- signal/return path L2: `0.297` / `0.954`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.218` / `0.076`
- raw/shape physical B residual to PyPEEC: `2.973` / `0.515`
- scalar fit to PyPEEC / delta vs no-topology: `0.226` / `1.003`

## `trace_with_return_path__v32` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.074`
- allocation error: `0.426`
- signal/return path L2: `0.284` / `0.954`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.302` / `0.075`
- raw/shape physical B residual to PyPEEC: `2.973` / `0.519`
- scalar fit to PyPEEC / delta vs no-topology: `0.226` / `0.956`

## `trace_with_return_path__v72` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.074`
- allocation error: `0.426`
- signal/return path L2: `0.284` / `0.954`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.302` / `0.075`
- raw/shape physical B residual to PyPEEC: `2.973` / `0.519`
- scalar fit to PyPEEC / delta vs no-topology: `0.226` / `0.956`

## `trace_with_return_path__v09` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.071`
- allocation error: `0.429`
- signal/return path L2: `0.304` / `0.978`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.225` / `0.075`
- raw/shape physical B residual to PyPEEC: `2.972` / `0.499`
- scalar fit to PyPEEC / delta vs no-topology: `0.228` / `0.651`

## `trace_with_return_path__v32` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.074`
- allocation error: `0.426`
- signal/return path L2: `0.284` / `0.954`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.242` / `0.075`
- raw/shape physical B residual to PyPEEC: `2.966` / `0.517`
- scalar fit to PyPEEC / delta vs no-topology: `0.227` / `0.950`

## `trace_with_return_path__v72` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.074`
- allocation error: `0.426`
- signal/return path L2: `0.284` / `0.954`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.242` / `0.075`
- raw/shape physical B residual to PyPEEC: `2.966` / `0.517`
- scalar fit to PyPEEC / delta vs no-topology: `0.227` / `0.950`

## `trace_with_return_path__v02` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.079`
- allocation error: `0.421`
- signal/return path L2: `0.297` / `0.954`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.232` / `0.076`
- raw/shape physical B residual to PyPEEC: `2.965` / `0.512`
- scalar fit to PyPEEC / delta vs no-topology: `0.227` / `0.994`

## `trace_with_return_path__v82` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.079`
- allocation error: `0.421`
- signal/return path L2: `0.297` / `0.954`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.232` / `0.076`
- raw/shape physical B residual to PyPEEC: `2.965` / `0.512`
- scalar fit to PyPEEC / delta vs no-topology: `0.227` / `0.994`

## `trace_with_return_path__v03` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.075`
- allocation error: `0.425`
- signal/return path L2: `0.307` / `0.951`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.188` / `0.074`
- raw/shape physical B residual to PyPEEC: `2.884` / `0.513`
- scalar fit to PyPEEC / delta vs no-topology: `0.232` / `0.855`

## `trace_with_return_path__v83` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.075`
- allocation error: `0.425`
- signal/return path L2: `0.307` / `0.951`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.188` / `0.074`
- raw/shape physical B residual to PyPEEC: `2.884` / `0.513`
- scalar fit to PyPEEC / delta vs no-topology: `0.232` / `0.855`

## `trace_with_return_path__v03` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.075`
- allocation error: `0.425`
- signal/return path L2: `0.307` / `0.951`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.240` / `0.074`
- raw/shape physical B residual to PyPEEC: `2.883` / `0.514`
- scalar fit to PyPEEC / delta vs no-topology: `0.232` / `0.855`

## `trace_with_return_path__v83` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.075`
- allocation error: `0.425`
- signal/return path L2: `0.307` / `0.951`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.240` / `0.074`
- raw/shape physical B residual to PyPEEC: `2.883` / `0.514`
- scalar fit to PyPEEC / delta vs no-topology: `0.232` / `0.855`

## `trace_with_return_path__v33` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.076`
- allocation error: `0.424`
- signal/return path L2: `0.272` / `0.946`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.201` / `0.084`
- raw/shape physical B residual to PyPEEC: `2.858` / `0.514`
- scalar fit to PyPEEC / delta vs no-topology: `0.234` / `0.837`

## `trace_with_return_path__v73` / `unet_topology_two_stage_refined`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.076`
- allocation error: `0.424`
- signal/return path L2: `0.272` / `0.946`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.201` / `0.084`
- raw/shape physical B residual to PyPEEC: `2.858` / `0.514`
- scalar fit to PyPEEC / delta vs no-topology: `0.234` / `0.837`

## `trace_with_return_path__v33` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.076`
- allocation error: `0.424`
- signal/return path L2: `0.272` / `0.946`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.223` / `0.084`
- raw/shape physical B residual to PyPEEC: `2.856` / `0.514`
- scalar fit to PyPEEC / delta vs no-topology: `0.234` / `0.835`

## `trace_with_return_path__v73` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.076`
- allocation error: `0.424`
- signal/return path L2: `0.272` / `0.946`
- true/pred/excess via components: `1` / `1` / `0`
- topology MSE / leakage: `0.223` / `0.084`
- raw/shape physical B residual to PyPEEC: `2.856` / `0.514`
- scalar fit to PyPEEC / delta vs no-topology: `0.234` / `0.835`

## `trace_with_return_path__v30` / `unet_no_topology`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.053`
- allocation error: `0.447`
- signal/return path L2: `0.352` / `1.035`
- true/pred/excess via components: `1` / `0` / `0`
- topology MSE / leakage: `0.283` / `0.046`
- raw/shape physical B residual to PyPEEC: `2.703` / `0.560`
- scalar fit to PyPEEC / delta vs no-topology: `0.239` / `0.000`

## `trace_with_return_path__v04` / `unet_topology_soft_loss`

- case type: `return_path`
- failure mode: `magnetic consistency failure`
- detailed mechanism: `layer-allocation mismatch`
- truth/pred return fraction: `0.500` / `0.048`
- allocation error: `0.452`
- signal/return path L2: `0.300` / `0.843`
- true/pred/excess via components: `1` / `2` / `1`
- topology MSE / leakage: `0.343` / `0.073`
- raw/shape physical B residual to PyPEEC: `2.648` / `0.301`
- scalar fit to PyPEEC / delta vs no-topology: `0.266` / `0.528`

