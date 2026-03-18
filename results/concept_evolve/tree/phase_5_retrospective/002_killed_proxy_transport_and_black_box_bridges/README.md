# Killed Proxy, Transport, And Black-Box Bridges

Status: killed

Trace-back artifact:

- `results/experiments/complexity_sweep.md`

Phase-5 synthesis:

- Proxy-heavy and transport-heavy ideas did not survive the final iterate pass.
- Retired bridges:
  - `anisotropic_current_screening`
  - `odometer_rotor_transport_bridge`
  - `observer_guided_macrocell_search`
- The earlier phase-3 neural-CA and modular-shadow kills remain correct.

Why this branch was killed:

- These ideas sit too close to bounded-slope trapping, transport analogies, or generic automated-search overlap.
- The phase-4 blocker reports left no exact evidence that any proxy observable predicts verified score.

Dependency for follow-up:

- none until exact-score calibration exists; without that, reopening this branch would recreate the proxy-metric trap.
