# Repository Structure and Tooling Analysis

## 1. Repository Overview

The repository is a research workspace managed by the Archivara system for investigating the **univalent Bloch constant** B_u. It uses OpenCode as the agent framework with multiple specialized agents (orchestrator, researcher, writer, reviewer) coordinated through a research rubric.

### Directory Layout
```
.archivara/           # Core tooling scripts
  concept_evolve.py   # ConceptEvolve: concept-tree exploration via sub-agents
  semantic_scholar.py  # Semantic Scholar API wrapper for literature search
  opencode.json       # Agent configuration and permissions
  logs/               # Execution logs
.opencode/            # OpenCode framework
  agents/             # Agent definitions
  tools/              # Custom tool definitions
  package.json        # Node dependencies
  node_modules/       # Installed packages
results/              # Research output (organized by phase)
  concept_evolve/     # ConceptEvolve output (concept cards, bridge, steering)
  phase1/             # Phase 1: Literature review & analysis
figures/              # Publication-quality figures (PNG + PDF)
research_rubric.json  # Central task tracking (30 items across 5 phases)
sources.bib           # Bibliography (to be built)
```

## 2. Modules in .archivara/ with APIs

### 2.1 concept_evolve.py
**Purpose**: Cross-domain concept exploration using OpenCode sub-agents.

**Commands**:
- `evolve <topic>`: Generates 10+ concept cards across multiple domains, builds a semantic bridge graph, produces steering directions. Launches a sub-agent that does websearch, semantic scholar queries, and writes structured JSON files.
- `probe <problem>`: Deep-dives into a specific bottleneck. Produces associations, forced bridges, anomaly results, and steering directions.
- `reframe <problem>`: Reframes a problem in 8+ distinct domains with concrete techniques from each.
- `walk [--seed SEED] [--depth N]`: Traverses the concept tree's walk paths, optionally filtered by seed term.

**Output Formats**:
- `results/concept_evolve/concept_cards.json`: Array of concept card objects
- `results/concept_evolve/semantic_bridge.json`: Graph with nodes, edges, bridge_chains
- `results/concept_evolve/introspection.json`: Associations, blind spots, anomaly results
- `results/concept_evolve/steering_directions.json`: Array of direction objects
- `results/concept_evolve/tree/`: Per-concept folders (NNN_slug/) with concept.json, README.md, literature.json
- `results/concept_evolve/tree/walk_paths.json`: All graph traversal paths
- `results/concept_evolve/tree/adjacency.json`: Graph adjacency structure
- `results/concept_evolve/tree/index.json`: Concept folder index

**Key Implementation Details**:
- Uses file-based locking (fcntl) to prevent concurrent evolve runs
- Cache TTL of 7200 seconds (2 hours) for evolve results
- Sub-agent timeout: 900s for evolve, 480s for probe, 360s for reframe
- Falls back gracefully if sub-agent fails (retries up to 2 times)
- Post-processes filesystem artifacts to build adjacency graphs and walk paths

### 2.2 semantic_scholar.py
**Purpose**: Robust wrapper around Semantic Scholar Graph API v1.

**Commands**:
- `search <query> [--limit N] [--json] [--save PATH]`: Full-text paper search
- `citations <paperId> [--limit N]`: Papers citing a given paper
- `references <paperId> [--limit N]`: Papers referenced by a given paper
- `recommend <paperId1> [paperId2...] [--limit N]`: Paper recommendations
- `graph <query> [--roots N] [--fanout N]`: Build citation graph (2-hop: search roots → references + citations)
- `bibtex <paperId>`: Generate BibTeX entry

**Output Fields**: paperId, title, year, citationCount, authors, venue, abstract, externalIds, url

**Robustness**: 6 retries with exponential backoff (0.75 * 2^attempt seconds). Handles HTTP 429 (rate limiting) gracefully.

## 3. ConceptEvolve Commands and Output Formats

The ConceptEvolve system uses a tree metaphor:
- **Evolve**: Seeds the tree with 10+ concept cards, builds a semantic bridge graph
- **Probe**: Deep investigation of a specific bottleneck (leaf-level analysis)
- **Reframe**: Multi-domain perspective expansion (branch exploration)
- **Walk**: Path traversal through the concept tree (route planning)

The concept tree for this project contains 12 concepts across domains including complex analysis, potential theory, optimization, probability, spectral theory, and machine learning. Key concepts:
1. Harmonic symmetry extremal slits (Carroll-Ortega-Cerda's approach)
2. Polya-Chebotarev capacity optimization
3. Schwarz-Christoffel interval arithmetic
4. Brownian lifetime-inradius duality
5. Hexagonal lattice local minimality
6. Level set conformal shape optimization
7. Variational schlicht function perturbation
8. Hyperbolic metric density bounds
9. Spectral gap torsion rigidity bridge
10. Conformal welding boundary correspondence
11. Quasiconformal deformation sensitivity
12. Neural surrogate conformal optimizer

25 walk paths connect these concepts, with the most connected hub being `hyperbolic_metric_density_bounds` (appears as endpoint in many paths).

## 4. Semantic Scholar Tool Capabilities

The tool provides access to the full Semantic Scholar academic graph:
- **Search**: Keyword-based paper discovery (returns paperId, title, authors, year, citations, abstract, venue, DOIs)
- **Citation/Reference traversal**: Forward and backward citation graph exploration
- **Recommendations**: Finds papers similar to given seed papers
- **Graph building**: Automated 2-hop citation graph construction
- **BibTeX export**: Direct bibliography entry generation

The tool is subject to rate limiting (HTTP 429). The built-in exponential backoff handles transient throttling, but sustained heavy use requires spacing requests.

## 5. Agent Roles and Permissions

From `opencode.json`:

| Agent | Description | ConceptEvolve | Semantic Scholar | Other Tools |
|-------|------------|---------------|-----------------|-------------|
| orchestrator | Planning-only rubric author | Denied | Default | bash (except concept_evolve) |
| researcher | Execution-heavy research worker | Enabled | Enabled | All standard tools |
| writer | Paper writing and synthesis | Denied | Enabled | All standard tools |
| reviewer | Peer review and QC | Denied | Enabled | All standard tools |
| concept_worker | ConceptEvolve sub-worker | Denied (no recursion) | Enabled | websearch, webfetch, bash, read, write, edit |

Key design decisions:
- Only the researcher agent can trigger ConceptEvolve (prevents infinite recursion)
- The concept_worker cannot call concept_evolve (anti-recursion guard)
- All agents have Semantic Scholar access for literature verification
- The model is `anthropic/claude-opus-4-6` across all agents
- All bash permissions are allowed; no tool restrictions beyond concept_evolve

## 6. Research Rubric Structure

The rubric tracks 30 items across 5 phases:
1. **Problem Analysis & Literature Review** (items 1-7): Repo analysis, literature search, bibliography, deep dives
2. **Baseline Implementation & Metrics** (items 8-12): Numerical toolkit, reproduction, domain families
3. **Core Research & Novel Approaches** (items 13-19): New bounds, variational analysis, concept exploration
4. **Experiments & Evaluation** (items 20-24): Optimization, validation, sensitivity
5. **Analysis & Documentation** (items 25-30): Report, summary, reproducibility, figures

Each item has: id, description, acceptance_criteria, status (pending/in_progress/completed/failed), notes, error.

## 7. Available Infrastructure for Research

- **Python 3**: Primary language for computation
- **mpmath**: Available for arbitrary-precision and interval arithmetic
- **numpy/scipy**: Numerical computation backbone
- **matplotlib**: Plotting framework
- **Semantic Scholar API**: Literature search and citation graph
- **Web search/fetch**: Access to arXiv, journal sites, Wikipedia
- **ConceptEvolve**: Cross-domain concept exploration
- **Git**: Version control for all artifacts

## 8. Key Research Tooling Gaps (to be filled)

The following tools would enhance the research:
- **Interval arithmetic library**: mpmath's `iv` module or `flamp` for rigorous bounds
- **SDP solver**: CVXPY with SCS/MOSEK backend for semidefinite programming
- **Schwarz-Christoffel toolbox**: `scpy` or custom implementation
- **High-precision arithmetic**: mpmath or arb for 50+ digit computations
- **Publication plotting**: seaborn + matplotlib with tuned rcParams
