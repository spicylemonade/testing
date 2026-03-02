# Perfect Cuboid Computational Investigation

A multi-method computational investigation of the **perfect cuboid problem**: does there exist a rectangular box with all edges, face diagonals, and space diagonal being positive integers?

## Problem

Given edge lengths a, b, c, find positive integers satisfying:

- a² + b² = d² (face diagonal)
- b² + c² = e² (face diagonal)
- a² + c² = f² (face diagonal)
- a² + b² + c² = g² (space diagonal)

This is an open problem in number theory dating to 1719. No perfect cuboid has been found, and no proof of non-existence has been accepted.

## Results Summary

- **1,714 Euler bricks** found with edges up to 10⁵
- **0 perfect cuboids** found (consistent with all prior searches up to 10¹³)
- **>10⁶x speedup** over brute-force via combined triple decomposition + sieving
- **99.8% candidate rejection** rate from modular arithmetic filters
- Near-miss analysis suggests weak trend of improving scores at larger magnitudes

## Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.8+.

## Quick Start

Run the full pipeline:

```bash
./run.sh
```

Or run individual components:

```bash
# Baseline brute-force search (edges up to 1000)
python3 src/baseline_search.py

# Triple decomposition search (edges up to 10000)
python3 src/triple_decomposition.py

# Combined search with all methods (edges up to 100000)
python3 src/combined_search.py

# Near-miss statistical analysis
python3 src/near_miss_analysis.py

# Generate publication-quality figures
python3 src/generate_figures.py
```

## Source Code

| File | Description |
|------|-------------|
| `src/euler_brick.py` | Saunderson and Euler parametric family generators |
| `src/modular_filter.py` | Multi-stage modular arithmetic sieve (parity, mod-24/48, QR) |
| `src/space_diagonal.py` | Perfect cuboid test, near-miss scoring, NearMissTracker |
| `src/baseline_search.py` | Brute-force search with modular pre-filtering |
| `src/triple_decomposition.py` | Pythagorean triple pair matching for Euler brick discovery |
| `src/elliptic_families.py` | Extended parametric families via Brahmagupta-Fibonacci identity |
| `src/constraint_solver.py` | CSP approach with precomputed modular residue classes |
| `src/quadratic_sieve.py` | 50-prime quadratic residue sieve |
| `src/combined_search.py` | Integrated search combining all methods |
| `src/near_miss_analysis.py` | Statistical analysis of near-miss distributions |
| `src/generate_figures.py` | Publication-quality figure generation |
| `src/metrics.py` | Search metrics tracking and JSON export |
| `src/config.py` | Search configuration management |

## Output

### Results (`results/`)

- `research_report.md` — Full research report (3000+ words)
- `literature_review.md` — Comprehensive literature review (22 papers)
- `benchmark_comparison.md` — Head-to-head method comparison
- `near_miss_statistics.md` — Statistical analysis of near-misses
- `nonexistence_analysis.md` — Review of proof attempts
- `search_summary.md` — Combined search results with top 50 near-misses
- `near_misses.csv` — Near-miss data for analysis
- `metrics.json` — Machine-readable search metrics

### Figures (`figures/`)

- `near_miss_trend.png` — Near-miss score vs. edge magnitude with regression
- `filter_funnel.png` — Candidate rejection funnel (log scale)
- `search_coverage.png` — Searched (a,b) space and edge magnitude distribution
- `benchmark_comparison.png` — Search method throughput comparison

### Bibliography

`sources.bib` contains 23 BibTeX entries covering the relevant literature from Euler (1770) through Stoll-Testa (2025) and Yelle (2026).

## References

See `sources.bib` for the complete bibliography. Key references:

- Stoll & Testa (2010). "The surface parametrizing cuboids." arXiv:1009.0388
- Rathbun (2017). "The Integer Cuboid Table." arXiv:1705.05929
- Matson (2014). "Results of computer search for a perfect cuboid."
- Guy (2004). *Unsolved Problems in Number Theory*, Problem D18.
