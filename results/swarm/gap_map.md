# Gap Map

## Readout

- The local prior-art cache is effectively empty for this topic: the watchlist was generated from a broken tokenized query, and there are no existing swarm or verification artifacts in the repo.
- Targeted checks do surface the real frontier: Green-Ruzsa (2019) covers the classical arithmetic Kakeya formulation; the exact `X`-constructible / forcing-pair language used here appears to be a repackaging of the Katz-Tao small-graph method rather than a mature standalone subliterature; Pohoata-Zakharov (2024) pushes a generalized variant; Tao (2025) discusses bounded-slope / rational-complexity barriers and notes that automated experiments improved lower bounds more readily than upper bounds; the FrontierMath arithmetic-Kakeya note says the current explicit limit `1.6751308` comes from constructions where `X` grows without bound as the score approaches that limit.
- The same FrontierMath note is also a warning about method choice: there is an easy `3/2` barrier for elementary arguments, so any CA program that behaves like a monotone local-growth heuristic is at real risk of rediscovering that ceiling instead of moving the frontier.
- I did not surface a direct literature bridge from cellular automata to verifier-compatible arithmetic Kakeya upper-bound certificates. That absence is itself part of the negative space.

## Priority Gaps

| Priority | Gap | Why It Looks Under-Served | Why It Matters Here | Concrete Next Move |
| --- | --- | --- | --- | --- |
| 1 | **Mesoscopic, low-height `X` families near `1.675`** | The clearest frontier note says the current explicit limit `1.6751308` is only reached with extremely large `X` that must grow without bound near the limit. That leaves the bounded or slowly growing alphabet regime thinly explored, especially for low-height but arithmetically asymmetric label sets. | A cellular-automata approach only makes sense if the label alphabet is tractable. If `X` must be huge, the method collapses into generic symbolic search; if `X` is low-height but asymmetric, rational-complexity effects may still be exploitable. | Fix a strict alphabet budget such as `|X| <= 5` or `|X| <= 8`, and search for verifier-valid families that beat `1.69` before chasing `1.675`. Do not only vary `|X|`; also vary determinant pattern, height, and asymmetry inside `X`. |
| 2 | **Local-to-global certificate gap** | The formal proof system is not local: arbitrary integer linear combinations in rule (3) are global, while the target output is a forcing certificate, not just a propagating pattern. Tao's 2025 note is especially revealing here: automated search helped with lower bounds, but not with efficiently establishing upper bounds. | This is the main modeling risk in “solve it with cellular automata.” A naive local automaton can mimic edge propagation but still fail to represent the row-span arithmetic needed to isolate `(a,-a)` at one vertex. | Build a block-local or hierarchical automaton whose state is a compressed lattice summary, not a binary occupancy rule. A useful prototype would alternate local updates with exact lattice-basis compression on tiles, then test whether those tile summaries compose under graph gluing. |
| 3 | **Anisotropic and self-similar recursive product geometries** | Most discussion in this area is asymptotic in slopes or projections, while the verifier’s legal objects are recursive product graphs with ordered stages `d_1, ..., d_k`. The degrees of freedom coming from highly uneven aspect ratios, stage order, and repeated macro-cells look largely unmined. | Cellular automata are naturally good at finite-size fronts, waveguides, and renormalized spacetime motifs. Those mechanisms map more naturally to thin-or-anisotropic products and repeated macro-gadgets than to symmetric grids. | Search over “corridor” families such as `(2,2,2,n)`, `(3,2,n)`, and repeated macro-cell constructions where a fixed gadget is recursively glued into a larger product. Evaluate whether anisotropy or renormalization can shrink `|R|` faster than it increases `m`. |
| 4 | **Defect-seeded, boundary-critical forcing pairs** | Lemm’s counterexamples on related sums-differences problems explicitly exploit non-uniform probability measures, which is a warning that symmetry-biased searches may be looking in the wrong place. On the constructive upper-bound side, the natural computational default is still regular, homogeneous gadgets. | If sparse irregular seeds can trigger large cancellation cascades inside an otherwise regular constructible graph, then a CA viewpoint should treat them as defects or nucleation sites rather than as noise. Boundary faces, slabs, and other critical-droplet patterns are especially plausible because support-clearing is part of the proof itself. | Hold `G` nearly regular but optimize a tiny irregular budget in `R` and `T`: seed placement, label heterogeneity, stage-specific defects, and boundary-facing support patterns. This is the right regime for “few smart impurities beat many uniform seeds.” |
| 5 | **Compile-to-certificate search space** | There is no existing benchmark set, no verifier traces, and no canonical search grammar in the repo. More importantly, the final object is a rigid six-line certificate `(X; d_i; f_i; T; R)`. Any search process that does not enforce this grammar from the start will overproduce attractive but unusable motifs. | This is the concrete failure mode for CA-guided research: finding beautiful spacetime diagrams that do not correspond to legal recursive gluings or admissible forcing pairs. | Make the search space certificate-first. The “genome” should already be `d_i`, sparse supports for each `f_i`, and admissible singleton-support seeds for `R`. If a CA is used, it should only evolve objects that are already compilable to the verifier format. |

## Why These Five Come First

1. The strongest immediate negative space is the mismatch between the current near-barrier construction regime and any finite-state or finite-alphabet computational search.
2. The most dangerous hidden failure mode is confusing local propagation with an actual forcing certificate.
3. The most plausible under-explored structure family is not “bigger symmetric grids,” but anisotropic recursive products with engineered boundaries, defects, and repeated macro-cells.
4. The repo itself confirms that the tooling layer is empty, so search-space design is not peripheral here; it is a first-order research bottleneck.

## CA-Specific Warning

- Do not start with a translation-invariant binary automaton.
- The formal system is signed, arithmetic, boundary-sensitive, and globally closed under integer linear combination.
- A viable CA framing would need to be:
  - hierarchical rather than flat
  - signed or multi-track rather than binary
  - certificate-compiling rather than pattern-first

## Evidence Anchors

- Green and Ruzsa (2019), `On the arithmetic Kakeya conjecture of Katz and Tao`
- Cowen-Breen et al. (2020), `Pattern Problems related to the Arithmetic Kakeya Conjecture`
- Lemm (2014), `New Counterexamples to the Sums-Differences Problem`
- Pohoata and Zakharov (2024), `A generalized arithmetic Kakeya theorem`
- Tao (2025), `Sum-difference exponents for boundedly many slopes and rational complexity`
- FrontierMath arithmetic-Kakeya problem note / PDF
