# Experiment Readout

Prepared from the deterministic outputs in [`results/experiments/h1_control_sweep.json`](/home/archivara/work/repo/results/experiments/h1_control_sweep.json), [`results/experiments/h1_target_sweep.json`](/home/archivara/work/repo/results/experiments/h1_target_sweep.json), [`results/experiments/h2_ladder.json`](/home/archivara/work/repo/results/experiments/h2_ladder.json), and [`results/experiments/h2_seed_attempt.json`](/home/archivara/work/repo/results/experiments/h2_seed_attempt.json).

## H1 control sweep

- The move-matched `direct_greedy` baseline beat `parallel_gain_ca` on the solved `4 x 79` control.
- Exact-hit rate:
  - `direct_greedy`: `0 / 16 = 0.0`
  - `parallel_gain_ca`: `0 / 16 = 0.0`
- Closest-target distance:
  - `direct_greedy`: min `24`, median `43`, mean `41.5`
  - `parallel_gain_ca`: min `32`, median `47`, mean `48.375`
- Stratified fairness check:
  - on `perturbed_solution` seeds, `direct_greedy` mean best distance was `36.5` versus `41.5`,
  - on `random_weight` seeds, `direct_greedy` mean best distance was `46.5` versus `55.25`.
- Reachability:
  - `direct_greedy` visited more unique dihedral orbits on median (`13` vs `4`) even though both methods used the same phase move cap.
- Negative controls:
  - `random_rule_ca` and `random_walk` explored more states but were still worse on the primary metric, so broad reachability alone did not rescue the CA branch.
- Decision effect: `H1` already fails its strongest positive-control gate on the solved template.

## H1 target sweep

- Neither method found an exact `167/80` witness.
- The fairness-corrected rerun removed the earlier apparent CA edge: `direct_greedy` beat `parallel_gain_ca` on both seed families.
- Closest-target distance:
  - `direct_greedy`: min `124`, median `151`, mean `147.917`
  - `parallel_gain_ca`: min `146`, median `187`, mean `188.5`
- Stratified fairness check:
  - on `modular_projection` seeds, `direct_greedy` mean best distance was `145.5` versus `203.25`,
  - on `random_weight` seeds, `direct_greedy` mean best distance was `149.125` versus `181.125`.
- Reachability:
  - `direct_greedy` again visited more unique dihedral orbits on median (`23.5` vs `7.5`).
- Negative controls:
  - `random_rule_ca` and `random_walk` were substantially worse than both serious methods.
- Decision effect: the exact-167 CA branch is a clean no-go under the registered rule set.

## H2 lift ladder

- The repaired structured `n = 9` ladder no longer kills `H2` outright, but it also does not support a positive claim.
- Goal-hit rate:
  - `parallel_gain_ca`: `2 / 3`
  - `direct_greedy`: `1 / 3`
  - `random_rule_ca`: `3 / 3`
  - `random_walk`: `2 / 3`
- Best `l1_defect`:
  - `parallel_gain_ca`: median `0`, mean `2.667`
  - `direct_greedy`: median `8`, mean `10.667`
- Start-level split:
  - both serious methods solved `qflip_mod_sparse_idx6`,
  - only `parallel_gain_ca` solved `sflip_mod_dense_idx8`,
  - neither serious method solved `sflip_mod_sparse_idx2`.
- Decision effect: this ladder is a weak discriminator. It shows that the CA can solve some tiny structured starts, but random controls also solve most of them, so the ladder cannot justify a broader `H2` claim by itself.

## H2 668 seed attempt

- Start state: deterministic `s[41]` flip of the published seed, degrading the published modulus from `64` to `16`.
- `parallel_gain_ca` and `direct_greedy` tied exactly on the actual order-668 attempt:
  - best `two_adic_modulus = 16`
  - best `l1_defect = 2944`
  - best `defect_count = 25`
  - best `max_defect_magnitude = 496`
  - accepted moves `= 48`
- Negative controls were worse:
  - `random_rule_ca` and `random_walk` both stalled at `l1_defect = 3200` with `max_defect_magnitude = 528`.
- Decision effect: the CA did not restore, lift, or improve the published seed beyond the matched non-CA baseline on the real 668 task.

## Stop / go call

- `H1`: stop. The CA lost to matched direct search on both the solved control and the exact `167/80` target sweep.
- `H2`: stop. The small ladder is only a weak sanity check, and the actual 668 seed attempt shows no CA advantage over the matched baseline.
- Overall: the current cellular-automata program is a no-go under the registered gates. Any follow-on work would need a materially different state representation or rule-selection mechanism, not a larger budget on the same update rules.
