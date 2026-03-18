# Phase 2 Baseline Review

Prepared for rubric `item_010` after the fairness-corrected reruns.

## Verdict

`item_010` is satisfied. The baseline packet is complete, the fairness review issues were repaired, and the resulting evidence is a no-go for the current cellular-automata program.

## Evidence that closes the gate

- The matched-budget `H1` control sweep kills the active branch:
  - `direct_greedy` beats `parallel_gain_ca` on the solved `4 x 79` control under the same representation, same neighborhood, same step budget, same accepted-move cap per phase, and same verifier.
  - Key summary: best-distance mean `41.5` for `direct_greedy` versus `48.375` for `parallel_gain_ca`, with median unique orbits `13` versus `4`.
- The matched-budget `H1` target sweep does not rescue the branch:
  - no exact `167/80` witness was found,
  - `direct_greedy` also beats `parallel_gain_ca` on both seed families,
  - key summary: best-distance mean `147.9167` for `direct_greedy` versus `188.5` for `parallel_gain_ca`.
- The registered `H1` kill rule in [`results/analysis/kill_rules.md`](/home/archivara/work/repo/results/analysis/kill_rules.md) is therefore triggered exactly as written.
- The `H2` toy lift ladder is not strong enough to revive the branch:
  - `parallel_gain_ca` solves `2 / 3` starts,
  - `direct_greedy` solves `1 / 3`,
  - but `random_rule_ca` solves `3 / 3` and `random_walk` solves `2 / 3`,
  - so the ladder is a weak discriminator rather than evidence of CA-specific reachability.
- The only decisive `H2` test is the real 668 seed attempt, and there the CA ties the matched baseline exactly:
  - both `parallel_gain_ca` and `direct_greedy` stop at modulus `16`,
  - both have best `l1_defect = 2944`,
  - both have best defect count `25`,
  - both have best max defect magnitude `496`.

## Fairness repairs verified

- `parallel_gain_ca` and `direct_greedy` share the same accepted-move cap per phase (`phase_move_cap = 4`) in both [`hadamard668/h1.py`](/home/archivara/work/repo/hadamard668/h1.py) and [`hadamard668/h2.py`](/home/archivara/work/repo/hadamard668/h2.py).
- Experiment summaries expose seed-family and start-state splits in [`results/experiments/h1_control_sweep.json`](/home/archivara/work/repo/results/experiments/h1_control_sweep.json), [`results/experiments/h1_target_sweep.json`](/home/archivara/work/repo/results/experiments/h1_target_sweep.json), [`results/experiments/h2_ladder.json`](/home/archivara/work/repo/results/experiments/h2_ladder.json), and [`results/experiments/h2_seed_attempt.json`](/home/archivara/work/repo/results/experiments/h2_seed_attempt.json).
- `H2` run records now distinguish literal exact repair from registered goal achievement through `goal_hit` and `goal_hit_step`, as documented in [`results/analysis/verifier_contracts.md`](/home/archivara/work/repo/results/analysis/verifier_contracts.md).
- The structured `n = 9` control artifact now has deterministic provenance and an explicit search-space record in [`results/artifacts/h2_control_structured_n9.json`](/home/archivara/work/repo/results/artifacts/h2_control_structured_n9.json).
- The runner now supports `run-h1`, `run-h2`, and `run-all` in [`hadamard668/experiments.py`](/home/archivara/work/repo/hadamard668/experiments.py), so later phases can respect the `H1 -> H2` promotion gate procedurally as well as substantively.

## Residual risks

- The `H2` evidence base is still small: three toy ladder starts and one degraded 668 start.
- The stop call closes only the current representation and rule family. A materially different reserve branch remains logically possible, but it would need a new design brief and new matched baselines rather than more budget on the present CA rules.

## Decision

- `H1`: retired.
- `H2`: retired.
- `H3` and other reserve concepts: can be discussed as pivots only, not as evidence that the present CA program succeeded.
