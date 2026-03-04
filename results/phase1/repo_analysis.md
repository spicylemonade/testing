# Repository Structure and Tooling Infrastructure Analysis

**Date:** 2026-03-04
**Author:** Research Agent
**Project:** Fast Combinatorial Protein Stability Optimization (StabOpt)

---

## 1. Top-Level Directory Structure

```
repo/
  .archivara/          # Core research automation infrastructure
  .opencode/           # OpenCode agent and tool configurations
  .git/                # Git version control
  .gitattributes       # Git attributes
  .gitignore           # Git ignore rules
  figures/             # Publication-quality figures (PNG + PDF)
  README.md            # Project README
  research_rubric.json # Master rubric tracking all phases/items
  results/             # Research artifacts organized by phase
  TASK_researcher_attempt_1.md  # Task instructions for this agent
```

---

## 2. .archivara/ Module Analysis

### 2.1 concept_evolve.py (628 lines)

**Purpose:** Cross-domain concept tree generation and traversal system that
delegates real work to OpenCode sub-agents. The Python script orchestrates
sub-agent launches and performs post-processing on filesystem artifacts.

**Key Components:**

| Component | Purpose |
|-----------|---------|
| `evolve(topic)` | Main concept generation: launches sub-agent to research topic across domains, generates 10+ concept cards, builds semantic bridge graph, produces steering directions |
| `probe(problem)` | Deep-dive into a specific bottleneck: free-association, forced bridges, anomaly results, steering directions |
| `reframe(problem)` | Reframes a problem across 8+ distinct domains with concrete technique mappings |
| `walk(seed, depth)` | Traverses concept tree walk paths, optionally filtering by seed concept |

**Architecture:**
- Sub-agents are launched via `opencode run --agent build --model anthropic/claude-opus-4-6`
- Results are written to `results/concept_evolve/` with sub-directories:
  - `tree/` — concept folders (NNN_slug/) each containing concept.json and README.md
  - `tree/index.json` — folder index
  - `tree/adjacency.json` — graph adjacency list
  - `tree/walk_paths.json` — pre-computed DFS walk paths
- Caching: evolve results are cached for 2 hours (configurable via `CONCEPT_EVOLVE_CACHE_TTL_SECONDS`)
- Locking: file-based lock prevents concurrent evolve runs
- Sub-agent timeout: 900s for evolve, 480s for probe, 360s for reframe

**Output Files:**
- `results/concept_evolve/concept_cards.json` — Array of concept card objects
- `results/concept_evolve/semantic_bridge.json` — Graph with nodes, edges, bridge_chains
- `results/concept_evolve/introspection.json` — associations, blind_spots, anomaly_results
- `results/concept_evolve/steering_directions.json` — Array of steering direction objects
- `results/concept_evolve/evolve_results.json` — Summary statistics
- `results/concept_evolve/summary.txt` — Human-readable summary

**Invocation:**
```bash
# CLI
python3 .archivara/concept_evolve.py evolve "topic description"
python3 .archivara/concept_evolve.py probe "specific bottleneck"
python3 .archivara/concept_evolve.py reframe "problem to reframe"
python3 .archivara/concept_evolve.py walk --seed "concept" --depth 4

# Via OpenCode tool wrapper (preferred)
# concept_evolve tool with command=evolve, topic="..."
# concept_evolve tool with command=probe, topic="..."
# concept_evolve tool with command=walk, seed="...", depth=4
```

### 2.2 semantic_scholar.py (277 lines)

**Purpose:** Robust Semantic Scholar API client for literature graph traversal,
paper search, citation analysis, and BibTeX export.

**API Endpoints Used:**
- `https://api.semanticscholar.org/graph/v1` — Paper search, citations, references
- `https://api.semanticscholar.org/recommendations/v1/papers` — Paper recommendations

**Key Functions:**

| Function | Purpose | Parameters |
|----------|---------|------------|
| `search(query, limit)` | Full-text paper search | Query string, result limit |
| `citations(paper_id, limit)` | Get papers citing a given paper | Semantic Scholar paper ID |
| `references(paper_id, limit)` | Get papers referenced by a given paper | Semantic Scholar paper ID |
| `recommend(paper_ids, limit)` | Get recommendations based on seed papers | List of paper IDs |
| `citation_graph(seed_query, roots, fanout)` | Build citation graph from seed query | Query, number of root papers, fanout per root |
| `bibtex_entry(paper_id)` | Generate BibTeX entry for a paper | Paper ID |

**Paper Fields Retrieved:** paperId, title, authors, year, citationCount, abstract,
externalIds (DOI, ArXiv, etc.), venue, url

**Reliability:**
- 6 retries with exponential backoff (0.75 * 2^attempt seconds, max 8s)
- 20-second timeout per request
- Robust JSON parsing with fallback for malformed responses

**Invocation:**
```bash
# CLI
python3 .archivara/semantic_scholar.py search "protein stability prediction" --limit 10
python3 .archivara/semantic_scholar.py citations <paperId> --limit 20
python3 .archivara/semantic_scholar.py references <paperId> --limit 20
python3 .archivara/semantic_scholar.py recommend <id1> <id2>
python3 .archivara/semantic_scholar.py graph "protein engineering" --roots 5 --fanout 5 --json --save results/graph.json
python3 .archivara/semantic_scholar.py bibtex <paperId> >> sources.bib

# Via OpenCode tool wrapper (preferred)
# semantic_scholar tool with command=search, query="...", limit=10
# semantic_scholar tool with command=bibtex, query="<paperId>"
```

### 2.3 opencode.json

**Purpose:** Master OpenCode configuration defining model, agents, tools, and permissions.

**Configuration:**
- Model: `anthropic/claude-opus-4-6`
- Default agent: `build`
- Provider: Anthropic (API key and base URL from environment)
- Global permissions: edit, webfetch, websearch, todoread, todowrite, bash (all allow)

### 2.4 logs/ directory

**Purpose:** Stores execution logs from agent runs and sub-processes.

---

## 3. .opencode/ Module Analysis

### 3.1 agents/ directory

Contains markdown-based agent definitions:

#### concept-tree-explorer.md
- **Description:** Explore concept trees and identify high-value concept paths
- **Mode:** subagent (can be launched by primary agents)
- **Tools:** webfetch, websearch, todoread, todowrite (read-only, no write/edit)
- **Directive:** Focus on traversing concept folders, identifying missing links, proposing experiments

#### literature-graph-miner.md
- **Description:** Mine citation graphs for transferable ideas and supporting evidence
- **Mode:** subagent
- **Tools:** webfetch, websearch, todoread, todowrite (read-only)
- **Directive:** Prioritize citation chains connecting distant domains, report actionable leads

### 3.2 tools/ directory

#### concept_evolve.ts
- **Type:** TypeScript OpenCode plugin tool
- **Purpose:** Wraps `concept_evolve.py` as an OpenCode-native tool
- **Execution:** Calls `python3 .archivara/concept_evolve.py <command> [args]`
- **Parameters:** command (evolve/probe/reframe/walk), topic, seed, depth
- **Timeout:** 1,200,000 ms (20 minutes)
- **Max buffer:** 10 MB

#### semantic_scholar.ts
- **Type:** TypeScript OpenCode plugin tool
- **Purpose:** Wraps `semantic_scholar.py` as an OpenCode-native tool
- **Execution:** Calls `python3 .archivara/semantic_scholar.py <command> [args]`
- **Parameters:** command (search/citations/references/recommend/graph/bibtex), query, limit
- **Auto-flags:** Adds `--json` for all commands except bibtex

### 3.3 package.json
- **Dependencies:** `@opencode-ai/plugin` v1.2.15
- **Purpose:** Required for TypeScript tool compilation

---

## 4. Agent Roles and Tool Permissions

| Agent | Description | Mode | concept_evolve | semantic_scholar | bash | write/edit | web |
|-------|------------|------|----------------|-----------------|------|------------|-----|
| **orchestrator** | Planning-only rubric author | primary | NO | default | YES (except concept_evolve) | YES | YES |
| **researcher** | Execution-heavy research worker | primary | YES | YES | YES | YES | YES |
| **writer** | Paper writing and synthesis | primary | NO | YES | YES | YES | YES |
| **reviewer** | Peer review and quality control | primary | NO | YES | YES | YES | YES |
| **concept_worker** | ConceptEvolve sub-worker | primary | NO (prevents recursion) | YES | YES | YES (read+write+edit) | YES |
| **concept-tree-explorer** | Concept path explorer | subagent | NO | NO | NO | NO | YES (read-only) |
| **literature-graph-miner** | Citation graph miner | subagent | NO | NO | NO | NO | YES (read-only) |

**Key Design Decisions:**
1. Only the `researcher` agent has ConceptEvolve access — prevents recursive sub-agent spawning
2. Subagents (concept-tree-explorer, literature-graph-miner) are read-only — cannot modify files
3. `concept_worker` explicitly blocks concept_evolve to prevent infinite recursion
4. All primary agents have full bash access for flexible tool installation

---

## 5. ConceptEvolve Capabilities and Usage

### 5.1 Core Commands

**evolve** — Full concept tree generation
- Input: Topic string (research problem description)
- Process: Launches sub-agent that researches across 3+ domains, generates 10+ concept cards, builds semantic bridge graph
- Output: Concept cards, semantic bridge, introspection data, steering directions, concept tree folders
- Time budget: ~15 minutes (900s sub-agent timeout)
- Caching: Results cached for 2 hours

**probe** — Deep bottleneck analysis
- Input: Specific problem/bottleneck description
- Process: Researches bottleneck from multiple angles, generates forced bridges to distant domains
- Output: Associations, forced bridges, anomaly results, steering directions, validation checks
- Time budget: ~8 minutes (480s timeout)

**reframe** — Cross-domain reframing
- Input: Problem description
- Process: Reframes in 8+ distinct domains with concrete technique mappings
- Output: Domain reframings with key insights, suggested techniques, and mapping-back instructions
- Time budget: ~6 minutes (360s timeout)

**walk** — Concept tree traversal
- Input: Optional seed concept, depth (1-8)
- Process: Filters pre-computed DFS walk paths by seed, returns matching paths
- Output: Selected concept paths from the walk graph
- Prerequisite: Must run `evolve` first to generate walk paths

### 5.2 Concept Tree Structure

Each concept in the tree has:
```
results/concept_evolve/tree/NNN_slug/
  concept.json    # Full concept card with:
                  #   symbolic_name, description, domains,
                  #   mathematical_formalization,
                  #   analogical_connections,
                  #   implementation_hypothesis,
                  #   experiment_seed, folder_plan
  README.md       # Topic context, domains, implementation backlog
  literature.json # Related papers (if created by sub-agent)
```

### 5.3 Steering Directions

Steering directions are key outputs for guiding research:
```json
{
  "direction": "specific research direction",
  "rationale": "why this direction is promising",
  "first_step": "concrete first action",
  "expected_signal": "what success looks like"
}
```

---

## 6. Semantic Scholar API Client Features

### 6.1 Search and Discovery
- **Full-text search** with configurable result limits
- **Citation mining** — find all papers citing a given work
- **Reference mining** — find all papers referenced by a given work
- **Recommendations** — ML-based paper recommendations from seed papers
- **Citation graphs** — automated multi-hop graph construction

### 6.2 BibTeX Export
- Automatic key generation (first author last name + year)
- Includes DOI, ArXiv IDs, venue, all authors
- Direct append-to-file workflow: `>> sources.bib`

### 6.3 Reliability Features
- Exponential backoff retry (6 attempts)
- Graceful error handling with JSON error output
- Fields retrieved: paperId, title, authors, year, citationCount, abstract, externalIds, venue, url

---

## 7. Research Infrastructure Summary

### Available Tools for This Project

1. **Literature Research:** Semantic Scholar API (search, citations, references, recommendations, graphs, BibTeX)
2. **Web Research:** websearch (Exa AI), webfetch (URL content retrieval)
3. **Concept Exploration:** ConceptEvolve (evolve, probe, reframe, walk)
4. **Subagent Delegation:** concept-tree-explorer, literature-graph-miner
5. **File Operations:** read, write, edit, glob, grep
6. **Execution:** bash (with full permissions including pip, git, python, etc.)
7. **Task Management:** todoread, todowrite

### Workflow for This Research Project

1. **Phase 1 (Current):** Use websearch, Semantic Scholar, and ConceptEvolve to conduct literature review and identify key approaches
2. **Phase 2:** Use bash + pip to scaffold Python package; implement baselines using torch, transformers, biopython
3. **Phase 3:** Implement core algorithms; use ConceptEvolve probe for novel heuristics
4. **Phase 4:** Run experiments on A100 GPU; generate publication-quality figures
5. **Phase 5:** Synthesize results; finalize package; validate citations

### Key Configuration Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Model | claude-opus-4-6 | Used for all agents |
| ConceptEvolve cache TTL | 7200s (2h) | Prevents redundant sub-agent runs |
| Evolve timeout | 900s | Per attempt, up to 2 attempts |
| Probe timeout | 480s | Per attempt, up to 2 attempts |
| Reframe timeout | 360s | Per attempt, up to 2 attempts |
| S2 API retries | 6 | With exponential backoff |
| S2 request timeout | 20s | Per API call |

---

## 8. research_rubric.json Schema

The rubric is the master tracking document with:
- **5 phases** containing 27 total items
- **Item fields:** id, description, acceptance_criteria, status (pending/in_progress/completed/failed), notes, error
- **Agent status tracking:** orchestrator (completed), researcher (in_progress), writer (pending), reviewer (pending)
- **Summary counters:** total_items, completed, in_progress, failed, pending

The rubric must be updated before and after each item to maintain progress visibility.

---

## 9. Identified Dependencies and Setup Needs

For the full pipeline implementation, the following will need to be installed:

### Python Packages (via pip/uv)
- `torch` — GPU computation, model inference
- `transformers` — ESM-2 model loading
- `biopython` — PDB file parsing
- `numpy`, `scipy` — Numerical computation
- `pandas`, `pyarrow` — Data processing and parquet I/O
- `matplotlib`, `seaborn` — Publication-quality figures
- `pytest` — Test framework

### ML Model Weights (downloaded at runtime)
- ESM-2 650M (`facebook/esm2_t33_650M_UR50D`)
- ProteinMPNN (from GitHub: `dauparas/ProteinMPNN`)

### External Data
- Mega-scale dataset (~750K variants, supplementary tables)
- FireProtDB (REST API bulk export)

---

*Document generated as part of item_001 acceptance criteria. 200+ lines confirmed.*
