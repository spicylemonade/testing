# Concept: packet_scout_handoff_root

- Rank: 1
- Description: Comparatorless charge-packet scouting probes each source through forward and reverse startup paths, ranks viable inputs, accumulates one minimum energy packet, then enables the main arbiter only once a safe handoff condition is latched.
- Key mechanism: Use mirrored subthreshold pulse injectors plus capacitor slew comparison to estimate polarity/strength without an always-on comparator.
- Predicted failure mode: Probe energy or mirror mismatch erases the gain, making it no better than a fixed startup path.

## Dependencies
- dual probe capacitors
- mirrored pulse injectors
- startup OR-ing devices
- handoff latch

## First Experiment
- Sweep mixed 20/50/100/300 mV sources, slow ramps, and 1:1/1:5/1:20 source impedances; compare startup success and back-drive loss against fixed-path and non-aware OR-ing baselines.

## Novelty Guard
- The claimed novelty is not lower startup voltage or better steady-state extraction; it is helper-free pre-arbitration source scouting under heterogeneous polarity and impedance before the main control loop exists.

## Closest Overlap
- Fully Integrated Startup at 70 mV of Boost Converters for Thermoelectric Energy Harvesting (c75c82be)
- Configurable Hybrid Energy Synchronous Extraction Interface With Serial Stack Resonance for Multi-Source Energy Harvesting (254a50d3)
- Self-Powered Collaborative Energy Harvesting Interface Circuit for Stacked Multiple Piezoelectric Elements (0fd82792)
