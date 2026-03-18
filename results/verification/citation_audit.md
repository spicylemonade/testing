# Citation Audit

## Scope

- `research_paper.tex` is absent, so this audit covers the claim-bearing repo artifacts instead:
  - `results/research_context.json`
  - `results/research_context.md`
  - `sources.bib`
  - `results/literature/semantic_scholar_manifest.json`
  - `results/phase4_h1_frontier.md`
  - `results/phase4_h2_screen.md`
  - `results/phase4_ablations.md`
  - `results/verification/verification_summary.md`
  - `results/phase5_ca_vs_search_prior.md`
  - `results/final_handoff.md`
  - `results/swarm/gap_map.md`
  - `results/swarm/falsifier.md`
- I distinguish:
  - repo-backed experimental claims, which should cite result files inside `results/`;
  - literature/background claims, which need support from `sources.bib` or additional primary sources.

## Findings

### 1. Missing core citations in the intro / problem background

Severity: high

The task text embedded in `results/research_context.json` makes several mathematical-history claims that are not fully supported by the current bibliography:

- arithmetic Kakeya was implicitly formulated by Katz and Tao;
- `AK(2)` is trivial;
- `AK(alpha)` implies the Hausdorff-dimension lower bound
  `alpha^{-1} d + 1 - alpha^{-1}`;
- Bourgain established the `method of slices` / Minkowski-dimension version;
- the Hausdorff-dimension upgrade follows from work of Leng, Sah, and Sawhney.

Current support is incomplete:

- `sources.bib` has Katz-Tao / Green-Ruzsa / Cowen-Breen / Pohoata-Zakharov, but no Bourgain Kakeya-dimension paper.
- `sources.bib` does not include the specific Leng-Sah-Sawhney paper named in the prose.
- There is no direct citation for the exact Hausdorff-dimension-upgrade sentence.

Verdict:

- The background section is under-cited and should not be used in a paper as-is.

### 2. Frontier-status claims are being sourced too indirectly

Severity: high

`results/swarm/gap_map.md` currently treats the FrontierMath / Epoch note as support for research-state claims:

- current explicit limit `1.6751308`;
- `X` must grow without bound near that limit;
- the easy `3/2` barrier for elementary arguments.

That is too weak for a paper citation trail.

Current support:

- `sources.bib` contains `epochai2025arithmetickakeya`, which is acceptable as task context.
- `sources.bib` contains `tao2025`, which is good support for "the current best upper bound is about `1.67513...`" and for the bounded-slope / rational-complexity warning line.
- `sources.bib` does not contain the primary papers needed for the stronger `1.6751308`, unbounded-`X`, or `3/2`-barrier statements.

Verdict:

- Keep `epochai2025arithmetickakeya` only as a task/frontier note.
- Replace theorem/history statements with primary citations before publication.

### 3. The negative experimental result is mostly supported, but it must be cited to repo artifacts, not to the bibliography

Severity: medium

The central negative claims are traceable in the repo:

- H1 exact one-seed obstruction:
  - `results/phase4_h1_frontier.md`
  - `results/phase4_h1_obstruction.json`
- H2 adds no screening value on the tested family set:
  - `results/phase4_h2_screen.md`
  - `results/phase4_h2_screen.json`
- direct width-4 / width-6 controls around score `2.0`:
  - `results/phase4_width4_seed601.json`
  - `results/phase4_width6_seed602.json`
- width-4 fragility under seed / `R` / `T` perturbations:
  - `results/phase4_ablations.md`
  - `results/phase4_ablations.json`

This supports a narrow claim only:

- the frozen H1 route is exactly obstructed;
- H2 adds no value on the tiny screened family set;
- surviving direct corridor controls stay around `2.0` and are fragile.

Verdict:

- These claims are supportable if the writeup cites the actual result files.
- They should not be cited to Green-Ruzsa, Tao 2025, or any other external paper.

### 4. Several literature-comparison sentences are only partially supported

Severity: medium

The final narrative repeatedly says that the surviving controls remain in a bounded-slope / low-rational-complexity basin:

- `results/phase4_h1_frontier.md`
- `results/phase4_ablations.md`
- `results/verification/verification_summary.md`
- `results/phase5_ca_vs_search_prior.md`

What is supported:

- `tao2025` is the correct barrier paper for bounded-slope / rational-complexity caution.

What is missing:

- the repo does not store an explicit rational-complexity measurement for the width-4 / width-6 / width-8 survivors;
- the claim is therefore interpretive, not directly measured.

Verdict:

- Keep this language only if it is explicitly framed as "consistent with" or "suggestive of", and cite both:
  - the local result artifact; and
  - `tao2025`.
- If the sentence is meant as a measured fact, add the missing slope / complexity summaries first.

### 5. `sources.bib` contains several hybrid records

Severity: medium

I do not see an obviously fabricated paper in `sources.bib`, but I do see multiple weak records that combine preprint-year metadata with journal DOI / journal venue metadata.

Most important keys to normalize:

- `green2017`
- `bond2013`
- `bond2014`
- `bond2015`
- `bollobas2014`
- `hartarsky2018`
- `kubica2018`
- `hemenway2013`

Pattern:

- arXiv/preprint year in `year={...}`;
- later journal venue and DOI in the same entry;
- in one case (`bollobas2014`) the author spelling is also garbled.

Verdict:

- These are weak citations, not clear hallucinations.
- Normalize each one to a single version:
  - either preprint metadata only;
  - or journal metadata only, with the journal publication year.

### 6. Some novelty-positioning claims are uncited inferences or likely overreads

Severity: medium

The most important ones:

- `results/swarm/gap_map.md` says the verifier-friendly `X`-constructible / forcing-pair language is a repackaging of Katz-Tao small-graph methods rather than a mature standalone subliterature.
- `results/swarm/gap_map.md` says Tao 2025 shows automated experiments improved lower bounds more readily than upper bounds.
- `results/swarm/falsifier.md` says abelian networks explicitly contain bootstrap percolation as an example.

These may be reasonable working interpretations, but the current repo does not attach precise citations to them.

Verdict:

- Treat them as author inference unless exact sources are added.
- The Tao 2025 lower-bound / upper-bound gloss is the closest thing here to a likely citation overread.

## Claim Support Matrix

| Claim | Support status | What should be cited |
| --- | --- | --- |
| H1 fails before scoring by an exact one-seed obstruction | supported | `results/phase4_h1_obstruction.json`, `results/phase4_h1_frontier.md` |
| H2 adds no screening value on the tested family set | supported, local only | `results/phase4_h2_screen.json`, `results/phase4_h2_screen.md` |
| Best direct controls are around score `2.0` on width 4 and 6 | supported | `results/phase4_width4_seed601.json`, `results/phase4_width6_seed602.json`, plus summary markdown if desired |
| Width-4 survivor is boundary-sensitive / fragile under ablation | supported | `results/phase4_ablations.json`, `results/phase4_ablations.md` |
| Surviving controls sit in a bounded-slope / low-rational-complexity basin | partially supported | local artifacts plus `tao2025`, or else soften wording |
| Arithmetic Kakeya background and Hausdorff-dimension implication paragraph | under-supported | add primary math citations; current `sources.bib` is insufficient |
| Current explicit limit `1.6751308`, unbounded-`X` near the limit, `3/2` elementary barrier | under-supported | add primary frontier/history papers; do not rely on `epochai2025arithmetickakeya` alone |

## Most Important Sources To Add

1. Jean Bourgain, *On the dimension of Kakeya sets and related maximal inequalities*.

- Needed for the `method of slices` / Minkowski-dimension discussion in the intro.

2. The exact Leng-Sah-Sawhney paper intended by the Hausdorff-dimension-upgrade sentence.

- The obvious candidate is *Improved Bounds for Szemeredi's Theorem*.
- Verify that it is in fact the paper being used before citing it.

3. Nets Katz and Terence Tao, *New bounds for Kakeya problems*.

- Needed if the writeup keeps the historical improvement line around `AK(7/4)` or the small-graph / concrete-construction discussion.

4. The Katz paper behind the `3/2` elementary-argument ceiling.

- `gap_map.md` and `falsifier.md` use this as a live objection, but `sources.bib` does not currently support it.

5. The primary paper(s) behind the current explicit `1.6751308` construction.

- If the writeup only needs "the current best upper bound is about `1.67513...`", `tao2025` is adequate.
- If it keeps the stronger `1.6751308` plus unbounded-`X` wording, add the primary construction papers instead of citing the Epoch page.

## Highest-Leverage Repairs Inside `sources.bib`

- Normalize the hybrid preprint/journal entries listed above.
- Add full journal metadata to `katz1999` if the journal version is intended.
- Decide whether `cowenbreen2020`, `pohoata2024`, and `tao2025` should stay as preprint-style entries rather than incomplete `@article` records.

## Audit Verdict

The final narrow negative position is supportable, but only if the writeup keeps the citation boundary clean:

- experimental outcomes must cite repo artifacts;
- historical and frontier claims must cite primary papers, not just Semantic Scholar or FrontierMath pages;
- bounded-slope / rational-complexity comparisons must be framed as interpretation unless explicit measurements are added.

No obvious nonexistent paper was found in `sources.bib`, but there is substantial metadata drift and several uncited comparison sentences. The main citation risk is over-claiming from secondary sources or from inference-heavy novelty language, not a single fake reference.
