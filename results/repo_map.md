# Repository Map

## Control plane
- `research_rubric.json` is the run-state machine. Each phase/item status gates what the researcher, writer, and reviewer are allowed to claim.
- `results/research_context.md` and `results/research_context.json` are the coarse session memory. They summarize rubric progress, literature counts, active direction, and final package pointers.

## Literature pipeline
- `.opencode/tools/semantic_scholar.ts` is the OpenCode wrapper. It turns tool calls into `python3 .archivara/semantic_scholar.py ...` executions.
- `.archivara/semantic_scholar.py` is the real literature runner. It queries Semantic Scholar, caches raw responses in `.archivara/cache/semantic_scholar/`, updates `results/literature/semantic_scholar_manifest.json`, and optionally saves JSON snapshots into `results/literature/`.
- `results/literature/` is the durable literature workspace: `literature_snapshot.json` is the baseline map, `prior_art_watchlist.md` and `novelty_guard.json` hold novelty risks, `prior_art_gap.md` is the living differentiation log, and `gap_frontier.*` stores open-problem or limitation-oriented search results.

## Concept pipeline
- `.opencode/tools/concept_evolve.ts` is the wrapper that shells out to `python3 .archivara/concept_evolve.py <command> ...`.
- `.archivara/concept_evolve.py` is the orchestration layer for concept generation. It fingerprints context, launches OpenCode sub-agents, watches target artifacts, and post-processes concept outputs into tree indices and walk paths.
- `.opencode/agents/concept-tree-explorer.md` defines the delegated tree-audit role. It is read-only and meant to inspect concept folders, identify promising branches, and suggest next experiments.
- `results/concept_evolve/` stores generated concept cards, bridge graphs, probe/reframe/iterate outputs, and the live tree under `results/concept_evolve/tree/`.
- `results/concept_evolve/tree/*/concept.json` is the per-concept source of truth; `README.md` is the implementation backlog; `literature.json` anchors each concept in prior work.

## Swarm and decision artifacts
- `results/swarm/director_brief.md` picks the champion and backup hypotheses.
- `results/swarm/hypotheses.json` is the structured hypothesis registry with falsifiers and budget envelopes.
- `results/swarm/tool_plan.md` constrains search breadth, selector fishing, and the handoff order across researcher/falsifier/writer/reviewer.
- `results/swarm/falsifier.md` is the adversarial checklist that prevents category mistakes such as word/value confusion or rational-triviality neglect.

## Verification and publication flow
- `results/verification/` is the final audit sink for novelty, citation, benchmark, and synthesis reports.
- Those verification artifacts feed back into `results/research_context.*`, `results/literature/prior_art_gap.md`, and `results/concept_evolve/concept_delta.md` before sign-off.

## Data flow summary
1. OpenCode tool wrappers in `.opencode/tools/` invoke the Python runners in `.archivara/`.
2. `semantic_scholar.py` populates `results/literature/` and updates the manifest/cache.
3. `concept_evolve.py` reads the literature and swarm context, then writes `results/concept_evolve/` artifacts and the concept tree.
4. The researcher converts those artifacts into experiment code, figures, and verification memos, which then update `results/verification/`, `results/research_context.*`, and the rubric.

## Repair note
- The kickoff evolve path in `.archivara/concept_evolve.py` was missing the `command`, `fingerprint`, `topic`, and `watched_paths` arguments required by `_run_sub_agent`. I repaired that call path and aligned the tree-folder slugging with the snake_case concept-card convention so ConceptEvolve outputs can be reused deterministically by the later phases.
