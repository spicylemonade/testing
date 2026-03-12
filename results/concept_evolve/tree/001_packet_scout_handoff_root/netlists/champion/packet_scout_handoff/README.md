# Packet Scout Handoff Variants

These are the original three H1 variants plus the DEEPEN near-tie branch under the champion subtree.

## Rank Order

1. `variant_01_rc_ranked_packet_gate`
   - preferred champion implementation
2. `variant_02_dual_bucket_polarity_merge`
   - mixed-polarity fallback inside the champion subtree
3. `variant_03_current_probe_token_gate`
   - low-helper current-probe and handoff-gating variant
4. `variant_04_confidence_gated_abstention`
   - DEEPEN branch for near-tie startup cases

## Mechanism Split

- `variant_01_rc_ranked_packet_gate`
  - source inference via recovery-time ranking after a small scout packet
  - minimum-energy accumulation via one shared startup reservoir
  - handoff gating via direct store-threshold release
- `variant_02_dual_bucket_polarity_merge`
  - polarity inference via separate positive and negative scout buckets
  - minimum-energy accumulation via staged bucket charge survival and merge
  - handoff gating via explicit merge latch
- `variant_03_current_probe_token_gate`
  - source inference via comparatorless current-probe delta
  - minimum-energy accumulation via fixed packet train into a shared reservoir
  - handoff gating via tokenized sustained-surplus release
- `variant_04_confidence_gated_abstention`
  - source inference via normalized RC scout margin and confidence integration
  - minimum-energy accumulation via blind packet isolation until the separability score commits
  - handoff gating via the shared store-threshold latch after confidence-based commit
