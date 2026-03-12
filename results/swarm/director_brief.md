# Director Brief

## Champion

- **H1_multisource_cold_start**: Source-Adaptive Cold Start for Weak Multi-Source Harvesters Under Ultra-Slow Ramps.

This is the best novelty-to-falsifiability trade in the current material. It is not directly entangled with the falsifier memo's near-dead branches, it targets a concrete circuit failure mode that matters in practice, and `gap_map.md` already flags it as the most simulation-ready ngspice-first route. The claim is narrow enough to verify cleanly: startup correctness under heterogeneous weak sources before normal arbitration is alive.

## Backup

- **H2_cryo_support_blocks**: Cryogenic low-frequency-noise-resilient bias/reference/comparator support blocks below 10 K.

This is the backup because its raw novelty moat is stronger than H3, but its first verification gate is worse. If validated cryogenic models or a collaborator path already exist, this lane becomes much more attractive. Without that model gate, it is too easy to write a plausible brief and too hard to generate an early, credible go/kill result.

## Reserve

- **H3_dynamic_source_impedance** remains the reserve lane.

It has a fast falsifier and good ngspice fit, but the 2025 variable-impedance overlap narrows the headline novelty margin enough that it should not outrank H2 unless cryogenic model access is absent and H1 dies early.

## Why The Other Branches Lost

- Do not reopen oscillator-based interleaving as a lead claim; `prior_art_gap.md` already records that pivot away.
- Do not use the falsifier memo's metaphor-heavy branches as backups. Reaction-diffusion gate meshes, converter-ringing reservoir framing, exceptional-point gate probes, ferroionic observers, electrocaloric tile drivers, and phased strain-wave meshes all carry higher rehash or accounting risk than the shortlisted directions.

## Blocker And Handoff

- `results/swarm/hypothesis_bridge.md` and `results/swarm/hypothesis_negative_space.md` are missing, so the scout chain is not fully auditable. The surviving selection therefore relies on `gap_map.md`, `falsifier.md`, and the prior-art notes that are present.
- Exact next experiment for the researcher on the champion:
  - Run one go/kill ngspice cold-start matrix covering source voltages `20/50/100/300 mV`, ramp rates `0.1/1/10/100 mV/s`, impedance ratios `1:1/1:5/1:20`, and mixed-polarity cases; report startup success, time-to-handoff, back-drive loss, and startup-control energy against two strong baselines.
- Exact next experiment for the researcher on the backup:
  - Only if validated cryogenic models exist, run one widened-corner sweep on a charge-domain reference/comparator macro-concept from `300 K` down to `4 K` with widened threshold-shift, mismatch, and low-frequency-noise assumptions; kill the lane if monotonicity or power budget collapses.
