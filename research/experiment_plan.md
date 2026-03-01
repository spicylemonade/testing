# Comprehensive Experiment Plan for BALT-H Evaluation

## 1. Independent Variables

### 1.1 Graph Type (4 families)
| Family | Generator | Structure | Expected BALT-H advantage |
|--------|-----------|-----------|--------------------------|
| Grid/Mesh | `Graph.grid(rows, cols)` | Planar, regular degree, spatial | Moderate (landmarks effective) |
| Scale-free | `Graph.barabasi_albert(n, m)` | Power-law degree, hubs | High (hub shortcuts) |
| Erdős-Rényi sparse | `Graph.erdos_renyi(n, p)` | Uniform random | Low (little structure) |
| Complete | `Graph.complete(n)` | All-pairs connected | Minimal (overhead dominates) |

### 1.2 Graph Size
| Scale | Grid dims | ER nodes | BA nodes | Complete nodes |
|-------|-----------|----------|----------|---------------|
| XS | 10×10 (100) | 100 | 100 | 50 |
| S | 20×20 (400) | 400 | 400 | 100 |
| M | 50×50 (2500) | 2500 | 2500 | 200 |
| L | 100×100 (10000) | 10000 | 10000 | — |
| XL | 200×200 (40000) | — | — | — |

### 1.3 Graph Density (for ER only)
- Sparse: p = 3/n (just above connectivity threshold)
- Medium: p = 10/n
- Dense: p = 0.1

### 1.4 Query Distribution
- Random pairs (uniform from all node pairs)
- Distant pairs (source and target chosen from opposite sides by BFS distance)
- Local pairs (source and target within BFS radius 5)

## 2. Dependent Variables

| Metric | Measurement | Units |
|--------|-------------|-------|
| Query runtime | `time.perf_counter()` | milliseconds |
| Nodes expanded | Counter in search loop | count |
| Peak memory | `resource.getrusage(RUSAGE_SELF).ru_maxrss` | kilobytes |
| Path optimality | `d_algorithm / d_dijkstra` | ratio (should be 1.0) |
| Preprocessing time | `time.perf_counter()` over BALTHPreprocessing() | milliseconds |

## 3. Algorithms Under Comparison

| ID | Algorithm | Implementation |
|----|-----------|---------------|
| DIJK | Standard Dijkstra (binary heap) | `dijkstra_standard` |
| DIJK-P2P | Dijkstra with early termination | `dijkstra_p2p` |
| DIJK-BI | Bidirectional Dijkstra | `dijkstra_bidirectional` |
| ASTAR-LM | A* with landmark heuristic | `astar_landmark` |
| BALTH | BALT-H (all optimizations) | `balth_query` |
| BALTH-NO | BALT-H (no optimizations) | `balth_query(opt_*=False)` |

## 4. Experimental Design

### 4.1 Number of Trials
- **10 random queries per (algorithm, graph) configuration** for statistical significance
- **3 repetitions** of each timing measurement, taking the median
- Total: 30 timed runs per cell

### 4.2 Seed Control
- Graph generation seed: 42
- Query generation seed: 123
- All results are deterministic and reproducible

### 4.3 Warmup
- 1 untimed warmup query before timing begins (Python JIT/cache effects)

## 5. Statistical Analysis

### 5.1 Central Tendency
- Report median and mean query time per configuration
- Report geometric mean speedup across all configurations

### 5.2 Variability
- Report standard deviation and interquartile range (IQR) for runtime
- Report min/max runtime per configuration

### 5.3 Statistical Tests
- **Wilcoxon signed-rank test**: Compare BALT-H vs each baseline on paired
  query sets (same source-target pairs). Preferred over t-test for non-normal
  distributions typical of runtime measurements.
- **Significance level**: α = 0.05
- **Effect size**: Compute Cohen's d for runtime differences

### 5.4 Multiple Comparison Correction
- Bonferroni correction for comparing BALT-H against 4 baselines (α' = 0.0125)

## 6. Hardware and Environment

### 6.1 Specification
- Platform: Linux 4.4.0 (container environment)
- Python: 3.10.x
- No GPU, single-threaded execution
- All algorithms in pure Python (no C extensions beyond stdlib)

### 6.2 Environment Controls
- Single process, no background tasks during timing
- `gc.disable()` during timed sections to prevent GC pauses
- Same Python process for all algorithms on same graph (shared memory state)
- Process affinity not controlled (container limitation)

## 7. Output Files

| File | Content |
|------|---------|
| `results/synthetic_results.csv` | All synthetic benchmark measurements |
| `results/realworld_results.csv` | Real-world dataset measurements |
| `results/comparison.csv` | Speedup ratios |
| `results/comparison_analysis.md` | Written analysis |
| `results/scalability_results.csv` | Scaling measurements |

## 8. Estimated Total Runs

- Synthetic: 4 graph types × 4-5 sizes × 6 algorithms × 10 queries × 3 reps = ~3600 runs
- Real-world: 2 datasets × 6 algorithms × 100 queries × 3 reps = ~3600 runs
- Scalability: 2 graph types × 6 sizes × 3 algorithms × 10 queries × 3 reps = ~1080 runs
- **Total: ~8280 individual timed runs (exceeds 500 requirement)**
