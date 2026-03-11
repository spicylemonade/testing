# Negative-Space Hypotheses

`results/literature/gap_frontier.md` is still empty, `results/swarm/director_brief.md` is absent, and I reviewed the current swarm/context artifacts (`results/concept_evolve/reframings.json`, `results/swarm/hypothesis_bridge.md`, `results/swarm/falsifier.md`) before drafting these. To stay out of the over-explored lane, the directions below avoid the usual Beatty/Sturmian/continued-fraction-first playbook and use the arithmetic reading: pick increasing integers `n_k` so that `b_k = floor(n_k r)` satisfies a fixed homogeneous constant-coefficient recurrence.

Families to avoid repeating: first-difference Sturmian arguments, bounded-partial-quotient classification by itself, and untargeted prefix-fitting searches for low-order recurrences.

## 1. Generalized-Polynomial / LRS Intersection Rigidity
- What prior work ignored: Beatty sets are generalized-polynomial objects, but most nearby literature studies symbolic codings rather than exact embedding of an integer linear recurrence sequence inside the Beatty set `B_r = {floor(n r) : n >= 1}`.
- Candidate hypothesis: If `B_r` contains an infinite nondegenerate linear recurrence sequence, then either `r` is rational or the embedding comes from the same sparse generalized-polynomial mechanisms that already produce Fibonacci/Tribonacci-type or Pisot/Salem-type recurrence sets. In particular, irrational positive cases should cluster around algebraic slopes with a shared generalized-polynomial model, not around generic bounded-type irrationals.
- Why this is negative space: it reframes the problem as an intersection-rigidity question between two arithmetic object classes instead of another recurrence-of-words question.
- Fast falsifiable test: use known recurrence families (Fibonacci, Tribonacci, companion-matrix sequences, Salem-type examples) and ask for exact infinite membership in `B_r`; compare against random algebraic and transcendental slopes, not just long finite prefixes.
- Overlap and pivot: this is adjacent to the existing Pisot bridge idea, but the pivot is to classify which external recurrence value sets can sit inside a Beatty set, not to study self-matching of `floor(n r)` itself.
- Angle to avoid: do not repackage bracket-word or central-set arguments about the gap word; the target is exact recurrence-set membership in `B_r`.

## 2. Modular Shadow / p-adic Semilinearity Barrier
- What prior work failed to test: an exact constant-coefficient recurrence should leave strong periodic signatures modulo `p^m` and in its zero relations, but Beatty experiments usually search in the reals before checking whether any multi-modulus shadow exists.
- Candidate hypothesis: For any fixed recurrence order and coefficient profile, an infinite subsequence `floor(n_k r)` satisfying that recurrence forces the selector `n_k` to have eventually semilinear shadows modulo many primes. Generic irrational Beatty sets will not support those shadows, so once the selector class is fixed in advance (arithmetic, automatic, recurrence-generated, or positive-density), rational slopes should be the only robust positives; irrational survivors, if any, should be exceptional zero-density constructions.
- Why this is negative space: it turns Skolem-Mahler-Lech style rigidity into a front-end obstruction rather than background theory.
- Fast falsifiable test: predeclare selector families, reduce candidate subsequences modulo many primes, and check whether the same recurrence profile produces consistent eventual periodicity across moduli; if the modular shadow disappears, drop the direction.
- Overlap and pivot: this touches standard linear-recurrence theory, but the pivot is to use modular/p-adic shadows to kill false positives before any symbolic or Diophantine polishing.
- Angle to avoid: do not trust a single modulus, floating-point fits, or post-selected sparse indices.

## 3. Sparse Rigidity Frontier for Structured Selectors
- What prior work could not scale: standard Beatty/Sturmian methods handle consecutive terms and some arithmetic progressions, but they do not directly test whether sparse structured selectors can force the hidden carry term `r n_k - floor(n_k r)` into the bounded regime needed by an exact recurrence.
- Candidate hypothesis: If `b_k = floor(n_k r)` is a nondegenerate linear recurrence, then the fractional parts `{n_k r}` must behave like a rigidity sequence for rotation by `r`, concentrating near finitely many phases determined by the dominant roots. For almost every irrational `r`, and for standard fast-growth selectors (polynomial, lacunary, or non-Pisot linear-recursive selectors), sparse equidistribution blocks this. The only plausible irrational survivors should come from selectors with built-in Pisot-type rigidity.
- Why this is negative space: it attacks the carry term directly instead of translating everything into word complexity.
- Fast falsifiable test: compare phase concentration and exact recurrence failure rates for arithmetic, polynomial, Fibonacci/Tribonacci, lacunary, and random linear-recursive selectors across rational, quadratic, higher-degree Pisot, Salem, and transcendental slopes.
- Overlap and pivot: this is near the ergodic/geometric reframings in `results/concept_evolve/reframings.json`, but the pivot is a concrete rigidity criterion for selector families rather than a generic discussion of rotations or quasicrystals.
- Angle to avoid: do not slide back to continued-fraction folklore or convergent-denominator near-misses unless the selector is proved to be a genuine rigidity sequence.
