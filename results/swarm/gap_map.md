# Gap Map

## Snapshot

- This map is based on the current local artifact set, not a fresh literature sweep.
- The active overlap boundary is already clear from the repo:
  - provenance baseline: OEIS `A129258`, `A129259`, Kimberling;
  - main overlap risk: Ford-style multiplication-table / divisor-in-an-interval language.
- The old small-horizon framing is stale.
  - The baseline million-step run now reaches record gap `30` at step `729353`.
  - The archived `column_immediate` run reaches row-gap `31`.
- Two strong negative facts now shape the search space:
  - the strong compact-certificate form of `H1` fails on the current corpus;
  - crude `H2` prime-support observables do not explain the late records.

## Prioritized Negative Space

### 1. Composite-Only Frontier Intervals

**Priority:** highest  
**Type:** under-explored setting

**Gap.**
Long record gaps already occur with no skipped primes at all, but the project has not yet treated this as its own mathematical regime.

**Why this looks genuinely under-served.**
Popular narrations drift toward prime placement or prime-support imbalance. The current corpus shows that those are, at best, background state. In the baseline run, gaps `17`, `20`, `21`, `28`, and `30` are composite-only; in the `column_immediate` run, gaps `20`, `21`, `23`, `26`, and `31` are composite-only as well.

**Concrete open question.**
Can arbitrarily long row-gap records occur inside fully composite skipped blocks, and is there a `T`-specific criterion for when the current border semigroup covers such a prime-free interval?

**Why it matters.**
Any eventual proof or disproof that still leans on prime obstruction as the main event is probably mis-specified.

**Minimal next step.**
Treat prime-free record intervals as a first-class benchmark family and compare them against prime-bearing record intervals and matched non-record windows.

**Overlap risk.**
If this is phrased only as generic local factor coverage, it collapses into the Ford branch.

### 2. Previous-Column Anchor And Offset Geometry

**Priority:** high  
**Type:** under-explored setting

**Gap.**
The only stable `T`-specific motif surviving late-record analysis is the one-point axis-1 marker `1 * previous_column_term`, but nobody has turned that into a serious geometric model of the frontier.

**Why this looks genuinely under-served.**
This anchor is endogenous to the mex-coupled process, not borrowed from generic multiplication-table language. Every analyzed late record gap contains the previous column term inside the row-gap interval, yet the current writeups treat it as an observation rather than a state variable.

**Concrete open question.**
Does boundedness reduce in part to controlling the offset process
`Delta_n = T(n,1) - T(1,n)`
and the two subintervals on either side of the previous-column anchor?

**Why it matters.**
If there is any compact `T`-specific obstruction left after the failure of raw witness compression, this anchor-and-offset geometry is the most plausible place for it to live.

**Minimal next step.**
Log the left/right interval structure around the previous-column anchor for every late record gap and matched non-record window, then test whether offset size or anchor position predicts future records.

**Failure mode.**
The anchor may be too thin to control more than one skipped value. If so, this line should be demoted quickly rather than romanticized.

### 3. Full-Witness Invariants Rather Than Chosen-Witness Taxonomy

**Priority:** high  
**Type:** failure mode plus under-explored setting

**Gap.**
The current `H1` and part of `H2` story are being judged from one stored witness per skipped integer plus a multiplicity count. That is enough to make raw `H1` look weak, but not enough to rule out compression at the level of the full witness hypergraph.

**Why this looks genuinely under-served.**
The benchmark audit is explicit that the chosen-witness summaries are canonicalization-sensitive, while the full hypergraph checks cover only selected late gaps. So the present negative result is informative but not yet structurally complete.

**Concrete open question.**
Do late record gaps share a bounded family of higher-level invariant profiles, such as hypergraph description length, branching profile, balancedness buckets, or other factorization-graph coordinates, even when explicit factor pairs diversify?

**Why it matters.**
This is the last credible rescue route for a compact witness story that is still more specific than generic local divisor coverage.

**Current evidence pushing this gap open.**
- Singleton coverage remains high even at late records.
- Tiny-factor share falls with scale.
- The `min factor > 100` bucket rises sharply by gap `30`.

That trend rejects a small-factor grammar, but it does not yet settle whether a coarser invariant compresses the interval.

**Minimal next step.**
Recompute every baseline record gap from `20` upward from full hypergraphs under at least two witness canonicalizations, then test whether any interval-level invariant stays stable.

### 4. Border-Ordered Interval-Extension Criterion

**Priority:** medium-high  
**Type:** under-explored setting

**Gap.**
Pointwise witnesses do not compress, but the repo has not yet tested whether interval-wide coverage is forced by a bounded ordered prefix of actual border factors.

**Why this looks genuinely under-served.**
This is a sharper question than “is the local product set dense?” It asks whether the mex-coupled border order itself carries a short interval-extension mechanism, which would be specific to `T` rather than to arbitrary product sets.

**Concrete open question.**
Is there a uniformly bounded, or at least slowly growing, ordered prefix of border factors whose coverage inequalities force the entire skipped interval below the next mex?

**Why it matters.**
If such a criterion exists, it would provide a real obstruction language for boundedness. If it fails, that failure is itself evidence that the process is drifting toward generic divisor-in-an-interval behavior.

**Minimal next step.**
For each late record gap, search for the shortest ordered border prefix that explains full interval coverage and compare that prefix length against matched surrogate product sets.

**Overlap risk.**
This item has the highest derivative risk. It survives only if the border order and mex coupling are mathematically essential.

### 5. Coupled Prime-Index Operator Beyond Crude Support Counts

**Priority:** medium  
**Type:** under-explored setting

**Gap.**
The negative-space memo points to the recursively selected prime-index supports with odious exponents as the real structural object, but `H2` only tested crude counts such as support imbalance below `sqrt(previous_row_term)`.

**Why this looks genuinely under-served.**
The existing `H2` failure does not kill the stronger structural question. It only kills the weak version in which smooth support counts are supposed to explain record gaps directly.

**Concrete open question.**
Does the coupled operator on the row-side and column-side prime-index sets admit a fixed-point, instability, or renormalized state variable that predicts when the induced row semigroup leaves a long uncovered frontier block?

**Why it matters.**
If this line works at all, it would explain boundedness or unboundedness through the exact recursive support law noted in the OEIS-linked framing, not through generic prime-gap heuristics.

**Minimal next step.**
Move past raw support counts. Define one or two sharper state variables on the prime-index supports and test them on the late baseline records `25`, `28`, `30` and the late axis-swapped row records.

**Failure mode.**
If the line is restated only as prime density, prime counts, or side imbalance, it is just the already-failed weak `H2` story.

## What To Explicitly De-Prioritize

- Repeating provenance:
  - rebuilding the array;
  - restating the prime split;
  - re-asking Kimberling's bounded-difference question.
- Positive compact-certificate rhetoric for `H1`.
  - The stored corpus currently supports a negative result, not a surviving compact mechanism.
- Prime-gap or prime-assignment stories by themselves.
  - Composite-only late records already block that narrative.
- Multiplication-table, sparse multiplicative-basis, or generic hypergraph rebranding without a new `T`-specific invariant.
- “More horizon” as a contribution by itself.
  - Computation matters here only when it emits proof-oriented artifacts and controls.

## Recommended Next Moves

1. Build the next record-gap table around composite-only intervals, anchor geometry, and matched non-record controls.
2. Upgrade from chosen witnesses to full-witness invariants before making any further witness-taxonomy claim.
3. Test one border-ordered interval-extension criterion against surrogate product-set controls.
4. Revisit the prime-support line only in the stronger prime-index-operator form, not the already-failed support-count form.
