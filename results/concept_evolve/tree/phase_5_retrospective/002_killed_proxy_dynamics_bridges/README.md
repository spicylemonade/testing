# Killed Proxy-Dynamics Bridges

## Status

Killed.

## Summary

The run retires proxy-heavy branches such as:

- `anisotropic_current_screening`
- `odometer_rotor_transport_bridge`
- `observer_guided_macrocell_search`
- the earlier phase-3 neural-CA and modular-shadow branches

These branches failed the final screening because they depend too heavily on transport observables, observer heuristics, modular detours, or generic automated-search framing rather than on direct exact-decoder evidence.

## Traceback

- `results/concept_evolve/tree/phase_3_core/004_killed_modular_shadow_curriculum/README.md`
- `results/concept_evolve/tree/phase_3_core/005_killed_neural_ca_black_box/README.md`
- `results/verification/benchmark_report.md`
- `results/verification/novelty_report.md`
- `results/concept_evolve/bridge_candidates.json`

## Dependency

No immediate follow-up is justified. Reopening any of these ideas would require exact evidence that they improve verified hit rate or score under the shared decoder, not just proxy behavior.
