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
