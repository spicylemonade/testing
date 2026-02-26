# Project Analysis: Minimal Gravity Simulation

## Existing Repository Files

| File | Purpose |
|------|---------|
| `README.md` | Project readme (placeholder) |
| `.gitignore` | Git ignore rules |
| `.gitattributes` | Git attributes |
| `research_rubric.json` | Research task tracking rubric |
| `sources.bib` | Bibliography file for citations |
| `.archivara/semantic_scholar.py` | Semantic Scholar API tool for paper discovery |

## Available Tools

- **Semantic Scholar API** (`.archivara/semantic_scholar.py`): Python script for searching academic papers, fetching citations/references, getting recommendations, and generating BibTeX entries.
  - Commands: `search`, `citations`, `references`, `recommend`, `bibtex`

## Proposed Directory Layout

```
repo/
├── src/                          # Source code
│   ├── __init__.py               # Package init
│   ├── bodies.py                 # Body/Particle data structures, System class
│   ├── forces/                   # Force computation modules
│   │   ├── __init__.py
│   │   ├── brute_force.py        # O(N^2) direct summation
│   │   ├── brute_force_vec.py    # NumPy-vectorized brute force
│   │   └── barnes_hut.py         # Barnes-Hut tree-based approximation
│   ├── integrators/              # Time integration schemes
│   │   ├── __init__.py
│   │   ├── euler.py              # Forward Euler integrator
│   │   ├── leapfrog.py           # Leapfrog / Velocity-Verlet
│   │   ├── yoshida.py            # 4th-order Yoshida symplectic
│   │   └── adaptive.py           # Adaptive timestep controller
│   ├── metrics.py                # Energy, momentum conservation diagnostics
│   ├── initial_conditions.py     # Kepler, figure-eight, Plummer sphere generators
│   └── visualization.py          # Matplotlib-based trajectory plotting
├── tests/                        # Unit and integration tests
│   ├── test_bodies.py
│   ├── test_forces.py
│   ├── test_integrators.py
│   ├── test_metrics.py
│   └── test_initial_conditions.py
├── results/                      # Experimental data (JSON/CSV)
├── figures/                      # Publication-quality plots (PNG/PDF)
├── data/                         # Input data files
├── docs/                         # Additional documentation
├── requirements.txt              # Python dependencies
├── sources.bib                   # BibTeX bibliography
├── literature_review.md          # Literature review document
├── ANALYSIS.md                   # This file
├── RESULTS.md                    # Experimental results summary
└── README.md                     # Project documentation
```

## Design Decisions

1. **2D simulation**: Start with 2D for simplicity; quadtree for Barnes-Hut
2. **NumPy-based**: Core computation uses NumPy arrays for vectorization
3. **Modular architecture**: Each force algorithm and integrator is a separate module
4. **Softening parameter**: Use ε (epsilon) to avoid gravitational singularities
5. **Fixed random seed**: Use seed=42 throughout for reproducibility
6. **SI-like units**: Use gravitational constant G=1 for simplicity (natural units)
