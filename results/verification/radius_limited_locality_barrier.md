# Radius-Limited Locality Barrier

This artifact upgrades the old H1 negative result into a certified statement over an explicit local rule family.

## Checked Objects

- Seed: `results/frontier/order_668_64m/seed_sequences.json`
- Machine-checkable checker: `scripts/check_radius_limited_locality_barrier.py`
- Checker output: `results/verification/radius_limited_locality_barrier.json`
- Retained composite library: `results/analysis/composite_packet_retained_library.json`

## Single-Actuator Barrier

The checker exhaustively verifies that **no single actuator** in the explicit class below improves the canonical frontier objective `13 / 2880 / 512`:

- all `334` one-packet moves
- all `55,611` unordered two-packet moves
- all `9` retained composite actions

Observed best cases:

- one-packet best: neutral `s[83]`, still `13 / 2880 / 512`
- two-packet best: neutral `['s[84]', 's[166]']`, still `13 / 2880 / 512`
- retained-composite best: the same neutral pair, still `13 / 2880 / 512`

So the canonical seed is certified frozen for every depth-`1` single-actuator local rule in that actuator class.

## First Certified Counterexample Rule Class

The barrier breaks at radius `1`, depth `2`, when the local rule class is widened from single actuators to retained causal-cone hyperedges.

- Rule class: two-step causal-cone hyperedges over the retained overlap graph
- Locality contract:
  - both actions must come from the retained low-splash library
  - the two actions must overlap on changed lags
  - the union of their changed-lag supports must stay inside the retained local envelope (`<= 25` lags)

The first certified counterexample on the canonical seed is:

- edge `[3, 7]`
- action sequence:
  - `['q[53]', 'q[136]']`
  - `['q[29]', 's[29]', 'q[114]', 's[114]']`
- end state:
  - state id `53`
  - packet mask `['q[29]', 'q[53]', 'q[114]', 'q[136]', 's[29]', 's[114]']`
  - objective `13 / 2744 / 480`

That is a strict lexicographic improvement over the canonical frontier seed.

## Interpretation

The certified statement is therefore:

- depth-`1` local rules over the explicit actuator class are blocked
- the first verified escape appears only at depth `2` in a radius-`1` retained hypergraph rule class

This is materially different from the old H1 result. The repo now has an explicit local-rule barrier together with the first certified counterexample class that crosses it.
