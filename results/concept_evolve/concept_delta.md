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
