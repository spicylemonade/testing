# Hypothesis Negative Space

## Grounding
- Read `results/research_context.md`, `results/literature/prior_art_gap.md`, `results/literature/gap_frontier.md`, and `results/swarm/director_brief.md`.
- Inspected `results/swarm/falsifier.md` plus the current ConceptEvolve artifacts: `concept_delta.md`, `probe_result.json`, `introspection.json`, `reframings.json`, `steering_directions.json`, the Phase 3 route freeze, and selected concept leaves.
- Working negative filter from that scan:
  - do not repeat `H1_macrocell_substitution` in another width-2 corridor wrapper,
  - do not repeat `H2_target_direction_abelian` as another invariant screen on the same family IDs,
  - do not repeat `H3_slope_bloom` as another tiny label schedule or bounded-slope story,
  - do not fall back to generic bootstrap-droplet, local-decoder, or SAT-wrapper narratives.

## Direction 1: Cooperative Residue Interface Automata
**What prior work ignored.** Most of the search mass went into whole-rule or whole-gadget stories. The less-tested object is the boundary code itself: whether a tiny interface really is a sufficient statistic for exact arithmetic composition.

**Derivative overlap and pivot.**
- Overlap: this is adjacent to `H1_macrocell_substitution`, `graph_grammar_macrosearch`, and regional boundary-control search.
- Pivot: make interface bandwidth and recognizability the first-class hypothesis. Reject occupancy-style, seed-count-only, or width-2-only boundaries before any level-transfer experiment.

**Hypothesis.** There exists a finite interface alphabet carrying a signed residue basis, a phase bit, and a seed-debt counter such that pairwise and `2 x 2` macrocell compositions remain exact under one unchanged extractor, and level-2 lowers `R` faster than it raises `m`.

**Why this attacks the negative space.** The repo-local gap analysis says fixed `X` can only win through boundary reuse, defect routing, or seed economics. This route attacks boundary reuse directly instead of searching another local rule and hoping transfer appears later.

**First experiment.**
- Fix one low-height asymmetric `X` under a strict alphabet budget.
- Enumerate exact local residue summaries on tiny macrotiles.
- Count canonical legal interface traces and compare them to the unresolved residue classes seen in exact local elimination.
- Continue only if the same interface table parses both level-1 and level-2 compositions with no new symbols and no repair pass.

**Kill signal.**
- The interface trace language is tiny or quickly periodic.
- Level 2 needs new interface symbols, new merge rules, or direct global repair.
- Direct grammar search with the same description budget finds the same family.

**Angle to avoid.** Do not propose another fixed-corridor transfer experiment and call it new. If interface sufficiency is not the explicit object being tested, this is just H1 again.

## Direction 2: Affine-Core / Nonlinear-Shell CA With UNSAT-Core Motif Mining
**What prior work failed to test.** The previous routes did not isolate where the useful nonlinearity lives. That leaves a major hidden-failure mode: diffuse nonlinear repair in the bulk, only discovered after extraction fails.

**Derivative overlap and pivot.**
- Overlap: this touches `affine_ca_negative_filter` and the SAT boundary-control compiler.
- Pivot: use SAT only for tiny-instance obstruction mining and gate certification. The bulk dynamics must stay interpretable and mostly affine; the solver is not allowed to become the real search engine.

**Hypothesis.** A viable AK-oriented CA family has an affine transport interior over fixed `X` and a very small nonlinear shell at interface or defect-collision sites, and that shell can be recovered from stable SAT/UNSAT motifs on `2`- and `3`-layer exact instances.

**Why this attacks the negative space.** The forcing formalism is globally linear but support-sensitive. Concentrating nonlinearity at audited gates is the cleanest way to distinguish a real local mechanism from hidden solver glue.

**First experiment.**
- Classify candidate local updates into affine interior pieces and nonlinear gates.
- Encode tiny exact instances into SAT or MaxSAT.
- Log satisfiable motifs and UNSAT cores.
- Keep only families whose extracted behavior survives when bulk nonlinearity is stripped away and whose UNSAT cores stabilize into a small gate library.

**Kill signal.**
- The gain disappears once bulk nonlinearity is removed.
- UNSAT cores do not stabilize into a reusable gate library.
- The route needs scale-specific repair or unrestricted direct search beats it on the same exact budget.

**Angle to avoid.** Do not run full-graph SAT or a diffuse nonlinear CA and retrofit a story afterward. That is another wrapper or prior, not a new CA mechanism.

## Direction 3: Phase-Coded Defect Transport On Aperiodic Corridors
**What prior work could not scale.** Fixed-`X` routes flattened into periodic strips, boundary programming, or tiny bounded-slope basins. The under-tested alternative is geometric phase structure: improve seed economics without adding slopes.

**Derivative overlap and pivot.**
- Overlap: this is adjacent to `sweep_decoder_defect_transport`, chip-firing or seed-compression motifs, and H3-style fixed-rule dynamics.
- Pivot: keep `X` fixed and use phase-coded stage order or aperiodic corridor geometry to route typed residues toward sinks. The point is lower seed debt, not larger realized slope complexity and not decoder-threshold folklore.

**Hypothesis.** A height-2 or height-3 anisotropic corridor with a tiny aperiodic phase schedule and one or two sink types can move anti-diagonal obligations efficiently enough that `r/n` falls with scale even though `X` stays fixed and slope complexity stays bounded.

**Why this attacks the negative space.** The probe artifacts say fixed `X` can only help through boundary reuse, defect routing, or better seed economics. This is the cleanest version of defect routing that is not just another diffusion metaphor.

**First experiment.**
- Use two corner defects and one typed sink on thin corridors.
- Compare periodic versus aperiodic phase schedules under the same extractor.
- Add orientation-randomized and transposed controls on the same geometry.
- Track `r/n`, exact score, stage-order robustness, and whether removing extra boundary seeds leaves transport intact.

**Kill signal.**
- Gains disappear under transposition or orientation perturbation.
- Seed reduction vanishes once periodicity is broken.
- The model needs wider interfaces or richer `X` to survive.

**Angle to avoid.** Do not market vanilla sandpile diffusion, toric-code threshold heuristics, or another slope-bloom schedule as progress. If the lever is not seed-debt reduction at fixed `X`, it is derivative.

## Recommended Order
1. Start with Direction 2. It is the cheapest audit and prevents hidden bulk nonlinearity or solver repair from contaminating everything else.
2. Move to Direction 1 only if a small nonlinear gate library survives the audit.
3. Keep Direction 3 as the scaling hedge once fixed-`X` seed economics becomes the real bottleneck.
