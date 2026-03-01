# BALT-H: Bidirectional ALT with Hub Acceleration

A novel point-to-point shortest path algorithm combining bidirectional Dijkstra search, landmark-based lower bounds (ALT heuristic), and hub-based early termination. Achieves **4.08x geometric mean speedup** over standard Dijkstra across diverse graph types.

## Project Structure

```
src/
  graph.py              # Graph data structure with generators
  dijkstra.py           # Dijkstra variants (standard, bidirectional, P2P)
  astar.py              # A* with Euclidean and landmark heuristics
  novel_algorithm.py    # BALT-H implementation
  benchmark.py          # Benchmarking infrastructure
  plot_results.py       # Figure generation
  run_synthetic_benchmarks.py
  run_realworld_benchmarks.py
  run_scalability.py
  generate_comparison.py
  measure_optimizations.py

tests/
  test_graph.py                  # 15 tests
  test_dijkstra.py               # 14 tests
  test_astar.py                  # 8 tests
  test_novel.py                  # 14 tests
  test_correctness_exhaustive.py # 13 tests (1000 random graphs)

research/
  algorithm_design.md     # BALT-H design with pseudocode
  bottleneck_analysis.md  # Baseline profiling analysis
  correctness_proof.md    # Formal correctness proof sketch
  experiment_plan.md      # Experiment methodology
  optimizations.md        # Optimization measurements

results/                  # CSV benchmark data
figures/                  # PNG and PDF figures
REPORT.md                 # Full research report (2400+ words)
LIMITATIONS.md            # Limitations and future work
sources.bib               # 22 BibTeX references
```

## Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.8+.

## Quick Start

```python
from src.graph import Graph
from src.novel_algorithm import BALTHPreprocessing, balth_query

# Create a graph
g = Graph.barabasi_albert(1000, m=3, seed=42)

# Preprocess (one-time cost)
prep = BALTHPreprocessing(g, k_landmarks=8, k_hubs=8)

# Query (fast, reusable)
distance, nodes_expanded = balth_query(g, source=0, target=999, prep=prep)
print(f"Distance: {distance}, Nodes expanded: {nodes_expanded}")
```

## Running Tests

```bash
python -m pytest tests/ -v
```

All 64 tests should pass.

## Reproducing All Results

Run the full pipeline (install, test, benchmark, plot):

```bash
make all
```

Or run individual steps:

```bash
make install       # Install dependencies
make test          # Run all tests
make benchmarks    # Run all benchmarks (~10 min)
make figures       # Generate figures from results
```

## Key Results

| Metric | Value |
|--------|-------|
| Geometric mean speedup vs Dijkstra | 4.08x |
| Best speedup (BA scale-free) | 6-8x |
| Nodes expanded reduction | 60-90% |
| Empirical complexity (BA graphs) | O(n^0.60) |
| Preprocessing time (10K nodes) | ~500ms |

See [REPORT.md](REPORT.md) for the full research report with figures and analysis.

## References

See [sources.bib](sources.bib) for 22 cited papers spanning classical algorithms (Dijkstra, Bellman-Ford, A*) and modern techniques (Contraction Hierarchies, Hub Labeling, ALT, CRP).
