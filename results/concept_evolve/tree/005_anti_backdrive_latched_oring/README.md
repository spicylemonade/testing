# Concept: anti_backdrive_latched_oring

- Rank: 5
- Domains: energy_harvesting_pmic, anti_backdrive, startup_isolation
- Key mechanism: Source-local latch delays and direction-locks OR-ing devices during startup.
- Novelty rationale: Important enabling block for H1, but too narrow to carry the full claim alone.

## Dependencies
- source-local latch capacitor
- ultra-low-leakage OR-ing switch
- reverse-current monitor
- startup reservoir

## First Experiment
- Run mixed-polarity, source-collapse, and UVLO-chatter cases while measuring back-drive loss versus ordinary diode-connected OR-ing.

## Predicted Failure Mode
- Latch set/reset chatter or monitor overhead makes it a useful sub-block but not a standalone thesis.

## Closest Overlap Papers
- Single- and multi-source battery-less power management circuits for piezoelectric energy harvesting systems (9fd5e15b325f8534ee928242f7e9507a01586677)
- Self-Powered Collaborative Energy Harvesting Interface Circuit for Stacked Multiple Piezoelectric Elements (0fd827923bda6369f44527bd52fdf7b4c60e4941)
