# Citation Audit

## Verdict

- Verdict: pass after the peer-review revision.
- The citation base covers the required branches: Beatty/Sturmian/Ostrowski, Beatty model theory, linearly recurrent subshifts/S-adic structure, generalized polynomials/Pisot-Salem, Skolem-Mahler-Lech, uniform recurrence, Beatty variants, and the Walnut/Pecan software-tool lane.

## What was repaired

- Corrected the peer-review mismatches for `gnaydin2020`, `byszewski2016`, `adamczewski2022`, `bell2005`, and `derksen2005` using publisher-grade DOI metadata.
- Replaced Semantic Scholar URLs in `sources.bib` with canonical DOI or arXiv URLs wherever available.
- Replaced the placeholder software entries with clean arXiv software-paper references: `mousavi2016walnut` and `oei2021pecan`.

## Remaining caution

- The raw lexical watchlist is still a search artifact, not a citation source. Outward-facing text should keep citing the curated branch notes and comparison tables instead of the noisy `top_papers` snapshot.
- Walnut and Pecan remain uncited in `research_paper.tex`; if the writer pass does not mention them, the final manuscript can simply omit those bibliography entries.
