# Falsifier Memo for Improving `R(5,5)`

## Scope

This memo attacks the current likely hypothesis families already present in the workspace:

- rare-event / defect-manifold lower-bound search
- finite-`n` Terwilliger / flag / spectral rigidity for the upper bound
- IC3/PDR / conflict-kernel / decomposition-reform SAT upper-bound search

The standard here is adversarial. A method does not get credit for looking sophisticated. It only gets credit if it crosses the threshold that actually moves the bound.

## Non-Negotiable Falsifier Thresholds

- Lower-bound work is not progress unless it outputs an independently verified `44`-vertex coloring. Better defect scores, a positive defect floor, or nicer search trajectories do not improve `R(5,5)`.
- Upper-bound work is not progress unless it outputs a machine-checkable proof or certificate that `45`-vertex colorings are impossible, or reduces to a residue with a clear and credible certificate path.
- Structural novelty is not established by importing a method name from physics, coding theory, or hardware verification. It is established only by a new reusable Ramsey obstruction, invariant, rigidity statement, or proof-grade lemma.

## 1. Rare-Event / Defect-Manifold / Frontier-Atlas Lower-Bound Family

### Easiest failure or rehash accusations

- This is still Exoo-style search with a fancier energy function. Prior overlap already includes Exoo, the 2010 symmetric-heuristic GA paper, Ge et al.'s re-analysis of Exoo with very low-defect `K_43` colorings, analog Max-SAT work, and RL-style Ramsey search.
- Multicanonical or population-annealed language only changes the optimizer. If the actual object is still "find lower-defect colorings," the work will read as optimizer theater.
- A reproducible positive defect floor at `n=44` is not evidence of impossibility. It is equally consistent with a poor move set, bad collective variables, symmetry bias, or an overfit energy.
- Learning obstruction cores only from known `42`-vertex or Exoo-derived families risks memorizing one construction lineage instead of discovering transferable structure.
- Search with live upper-bound filters is one unsound pruning rule away from deleting a real witness.

### Missing controls

- Recover known `42`- and `43`-vertex witnesses from neutral random starts, not only from Exoo-like seeds.
- Run leave-one-parent-out evaluation on `42 -> 43` extension data.
- Test non-Exoo seed families and deliberately asymmetric perturbations.
- Ablate each defect coordinate, collective variable, nonlocal move, and symmetry-breaking rule.
- Prove soundness, or at minimum exhaustively stress-test survival, for every upper-bound-derived pruning filter on all known witnesses.
- Compare against equalized baselines by total edge flips, neighbor evaluations, and SAT or LP calls, not by wall-clock on mismatched implementations.

### Benchmark traps

- Counting best defect seen instead of witness-finding probability.
- Reporting one lucky run, one seed family, or one highly curated near-miss corpus.
- Using near-miss quality as a surrogate for extendability to `44` vertices.
- Claiming a "new basin" without automorphism-class and defect-overlap clustering.
- Treating failure to find `K_44` as evidence toward an upper bound.

### Literature branches that invalidate weak claims

- Exoo-style constructive lower-bound search.
- The 2010 symmetric-heuristic GA paper for `R(5,5)`.
- Ge et al. on Exoo's lower bound and low-defect variants.
- Analog Max-SAT or analog-solver Ramsey work.
- RL or learning-based Ramsey graph search.
- Generic rare-event and multicanonical optimization literature, if the claimed novelty is only algorithmic and not Ramsey-structural.

## 2. Terwilliger / Flag / Spectral / Finite-Stability Upper-Bound Family

### Easiest failure or rehash accusations

- This is generic SDP or flag-algebra tightening with coding-theory branding. The overlap is already explicit: McKay-Radziszowski, Angeltveit-McKay `<= 48` and `<= 46`, semidefinite Ramsey papers, and split-Terwilliger code bounds.
- A degree-`4` or low-order colored moment relaxation at `n=45` may still leave a residue no smaller than the current LP-plus-gluing frontier.
- Floating-point infeasibility is not a Ramsey bound. Without rational reconstruction or an exact certificate path, it is just a numerical-artifact candidate.
- Finite-`n` rigidity around a `13`-part asymptotic template may simply not bite at `n=45`; asymptotic stability does not automatically control the exact frontier.
- Seidel or spectral filtering can remove many switching classes while proving nothing about actual graph existence. That is a search aid, not an upper-bound result.

### Missing controls

- Reproduce smaller solved Ramsey instances, `R(4,5)=25`-style subcases, or known extremal catalogues before touching `n=45`.
- Run side-by-side ablations versus plain LP, plain flag, and plain SDP with the same type basis.
- Audit exactness of every block diagonalization, symmetry quotient, and basis truncation.
- Export rationalized or exact infeasibility certificates for any claimed upper-bound implication.
- Show that surviving parameter signatures can be exhaustively checked faster than the status quo.
- Remove `13`-part priors and spectral priors and verify the claimed gain survives.

### Benchmark traps

- Reporting variable-count reduction instead of final certificate size or checker runtime.
- Testing only toy instances where any low-order relaxation succeeds.
- Comparing different bases or different solvers and attributing all gains to Terwilliger structure.
- Calling a smaller feasible moment region "progress" when it does not shrink the exact endgame.

### Literature branches that invalidate weak claims

- McKay-Radziszowski subgraph-counting and upper-bound work.
- Angeltveit-McKay `R(5,5) <= 48` and `R(5,5) <= 46`.
- Semidefinite programming for Ramsey numbers.
- Schrijver, Terwilliger, and association-scheme SDP bounds for codes.
- Seidel-switching, spectral, and equiangular-line literature if the method is only a spectral-compression story.
- Recent multiplicity and stability work if the claim is merely that `13`-part templates matter.

## 3. IC3/PDR / Conflict-Kernel / Decomposition-Reform Upper-Bound Family

### Easiest failure or rehash accusations

- If the state space is still split-vertex, edge-gluing, or transverse-edge gluing, this is the same decomposition with a stronger SAT engine.
- Conflict kernels extracted after the fact may fail to transfer across branches. If so, they are compressed proof logs, not new structural obstructions.
- Orbit-canonicalization and invariant learning may cost more than the branching they save.
- Learned clauses can be encoding-specific and fail to survive changes in decomposition or symmetry conventions.
- A dramatic branch-count reduction on easy subcases may still fail to reduce proof size, proof-check time, or unresolved residue on `n=45`.
- Adding clause learning to a line that previously used a special-purpose solver without clause learning is an engineering delta, not by itself a new Ramsey idea.

### Missing controls

- Compare against the exact same decomposition with modern SAT and proof logging but without IC3/PDR or invariant learning.
- Separate gains from decomposition choice, clause learning, symmetry reduction, and learned-kernel reuse.
- Run held-out transfer tests: kernels learned on one gluing family must prune a disjoint family.
- Maintain end-to-end certificate artifacts: CNFs, proof logs, checker outputs, and regeneration scripts.
- Climb a verified benchmark ladder before making `n=45` claims: Schur Number Five, SAT+CAS Ramsey certificates, and formal `R(4,5)=25`-style proof pipelines.

### Benchmark traps

- Counting eliminated branches instead of proof bytes or verified runtime.
- Using handcrafted subproblems rich in repeated motifs.
- Calling a small residue "tractable" without actually finishing it.
- Optimizing unknown-edge count, isomorphism collapse, or UNSAT-core reuse while the actual checked proof gets larger.

### Literature branches that invalidate weak claims

- Angeltveit-McKay `<= 46`, which already integrates SAT inside LP-plus-gluing.
- Gauthier's 2025 upper-bound strategy, which already pushes SAT decomposition through splitting vertices and transverse-edge gluing.
- Schur Number Five and SAT proof logging.
- SAT+CAS verified Ramsey certificates for nearby problems.
- Formal proof and certificate pipelines such as `R(4,5)=25`.

## 4. Cross-Cutting Novelty Illusions

- Method-import theater: rare-event sampling, Terwilliger algebra, IC3/PDR, or CEGAR names are doing the novelty work while the Ramsey object is unchanged.
- Proxy-metric inflation: fewer defects, fewer branches, smaller SDPs, or cleaner switching classes without a new bound or a certificate path.
- Frontier overfitting: tuning to known `42`-vertex graphs or friendly gluing instances and mistaking memorization for structure.
- Stale-baseline illusion: the local watchlist and frontier files are noisy enough that a weak literature review can make almost anything look novel.
- Search/proof conflation: heuristic evidence toward infeasibility is being blurred with proof of infeasibility.
- Residue laundering: a method reports "dramatic reduction" and quietly hands the hard part back to the old pipeline.

## 5. Fastest Invalidators To Apply Before Taking Any Claim Seriously

1. Ask whether the output is a verified `44`-vertex witness or a machine-checkable `45`-vertex impossibility proof. If not, it is intermediate evidence only.
2. Replace the imported engine with a plain baseline using the same representation, decomposition, and filters. If the gain disappears, the novelty claim collapses.
3. Remove Exoo-family seeds, `13`-part priors, and favored symmetry coordinates. If performance collapses, the method is overfit.
4. Move to held-out frontier families and verified benchmark ladders. If kernels, defects, or invariants do not transfer, the structural claim is false.
5. Demand exact certificates or rationalized outputs for any upper-bound statement. If that path is absent, the claim is not bound-improving.

## Bottom Line

- The easiest bad paper here is "same search or proof pipeline, new imported engine."
- The easiest honest failure is "strong proxy metrics, no certificate."
- The only durable moat is a new reusable Ramsey structural object: an obstruction family, exact rigidity statement, or proof-grade invariant that survives held-out tests and feeds directly into a verified bound.
