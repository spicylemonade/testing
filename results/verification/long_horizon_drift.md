# Long-Horizon Drift

Generated: 2026-03-06T03:07:58Z

## circular_two_body

| dt | max energy drift | max angular-momentum drift | max COM drift | pass |
| --- | --- | --- | --- | --- |
| 0.0200 | 3.998e-08 | 2.998e-15 | 0.000e+00 | pass |
| 0.0100 | 2.500e-09 | 2.442e-15 | 0.000e+00 | pass |
| 0.0050 | 1.562e-10 | 2.442e-15 | 0.000e+00 | pass |

Convergence check: pass based on monotonic improvement under timestep halving.

## figure_eight_three_body

| dt | max energy drift | max angular-momentum drift | max COM drift | pass |
| --- | --- | --- | --- | --- |
| 0.0100 | 5.903e-05 | 1.887e-03 | 5.495e-15 | pass |
| 0.0050 | 1.474e-05 | 3.164e-03 | 5.782e-15 | pass |
| 0.0025 | 3.683e-06 | 3.664e-03 | 7.290e-15 | pass |

Convergence check: fail based on monotonic improvement under timestep halving.
Figure-eight note: the angular-momentum convergence gate is flagged because this choreography starts near zero total angular momentum, so the relative-drift ratio is especially noise-sensitive.

## small_n_ring

| dt | max energy drift | max angular-momentum drift | max COM drift | pass |
| --- | --- | --- | --- | --- |
| 0.0040 | 8.612e-07 | 2.735e-15 | 1.646e-18 | pass |
| 0.0020 | 2.181e-07 | 1.709e-15 | 1.840e-18 | pass |
| 0.0010 | 5.469e-08 | 3.931e-15 | 1.646e-18 | pass |

Convergence check: pass based on monotonic improvement under timestep halving.

