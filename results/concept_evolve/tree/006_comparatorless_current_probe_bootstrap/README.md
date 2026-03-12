# Concept: comparatorless_current_probe_bootstrap

- Rank: 6
- Description: Estimate source strength by injecting symmetric charge probes and reading only passive capacitor slew, avoiding explicit comparator bias until after the first viable source wins startup.
- Key mechanism: A purely charge-domain probe might be cheaper than RC rankers when ramps are extremely slow and source impedance is the main uncertainty.
- Predicted failure mode: Capacitor mismatch and injected charge loss make the probe estimate too inaccurate to justify the complexity.

## Dependencies
- probe capacitor
- charge injector
- differential storage node

## First Experiment
- Compare probe energy versus startup-time benefit against the time-constant ranker in the 1:5 and 1:20 impedance cases.

## Novelty Guard
- This is the lowest-overhead source-awareness path; it survives only if the passive probe remains materially cheaper than explicit arbitration hardware.

## Closest Overlap
- Fully Integrated Startup at 70 mV of Boost Converters for Thermoelectric Energy Harvesting (c75c82be)
- Single- and multi-source battery-less power management circuits for piezoelectric energy harvesting systems (9fd5e15b)
