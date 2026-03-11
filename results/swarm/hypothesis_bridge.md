# Bridge Hypotheses

`results/swarm/director_brief.md` was not present in the workspace, and no ConceptEvolve artifacts were found. To avoid a derivative pass on the standard Sturmian/continued-fraction route, each candidate below pivots to a different outside toolkit.

## 1. Pisot Self-Matching Beyond Quadratic Units
- Title: Pisot Self-Matching Beyond Quadratic Units
- Closest prior art: Masakova-Pelantova, "Self-matching properties of Beatty sequences" (quadratic units), plus substitution/cut-and-project work on linearly repetitive sets.
- Why it is different: The obvious derivative route is to stay inside Sturmian words and bounded partial quotients. This hypothesis pivots to beta-numeration and Pisot spectral decay: the claim is not just that the coding of `floor(n r)` is regular, but that higher-degree Pisot renormalization can force exact homogeneous linear recurrences in sparse value subsequences.
- Falsifiable prediction: If `r > 1` is Pisot, then there exists an integer linear recurrence `U_k` and a residue class `a mod m` such that `floor(U_{m k + a} r)` is itself a homogeneous linear recurrence sequence for all large `k`. For non-Pisot algebraic `r`, the same companion-matrix construction fails infinitely often.
- Required experiments: Generate low-degree Pisot, Salem, and non-Pisot algebraic test cases; build canonical recurrence index sequences from convergents or companion matrices; test exact identities of the form `floor(U_k r) = V_k + c`; recover characteristic polynomials; compare success rates across the three algebraic classes.

## 2. Ostrowski-Automaton Classification of Hidden Recurrences
- Title: Ostrowski-Automaton Classification of Hidden Recurrences
- Closest prior art: Schaeffer-Shallit-Zorcic, "Beatty Sequences for a Quadratic Irrational: Decidability and Applications" (2024), and Ostrowski-automatic sequence theory.
- Why it is different: There is overlap with the standard quadratic/Sturmian toolbox, but the pivot is algorithmic rather than combinatorial. Instead of polishing factor-complexity or central-set arguments, use synchronization and Walnut-style logic to quantify over index sets and recurrence coefficients, turning existence of an infinite recurrence subsequence into a model-checking problem.
- Falsifiable prediction: For quadratic irrational `r` and fixed order `d`, every infinite order-`d` recurrence subsequence of `floor(n r)` comes from one of finitely many Ostrowski-automatic index schemas determined by the continued-fraction period; Walnut should either exhibit those schemas or certify their absence for bounded `d`. The same pipeline should fail to close cubic cases because synchronization disappears.
- Required experiments: Encode the Beatty relation and order-`d` recurrence constraints in Walnut; sweep `d = 1..4` for representative quadratic irrationals; compare discovered schemas with convergent-denominator and period-`m` subsamples; rerun on cubic irrationals to see whether the decidable/quadratic boundary is real or only an artifact of the search.

## 3. Sparse Hankel-Rank Barrier for Generic Slopes
- Title: Sparse Hankel-Rank Barrier for Generic Slopes
- Closest prior art: Prony/Hankel low-rank methods for exact recurrence detection and sparse interpolation, rather than Beatty-specific papers.
- Why it is different: This is a full cross-domain pivot away from symbolic dynamics. It treats a Beatty sequence as a quantized line and asks whether any structured thinning can create exact low Hankel rank. A positive answer means a hidden linear system is present; a negative answer becomes a rank-rigidity obstruction instead of a continued-fraction argument.
- Falsifiable prediction: For rational and Pisot-type `r`, there exist low-description-complexity index families (for example, linear-recursive index sets) whose sampled Hankel matrices have uniformly bounded exact rank. For non-Pisot algebraic `r` and for generic transcendental `r`, the minimum exact Hankel rank over the same family classes grows with sample length, so long apparent recurrences are only convergent-driven near misses.
- Required experiments: Search over arithmetic, convergent-based, morphic, and linear-recursive index families; compute exact Hankel ranks of `floor(n_k r)` over `Z` and modulo several primes; recover candidate recurrences via Berlekamp-Massey or LLL; measure rank growth separately for rational, quadratic, higher-degree Pisot, Salem, and transcendental slopes.
