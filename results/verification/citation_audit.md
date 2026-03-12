# Citation Audit

## Verdict

- Verdict: conditional pass.
- The citation base now covers the required branches: Beatty/Sturmian/Ostrowski, Beatty model theory, linearly recurrent subshifts/S-adic structure, generalized polynomials/Pisot-Salem, Skolem-Mahler-Lech, uniform recurrence, and Beatty variants.

## Blockers

- `sources.bib` needed metadata normalization; the obvious year/venue mismatches were repaired, but software references (Walnut/Pecan) are still only documented in the literature snapshot and repository-search note, not yet cited in BibTeX form.
- The raw lexical snapshot still contains noisy false positives, so outward-facing text should cite the curated branches rather than the raw `top_papers` list.

## Recommended Follow-Up

- Add formal software citations for Walnut and Pecan if they are mentioned in the final package.
- When writing the final claim memo, cite the exact branch rows from `results/experiments/literature_baseline_comparison.md` rather than relying on broad umbrella citations.
