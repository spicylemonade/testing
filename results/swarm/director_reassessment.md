# Director Reassessment: item_005

## Decision

`H1_defect_syndrome_ca_64m` remains the champion, and the case for it is stronger than in `results/swarm/director_brief.md`. The original swarm ranking in `results/swarm/hypotheses.json`, `results/swarm/tool_plan.md`, and `results/swarm/falsifier.md` already favored H1 on novelty-to-falsifiability grounds; the new fact does not change that ordering, it removes H1's biggest blocker. With the 2025 frontier paper now recovered directly, H1 no longer depends on a hypothetical seed source: it has an actual compact seed anchor, including `q:(83,2,81,1)` and the compact run-length encoding for `s`. That makes H1 the only branch that is simultaneously tied to the real order-668 frontier artifact, narrow enough to defend against prior-art overlap, and paired with a clean seed-matched kill test.

The concept-evolution pass does not overturn this. `results/concept_evolve/evolve_results.json` and `results/concept_evolve/tree/index.json` show a widened tree of 11 concepts, but the indexed alternatives still map to the same ordering logic: H2 is the best fallback if locality fails, and H3 remains the most radical but least frontier-anchored option. `results/literature/literature_snapshot.json` now explicitly treats the recovered 2025 paper as the frontier anchor that supplies the published q/s seed and the defect profile needed for H1, while `sources.bib` already contains the frontier paper plus the relevant annealing, QAOA, SAT+CAS, and CA-adjacent comparators. There is no new evidence here that promotes H2 or H3 above H1.

What changes is blocker language. The old blocker in `results/swarm/director_brief.md` should be considered superseded. The remaining prerequisites are narrower: canonicalize the recovered seed under standard symmetries, verify the coordinate system induced by the published compact encoding, and run the seed-matched benchmark harness. That is an execution prerequisite, not a branch-selection blocker.

## Exact `selection_note` Text

```md
Select `H1_defect_syndrome_ca_64m` as the initial branch. The recovered 2025 frontier paper removes H1's main blocker by supplying an actual compact order-668 seed (`q:(83,2,81,1)` plus the published compact run-length encoding for `s`), so this branch is now directly executable rather than hypothetical. H1 still has the best novelty-to-falsifiability tradeoff because it is the most tightly anchored to the real order-668 frontier object and has the cleanest first kill test: from the same canonicalized seed and in the same compressed coordinates, a genuinely local CA repair dynamic must beat matched greedy, tabu, simulated annealing, and same-coordinate non-CA repair on exact-feasibility outcomes. Keep the claim narrow: this is a seeded repair heuristic for the open real order-668 case, not a general CA Hadamard-construction claim, and nothing counts as solving Hadamard 668 unless exact orthogonality is reached up to standard equivalence. If H1 fails because locality is false rather than because the implementation is weak, move next to `H2_lag_space_ca_167`; keep `H3_spacetime_row_emission_ca` in reserve.
```

## Boundaries To Preserve

- Preserve the novelty boundary: do not claim CA is new for Hadamard matrices in general. The defensible claim stays narrow, as already framed in the swarm brief and falsifier memo: CA as a seeded repair dynamic on the recovered order-668 frontier object.
- Preserve the exactness boundary: better defect traces, fewer residual Gram errors, or improved modular statistics are not a solution to Hadamard 668. Exact orthogonality up to standard equivalence remains the only success gate.
- Preserve the method-identity boundary: if H1 requires dense global recomputation every step or behaves as ordinary full-matrix energy descent, the CA claim collapses toward rebranded local search. The state and updates must stay genuinely local in the claimed compressed representation.
- Preserve the fairness boundary: comparisons must remain seed-matched, representation-matched, and budget-matched against greedy, tabu, simulated annealing, and same-coordinate non-CA local search.
- Preserve the family-leakage boundary on fallback branches: if H2 only works by collapsing into Williamson, Turyn, Goethals-Seidel, cocyclic, block-circulant, or related known families, relabel it as optimizer-over-known-family rather than a new branch.
- Preserve the routing boundary: do not widen into random-start full `668 x 668` CA, broad family sweeps, or speculative generative-rule searches before H1 survives the first seeded kill test.

## Bottom Line

The reassessment is affirmative: H1 remains champion, more decisively than before, because the recovered frontier paper converts its main blocker from "missing seed" into "seed ready for canonicalization and benchmark setup." The branch order does not change. The language discipline also does not change.
