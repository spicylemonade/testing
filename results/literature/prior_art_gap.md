# Prior Art Gap Analysis

Update this file throughout the run. If a branch is already covered by existing work, document the overlap here and pivot instead of polishing a derivative story.

## Run Notes

- The auto-generated watchlist for this task is malformed. Its highest-ranked matches are largely LaTeX-token collisions rather than topic-aware neighbors.
- The current director brief is present and authoritative. Older notes claiming it is absent are stale.
- The only defensible novelty target in the current run is methodological: a verifier-coupled CA search procedure over the product-grid witness representation. It is not a new arithmetic-Kakeya theorem unless exact verified witnesses are produced.
- The missing exact verifier remains the dominant blocker. Until that is resolved, all novelty claims stay at the level of design and audit, not mathematical progress.

## False Overlaps From The Malformed Watchlist

### 1. `2x2-Convexifications for convex quadratic optimization with indicator variables` (2023)
- Overlap type: superficial token collision only.
- Why it appeared: the seed query was polluted by LaTeX tokens such as `mathbf`, `times`, and `then`.
- Differentiation hypothesis: no mathematical, algorithmic, or methodological overlap with arithmetic Kakeya or CA-guided witness search.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`, `results/literature/literature_snapshot.json`.
- Pivot decision: treat as false overlap; do not use as prior art beyond documenting watchlist failure.

### 2. `On Hopf hypersurfaces of the homogeneous nearly Kähler S^3 x S^3` (2019)
- Overlap type: superficial token collision only.
- Why it appeared: shared formatting tokens around products and bold math, not shared problem structure.
- Differentiation hypothesis: unrelated differential-geometry paper; no relevant overlap with arithmetic projections, forcing pairs, or CA search.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`, `results/context_sync.md`.
- Pivot decision: false overlap; exclude from real adjacent-literature reasoning.

### 3. `Continued A_2-fractions and singular functions` (2022)
- Overlap type: superficial token collision only.
- Why it appeared: token overlap on `finite` and LaTeX fragments rather than on Kakeya or additive-combinatorics content.
- Differentiation hypothesis: unrelated number-theoretic topic; no meaningful overlap with the present lane.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`, `results/context_sync.md`.
- Pivot decision: false overlap; retain only as evidence that the initial watchlist is unreliable.

### 4. `mu-Hybrid Inflation and Metastable Cosmic Strings ...` (2025)
- Overlap type: superficial token collision only.
- Why it appeared: shared math formatting around products and bold symbols.
- Differentiation hypothesis: no overlap with arithmetic Kakeya mathematics or CA witness search.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`.
- Pivot decision: false overlap; ignore for novelty analysis.

### 5. `First measurement of the |t|-dependence of coherent J/psi photonuclear production` (2021)
- Overlap type: superficial token collision only.
- Why it appeared: malformed token retrieval, not scientific relevance.
- Differentiation hypothesis: no overlap with the present task.
- Evidence artifact(s): `results/literature/prior_art_watchlist.md`.
- Pivot decision: false overlap; ignore for novelty analysis.

## Real Adjacent Literature

### Katz-Tao (1999): `Bounds on arithmetic projections, and applications to the Kakeya conjecture`
- Overlap type: mathematical direct.
- Why it is close: this is the foundational arithmetic-projection framework underlying the present witness problem.
- Differentiation hypothesis: a CA-based contribution would only be different if it discovers or organizes legal witnesses more effectively; it is not different merely because the search loop is automated.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/director_brief.md`.
- Pivot decision: every proposed method must compile back to the original six-line witness and exact score, or it is not progress on Katz-Tao's formulation.

### Green-Ruzsa (2017): `On the arithmetic Kakeya conjecture of Katz and Tao`
- Overlap type: mathematical direct, with finite-field caution.
- Why it is close: it studies the arithmetic Kakeya conjecture itself and highlights the finite-field variant.
- Differentiation hypothesis: modular or finite-field CA behavior is not enough. Any curriculum over finite alphabets must lift back to exact integer witnesses.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/falsifier.md`.
- Pivot decision: reject any branch whose apparent gain exists only modulo `p` or `N`.

### Cowen-Breen, Karangozishvili, Varadarajan, Wang (2020): `Pattern Problems related to the Arithmetic Kakeya Conjecture`
- Overlap type: mathematical adjacent.
- Why it is close: it maps nearby pattern and homothet formulations that are equivalent or tightly related to arithmetic Kakeya.
- Differentiation hypothesis: a CA objective must not silently optimize a denser adjacent pattern task while claiming progress on forcing pairs.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/falsifier.md`.
- Pivot decision: keep the target on exact `(X,G,R,T)` witnesses rather than pattern proxies.

### Pohoata-Zakharov (2024): `Generalized Arithmetic Kakeya`
- Overlap type: mathematical adjacent.
- Why it is close: it broadens the arithmetic-Kakeya landscape and shows that formulation changes can create apparent progress.
- Differentiation hypothesis: the current lane is only novel if it feeds back into the original forcing-pair problem, not merely a generalized reformulation.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/gap_map.md`.
- Pivot decision: treat generalized formulations as adjacency checks, not as substitutes for the target verifier.

### Tao (2025): `Sum-difference exponents for boundedly many slopes, and rational complexity`
- Overlap type: mathematical direct warning.
- Why it is close: it is the sharpest current warning against bounded-slope or low-rational-complexity stories.
- Differentiation hypothesis: a small fixed CA alphabet is at high risk of rediscovering exactly the low-complexity regime Tao warns about.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/falsifier.md`, `results/swarm/director_brief.md`.
- Pivot decision: reject branches that only work for tiny fixed `X` or boundedly many slopes.

### Hickman-Wright (2018): `The Fourier restriction and Kakeya problems over rings of integers modulo N`
- Overlap type: mathematical adjacent.
- Why it is close: it is the main modular/ring analogue relevant to any finite-state automaton curriculum.
- Differentiation hypothesis: modular success can be used as a curriculum signal only if there is a deterministic and honest lift back to `\mathbb{Z}`.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/gap_map.md`.
- Pivot decision: modular-only wins do not count.

### Bond-Levine (2013): `Abelian Networks I. Foundations and Examples`
- Overlap type: methodological adjacent.
- Why it is close: it supplies a rigorous local-processing framework that could inform proof-carrying or abelian-network interpretations of forcing.
- Differentiation hypothesis: the current lane is not an abelian-network result unless it proves that such invariants predict or generate lower verified scores.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/hypothesis_bridge.md`.
- Pivot decision: use only as an adjacent structural bridge, not as a novelty claim on its own.

### Bond-Levine (2014): `Abelian networks II: halting on all inputs`
- Overlap type: methodological adjacent.
- Why it is close: it strengthens the local-dynamics bridge with rigorous halting criteria.
- Differentiation hypothesis: unless halting or production-matrix structure predicts exact forcing, the overlap remains only analogical.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/hypothesis_bridge.md`.
- Pivot decision: keep as a reserve bridge, not the main claim.

### Dennunzio-Formenti-Margara (2023): `An Easy to Check Characterization of Positive Expansivity for Additive Cellular Automata Over a Finite Abelian Group`
- Overlap type: methodological adjacent.
- Why it is close: it is a precise CA-theory anchor for additive local rules over finite abelian alphabets.
- Differentiation hypothesis: citing additive-CA structure is only useful if the CA state remains proof-aware and verifier-coupled; otherwise it is just standard CA machinery.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/falsifier.md`.
- Pivot decision: use as CA-method background, not as evidence of arithmetic-Kakeya progress.

### Faldor-Cully (2024): `Toward Artificial Open-Ended Evolution within Lenia using Quality-Diversity`
- Overlap type: methodological adjacent.
- Why it is close: it is a relevant search-method baseline for diversity-driven CA exploration.
- Differentiation hypothesis: a quality-diversity engine alone is not novel here; novelty would have to come from the exact witness compiler and verifier-coupled objective.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/gap_map.md`.
- Pivot decision: use only as a benchmark-search reference.

### Novikov et al. (2025): `AlphaEvolve: A coding agent for scientific and algorithmic discovery`
- Overlap type: methodological/system reference.
- Why it is close: it is the clearest prior example of automated open-problem search with coding agents.
- Differentiation hypothesis: if the present work is merely automated search over witness encodings, it collapses into AlphaEvolve-style overlap.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/swarm/falsifier.md`.
- Pivot decision: any novelty claim must rest on verifier-coupled witness structure, not on automation alone.

### Georgiev, Gomez-Serrano, Tao, Wagner (2025): `Mathematical exploration and discovery at scale`
- Overlap type: methodological/system reference.
- Why it is close: it broadens the automated-discovery comparison class beyond one system.
- Differentiation hypothesis: the current lane must contribute a domain-specific exact-decoding discipline, not just a large-scale exploration loop.
- Evidence artifact(s): `results/literature/literature_snapshot.json`, `results/context_sync.md`.
- Pivot decision: treat as a novelty floor for any AI-assisted search claim.

## Current Bottom Line

- The watchlist overlaps are mostly false.
- The real prior-art pressure comes from:
  - exact arithmetic-Kakeya papers that constrain what counts as genuine mathematical progress, and
  - CA / automated-search papers that constrain what counts as genuine methodological novelty.
- The present lane remains viable only as a verifier-coupled search-and-design program. Without an exact verifier, it cannot graduate from design novelty to mathematical evidence.

## Phase 3 Design Checkpoint: H1-Specific Differentiation

This checkpoint records how the current `H1` design in `results/core/h1_design.md` clears, or fails to clear, the strongest real adjacent work.

### Katz-Tao (1999): `Bounds on arithmetic projections, and applications to the Kakeya conjecture`
- Overlap type: mathematical direct.
- Phase-3 differentiation: `H1` does not claim a new reformulation or theorem. Its only admissible distinction is methodological: every CA state must decode directly into the original six-line witness over the Katz-Tao arithmetic-projection object, with no repair and no proxy objective.
- Failure mode if ignored: a flat CA over images or adjacency patterns would stop being progress on Katz-Tao's witness problem and become an unrelated heuristic search.

### Green-Ruzsa (2017): `On the arithmetic Kakeya conjecture of Katz and Tao`
- Overlap type: mathematical direct.
- Phase-3 differentiation: `H1` explicitly treats modular or finite-field behavior as non-evidence. The stage-indexed fiber layout and decoder contract require an integer witness over `\mathbb{Z}`, not just a finite-field shadow.
- Failure mode if ignored: the lane collapses into a modular curriculum story that does not meet the arithmetic-Kakeya target.

### Cowen-Breen, Karangozishvili, Varadarajan, Wang (2020): `Pattern Problems related to the Arithmetic Kakeya Conjecture`
- Overlap type: mathematical adjacent.
- Phase-3 differentiation: `H1` is constrained to decode into forcing pairs `(X,G,R,T)` rather than any denser pattern-count, homothety, or proxy configuration. The fixed decoder and no-repair rule are what keep the lane from drifting into nearby pattern problems.
- Failure mode if ignored: a CA could optimize a friendlier adjacent pattern objective and be misreported as arithmetic-Kakeya progress.

### Pohoata-Zakharov (2024): `Generalized Arithmetic Kakeya`
- Overlap type: mathematical adjacent.
- Phase-3 differentiation: `H1` uses generalized formulations only as stress tests for false transfer, never as substitute targets. The current design is novel only if any future gain lands back in the original witness format.
- Failure mode if ignored: the project could overclaim on a generalized formulation without improving the stated forcing-pair problem.

### Tao (2025): `Sum-difference exponents for boundedly many slopes, and rational complexity`
- Overlap type: mathematical direct warning.
- Phase-3 differentiation: `H1` keeps `X` in an explicit registry fiber instead of hard-wiring a tiny local alphabet, and the evaluation plan requires small-, medium-, and unrestricted-complexity sweeps. This is the main guard against bounded-slope trapping.
- Failure mode if ignored: a proof-carrying CA with a tiny frozen alphabet would still just be a bounded-slope search in different clothing.

### AlphaEvolve / Mathematical-discovery systems (2025)
- Overlap type: methodological direct.
- Phase-3 differentiation: `H1` is only different from generic automated discovery if the cell state is proof-carrying, the decoder is fixed and exact, and malformed candidates are rejected rather than repaired. Otherwise the lane reduces to ordinary automated search over witness serializations.
- Failure mode if ignored: any claim of novelty collapses into "a coding agent searched a math object."

### Bond-Levine abelian-network papers (2013, 2014)
- Overlap type: methodological adjacent.
- Phase-3 differentiation: `H1` does not claim an abelian-network theorem or a halting invariant. Abelian-network language is permitted only as a structural analogy or future cache design; the active design remains a direct witness compiler with exact score accounting.
- Failure mode if ignored: the project turns into a transferless sandpile or abelian-network analogy without verified forcing benefit.

### Malformed watchlist trio
- Overlap type: superficial only.
- Phase-3 differentiation: unchanged. The `2x2` convexification paper, the Hopf-hypersurface paper, and the `A_2`-fractions paper remain false overlaps and place no real novelty constraint on the `H1` design.

## Phase 5 Closeout Freeze

Final branch decision: `pivot to verifier recovery`.

Final evidence state: no exact verified witness, no exact score improvement, and no empirical CA advantage claim. The comparisons below freeze the strongest cited prior-work relations actually used in phase-4 analysis.

### Katz-Tao (1999)
- Overlap type: mathematical direct.
- Final comparison: not surpassed. The run stayed within Katz-Tao's witness format but produced no new legal witness or theorem.

### Green-Ruzsa (2017)
- Overlap type: mathematical direct.
- Final comparison: not surpassed. No integer result or finite-field-to-integer lift was obtained.

### Cowen-Breen et al. (2020)
- Overlap type: mathematical adjacent.
- Final comparison: cleared only at the target-definition level. The run avoided pattern-proxy drift, but showed no exact transfer back to forcing-pair improvements.

### Pohoata-Zakharov (2024)
- Overlap type: mathematical adjacent.
- Final comparison: not surpassed. No generalized or original arithmetic-Kakeya gain was produced.

### Tao (2025)
- Overlap type: mathematical direct warning.
- Final comparison: warning unresolved. The phase-4 complexity sweep remained blocked, so bounded-slope and rational-complexity objections were not defeated.

### Hickman-Wright (2018)
- Overlap type: mathematical adjacent.
- Final comparison: modular-only evidence remains inadmissible. No honest modular-to-integer lift was demonstrated.

### Bond-Levine (2013)
- Overlap type: methodological adjacent.
- Final comparison: adjacent only. No abelian-network invariant was shown to predict or certify forcing progress.

### Bond-Levine (2014)
- Overlap type: methodological adjacent.
- Final comparison: adjacent only. No halting or production-matrix result was connected to exact witness generation.

### Dennunzio-Formenti-Margara (2023)
- Overlap type: methodological adjacent.
- Final comparison: background only. The run did not produce an additive-CA theorem or verified additive-rule advantage.

### Faldor-Cully (2024)
- Overlap type: methodological adjacent.
- Final comparison: not exceeded. No diversity-driven CA search result was obtained; only the exact-evaluation discipline is sharper here.

### Novikov et al. (2025) / AlphaEvolve
- Overlap type: methodological direct.
- Final comparison: differentiated only at the design level. Proof-carrying state and no-repair decoding narrow the search story, but no empirical capability beyond generic automated discovery was shown.

### Georgiev et al. (2025)
- Overlap type: methodological direct.
- Final comparison: differentiated only at the design level. The run contributes an audited domain-specific evaluator discipline, not a demonstrated search advance.

## Final Bottom Line

- The strongest cited mathematical prior work remains completely unchallenged because no exact witness was produced.
- The strongest cited methodological prior work is only partially cleared, and only at the level of representation and evaluation discipline.
- The final honest story is therefore a blocker-aware design program plus a verifier-recovery pivot, not a solved cellular-automata witness construction.
