# Concept Delta

Date: 2026-03-12
Focus: `H1_multisource_cold_start`

## Suggestion

- Narrow the active H1 story to helper-free, pre-arbitration source scouting for heterogeneous weak sources.
- Keep one mixed-polarity fallback alive because that is the only nearby branch that could still widen the novelty moat if the main RC-ranked path underperforms.
- Retire branches that lean on leakage sensing or standalone comparatorless current probing unless the benchmark matrix later shows a clear overhead win.

## Implementation

- Ran:
  - `python3 .archivara/concept_evolve.py iterate "Do electrical engineering research and discover something new/interesting. nontrivial and important. maybe you design a new circuit and use ng spice or something"`
- Accepted the generated machine-readable state files:
  - `results/concept_evolve/bridge_candidates.json`
  - `results/concept_evolve/concept_delta.json`
  - `results/concept_evolve/recurrent_state.json`
- Bound the iterate output to the already validated novelty screen and benchmark gate:
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/claim_matrix.md`
  - `results/concept_evolve/tree/001_packet_scout_handoff_root/verification/item011_signoff.md`
  - `results/concept_evolve/integrator_selection.md`

## Result

- Active champion remains:
  - `packet_scout_handoff_root::variant_01_rc_ranked_packet_gate`
- Kill-ready fallback remains:
  - `dual_bucket_polarity_split_bootstrap`
- Hold only as support or controls:
  - `time_constant_ranked_arbiter`
  - `tokenized_uvlo_handoff_gate`
- Retired as standalone bridges:
  - `reverse_leakage_vote_or`
  - `comparatorless_current_probe_bootstrap`
- Next experiment priority from the iterate pass:
  - run the frozen H1 matrix on the RC-ranked champion against both baselines
  - stress mixed polarity and `1:20` impedance cases first
  - open the dual-bucket fallback only if the champion fails or the polarity-safe startup gap remains real

## Novelty Delta

- Stronger than before:
  - the claim boundary is now tied to one concrete mechanism and one concrete fallback instead of six loosely related bridge candidates
  - weak anti-backdrive and low-confidence sensing branches were explicitly retired instead of being left alive as accidental novelty inflation
- Weaker than before:
  - the probe sub-question still has a parse-error output and the earlier reframe pass produced no reframings
  - the iterate pass itself notes that `results/verification/novelty_report.md`, `benchmark_report.md`, and `citation_audit.md` are still absent, so bridge promotion is structural rather than performance-backed
- Net effect:
  - H1 remains alive, but only as a narrow startup-correctness thesis that can still be killed quickly if the upcoming matrix fails to separate it from the nonaware baseline on `startup_ok`, `t_handoff`, or `e_backdrive`

## DEEPEN Addendum

Date: 2026-03-12
Focus: `H1_confidence_gated_abstention`

### Suggestion

- Stop searching for a better winner-take-all selector.
- Test whether the right startup behavior in near-tie regimes is to abstain from committing until separability clears, then hand off from the same packet-gated scaffold.

### Implementation

- Reconstructed `research_rubric.json` to restore the pre-DEEPEN ledger and add a new `Novelty Deepening` phase.
- Froze the active lane from:
  - `results/swarm/director_brief.md`
  - `results/swarm/hypotheses.json`
  - `results/swarm/tool_plan.md`
- Ran:
  - `python3 .archivara/concept_evolve.py probe "Can a low-energy confidence metric outperform blind packet gating on near-tie weak-source startup cases without hidden helper behavior?"`
- The helper failed cleanly only up to a degraded artifact:
  - `results/concept_evolve/probe_result.json`
  - repeated Archivara responses-proxy disconnects prevented a full concept-worker return

### Result

- The useful surviving probe output is the recovered sub-problem:
  - `What is the minimum-energy source-inference mechanism that still improves helper-free multi-source cold start under mixed polarity and 1:20 impedance asymmetry?`
- That reframes the lane away from `smarter ranking` and toward `confidence-aware refusal to over-infer`.
- The experiment freeze is now:
  - compare `source_blind`, `time_constant_ranked`, and one confidence-gated fallback variant only on near-tie cases
  - keep packet-gating claims bounded until a same-scaffold no-packet control runs under equal accounting

### Novelty Delta

- Stronger than the prior RC-ranked story:
  - the proposed contribution is no longer generic source awareness or mixed-polarity startup, both of which the overlap set already crowds
  - the new hypothesis asks whether analog startup logic should detect non-separability and intentionally defer ranking
- Still fragile:
  - the probe tooling did not return new bridge candidates, so the lane still depends on measured separation rather than concept-worker novelty support
  - if the confidence node only reproduces `source_blind` with extra overhead, the lane dies immediately

## Confidence-Gated Implementation

Date: 2026-03-12
Focus: `variant_04_confidence_gated_abstention`

### Suggestion

- Do not use absolute probe difference as the confidence signal.
- Use a normalized separability score that only turns on after a minimum scout amplitude:
  - `|a_probe - b_probe| / (eps + |a_probe| + |b_probe|)`
- Keep the startup path in the `source_blind` posture until that score integrates past a commit threshold.

### Implementation

- Ran:
  - `python3 .archivara/concept_evolve.py reframe "Do electrical engineering research and discover something new/interesting. nontrivial and important. maybe you design a new circuit and use ng spice or something"`
- The saved `results/concept_evolve/reframings.json` remained empty, so the DEEPEN implementation proceeded from the director brief and probe freeze rather than a useful helper reframe.
- Added:
  - `netlists/champion/packet_scout_handoff/variant_04_confidence_gated_abstention/README.md`
  - `netlists/champion/packet_scout_handoff/variant_04_confidence_gated_abstention/confidence_gated_abstention.cir`
- Extended `packet_scout_blocks.inc` with `confidence_gated_packet_gate`, which:
  - computes a normalized scout-margin ratio after a minimum amplitude floor
  - integrates that ratio on `n_conf`
  - exposes `n_commit`
  - blends from blind packet isolation toward the winning branch only after `n_commit` rises

### Result

- The new deck executes without helper rails under the same shared source, startup, and measurement includes.
- Smoke-test behavior is directionally correct:
  - late-arrival case:
    - `t_commit = 1.02771 s`
    - `t_handoff = 4.73294 s`
    - `source_blind t_handoff = 4.76565 s`
  - near-tie case:
    - `t_commit = none`
    - `conf_final = 0.01659312`
    - `t_handoff = 4.70396 s`, effectively matching `source_blind`
- Interpretation:
  - the variant now behaves like an explicit abstain-to-commit controller instead of a slower hidden copy of the blind path

### Novelty Delta

- Stronger:
  - the mechanism is no longer `better ranking`; it is an analog refusal-to-commit rule tied to normalized separability
  - the design exposes a measurable `t_commit` state, which gives the DEEPEN matrix a new behavioral axis that the prior H1 family did not report
- Still provisional:
  - the current evidence is only smoke-test scale
  - the lane still dies if the near-tie matrix shows no improvement over `source_blind` under equal accounting

## Final Iterate Closure

Date: 2026-03-12
Focus: `H1_confidence_gated_abstention`

### Suggestion

- Stop treating the DEEPEN lane as a search for a universally better selector.
- Use the final iterate pass to lock the concept search onto one bounded research claim:
  - stay blind on static near ties
  - commit only when temporal separability appears

### Implementation

- Ran:
  - `python3 .archivara/concept_evolve.py iterate "Do electrical engineering research and discover something new/interesting. nontrivial and important. maybe you design a new circuit and use ng spice or something"`
- Refreshed the verification boundary before the iterate pass:
  - `results/verification/novelty_report.md`
  - `results/verification/benchmark_report.md`
  - `results/verification/citation_audit.md`
  - `results/verification/verification_summary.md`
- Consumed the generated state files:
  - `results/concept_evolve/bridge_candidates.json`
  - `results/concept_evolve/concept_delta.json`
  - `results/concept_evolve/recurrent_state.json`

### Result

- The iterate pass promoted exactly one bridge:
  - `H1_confidence_gated_abstention`
- It retired five earlier bridge candidates:
  - `packet_scout_handoff_root::variant_01_rc_ranked_packet_gate`
  - `dual_bucket_polarity_split_bootstrap`
  - `tokenized_uvlo_handoff_gate`
  - `reverse_leakage_vote_or`
  - `comparatorless_current_probe_bootstrap`
- The recurrent state now agrees with the DEEPEN verification package:
  - broad architecture novelty is dead
  - the confidence lane survives only with a narrow temporal-separability claim
  - `time_constant_ranked` stays as a benchmark anchor, not a promoted novelty bridge
- The next-step list from `concept_delta.json` is now correctly downstream of the final result:
  - robustness on late-arrival DEEPEN cases
  - bounded parasitic sweeps against `blind_packet_merge`
  - immediate kill if a close abstention-style prior-art overlap is later recovered

### Novelty Delta

- Stronger:
  - the structured concept search now converges on the same claim boundary as the executed evidence pack
  - the project is no longer inflating novelty with alternate selector families that the repo has already killed or crowded out
- Weaker:
  - the surviving claim is explicitly not `best overall`
  - no literature-faithful executed comparator exists yet
  - the literature-gap language must stay scoped to the recovered overlap set
- Net effect:
  - the research contribution is now a bounded operating-regime insight about abstain-to-commit startup control, not a general adaptive multi-input startup architecture
