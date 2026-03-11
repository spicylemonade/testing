# Adversarial Falsifier

There are no recorded swarm hypotheses yet (`results/research_context.md` says `Swarm hypotheses: 0`), so this note attacks the default hypotheses the project is most likely to drift toward.

## Immediate credibility failures

- The current prior-art watchlist is not a serious novelty screen. It is dominated by lexical false positives (`Louisville Seamount Trail`, `A Data Prefetch Mechanism for Accelerating General-Purpose Computation`, `MATERIAL BEHAVIOR IN MICROFORMING AT ELEVATED TEMPERATURE`, etc.). Any claim of novelty built on `results/literature/prior_art_watchlist.md` can be dismissed immediately.
- `results/literature/prior_art_gap.md` is still blank in the places where the actual differentiating evidence should live. Right now there is no documented proof that the real Beatty/Sturmian/linear-recurrence literature has even been checked.
- The phrase `homogeneous linearly recurrent subsequence` is ambiguous enough to sink the project if it is not fixed up front. The two dangerous readings are:
  - a subsequence that satisfies a homogeneous linear recurrence with constant coefficients;
  - a symbolic-dynamics / combinatorics-on-words notion of linear recurrence.
  Sliding between these two notions will make every theorem vulnerable to the charge that it solves the wrong problem.

## Easiest ways likely hypotheses fail

### 1. `Quadratic irrationals are the special numbers`

- This dies instantly if rationals are not handled first. If `r = a/b` is rational, then along the index progression `n = kb` one has `floor(kb*r) = ka`, an arithmetic subsequence. Arithmetic progressions satisfy a homogeneous order-2 recurrence, so every rational `r` is already a positive case.
- If the argument passes through codings of rotations / Sturmian words, then `quadratic` is a suspicious invariant. The natural invariant in that literature is usually continued-fraction behavior (bounded partial quotients, eventually periodic continued fractions, etc.), not algebraic degree by itself.
- So a quadratic-only claim is exposed from both sides:
  - too weak / derivative if it is really a Sturmian-mechanical-word argument in disguise;
  - too strong if it is meant as a statement about integer-valued constant-recursive subsequences rather than symbolic codings.

### 2. `Bounded partial quotients characterize the good irrationals`

- This is the most obvious symbolic-dynamics route, which makes it the easiest one to accuse of rehashing prior art. Repetitions, powers, and recurrence properties of Sturmian words are already deeply tied to the continued fraction of the slope.
- If the proposed subsequences come from arithmetic progressions, gap codings, or other standard codings of `floor(n*r)`, then this is very likely already living inside the Sturmian / circle-map / S-adic literature.
- If the subsequence indices are allowed to be arbitrary, bounded partial quotients may also be the wrong invariant: sparse extraction can create misleadingly low-complexity behavior without giving a genuine structural characterization.

### 3. `The first-difference word solves the original problem`

- For irrational `r`, the difference sequence `floor((n+1)*r) - floor(n*r)` is a finite-alphabet mechanical word, often exactly in Sturmian territory.
- But a linearly recurrent word in the symbolic sense is not the same thing as an integer subsequence of `floor(n*r)` satisfying a homogeneous constant-coefficient recurrence.
- Any argument that proves recurrence of the gap word and then claims to have solved the subsequence problem will be attacked as a category error.

### 4. `Computation found many low-order recurrences, so the theorem is probably true`

- This is not serious evidence unless the index-selection rule is fixed before searching.
- Without a density or definability restriction on the chosen indices, one can post-select sparse subsequences that mimic familiar recurrences for a long initial window.
- Continued-fraction convergents give especially dangerous false positives: near-equalities `q*r ~ p` can produce long finite stretches that look arithmetic or Beatty-like without giving an infinite recurrence subsequence.

### 5. `The problem is nontrivial even for arbitrary subsequences`

- This may simply be false unless `subsequence` is constrained. If completely arbitrary extractions are allowed, the problem risks becoming too permissive to support an interesting characterization.
- At minimum, any strong claim should explain why the result does not collapse under one of these weakened notions:
  - arbitrary increasing indices;
  - arithmetic-progression indices;
  - positive-density indices;
  - automatic / Ostrowski-definable indices.

## Missing controls that would invalidate weak claims

### Definition controls

- Specify the domain of `r` (`r > 0`? `r > 1`? all real `r`?).
- Specify what counts as a subsequence: arbitrary extraction, contiguous block, arithmetic progression, positive-density set, definable set.
- Specify what `homogeneous linear recurrence` means:
  - constant coefficients or variable coefficients;
  - coefficients in `Z`, `Q`, `R`, or `C`;
  - fixed order or order depending on `r`;
  - degenerate recurrences allowed or excluded.

### Baseline families

- Rationals: integers, nonintegral rationals, `0 < r < 1`, and negative rationals if the domain allows them.
- Canonical bounded-type irrationals: `(1 + sqrt(5))/2`, `sqrt(2)`.
- Canonical unbounded-type irrationals: `e`, Liouville-type examples, or generic random continued fractions.
- Algebraic but nonquadratic irrationals: needed to separate `quadratic` from `bounded-type` narratives.
- Inhomogeneous comparison family `floor(n*r + beta)`: needed to show the argument is really about the zero intercept and not about generic mechanical-word structure.

### Index-set controls

- Same slope, different index classes: if the theorem only works for one highly tuned extraction rule, it is not a characterization of `r` in any robust sense.
- Positive-density vs zero-density extractions: if the proof only finds zero-density subsequences, expect accusations that the property is too weak to be mathematically meaningful.

## Benchmark traps

- Rational-triviality trap: forgetting that rational `r` already give arithmetic subsequences.
- Sparse-subsequence trap: proving existence by a hand-picked zero-density extraction and then overselling the statement.
- Prefix-fitting trap: mistaking long finite agreement for an infinite recurrence law.
- Word/value trap: proving a statement about codings of rotations instead of about the integer sequence itself.
- Set/sequence trap: importing results about the Beatty set `{floor(n*r) : n >= 1}` when the problem is ordered and subsequential.
- Search-query trap: using the current keyword-overlap watchlist as if it were a relevant literature map.

## Novelty illusions most likely to get called out

- `This is new because it mentions linearly recurrent subsequences of Beatty sequences.`
  - Not enough. Beatty sequences, mechanical words, Sturmian words, repetitions, powers, and S-adic recurrence have been heavily mined already.
- `Quadratic irrationals are new because Beatty decidability is recent.`
  - Weak. Schaeffer, Shallit, and Zorcic (2024) already show synchronized / decidable structure for quadratic-field Beatty sequences `floor(n*alpha + beta)`.
- `The floor function makes this fundamentally different from Sturmian work.`
  - Weak. The floor-function viewpoint is already central to Beatty sequences, codings of rotations, Ostrowski numeration, and generalized-polynomial work.
- `Low complexity implies recurrence, so we are done.`
  - Weak and possibly wrong for the integer-valued problem. Symbolic low complexity does not automatically produce a homogeneous constant-coefficient recurrence for subsequence values.

## Literature branches that would invalidate weak claims

These are the branches missing from the current watchlist that should be treated as default prior art until ruled out.

- Beatty sequences and their variants:
  - classical homogeneous / inhomogeneous Beatty theory;
  - complementary Beatty sequences;
  - iterated Beatty sequences and decompositions.
- Sturmian / mechanical words and codings of irrational rotations:
  - powers, repetitions, critical exponent, initial powers;
  - dependence on continued fractions and bounded partial quotients.
- Linearly recurrent subshifts and S-adic structure:
  - Durand's characterization of linearly recurrent subshifts;
  - any circle-map or Sturmian specialization of that framework.
- Quadratic-Ostrowski automata / decidability:
  - Schaeffer, Shallit, Zorcic, `Beatty Sequences for a Quadratic Irrational: Decidability and Applications` (2024).
- Generalized polynomials / bracket words:
  - Adamczewski and Konieczny, `Bracket words: a generalisation of Sturmian words arising from generalised polynomials` (2022).
- Repetition structure in Sturmian words:
  - Damanik-Lenz on powers / index;
  - Justin-Pirillo on fractional powers;
  - Berthe-Holton-Zamboni on initial powers;
  - Peltomaki's 2015 reproof via Diophantine approximation.
- Recent recurrence / balancedness work:
  - linearly recurrent and factor-balanced Sturmian / Arnoux-Rauzy directions, including 2026 work tying bounded weak partial quotients to recurrence-adjacent regularity.
- Linear recurrence sequence theory itself:
  - Skolem-Mahler-Lech and standard structure theory are the baseline for what a homogeneous constant-recursive claim must even mean.

## Minimum burden of proof before making any claim

- Lock the definition of `subsequence` and `homogeneous linear recurrence`.
- Separate symbolic statements from arithmetic constant-recursive statements.
- Prove the rational cases cleanly before discussing any irrational classification.
- Show why the argument is not already implied by known Beatty / Sturmian / S-adic / generalized-polynomial results.
- If the claim is about `quadratic` or `bounded-type` slopes, test it against both families explicitly instead of assuming the same invariant controls both problems.

Until those checks are passed, the easiest adversarial verdict is: the claim is either trivial (rationals), ill-posed (ambiguous recurrence notion / subsequence notion), or already sitting in the Beatty-Sturmian literature under a slightly different phrasing.
