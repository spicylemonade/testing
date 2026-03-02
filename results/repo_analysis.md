# Repository Structure & Tooling Analysis

## Overview

This repository is a research project framework designed for systematic, reproducible computational research on the Collatz conjecture. It integrates AI-powered research tools (ConceptEvolve, Semantic Scholar API) with a structured experimental pipeline managed via a JSON rubric.

## Directory Structure

```
/home/codex/work/repo/
├── research_rubric.json     # Master research plan with 25 items across 5 phases
├── sources.bib              # BibTeX bibliography (populated during research)
├── README.md                # Project readme
├── TASK_researcher_attempt_1.md  # Task specification for the researcher agent
├── .archivara/              # AI research tooling
│   ├── concept_evolve.py    # Cross-domain concept discovery tool
│   ├── semantic_scholar.py  # Academic paper search & citation graph traversal
│   └── logs/                # Logging directory for tool runs
├── results/                 # All experimental data outputs (JSON files)
│   └── concept_evolve/      # ConceptEvolve outputs (concept cards, bridges, probes)
├── figures/                 # All visualizations (PNG, PDF)
└── src/                     # (To be created) Modular research code
```

## Available Tooling

### 1. ConceptEvolve (`.archivara/concept_evolve.py`)

**Purpose**: Spawns dedicated Claude sub-agents to perform cross-domain concept discovery. Based on the Concept-Guided Evolutionary Discovery framework (2026). Generates novel concept connections, semantic bridge graphs, and proxy introspection results.

**Commands**:
- `evolve "topic"` — Full pipeline: concept externalization → semantic bridge graph → introspection → anomaly injection. Outputs to `results/concept_evolve/`:
  - `concept_cards.json` — Array of 8-12 concept cards bridging distant domains, each with symbolic_name, description, domains, mathematical_formalization, analogical_connections
  - `semantic_bridge.json` — Typed directed graph of concept relationships with nodes, edges (typed: structural/functional/mathematical/metaphorical), and bridge_chains
  - `introspection.json` — Self-reflective associations, surprise ratings, blind spot analysis, anomaly injection results
  - `evolve_results.json` — Metadata summary
  - `summary.txt` — Human-readable summary
- `probe "sub-problem"` — Deep introspection with forced bridging, anomaly injection, and concrete steering directions. Output: `probe_result.json`
- `reframe "problem"` — Restates problem in 5 different domain vocabularies. Output: `reframings.json`

**Input**: String describing research topic/problem
**Output**: JSON files in `results/concept_evolve/`
**Timeout**: 600s (evolve), 300s (probe), 180s (reframe)
**Model**: Uses Claude via CLI sub-agent (`claude -p`)

### 2. Semantic Scholar API (`.archivara/semantic_scholar.py`)

**Purpose**: Programmatic access to the Semantic Scholar academic paper database. Enables search, citation graph traversal, recommendation, and BibTeX export.

**Commands**:
- `search "query" --limit N` — Keyword search for papers. Returns paper ID, title, year, citation count, authors, abstract.
- `citations <paperId> --limit N` — Papers that cite a given paper (forward traversal).
- `references <paperId> --limit N` — Papers referenced by a given paper (backward traversal).
- `recommend <paperId1> <paperId2> ...` — Cross-domain paper recommendations based on multiple seed papers.
- `bibtex <paperId>` — Generate BibTeX entry for a paper (append to sources.bib with `>> sources.bib`).

**Input**: Paper IDs (hex strings from search results) or query strings
**Output**: Formatted text to stdout (paper listings or BibTeX entries)
**API**: `https://api.semanticscholar.org/graph/v1` with automatic retry (3 attempts)

### 3. Research Rubric (`research_rubric.json`)

**Purpose**: Master research plan with 25 items across 5 phases. Tracks status (pending/in_progress/completed/failed), notes, and errors for each item. Agent status tracks orchestrator → researcher → writer → reviewer pipeline.

**Format**: JSON with nested phases → items structure. Summary block tracks totals.

## Conventions

- **Results**: All experimental data saved as JSON in `results/` directory, organized by experiment
- **Figures**: All visualizations saved as PNG (300 DPI) and PDF in `figures/` directory. Must use publication-quality matplotlib+seaborn styling.
- **Bibliography**: All sources tracked in `sources.bib` with valid BibTeX entries
- **Reproducibility**: Fixed random seed (42), all parameters recorded, experiments must be re-runnable
- **Code Organization**: Research code in modular files (< 200 lines each), with imports expressing logical dependencies

## Workflow Integration

The tools connect as follows:
1. **Semantic Scholar** discovers relevant papers → populates `sources.bib`
2. **ConceptEvolve** generates cross-domain insights → steers research directions
3. **Research code** (Python modules) implements experiments → saves to `results/` and `figures/`
4. **Rubric** tracks progress and ensures systematic coverage of all research items
5. Citation graph traversal (references/citations/recommend) discovers novel cross-domain connections

The key insight is that ConceptEvolve outputs are **steering mechanisms**, not answers. They guide which experiments to prioritize, what unexpected connections to explore, and which domains might offer transferable techniques for Collatz analysis.
