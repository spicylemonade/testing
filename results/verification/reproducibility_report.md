# Reproducibility Report

## Cross-Runtime Envelope

| scenario | sample every | terminal relative error | python runtime (s) | node runtime (s) |
| --- | --- | --- | --- | --- |
| circular_two_body | 1 | 0.000e+00 | 0.063 | 0.012 |
| figure_eight_three_body | 5 | 1.165e-14 | 0.067 | 0.017 |
| small_n_ring | 20 | 5.243e-15 | 0.163 | 0.022 |
| star_grazing_two_body | 2 | 1.032e-15 | 0.018 | 0.005 |

## Close-Encounter Safe And Unsafe Regimes

| mode | dt | final state error vs REBOUND | max energy drift | regime |
| --- | --- | --- | --- | --- |
| direct | 0.040 | 2.453e+00 | 1.436e+01 | unsafe |
| encounter_microstep | 0.040 | 5.043e-03 | 1.265e-01 | unsafe |
| resolution_coupled | 0.040 | 2.602e+00 | 1.516e+01 | unsafe |
| direct | 0.020 | 6.562e-01 | 2.516e+00 | unsafe |
| encounter_microstep | 0.020 | 4.546e-03 | 3.233e-02 | safe |
| resolution_coupled | 0.020 | 1.231e+00 | 5.126e+00 | unsafe |
| direct | 0.010 | 1.638e-01 | 5.380e-01 | unsafe |
| encounter_microstep | 0.010 | 2.190e-03 | 8.066e-03 | safe |
| resolution_coupled | 0.010 | 9.255e-01 | 3.639e+00 | unsafe |
| direct | 0.005 | 4.135e-02 | 1.307e-01 | unsafe |
| encounter_microstep | 0.005 | 5.502e-04 | 2.024e-03 | safe |
| resolution_coupled | 0.005 | 8.725e-01 | 3.403e+00 | unsafe |

## Divergence Notes

- The Python and Node direct-sum kernels stay within a tight tolerance envelope on the canonical bundle, so cross-runtime replay is bounded rather than exact.
- On the star-grazing stress case, the plain direct kernel is unsafe at coarse `dt`, while the encounter microstep variant becomes safe earlier than the unmodified path.
- Resolution-coupled softening can stabilize some coarse runs, but it changes the physics enough that it should be treated as an explicit teaching or visualization regime rather than a fidelity-preserving default.
