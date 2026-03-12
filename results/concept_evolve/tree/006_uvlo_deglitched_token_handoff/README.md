# Concept: uvlo_deglitched_token_handoff

- Rank: 6
- Domains: energy_harvesting_pmic, handoff_control, uvlo_chatter_mitigation
- Key mechanism: Token accumulator measures sustained energy margin before handoff.
- Novelty rationale: High practical value for H1 experiments, but too incremental to headline by itself.

## Dependencies
- token integrator
- window comparator
- handoff gate
- reset path

## First Experiment
- Ultra-slow 0.1 and 1 mV/s ramps with source collapse near handoff; compare false starts and control energy against ordinary UVLO wakeup.

## Predicted Failure Mode
- Delay and integrator leakage make it useful only as an ablation switch, not the main novelty claim.

## Closest Overlap Papers
- A 220-mV Power-on-Reset Based Self-Starter With 2-nW Quiescent Power for Thermoelectric Energy Harvesting Systems (d30bff950b51bfb17324047f1b9193d837341002)
- A CMOS Startup Circuit for Thermoelectric Energy Harvesting Systems (d9415d1253fb75da110cffc9d1ab87509010d30e)
