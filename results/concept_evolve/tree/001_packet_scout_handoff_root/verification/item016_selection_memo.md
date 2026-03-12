# Item 016 Selection Memo

Date: 2026-03-12
Scope: core-research synthesis for `H1_multisource_cold_start`
Status: PASS with one active champion and one kill-ready fallback

## Execution Note

- One parallel `spawn_agent` pass was launched for `research_director`, `hypothesis_scout`, `novelty_checker`, `falsifier`, and `integrator`.
- No role-note files materialized under `results/swarm/` within the observation window.
- Fallback used here:
  - direct parent synthesis over the frozen H1 artifacts, with the role outputs preserved as explicit sections below so the gate is documented instead of skipped.

## Research Director

- Champion:
  - `packet_scout_handoff_root::variant_01_rc_ranked_packet_gate`
- Fallback:
  - `dual_bucket_polarity_split_bootstrap`
- Why:
  - the RC-ranked packet gate is still the only branch that matches the director brief exactly: helper-free pre-arbitration source selection under heterogeneous weak-source conditions
  - the dual-bucket branch is the only remaining backup that can widen the novelty moat if mixed-polarity startup proves to be the real unresolved failure mode
- Budget consequence:
  - do not fund any third headline branch before the RC-ranked matrix and the first mixed-polarity falsifier cases land

## Hypothesis Scout

- No branch displaces the current champion.
- Why `002` beats `003` as fallback:
  - `003_time_constant_ranked_arbiter` is still useful, but it reads too much like ordinary low-overhead RC arbitration to carry the backup story
  - `002_dual_bucket_polarity_split_bootstrap` stays more differentiated when polarity mismatch is central, even though it is riskier on overhead
- Scout conclusion:
  - keep `003` only as a control or ablation line
  - do not reopen `004`, `005`, or `006` as independent architecture candidates

## Novelty Checker

- Active champion novelty boundary:
  - valid only as helper-free source-aware startup sequencing before the main arbiter exists
- Why the fallback survives:
  - `002` remains materially different from the closest self-powered multi-input piezo family only when the claim is narrowed to polarity-safe startup isolation and merge timing
- Branches retired on novelty grounds:
  - `004_reverse_leakage_vote_or`
    - too close to anti-backdrive hygiene around existing OR-ing devices
  - `006_comparatorless_current_probe_bootstrap`
    - too close to a sub-block optimization unless it proves a clear overhead win
- Branches not active:
  - `003_time_constant_ranked_arbiter`
    - strong control line, weak headline novelty
  - `005_tokenized_uvlo_handoff_gate`
    - useful sub-block, not an architecture thesis

## Falsifier

- Fastest kill path for the champion:
  - if the 24-case matrix does not show a clean improvement over both baselines on `startup_ok`, `t_handoff`, or `e_backdrive`, the RC-ranked branch collapses to extra startup logic with equal or worse accounting
- Fastest kill path for the fallback:
  - if bucket leakage or merge overhead dominates below `50 mV`, `002` becomes a helper-like detour rather than a defensible fallback
- Why other branches are not active:
  - `003` is too easy to accuse of being ordinary arbitration
  - `004` depends on fragile leakage signatures
  - `005` risks becoming a hidden control rail
  - `006` already failed to gain new evidence from the focused probe pass

## Integrator

- Keep exactly one active champion:
  - `packet_scout_handoff_root::variant_01_rc_ranked_packet_gate`
- Keep exactly one kill-ready fallback:
  - `dual_bucket_polarity_split_bootstrap`
- Hold as support or control only:
  - `time_constant_ranked_arbiter`
  - `tokenized_uvlo_handoff_gate`
- Retire as standalone branches:
  - `reverse_leakage_vote_or`
  - `comparatorless_current_probe_bootstrap`

## Net Result

- Active champion architecture:
  - `packet_scout_handoff_root::variant_01_rc_ranked_packet_gate`
- Kill-ready fallback:
  - `dual_bucket_polarity_split_bootstrap`
- Retired or downgraded branches:
  - retire `reverse_leakage_vote_or`
  - retire `comparatorless_current_probe_bootstrap`
  - downgrade `time_constant_ranked_arbiter` to control status
  - downgrade `tokenized_uvlo_handoff_gate` to support-block status
- Next gate:
  - run the bounded 24-case champion matrix first
  - only activate the dual-bucket fallback if the champion fails the mixed-polarity or anti-backdrive gate
