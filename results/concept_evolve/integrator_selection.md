# Integrator Selection

Date: 2026-03-12
Lane: `H1_multisource_cold_start`
Method: saved-artifact-only synthesis from the specified H1 context, literature, swarm, falsifier, and concept-evolve notes. No new broad search.

There are exactly six viable canonical H1 concept folders in the saved tree. Materialize all six folders, but keep only the top three as independent experiment lines. Folders 4-6 are downgraded to supporting or conditional roles because their novelty margin is too thin once overhead and falsifier rules are enforced.

## Canonicalization

- `001_packet_scout_handoff_root` is the canonical folder for scout alias `impedance_ranked_packet_probe`.
- `002_dual_bucket_polarity_split_bootstrap` is the canonical folder for scout alias `polarity_split_dual_bucket_bootstrap`.
- `004_reverse_leakage_vote_or` is the canonical folder for scout alias `anti_backdrive_latched_oring`.
- `005_tokenized_uvlo_handoff_gate` is the canonical folder for scout alias `uvlo_deglitched_token_handoff`.
- `dual_path_helperless_startup` is retired as a standalone folder. Its useful pieces can only survive inside `001` or `002`.
- `source_signature_charge_packet_startup` is downgraded and absorbed into `001` and `006` rather than materialized as its own folder.

## Top 6 To Materialize

1. `results/concept_evolve/tree/001_packet_scout_handoff_root`
- Tier: champion.
- H1 novelty: this is the only concept that keeps the director-brief claim intact: helper-free source scouting before the main arbiter is alive, under heterogeneous ramp, impedance, and polarity conditions.
- Overhead risk: probe energy, sequencing delay, mirror mismatch, or any hidden precharge node can erase the gain fast.
- Falsifier fit: keep only if it beats fixed-path and non-source-aware multi-input startup under equal accounting, includes mixed-polarity plus `1:20` impedance cases, and never behaves like a helper rail.

2. `results/concept_evolve/tree/002_dual_bucket_polarity_split_bootstrap`
- Tier: narrow fallback.
- H1 novelty: strongest backup only if mixed-polarity cold start remains the unresolved failure mode not covered by the closest 2023-2024 multi-input piezo interfaces.
- Overhead risk: two scout buckets, merge clamps, and cross-coupled control are expensive below `50 mV`; leakage can collapse the benefit.
- Falsifier fit: downgrade immediately if a simple rectifier or ideal-diode baseline removes the advantage, or if one bucket effectively becomes a helper reservoir.

3. `results/concept_evolve/tree/003_time_constant_ranked_arbiter`
- Tier: low-overhead ablation and benchmark line.
- H1 novelty: weaker than the top two, but it is the cleanest source-aware comparator that can satisfy the falsifier demand for a strong equal-accounting baseline.
- Overhead risk: acceptable only if the RC ranker is materially cheaper than explicit compare-and-select logic.
- Falsifier fit: keep as a benchmark family, not a thesis family; retire as a lead claim if it collapses to ordinary arbitration or fails to improve startup benefit per control energy.

4. `results/concept_evolve/tree/004_reverse_leakage_vote_or`
- Tier: supporting sub-block only.
- Why downgraded: anti-backdrive is necessary for H1, but leakage-vote sensing is too process-sensitive and too easy for ideal-diode or latched-OR baselines to match.
- Overhead risk: windowing, latch stability, and calibration overhead can dominate the small reverse-current win.
- Falsifier fit: keep only if it measurably improves startup correctness, not just reverse-current cosmetics.

5. `results/concept_evolve/tree/005_tokenized_uvlo_handoff_gate`
- Tier: supporting handoff block only.
- Why downgraded: by itself it reads like a refined POR or UVLO deglitcher, not a multi-source cold-start architecture.
- Overhead risk: token accumulation and reset energy can drift toward the same control budget as ordinary startup-control baselines.
- Falsifier fit: keep only if it fixes real UVLO chatter or false handoff in the H1 mixed-source matrix that conventional hysteresis does not.

6. `results/concept_evolve/tree/006_comparatorless_current_probe_bootstrap`
- Tier: conditional merge candidate.
- Why downgraded: it only earns a separate folder if it is the lowest-overhead implementation of packet scouting; otherwise it is an implementation detail of `001`.
- Overhead risk: capacitor mismatch, injected-charge loss, and weak-source perturbation can corrupt the estimate while spending the same budget as the RC ranker.
- Falsifier fit: keep only if it beats `003` on startup benefit per control energy without requiring precharge, sense amplification, or hidden bias.

## Retired Or Absorbed Scout Concepts

- `dual_path_helperless_startup`
- Retired as a standalone concept because duplicated startup engines and selector leakage push directly into the H1 kill rule on overhead, while the framing drifts too close to existing low-voltage startup and assisted-startup prior art.

- `source_signature_charge_packet_startup`
- Downgraded and absorbed into `001_packet_scout_handoff_root` and `006_comparatorless_current_probe_bootstrap` because local signature timing plus packet transfer overlaps the 2023-2024 multi-input extraction family too closely once equal energy accounting is enforced.

## Decision

- Rank 1 `001_packet_scout_handoff_root` as the only active headline family.
- Rank 2 `002_dual_bucket_polarity_split_bootstrap` as the narrow fallback if mixed polarity is the real novelty moat.
- Rank 3 `003_time_constant_ranked_arbiter` as the required low-overhead ablation and benchmark line.
- Treat `004`, `005`, and `006` as downgraded support or conditional branches, not independent thesis claims.
