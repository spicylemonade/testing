# Phase 1 Literature Synthesis

## Inputs Reviewed

- `results/literature/literature_snapshot.json`
- `results/literature/prior_art_gap.md`
- `results/context_sync.md`
- `results/swarm/director_brief.md`
- `results/swarm/falsifier.md`
- `sources.bib`
- Multi-agent memos from `explorer`, `citation_auditor`, and `integrator`

## Bottom-Line Decision

- Keep `H1` as the only champion lane.
- Keep `H2` as backup-only.
- Keep `H3` reserve-only.
- Treat the malformed watchlist as a novelty-sanity check, not as a real bibliography.

## Champion Lane

`H1`, the proof-carrying symbolic forcing-front CA, remains the least derivative direction. It is the only lane that uses the product-grid witness representation itself as the automaton substrate and requires local state to carry verifier-relevant symbolic information rather than heuristic pattern statistics. That makes it meaningfully different from generic neural CA, fixed-pattern search, or AlphaEvolve-style automation only if the decoder compiles outputs directly to legal `(X,G,R,T)` witnesses with no repair step.

## Strongest Adjacent Prior-Art Pressure

The genuine pressure comes from the real arithmetic-Kakeya and adjacent-method literature, not from the malformed watchlist.

- Katz-Tao (1999) fixes the target: any claim must land on the original arithmetic-projection / forcing-pair problem.
- Green-Ruzsa (2017) blocks modular-only or finite-field CA stories.
- Cowen-Breen et al. (2020) blocks drift into nearby pattern problems while claiming forcing-pair progress.
- Pohoata-Zakharov (2024) blocks novelty-by-reformulation.
- Tao (2025) is the main structural warning that a small fixed CA alphabet risks becoming bounded-slope search in disguise.
- Bond-Levine (2013, 2014), Dennunzio et al. (2023), and Faldor-Cully (2024) are method-side anchors, but they are adjacent scaffolding rather than evidence of arithmetic-Kakeya progress.
- AlphaEvolve (2025) and `Mathematical exploration and discovery at scale` (2025) block novelty claims based on automation alone.

## Main Novelty Risk

The primary failure mode is not that CA ideas are irrelevant. It is that the project collapses into one of three already-criticized stories:

1. bounded-slope or low-rational-complexity search in CA clothing;
2. modular or finite-alphabet mirages that never lift back to `\mathbb{Z}`;
3. generic automated search where the compiler or decoder does the real intellectual work.

That means the novelty bar is narrow. The lane only survives if it remains verifier-coupled, fails under label shuffling, escapes low-complexity slope traps, and eventually survives exact integer verification.

## Watchlist Triage

The required watchlist comparisons are negative:

- `2x2-Convexifications for convex quadratic optimization with indicator variables` is a false overlap caused by LaTeX-token pollution.
- `On Hopf hypersurfaces of the homogeneous nearly Kahler S^3 x S^3` is a false overlap caused by product-notation token collision.
- `Continued A_2-fractions and singular functions` is a false overlap caused by token noise.

These are not genuine novelty constraints for the arithmetic-Kakeya CA lane.

## Sufficiency Check

The citation-audit pass judged the current phase-1 literature set sufficient for synthesis: the curated extension contains 12 relevant entries and `sources.bib` contains 12 BibTeX records. One optional next source is Bourgain’s original arithmetic-projection / method-of-slices paper, but it is not blocker-grade for the current phase.

## Phase-1 Decision

- Promote the concept card `Proof-Carrying Symbolic Forcing-Front CA`.
- Keep a pressure card for the real adjacent arithmetic-Kakeya literature.
- Keep a risk card for the generic-search novelty failure mode.
