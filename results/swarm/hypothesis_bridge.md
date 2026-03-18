# Hypothesis Bridge

Exact integer decoding and forcing verification are still the gating blocker in this repo. The three bridges below are therefore framed as post-verifier-recovery hypotheses, not as active empirical claims.

Overlap/pivot note:
- I am not reviving the retired transport-first families: `anisotropic_current_screening`, `odometer_rotor_transport_bridge`, or `observer_guided_macrocell_search`.
- I am also not polishing generic neural-CA search. Where a candidate overlaps an existing ConceptEvolve branch, I state the overlap and the pivot explicitly.

## 1. Threshold-Saturated Certificate-Wave CA

**Title:** Threshold-Saturated Certificate-Wave CA

**Closest prior art:** Spatial coupling and threshold saturation for LDPC decoding; the repo's `spatially_coupled_peeling_ladders` bridge; adjacent arithmetic-Kakeya pattern formulations where local templates matter more than a single global inequality.

**Why it is different:** This overlaps the surviving `spatially_coupled_peeling_ladders` branch, but the pivot is decisive: the CA would not propagate a heuristic peeling score or a generic infection rule. Each update would consume only verifier-legal singleton certificate templates mined from tiny exact-valid witnesses, and the cell alphabet would carry stage ancestry so that only legal copy/glue moves are expressible. The imported invariant is threshold saturation, not percolation rhetoric. The hypothesis is that boundary coupling can lower verified score density because exact certificate waves avoid paying the full seed cost in every slab.

**Falsifiable prediction:** After the exact decoder exists, a coupled boundary-seeded CA built from exact certificate templates will produce a strictly better distribution of exact verified scores than uncoupled repetition, random local search, and whole-witness mutation at matched decode budget. That advantage should collapse under `X`-label shuffling, randomized template banks, or held-out larger/aspect-ratio grids if the effect is only geometric.

**Required experiments:**
- Recover or implement the exact six-line decoder and integer forcing verifier.
- Build a bank of tiny exact-valid witness fragments and extract local singleton-certificate templates from them.
- Implement a stage-indexed CA whose local state includes template IDs, ancestry tags, and active `X` labels.
- Compare coupled and uncoupled constructions against matched non-CA baselines under label-shuffle, held-out geometry, held-out `X`, and rational-complexity sweeps.

## 2. SAT-Synthesized Quotient CA over E-Graph Proof States

**Title:** SAT-Synthesized Quotient CA over E-Graph Proof States

**Closest prior art:** SAT-based cellular-automata analysis; equality saturation and `egg`; the repo's `sat_egraph_symbolic_backbone` and `egraph_linear_span_rewriting` branches.

**Why it is different:** This clearly overlaps the surviving `sat_egraph_symbolic_backbone` idea, so the pivot has to be explicit: the e-graph is not an offline cache or a post-hoc simplifier. It becomes part of the CA state space. Each cell stores a small canonical equivalence class of local linear-span derivations, and SAT synthesizes only local rules whose spacetime orbits remain directly decodable into legal witness fragments. That turns the search object into a CA over canonical proof states rather than over raw witness strings, arbitrary motifs, or generic rule tables.

**Falsifiable prediction:** A quotient CA whose state alphabet is e-graph-canonicalized proof data will beat unconstrained CA rule sampling and decoder-matched non-CA search on exact-valid hit rate per decode budget, while also reducing redundant `R` growth or verifier time. If the gain disappears when canonical class IDs are randomized, when the e-graph layer is removed, or when `X` labels are shuffled, the bridge is dead.

**Required experiments:**
- Build a minimal e-graph over local witness atoms: singleton seeds, edge differences, subtraction, and short motif compositions.
- Encode exact decodability, locality, and optional symmetry constraints as a SAT family that synthesizes tiny-radius CA rules.
- Evaluate exact-valid yield, verified score distribution, `|R|` compression, and verifier runtime against random rule sampling, whole-witness mutation, and decoder-matched non-CA search.
- Run ablations for e-graph removal, randomized canonicalization, label shuffling, held-out board sizes, and held-out legal alphabets.

## 3. Cooperative Macro-Tile Defect CA for Recursive Witness Assembly

**Title:** Cooperative Macro-Tile Defect CA for Recursive Witness Assembly

**Closest prior art:** Algorithmic self-assembly and macro-tile constructions; the repo's `tile_assembly_constructible_grammar` branch; self-assembly work that uses cellular-automaton-style local update patterns to stabilize growth.

**Why it is different:** This overlaps the held `tile_assembly_constructible_grammar` direction, but the pivot is away from static tilings or SFT-style encodings. The proposal is an asynchronous macrocell CA whose temperature-2-style cooperative boundaries encode stage ancestry, active `X` membership, and admissible gluing interfaces. Rare defect tiles are the only places where nonzero edges or seed relations can appear. The imported assumption from self-assembly is that cooperative boundary matching can enforce recursive legality more effectively than a flat CA or a handwritten decoder.

**Falsifiable prediction:** A cooperative macro-tile CA seeded from a tiny library of exact-valid gadgets will generalize to larger macroboards and new aspect ratios with better exact-valid rate and lower score density than flat-lattice CA or static grammar enumeration at matched defect budget. If the gain survives label shuffling or disappears when cooperative boundary states are replaced by independent local matching, then the bridge is only exploiting geometry and should be killed.

**Required experiments:**
- Recover the exact verifier, then distill a small library of exact-valid micro-gadgets into 8-16 macro-tile types.
- Implement an asynchronous macrocell CA whose boundary states encode ancestry, legality, and active alphabet membership.
- Decode `3x3`, `4x4`, and `5x5` macroboards into six-line witnesses and compare against flat CA, uncoupled tilings, and random defect grammars under matched budgets.
- Run label-shuffle, held-out aspect-ratio, decoder-ablation, and defect-density-matched controls before promoting the bridge.
