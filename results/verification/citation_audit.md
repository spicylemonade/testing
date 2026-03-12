# Citation Audit

## Coverage Status

### Strong

- `sources.bib` currently contains `15` entries, which clears the minimum depth target.
- The provenance baseline is covered by `oeisA129258`, `oeisA129259`, and
  `kimberling100conjectures`.
- The main overlap boundary is covered by `ford2011multiplicationtable` and
  `ford2008divisorinterval`, with multiplicative-basis controls also present.
- The final written artifacts now point to
  `results/verification/claim_source_matrix.md`, which maps each major artifact to
  bibliography keys and local evidence files.
- The empirical claims used in the final package are backed by reproducible local
  artifacts:
  - `results/baseline/run_30000/contract.json`
  - `results/baseline/run_30000/record_gaps.json`
  - `results/experiments/run_1000000/contract.json`
  - `results/experiments/run_1000000/experiment_note.md`
  - `results/experiments/variant_comparison.md`

### Weak

- OEIS entries in `sources.bib` still use access-year style metadata and should be
  treated as provenance references rather than polished bibliographic records.
- Secondary-metadata items such as `koukoulopoulos2010restrictedtables` and
  `brent2019algorithmsmultiplicationtable` remain overlap controls only, not
  load-bearing sources.

### Resolved During This Phase

- Removed stale references to deleted `summary.json` files.
- Added a claim-to-source matrix that explicitly maps the final memo, outline, novelty
  report, benchmark report, and literature comparison to bibliography keys and local
  evidence.
- Added explicit `sources.bib` / source-matrix pointers to the substantive written
  artifacts used in the closing package.

## Claim-To-Source Map

Primary map: `results/verification/claim_source_matrix.md`

Load-bearing final claims:

- provenance of the object and open problem:
  - `oeisA129258`
  - `oeisA129259`
  - `kimberling100conjectures`
- overlap boundary:
  - `ford2011multiplicationtable`
  - `ford2008divisorinterval`
  - `pach2017multiplicativebases`
- final empirical status:
  - `results/experiments/run_1000000/contract.json`
  - `results/experiments/run_1000000/experiment_note.md`
  - `results/experiments/variant_comparison.md`
  - `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json`

## Audit Conclusion

The closing package now has a coherent citation trail:

- bibliography depth is adequate;
- the named prior work used in comparisons is mapped consistently;
- the final status memo is tied both to `sources.bib` and to concrete local evidence.

Residual citation debt is modest:

- improve OEIS/Kimberling metadata if preparing an external paper draft;
- verify or quarantine the secondary multiplication-table records if they ever become
  load-bearing.
