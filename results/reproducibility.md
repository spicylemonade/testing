# Reproducibility Guide

## Environment setup

```bash
scripts/setup_research_tools.sh
```

This creates `.venv/` and installs the exact-arithmetic and plotting stack used by the research scripts.

## Literature review

- Core snapshot and curated map: `results/literature/literature_snapshot.json`
- Citation base: `sources.bib`
- Prior-art differentiation log: `results/literature/prior_art_gap.md`
- Re-run the exact targeted helper queries with the saved Semantic Scholar wrapper, for example:

```bash
python3 .archivara/semantic_scholar.py search "\"Beatty Sequences for a Quadratic Irrational: Decidability and Applications\"" --limit 5 --json --save results/literature/ss_quadratic_beatty_decidability.json
python3 .archivara/semantic_scholar.py search "\"Linearly recurrent subshifts have a finite number of non-periodic subshift factors\"" --limit 10 --json --save results/literature/ss_linearly_recurrent_subshifts_full.json
python3 .archivara/semantic_scholar.py search '"Automatic Theorem Proving in Walnut"' --skip-known
python3 .archivara/semantic_scholar.py search '"Pecan: An Automated Theorem Prover for Automatic Sequences using Büchi Automata"' --skip-known
```

## ConceptEvolve workflow

```bash
python3 .archivara/concept_evolve.py evolve "Special Numbers

Characterize the numbers r for which the sequence floor(n*r) contains a homogeneous linearly recurrent subsequence. "
python3 .archivara/concept_evolve.py probe "Are quadratic irrationals the only irrational slopes in the frozen selector families that survive exact and modular-shadow screening, or can higher-degree Pisot beta-endpoint selectors yield genuine homogeneous recurrences?"
python3 .archivara/concept_evolve.py reframe "Special Numbers

Characterize the numbers r for which the sequence floor(n*r) contains a homogeneous linearly recurrent subsequence. "
```

## Baseline and diagnostics

```bash
./.venv/bin/python scripts/run_baseline_smoke.py
./.venv/bin/python scripts/run_modular_shadow_smoke.py
./.venv/bin/python scripts/run_metrics_smoke.py
```

## Concept-specific experiments

```bash
./.venv/bin/python results/concept_evolve/tree/005_convergent_hankel_detector/experiment.py
./.venv/bin/python results/concept_evolve/tree/009_pisot_beta_endpoint_sampler/experiment.py
```

## Full experiment matrix

```bash
./.venv/bin/python scripts/run_full_panel.py
```

This regenerates:
- `results/experiments/full_panel_results.json`
- `results/experiments/full_panel_summary.csv`
- the derived ablation and evaluation memos once the follow-up scripts are rerun.

## Revision follow-up

```bash
./.venv/bin/python scripts/run_claim_sensitive_ablations.py
./.venv/bin/python scripts/generate_figures.py
```

This refreshes the peer-review revision artifacts:
- `results/experiments/claim_sensitive_ablation.json`
- `results/experiments/claim_sensitive_ablation.md`
- `figures/fig4_full_panel_heatmap.pdf`
- `figures/fig4_full_panel_heatmap.png`
- `figures/fig6_claim_sensitive_ablations.pdf`
- `figures/fig6_claim_sensitive_ablations.png`
- `figures/fig7_variant_matrix.pdf`
- `figures/fig7_variant_matrix.png`

## Verification artifacts

- `results/verification/novelty_report.md`
- `results/verification/citation_audit.md`
- `results/verification/benchmark_report.md`
- `results/verification/verification_summary.md`

These are synthesized from delegated audits plus the exact experiment artifacts listed above.
