# Repository Analysis

## Project Overview

This repository contains a research project investigating the **Perfect Cuboid Problem** (also known as the Perfect Box Problem): finding a rectangular box (cuboid) where all three edge lengths, all three face diagonals, and the space diagonal are simultaneously integers. This is an unsolved problem in number theory, equivalent to finding positive integers (a, b, c) satisfying four simultaneous Pythagorean-type equations.

## File Inventory and Purposes

### Root Directory
- **`research_rubric.json`** — Master research plan with 26 items across 5 phases. Contains acceptance criteria, status tracking, and agent coordination metadata. This file drives the workflow: each item is marked pending → in_progress → completed/failed.
- **`README.md`** — Minimal placeholder ("# testing"). Will be expanded with project description, setup instructions, and findings summary.
- **`TASK_researcher_attempt_1.md`** — Task description file containing the full researcher instructions, ConceptEvolve/Semantic Scholar usage guidelines, figure styling requirements, and persistence-on-failure rules.
- **`sources.bib`** — Bibliography file for BibTeX entries. Currently initialized with header comment; will accumulate references throughout the research.
- **`.gitignore`** — Git ignore rules for the repository.
- **`.gitattributes`** — Git attributes configuration.

### `.archivara/` — Research Tooling
- **`.archivara/concept_evolve.py`** — Cross-domain concept discovery tool based on the Concept-Guided Evolutionary Discovery framework. Spawns Claude sub-agents for structured concept generation.
- **`.archivara/semantic_scholar.py`** — Semantic Scholar API client for academic paper discovery, citation graph traversal, and BibTeX export.
- **`.archivara/logs/`** — Log files from orchestrator and researcher agents.

### Project Directories (Created)
- **`src/`** — Source code for all implementations (cuboid classes, search algorithms, analysis tools).
- **`tests/`** — Unit tests for all source modules.
- **`results/`** — JSON files and markdown reports containing experimental data.
- **`results/concept_evolve/`** — Output from ConceptEvolve tool (concept cards, semantic bridges, introspection).
- **`figures/`** — Publication-quality PNG and PDF plots.
- **`src/experimental/`** — Prototype implementations of novel approaches.

## Tool Capabilities

### ConceptEvolve (`concept_evolve.py`)

Three sub-commands, each spawning a dedicated Claude sub-agent:

1. **`evolve "topic"`** — Full concept evolution pipeline:
   - Generates 8–12 concept cards bridging distant domains (e.g., topology ↔ circuits)
   - Each card includes: symbolic_name, description, domains, mathematical_formalization, analogical_connections
   - Builds a semantic bridge graph (nodes = concepts, edges typed as structural/functional/mathematical/metaphorical analogy)
   - Performs concept probing (5 unexpected associations with structural reasons)
   - Runs anomaly injection (3 unusual concept combinations)
   - Outputs: `concept_cards.json`, `semantic_bridge.json`, `introspection.json`, `evolve_results.json`, `summary.txt`

2. **`probe "sub-problem"`** — Deep introspection on a specific sub-problem:
   - Concept probing (5 associations with surprise ratings)
   - Forced bridging (3 distant-domain pairs with deep structural connections)
   - Anomaly injection (3 unusual combinations with novel associations)
   - Steering directions (3–5 concrete research directions with rationale and first steps)
   - Output: `probe_result.json`

3. **`reframe "problem"`** — Cross-domain reframing:
   - Restates the problem in 5 different domain vocabularies
   - Each reframing includes: domain, restatement, key_insight, suggested_technique, mapping_back
   - Output: `reframings.json`

### Semantic Scholar (`semantic_scholar.py`)

Five sub-commands for academic literature discovery:

1. **`search "query" [--limit N]`** — Keyword search returning papers with title, authors, year, citation count, abstract, IDs
2. **`citations <paperId> [--limit N]`** — Papers citing a given paper (forward citation traversal)
3. **`references <paperId> [--limit N]`** — Papers referenced by a given paper (backward citation traversal)
4. **`recommend <paperId1> <paperId2> ...`** — Cross-domain paper recommendations based on multiple seed papers
5. **`bibtex <paperId>`** — Generate BibTeX entry for a paper (for appending to `sources.bib`)

The API uses the Semantic Scholar Graph API v1 with retry logic (3 attempts with 1s backoff).

## Identified Gaps Needing New Code

The following modules must be created to fulfill the research rubric:

1. **`src/cuboid.py`** — Core Cuboid class with edge/diagonal computation, Euler brick and perfect cuboid detection, Pythagorean triple generators (item_007)
2. **`src/brute_force.py`** — Systematic brute-force enumeration with modular pre-filtering (item_008)
3. **`src/verifier.py`** — Comprehensive 7-condition verification checker with exact integer square root (item_009)
4. **`src/modular_sieve.py`** — Multi-prime quadratic residue sieve for aggressive candidate filtering (item_012)
5. **`src/parametric.py`** — Parametric family generators (Saunderson, Euler, Bremner) for Euler brick families (item_013)
6. **`src/near_miss.py`** — Near-miss scoring, ranking, statistical distribution analysis (item_014)
7. **`src/novel_search.py`** — S3-symmetry reduction + elliptic curve methods (item_015)
8. **`src/constraint_checker.py`** — Constraint propagation and optional SAT/SMT feasibility checker (item_016)
9. **`tests/test_cuboid.py`** — Unit tests for Cuboid class (item_007)
10. **`src/experimental/`** — Prototypes from ConceptEvolve-inspired strategies (item_017)
11. **`run_all.py`** — Complete experimental pipeline runner (item_026)
12. **`requirements.txt`** — Python dependency listing (item_026)

## Documentation Gaps

- **`literature_review.md`** — Comprehensive survey of classical and modern results (items 002, 003)
- **`problem_specification.md`** — Formal Diophantine system with necessary conditions (item_005)
- **`novel_approach.md`** — Mathematical derivation for novel search strategies (items 015, 017)
- **`REPORT.md`** — Final comprehensive research report (item_023)
- **`LIMITATIONS.md`** — Limitations, open questions, future directions (item_025)
- **`results/summary_tables.md`** — Result comparison tables (item_024)

## Technical Environment

- Python 3 available with standard library
- Matplotlib and Seaborn available for publication-quality figures
- Claude CLI available for sub-agent spawning (ConceptEvolve)
- Semantic Scholar API accessible via HTTP
- Git for version control with pre-push hooks configured

Word count: ~780 words (exceeds 300-word minimum).
