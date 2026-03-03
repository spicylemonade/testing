# The Univalent Bloch Constant: A Multi-Method Investigation

## Overview

This repository contains a comprehensive computational and theoretical investigation of the **univalent Bloch constant** $B_u$, defined as

$$B_u = \inf\{B_f : f \in \mathcal{S}\}$$

where $\mathcal{S}$ is the class of schlicht (univalent) functions $f : \mathbb{D} \to \mathbb{C}$ with $f(0)=0$, $f'(0)=1$, and $B_f$ is the inradius of the image domain $f(\mathbb{D})$. The best known bounds are

$$0.5708858 < B_u \leq 0.6564$$

established by Skinner (2009, lower) and Carroll--Ortega-Cerd&agrave; (2009, upper).

## Main Results

We applied five complementary approaches to study $B_u$ and obtained:

| Bound | Value | Method | Rigorous? |
|-------|-------|--------|-----------|
| Best lower (literature) | 0.5708858 | Skinner bootstrap | Yes |
| Best upper (literature) | 0.6564 | Carroll--Ortega-Cerd&agrave; slit disk | Yes |
| Our best independent upper | 0.6808 | Degree-7 polynomial coefficient optimization | Yes |
| Our second upper | 0.6833 | Close-to-convex function optimization | Yes |

**Novel theoretical contributions:**
- An extremal length inequality $B_f \geq r \cdot \exp(\pi M(r))/4$ connecting the inradius to the conformal modulus of separating curve families
- Identification of the conformal radius normalization $R(0,\Omega) = 1$ as the binding constraint in optimization formulations (not the area theorem)
- A comprehensive catalog of 11 distinct proof techniques with applicability assessments for $B_u$

**Key finding:** Despite extensive numerical search (1504 optimization evaluations, 1294 slit mapping configurations), we did not improve the Skinner lower bound, confirming that genuinely new theoretical ingredients are needed beyond pointwise distortion estimates. The gap $0.6564 - 0.5709 \approx 0.086$ (15% relative width) remains open.

## Repository Structure

```
research_rubric.json          Master rubric tracking all 28 research items
sources.bib                   34 BibTeX references
requirements.txt              Python dependencies (pinned versions)

results/
  phase1/                     Literature review, citation graph, technique catalog
    literature_review.json    24 papers surveyed
    citation_graph.json       29 nodes, 66 edges, 6 bridge papers
    technique_catalog.md      11 proof methods cataloged
    skinner_analysis.md       Detailed Skinner 2009 analysis (4 bottlenecks)

  phase2/                     Baseline implementations and benchmarks
    compute_Bf.py             Core B_f computation module (6 function families)
    benchmark.py              Benchmark suite (5+ families, seed 42)
    upper_bounds.py           Upper bound search (6 candidate families)
    reproduce_skinner.py      Skinner reproduction attempt

  phase3/                     Core research and novel approaches
    hyperbolic_approach.md    Schwarz-Pick / Poincar&eacute; metric analysis
    variational_method.md     Jenkins-type variational characterization
    coefficient_optimization.py  de Branges coefficient optimization (best: 0.6808)
    extremal_length.md        New extremal length inequality

  phase4/                     Large-scale experiments
    optimization_campaign.py  1504-evaluation optimization campaign
    slit_mapping_search.py    1294-configuration slit mapping search
    generate_figures.py       Publication-quality figure generation
    bounds_comparison.json    Comprehensive bounds comparison table

  phase5/                     Analysis and documentation
    main_report.md            Full research report (3319 words)
    final_bounds.json         Final verified bounds table
    verification.py           Independent verification (7/7 pass)
    future_directions.json    6 open problems, 2 conjectures

  concept_evolve/             ConceptEvolve exploration tree
    tree/                     14 concept nodes, 27 edges

figures/                      Publication-quality figures (PNG + PDF)
  bounds_timeline.{png,pdf}
  extremal_function.{png,pdf}
  optimization_landscape.{png,pdf}
  method_comparison.{png,pdf}
```

## Reproducing Results

### Prerequisites

- Python 3.10+
- Install dependencies: `pip install -r requirements.txt`

### Run All Computations

```bash
bash results/phase5/reproduce.sh
```

This script re-runs all Phase 2--4 computations, regenerates figures, and runs independent verification. Expected runtime: 10--15 minutes. All scripts use deterministic seeds (42) for reproducibility.

### Run Individual Components

```bash
# Phase 2: Core computations
python3 results/phase2/compute_Bf.py
python3 results/phase2/benchmark.py
python3 results/phase2/upper_bounds.py

# Phase 3: Coefficient optimization
python3 results/phase3/coefficient_optimization.py

# Phase 4: Large-scale search
python3 results/phase4/optimization_campaign.py
python3 results/phase4/slit_mapping_search.py

# Figures
python3 results/phase4/generate_figures.py

# Verification
python3 results/phase5/verification.py
```

## Main Report

The full research report is at [`results/phase5/main_report.md`](results/phase5/main_report.md). It includes:
- Problem formulation and historical context (citing 10+ papers)
- Detailed description of all five approaches attempted
- Precise statements of bounds with rigorous arguments
- Comparison with Skinner (2009) and Yanagihara (1995)
- Discussion of limitations and open questions

## References

All 34 references are collected in [`sources.bib`](sources.bib). Key references:

- Skinner, D.G. (2009). Improved bounds for the univalent Bloch constant. *PhD thesis*.
- Carroll, T. & Ortega-Cerd&agrave;, J. (2009). The univalent Bloch constant. *J. reine angew. Math.*.
- Bhowmik, B. & Sen, S. (2023). On bounds of certain Bloch constants.
- Yanagihara, N. (1995). Sharp distortion estimates for locally univalent Bloch functions.
- Bonk, M. (1990). On Bloch's constant. *Proc. Amer. Math. Soc.*
