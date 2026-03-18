# Prior Art Gap Analysis

Update this file throughout the run. If you discover a branch that is already well-covered by prior work, document it here and pivot rather than repeating it.

## 1. Cellular Automata Applications in Shortest Path Problem (2017)
- Paper ID: 4b85674750c1ad93a8d26427e52e7bec82d7e392
- Why it is close: It is genuine prior art for using cellular automata as a local propagation / optimization heuristic on a hard combinatorial problem, so it weakens any broad claim that "CA for search is new."
- Differentiation hypothesis: H1 is not a grid shortest-path CA and not a generic CA-for-optimization claim. The intended state is the recovered order-668 defect/correlation field attached to the published `64`-modular seed, with exact orthogonality as the gate and matched non-CA repair baselines as the comparator.
- Evidence artifact(s): `results/problem_statement.md`; `results/swarm/selection_note.md`; `results/swarm/director_reassessment.md`; `results/swarm/explorer_alignment_note.md`; `results/literature/code_watchlist.md`; `results/branches/H1_defect_syndrome_ca_64m.md`; `results/branches/H1_precheck.md`; `results/verification/novelty_precheck.md`.
- Pivot decision (if any): Keep H1, but keep the novelty claim narrow: seeded CA repair on the real order-668 frontier object, not CA optimization in general.

## 2. Learning Automata-Based Solutions to the Single Elevator Problem (2019)
- Paper ID: 74159b79e948de4dd6fab33ecd01d4a0c96a51c5
- Why it is close: The initial watchlist pulled it in because it is an automata-based optimization paper, so it is a useful check against over-broad "automata are untried here" language.
- Differentiation hypothesis: This is learning-automata scheduling, not cellular automata, not combinatorial-design search, and not an exact-search method over a recovered order-668 seed. Its overlap is lexical and methodological only at the most generic level.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/problem_statement.md`; `results/swarm/explorer_alignment_note.md`; `results/verification/novelty_precheck.md`; `sources.bib`.
- Pivot decision (if any): Treat as a watchlist false positive for branch novelty. Keep it in the file only as a reminder not to confuse learning automata with cellular automata.

## 3. On the possibility of oscillating in the Ebola virus dynamics and investigating the effect of the lifetime of T lymphocytes (2022)
- Paper ID: 4c744f3e519204bac75f7a99661bbe3491393fc1
- Why it is close: It surfaced only because the early lexical watchlist over-weighted the token `automata`.
- Differentiation hypothesis: This is a biomedical dynamics paper with no meaningful overlap in state representation, objective, verification style, or search method. It is not prior art for Hadamard search or CA repair.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/swarm/explorer_alignment_note.md`; `results/verification/novelty_precheck.md`; `sources.bib`.
- Pivot decision (if any): Mark as pure query-noise false positive; no branch pivot is needed.

## 4. Engineering Societies in the Agents World (2000)
- Paper ID: 094836f18350868a0b8cfe57a127906496120841
- Why it is close: It appeared because the initial search also drifted into agent-system language, which can superficially resemble distributed-update rhetoric.
- Differentiation hypothesis: The paper is about multi-agent systems, not cellular automata, not Hadamard matrices, and not exact combinatorial search from a known near-solution.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/swarm/explorer_alignment_note.md`; `results/branches/H3_gate.md`; `results/verification/novelty_precheck.md`; `sources.bib`.
- Pivot decision (if any): Mark as false positive; do not use agent-society metaphors as evidence of novelty for the CA branch.

## 5. Learning Automata-Based Solutions to the Multi-Elevator Problem (2019)
- Paper ID: 9a8e718e861bc6a07be3b5cee1fa506c7f413b3d
- Why it is close: Same generic overlap as the single-elevator paper: automata-based optimization on a structured control problem.
- Differentiation hypothesis: It is learning-automata scheduling, not cellular-automaton defect repair on a compressed Hadamard seed representation.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`; `results/literature/literature_snapshot.json`; `results/swarm/explorer_alignment_note.md`.
- Pivot decision (if any): Keep as a named false positive and do not treat it as blocking novelty for H1.

## 6. A 64-Modular Hadamard Matrix of Order 668 (2025)
- Paper ID: unavailable in current Semantic Scholar results; tracked manually in `sources.bib` as `eliahou2025_64mod668`
- Why it is close: This is the true frontier anchor. Any order-668 search that starts from the compact `q` / `s` seed or from the published residual defect pattern is operating directly on top of this result.
- Differentiation hypothesis: The frontier paper is not CA prior art and does not claim an exact Hadamard matrix. It constructs a `64`-modular near-solution with 13 nonzero correlation coefficients (equivalently 26 nonzero off-diagonal Gram defects per row). The present branch uses that recovered object only as a canonical seed for exact-search repair and compares CA against matched non-CA controls in the same compressed coordinates.
- Evidence artifact(s): `results/problem_statement.md`; `results/swarm/selection_note.md`; `results/swarm/director_reassessment.md`; `results/literature/literature_snapshot.json`; `results/branches/H1_defect_syndrome_ca_64m.md`; `results/branches/H1_precheck.md`; `results/branches/H1_frontier_micro_smoke.json`; `results/branches/H1_frontier_sensitivity_probe.json`; `results/concept_evolve/probe_result.json`; `results/verification/novelty_precheck.md`; `sources.bib`.
- Pivot decision (if any): Keep as the frontier anchor and benchmark source. Do not overclaim seed recovery or modular improvement itself as CA progress.
