# Exp08 P5 synthetic registration stress curve

| stress | mode | n | 4-way acc | H0 acc | H1 acc | H2 acc | H3 acc | no-via FP | median residual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| identity | base | 32 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.009e-06 |
| identity | global_registered | 32 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.009e-06 |
| translation_40um | base | 32 | 0.8125 | 0.6250 | 0.6250 | 1.0000 | 1.0000 | 0.1250 | 0.1596 |
| translation_40um | global_registered | 32 | 0.7812 | 0.5000 | 0.6250 | 1.0000 | 1.0000 | 0.0417 | 0.1588 |
| translation_80um | base | 32 | 0.5938 | 0.1250 | 0.3750 | 1.0000 | 0.8750 | 0.3750 | 0.3020 |
| translation_80um | global_registered | 32 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.008e-06 |
| translation_120um | base | 32 | 0.3750 | 0.0000 | 0.0000 | 1.0000 | 0.5000 | 0.5000 | 0.4192 |
| translation_120um | global_registered | 32 | 0.8125 | 0.6250 | 0.6250 | 1.0000 | 1.0000 | 0.1250 | 0.1593 |
| rotation_1.0deg | base | 32 | 0.7812 | 0.3750 | 0.7500 | 1.0000 | 1.0000 | 0.0000 | 0.0657 |
| rotation_1.0deg | global_registered | 32 | 0.9375 | 0.7500 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0331 |
| rotation_2.0deg | base | 32 | 0.6250 | 0.1250 | 0.5000 | 1.0000 | 0.8750 | 0.0000 | 0.1307 |
| rotation_2.0deg | global_registered | 32 | 0.9062 | 0.6250 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0333 |
| scale_0.010 | base | 32 | 0.8438 | 0.3750 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0225 |
| scale_0.010 | global_registered | 32 | 0.9688 | 0.8750 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0111 |
| scale_0.020 | base | 32 | 0.7812 | 0.2500 | 0.8750 | 1.0000 | 1.0000 | 0.0000 | 0.0447 |
| scale_0.020 | global_registered | 32 | 0.9688 | 0.8750 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0110 |
| standoff_15um | base | 32 | 0.4062 | 0.0000 | 0.3750 | 1.0000 | 0.2500 | 0.0000 | 0.0916 |
| standoff_15um | global_registered | 32 | 0.3750 | 0.0000 | 0.3750 | 0.8750 | 0.2500 | 0.0000 | 0.0916 |
| standoff_30um | base | 32 | 0.3125 | 0.0000 | 0.0000 | 1.0000 | 0.2500 | 0.0000 | 0.1568 |
| standoff_30um | global_registered | 32 | 0.3125 | 0.0000 | 0.0000 | 1.0000 | 0.2500 | 0.0000 | 0.1554 |
| tilt_10mrad | base | 32 | 0.8438 | 0.3750 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0382 |
| tilt_10mrad | global_registered | 32 | 0.8438 | 0.3750 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0382 |
| tilt_20mrad | base | 32 | 0.8125 | 0.2500 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0770 |
| tilt_20mrad | global_registered | 32 | 0.8125 | 0.2500 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0770 |

The stressed observation field is generated from transformed graph geometry while the scorer sees the original graph. This is a synthetic registration sensitivity curve, not real CAD alignment.
