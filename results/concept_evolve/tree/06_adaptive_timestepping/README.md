# ADAPTIVE_TIMESTEPPING

Dynamically adjust dt based on local acceleration magnitude or closest approach distance. Essential for handling the extreme dynamic range of gravitational encounters (close periapsis vs. distant apoapsis).

## Mathematical Formalization

dt_new = eta * min_i(|v_i|/|a_i|, sqrt(eps/|a_i|)).  Block time-stepping: group particles by dt into powers of 2, synchronize at common multiples.  Constraint: sum(dt_k) = T_total, max(|dE/E|) < tolerance.

## Analogical Connections

- Adaptive dt <-> learning rate scheduling in training (reduce step size in hard regions)
- Block time-stepping <-> hierarchical task scheduling (different tasks at different frequencies)
- Close encounter detection <-> collision detection in game engines (narrow-phase trigger)

## Implementation Hypothesis

Simplest version: dt = eta * min(v/a) globally. More sophisticated: per-particle block timesteps with shared synchronization points. Start with global adaptive, upgrade later. ~25 lines for global.

## Experiment Seed

Simulate a highly eccentric (e=0.95) two-body orbit with fixed dt=0.01 and adaptive dt(eta=0.01). Compare energy conservation and wall-clock time. Adaptive should achieve 100x better conservation at equal or less compute.
