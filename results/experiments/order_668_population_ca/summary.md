# Population CA Summary

Self-stabilizing population CA over control-trained orbit representatives.

## Setup

- Rule table trained on non-frontier controls only.
- RNG seeds: `[11, 13, 17, 19, 23]`.
- Equal executed restart coverage: `5` runs per state for both coupled and zero-coupling population methods.
- Population size `64`, coupling `1.6`, threshold `0.42`, temperature `1.2`, memory mix `0.55`, max rounds `6`.

## Outcomes

- `canonical_frontier`: population median `13/2744/480`, zero_coupling median `13/2744/480`, raw local `13/2880/512`, scorer_only `13/2880/512`, population contractions `3/5`.
- `barrier_ladder_01`: population median `13/2880/512`, zero_coupling median `13/2880/512`, raw local `14/2812/496`, scorer_only `14/2812/496`, population contractions `3/5`.
- `barrier_ladder_02`: population median `13/2744/480`, zero_coupling median `13/2744/480`, raw local `14/2820/496`, scorer_only `14/2820/496`, population contractions `3/5`.
- `barrier_ladder_03`: population median `15/2408/416`, zero_coupling median `15/2408/416`, raw local `15/2408/416`, scorer_only `15/2408/416`, population contractions `1/5`.
- `barrier_ladder_04`: population median `13/2744/480`, zero_coupling median `13/2744/480`, raw local `15/2408/416`, scorer_only `15/2408/416`, population contractions `3/5`.
- `barrier_ladder_05`: population median `15/2408/416`, zero_coupling median `15/2408/416`, raw local `15/2544/448`, scorer_only `15/2544/448`, population contractions `3/5`.

## Verdict

- The item fails honestly: canonical success = `False` and perturbation-suite wins = `0` of `5`, so the coupled population never separates from the zero-coupling ablation strongly enough to support a self-stabilization claim.
