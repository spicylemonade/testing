# Killed Proxy-Dynamics Bridges

## Status

Killed.

## Summary

The final run retires the proxy-heavy bridge family:

- `anisotropic_current_screening`
- `odometer_rotor_transport_bridge`
- `observer_guided_macrocell_search`

These branches were not killed because cellular automata are irrelevant in general. They were killed because they lean on current, transport, observer, or generic-search stories that do not survive the run's exact-score and no-repair discipline.

## Traceback

- `results/swarm/falsifier.md`
- `results/verification/benchmark_report.md`
- `results/verification/novelty_report.md`
- `results/concept_evolve/bridge_candidates.json`

## Dependency

There is no direct follow-up on these branches unless a future exact-valid dataset shows that one of their proxy observables predicts exact score after full decode. Without that dependency being met, they stay retired.
