# Prior Art Gap Analysis

Update this file throughout the run. If you discover a branch that is already well-covered by prior work, document it here and pivot rather than repeating it.

## Ramsey-Specific Overlap Notes (2026-03-13)
- Branch: Plain evolutionary / GA / generic metaheuristic lower-bound search.
- Why it is already covered: This overlaps with Exoo-style computational search, `Can genetic algorithms with the symmetric heuristic find the Ramsey number R(5,5)`, later statistical-physics framing of Ramsey lower bounds, and more recent RL-style graph generation work.
- Differentiation hypothesis: Keep only a rare-event bridge that learns the defect landscape of near-miss colorings and uses multicanonical or population-annealed sampling rather than polishing another direct optimizer.
- Evidence artifact(s): `results/literature/gap_probe_1.json`, targeted web checks on Ramsey lower-bound search papers.
- Pivot decision (if any): Do not propose plain GA, hill-climbing, or RL search as a standalone hypothesis.

- Branch: Plain LP / flag-algebra / generic SDP tightening for the upper bound.
- Why it is already covered: This overlaps with McKay-Radziszowski, Angeltveit-McKay `R(5,5) <= 48`, the newer `R(5,5) <= 46` case-checking line, and prior SDP/flag-algebra applications to Ramsey numbers.
- Differentiation hypothesis: Pivot to a finite-`n` rigidity program that imports coding-theory association-scheme block diagonalization (Terwilliger-style) so exact checking is only the last residue step.
- Evidence artifact(s): `results/literature/gap_probe_1.json`, `results/literature/literature_graph.json`, targeted web checks on the 2024 `R(5,5) <= 46` preprint and SDP/coding references.
- Pivot decision (if any): Do not propose "more LP" or "more generic flag algebra" as the main novelty claim.

- Branch: Plain SAT / cube-and-conquer / static symmetry-breaking search.
- Why it is already covered: SAT proof logging and verified certificates already exist for nearby exact problems (`Schur Number Five`) and for recent certified Ramsey computations.
- Differentiation hypothesis: Pivot to IC3/PDR or CEGAR-style invariant learning on orbit quotients so each UNSAT core blocks a whole family of partial colorings online.
- Evidence artifact(s): targeted web checks on proof-logging and SAT+CAS Ramsey verification papers.
- Pivot decision (if any): Do not propose a vanilla SAT encoding without an invariant-learning layer.

## 1. Senolytics Improve Physical Function and Increase Lifespan in Old Age (2018)
- Paper ID: 918fb15a620d71230dc7ee961c0c2cfce924e9a7
- Why it is close: It is not mathematically close. It appeared only because the original lexical query over-weighted the words `improve` and `number`.
- Differentiation hypothesis: Treat it as a watchlist false positive that proves the seed search was noisy; it contributes no substantive prior art to Ramsey computation.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`, `results/literature/novelty_guard.json`, `results/literature/literature_snapshot.json`.
- Pivot decision (if any): Exclude from the actual Ramsey bibliography except as a novelty-guard example of lexical query noise.

## 2. Leveraging polygenic functional enrichment to improve GWAS power (2017)
- Paper ID: 28b910931f8d5c4a24b96b543e2f8b02b347dc40
- Why it is close: It is not domain-close. It entered the watchlist because the query matched generic improvement language instead of Ramsey-specific combinatorics.
- Differentiation hypothesis: Keep only the meta-lesson that broad lexical searches can hallucinate relevance; do not use it as methodological or evaluative prior art.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`, `results/literature/novelty_guard.json`.
- Pivot decision (if any): Exclude from candidate baselines and route selection.

## 3. Using Simulation and Domain Adaptation to Improve Efficiency of Deep Robotic Grasping (2018)
- Paper ID: 6ebdf55cade577979515dc5d09620204a07e7c92
- Why it is close: The only plausible overlap is abstract workflow shape: simulated search data plus adaptation. It is still not actual Ramsey prior art.
- Differentiation hypothesis: If any transfer survives, it is only at the level of proof/data reuse, not robotics or domain adaptation itself. No claim in this run relies on robotic-grasping methods.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`, `results/literature/novelty_guard.json`, `results/plans/ramsey_research_program.md`.
- Pivot decision (if any): Do not cite this as a close scientific predecessor; use it only as a reminder not to mistake imported method names for novelty.

## 4. The EPR effect and beyond: Strategies to improve tumor targeting and cancer nanomedicine treatment efficacy (2020)
- Paper ID: 6c2403053bfd486f14eaa9022b91696d2de6b55e
- Why it is close: It is another lexical false positive driven by `improve` rather than any Ramsey overlap.
- Differentiation hypothesis: None beyond documenting the query-noise failure mode.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`, `results/literature/novelty_guard.json`.
- Pivot decision (if any): Exclude from substantive prior-art comparison.

## 5. Automatic Number Plate Recognition (2024)
- Paper ID: 0a14c36b2b42caaf3f91645c0a19fd33484fa31a
- Why it is close: It is not close at all; `number` in the task string matched `number plate`.
- Differentiation hypothesis: None. Its value is only diagnostic: the lexical watchlist must be filtered before any novelty judgment.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`, `results/literature/novelty_guard.json`.
- Pivot decision (if any): Exclude from the real bibliography and baseline set.

## 6. Study of Exoo's Lower Bound for Ramsey number R(5,5) (2022)
- Paper ID: 3731e1a2fd6dfaefa5166c772b2b48149fe1bed0
- Why it is close: This is the closest lower-bound structural paper in the saved artifact set. It re-verifies Exoo's `R(5,5) >= 43` construction and studies low-defect `K_43` variants.
- Differentiation hypothesis: `H1` is not another verification of a known witness and not another low-defect search note. It claims a reusable obstruction atlas for why diverse `42 -> 43` extensions fail, with transfer and witness-safety obligations across parent families.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/hypotheses.json`, `results/swarm/director_brief.md`.
- Pivot decision (if any): Keep as the closest lower-bound overlap and benchmark against it directly.

## 7. Can genetic algorithms with the symmetric heuristic find the Ramsey number R(5,5) (2010)
- Paper ID: 64a7aff133af1ebd2fbeffd7de7b654cd495c9dd
- Why it is close: It is the named overlap point for any plain GA/symmetric-heuristic claim on `R(5,5)`.
- Differentiation hypothesis: The current route does not claim novelty from a better optimizer, better symmetry handling, or better defect minimization. The novelty claim lives in transferable minimal obstruction cores, not in the search trajectory.
- Evidence artifact(s): `results/literature/gap_probe_1.json`, `results/swarm/falsifier.md`, `results/plans/ramsey_research_program.md`.
- Pivot decision (if any): Kill any branch that collapses into optimizer-only improvement.

## 8. A new upper bound on the Ramsey number R(5,5) (1992)
- Paper ID: 160081e3e1f57e3478499da04264f84564db90f2
- Why it is close: It is the foundational upper-bound case-analysis line for modern `R(5,5)` computation.
- Differentiation hypothesis: `H1` differs by extracting reusable failure objects from extensions rather than directly enlarging the old case split. `H2` is allowed only if it changes the decomposition primitive itself and beats the old line on residue/proof metrics under matched conditions.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/hypotheses.json`, `results/swarm/tool_plan.md`.
- Pivot decision (if any): Keep as the upper-bound baseline ancestor; do not present a stronger engine on the same object as a novelty claim.

## 9. R(5,5) <= 48 (2018)
- Paper ID: a9604442aea6ca62ee3cf6ff83d0f281d6afeb83
- Why it is close: This is the direct predecessor to the current `<= 46` line and the natural comparison point for exact upper-bound improvements.
- Differentiation hypothesis: A credible successor must either tighten the exact frontier or change the verified proof object. Smaller raw residues or faster SAT without certificate impact are not enough.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/falsifier.md`, `results/plans/ramsey_research_program.md`.
- Pivot decision (if any): Use as a baseline in every upper-bound comparison table.

## 10. R(5,5) <= 46 (2024)
- Paper ID: arxiv:2409.15709
- Why it is close: This is the current best published upper bound and therefore the main frontier overlap.
- Differentiation hypothesis: `H1` differs because it is not a larger LP-plus-case-checking run. It seeks a transferable obstruction atlas that can become both pruning logic and proof-grade lemmas. `H2` differs only if it replaces the decomposition primitive rather than strengthening the same split/gluing machinery.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/gap_map.md`, `results/swarm/director_brief.md`, `results/swarm/falsifier.md`.
- Pivot decision (if any): Treat this as the current source of truth for upper-bound benchmarking.

## 11. Decreasing the upper bound on the Ramsey number R(5,5) (2025)
- Paper ID: acmdl:3727993.3728010
- Why it is close: This is the closest direct overlap for the `H2` family because it explicitly advances the split-vertex/transverse-edge gluing line.
- Differentiation hypothesis: Any surviving `H2` claim must demonstrate a new decomposition primitive or a better proof object under matched certificate metrics. Otherwise it is just the Gauthier line with a stronger engine.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/director_brief.md`, `results/swarm/hypotheses.json`, `results/swarm/falsifier.md`.
- Pivot decision (if any): Keep `H2` in reserve and do not promote it unless `H1` fails and the decomposition change is real.
