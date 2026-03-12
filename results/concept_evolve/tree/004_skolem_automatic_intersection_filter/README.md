# Skolem Automatic Intersection Filter

## Topic context
Skolem-Mahler-Lech gives arithmetic-progression structure for zero sets of linear recurrences, and automatic Beatty presentations turn membership into finite-state constraints. This card combines them into a rejection filter: many candidate LRS templates should fail because the required Beatty-intersection pattern cannot simultaneously look progression-like and automatic in the right coordinates.

This concept targets the problem of characterizing real numbers r for which the Beatty sequence floor(n*r) contains a homogeneous linearly recurrent subsequence.

## Mathematical sketch
Given an LRS u_k and Beatty set B_r, study S = {k : u_k in B_r}. Use algebraic relations among shifted tuples of the recurrence to derive SML-type arithmetic constraints, then intersect those constraints with automata or numeration constraints defining B_r or y = floor(r*n). The heuristic prediction is that infinite S must lie in a very small family of progression-compatible selector languages.

## Cross-domain analogies
- Sieve arithmetic progressions against DFA traces.
- Cross p-adic regularity with finite-state regularity.
- Treat a recurrence witness as an orbit-intersection problem with two incompatible symmetries.

## Novel move
Skolem-Mahler-Lech is used here as a pre-filter for Beatty subsequence existence, not only as a theorem about zeros of a known recurrence.

## Why this is not just a reimplementation
Existing SML papers analyze recurrence zero sets or affine-orbit intersections in isolation. This proposal couples them to automatic Beatty membership and subsequence search.

## Implementation backlog
1. Translate the mathematical sketch into a concrete prototype: For fixed LRS families, derive modular and p-adic necessary conditions on membership in B_r. Intersect those conditions with Beatty automata or Ostrowski recognizers and discard templates whose admissible k-set collapses to a finite or inconsistent progression pattern.
2. Run the first experiment: Start with Fibonacci, Pell, and Tribonacci values against B_r for r in {phi, sqrt(2), plastic constant, random algebraic}. Measure how quickly modular filters eliminate candidate selectors before any exhaustive search.
3. Compare the observed patterns against the closest prior art and record where the new bridge adds information.

## Literature anchors
- A Generalised Skolem-Mahler-Lech Theorem for Affine Varieties (a14e28b77b148c3f351936f109820a3a88950037, 2005, venue not specified in the local snapshot): Extends SML to affine-orbit intersection language useful for subsequence filtering.
- A Skolem-Mahler-Lech theorem in positive characteristic and finite automata (6b07357c75ab7826e36cf9e2758dc491cee20211, 2005, venue not specified in the local snapshot): Introduces the finite-automata viewpoint on recurrence-zero patterns.
- Beatty Sequences for a Quadratic Irrational: Decidability and Applications (74492951ce0e23319ffde058fc107cefc4488d0e, 2024, arXiv.org): Supplies a finite-state Beatty-membership interface in the quadratic regime.
- Ostrowski-automatic sequences: Theory and applications (60d51405e92dd39f0836d04dbbe88f5904b094b3, 2021, Theoretical Computer Science): Provides automatic-sequence tooling for the Beatty side of the filter.

## Current decision
- Alignment: `H1`
- Promotion status: promoted as the champion obstruction layer.
- Evidence links: `results/core/h1_modular_shadow_memo.md`, `results/baseline/modular_shadow_smoke.json`, `results/literature/literature_graph_memo.md`
- Current experiment status: the modular-shadow implementation exists in `special_numbers/diagnostics.py`, but the concept-specific Beatty-membership sieve is still pending.
- Next experiment: use Fibonacci and Pell value sets against `r in {phi, sqrt(2), plastic}` and record admissible `k`-shadows modulo `2,3,5,7,11,25`.
