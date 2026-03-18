# Gap Map: Negative Space Around Cellular-Automata Search for Arithmetic Kakeya

## Signal Check
- The stored watchlist for this run is low-signal for the actual topic. Its top hits are LaTeX-token collisions rather than arithmetic-Kakeya papers.
- The usable primary-source anchors recovered in this session are much narrower: Katz-Tao (1999), Green-Ruzsa (2017), Cowen-Breen et al. (2020), Pohoata-Zakharov (2024), Tao (2025), Bond-Levine (2013, 2014), Dennunzio-Formenti-Margara (2023), Faldor-Cully (2024), and the 2025 automated-search papers around AlphaEvolve.
- The targeted scan did not surface meaningful prior art that directly uses cellular automata to search for arithmetic-Kakeya constructible graphs or forcing pairs. That absence is only a search result from this pass, not a proof of nonexistence.

## 1. Proof-carrying local-to-global elimination
- Priority: highest
- Type: core under-explored gap
- Why this looks under-served:
  The verifier does not reward generic propagation. A candidate only works if the generated relations actually place `(a,-a)` on a single vertex after integer linear combinations and the `T` masking condition are taken into account. That is much closer to local processors cooperating on a global elimination problem than to ordinary CA diffusion.
- Why a naive CA fails:
  A local rule can create coherent space-time patterns while still never certifying that a legal singleton-supported relation lies in the `Z`-span of the produced generators. This creates attractive false positives.
- Concrete next move:
  Build a proof-carrying hybrid CA in which each block stores sparse generator identities, coefficient summaries, and provenance tags, and require every terminal state to compile directly into the six-line `(X,G,R,T)` witness format.
- Evidence anchors:
  `results/research_context.md`; Bond-Levine, *Abelian networks I. Foundations and examples* (2013); Bond-Levine, *Abelian networks II. Halting on all inputs* (2014).

## 2. Escaping the bounded-slope / low-complexity trap
- Priority: high
- Type: failure mode plus under-explored setting
- Why this looks under-served:
  Tao's 2025 note shows that when the slope set is bounded, the relevant sum-difference exponents are driven back toward `2`, with the rate controlled by rational complexity. A CA with a fixed small alphabet is naturally biased toward exactly that low-complexity regime.
- Why a naive CA fails:
  It will overfit to periodic, low-complexity label sets that are computationally convenient but structurally misaligned with the frontier near `1.67513...`.
- Concrete next move:
  Treat `|X|`, rational complexity, and score as a Pareto objective. Compare fixed-alphabet CA rules against rules that can grow or mutate the slope alphabet across scales, and reject any architecture that only succeeds in the bounded-slope regime.
- Evidence anchors:
  Tao, *Sum-difference exponents for boundedly many slopes, and rational complexity* (2025).

## 3. Modular shadow search without a trustworthy integer lift
- Priority: high
- Type: under-explored bridge
- Why this looks under-served:
  Green-Ruzsa show that a natural finite-field variant of arithmetic Kakeya does hold, and mod-`p` or `Z/NZ` state spaces are far more natural for finite automata than the full integer witness space. What is missing is a disciplined pipeline that uses modular search only as a shadow of the integer problem rather than as a misleading surrogate.
- Why a naive CA fails:
  Perfect-looking cancellations modulo `p` can disappear completely over `Z`. A bounded-state automaton can therefore report fake progress unless integer lift conditions are built into the evaluation loop.
- Concrete next move:
  Use `F_p` and `Z/NZ` tasks as curriculum instances for motif discovery, then force every promising modular pattern through a deterministic integer-lift and witness-compilation test before it counts as progress.
- Evidence anchors:
  Green-Ruzsa, *On the arithmetic Kakeya conjecture of Katz and Tao* (2017); Hickman-Wright, *The Fourier restriction and Kakeya problems over rings of integers modulo N* (2018); `results/research_context.md`.

## 4. Flat-lattice automata ignore recursive constructibility
- Priority: medium-high
- Type: structural mismatch
- Why this looks under-served:
  The legal search space is not the space of arbitrary edge-labeled grids. It is the space of recursively built copy-and-glue constructions encoded by `d_1,...,d_k` and the stagewise dictionaries `f_i`. A flat CA on the realized graph forgets the ancestry that determines legality and cost.
- Why a naive CA fails:
  It can discover visually regular or algebraically suggestive local motifs that are either not valid constructible graphs at all or only become valid after expensive repairs that destroy the score.
- Concrete next move:
  Run the automaton on the construction tree, or on stage-indexed fibers of the product representation, so legality is enforced by the state space itself. The automaton should natively mutate copy, glue, and edge-label choices rather than paint over a final graph.
- Evidence anchors:
  `results/research_context.md`; Pohoata-Zakharov, *Generalized Arithmetic Kakeya* (2024), which shows how much leverage can come from iterative strengthening rather than a single flat inequality view.

## 5. Search is trapped in one sparse objective and one uniform encoding
- Priority: medium-high
- Type: under-explored benchmarking gap
- Why this looks under-served:
  Arithmetic Kakeya already has nearby equivalent or adjacent formulations, including the pattern / homothet problems of Cowen-Breen et al., while Katz-Tao and later work point toward gains from richer projection or slice information. In contrast, most CA-style search setups would optimize a single final score on a single encoding and therefore inherit an extremely sparse reward.
- Why a naive CA fails:
  Pure score optimization encourages short-period, translation-invariant motifs because they are easy to rediscover. The genuinely useful witnesses may instead depend on rare defects, nonuniform stage schedules, or formulations with denser local rewards.
- Concrete next move:
  Build a descriptor-rich benchmark suite that tracks forcing depth, slope entropy, defect density, modular lift rate, certificate compression, and pattern-problem proxies. Use novelty or quality-diversity style search to force exploration of sparse, nonuniform motifs before translating back into exact `(X,G,R,T)` witnesses.
- Evidence anchors:
  Katz-Tao, *Bounds on arithmetic projections, and applications to the Kakeya conjecture* (1999); Cowen-Breen, Karangozishvili, Varadarajan, Wang, *Pattern Problems related to the Arithmetic Kakeya Conjecture* (2020); Faldor-Cully, *Toward Artificial Open-Ended Evolution within Lenia using Quality-Diversity* (2024).

## Prior-Art Anchors Used
- Katz-Tao, *Bounds on arithmetic projections, and applications to the Kakeya conjecture* (1999).
- Green-Ruzsa, *On the arithmetic Kakeya conjecture of Katz and Tao* (2017).
- Cowen-Breen, Karangozishvili, Varadarajan, Wang, *Pattern Problems related to the Arithmetic Kakeya Conjecture* (2020).
- Hickman-Wright, *The Fourier restriction and Kakeya problems over rings of integers modulo N* (2018).
- Pohoata-Zakharov, *Generalized Arithmetic Kakeya* (2024).
- Tao, *Sum-difference exponents for boundedly many slopes, and rational complexity* (2025).
- Bond-Levine, *Abelian networks I. Foundations and examples* (2013).
- Bond-Levine, *Abelian networks II. Halting on all inputs* (2014).
- Dennunzio-Formenti-Margara, *An Easily Checkable Algebraic Characterization of Positive Expansivity for Additive Cellular Automata over a Finite Abelian Group* (2023).
- Faldor-Cully, *Toward Artificial Open-Ended Evolution within Lenia using Quality-Diversity* (2024).
- Novikov et al., *AlphaEvolve: A coding agent for scientific and algorithmic discovery* (2025).
- Georgiev, Gomez-Serrano, Tao, Wagner, *Mathematical exploration and discovery at scale* (2025).

## Bottom Line
- The most under-served directions are not generic "use CA" ideas.
- They are the parts where local dynamics must become certificate-carrying, complexity-aware, modularly disciplined, recursive-constructibility-aware, and benchmarked against sparse nonuniform motifs rather than only against a single final score.
