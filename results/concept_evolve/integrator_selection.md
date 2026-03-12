# Integrator Selection

Date: 2026-03-12
Lane: H1_multisource_cold_start

## Top 3 Concept Folders

1. `001_packet_scout_handoff_root`
   - Keep active as the champion family.
   - Why: It is the narrowest concept that directly targets helper-free pre-arbitration source scouting under heterogeneous weak sources.
2. `002_dual_bucket_polarity_split_bootstrap`
   - Keep as the first fallback / mixed-polarity specialist.
   - Why: It best preserves novelty if polarity mismatch proves to be the main differentiator versus recent multi-input piezo work.
3. `003_time_constant_ranked_arbiter`
   - Keep as the low-overhead comparator / source-awareness ablation line.
   - Why: It gives a cleaner path to equal-overhead comparison than the more speculative leakage-vote or charge-probe variants.

## Retired Or Secondary Concepts

- `004_reverse_leakage_vote_or`
  - Secondary only: valuable as a sub-block but too process-sensitive to lead the claim.
- `005_tokenized_uvlo_handoff_gate`
  - Secondary only: necessary control block, not strong enough as the headline novelty.
- `006_comparatorless_current_probe_bootstrap`
  - Secondary only until probe overhead is shown to beat the RC-ranker variant.

## Integration Notes

- The broad-task `concept_evolve.py evolve` run was not used as the concept source because it produced no target artifacts and drifted off-lane.
- The concept tree here is a focused H1 workaround grounded in the repaired literature snapshot and the prior-art gap matrix.
- All later baseline, netlist, and verification artifacts should link back to `001_packet_scout_handoff_root` as the champion family root.
