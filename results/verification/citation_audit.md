# Citation Audit

## Coverage Status

### Strong

- `oeisA129258`, `oeisA129259`, and `kimberling100conjectures` cover the core provenance line for the object and the public problem statement.
- `ford2011multiplicationtable` and `ford2008divisorinterval` cover the two main overlap risks identified by the falsifier.
- `results/baseline/run_30000/summary.json` and `results/baseline/run_30000/record_gaps.json` now cover the empirical claims that the baseline reaches record gaps `19`, `20`, and `21`, including the step-`29373` gap `139039 -> 139060` with zero skipped primes.

### Weak

- The exact OEIS comment/reference material behind the prime split and bounded-difference phrasing is only indirectly represented by generic OEIS entries plus the Kimberling problem page.
- `koukoulopoulos2010restrictedtables` and `brent2019algorithmsmultiplicationtable` remain secondary-metadata-only sources and should not carry core claims.

### Missing Or Deferred

- A local claim-to-source matrix for every markdown artifact is still missing and should be completed in Phase 5.
- If later drafts rely on exact OEIS comment wording, a local snapshot or more exact provenance artifact should be added.

## Metadata Issues

- The OEIS and Kimberling entries in `sources.bib` currently use access-year style metadata rather than original publication/update year.
- Some snapshot years came from Semantic Scholar search records while `sources.bib` uses validated DOI metadata. The bibliography is more trustworthy where the two disagree.
- Secondary metadata entries are quarantined as overlap controls only.

## Claim-To-Source Map

- Recurrence definition:
  - `oeisA129258`
  - `oeisA129259`
  - `results/baseline_spec.md`
  - `scripts/prime_separator.py`
- Bounded-difference problem provenance:
  - `kimberling100conjectures`
  - `oeisA129259`
- Ford overlap boundary:
  - `ford2011multiplicationtable`
  - `ford2008divisorinterval`
  - `ford2020roughdivisorinterval`
- Multiplicative-basis overlap boundary:
  - `pach2017multiplicativebases`
  - `pus1992multiplicativebases`
  - `dressler1970newmultiplicativebases`
  - `nathanson1987multiplicativerepresentations`
- Baseline empirical claims:
  - `results/baseline/run_30000/summary.json`
  - `results/baseline/run_30000/record_gaps.json`
  - `results/baseline/test_11/summary.json`

## Audit Conclusion

The repo now has a defensible provenance baseline for OEIS/Kimberling/Ford and a reproducible local artifact for the key empirical claims used by the falsifier. The remaining citation debt is mostly cleanup:

- tighten OEIS/Kimberling metadata;
- keep secondary overlap sources non-load-bearing;
- add final artifact-level claim tracing in Phase 5.
