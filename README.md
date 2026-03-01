# HopGuidedSSSP: Breaking the Sorting Barrier for Shortest Paths

A novel Single-Source Shortest Paths algorithm achieving **O(m (log log n)^2 + n log n log log n)** time in the comparison-addition model, improving upon the O(m sqrt(log n)) state-of-the-art for sufficiently dense graphs.

## Key Result

**HopGuidedSSSP** replaces the distance-rank-based frontier partition in the Duan et al. (DMMSY 2025) framework with a *hop-guided partition* computable in O(m) time using zero weight comparisons. Combined with geometric BFS-layer grouping and recursive frontier reduction, this achieves:

- **O(m (log log n)^2)** comparisons for m = Omega(n log n / log log n)
- Provably correct on all directed graphs with non-negative real weights
- Empirically validated on 11 graph families (8 standard + 3 adversarial)

## Repository Structure

```
src/
  baselines/          # Dijkstra + Fibonacci heap, DMMSY implementations
  novel/              # HopGuidedSSSP: core.py (partition), sssp.py (full algorithm)
  benchmarks/         # Graph generators, runner, plotting scripts
results/
  paper.md            # Full research paper draft
  correctness_proof.md
  complexity_analysis.md
  novel_algorithm_design.md
  empirical_validation.md
  negative_weight_extension.md
  open_problems.md
  baselines.csv       # Baseline benchmark data
  novel_results.csv   # Novel algorithm benchmark data
  stress_test.csv     # Adversarial benchmark data
figures/              # Publication-quality plots (10 figures)
sources.bib           # 30 BibTeX entries
survey.md             # Technical survey of SSSP frontier
research_rubric.json  # 25-item research rubric (all completed)
```

## Setup

```bash
pip install -r requirements.txt
```

Dependencies: Python 3.8+, numpy, matplotlib, seaborn.

## Reproduce All Results

```bash
python run_all.py
```

This runs all correctness tests, benchmarks, and generates all figures (~10 minutes).

## Quick Correctness Check

```bash
python3 src/novel/test_novel.py
```

## Algorithms Implemented

| Algorithm | File | Time Complexity |
|-----------|------|----------------|
| Dijkstra + Fibonacci Heap | `src/baselines/dijkstra_fib.py` | O(m + n log n) |
| DMMSY (2025) | `src/baselines/dmmsy.py` | O(m log^{2/3} n) |
| **HopGuidedSSSP** | `src/novel/sssp.py` | **O(m (log log n)^2)** |

## Graph Families

8 standard families: Erdos-Renyi, sparse random, dense random, grid/lattice, planar, high-diameter, expander-like, adversarial (decrease-key chains).

3 adversarial families: flat-hop (single-block), deep-chain (max recursion), layered-bipartite (max inter-block edges).

## Citation

See `sources.bib` for all references. The full paper draft is at `results/paper.md`.
