# Concept: dual_path_helperless_startup

- Rank: 2
- Domains: energy_harvesting_pmic, multi_mode_startup, weak_source_conversion
- Key mechanism: Self-referenced mode selection between two startup paths before the main PMU comes alive.
- Novelty rationale: Distinct from low-voltage single-source startup papers because the claim is about helper-free mode selection among heterogeneous weak sources.

## Dependencies
- passive stacker
- burst-transfer startup path
- mode selector
- startup reservoir
- anti-backdrive OR-ing

## First Experiment
- Run the H1 matrix with asymmetric impedance and ramp-rate corners, logging whether the selected startup path matches the winning source regime and whether handoff time improves over a one-path startup.

## Predicted Failure Mode
- Duplicated startup-path parasitics and selector leakage dominate at 20-50 mV.

## Closest Overlap Papers
- Fully Integrated Startup at 70 mV of Boost Converters for Thermoelectric Energy Harvesting (c75c82be2e98a8d66907742a89b886902c1a0162)
- A CMOS Startup Circuit for Thermoelectric Energy Harvesting Systems (d9415d1253fb75da110cffc9d1ab87509010d30e)
- A Thermoelectric Energy Harvesting System Assisted by a Piezoelectric Transducer Achieving 10-MV Cold-Startup and 82.7% Peak Efficiency (dfecac253dbefc0807d87edafe69873b2a45bfc1)
