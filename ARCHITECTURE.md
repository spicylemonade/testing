# Repository Architecture

## Project Overview

This repository implements research on faster shortest path algorithms. The project
follows a structured experimental pipeline: graph generation → algorithm implementation →
benchmarking → analysis → publication-quality figures and report.

## Directory Structure

```
.
├── ARCHITECTURE.md          # This file — repo structure and tooling reference
├── README.md                # Project overview and usage instructions
├── research_rubric.json     # Research progress tracking (25 items across 5 phases)
├── sources.bib              # BibTeX bibliography for all consulted references
├── .gitattributes           # Git LFS tracking rules (see below)
├── .gitignore               # Ignored files (.env, secrets, .claude/, .archivara/)
│
├── src/                     # Source code — algorithms and infrastructure
│   ├── graph.py             # Core graph data structures (adjacency list, I/O, generators)
│   ├── dijkstra.py          # Baseline: Dijkstra variants (binary heap, Fibonacci, bidirectional)
│   ├── astar.py             # Baseline: A* search with pluggable heuristics
│   ├── novel_algorithm.py   # Novel algorithm implementation
│   ├── benchmark.py         # Benchmarking infrastructure (timing, memory, node counts)
│   └── plot_results.py      # Figure generation scripts
│
├── tests/                   # Unit and integration tests (pytest)
│   ├── test_graph.py        # Graph data structure tests
│   ├── test_dijkstra.py     # Dijkstra correctness tests
│   ├── test_astar.py        # A* correctness tests
│   ├── test_novel.py        # Novel algorithm tests
│   └── test_correctness_exhaustive.py  # Exhaustive correctness verification
│
├── research/                # Research documents and analysis
│   ├── bottleneck_analysis.md   # Profiling insights and improvement opportunities
│   ├── algorithm_design.md      # Novel algorithm design with pseudocode
│   ├── correctness_proof.md     # Correctness proof sketch
│   ├── optimizations.md         # Optimization results and measurements
│   └── experiment_plan.md       # Experiment design with statistical methodology
│
├── results/                 # Experimental data (CSV, JSON)
│   ├── baseline_results.csv     # Baseline algorithm benchmarks
│   ├── baseline_profile.md      # Profiling report for baselines
│   ├── synthetic_results.csv    # Synthetic graph benchmarks
│   ├── realworld_results.csv    # Real-world graph benchmarks
│   ├── comparison.csv           # Algorithm comparison table
│   ├── comparison_analysis.md   # Comparison discussion
│   └── scalability_results.csv  # Scaling analysis data
│
├── figures/                 # Publication-quality figures (PNG @ 300 DPI + PDF)
│   ├── runtime_comparison.{png,pdf}
│   ├── scalability.{png,pdf}
│   ├── nodes_expanded.{png,pdf}
│   ├── speedup_heatmap.{png,pdf}
│   └── memory_usage.{png,pdf}
│
├── data/                    # Real-world graph datasets
│   └── README.md            # Dataset sources and download procedures
│
└── .archivara/              # Research tooling (gitignored)
    ├── semantic_scholar.py  # Semantic Scholar API client (see below)
    └── logs/                # Agent execution logs
```

## Available Tools

### Semantic Scholar API Client (`.archivara/semantic_scholar.py`)

A Python CLI for academic paper discovery via the Semantic Scholar API:

| Command | Usage | Description |
|---------|-------|-------------|
| `search` | `python3 .archivara/semantic_scholar.py search "query" --limit N` | Keyword search for papers |
| `citations` | `python3 .archivara/semantic_scholar.py citations <paperId> --limit N` | Papers citing a given paper |
| `references` | `python3 .archivara/semantic_scholar.py references <paperId> --limit N` | References of a given paper |
| `recommend` | `python3 .archivara/semantic_scholar.py recommend <id1> <id2>` | Cross-domain paper recommendations |
| `bibtex` | `python3 .archivara/semantic_scholar.py bibtex <paperId> >> sources.bib` | Generate BibTeX entry |

The tool supports retry logic (3 attempts with 1s delay) and returns JSON on error.
Fields returned: title, authors, year, citationCount, abstract, externalIds, venue.

## Git LFS Configuration (`.gitattributes`)

Large binary files are tracked via Git LFS to keep the repository lightweight:

| Extension | Typical Content |
|-----------|-----------------|
| `*.csv` | Benchmark results, experimental data |
| `*.gz`, `*.tar`, `*.tar.gz`, `*.zip` | Compressed datasets |
| `*.npy`, `*.npz` | NumPy arrays |
| `*.hdf5`, `*.h5` | HDF5 datasets |
| `*.pkl`, `*.pickle` | Pickled Python objects |
| `*.feather`, `*.parquet` | Columnar data formats |
| `*.dat`, `*.obj`, `*.ply`, `*.stl` | Binary/mesh data |

## Data Pipeline

```
Input Graphs                    Algorithms                  Benchmarking
─────────────                   ──────────                  ────────────
1. Random generators     ──►   Dijkstra (3 variants)  ──►  Wall-clock time
   - Erdős-Rényi               A* (2 heuristics)           Nodes expanded
   - Grid/lattice               Novel algorithm             Peak memory
   - Barabási-Albert                                        Path optimality
   - Complete graphs
2. Real-world datasets   ──►   Same algorithms        ──►  Same metrics
   - DIMACS road networks
   - SNAP social networks

                               Results (CSV)           ──►  Figures (PNG/PDF)
                               └── results/                 └── figures/
                                                       ──►  Report (REPORT.md)
```

## Reproducibility

- All random operations use seed 42
- Python dependencies pinned in `requirements.txt`
- Full pipeline executable via `make all` or `run.sh`
- Tests runnable via `pytest tests/`
