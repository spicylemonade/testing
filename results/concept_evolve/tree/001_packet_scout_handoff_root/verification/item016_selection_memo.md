# Item 016 Selection Memo

Date: 2026-03-12
Scope: core research synthesis for the active H1 architecture set
Status: PASS with one champion and one kill-ready fallback

## Execution Note

- Attempted delegated `research_director`, `hypothesis_scout`, `novelty_checker`, `falsifier`, and `integrator` child passes via `spawn_agent`.
- Result:
  - the child file-writing pass did not materialize the requested note files before timeout
  - an interrupt redirect also returned only `Interrupted` notifications rather than usable role notes
- Fallback used here:
  - direct parent synthesis over the same frozen evidence pack, preserving the five role outputs below as explicit sections so the architecture gate is documented instead of skipped

## Research Director View

- Active champion:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/netlists/champion/packet_scout_handoff/variant_01_rc_ranked_packet_gate/rc_ranked_packet_gate.cir`
- Kill-ready fallback:
  - `results/concept_evolve/tree/002_dual_bucket_polarity_split_bootstrap`
- Why this fallback is the only one still worth keeping:
  - it is the only remaining branch that opens a materially different failure regime, namely mixed-polarity startup isolation, without collapsing all the way into ordinary RC arbitration or helper-assisted startup
- Next experiment gate:
  - run the bounded H1 startup matrix on the RC-ranked champion against both baselines first
  - activate the dual-bucket fallback only if mixed-polarity cases remain unresolved or the champion fails its source-awareness kill rule

## Hypothesis Scout View

- No branch displaces the current fallback.
- `time_constant_ranked_arbiter` stays useful only as a control because its novelty guard is too close to ordinary RC ranking and benchmark-line arbitration.
- `tokenized_uvlo_handoff_gate` stays useful only as a support block if later adversarial cases expose real UVLO chatter.
- Final ranking remains:
  - champion `variant_01_rc_ranked_packet_gate`
  - fallback `dual_bucket_polarity_split_bootstrap`

## Novelty Checker View

- The RC-ranked champion remains materially different enough only under the narrow wording already frozen in `claim_matrix.md`:
  - helper-free, pre-arbitration source scouting under heterogeneous weak sources
- The dual-bucket fallback remains materially different enough only as a mixed-polarity contingency branch, not as a general multi-input PMU claim.
- Retire now on novelty grounds:
  - `reverse_leakage_vote_or`
  - `comparatorless_current_probe_bootstrap`
- Wording constraint:
  - keep disallowing `first`, `novel`, `best`, `lowest-voltage`, and steady-state efficiency claims until the experiment matrix exists

## Falsifier View

- Fastest kill path for the champion:
  - if the nonaware baseline shows negligible `e_backdrive` and similar `t_handoff` in mixed-polarity plus `1:20` cases, the RC-ranked branch compresses to extra logic with better accounting instead of a publishable new mechanism
- Fastest kill path for the fallback:
  - if bucket leakage or merge overhead dominates below `50 mV`, the dual-bucket branch becomes a slower helper-like reservoir instead of a cleaner startup path
- Branches not worth keeping active:
  - `reverse_leakage_vote_or` because leakage signatures are too process-sensitive
  - `comparatorless_current_probe_bootstrap` because the minimum-energy probe sub-question never produced new evidence and the overhead risk is still high

## Integrator Decision

- Keep exactly one active H1 champion:
  - `variant_01_rc_ranked_packet_gate`
- Keep exactly one kill-ready H1 fallback:
  - `dual_bucket_polarity_split_bootstrap`
- Demote from active architecture status:
  - `time_constant_ranked_arbiter`
    - benchmark and ablation control only
  - `tokenized_uvlo_handoff_gate`
    - support block only if chatter is observed later
- Retire from the active tree:
  - `reverse_leakage_vote_or`
  - `comparatorless_current_probe_bootstrap`

## Net Result

- `item_016` is clear to proceed
- The architecture race is now bounded tightly enough for the startup matrix:
  - one champion
  - one fallback
  - two support-only branches
  - two retired branches
