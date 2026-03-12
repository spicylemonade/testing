# H1 Multisource Cold-Start Concept Cards

Derived only from the saved H1 lane artifacts: `research_rubric.json`, `results/research_context.md`, `results/literature/literature_snapshot.json`, `results/literature/prior_art_gap.md`, `results/swarm/director_brief.md`, `results/swarm/hypotheses.json`, `results/swarm/tool_plan.md`, and `results/swarm/falsifier.md`.

## 1. `packet_scout_handoff_root`
- `symbolic_name`: `packet_scout_handoff_root`
- `description`: Issue tiny startup charge packets into each source branch, observe which branch recovers fastest, and let only that branch seed the shared startup reservoir until enough energy exists to pay for wider arbitration.
- `dependency list`: `scout packet capacitor`, `source-local sampling switch`, `recovery detector or monotonic latch`, `startup reservoir`, `sequenced OR-ing gate`, `handoff gate`
- `first experiment`: Run the H1 matrix over `20/50/100/300 mV` and `1:1/1:5/1:20` impedance ratios, then compare startup success, time-to-handoff, and probe/control energy against a fixed startup path and a non-source-aware multi-input startup path.
- `predicted failure mode`: The packet probes collapse the weakest sources or produce ambiguous rankings under ultra-slow ramps, so the control overhead exceeds the saved back-drive loss.
- `novelty rationale`: This keeps the H1 claim centered on pre-arbitration source selection rather than generic multi-source harvesting. It is materially different from single-source low-voltage startup papers because the main question is which source should be trusted first before the normal controller exists.

## 2. `time_constant_ranked_arbiter`
- `symbolic_name`: `time_constant_ranked_arbiter`
- `description`: Apply a fixed micro-load pulse to each source and use the recovery time constant, not open-circuit voltage alone, as an analog ranking signal for which source gets first access to startup.
- `dependency list`: `micro-load pulse injector`, `recovery timing capacitor`, `source ranking latch`, `branch isolation switch`, `startup reservoir`
- `first experiment`: Hold source voltage equal while varying source impedance and ramp rate, then test whether recovery-time ranking predicts the winning startup branch better than voltage-only selection.
- `predicted failure mode`: RC timing spread and leakage dominate below `50 mV`, so the measured time constant reflects circuit parasitics more than source strength.
- `novelty rationale`: The adaptation variable is source recoverability under load, which is more specific than the steady-state efficiency framing in the overlap papers. That makes it a direct H1 concept rather than another multi-input PMU story.

## 3. `dual_bucket_polarity_split_bootstrap`
- `symbolic_name`: `dual_bucket_polarity_split_bootstrap`
- `description`: Keep positive and negative or phase-opposed sources in separate scout buckets, then merge only the surviving bucket into the main reservoir once it can pay the isolation overhead.
- `dependency list`: `positive scout bucket`, `negative scout bucket`, `merge gate`, `cross-coupled isolation latch`, `main startup reservoir`
- `first experiment`: Run mixed-polarity `20-100 mV` cases with `1:20` impedance asymmetry and compare back-drive loss, startup success, and merge latency against a single-reservoir OR-ing baseline.
- `predicted failure mode`: Scout-bucket leakage and merge-threshold overhead erase the benefit below about `50 mV` or during very slow ramps.
- `novelty rationale`: This directly targets the mixed-polarity startup regime that the recovered H1 prior art does not make central. The contribution is staged cold-start aggregation, not just another rectifier or piezo interface.

## 4. `reverse_leakage_vote_or`
- `symbolic_name`: `reverse_leakage_vote_or`
- `description`: Turn on a branch OR-ing device only after multiple source-local indications agree that forward conduction is useful, then hold that decision through short reservoir droops to suppress cross-source back-drive during startup.
- `dependency list`: `source-local evidence capacitor`, `vote latch`, `ultra-low-leakage OR switch`, `reverse-current sense element`, `reservoir droop hold path`
- `first experiment`: Under source collapse, polarity mismatch, and UVLO-chatter cases, compare back-drive loss and false conduction events against diode-connected OR-ing and static ideal-switch OR-ing.
- `predicted failure mode`: The vote mechanism chatters or leaks enough current that it remains only a useful sub-block, not a viable top-level architecture.
- `novelty rationale`: This makes anti-backdrive a startup-state decision rather than a passive device choice. That is different enough to test cleanly, but still vulnerable to the H1 kill rule if the overhead dominates.

## 5. `tokenized_uvlo_handoff_gate`
- `symbolic_name`: `tokenized_uvlo_handoff_gate`
- `description`: Replace edge-triggered UVLO wakeup with a token integrator that releases the main controller only after sustained energy surplus, reducing premature handoff under ultra-slow ramps and asynchronous source arrival.
- `dependency list`: `token integrator capacitor`, `window detector`, `handoff gate`, `reset/discharge path`, `startup reservoir monitor`
- `first experiment`: At `0.1` and `1 mV/s` ramps with near-handoff source collapse, compare false starts, handoff time, and startup-control energy against ordinary UVLO wakeup.
- `predicted failure mode`: Integrator leakage adds too much delay, so chatter is reduced but successful startups are lost.
- `novelty rationale`: This is not a standalone thesis, but it is a plausible H1-specific adaptation for the failure mode where ordinary UVLO is too binary. Its value comes from being part of source-aware cold-start sequencing, not from claiming a generic reset invention.

## 6. `comparatorless_current_probe_bootstrap`
- `symbolic_name`: `comparatorless_current_probe_bootstrap`
- `description`: Infer source deliverability from the voltage delta caused by a fixed switched-cap current probe, using passive ratios and latches instead of a powered comparator so source awareness appears before any helper rail exists.
- `dependency list`: `switched-cap current probe`, `delta-hold capacitor`, `comparatorless latch or cross-coupled sampler`, `branch selector`, `startup reservoir`
- `first experiment`: Compare comparatorless probing against open-circuit-voltage selection in equal-voltage but unequal-impedance cases, measuring ranking accuracy and control energy at `20/50/100 mV`.
- `predicted failure mode`: Probe disturbance or sampler mismatch obscures the voltage delta at the lowest voltages, collapsing the advantage over a simpler selector.
- `novelty rationale`: This pushes H1 toward genuinely helper-free source inference. Unlike prior integrated startup work that mainly optimizes voltage threshold or startup path, this asks whether useful source classification can be done without an active comparator or helper rail.
