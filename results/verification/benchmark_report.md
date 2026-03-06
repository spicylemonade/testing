# Benchmark Report

Generated: 2026-03-06T05:13:32Z

## Error Tables

### circular_two_body

| comparator | dt | final state error vs REBOUND | max energy drift | runtime (s) |
| --- | --- | --- | --- | --- |
| minigrav_direct | 0.0100 | 2.094e-04 | 2.500e-09 | 0.058 |
| explicit_euler_classroom | 0.0100 | 5.229e-01 | 1.010e-01 | 0.054 |
| poliastro_two_body | 0.0100 | 9.915e-14 | 6.661e-16 | 6.859 |
| rebound_ias15 | 0.0100 | 0.000e+00 | 4.441e-16 | 0.079 |

### figure_eight_three_body

| comparator | dt | final state error vs REBOUND | max energy drift | runtime (s) |
| --- | --- | --- | --- | --- |
| minigrav_direct | 0.0050 | 5.938e-05 | 1.473e-05 | 0.063 |
| explicit_euler_classroom | 0.0050 | 8.214e-01 | 1.194e-01 | 0.056 |
| rebound_ias15 | 0.0050 | 0.000e+00 | 8.625e-16 | 0.040 |

### small_n_ring

| comparator | dt | final state error vs REBOUND | max energy drift | runtime (s) |
| --- | --- | --- | --- | --- |
| minigrav_direct | 0.0020 | 1.366e-04 | 2.180e-07 | 0.154 |
| explicit_euler_classroom | 0.0020 | 5.810e-01 | 9.755e-02 | 0.148 |
| rebound_leapfrog | 0.0020 | 0.000e+00 | 1.710e-09 | 0.008 |

### star_grazing_two_body

| comparator | dt | final state error vs REBOUND | max energy drift | runtime (s) |
| --- | --- | --- | --- | --- |
| minigrav_direct | 0.0200 | 6.562e-01 | 2.516e+00 | 0.009 |
| explicit_euler_classroom | 0.0200 | 2.965e+00 | 2.268e+01 | 0.008 |
| poliastro_two_body | 0.0200 | 7.453e-16 | 7.105e-15 | 0.048 |
| encounter_microstep | 0.0200 | 4.546e-03 | 3.233e-02 | 0.039 |
| rebound_ias15 | 0.0200 | 0.000e+00 | 3.553e-15 | 0.009 |

## Runtime Table

| scenario | fastest comparator | slowest comparator |
| --- | --- | --- |
| circular_two_body | explicit_euler_classroom (0.054s) | poliastro_two_body (6.859s) |
| figure_eight_three_body | rebound_ias15 (0.040s) | minigrav_direct (0.063s) |
| small_n_ring | rebound_leapfrog (0.008s) | minigrav_direct (0.154s) |
| star_grazing_two_body | explicit_euler_classroom (0.008s) | poliastro_two_body (0.048s) |

## Narrative

- `minigrav_direct` ties REBOUND closely on smooth two-body and small-N controls, while the classroom Euler baseline is consistently less accurate for the same timestep.
- `poliastro_two_body` is strongest on smooth two-body propagation but is not a mutual-gravity small-N baseline, so it does not replace REBOUND or the audited kernel on 3-body and small-N cases.
- `encounter_microstep` is the only variant aimed at the promoted close-encounter trust spine; it pays extra runtime on `star_grazing_two_body` in exchange for a dedicated encounter policy and round-trip reporting layer.
- REBOUND remains the accuracy anchor, which is expected; the minimal simulator wins only when transparency, machine-readable audit outputs, and close-encounter honesty matter more than feature breadth or raw integration sophistication.
