# Champion Concept: packet_scout_handoff_root

This folder is the canonical H1 root for all later netlists, manifests, tables, and verification outputs in the `H1_multisource_cold_start` lane.

- Rank: 1
- Description: Comparatorless charge-packet scouting probes each source through forward and reverse startup paths, ranks viable inputs, accumulates one minimum energy packet, then enables the main arbiter only once a safe handoff condition is latched.
- Key mechanism: mirrored subthreshold pulse injectors plus capacitor slew comparison to estimate polarity and source strength without an always-on comparator.
- Predicted failure mode: probe energy or mirror mismatch erases the gain, making the design no better than a fixed startup path.

## Canonical Links

- Dependency map: [dependency_map.md](dependency_map.md)
- Experiment spec: [experiment_spec.md](experiment_spec.md)
- Netlists: [netlists/README.md](netlists/README.md)
- Raw outputs and manifests: [results/README.md](results/README.md)
- Tables: [tables/README.md](tables/README.md)
- Lane-local verification: [verification/README.md](verification/README.md)

## Novelty Guard

The claim is not lower startup voltage or better steady-state extraction. The claim is helper-free pre-arbitration source scouting under heterogeneous polarity and impedance before the main control loop exists.

## Closest Overlap

- Fully Integrated Startup at 70 mV of Boost Converters for Thermoelectric Energy Harvesting (`c75c82be`)
- Configurable Hybrid Energy Synchronous Extraction Interface With Serial Stack Resonance for Multi-Source Energy Harvesting (`254a50d3`)
- Self-Powered Collaborative Energy Harvesting Interface Circuit for Stacked Multiple Piezoelectric Elements (`0fd82792`)
