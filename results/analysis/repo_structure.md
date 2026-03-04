# Repository Structure and Archivara Framework Analysis

## 1. Modules in `.archivara/`

The `.archivara/` directory contains the core orchestration infrastructure:

### `concept_evolve.py` (628 lines)
The central research ideation engine. It orchestrates sub-agents to generate cross-domain concept cards and semantic bridges. Key components:

- **Sub-agent runner** (`_run_sub_agent`, line 62): Launches OpenCode sub-agents via `opencode run --agent build --model <model>` as child processes. The sub-agent receives a detailed prompt and writes results directly to the filesystem. The parent process only monitors exit codes—it never parses stdout for structured data (line 68-70).
- **Evolve command** (`evolve()`, line 387): The main concept generation pipeline:
  1. Checks for cached results with a configurable TTL (default 7200s, line 33)
  2. Acquires an exclusive file lock to prevent duplicate runs (line 397-401)
  3. Dispatches the `_EVOLVE_PROMPT` (line 281) to a sub-agent requesting 10+ concept cards, semantic bridge graph, introspection analysis, and steering directions
  4. Post-processes artifacts: builds adjacency graph from bridge edges (line 202), generates DFS walk paths (line 214), creates concept folder scaffolding (line 235)
  5. Writes `evolve_results.json` with summary statistics
- **Probe command** (`probe()`, line 494): Deep investigation of a specific bottleneck. Dispatches `_PROBE_PROMPT` requesting free-associations, forced bridges to distant domains, and steering directions.
- **Reframe command** (`reframe()`, line 525): Problem reframing across 8+ domains. Dispatches `_REFRAME_PROMPT` requesting domain-specific reinterpretations with concrete techniques mapped back to the original problem.
- **Walk command** (`walk()`, line 549): Traverses the pre-computed concept graph paths, optionally filtered by seed concept and depth.

### `semantic_scholar.py` (277 lines)
Literature search and citation graph traversal utility. Interfaces with the Semantic Scholar Graph API v1:

- **API interface**: Uses `urllib.request` with retry logic (6 attempts, exponential backoff, line 30-38). Queries fields: `paperId, title, authors, year, citationCount, abstract, externalIds, venue, url`.
- **Commands**: `search` (keyword search), `citations`/`references` (citation graph traversal), `recommend` (paper recommendations via POST), `graph` (builds a citation subgraph from seed query with configurable roots and fanout), `bibtex` (generates BibTeX entries).
- **Citation graph builder** (`citation_graph()`, line 112): Seeds with keyword search, then expands each root by fetching its references and citations up to a configurable fanout, building a node/edge graph.

### `opencode.json` (88 lines)
Configuration file defining the model (`anthropic/claude-opus-4-6`), default agent (`build`), provider settings, global tool/permission policies, and per-agent overrides.

### `logs/`
Directory for operational logs from agent runs.

## 2. How `concept_evolve.py` Orchestrates Sub-Agents

The orchestration model is **fire-and-forget with filesystem contracts**:

1. **Prompt construction**: Each command (`evolve`, `probe`, `reframe`) formats a detailed prompt string with the topic and target filesystem paths (e.g., `_EVOLVE_PROMPT.format(topic=..., results_dir=..., tree_dir=...)`, line 414-418).
2. **Sub-agent invocation**: `_run_sub_agent()` spawns `opencode run --agent build --model <model> <prompt>` as a subprocess (line 73-81). The sub-agent has full tool access (bash, write, edit, websearch, webfetch, semantic_scholar) and writes JSON files directly to the specified paths.
3. **Result collection**: After the sub-agent exits, the parent reads the expected JSON files from disk using `_read_json()` which tolerates markdown fences and leading text (line 127-156).
4. **Retry logic**: If expected outputs are missing, the sub-agent is re-launched (up to 2 attempts, line 421-429).
5. **Post-processing**: Mechanical graph operations (adjacency construction, DFS walk, folder scaffolding) are performed by the Python script, not the sub-agent (line 446-451).
6. **Caching**: Results are cached with timestamps. Subsequent calls within the TTL return cached results without re-running the sub-agent (line 172-189).

## 3. How `semantic_scholar.py` Interfaces with the API

The utility uses the Semantic Scholar Graph API v1 (`https://api.semanticscholar.org/graph/v1`) and Recommendations API v1. All requests use `urllib.request` (no external dependencies) with:

- **Retry strategy**: 6 attempts with exponential backoff (0.75s * 2^attempt, capped at 8s) for transient errors (line 30-40).
- **Rate limiting**: Handled implicitly through retries and backoff.
- **Field selection**: Requests a fixed set of fields via the `fields` query parameter (line 18).
- **Output normalization**: `_paper()` normalizes API responses to a consistent dict format (line 43-57). `_pretty_paper()` formats for human-readable display (line 60-76).
- **Recommendations**: Uses POST endpoint with `positivePaperIds` payload (line 103-109).
- **BibTeX generation**: Fetches paper metadata and constructs BibTeX entries with heuristic citation keys (first author last name + year, line 146-175).

## 4. The 5 Agent Roles and Their Tool Permissions

Defined in `.archivara/opencode.json` (lines 36-87):

| Agent | Description | concept_evolve | semantic_scholar | bash | websearch | webfetch |
|-------|-------------|:-:|:-:|:-:|:-:|:-:|
| **orchestrator** | Planning-only rubric author | ✗ (denied) | - | ✓ (except CE) | ✓ | ✓ |
| **researcher** | Execution-heavy research worker | ✓ | ✓ | ✓ | ✓ | ✓ |
| **writer** | Paper writing and synthesis | ✗ | ✓ | ✓ | ✓ | ✓ |
| **reviewer** | Peer review and QC | ✗ | ✓ | ✓ | ✓ | ✓ |
| **concept_worker** | ConceptEvolve sub-worker | ✗ (prevents recursion) | ✓ | ✓ | ✓ | ✓ |

Key design decisions:
- The **orchestrator** is explicitly denied concept_evolve access to prevent accidental expensive sub-agent launches during planning.
- The **concept_worker** lacks concept_evolve to prevent recursive sub-agent spawning (a CE sub-agent cannot launch another CE sub-agent).
- All agents share basic tool access (bash, read, write, edit, websearch, webfetch).

## 5. Modules in `.opencode/`

### `.opencode/agents/`
Two subagent definitions:
- **concept-tree-explorer.md**: Read-only subagent (write/edit disabled) for traversing concept folders, identifying missing links, and proposing next experiments. Has websearch/webfetch access.
- **literature-graph-miner.md**: Read-only subagent for mining citation graphs and reporting actionable cross-domain leads.

### `.opencode/tools/`
Two custom tool wrappers (TypeScript, using `@opencode-ai/plugin`):
- **concept_evolve.ts** (33 lines): Wraps `concept_evolve.py` CLI invocation. Accepts `command` (evolve/probe/reframe/walk), `topic`, `seed`, `depth`. Timeout: 1.2M ms (20 minutes). Executes via `execFileSync`.
- **semantic_scholar.ts** (38 lines): Wraps `semantic_scholar.py` CLI. Accepts `command`, `query`, `limit`. Automatically appends `--json` flag for non-bibtex commands.

## 6. Data Flow Diagram

```
                    ┌──────────────────┐
                    │   ORCHESTRATOR   │
                    │  (rubric author) │
                    └────────┬─────────┘
                             │ Creates research_rubric.json
                             ▼
                    ┌──────────────────┐
                    │   RESEARCHER     │◄──── concept_evolve tool
                    │ (execution hub)  │◄──── semantic_scholar tool
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌────────────┐  ┌────────────┐  ┌──────────┐
     │ CE Sub-    │  │ Literature │  │ Concept  │
     │ agent      │  │ Graph      │  │ Tree     │
     │ (concept_  │  │ Miner      │  │ Explorer │
     │  worker)   │  │ (subagent) │  │(subagent)│
     └──────┬─────┘  └─────┬──────┘  └────┬─────┘
            │               │              │
            ▼               ▼              ▼
     results/concept_evolve/    sources.bib
     ├── concept_cards.json     results/literature/
     ├── semantic_bridge.json
     ├── steering_directions.json
     ├── tree/NNN_concept/
     │   ├── concept.json
     │   ├── README.md
     │   └── literature.json
     └── ...
                             │
                    ┌────────┴─────────┐
                    │     WRITER       │
                    │ (paper synthesis)│
                    └────────┬─────────┘
                             │ research_paper.tex
                             ▼
                    ┌──────────────────┐
                    │    REVIEWER      │
                    │   (QC/review)    │
                    └──────────────────┘
```

The orchestrator creates the rubric; the researcher executes all items, delegating to concept_evolve (which spawns concept_worker sub-agents) and subagent tools (literature-graph-miner, concept-tree-explorer) for discovery work. The researcher produces code (`src/`), data (`results/`), and figures (`figures/`). The writer synthesizes these into `research_paper.tex` with `sources.bib`. The reviewer performs quality control on the final outputs.

**Word count: ~900 words (excluding table and diagram)**
