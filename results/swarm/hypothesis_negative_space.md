# Hypothesis Negative Space

## Context Check
- Read `results/research_context.md`, `results/literature/prior_art_gap.md`, and `results/literature/gap_frontier.md`.
- `results/swarm/director_brief.md` is not present in this repo.
- No ConceptEvolve artifacts were found in this repo.
- The repo-local literature snapshot is low-signal for this task because the seed query drifted away from arithmetic Kakeya, so the guardrails below come from a narrow external check rather than the generated watchlist.
- External boundary to respect: current public automated work still frames arithmetic Kakeya through entropy and sum-difference exponents, and Tao's 2025 bounded-many-slopes follow-up suggests that squeezing a bounded slope tuple harder is asymptotically pulled back toward exponent `2`. Treat that basin as explored.

## Do Not Repeat
- Static bounded-slope tuning or "just optimize `X`" with a fixed tiny slope alphabet.
- Another entropy-only or sum-difference inequality pass with no verifier-local mechanism.
- Whole-graph mutation or brute-force SAT on tiny instances with no reusable local generator.
- Euclidean Kakeya intuition with no exact mapping to forcing operations 1 to 3.

## Direction 1: Slope-Bloom Spacetime Automata
**Gap attacked.** Prior work has spent real effort on fixed slope sets and fixed inequality templates. The negative space is a local generator whose rule table stays small while the *realized* slope set grows with scale.

**CA formulation.**
- Use a 1D or 2D radius-1 CA with state like `(phase, label, carry)`.
- Interpret time as an extra constructibility dimension.
- Let local collisions emit edge labels for the next layer, so the induced `f_i` dictionaries are generated rather than hand-written.

**Testable hypothesis.** There exists a finite rule with small alphabet but unbounded effective slope complexity `|X_T|` as the automaton is unrolled for `T` steps, and the score surrogate drops because the rule reuses a short description to realize many labels.

**First experiment.**
- Search reversible or second-order rules on strips and small tori.
- Unroll `L x T` spacetime into a constructible graph.
- Measure:
  - effective `|X_T|`,
  - rational complexity of realized labels,
  - greedy forcing yield,
  - score surrogate `(m+r)/(n-t)`.

**Strongest failure mode.** The automaton falls into a short periodic orbit, so the realized slope complexity stays bounded and the whole direction collapses back into the bounded-slope regime.

**Angle to avoid.** Do not keep a tiny fixed slope alphabet and call the time evolution "cellular automata." That is only a relabeling of the already-explored bounded-slope basin.

## Direction 2: Abelian Chip-Firing Forcing Waves
**Gap attacked.** Forcing rule 3 gives arbitrary `Z`-linear closure, but current arithmetic Kakeya work is not organized around abelian-network or odometer dynamics that might compress the seed term `r`.

**CA formulation.**
- Give each vertex a two-component integer charge.
- Treat operation 1 as a local signed transport rule.
- Treat topplings as chip-firing events that isolate `(a,-a)` residues off the already-solved set.
- Use the odometer as the certificate that the forcing wave is well defined.

**Testable hypothesis.** There exists an anisotropic chip-firing family where boundary seeds of size `O(L)` or smaller force `Theta(L^2)` or better solved volume, so `r/n -> 0` while `m/n` stays below the target regime.

**First experiment.**
- Search directed strips or sparse anisotropic lattices rather than full square grids.
- Compare regular-grid controls against hand-biased transport rules.
- Track `r(L)`, `m(L)`, `t(L)`, and whether isolated `(a,-a)` residues are produced systematically.

**Strongest failure mode.** Symmetric diffusion smears certificates instead of isolating them, so the model becomes a pretty metaphor for linear closure but does not actually create new forced vertices efficiently.

**Angle to avoid.** Do not run vanilla sandpile diffusion on a regular grid and hope the verifier likes it. If the dynamics are not explicitly engineered to isolate `(a,-a)` residues and shrink `r`, the CA interpretation is cosmetic.

## Direction 3: Renormalized Macro-Cell / Substitution Automata
**Gap attacked.** Numerical constructions can discover intricate finite gadgets, but that does not automatically produce a scalable family. The missing piece is a recursive local-rule grammar whose score can be analyzed level by level.

**CA formulation.**
- Build a macro-cell automaton that emits sparse active corridors and shared boundary interfaces.
- Use substitution rules to tile macro-cells into larger ones.
- Use SAT or SMT only to verify one local motif and its lift across scales, not to brute-force whole graphs.

**Testable hypothesis.** There exists a substitution family with transfer matrix
that makes `m+r` grow strictly slower than `n-t`, so the level-`k` score `S_k`
decreases with scale and crosses `1.675`.

**First experiment.**
- Solve level-1 and level-2 motifs with hard verifier legality constraints.
- Derive a transfer matrix on boundary certificate types.
- Reject motifs whose transfer ratio is flat or worse than the target.
- Keep only motifs with sublinear or shared-boundary growth in active edges.

**Strongest failure mode.** Interfaces duplicate costs as fast as they create solved volume, so recursion gives no asymptotic gain and the substitution system is just a dressed-up tensor product.

**Angle to avoid.** Do not repeat wallpaper tilings, plain tensor powers, or SAT on whole small graphs with no renormalizable grammar. If there is no reusable macro-cell interface, there is no scaling story.

## Recommended Order
1. Start with Direction 2 if the team wants the cleanest alignment with forcing rule 3.
2. Start with Direction 3 if the team wants the fastest scale or no-scale verdict.
3. Keep Direction 1 as the hedge against bounded-slope saturation.

## Pivot Triggers
- Realized slope complexity stays `O(1)` across scale.
- `r/n` does not shrink.
- Level-to-level transfer ratios stop improving.
- The CA description is no shorter or more reusable than directly writing `f_i`.
