# Hypothesis Scout H1 Cards

Parent reconstruction after codex child-pass stream disconnect.

## impedance_ranked_packet_probe
- Description: Probe each weak source with a nanowatt packet load, rank recovery slope without a helper rail, and grant the strongest source first access to the startup path before enabling the rest. The goal is source-aware cold start without a full MPPT controller.
- Dependencies: source models, packet probe capacitor, recovery-slope detector, source-ranking latch, sequenced OR-ing network, startup reservoir
- First experiment: Sweep 20/50/100/300 mV sources across 1:1, 1:5, and 1:20 impedance ratios and compare startup success, time-to-handoff, and startup-control energy against a fixed path and a non-source-aware multi-input baseline.
- Predicted failure mode: Probe energy or ranking ambiguity under ultra-slow ramps erases the startup benefit.

## dual_path_helperless_startup
- Description: Use two helper-free startup engines that share one reservoir: a passive charge-stacking path for very high-impedance weak sources and a burst-transfer path for lower-impedance sources. A self-referenced selector activates only one engine until the reservoir can sustain arbitration overhead.
- Dependencies: passive stacker, burst-transfer startup path, mode selector, startup reservoir, anti-backdrive OR-ing
- First experiment: Run the H1 matrix with asymmetric impedance and ramp-rate corners, logging whether the selected startup path matches the winning source regime and whether handoff time improves over a one-path startup.
- Predicted failure mode: Duplicated startup-path parasitics and selector leakage dominate at 20-50 mV.

## polarity_split_dual_bucket_bootstrap
- Description: Accumulate positive and negative or phase-skewed inputs into separate low-leakage scout buckets, then merge into the main reservoir only after one bucket can sustain isolation overhead. This converts mixed-polarity startup from a rectification problem into a staged-energy-aggregation problem.
- Dependencies: positive scout bucket, negative scout bucket, merge gate, cross-coupled latch, main reservoir
- First experiment: Mixed-polarity cases at 20-100 mV with 1:20 impedance asymmetry; compare back-drive loss and handoff success against a single-reservoir OR-ing baseline.
- Predicted failure mode: Bucket leakage or merge-threshold overhead destroys net gain below 50 mV.

## source_signature_charge_packet_startup
- Description: Transfer charge from each source in discrete packets only when a local envelope and recovery signature indicate that the source can recover before the next packet. The reservoir sees controlled packet arrivals instead of uncontrolled contention.
- Dependencies: local envelope detector, packet switch, recovery timer, shared reservoir, handoff gate
- First experiment: Impedance-asymmetry and source-collapse falsifier cases comparing packetized versus always-connected startup paths.
- Predicted failure mode: Local timing blocks consume more energy than the packetization saves.

## anti_backdrive_latched_oring
- Description: Keep startup OR-ing devices hard-off until a source-local latch has enough evidence to justify one-way conduction, then hold directionality through short reservoir droops. This makes reverse leakage an explicit startup design variable.
- Dependencies: source-local latch capacitor, ultra-low-leakage OR-ing switch, reverse-current monitor, startup reservoir
- First experiment: Run mixed-polarity, source-collapse, and UVLO-chatter cases while measuring back-drive loss versus ordinary diode-connected OR-ing.
- Predicted failure mode: Latch set/reset chatter or monitor overhead makes it a useful sub-block but not a standalone thesis.

## uvlo_deglitched_token_handoff
- Description: Require a time-integrated token, not a single UVLO crossing, before waking the main control path. This trades a tiny analog state element for lower chatter under ultra-slow ramps and asynchronous source arrival.
- Dependencies: token integrator, window comparator, handoff gate, reset path
- First experiment: Ultra-slow 0.1 and 1 mV/s ramps with source collapse near handoff; compare false starts and control energy against ordinary UVLO wakeup.
- Predicted failure mode: Delay and integrator leakage make it useful only as an ablation switch, not the main novelty claim.
