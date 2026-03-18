# Novelty Report

## Verdict

- Positive novelty claim: `fail`
- Narrow negative-result claim: `pass`

## Supporting evidence

- `H1` was specific enough to test a real novelty claim on the exact `167/80` obstruction, but it lost to the matched direct-search baseline.
- `H2` was specific enough to test a repair-style novelty claim on the published modular seed, but it tied the matched non-CA baseline on the decisive order-`668` attempt.
- The literal `cellar` reading survives only as an untested reserve branch in the form of a pushdown-style prefix filter; it is not validated evidence.

## Unresolved risks

- Reserve branches may still collapse into SAT+CAS or branch-and-bound packaging unless they prove a genuinely different proposal or pruning mechanism.
- The phrase `cellar automata` cannot support a claim by itself; only a formal model and benchmark win could.

## Recommendation

Allow only the following claim:

- the repo tested a cellular-automata research program for Hadamard `668`, and the current implementations failed under matched controls.

Reject any stronger claim of promise, novelty, or proximity to a solution.
