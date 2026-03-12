# Item 016 Selection Memo

Date: 2026-03-12
Scope: core-research synthesis for `H1_multisource_cold_start`
Status: PASS with one active champion and one kill-ready fallback

## Execution Note

- Fresh item-specific child refresh was attempted, but it did not materialize dedicated `item016_*` note files before the parent run resumed.
- This memo therefore synthesizes the saved role outputs already present in the repo plus the new iterate-state artifacts:
  - research director: `results/swarm/director_brief.md`
  - hypothesis scout: `results/concept_evolve/notes/hypothesis_scout_h1_cards.md`
  - novelty checker: `results/concept_evolve/notes/novelty_checker_h1.md`
  - falsifier: `results/swarm/falsifier.md`
  - integrator: `results/concept_evolve/integrator_selection.md`
  - iteration refresh: `results/concept_evolve/bridge_candidates.json`, `results/concept_evolve/concept_delta.json`, `results/concept_evolve/recurrent_state.json`

## Research Director Input

- Keep the H1 lane active because it remains the best novelty-to-falsifiability trade in the saved swarm state.
- Within H1, stay on the narrow startup-correctness thesis rather than broad multi-source PMU or efficiency language.
- The next experiment gate remains the bounded `ngspice` startup matrix under weak heterogeneous sources.

## Hypothesis Scout Input

- `packet_scout_handoff_root` remains the only branch whose first experiment directly matches the H1 claim.
- `dual_bucket_polarity_split_bootstrap` is the only alternative branch that still opens a materially different failure regime: mixed-polarity startup before safe rail merge.
- `time_constant_ranked_arbiter` remains useful, but only as a lower-overhead comparison line.

## Novelty Checker Input

- `packet_scout_handoff_root` is the only headline-worthy H1 angle.
- `dual_bucket_polarity_split_bootstrap` remains defensible only as a narrow fallback.
- `time_constant_ranked_arbiter` is too close to ordinary adaptive arbitration to anchor the thesis.
- `reverse_leakage_vote_or`, `tokenized_uvlo_handoff_gate`, and `comparatorless_current_probe_bootstrap` do not retain enough independent novelty margin.

## Falsifier Input

- The champion survives only if mixed-polarity and `1:20` impedance cases show a real difference against both baselines.
- The fallback survives only if its extra buckets do not become a hidden helper reservoir or leak away the benefit below `50 mV`.
- Weak branches should be retired now rather than being allowed to inflate the apparent search space.

## Integrator Input

- The canonical concept-tree ranking already narrowed the H1 family to:
  - one active headline family: `001_packet_scout_handoff_root`
  - one narrow fallback: `002_dual_bucket_polarity_split_bootstrap`
  - one benchmark-only line: `003_time_constant_ranked_arbiter`
- The iterate pass reinforces the same outcome:
  - promoted bridges: `packet_scout_handoff_root`, `dual_bucket_polarity_split_bootstrap`
  - retired bridges: `reverse_leakage_vote_or`, `comparatorless_current_probe_bootstrap`

## Decision

- Active champion:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/rc_ranked_packet_gate.cir`
- Kill-ready fallback:
  - `results/concept_evolve/tree/002_dual_bucket_polarity_split_bootstrap`

## Why The Fallback Is Kill-Ready

- It is the only remaining branch that attacks a different direct failure mode than the champion:
  - polarity-safe startup and delayed rail merge under mixed-polarity weak sources
- It already has a frozen concept folder, novelty guard, first experiment, and explicit failure mode.
- If the champion collapses because source ranking does not separate from the nonaware baseline, the dual-bucket branch is the next H1 test that could still preserve a nontrivial mixed-polarity thesis.

## Retired Or Downgraded Branches

- Retired from the architecture race:
  - `003_time_constant_ranked_arbiter`
  - `004_reverse_leakage_vote_or`
  - `005_tokenized_uvlo_handoff_gate`
  - `006_comparatorless_current_probe_bootstrap`
- Retirement rationale:
  - `003` stays valuable only as an ablation or benchmark line
  - `004` depends on fragile leakage-signature sensing with weak novelty margin
  - `005` is a support block, not a distinct multi-source architecture
  - `006` is at best an implementation detail inside the packet-scout family

## Net Result

- Exactly one H1 champion architecture remains active.
- Exactly one H1 fallback remains available for activation if the champion fails its startup matrix.
- All other H1 branches are retired from headline status before the experiment phase begins.
