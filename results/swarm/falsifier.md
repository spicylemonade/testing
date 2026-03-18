# Falsifier Memo: Hadamard 668 via Cellular Automata

Scope: adversarial review of the repo's cellular-automata directions for Hadamard order `668`, using `results/research_context.md`, `results/literature/prior_art_watchlist.md`, `results/literature/prior_art_gap.md`, `results/swarm/gap_map.md`, and `results/swarm/hypothesis_negative_space.md`.

Terminology note: in the relevant literature, `cellar automata` does not appear as a distinct Hadamard-search method family. Treat it as `cellular automata` unless a different meaning is supplied explicitly.

Status note: the exact real order-`668` problem still appears open in the latest material reviewed here. The strongest current anchor is the recent `64`-modular order-`668` construction, which is a near miss, not an exact Hadamard matrix.

## Likely Hypotheses Under Review

1. Defect-repair CA starting from the recent `64`-modular order-`668` construction.
2. Lag-space CA over four length-`167` channels instead of a raw `668 x 668` sign matrix.
3. Generative spacetime CA whose rule table and seed emit the rows of a candidate order-`668` matrix.

## Highest-Risk Failure Modes

### 1. The proposal can collapse into "just another local search heuristic"

- The easiest accusation against the defect-repair direction is that it is only asynchronous hill-climbing, tabu-like repair, Ising descent, or decoder-style defect transport with CA language pasted on top.
- If each update step still depends on the full Gram matrix, full autocorrelation spectrum, or a dense global score recomputation, then the method is not meaningfully local in the CA sense.
- If the only novelty is the update schedule or the use of local neighborhoods around defects, that is too weak. The Hadamard search literature already contains annealing and quantum/Ising-style formulations, and the broader CA literature already contains local defect-propagation and repair dynamics.

Kill test:
- Reject the CA framing if matched greedy, tabu, simulated annealing, or quantum/Ising surrogates repair the same seeded instance as well or better under equal evaluation budgets.

### 2. The proposal can collapse back into standard structured-sequence search

- The lag-space direction is easy to accuse of rehashing `Williamson`, `Turyn`, `Goethals-Seidel`, cocyclic, or supplementary-sequence search if its state space or invariants reconstruct those families.
- For the arithmetic actually relevant here, `668 = 4p` with `p = 167 ≡ 3 mod 4`, even the cocyclic branch is already funneled into highly specific Williamson-type or transposed-Ito structure. That makes "CA over quotient coordinates" especially vulnerable to the accusation that it is just a new neighborhood policy over a known constrained family.
- If successful trajectories only occur after imposing circulant, quasi-circulant, compression, amicability, or other classical structure, then the CA is not the main contribution. The structure is.
- If the representation is sequence-native but the update rule is just a localized move operator inside an existing ansatz, the novelty claim shrinks to "another optimizer over a known family."

Kill test:
- Reject the novelty claim if every exact or near-exact success canonically maps into an already-studied structured family.

### 3. The generative spacetime idea may be too rigid to express the relevant `668` frontier

- Order `668 = 4 * 167` is driven by a prime-length core `167`, while much of the direct CA-to-Hadamard literature is comfortable in prime-power, finite-field, or `4t^2`-type constructive regimes.
- A compact local rule table may simply be too restrictive: it can generate short periodic or algebraically tidy orbits without ever expressing the irregular structure needed for the known `64`-modular near-solution, let alone an exact real Hadamard matrix.
- If the only productive rules are linear or bipermutive ones, the work risks collapsing directly into prior CA construction literature rather than solving the open `668` case.

Kill test:
- Reject the generative CA route if it cannot reproduce the qualitative defect profile of the best known `64`-modular seed or if it only yields power-of-two or prime-power-flavored behavior.

### 4. The locality assumption may simply be false

- Hadamard orthogonality is dense and all-to-all. A small local improvement can create long-range damage elsewhere.
- The defect-repair hypothesis assumes the remaining violations in the modular seed behave like sparse mobile charges. That may be wrong: a few visible defects can still require globally coordinated sign changes.
- The lag-space version has the same issue in another coordinate system. Local lag fixes may interact nonlocally through the rest of the autocorrelation spectrum.

Kill test:
- Reject the sparse-defect story if defect count plateaus quickly, diffuses instead of annihilating, or requires increasingly global corrective packets as the search improves.

### 5. The project can overclaim from approximate progress

- The recent order-`668` result is a `64`-modular Hadamard matrix with only `26` nonzero off-diagonal Gram entries. That is strong approximate structure, but it is not an exact Hadamard matrix.
- A CA that improves defect count, defect magnitude, or modular residuals without reaching exact zero does not solve Hadamard `668`.
- There is already a literature on approximate and near-Hadamard objects. Falling short of exact orthogonality moves the claim into that bucket, not into a solution of the order-`668` problem.

Kill test:
- Reject any "solves Hadamard 668" wording unless the final matrix is exactly Hadamard up to standard equivalence.

### 6. The wording "nobody tried CA here" is easy to falsify

- That statement is already too broad. CA have been used to generate Hadamard-adjacent objects through linear bipermutive CA, orthogonal arrays, orthogonal Latin squares, bent functions, and mutually unbiased bases.
- Even if none of that reaches real order `668`, a broad novelty claim will be attacked immediately.
- The defensible claim is narrower: CA do not appear to be established as a successful exact-search method for the specific real open case `668`, especially not on top of the new `64`-modular length-`167` frontier object.

Kill test:
- Reject any paper or memo draft that says or implies "cellular automata have not been used for Hadamard matrices" without the narrower qualifiers above.

## Missing Controls

1. Seed-matched non-CA repair baselines.
   - Any defect-repair CA started from the `64`-modular seed must be compared against greedy repair, tabu/local search, simulated annealing, and quantum/Ising-style baselines from the same seed.

2. Representation control.
   - If CA is run on length-`167` sequences, compare it against non-CA local search in exactly the same structured coordinate system.
   - Otherwise any gain may come from the representation, not from CA dynamics.

3. Exactness control.
   - Report exact Hadamard hits, not just defect counts, modular residuals, low-rank defect spectra, or best-so-far energies.

4. Symmetry and equivalence control.
   - Canonicalize under row/column sign flips, permutations, and any family-specific symmetries.
   - Otherwise the search may look broader than it is and comparisons become meaningless.

5. Structured-family leakage control.
   - Track whether the search has silently re-entered `Williamson`, `Turyn`, `Goethals-Seidel`, cocyclic, block-circulant, or other classical families.
   - If it has, evaluate novelty as an optimizer-only contribution.

6. Budget control.
   - Compare wall-clock time, objective evaluations, and update counts on equal hardware and equal seeds.
   - CA time steps are not a fair unit if one method uses cheap local counters and another recomputes global correlations.

7. Generalization control.
   - Rule tables or learned local policies should be trained or tuned on known solved instances, then tested on held-out instances and on `668`.
   - If the rule is hand-tuned on `668`, the result is not credible as a method claim.

8. Restart-statistics control.
   - Separate mean performance, variance, and best-of-many-restarts performance.
   - Hadamard-search heuristics can look much stronger when only the most favorable restart trace is shown.

## Benchmark Traps

1. Toy-order trap.
   - Success on small or power-of-two orders says little about `668`. That region overlaps too strongly with classical CA constructive families.

2. Seed unfairness trap.
   - Starting CA from the `64`-modular near-solution and comparing to random-start baselines is not informative.

3. Approximate-progress trap.
   - Reporting fewer defects on top of the modular seed as if the open order is nearly solved.

4. Global-information trap.
   - Advertising a method as CA while each update step depends on full Gram or full-spectrum recomputation.

5. Family-reentry trap.
   - Quietly imposing classical structured constraints to make the search work, then crediting CA instead of the recovered ansatz.

6. Single-seed trap.
   - A handpicked successful run from one seed or one rule table is weak evidence in a landscape this rugged.

7. Metric trap.
   - Comparing by raw iteration count instead of by exact objective evaluations, correlation updates, or wall-clock time.

8. Symmetry-leakage trap.
   - Counting equivalent matrices or equivalent sequence quadruples as separate successes.

9. Restart-cherry-picking trap.
   - Highlighting the best restart, prettiest trace, or most favorable seed instead of the full run distribution.

## Novelty Illusions

### "CA is new because no one tried automata on Hadamard matrices"

Weak. CA-to-Hadamard-adjacent construction work already exists. The stronger and narrower claim is only about CA as an exact search dynamic for the specific real order `668` problem.

### "Defect transport makes this fundamentally different from annealing"

Only if the defects are truly the operative state variable and the updates remain genuinely local. If a global energy still drives every move, the distinction is cosmetic.

### "Sequence-space CA is outside prior art"

Not automatically. If the state encodes the same constraints used by `Turyn`, `Williamson`, or `Goethals-Seidel` searches, it is still inside that branch.

### "Generative CA compresses the search, so it must be novel"

Compression alone is not novelty. The rule-table search must express the relevant frontier behavior and outperform simpler structured priors.

### "Improving the `64`-modular seed is basically solving `668`"

False. Approximate modular repair and exact real Hadamard existence are different claims.

### "Cellar automata is an untried method family"

As written, this looks like a terminology error more than a new method family. Leaving it uncorrected weakens credibility immediately.

## Literature Branches That Invalidate Weak Claims

### 1. The actual order-`668` frontier

- `A 64-Modular Hadamard Matrix of Order 668` (2025).
- This is the current hard anchor. Any method for `668` that ignores the special `64`-modular Golay quadruple / length-`167` structure is attacking the wrong object.

### 2. Structured Hadamard search and construction families

- `Williamson`, `Turyn`, `Goethals-Seidel`, cocyclic / `D_{4t}`, block-circulant, best/good matrices, quaternionic perfect sequences, and modern SAT/CAS-style enumeration and pruning.
- For the specific `4p` case with `p = 167 ≡ 3 mod 4`, the cocyclic branch is already strongly constrained. A CA acting in those coordinates is therefore much closer to "optimizer over an existing family" than to a new family.
- If CA enters these coordinates, the best interpretation is "another search operator inside a known family."

### 3. Quantum, annealing, and energy-based Hadamard search

- Quantum annealing and QAOA-style papers already formulate Hadamard search as optimization over structured variables.
- If the CA method is fundamentally an energy minimizer on the same objective, it is rehash-adjacent unless locality provides a demonstrable new advantage.

### 4. CA construction literature already touching Hadamard-adjacent objects

- Linear bipermutive CA have already been used to generate orthogonal Latin squares, orthogonal arrays, Hadamard matrices, and bent functions.
- CA-based mutually unbiased bases and related finite-field constructions further shrink any broad novelty claim.
- These branches matter even if they do not touch `668`, because they invalidate the claim that CA-plus-orthogonality is itself new.

### 5. Generic CA repair / decoder / learned-local-rule literature

- If the proposal becomes "local defect propagation" or "learned CA repair," then the novelty is at most a domain transfer to Hadamard search.
- That is still publishable if the performance is real, but it is not a brand-new method family.

### 6. Approximate / near-Hadamard literature

- If exact orthogonality is not achieved, the contribution belongs here, not in the exact Hadamard-existence line.

## Per-Hypothesis Falsifier Summary

### Defect-repair CA on the `64`-modular seed

- Strongest accusation: rebranded seeded local search.
- Fastest invalidator: equal-seed greedy/tabu/annealing repair matches or beats it.
- Hard requirement for survival: exact repair from the modular seed, not just better defect statistics.

### Lag-space CA on four `167`-channels

- Strongest accusation: disguised `Williamson`/`Turyn`/supplementary-sequence search.
- Fastest invalidator: all successful runs collapse into standard structured sequence families.
- Hard requirement for survival: nontrivial CA dynamics in a coordinate system that is smaller than the full matrix but not merely classical family syntax.

### Generative spacetime CA

- Strongest accusation: mismatched constructive family, too rigid for prime-length `167` core.
- Fastest invalidator: only short-period, linear, or power-of-two-style rules show traction.
- Hard requirement for survival: show that the rule-and-seed family can even approximate the known order-`668` frontier profile before claiming exact-search relevance.

## Bottom Line

The easiest way for this project to fail is not computational first. It is conceptual:

- overclaiming novelty where there is already CA-to-Hadamard-adjacent literature,
- overclaiming progress where there is only approximate modular repair,
- and overclaiming method identity where the engine is really standard structured search or standard local optimization.

The narrowest defensible version is also the safest one:

- CA as one local repair heuristic layered on top of the real `668` frontier object, namely the structured length-`167` modular seed,
- benchmarked against seed-matched non-CA repair baselines,
- with exactness, symmetry control, and structured-family leakage checked explicitly,
- and with the novelty claim limited to the optimizer role rather than to Hadamard constructions in general.
