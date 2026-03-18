# Citation Audit

Snapshot date: 2026-03-18 UTC

## Audit Scope

This audit covers the current blocker-driven experiment and novelty artifacts:

- `results/verification/verification_summary.md`
- `results/verification/benchmark_report.md`
- `results/verification/novelty_report.md`
- `results/literature/prior_art_gap.md`
- `results/experiments/h1_tiny_grid_report.md`
- `results/experiments/h1_controls.md`
- `results/experiments/complexity_sweep.md`

## Coverage Strength

### Adequately supported source classes

- Foundational arithmetic-Kakeya framing:
  - Katz-Tao (1999)
  - Green-Ruzsa (2017)
  - Cowen-Breen et al. (2020)
  - Pohoata-Zakharov (2024)
  - Tao (2025)
- Modular / adjacent arithmetic analogues:
  - Hickman-Wright (2018)
- Local-dynamics / abelian-network bridge papers:
  - Bond-Levine (2013, 2014)
- CA / search-method comparison papers:
  - Dennunzio-Formenti-Margara (2023)
  - Faldor-Cully (2024)
  - Novikov et al. (2025)
  - Georgiev et al. (2025)

`sources.bib` contains these references, so the current blocker and novelty framing are not operating without literature support.

### Claims supported mainly by repo evidence rather than bibliography

- No exact verifier exists in the current repo snapshot.
- No exact H1 families were run.
- Budgets remained unspent and distributions remained empty.

These are appropriately supported by local artifacts rather than outside citations.

## Weak Or Missing Citation Areas

### Reframing-only domains

`results/concept_evolve/reframings.json` introduces additional analogical domains, but those domain-specific sources were not added to `sources.bib`. Therefore:

- those reframings may be used as hypothesis-generation context;
- they should not be cited as established prior art in the main report without adding the underlying sources first.

### Neural-CA background

The concept tree mentions neural-CA style ideas, but the current bibliography is stronger on additive CA and automated-search systems than on neural-CA primary sources. Any writeup that compares directly against neural-CA literature should add the relevant citations first.

## Citation-Safe Claim Scope

The following claims are citation-safe with the current bibliography and repo evidence:

- the run targeted the arithmetic-Kakeya witness problem in Katz-Tao's format;
- the watchlist produced mostly false overlaps;
- the strongest real novelty constraints come from arithmetic-Kakeya papers and automated-search / CA-method papers;
- no exact verifier was available in the repo snapshot used here;
- no exact experiment was run;
- the remaining contribution is a verifier-coupled design and audit discipline, not a mathematical advance.

The following claims are **not** citation-safe yet:

- any claim of exact verified witness improvement;
- any claim of beating prior CA or automated-search systems empirically;
- any claim that the reframed domains are already grounded as literature comparisons in this repo.

## Bottom Line

Citation status: `adequate for blocker and design-level claims`, `insufficient for empirical-performance claims or reframing-domain comparisons`.
