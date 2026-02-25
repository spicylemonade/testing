# Project Overview: Better Heuristics for TSP on Real Road Networks

## 1. Existing Repository Files

| File | Purpose |
|------|---------|
| `README.md` | Repository description (placeholder) |
| `.gitignore` | Git ignore rules (env files, secrets, logs) |
| `research_rubric.json` | Research plan with phased items and acceptance criteria |
| `sources.bib` | BibTeX bibliography for all consulted literature |
| `TASK_researcher_attempt_1.md` | Task description for researcher agent (gitignored) |
| `.archivara/` | Orchestration logs (gitignored) |

## 2. Directory Structure

```
repo/
├── src/                    # Source code
│   ├── solvers/            # Solver implementations (LKH wrapper, baselines)
│   ├── novel/              # Novel heuristic approaches
│   ├── osrm_matrix.py      # OSRM distance matrix generator
│   └── benchmark_harness.py # Benchmark evaluation harness
├── data/
│   └── benchmarks/         # ATSP benchmark instances (JSON/numpy)
├── results/                # Experimental results (JSON, markdown summaries)
├── figures/                # Generated plots (PNG, PDF)
├── models/                 # Trained model checkpoints
├── sources.bib             # Bibliography
├── literature_review.md    # Literature review document
├── tools_and_data.md       # Survey of tools and datasets
├── project_overview.md     # This file
├── requirements.txt        # Python dependencies
└── research_rubric.json    # Research plan tracking
```

## 3. Core Dependencies

Listed in `requirements.txt`:
- **numpy** — Numerical arrays, distance matrices
- **networkx** — Graph algorithms, TSP utilities
- **requests** — HTTP client for OSRM API queries
- **matplotlib** — Publication-quality plotting
- **seaborn** — Statistical visualization
- **scipy** — Statistical tests, spatial algorithms
- **pandas** — Tabular data handling for results
- **tqdm** — Progress bars for long-running computations
