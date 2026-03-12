# Item 016 Selection Memo

Date: 2026-03-12
Scope: one active H1 champion architecture and one kill-ready fallback after the novelty screen and concept-iterate refresh
Status: PASS

## Input Role Set

This memo synthesizes the saved role outputs and refreshed concept state:

- `research_director`:
  - `results/swarm/director_brief.md`
- `hypothesis_scout`:
  - `results/concept_evolve/notes/hypothesis_scout_h1_cards.md`
- `novelty_checker`:
  - `results/concept_evolve/notes/novelty_checker_h1.md`
- `falsifier`:
  - `results/swarm/falsifier.md`
  - `verification/item011_signoff.md`
- `integrator`:
  - `results/concept_evolve/integrator_selection.md`
- refreshed recurrent state:
  - `results/concept_evolve/bridge_candidates.json`
  - `results/concept_evolve/concept_delta.json`
  - `results/concept_evolve/recurrent_state.json`
  - `verification/claim_matrix.md`

## Role Synthesis

### Research Director

- Keep H1 alive only as a startup-correctness thesis under heterogeneous weak sources.
- The active architecture must stay close to the exact first experiment and the kill rule in `results/swarm/tool_plan.md`.
- Conclusion:
  - champion = `001_packet_scout_handoff_root / variant_01_rc_ranked_packet_gate`
  - fallback = `002_dual_bucket_polarity_split_bootstrap`

### Hypothesis Scout

- `packet_scout_handoff_root` remains the only concept that keeps source scouting itself as the pre-arbitration control problem.
- `dual_bucket_polarity_split_bootstrap` is the only alternate branch that opens a distinct mixed-polarity regime rather than collapsing into ordinary arbitration.
- `time_constant_ranked_arbiter` is useful, but only as a lower-complexity comparison line.

### Novelty Checker

- `packet_scout_handoff_root` survives the closest startup and multi-input overlap only if mixed polarity, impedance asymmetry, and helper-free accounting stay mandatory.
- `dual_bucket_polarity_split_bootstrap` remains materially different enough to keep only as a fallback because its moat is narrow and disappears if startup is rectified to one polarity or if one bucket behaves like a helper reservoir.
- `time_constant_ranked_arbiter` is too close to ordinary adaptive arbitration to remain an active thesis branch.

### Falsifier

- The fastest way to kill H1 is still:
  - negligible `e_backdrive` on the nonaware baseline
  - no `startup_ok` or `t_handoff` advantage under mixed-polarity and `1:20` cases
  - hidden helper behavior or uncounted control overhead
- `dual_bucket_polarity_split_bootstrap` is kill-ready because one focused mixed-polarity sweep can invalidate it quickly if bucket leakage or merge overhead dominates.
- `time_constant_ranked_arbiter` is not the fallback because it is easier to accuse of ordinary RC arbitration and weaker on novelty even if it is useful as a control.

### Integrator

- Keep exactly one active architecture:
  - `variant_01_rc_ranked_packet_gate`
- Keep exactly one fallback:
  - `dual_bucket_polarity_split_bootstrap`
- Retire the rest from the architecture race:
  - `time_constant_ranked_arbiter`
  - `reverse_leakage_vote_or`
  - `tokenized_uvlo_handoff_gate`
  - `comparatorless_current_probe_bootstrap`

## Decision

- Active champion:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/rc_ranked_packet_gate.cir`
- Kill-ready fallback:
  - `results/concept_evolve/tree/002_dual_bucket_polarity_split_bootstrap`

## Why Other Branches Were Retired

- `time_constant_ranked_arbiter`
  - retained only as a control or ablation family
  - retired from fallback status because it is too close to ordinary source arbitration and does not materially widen the novelty moat
- `reverse_leakage_vote_or`
  - retired because leakage voting looks process-sensitive and architecture-thin
- `tokenized_uvlo_handoff_gate`
  - retired as a standalone architecture because it reads like a support block, not a multi-source cold-start thesis
- `comparatorless_current_probe_bootstrap`
  - retired as a separate bridge because it only survives as an implementation detail inside the packet-scout family unless it later proves a clear control-energy advantage

## Next Experiment Gate

- Run the frozen H1 matrix on the RC-ranked champion against both baselines first.
- Keep mixed-polarity and `1:20` impedance asymmetry in the primary 24-case budget.
- Open the fallback only if:
  - the champion fails its kill rule, or
  - mixed-polarity startup remains the only regime with unresolved separation from the closest prior-art family.
