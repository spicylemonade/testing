# Perfect Cuboid Computational Search

A computational investigation of the perfect cuboid problem: does there exist a rectangular box with integer edges, integer face diagonals, and an integer space diagonal?

## Problem Statement

Find positive integers a, b, c such that all seven quantities are integers:
- Edges: a, b, c
- Face diagonals: sqrt(a^2+b^2), sqrt(a^2+c^2), sqrt(b^2+c^2)
- Space diagonal: sqrt(a^2+b^2+c^2)

This problem has been open since 1719. Our search found **no perfect cuboid**, consistent with all prior work up to edge bounds of 2.5 x 10^13.

## Setup

```bash
pip install -r requirements.txt
```

## Running the Pipeline

```bash
python run_all.py
```

This executes the complete experimental pipeline:
1. Brute-force exhaustive search (bound=5000)
2. Modular arithmetic sieve with quadratic residue filtering
3. Novel Pythagorean triple intersection search
4. Parametric family generation (Saunderson, Euler, Bremner)
5. Verification of all Euler bricks found
6. Near-miss statistical analysis with histogram generation

## Running Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
src/
  cuboid.py            Core data structures (Cuboid class, integer sqrt, Pythagorean triples)
  brute_force.py       Exhaustive search with S3 symmetry reduction
  modular_sieve.py     QR sieve + Pythagorean pair enumeration + NumPy vectorization
  novel_search.py      Pythagorean graph triangle intersection (O(n^1.3) scaling)
  parametric.py        Saunderson, Euler, and Bremner parametric families
  near_miss.py         Near-miss scoring and chi-squared statistical analysis
  verifier.py          7-condition verification of cuboid candidates
  constraint_checker.py  Multi-prime constraint propagation
  experimental/        Distance geometry prototype

tests/
  test_cuboid.py       13 unit tests for core functionality

results/               Experimental data (JSON) and analysis reports (Markdown)
figures/               Scaling plots, ablation studies, near-miss histograms
```

## Key Results

- **69 Euler bricks** found with edges up to 5,000 (exhaustive)
- **517 Euler bricks** from parametric families (edges up to ~10^10)
- **No perfect cuboid** found
- Modular sieve achieves **4.4x speedup** over brute force
- Novel triple intersection achieves **1000x speedup** (partial coverage)
- Near-miss gap distribution is **consistent with random** (chi-squared test)

## Documentation

- `REPORT.md` -- Full research report (2900+ words)
- `LIMITATIONS.md` -- Computational limits, open questions, future directions
- `literature_review.md` -- 23 references spanning 1719-2026
- `sources.bib` -- 26 BibTeX entries
- `results/summary_tables.md` -- Comprehensive comparison tables
