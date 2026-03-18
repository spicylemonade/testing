# Phase 3 H1 Review

Inputs reviewed:

- `results/core/h1_design.md`
- `results/swarm/director_brief.md`
- `results/swarm/hypotheses.json`
- `results/swarm/falsifier.md`
- `results/verification/verification_summary.md`

Required review roles for this checkpoint:

- `research_director`
- `hypothesis_scout`
- `falsifier`
- `integrator`

## Decision

- `H1`: `keep active, blocked at exact gate`
- `H2`: `closed`
- `H3`: `reserve only`

## Why H1 Is Kept

- The design is still the least derivative lane in the current artifact set.
- It is the only lane that compiles naturally to the product-grid witness representation with a no-repair rule.
- The exact verifier blocker prevents the first real keep/kill experiment, so killing `H1` now would be premature.

## H1 Kill Criteria

Kill `H1` immediately if any of the following occur:

1. The candidate representation cannot decode directly to legal `(X,G,R,T)` witnesses.
2. The decoder must repair malformed outputs rather than reject them.
3. Any apparent gain survives `X`-label shuffling at fixed geometry.
4. The family works only in bounded-slope or very low-rational-complexity regimes.
5. Out-of-distribution grids or alphabets destroy the effect once exact evaluation exists.
6. The exact verifier, once found, shows no improvement in verified score distribution.

## H1 Keep Criteria

Keep `H1` active only if all of the following eventually hold:

1. A fixed decoder maps states directly into legal witnesses.
2. Exact integer verification is available.
3. The verified score distribution improves relative to matched non-CA baselines.
4. The signal collapses under label shuffling.
5. The effect survives at least one held-out grid or aspect-ratio condition.

## Lane-Opening Rule

- `H2` opens only if `H1` is killed cleanly or stalls after the first exact-verification gate.
- The current state does **not** satisfy that trigger because the first exact-verification gate has not opened.
- Therefore `H2` remains closed.

## Reserve Rule

- `H3` remains reserve-only.
- It does not open while `H1` is still the champion lane and the verifier gate is unresolved.

## Immediate Next Step

Do not expand to backup lanes. Continue with concept-tree population, novelty differentiation, and lane-gate documentation under the standing verifier blocker.
