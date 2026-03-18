# Repo Map

Snapshot date: 2026-03-18 UTC

## Top-Level Layout

- `.archivara/concept_evolve.py`
  - Child-agent orchestration helper for `evolve`, `probe`, `reframe`, `iterate`, and `walk`.
  - Writes under `results/concept_evolve/`.
  - Not a mathematical verifier. It manages prompts, caches, state files, and tree materialization.
  - Intake note: the `evolve()` call path in this snapshot was locally broken because it called `_run_sub_agent()` without the required keyword arguments. That was patched in-session before the mandatory `evolve` run.
- `.archivara/semantic_scholar.py`
  - Literature helper for `search`, `citations`, `references`, `recommend`, `graph`, and `bibtex`.
  - Maintains `results/literature/semantic_scholar_manifest.json` as the canonical memory of prior queries.
- `results/literature/`
  - Stores the malformed initial watchlist, novelty guard, literature snapshot, graph cache, and gap notes.
  - This is the main persistent literature layer.
- `results/swarm/`
  - Stores hypothesis selection, director brief, falsifier memo, tool routing, and negative-space notes.
  - These files are planning and policy artifacts, not executable tooling.
- `results/verification/`
  - Intended home for verifier, benchmark, novelty, and citation audit outputs.
  - At intake, there was no exact witness-verifier implementation or report in this directory.
- `figures/`
  - Empty publication-figure staging area at intake.
- `results/concept_evolve/tree/`
  - Missing at intake.
  - After the mandatory `concept_evolve.py evolve` launch, only `results/concept_evolve/.state/` and `.debug/` existed so far; no concept cards or tree folders had materialized yet.

## Executable Entry Points

- Present helper scripts:
  - `.archivara/concept_evolve.py`
  - `.archivara/semantic_scholar.py`
- Absent helper scripts:
  - No exact decoder or verifier for six-line `(X,G,R,T)` witnesses over `\mathbb{Z}`.
  - No search runner for CA experiments.
  - No tests, notebooks, package modules, or CLI commands beyond the two helpers above.

## Shell Discovery Evidence

Commands used to audit the snapshot:

- `rg --files`
- `find . -maxdepth 3 -type d | sort`
- `rg -n "verify|verifier|forcing pair|constructible graph|AK\\(|arithmetic Kakeya|Kakeya|witness" .`
- `sed -n '1,260p' .archivara/concept_evolve.py`
- `sed -n '1,260p' .archivara/semantic_scholar.py`

These checks found only planning artifacts plus the two helper scripts. They did not reveal any exact evaluator or witness-decoding code.

## Dependency Graph

```text
semantic_scholar.py / web / local notes
    -> results/literature/*
    -> results/swarm/{hypotheses,director_brief,falsifier,tool_plan}.md|json
    -> research decisions for H1/H2/H3
    -> expected exact verifier / experiment runner
    -> results/verification/*
    -> results/final_assessment.md and writeup handoff

concept_evolve.py
    -> results/concept_evolve/*
    -> concept cards / bridge structure / steering directions
    -> feeds baseline and core-design branch selection
```

## Immediate Takeaway

This repo is a research-planning workspace, not an implementation repo. The critical missing component is an exact verifier or decoder for legal arithmetic-Kakeya witnesses; every later experiment phase depends on resolving or formally logging that blocker.
