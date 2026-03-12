# Concept: dual_bucket_polarity_split_bootstrap

- Rank: 2
- Description: Maintain two startup reservoirs, one for forward-chargeable sources and one for reverse-suspect sources, and merge them only after a polarity-safe latch confirms that no source will be back-driven during handoff.
- Key mechanism: Use separate isolation FET stacks and tiny sign-detection packets to hold ambiguous sources out of the main startup bus until safe.
- Predicted failure mode: Extra bucket and merge overhead dominate the startup budget under the weakest ramps.

## Dependencies
- positive startup bucket
- negative startup bucket
- merge clamp
- polarity-safe latch

## First Experiment
- Inject one positive and one inverted source with unequal source resistances and measure whether the architecture prevents wrong-way current while still reaching handoff.

## Novelty Guard
- Survives only if mixed-polarity startup is shown as a first-class failure mode instead of being hidden inside a helper-source or single-polarity experiment.

## Closest Overlap
- A self-powered multi-input OSECE interface circuit for multiple piezoelectric transducers (6022e537)
- Self-Powered Collaborative Energy Harvesting Interface Circuit for Stacked Multiple Piezoelectric Elements (0fd82792)
- A Thermoelectric Energy Harvesting System Assisted by a Piezoelectric Transducer Achieving 10-MV Cold-Startup and 82.7% Peak Efficiency (dfecac25)
