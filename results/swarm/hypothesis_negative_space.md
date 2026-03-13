# Hypothesis Negative Space

Date: 2026-03-13
Task: Improve the Ramsey number `R(5,5)` bound
Role: `hypothesis_scout`

## Scope

This memo deliberately avoids the families that are already crowded, promoted, demoted, or retired in the current packet:

- promoted `H1` atlas / canonicalization / transfer / witness-safety work
- backup `H2` decomposition upgrades around pair split or shell gluing
- reserve `H3` certificate packaging or IC3-style proof reuse
- generic GA, SA, RL, rare-event, or defect-minimization stories
- generic LP, flag, SDP, or Terwilliger tightening
- same split/glue plus a stronger SAT engine

The goal is not to polish those routes. The goal is to identify three testable directions that attack what the current packet still leaves structurally unclaimed.

## Derivative Branches Rejected Up Front

### 1. Plain canonical augmentation / orderly generation

Overlap:
- Too close to Lehavi-style one-vertex extension plus the current `H1` frontier-parent surface.
- Narrow external checks also found constructive-generation overlap in the generalized triangle Ramsey literature.

Pivot:
- Do not reopen this as a main direction unless the output is a completeness-certified parent/child poset with replayable exclusion certificates, not just a cleaner enumerator.

### 2. Switching-class or spectral compression

Overlap:
- The local falsifier already warns that Seidel/spectral compression is a search aid unless it yields a real Ramsey obstruction or certificate path.

Pivot:
- Do not spend budget here as a headline route.

## Narrow Overlap Guardrails From External Checks

I used a narrow search budget only to test a few surprising abstractions before drafting this memo.

- Degree-matrix abstraction is real prior art in smaller exact Ramsey computation, so "add degree constraints" is not novel by itself.
- BDD/ZDD-based Ramsey algorithms also exist, so "use decision diagrams" is not novel by itself.
- Constructive graph generation for Ramsey problems also exists, so "generate isomorph-free Ramsey graphs" is not novel by itself.

That means each surviving direction below is phrased around the missing Ramsey object or certificate path, not around importing a tool name.

## Candidate 1: Degree-Matrix And Joint-Neighborhood Bundle Polytope

### Why this is negative space

The current repo uses degrees, neighborhood types, and LP-feasible count vectors mostly as cheap filters. It does not treat them as the primary exact abstraction layer. That leaves a gap between "weak admissibility check" and "full split/glue residue search."

This direction attacks that gap directly:

- ignored: two-level colored degree abstractions as the main state variable
- failed to test: whether joint red/blue neighborhood bundle types already determine most impossible `45`-vertex states
- could not scale: exact search that branches before coarse structural signatures are frozen

### Hypothesis

A feasible colored degree matrix plus a small catalog of compatible joint-neighborhood bundle types will collapse most of the `R(5,5)` upper-bound residue before split/glue or SAT ever starts. If true, the endgame can become "enumerate a much smaller exact abstract state space, then certify the residue" rather than "branch on raw partial colorings."

### First falsifiable experiment

1. Start on a solved ladder rung or on the reconstructed `42/43` frontier packet.
2. Enumerate feasible colored degree matrices and pair-neighborhood bundle signatures.
3. Check whether all known `42`- and `43`-vertex witnesses survive.
4. Measure whether the surviving abstract states shrink the candidate family by an order-of-magnitude style factor before any decomposition primitive is applied.

### Overlap and pivot note

Overlap risk:
- current cheap degree/neighborhood filtering in the repo
- Codish-style abstraction-and-symmetry-breaking work on smaller Ramsey instances

Pivot rule:
- If this becomes "same split/glue with extra degree headers" or "more LP," kill it.

### Angle To Avoid

Do not pitch this as more degree constraints, more LP, or a warmed-over split-plus-SAT pipeline.

## Candidate 2: Witness-Preserving Rewrite Grammar For Exact `K_43` Family Geometry

### Why this is negative space

The benchmark packet repeatedly notes that exact `K_43` witnesses are still treated mostly as endpoints. The repo lacks neutral-start recovery, automorphism/defect-overlap clustering, and a real map of how distinct exact witnesses are related. Non-Exoo and deliberately asymmetric families are discussed as controls, but not as the primary constructive object.

This direction attacks that omission:

- ignored: exact witness-family geometry as an object of study
- failed to test: whether a small set of exact local rewrites moves between non-isomorphic valid `43`-vertex witnesses
- could not scale: seed diversification beyond Exoo-like lineages without collapsing into raw optimizer search

### Hypothesis

There is a compact grammar of exact local rewrites - motif swaps, orbit-breaking rewires, or witness-preserving edge exchanges - that connects meaningful regions of the valid `43`-vertex witness space. If true, that grammar can synthesize genuinely asymmetric parent families and identify which local transformations actually change extendability pressure toward `44`, rather than just improving defect scores.

### First falsifiable experiment

1. Start from the stored exact `43`-vertex witnesses.
2. Enumerate minimal local rewrites that preserve the `R(5,5)` witness property exactly.
3. Build a reachability graph of witness families under those rewrites.
4. Compare extension behavior and family diversity against Exoo-only and curated-seed baselines.

### Overlap and pivot note

Overlap risk:
- Exoo-line search
- Ge-style low-defect witness analysis
- generic move-set tweaking from GA / rare-event narratives

Pivot rule:
- If the rewrite system does not preserve exact witnesses, or only produces nicer near-misses, it has collapsed back into optimizer theater and should be killed.

### Angle To Avoid

Do not sell this as a better move set, a new basin, or "more asymmetric seeds." The object has to be an exact rewrite grammar with family-level transfer, not a search heuristic.

## Candidate 3: Decision-Diagram Compiler For Residue And Obstruction Families

### Why this is negative space

The live packet branches over individual partial colorings, then worries about proof logs and replay later. That leaves the family object itself mostly implicit. Narrow external checks found prior BDD-based Ramsey algorithms, but the repo has not explored decision diagrams as a proof-carrying representation for `R(5,5)` residue families, extension families, or obstruction transversals.

This direction attacks that representational gap:

- ignored: exact family compression as the primary proof object
- failed to test: whether repeated branch families can be compiled once and reused canonically
- could not scale: branch-local SAT or proof logging that rediscovers the same sparse families many times

### Hypothesis

A ZDD/BDD layer over partial colorings or obstruction-transversal families can compress the repetitive part of the `R(5,5)` search enough to make pruning cumulative and replayable. The gain would not be "BDD is faster than SAT." The gain would be that the stored object is an exact reusable family certificate rather than a branch-specific proof trace.

### First falsifiable experiment

1. Encode a solved smaller certificate case, or the `42 -> 43` extension family, as a decision-diagram object.
2. Compare it against the CNF / proof-log baseline on three axes:
   - witness survival
   - reusable family exclusions
   - checker-visible replay size
3. Kill the route immediately if the compiled object does not improve certificate-path quality or exact family reuse.

### Overlap and pivot note

Overlap risk:
- older BDD-based Ramsey algorithms
- certificate-only infrastructure if the result is just a new storage format

Pivot rule:
- If this is only a backend swap, it is derivative. Keep it only if it yields a reusable family certificate that shrinks checked proof cost or exact search state.

### Angle To Avoid

Do not count node totals or runtime alone. If it does not improve witness-safe family compression or a replayable certificate path, it is not a live hypothesis.

## Recommended Order

1. `Degree-Matrix And Joint-Neighborhood Bundle Polytope`
   - Best chance to open a new exact abstraction layer without re-entering retired H2/H3 language.
2. `Witness-Preserving Rewrite Grammar For Exact K43 Family Geometry`
   - Best lower-bound-side negative space if the team wants a non-optimizer constructive object.
3. `Decision-Diagram Compiler For Residue And Obstruction Families`
   - Highest representation novelty, but easiest to accidentally demote into backend engineering.

## Bottom Line

The clean negative space is not "another optimizer," "another SAT engine," or "another certificate wrapper." The clean negative space is:

1. a stronger exact abstraction before decomposition,
2. an exact rewrite object for witness families, or
3. a reusable family certificate representation.

Anything softer than that is too close to routes the repo has already promoted, demoted, or retired.
