# Repository Map

## Core Research Tooling

- `.archivara/concept_evolve.py`
  - Python entrypoint for concept-tree generation, probing, reframing, and iteration.
  - Launches `opencode run`, post-processes concept artifacts, and writes `results/concept_evolve/` outputs.
- `.archivara/semantic_scholar.py`
  - Python helper for Semantic Scholar search, citation graph traversal, recommendations, and BibTeX export.
  - Updates `results/literature/semantic_scholar_manifest.json` and optional saved JSON snapshots.
- `.opencode/tools/concept_evolve.ts`
  - TypeScript wrapper that invokes `.archivara/concept_evolve.py` from the OpenCode tool surface.
- `.opencode/tools/semantic_scholar.ts`
  - TypeScript wrapper that invokes `.archivara/semantic_scholar.py` with JSON-friendly arguments.

## Agent Prompts

- `.opencode/agents/concept-tree-explorer.md`
  - Subagent prompt for concept-tree traversal and next-experiment selection.
- `.opencode/agents/literature-graph-miner.md`
  - Subagent prompt for mining citation neighborhoods and transferable ideas.

## Results Folders

- `results/literature/`
  - Stores the literature snapshot, watchlist, gap analysis, graph exports, and the persistent Semantic Scholar manifest.
- `results/swarm/`
  - Stores the hypothesis shortlist, director brief, falsifier notes, and budget/tool governance outputs.
- `results/verification/`
  - Reserved for benchmark audits, novelty checks, reproducibility reports, and final verification summaries.
- `results/concept_evolve/`
  - Stores concept cards, bridge graphs, reframings/probes, tree folders, and steering notes for the novelty program.

## Wrapper-To-Python-To-Results Flow

1. OpenCode tool wrappers in `.opencode/tools/*.ts` expose `concept_evolve` and `semantic_scholar` as callable tools.
2. Each wrapper shells into its paired Python helper under `.archivara/`.
3. `.archivara/concept_evolve.py` may spawn a sub-agent with `opencode run`, then normalizes outputs into `results/concept_evolve/`.
4. `.archivara/semantic_scholar.py` queries Semantic Scholar directly, caches responses under `.archivara/cache/semantic_scholar/`, and records canonical search memory in `results/literature/semantic_scholar_manifest.json`.
5. Downstream planning artifacts in `results/swarm/`, `results/literature/`, and later `results/verification/` consume those saved outputs instead of restarting discovery from scratch.

## Current Implementation Reality Check

- The repository contains research scaffolding and concept-generation outputs, but no actual gravity simulator implementation yet.
- There is no physics core, scenario runner, diagnostics module, benchmark harness, or reproducibility script in the tracked workspace at this stage.
- `results/verification/` is still empty, so all simulator code and experimental evidence remain to be built.
