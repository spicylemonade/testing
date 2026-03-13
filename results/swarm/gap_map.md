# Gap Map: Negative Space Around Improving `R(5,5)`

## Scope

- The named markdown artifacts were read first, but most of their watchlist/frontier content is query noise rather than real Ramsey prior art.
- The useful local signal is concentrated in the `R(5,5)`-specific probe files, especially the Exoo line, the older McKay/Radziszowski upper-bound line, and the Angeltveit-McKay updates.
- A small targeted external check was used only to refresh the stale upper-bound frontier and inspect the recent proof-strategy direction.
- Working frontier on 2026-03-13: `43 <= R(5,5) <= 46`.
- The gap is not "do more search." The gap is the missing structural layer between lower-bound constructions and upper-bound case proofs.

## Ranked Gaps

### 1. Frontier Atlas of `42`-Vertex Critical Colorings

- Why it is under-served:
  The `42`-vertex witnesses are still mostly used as existence proofs. There is no shared structural atlas of the frontier itself.
- Failure mode:
  Search on `43`-`45` vertices starts almost blind, even though the only exact frontier data already lives on `42` vertices.
- Concrete first experiment / proof angle:
  Build a canonical atlas of the available `42`-vertex graphs: automorphism groups, orbit partitions, degree profiles, spectra, common-neighborhood fingerprints, and small induced subgraph frequencies. Then classify orbit-distinct one-vertex extensions and their failure types.
- Why it matters:
  This is the one part of the search space where exact information already exists and can be compressed instead of rediscovered.

### 2. Extension-Obstruction Mining Instead of Raw Near-Miss Optimization

- Why it is under-served:
  Repo-local artifacts and recent heuristic work both point to many near-miss `43`-vertex colorings with very few monochromatic `K_5`s, but almost none of that effort is organized around recurring minimal obstructions.
- Failure mode:
  Minimizing the total number of monochromatic `K_5`s rewards graphs that look close while remaining structurally unextendable.
- Concrete first experiment / proof angle:
  For each `42`-vertex frontier graph, enumerate inequivalent one-vertex extensions and record a minimal obstruction witness for failure: which local edge pattern forces a red `K_5` or blue `K_5`, how localized it is, and which obstruction cores recur across many parents. Reuse those cores as SAT clauses, MaxSAT penalties, and local-search rejection rules.
- Why it matters:
  The right object is not "a graph with few bad cliques." It is "a graph whose extension failures share reusable structure."

### 3. Lower-Bound Search With Upper-Bound Filters in the Loop

- Why it is under-served:
  The lower-bound and upper-bound literatures are still largely siloed. Constructive search chases low defect counts, while upper-bound work derives strong necessary conditions from degrees, neighborhood types, linear constraints, and gluing impossibility.
- Failure mode:
  Lower-bound search repeatedly walks into regions that upper-bound machinery already knows are impossible.
- Concrete first experiment / proof angle:
  Turn the cheapest necessary conditions from the `R(5,5) <= 46` pipeline into incremental rejection or scoring oracles for search on `43`-`45` vertices:
  - degree admissibility
  - allowed neighborhood / dual-neighborhood profiles
  - LP-feasible count vectors
  - small local impossibility templates derived from failed gluing cases
- Why it matters:
  This uses upper-bound structure as active pruning rather than as a separate proof after the fact.

### 4. Better Decomposition Primitives Than One-Vertex Split Plus Edge Gluing

- Why it is under-served:
  The strongest upper-bound line now leans heavily on one decomposition language: split by a single vertex and glue along a transverse edge. The 2024 `<= 46` work pushed that language hard, and the 2025 strategy note still inherits the same basic bottleneck.
- Failure mode:
  Case explosion survives faster SAT and more hardware because the decomposition primitive itself is weak.
- Concrete first experiment / proof angle:
  Benchmark alternative decomposition primitives on known frontier objects and hypothetical partial colorings:
  - two adjacent vertices instead of one
  - two nonadjacent vertices
  - small separator shells built around a forced `K_4` or independent `4`-set
  - orbit-balanced or equitable partitions suggested by automorphism data
  Track each primitive by unknown-edge count, isomorphism collapse rate, proof-core reuse, and compatibility with LP constraints.
- Why it matters:
  If the upper bound moves again, it is likely because the decomposition got better, not because the same split ran longer.

### 5. Proof-Carrying Exact Computation and Reusable Obstruction Certificates

- Why it is under-served:
  Exact computations in this area are still mostly result-oriented. Dead branches are rarely turned into compact, independently checkable, reusable certificates.
- Failure mode:
  Each new run re-discovers many of the same impossible partial colorings, and independent verification remains expensive.
- Concrete first experiment / proof angle:
  Start with verified small benchmarks and tractable `R(5,5)` subcases. Extract canonical UNSAT cores, forbidden partial-coloring lemmas, and orbit-stable obstruction certificates from failed branches. Measure whether those certificates prune fresh branches in later runs rather than merely documenting one proof.
- Why it matters:
  This converts computation from a one-off search into a cumulative constraint library.

## Space To Deprioritize

- Generic GA / simulated annealing / RL over raw monochromatic `K_5` count.
  This repeatedly yields near-misses without exposing reusable structure.
- Pure circulant or full-symmetry search.
  Symmetry should be used as a prior and compression device, not as a hard cage.
- Monolithic SAT case-splitting with no new abstraction layer.
  The present bottleneck is structural compression, not only solver throughput.

## Working Thesis

If `R(5,5)` moves soon, it is more likely to move because someone compresses the frontier structurally than because someone reruns the same objective with more compute. The most credible negative space is therefore:

1. exact frontier mining on `42` vertices,
2. extension-obstruction learning,
3. coupling upper-bound filters into constructive search,
4. replacing the current decomposition language with stronger primitives, and
5. turning failed computation into reusable certificates.

## Anchor Signals Used

- Exoo's lower-bound line and the 2022 study of that construction
- McKay/Radziszowski upper-bound work and Angeltveit/McKay's later `R(5,5)` improvements
- the recent strategy work on lowering the upper bound with SAT-style decomposition
