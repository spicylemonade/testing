# Repository Structure & Tooling Analysis

## 1. Modules in `.archivara/`

| File | Purpose | Key Details |
|------|---------|-------------|
| `concept_evolve.py` (628 lines) | ConceptEvolve: concept-tree exploration via OpenCode sub-agents. Supports `evolve`, `probe`, `reframe`, and `walk` commands. Sub-agents do real work via tools (bash, read, write, websearch, webfetch, semantic_scholar). Python orchestrates launches and post-processes filesystem artifacts. | Uses file locking (`fcntl`) for concurrent safety (line 399). Caches evolve results with configurable TTL (line 33: `EVOLVE_CACHE_TTL_SECONDS`). Results stored in `results/concept_evolve/`. |
| `semantic_scholar.py` (277 lines) | Robust Semantic Scholar API wrapper for literature graph traversal. Supports search, citations, references, recommendations, citation graph building, and BibTeX export. | Retries with exponential backoff up to 6 attempts (line 30). Fields requested: paperId, title, authors, year, citationCount, abstract, externalIds, venue, url (line 18). |
| `opencode.json` (88 lines) | OpenCode configuration file. Defines model (`anthropic/claude-opus-4-6`), default agent (`build`), provider settings, permission allowlists, and agent definitions. | 5 agents defined: orchestrator, researcher, writer, reviewer, concept_worker (lines 37-87). |
| `logs/` | Directory for runtime logs from concept_evolve and other processes. | Empty at analysis time. |

## 2. Modules in `.opencode/`

| File/Dir | Purpose |
|----------|---------|
| `agents/concept-tree-explorer.md` (12 lines) | Subagent for exploring concept trees and identifying high-value paths. Read-only (no write/edit), has websearch/webfetch access. |
| `agents/literature-graph-miner.md` (12 lines) | Subagent for mining citation graphs for transferable ideas. Read-only, has websearch/webfetch access. |
| `tools/concept_evolve.ts` (33 lines) | TypeScript tool wrapper that invokes `concept_evolve.py` via `execFileSync`. Timeout: 1,200,000ms (20 minutes). Supports evolve/probe/reframe/walk commands (line 8). |
| `tools/semantic_scholar.ts` (38 lines) | TypeScript tool wrapper that invokes `semantic_scholar.py`. Auto-appends `--json` flag for all commands except `bibtex` (line 28). |
| `package.json` | Node.js package config for OpenCode plugin infrastructure. |
| `bun.lock`, `node_modules/` | Bun package manager artifacts. |

## 3. Available Tools

| Tool | Type | Description |
|------|------|-------------|
| **concept_evolve** | Custom OpenCode tool | Cross-domain concept tree exploration. Commands: `evolve` (generate concept cards + semantic bridge), `probe` (deep-dive on bottleneck), `reframe` (multi-domain reframing), `walk` (traverse concept paths). |
| **semantic_scholar** | Custom OpenCode tool | Academic paper search, citation/reference traversal, recommendations, citation graph building, BibTeX export. |
| **websearch** | Built-in | Exa AI web search with configurable result counts, search types (auto/fast/deep), and live crawl modes. |
| **webfetch** | Built-in | URL content fetching with markdown/text/html format options. |
| **bash** | Built-in | Shell command execution with persistent session. |
| **read/write/edit** | Built-in | File system operations. |
| **glob/grep** | Built-in | Pattern-based file and content search. |
| **task** | Built-in | Subagent delegation (general, explore, concept-tree-explorer, literature-graph-miner). |

## 4. Agent Roles

| Agent | Role | ConceptEvolve Access | Semantic Scholar Access |
|-------|------|---------------------|----------------------|
| **orchestrator** | Planning-only rubric author. Creates research plans, never executes experiments. | No (explicitly denied, line 43-46 of opencode.json) | No |
| **researcher** | Execution-heavy research worker. Runs experiments, implements code, conducts searches. | Yes | Yes |
| **writer** | Paper writing and synthesis worker. Produces final documents and summaries. | No | Yes |
| **reviewer** | Peer review and quality control worker. Validates claims and checks methodology. | No | Yes |
| **concept_worker** | ConceptEvolve sub-worker. Launched by concept_evolve.py for concept generation. Cannot recursively invoke concept_evolve. | No (prevents recursion) | Yes |

## 5. Results Directory Structure Conventions

```
results/
  phase1/          # Literature review, repo analysis, code survey
  phase2/          # Baseline implementation, known records, sieve, metrics
  phase3/          # Novel approaches: tail predictor, probabilistic model, search engine
  phase4/          # Search execution, verification, comparison, ablation
  phase5/          # Final summary, verification script, visualizations, tweet
  concept_evolve/  # ConceptEvolve artifacts
    concept_cards.json
    semantic_bridge.json
    introspection.json
    steering_directions.json
    evolve_results.json
    tree/            # Concept folders (NNN_slug/)
      index.json
      adjacency.json
      walk_paths.json
    .debug/          # Sub-agent debug logs
figures/             # Publication-grade plots (PNG 300dpi + PDF)
sources.bib          # BibTeX references (cumulative)
```

## 6. Key File References

1. `.archivara/concept_evolve.py:62` — `_run_sub_agent()` function that launches OpenCode sub-agents
2. `.archivara/concept_evolve.py:281` — `_EVOLVE_PROMPT` template with full instructions for concept generation
3. `.archivara/semantic_scholar.py:79` — `search()` function for paper discovery
4. `.archivara/semantic_scholar.py:112` — `citation_graph()` for building multi-hop citation networks
5. `.archivara/opencode.json:36` — Agent definitions with tool permissions
6. `.opencode/tools/concept_evolve.ts:13` — Tool execution bridge from TypeScript to Python
7. `.opencode/agents/concept-tree-explorer.md:1` — Subagent definition for concept path exploration
