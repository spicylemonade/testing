# Citation Audit

Snapshot date: 2026-03-18 UTC

## Scope

- `research_paper.tex` is not present in this snapshot, so this audit is artifact-level rather than manuscript-level.
- Required inputs checked: `sources.bib`, `results/research_context.md`, and `results/literature/semantic_scholar_manifest.json`.
- Because the manuscript file is absent, I also checked the claim-bearing files that would most likely feed any writeup:
  - `results/verification/verification_summary.md`
  - `results/verification/novelty_report.md`
  - `results/final_assessment.md`
  - `results/literature/prior_art_gap.md`
  - `results/core/h1_design.md`
  - `results/core/lane_gates.md`
  - `results/swarm/falsifier.md`
  - the repeated introduction/problem statement embedded in `results/concept_evolve/tree/*/README.md`

Important scoping note:

- `sources.bib:1-2` explicitly says the bibliography was frozen to support `design-level and blocker-level claims only`.
- That scope is narrower than the manuscript-style mathematical introduction copied into the concept-tree READMEs and JSON artifacts.

## Verdict

- `Pass` for blocker-level and repo-internal negative claims.
- `Fail / incomplete` for the mathematical introduction and for several literature-comparison claims if they are promoted into a paper without more sources.

## Claims With Adequate Support

These claims are supported primarily by repo evidence, not by external citations, and that is acceptable:

- No exact integer verifier or decoder was found in the repo snapshot:
  - `results/verification/verification_summary.md:5-33`
  - `results/repo_map.md:30-50`
- No exact H1 sweep, controls, or complexity sweep were run:
  - `results/experiments/h1_tiny_grid_report.md:7-46`
  - `results/experiments/h1_controls.md:7-49`
  - `results/experiments/complexity_sweep.md:7-40`
- No empirical baseline or superiority claim survives:
  - `results/verification/benchmark_report.md:24-69`
  - `results/final_assessment.md:7-28`
- The surviving contribution is design-level only:
  - `results/verification/novelty_report.md:7-15`
  - `results/core/h1_design.md:5`

## Findings

### 1. Missing citations for the manuscript-style mathematical introduction

The strongest citation gap is not in the blocker reports. It is in the repeated introduction text used throughout the concept artifacts, for example:

- `results/concept_evolve/tree/002_spatially-coupled-peeling-ladders/README.md:5-23`

That text makes several source-dependent claims:

- Katz-Tao implicitly formulated the arithmetic Kakeya conjecture.
- `AK(alpha)` implies a Hausdorff-dimension lower bound for Kakeya sets.
- Bourgain established the method-of-slices / Minkowski-dimension part.
- The Hausdorff-dimension upgrade follows from work of Leng, Sah, and Sawhney.

Current support status:

- `sources.bib` contains Katz-Tao (`katz1999`), but it does **not** contain Bourgain or any Leng-Sah-Sawhney entry.
- Therefore the introduction as written is not citation-complete.
- The same uncited background text is duplicated in `results/research_context.json`, `results/concept_evolve/recurrent_state.json`, and multiple `results/concept_evolve/tree/*/README.md` files, so the gap is replicated rather than isolated.

### 2. Reframing-domain claims remain uncited

`results/verification/novelty_report.md:81-89` says the run now has `11` reframing domains, and `results/concept_evolve/reframings.json:3-91` spells them out:

- proof-labeling schemes
- Petri nets / vector addition systems
- network coding
- group testing
- chemical reaction networks
- structural observability
- factor graphs
- Datalog / chase
- abstract interpretation
- applied sheaf theory
- synchronizing automata

Current support status:

- `sources.bib:1-2` already admits these are uncited hypothesis generators.
- No primary sources for any of these domains were added to the bibliography.
- These comparisons are therefore not safe to present as literature-grounded prior-art clearance.

### 3. Several comparison claims are only weakly supported

The comparison set is directionally reasonable, but many statements are still title-level or abstract-level summaries rather than tightly sourced claims. This shows up in:

- `results/literature/prior_art_gap.md:72-133`
- `results/literature/prior_art_gap.md:147-238`
- `results/core/h1_design.md:122-127`
- `results/core/lane_gates.md:44-50`
- `results/swarm/falsifier.md:74-89`

High-risk examples:

- `results/literature/prior_art_gap.md:74-75`
  - "`Generalized Arithmetic Kakeya` ... shows that formulation changes can create apparent progress."
  - This is a reasonable inference, but it is stronger than a bare bibliographic citation unless tied to a precise result or section.
- `results/literature/prior_art_gap.md:81-84`
  - Tao is described as the main current warning against bounded-slope or low-rational-complexity stories.
  - The paper is highly relevant, but the phrasing is interpretive and should be either softened or backed by a precise citation.
- `results/literature/prior_art_gap.md:95-105`
  - Bond-Levine is used as a rigorous local-processing / halting bridge.
  - That is an adjacent-method analogy, not direct evidence for this witness-search lane.
- `results/literature/prior_art_gap.md:123-133`
  - AlphaEvolve and `Mathematical exploration and discovery at scale` are used as novelty-floor system references.
  - The overlap argument is plausible, but still qualitative.

These are not necessarily wrong. They are just not yet traceable enough for manuscript-grade claims.

### 4. Bibliography hygiene is weak even where the papers are real

I did not find an obviously fabricated paper in `sources.bib`, but I did find several entries that are weak, inconsistent, or likely to produce misleading references:

- `sources.bib:12-19` (`green2017`)
  - Uses year `2017` while also citing the final `Periodica Mathematica Hungarica` journal version, which should be treated as the 2019 publication.
- `sources.bib:51-67` (`bond2013`, `bond2014`)
  - Uses preprint years `2013` and `2014` together with journal DOIs for later journal publications; the journal versions are 2016-era publications, not 2013/2014 journal records.
- `sources.bib:78-85` (`faldor2024`)
  - Mixes ALIFE proceedings venue metadata with an arXiv DOI instead of the proceedings DOI.
- `sources.bib:21-40` (`cowenbreen2020`, `pohoata2024`, `tao2025`)
  - Provides only Semantic Scholar URLs; no canonical arXiv IDs or DOIs are recorded.
- `sources.bib:87-102` (`novikov2025`, `georgiev2025`)
  - Author names are encoding-damaged.

So the likely hallucination risk here is not "invented papers." It is "real papers with inconsistent or low-fidelity metadata."

### 5. There is no manuscript-ready citation wiring yet

The current writeup artifacts usually mention papers by name in prose. They do not expose a stable citation map from specific claims to specific keys.

That is acceptable for planning notes, but not for a final paper. The absence of `research_paper.tex` means there is no place yet where the repo demonstrates:

- which exact claims get which exact citation keys;
- whether one citation is carrying too much argumentative weight;
- and whether the mathematical background claims are actually cited where they appear.

## Highest-Priority Sources To Add Or Fix

### Add for the introduction / mathematical background

1. Bourgain, `On the dimension of Kakeya sets and related maximal inequalities` (GAFA, 1999).
   - Needed for the method-of-slices / Minkowski-dimension history currently asserted in the introduction.
2. Leng, Sah, Sawhney, `Improved Bounds for Szemerédi's Theorem` (arXiv:2402.17995), or the exact downstream source actually being relied on for the Hausdorff-dimension upgrade.
   - Right now the repo names these authors but gives no citation at all.

### Upgrade weak arithmetic-Kakeya adjacency entries to canonical records

3. Cowen-Breen, Karangozishvili, Varadarajan, Wang, `Pattern Problems related to the Arithmetic Kakeya Conjecture` (arXiv:2011.07056).
4. Pohoata and Zakharov, `Generalized Arithmetic Kakeya` (arXiv:2411.13395).
5. Tao, `Sum-difference exponents for boundedly many slopes, and rational complexity` (arXiv:2511.15135).

### Normalize publication-state mismatches

6. `green2017`
   - Either cite the final 2019 journal publication consistently or make it an explicit 2017 preprint entry with eprint metadata.
7. `bond2013` and `bond2014`
   - Either cite the final journal versions consistently or mark them as preprints. Do not mix preprint years with 2016 journal metadata.
8. `faldor2024`
   - Either cite the ALIFE proceedings paper consistently using DOI `10.1162/isal_a_00827` or cite the arXiv preprint consistently. Do not mix the two.

### Clean up AI-system references before any paper build

9. Fix author encoding and canonicalization for:
   - `novikov2025`
   - `georgiev2025`

### Optional provenance source

10. If a future writeup wants to cite the exact FrontierMath problem wording or the provenance of the `<= 1.675` target, add a separate task-provenance source explicitly.
    - That should be treated as task provenance, not as a substitute for the underlying research literature.

## Bottom Line

- Citation support is currently adequate for blocker accounting, negative experimental claims, and the narrow design-level story.
- Citation support is currently **not** adequate for:
  - the manuscript-style mathematical introduction,
  - the `11` reframing domains,
  - or section-specific literature-comparison prose that sounds stronger than a title/abstract-level comparison.
- No clear fake paper was found, but several bibliography entries need canonicalization before they can be trusted in a manuscript.
