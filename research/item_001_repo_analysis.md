# Repository Structure Analysis

## Overview

This repository serves as the research laboratory for investigating Single-Source Shortest Path (SSSP) algorithms with the goal of achieving asymptotically fewer operations than the current best known bound of O(m + n log n) on general weighted directed graphs.

## Current Repository State

The repository is in a **fresh initialization state**. The orchestrator agent has created the research rubric, but no source code, tests, or experimental infrastructure exists yet. All modules listed below are **planned** and will be created during this research project.

## Planned Module Structure

### Core Source Modules (src/)

| Module | Purpose | Dependencies |
|--------|---------|-------------|
| `src/graph.py` | Graph data structure (adjacency list representation for weighted directed graphs) and graph generator functions for benchmarking | None |
| `src/fibonacci_heap.py` | True Fibonacci heap implementation with O(1) amortized decrease-key and O(log n) amortized extract-min | None |
| `src/dijkstra.py` | Dijkstra's algorithm using Fibonacci heap, with operation counting instrumentation | `graph.py`, `fibonacci_heap.py`, `op_counter.py` |
| `src/op_counter.py` | Operation-counting framework tracking comparisons, additions, and heap operations in the comparison-addition model | None |
| `src/graph_generators.py` | Six graph generator families: adversarial, sparse Erdos-Renyi, dense, layered DAG, grid/lattice, planted shortest-path tree | `graph.py` |
| `src/novel_algorithm.py` | The novel SSSP algorithm achieving sub-O(m + n log n) operations | `graph.py`, `op_counter.py` |
| `src/batch_dijkstra.py` | Simplified sorting-barrier-breaking reference implementation (Duan et al. style) | `graph.py`, `op_counter.py` |
| `src/benchmark.py` | Benchmark harness for running all algorithms across all graph families with CSV output | All algorithm modules, `graph_generators.py` |

### Test Modules (tests/)

| Module | Purpose |
|--------|---------|
| `tests/test_dijkstra.py` | Correctness tests for Dijkstra with Fibonacci heap |
| `tests/test_novel.py` | Comprehensive correctness tests for the novel algorithm (20+ test cases) |
| `tests/test_graph.py` | Tests for graph data structure and generators |

### Research Documents (research/)

| Document | Purpose |
|----------|---------|
| `research/item_001_repo_analysis.md` | This document |
| `research/literature_review.md` | Comprehensive SSSP literature review |
| `research/duan_et_al_study.md` | Deep technical study of Duan et al. STOC 2025 |
| `research/techniques.md` | Analysis of key algorithmic techniques |
| `research/open_problems.md` | Open problems and research directions |
| `research/algorithm.md` | Formal algorithm description with pseudocode |
| `research/proofs.md` | Correctness and complexity proofs |

### Output Directories

| Directory | Purpose |
|-----------|---------|
| `results/` | CSV and JSON experimental data |
| `figures/` | Publication-quality PNG (300 DPI) and PDF figures |

## Existing Infrastructure

### Archivara Tools (.archivara/)

1. **semantic_scholar.py**: Command-line interface to Semantic Scholar API for paper discovery, citation traversal, and BibTeX generation
2. **concept_evolve.py**: Cross-domain concept discovery tool that spawns Claude Code sub-agents for research ideation (evolve, probe, reframe commands)

### Configuration Files

- **.gitignore**: Excludes secrets, IDE directories, archivara files, and task logs
- **.gitattributes**: Git LFS tracking for large data files (.csv, .npy, .h5, .parquet, etc.)
- **research_rubric.json**: 28-item rubric across 5 phases tracking all research deliverables

## Relationship to Prior BALT-H Work

The research rubric references an existing "BALT-H result (practical 4.08x speedup)" from a prior research project on this branch. Key distinctions from the current research goal:

| Dimension | BALT-H (Prior Work) | Current Goal |
|-----------|---------------------|--------------|
| **Metric** | Practical wall-clock speedup | Worst-case asymptotic operation count |
| **Baseline** | Dijkstra with binary heap | O(m + n log n) Fibonacci heap Dijkstra |
| **Improvement type** | Constant-factor speedup (4.08x) | Asymptotic improvement (o(m + n log n)) |
| **Model** | Practical RAM model | Comparison-addition model |
| **Graph types** | Specific benchmark families | All directed graphs with non-negative weights |
| **Theoretical significance** | Engineering contribution | Complexity-theoretic breakthrough |

The prior BALT-H work demonstrated that heuristic techniques (bidirectional search, ALT preprocessing with landmarks, hub-based shortcuts) can dramatically improve practical SSSP performance. However, these techniques do not improve worst-case asymptotic complexity — they exploit structure in specific graph families.

The current research aims for a fundamentally different kind of improvement: reducing the asymptotic operation count in the comparison-addition model, which requires new algorithmic ideas rather than engineering optimizations. The state-of-the-art in this direction is the Duan-Mao-Mao-Shu-Yin STOC 2025 result achieving O(m log^{2/3} n), which broke the long-standing "sorting barrier" showing that Dijkstra's O(m + n log n) is not optimal even for non-negative weights.

## Module Interconnections (Planned)

```
graph.py ──────┐
               ├──> dijkstra.py ──────┐
fibonacci_heap.py ─┘                  │
                                      ├──> benchmark.py ──> results/
graph_generators.py ──────────────────┤
                                      │
op_counter.py ────────────────────────┤
               ┌──> novel_algorithm.py┤
               │                      │
               └──> batch_dijkstra.py─┘
```

## Next Steps

1. Conduct comprehensive literature review (Items 002-005)
2. Build bibliography (Item 006)
3. Implement baseline infrastructure (Items 007-010)
4. Design and implement the novel algorithm (Items 012-018)
5. Run experiments and produce publication-quality results (Items 019-028)
