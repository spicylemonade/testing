# Prior Art Gap Analysis

Update this file throughout the run. If you discover a branch that is already well-covered by prior work, document it here and pivot rather than repeating it.

## 1. Cellular Automata Applications in Shortest Path Problem (2017)
- Paper ID: 4b85674750c1ad93a8d26427e52e7bec82d7e392
- Why it is close: It is genuine prior art for using cellular automata as a local propagation / optimization heuristic on a hard combinatorial problem, so it weakens any broad claim that "CA for search is new."
- Differentiation hypothesis: H1 is not a grid shortest-path CA and not a generic CA-for-optimization claim. The intended state is the recovered order-668 defect/correlation field attached to the published `64`-modular seed, with exact orthogonality as the gate and matched non-CA repair baselines as the comparator.
- Evidence artifact(s): `results/swarm/selection_note.md`; `results/swarm/director_reassessment.md`; `results/swarm/explorer_alignment_note.md`; `results/branches/H1_defect_syndrome_ca_64m.md`; `results/branches/H1_precheck.md`; `results/experiments/order_668_64m/summary.md`; `results/verification/novelty_report.md`; `results/verification/citation_audit.md`; `results/verification/benchmark_report.md`.
- Pivot decision (if any): Keep this paper as the strongest CA-shape warning, but the executed H1 branch no longer survives as a new CA repair method. After the first frontier kill test, the honest move is to retire H1 and pivot to H2 under a narrower locality claim.

## 2. Learning Automata-Based Solutions to the Single Elevator Problem (2019)
- Paper ID: 74159b79e948de4dd6fab33ecd01d4a0c96a51c5
- Why it is close: The initial watchlist pulled it in because it is an automata-based optimization paper, so it is a useful check against over-broad "automata are untried here" language.
- Differentiation hypothesis: This is learning-automata scheduling, not cellular automata, not combinatorial-design search, and not an exact-search method over a recovered order-668 seed. Its overlap is lexical and methodological only at the most generic level.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/swarm/explorer_alignment_note.md`; `results/verification/novelty_report.md`; `results/verification/citation_audit.md`; `sources.bib`.
- Pivot decision (if any): Keep as a language-discipline false positive only. Do not use it for detailed paraphrase until the metadata mismatch noted in `results/verification/citation_audit.md` is revalidated.

## 3. On the possibility of oscillating in the Ebola virus dynamics and investigating the effect of the lifetime of T lymphocytes (2022)
- Paper ID: 4c744f3e519204bac75f7a99661bbe3491393fc1
- Why it is close: It surfaced only because the early lexical watchlist over-weighted the token `automata`.
- Differentiation hypothesis: This is a biomedical dynamics paper with no meaningful overlap in state representation, objective, verification style, or search method. It is not prior art for Hadamard search or CA repair.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/swarm/explorer_alignment_note.md`; `results/verification/novelty_report.md`; `results/verification/citation_audit.md`; `sources.bib`.
- Pivot decision (if any): Mark as pure query-noise false positive; no branch pivot is needed.

## 4. Engineering Societies in the Agents World (2000)
- Paper ID: 094836f18350868a0b8cfe57a127906496120841
- Why it is close: It appeared because the initial search also drifted into agent-system language, which can superficially resemble distributed-update rhetoric.
- Differentiation hypothesis: The paper is about multi-agent systems, not cellular automata, not Hadamard matrices, and not exact combinatorial search from a known near-solution.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/swarm/explorer_alignment_note.md`; `results/branches/H3_gate.md`; `results/verification/novelty_report.md`; `results/verification/citation_audit.md`; `sources.bib`.
- Pivot decision (if any): Mark as false positive; do not use agent-society metaphors as evidence of novelty for the CA branch.

## 5. Learning Automata-Based Solutions to the Multi-Elevator Problem (2019)
- Paper ID: 9a8e718e861bc6a07be3b5cee1fa506c7f413b3d
- Why it is close: Same generic overlap as the single-elevator paper: automata-based optimization on a structured control problem.
- Differentiation hypothesis: It is learning-automata scheduling, not cellular-automaton defect repair on a compressed Hadamard seed representation.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`; `results/literature/literature_snapshot.json`; `results/swarm/explorer_alignment_note.md`; `results/verification/citation_audit.md`.
- Pivot decision (if any): Keep as a named false positive only. It is not in `sources.bib`, so do not let it carry any citation-bearing novelty claim.

## 6. A 64-Modular Hadamard Matrix of Order 668 (2025)
- Paper ID: unavailable in current Semantic Scholar results; tracked manually in `sources.bib` as `eliahou2025_64mod668`
- Why it is close: This is the true frontier anchor. Any order-668 search that starts from the compact `q` / `s` seed or from the published residual defect pattern is operating directly on top of this result.
- Differentiation hypothesis: The frontier paper is not CA prior art and does not claim an exact Hadamard matrix. It constructs a `64`-modular near-solution with 13 nonzero correlation coefficients (equivalently 26 nonzero off-diagonal Gram defects per row). The present branch uses that recovered object only as a canonical seed for exact-search repair and compares CA against matched non-CA controls in the same compressed coordinates.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/branches/H1_defect_syndrome_ca_64m.md`; `results/branches/H1_precheck.md`; `results/concept_evolve/probe_result.json`; `results/experiments/order_668_64m/summary.md`; `results/verification/novelty_report.md`; `results/verification/benchmark_report.md`; `results/verification/verification_summary.md`; `sources.bib`.
- Pivot decision (if any): Keep as the frontier anchor and benchmark source. The executed H1 branch now collapses to a tested optimizer / falsification attempt on top of this seed rather than a surviving new CA repair method. Any renewed novelty claim must come from H2 or a representation-changing bridge that survives matched controls and leakage audits.

## 7. Finding a Hadamard Matrix by Simulated Quantum Annealing (2018)
- Paper ID: d98246df005a52ff9a5e99b6c5f548c1def1ba12
- Why it is close: It is a direct Hadamard-search baseline in the same broad heuristic family as the in-repo `simulated_annealing` comparator.
- Differentiation hypothesis: The current run is much narrower: one seed-matched frontier falsification scaffold rather than a general annealing program. The intended distinct claim was locality-driven CA repair, not generic energy minimization.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/analysis/prior_work_comparison.md`; `results/verification/benchmark_report.md`; `results/verification/citation_audit.md`; `sources.bib`.
- Pivot decision (if any): Keep as a strong non-CA comparator. The current H1 branch does not outperform the matched annealing-style baseline strongly enough to justify continuation.

## 8. Finding Hadamard Matrices by a Quantum Annealing Machine (2019)
- Paper ID: c42e6a8a231cd8cd638ff953b6aa7b539c4596e9
- Why it is close: It is another direct Hadamard-search optimizer baseline and therefore a useful guardrail against overclaiming benchmark significance.
- Differentiation hypothesis: The present run is a seed-matched branch gate on the published order-668 frontier object, not a hardware-level or general-purpose annealing claim.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/analysis/prior_work_comparison.md`; `results/verification/benchmark_report.md`; `results/verification/citation_audit.md`; `sources.bib`.
- Pivot decision (if any): Keep as literature context only. Do not claim competitiveness with this line of work from the current pilot budget.

## 9. The SAT+CAS method for combinatorial search with applications to best matrices (2019)
- Paper ID: 74aeec834364032b323d56b8a1c03c798fcd2844
- Why it is close: It represents certificate-rich exact combinatorial search, which is the strongest contrast case for what the current CA branch is not.
- Differentiation hypothesis: The current run is heuristic, seed-matched, and non-certifying. Its role is branch elimination, not proof-producing exact search.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/analysis/prior_work_comparison.md`; `results/verification/benchmark_report.md`; `results/verification/citation_audit.md`; `sources.bib`.
- Pivot decision (if any): Keep as the certification benchmark. The current H1 branch falls well short of this standard and should not be described as an exact-search method contribution.

## 10. Douglas-Rachford feasibility methods for matrix completion problems (2013)
- Paper ID: 57fca051597c048ba77b11e9efcafd5741ea4dbc
- Why it is close: It is a non-CA feasibility/search baseline for matrix-style completion problems and therefore a useful comparator for seed dependence and convergence style.
- Differentiation hypothesis: The current run is more local and more frontier-seed-dependent, but also much weaker on convergence guarantees and feasibility theory.
- Evidence artifact(s): `results/literature/literature_snapshot.json`; `results/analysis/prior_work_comparison.md`; `sources.bib`.
- Pivot decision (if any): Keep as a feasibility comparator only. The present CA work should not borrow convergence language from this line of work.

## 11. Current novelty status
- Status note: the executed H1 branch does **not** remain a new CA repair method after the first matched frontier batch.
- Honest interpretation: it collapses to a well-documented seeded optimizer / falsification attempt over the published order-668 frontier object.
- Remaining opening: H2 and the promoted representation-changing bridges (`lag_residue_ca_167`, decoder-graph / influence-graph variants) may still recover a distinct claim, but only if they survive matched controls and the family-leakage audit.
