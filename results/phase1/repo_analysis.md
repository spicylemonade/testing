# Repository Structure & Infrastructure Analysis

**Project**: Minimal Gravity Simulation  
**Analysis Date**: 2026-03-02  
**Rubric Item**: item_001  

---

## 1. Top-Level Directory Layout

```
repo/
  .archivara/            # Archivara research tooling (gitignored)
  .git/                  # Git repository metadata
  .gitattributes         # Git LFS tracking rules for binary data
  .gitignore             # Ignore rules for secrets, logs, tool configs
  .opencode/             # OpenCode agent/tool configuration (gitignored)
  figures/               # Output directory for generated plots (empty at init)
  results/               # Output directory for research artifacts (empty at init)
  opencode.json          # OpenCode CLI configuration
  README.md              # Project README (placeholder: "# testing")
  research_rubric.json   # Master rubric tracking 25 items across 5 phases
  TASK_researcher_attempt_1.md  # Previous task attempt log (gitignored)
```

### 1.1 Directory Purposes

| Directory | Purpose | Tracked in Git |
|-----------|---------|----------------|
| `.archivara/` | Houses research automation scripts (concept_evolve.py, semantic_scholar.py) and logs | No (.gitignore) |
| `.opencode/` | OpenCode agent definitions and custom tool wrappers | No (.gitignore) |
| `figures/` | Destination for all generated plots (PNG 300 DPI + PDF) | Yes (empty) |
| `results/` | Destination for all research data artifacts (JSON, CSV, Markdown) | Yes (empty) |
| `src/` | *To be created* - Python source modules for the gravity simulator | Yes |
| `tests/` | *To be created* - pytest test suite | Yes |
| `benchmarks/` | *To be created* - Performance benchmarking scripts | Yes |

---

## 2. Available Tooling

### 2.1 ConceptEvolve (`concept_evolve.py`)

**Location**: `.archivara/concept_evolve.py` (524 lines)  
**Purpose**: Concept-tree generation and traversal for structured research exploration.

#### Commands

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `evolve` | Generate concept cards, semantic bridge, and steering directions | `topic` (positional) |
| `probe` | Deep dive into a specific bottleneck or sub-problem | `problem` (positional) |
| `reframe` | Reframe a problem across 8+ distinct domains | `problem` (positional) |
| `walk` | Traverse existing concept tree paths | `--seed`, `--depth` (1-8) |

#### Architecture Details

- **Sub-agent execution**: Runs `opencode run --agent build --model anthropic/claude-opus-4-6 --format json` as subprocess
- **Model configuration**: Uses `CONCEPT_EVOLVE_MODEL` or `OPENCODE_MODEL` env vars, defaults to `anthropic/claude-opus-4-6`
- **Output directory**: `results/concept_evolve/`
- **Artifacts produced by `evolve`**:
  - `concept_cards.json` - Array of concept card objects
  - `semantic_bridge.json` - Graph with nodes, edges, bridge_chains
  - `introspection.json` - Associations, blind spots, anomaly results
  - `steering_directions.json` - Actionable research directions
  - `literature_seed.json` - Initial Semantic Scholar results
  - `evolve_results.json` - Summary statistics
  - `summary.txt` - Human-readable summary
  - `tree/` - Materialized concept folders with:
    - `index.json` - Concept index
    - `adjacency.json` - Graph adjacency list
    - `walk_paths.json` - Pre-computed walk paths
    - `NNN_slug/concept.json` - Individual concept metadata
    - `NNN_slug/literature.json` - Per-concept Semantic Scholar results
    - `NNN_slug/README.md` - Concept backlog template

#### Concept Card Schema

Each concept card includes:
- `symbolic_name`: Identifier
- `description`: Natural language description
- `domains`: Array of relevant domains
- `mathematical_formalization`: Formal notation
- `analogical_connections`: Cross-domain bridges
- `implementation_hypothesis`: Coding plan
- `experiment_seed`: Testable prediction
- `folder_plan`: File structure for the concept module

### 2.2 Semantic Scholar (`semantic_scholar.py`)

**Location**: `.archivara/semantic_scholar.py` (277 lines)  
**Purpose**: Literature search, citation graph traversal, and BibTeX export via Semantic Scholar API.

#### Commands

| Command | Description | Key Parameters |
|---------|-------------|----------------|
| `search` | Keyword search for papers | `query`, `--limit`, `--json`, `--save` |
| `citations` | Papers citing a given paper | `paper_id`, `--limit` |
| `references` | References of a given paper | `paper_id`, `--limit` |
| `recommend` | Paper recommendations from seed papers | `paper_ids`, `--limit` |
| `graph` | Build citation subgraph from seed query | `query`, `--roots`, `--fanout` |
| `bibtex` | Export BibTeX entry for a paper ID | `paper_id` |

#### API Details

- **Base URL**: `https://api.semanticscholar.org/graph/v1`
- **Fields requested**: paperId, title, authors, year, citationCount, abstract, externalIds, venue, url
- **Retry logic**: 6 attempts with exponential backoff (0.75 * 2^attempt seconds, max 8s)
- **Paper record**: Normalized dict with paperId, title, year, citationCount, authors, venue, abstract, externalIds, url

### 2.3 OpenCode Custom Tool Wrappers

#### `concept_evolve.ts` (`.opencode/tools/`)

- TypeScript wrapper exposing ConceptEvolve as an OpenCode native tool
- Accepts `command`, `topic`, `seed`, `depth` parameters
- Executes `.archivara/concept_evolve.py` via `execFileSync`
- Available as `concept_evolve` tool in the OpenCode CLI

#### `semantic_scholar.ts` (`.opencode/tools/`)

- TypeScript wrapper exposing Semantic Scholar as an OpenCode native tool
- Accepts `command`, `query`, `limit` parameters
- Executes `.archivara/semantic_scholar.py` via `execFileSync`
- Available as `semantic_scholar` tool in the OpenCode CLI

### 2.4 OpenCode Subagents

#### `concept-tree-explorer` (`.opencode/agents/concept-tree-explorer.md`)

- **Mode**: subagent
- **Capabilities**: Read-only (no write/edit)
- **Purpose**: Traverse concept folders, identify missing links, propose next experiments
- **Use case**: Systematic concept path analysis during Phase 1 and Phase 5

#### `literature-graph-miner` (`.opencode/agents/literature-graph-miner.md`)

- **Mode**: subagent
- **Capabilities**: Read-only (no write/edit)
- **Purpose**: Mine citation graphs for transferable ideas and supporting evidence
- **Focus**: Citation chains connecting distant domains, actionable leads
- **Use case**: Literature review expansion (item_002, item_005)

---

## 3. Configuration Files

### 3.1 `opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-opus-4-6",
  "default_agent": "build",
  "enabled_providers": ["anthropic"],
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}",
        "baseURL": "{env:ANTHROPIC_BASE_URL}"
      }
    }
  },
  "permission": {
    "edit": "allow",
    "webfetch": "allow",
    "bash": { "*": "allow" }
  },
  "tools": {
    "write": true,
    "edit": true,
    "bash": true
  }
}
```

**Key settings**:
- Model: `anthropic/claude-opus-4-6` (Claude Opus latest)
- Default agent: `build`
- All permissions granted: edit, webfetch, bash
- All tools enabled: write, edit, bash

### 3.2 `research_rubric.json`

- **Version**: 1.0
- **Agent pipeline**: orchestrator -> researcher -> writer -> reviewer
- **Current agent**: researcher (in_progress)
- **Total items**: 25 across 5 phases
- **Phase breakdown**:
  - Phase 1 (Problem Analysis & Literature Review): 5 items
  - Phase 2 (Baseline Implementation & Metrics): 5 items
  - Phase 3 (Core Research & Novel Approaches): 5 items
  - Phase 4 (Experiments & Evaluation): 6 items
  - Phase 5 (Analysis & Documentation): 4 items

### 3.3 `.gitignore`

Ignores:
- `.env`, `.env.*`, `.env.local` - Environment/secret files
- `*.key`, `*.pem` - Private key files
- `.opencode/` - OpenCode configuration directory
- `.archivara/` - Research tooling directory
- `TASK_*.md` - Task attempt logs
- `agent_*.log`, `orchestration.log` - Agent execution logs

---

## 4. Git LFS Rules (`.gitattributes`)

Binary data types tracked via Git Large File Storage:

| Pattern | Data Type | Expected Use |
|---------|-----------|-------------|
| `*.stl` | 3D mesh (STereoLithography) | N/A for this project |
| `*.ply` | 3D point cloud | N/A |
| `*.npz` | NumPy compressed archive | Simulation state snapshots |
| `*.pickle`, `*.pkl` | Python pickle | Serialized objects |
| `*.zip`, `*.gz`, `*.tar`, `*.tar.gz` | Compressed archives | Dataset bundles |
| `*.hdf5`, `*.h5` | HDF5 hierarchical data | Large simulation outputs |
| `*.feather` | Apache Feather columnar | Tabular results |
| `*.npy` | NumPy array file | Array data |
| `*.dat` | Generic binary data | Raw simulation output |
| `*.csv` | Comma-separated values | Tabular results |
| `*.obj` | 3D object file | N/A |
| `*.parquet` | Apache Parquet columnar | Large tabular data |

**Note**: CSV files are tracked via LFS, which means large result tables will not bloat the git history. JSON files are NOT tracked via LFS, making them suitable for small structured results that benefit from diffing.

---

## 5. Project Dependencies (To Be Installed)

### 5.1 Core Python Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| `numpy` | Array operations, vectorized force computation | Latest |
| `matplotlib` | Plotting and figure generation | Latest |
| `seaborn` | Publication-grade plot styling | Latest |
| `pytest` | Test framework | Latest |
| `pytest-cov` | Code coverage reporting | Latest |

### 5.2 Additional Dependencies (Potential)

| Package | Purpose | Phase |
|---------|---------|-------|
| `scipy` | Special functions, optimization, ODE reference solutions | Phase 3+ |
| `numba` | JIT compilation for performance-critical loops | Phase 3 (optional) |

---

## 6. Planned Source Structure

Based on rubric requirements, the following structure will be created:

```
src/
  __init__.py
  bodies.py              # item_006: Body dataclass, System class
  metrics.py             # item_009: Energy, momentum, angular momentum
  initial_conditions.py  # item_015: Benchmark scenario generators
  forces/
    __init__.py
    brute_force.py       # item_007: O(N^2) pairwise gravity
    barnes_hut.py        # item_012: O(N log N) tree code
  integrators/
    __init__.py
    euler.py             # item_008: Symplectic Euler
    leapfrog.py          # item_008: Stormer-Verlet leapfrog
    yoshida.py           # item_013: 4th-order Yoshida
    adaptive.py          # item_014: Adaptive timestep wrapper
sim.py                   # item_010: Main simulation loop
tests/
  __init__.py
  test_bodies.py         # item_006 tests
  test_forces.py         # item_007 tests
  test_barnes_hut.py     # item_012 tests
  test_integrators.py    # item_008 tests
  test_metrics.py        # item_009 tests
benchmarks/
  scaling.py             # item_016: N-scaling benchmark
  integrator_comparison.py # item_017: Method comparison
  theta_sweep.py         # item_018: Barnes-Hut accuracy sweep
  adaptive_test.py       # item_020: Adaptive vs fixed timestep
```

---

## 7. Research Artifact Organization

```
results/
  phase1/
    repo_analysis.md          # item_001 (this document)
    literature_review.md      # item_002
    problem_scope.md          # item_004
    prior_implementations.md  # item_005
  phase2/
    kepler_validation.json    # item_010
  phase4/
    scaling_benchmark.json    # item_016
    integrator_comparison.json # item_017
    theta_sweep.json          # item_018
    figure_eight.json         # item_019
    adaptive_comparison.json  # item_020
    coverage_report.txt       # item_021
  phase5/
    design_rationale.md       # item_022
  concept_evolve/
    concept_cards.json        # ConceptEvolve output
    semantic_bridge.json      # Concept graph
    steering_directions.json  # Research directions
    tree/                     # Materialized concept folders
figures/
  kepler_orbit.png            # item_010
  scaling_comparison.png      # item_016
  energy_drift.png            # item_017
  convergence_order.png       # item_017
  theta_accuracy_speed.png    # item_018
  figure_eight_trajectory.png # item_019
  adaptive_timestep.png       # item_020
  summary/
    combined_performance.png  # item_024
    conservation_analysis.png # item_024
    algorithm_comparison.png  # item_024
```

---

## 8. Workflow and Automation

### 8.1 Agent Pipeline

The research rubric defines a 4-stage agent pipeline:

1. **Orchestrator** (completed) - Generated the rubric and project structure
2. **Researcher** (in_progress) - Executes all 25 rubric items
3. **Writer** (pending) - Post-processing and final documentation
4. **Reviewer** (pending) - Quality assurance and validation

### 8.2 Subagent Delegation Pattern

The rubric notes suggest delegating specific tasks:
- `literature-graph-miner`: Citation graph traversal for item_002
- `concept-tree-explorer`: Concept path synthesis for item_003, item_011, item_022
- `@explore` (Task tool): Quick codebase/literature scanning
- `@general` (Task tool): Deeper synthesis and alternative exploration

### 8.3 ConceptEvolve Integration

ConceptEvolve serves as the project's structured brainstorming engine:
- **Phase 1**: Initial `evolve` to explore the gravity simulation design space
- **Phase 3**: `probe` for force computation bottlenecks; `walk` for exploring paths
- **Phase 5**: Synthesis of explored concept paths into design rationale

### 8.4 Deterministic Seeds

All stochastic operations must use seed=42 for reproducibility, as specified in the task requirements.

---

## 9. Key Observations and Risks

### 9.1 Strengths
- Well-structured rubric with clear acceptance criteria
- Rich tooling ecosystem (ConceptEvolve, Semantic Scholar, subagents)
- LFS configured for binary data preventing repo bloat
- All permissions granted for research agent flexibility

### 9.2 Risks and Mitigations
- **CSV files tracked via LFS**: Small CSV results may have unnecessary LFS overhead; prefer JSON for small outputs
- **No requirements.txt yet**: Need to create for reproducibility
- **Empty source tree**: All code must be written from scratch
- **ConceptEvolve depends on `opencode` binary**: May fail if not available in PATH; fallback to manual concept generation

### 9.3 Technical Constraints
- Python 3.10.17 environment
- No GPU available (CPU-only simulation)
- All figures must be 300+ DPI with publication styling
- Deterministic seed 42 for all random operations

---

## 10. Summary

This repository is a greenfield research project with mature research automation tooling (ConceptEvolve, Semantic Scholar) already in place. The core simulation code (src/, tests/, benchmarks/) needs to be built from scratch following the 25-item rubric across 5 phases. The infrastructure supports structured concept exploration, automated literature search, and multi-agent delegation for parallel research tasks.

**Estimated code deliverables**:
- ~15 Python source files
- ~30+ unit tests
- ~6 benchmark scripts
- ~10 publication-quality figures
- ~15+ bibliography entries
- ~5 research documents

**Next step**: Begin item_002 (literature review) and item_003 (ConceptEvolve) to establish the research foundation before implementation.
