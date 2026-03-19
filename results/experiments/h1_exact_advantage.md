# H1 Exact Advantage

## Status

Failed.

## What was attempted

The exact search work in this pass focused on families that would already clear
the score budget if they admitted a forcing wave:

- full `2 x N` ladders with `3` to `5` exact seed atoms;
- full `3 x N` strips with two exact seed atoms;
- full `3 x N` strips with one initial forced vertex;
- reduced-model SAT searches on tiny rectangles and strips.

Observed outcomes:

- `2 x 8`, `k=3` seeds: best exact forced count `4/16`, no hit;
- `2 x 8`, `k=4` seeds: best exact forced count `6/16`, no hit;
- `2 x 12`, `k=4` seeds: best exact forced count `6/24`, no hit;
- `2 x 12`, `k=5` seeds: best exact forced count `6/24`, no hit;
- `3 x 6` with two seeds: best exact forced count `6/18`, no hit;
- `3 x 8` with two seeds: best exact forced count `5/24`, no hit;
- `3 x 10` with two seeds: best exact forced count `4/30`, no hit;
- one-sided local strip activation in widths `2` and `3`: exact strict-improvement
  count `0`; see `results/theory/forcing_traces/local_strip_states/`.

## Why the item fails

The acceptance criterion requires an exact-valid proof-state CA family that
beats Random Local Search, Whole-Witness Mutation, and Decoder-Matched Search on
matched budgets across multiple geometries and a held-out legal alphabet.

No exact-valid promoted family was found in this pass, so:

- there is no positive CA family to benchmark;
- there is no exact score distribution to compare against baselines;
- there is no advantage claim to stress with label shuffling or canonicalization
  randomization.

The failure is therefore substantive, not procedural: the search collapsed
before a baseline-cleared comparison became meaningful.
