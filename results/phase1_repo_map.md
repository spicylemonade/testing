# Phase 1 Repo Map

## Root

- `README.md`
  - Current state: placeholder only (`# testing`).
  - Practical implication: the research pipeline is driven by `results/` and `.archivara/`, not by a project README.
- `research_rubric.json`
  - Phase-by-phase execution contract for this run.
  - Every downstream artifact in this map exists to satisfy one or more rubric items.
- `.archivara/concept_evolve.py`
  - Required structured exploration tool. This run patched a broken `evolve()` call path before use.
- `.archivara/semantic_scholar.py`
  - Canonical literature helper. Its manifest in `results/literature/semantic_scholar_manifest.json` is the persistent memory for prior searches.

## Research Context

- `results/research_context.md`
  - Human-readable run context: stage, tracked papers, recent Semantic Scholar activity, and high-level prior-art framing.
- `results/research_context.json`
  - Structured companion to the markdown context.
  - Stores the exact task text, rubric summary, git snapshot, literature stats, and swarm availability.

## Literature Layer

- `results/literature/literature_snapshot.json`
  - Current snapshot of discovered papers.
  - Present state is low-signal because it was seeded from a corrupted query and therefore must be repaired rather than trusted.
- `results/literature/seed_search.json`
  - Raw first-pass seed search output used to create the broken snapshot.
- `results/literature/literature_graph.json`
  - Citation-graph style expansion from the same poor seed. Useful mainly as a record of what not to reuse blindly.
- `results/literature/semantic_scholar_manifest.json`
  - Canonical search memory. This is the file that prevents duplicated literature work and records whether new searches were exact-title, citation, reference, or recommendation based.
- `results/literature/prior_art_watchlist.md`
  - Current watchlist generated from the corrupted seed query.
  - It is not reliable novelty evidence, but it is still a required artifact because the novelty guard and reviewer prompts reference it.
- `results/literature/novelty_guard.json`
  - Encodes the watchlist-derived guardrails and novelty questions.
  - Function: forces every later route to state why it is not just overlap dressed in new language.
- `results/literature/prior_art_gap.md`
  - Durable gap log.
  - Intended use: record exact overlap, evidence, and pivot decisions whenever a branch is too close to existing work or to the corrupted watchlist.
- `results/literature/gap_frontier.md`
  - Free-form frontier notes focused on limitations and open problems rather than nearest-neighbor similarity.
- `results/literature/gap_frontier.json`
  - Structured counterpart to the frontier notes.

## Swarm Layer

- `results/swarm/director_brief.md`
  - Decides the route order.
  - Current binding decision: `H1_macrocell_substitution` is champion, `H2_target_direction_abelian` is the only live backup, `H3_slope_bloom` is reserve-only.
- `results/swarm/hypotheses.json`
  - Structured hypothesis registry with novelty claims, easiest falsifiers, and budget envelopes.
- `results/swarm/tool_plan.md`
  - Operational contract for each role.
  - Important constraint: no experiments before one certificate grammar, one matched baseline matrix, and one symmetry-quotient policy are frozen.
- `results/swarm/falsifier.md`
  - Adversarial memo listing immediate kill criteria and comparison traps.
- `results/swarm/gap_map.md`
  - Synthesized map of the most plausible under-served directions after correcting for the broken literature seed.
- `results/swarm/hypothesis_bridge.md`
  - Cross-domain bridge proposals linking arithmetic Kakeya to CA-adjacent theories.
- `results/swarm/hypothesis_negative_space.md`
  - Explicit list of directions not to repeat, plus guardrails around metaphor-only CA formulations.

## Verification Layer

- `results/verification/`
  - Exists but is currently empty.
  - Intended terminal sink for:
    - `novelty_report.md`
    - `citation_audit.md`
    - `benchmark_report.md`
    - `verification_summary.md`
  - Meaning in the artifact flow: literature and swarm planning are hypotheses; verification artifacts are where those claims are either supported, weakened, or rejected after exact extraction and matched controls.

## Intended Artifact Flow

1. `research_context.{md,json}` captures the problem statement, run state, and existing memory.
2. `literature_snapshot.json`, `semantic_scholar_manifest.json`, `prior_art_watchlist.md`, and `novelty_guard.json` define what has been searched and what overlap risks must stay live.
3. `gap_frontier.{md,json}` and `prior_art_gap.md` convert raw literature into gap-first decisions and explicit pivot logs.
4. `swarm/*.md` and `swarm/hypotheses.json` turn those gaps into route selection, kill criteria, and benchmark discipline.
5. `results/concept_evolve/` is the structured idea-expansion layer that must stay aligned with the saved literature and swarm constraints.
6. `results/verification/` is the final adjudication layer. Nothing counts as a contribution until claims survive exact certificate extraction, matched baselines, ablations, and novelty/citation audit there.
