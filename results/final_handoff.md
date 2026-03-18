# Final Handoff

## Outcome

No verifier-backed certificate with score `<= 1.675` was found in the frozen width-2 corridor program.

The final verified position is:

- `H1_macrocell_substitution` failed by an exact one-seed obstruction.
- `H2_target_direction_abelian` failed because it added no screening value beyond raw arithmetic descriptors.
- The best surviving exact objects are small direct corridor controls around score `2.0`.

## Best Exact Witnesses

- `2 x 4` direct corridor control:
  - score `2.0`
  - `m=7`, `r=5`, `n=8`, `t=2`
  - file: `results/phase4_width4_seed601.json`
- `2 x 6` direct corridor control:
  - score `2.0`
  - `m=13`, `r=7`, `n=12`, `t=2`
  - file: `results/phase4_width6_seed602.json`
- best exploratory `2 x 8` direct corridor control:
  - `29/14 = 2.071428...`
  - `m=20`, `r=9`, `n=16`, `t=2`
  - file: `results/phase4_width8_seed501.json`

## Key Artifacts

- literature and novelty context:
  - `sources.bib`
  - `results/literature/literature_snapshot.json`
  - `results/literature/prior_art_gap.md`
- concept search state:
  - `results/concept_evolve/tree/index.json`
  - `results/concept_evolve/bridge_candidates.json`
  - `results/concept_evolve/concept_delta.json`
  - `results/concept_evolve/recurrent_state.json`
- exact H1 failure:
  - `results/phase4_h1_obstruction.json`
  - `results/phase4_h1_frontier.md`
- H2 screen:
  - `results/phase4_h2_screen.json`
  - `results/phase4_h2_screen.md`
- ablations:
  - `results/phase4_ablations.json`
  - `results/phase4_ablations.md`
- verification:
  - `results/verification/benchmark_report.md`
  - `results/verification/verification_summary.md`
  - `results/verification/novelty_report.md`
  - `results/verification/citation_audit.md`
- interpretation:
  - `results/phase5_ca_vs_search_prior.md`
  - `results/phase5_negative_results.md`

## If Work Continues

The next credible step is not another pass on the same frozen CA route. It would require one of:

- leaving the frozen H1 template family so the one-seed obstruction disappears,
- moving beyond the width-2 corridor family,
- or running a broader exact search over different constructible graph grammars rather than repackaging the current corridor controls.
