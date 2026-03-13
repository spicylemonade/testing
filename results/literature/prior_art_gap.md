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
- Why it is close:
- Differentiation hypothesis:
- Evidence artifact(s):
- Pivot decision (if any):

## 2. Leveraging polygenic functional enrichment to improve GWAS power (2017)
- Paper ID: 28b910931f8d5c4a24b96b543e2f8b02b347dc40
- Why it is close:
- Differentiation hypothesis:
- Evidence artifact(s):
- Pivot decision (if any):

## 3. Using Simulation and Domain Adaptation to Improve Efficiency of Deep Robotic Grasping (2018)
- Paper ID: 6ebdf55cade577979515dc5d09620204a07e7c92
- Why it is close:
- Differentiation hypothesis:
- Evidence artifact(s):
- Pivot decision (if any):

## 4. The EPR effect and beyond: Strategies to improve tumor targeting and cancer nanomedicine treatment efficacy (2020)
- Paper ID: 6c2403053bfd486f14eaa9022b91696d2de6b55e
- Why it is close:
- Differentiation hypothesis:
- Evidence artifact(s):
- Pivot decision (if any):

## 5. Automatic Number Plate Recognition (2024)
- Paper ID: 0a14c36b2b42caaf3f91645c0a19fd33484fa31a
- Why it is close:
- Differentiation hypothesis:
- Evidence artifact(s):
- Pivot decision (if any):
