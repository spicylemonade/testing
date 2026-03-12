# Concept: polarity_split_dual_bucket_bootstrap

- Rank: 3
- Domains: energy_harvesting_pmic, mixed_polarity_startup, anti_backdrive
- Key mechanism: Dual scout buckets plus cross-coupled merge gating delay shared-reservoir exposure until startup is safe.
- Novelty rationale: Targets the exact mixed-polarity startup regime that most recovered overlap papers do not benchmark explicitly.

## Dependencies
- positive scout bucket
- negative scout bucket
- merge gate
- cross-coupled latch
- main reservoir

## First Experiment
- Mixed-polarity cases at 20-100 mV with 1:20 impedance asymmetry; compare back-drive loss and handoff success against a single-reservoir OR-ing baseline.

## Predicted Failure Mode
- Bucket leakage or merge-threshold overhead destroys net gain below 50 mV.

## Closest Overlap Papers
- Self-Powered Collaborative Energy Harvesting Interface Circuit for Stacked Multiple Piezoelectric Elements (0fd827923bda6369f44527bd52fdf7b4c60e4941)
- A self-powered multi-input OSECE interface circuit for multiple piezoelectric transducers (6022e53796c25cba2130c9505c6e6c908fd43cb0)
- Configurable Hybrid Energy Synchronous Extraction Interface With Serial Stack Resonance for Multi-Source Energy Harvesting (254a50d3d11f95e13c87d5b068a92e29fb0f2dee)
