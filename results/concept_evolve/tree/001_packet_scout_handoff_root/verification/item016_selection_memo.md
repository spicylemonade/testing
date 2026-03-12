# Item 016 Selection Memo

Date: 2026-03-12
Scope: one-champion and one-fallback freeze for `H1_multisource_cold_start`
Status: PASS with narrowed architecture set

## Execution Note

- Attempted delegated role pass:
  - `research_director`
  - `hypothesis_scout`
  - `novelty_checker`
  - `falsifier`
  - `integrator`
- Attempted method:
  - parallel `codex exec` child sessions from the repo root, each instructed to read the same frozen H1 evidence and write one role-local note
- Observed blocker:
  - all five child sessions hit the same responses-proxy failure seen earlier in the run:
    - `stream disconnected before completion`
  - no role-local note files were written
- Parent fallback used here:
  - preserve the required role structure below, but reconstruct each section directly from the same frozen inputs:
    - `results/concept_evolve/bridge_candidates.json`
    - `results/concept_evolve/concept_delta.json`
    - `results/concept_evolve/recurrent_state.json`
    - `results/concept_evolve/integrator_selection.md`
    - `verification/claim_matrix.md`
    - `verification/item011_signoff.md`

## Research Director

- Selected champion:
  - `packet_scout_handoff_root::variant_01_rc_ranked_packet_gate`
- Selected fallback:
  - `dual_bucket_polarity_split_bootstrap`
- Retired branches:
  - `time_constant_ranked_arbiter` as a benchmark/control line only
  - `tokenized_uvlo_handoff_gate` as a support block only
  - `reverse_leakage_vote_or` as a retired standalone bridge
  - `comparatorless_current_probe_bootstrap` as a retired standalone bridge
- Why this is the correct freeze:
  - the RC-ranked packet gate is the only implemented branch that still matches the claim boundary in `claim_matrix.md`: helper-free pre-arbitration source scouting under heterogeneous weak sources
  - the dual-bucket branch is the only surviving fallback that opens a materially different mixed-polarity startup regime instead of collapsing into ordinary arbitration

## Hypothesis Scout

- Champion:
  - keep `packet_scout_handoff_root` active because it is already netlisted and directly maps to the strongest surviving bridge in `bridge_candidates.json`
- Fallback:
  - keep `dual_bucket_polarity_split_bootstrap` because mixed-polarity startup remains the only nearby route that could widen the novelty moat if the champion underperforms
- Why `003` is not the fallback:
  - `time_constant_ranked_arbiter` remains useful, but only as the cleanest low-overhead source-awareness control; it is too close to ordinary RC arbitration to justify fallback status

## Novelty Checker

- Champion novelty boundary:
  - valid only as source-aware startup sequencing before arbitration exists
- Fallback novelty boundary:
  - valid only if polarity-safe startup turns out to be the decisive unresolved failure mode
- Retirements justified:
  - `reverse_leakage_vote_or` is too easy to compress into expected anti-backdrive behavior
  - `comparatorless_current_probe_bootstrap` still lacks evidence that it beats the RC-ranked branch without hidden bias or probe-as-helper behavior
  - `tokenized_uvlo_handoff_gate` reads as a useful control primitive, not a thesis family

## Falsifier

- Main champion kill conditions:
  - if mixed-polarity plus `1:20` impedance cases do not separate the champion from the nonaware baseline on `startup_ok`, `t_handoff`, or `e_backdrive`
  - if the nonaware baseline keeps `e_backdrive` near zero across the main matrix, shrinking H1 to extra logic with slightly better accounting
- Why the fallback is kill-ready:
  - the dual-bucket branch has a fast, explicit failure mode
  - below `50 mV`, bucket leakage and merge overhead should either show a clear polarity-safe startup benefit or kill the branch quickly
- Retired branches:
  - `reverse_leakage_vote_or`
  - `comparatorless_current_probe_bootstrap`
  - both are too vulnerable to hidden sensing overhead and process-sensitive behavior

## Integrator Decision

- Keep exactly one active champion:
  - `packet_scout_handoff_root::variant_01_rc_ranked_packet_gate`
- Keep exactly one kill-ready fallback:
  - `dual_bucket_polarity_split_bootstrap`
- Keep as non-headline controls or support blocks only:
  - `time_constant_ranked_arbiter`
  - `tokenized_uvlo_handoff_gate`
- Retire from the architecture race:
  - `reverse_leakage_vote_or`
  - `comparatorless_current_probe_bootstrap`

## Next Experiment Gate

- Run the frozen primary H1 matrix on the champion with both strong baselines:
  - source voltages `20/50/100/300 mV`
  - ramp rates `0.1/1/10/100 mV/s`
  - impedance ratios `1:1/1:5/1:20`
  - mandatory mixed-polarity cases
- Do not activate the fallback unless one of these is true:
  - the champion fails startup correctness or handoff in mixed-polarity cases
  - the champion shows no meaningful separation from the nonaware baseline on back-drive or handoff
  - the claim narrows so far that only polarity-safe startup remains defensible
