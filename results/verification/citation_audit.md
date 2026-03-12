# Citation Audit

## Scope

- `research_paper.tex` is not present in this repo, so the audit applies to the current
  note-style outputs rather than to a manuscript.
- Primary inputs reviewed: `sources.bib`, `results/research_context.md`,
  `results/literature/semantic_scholar_manifest.json`,
  `results/verification/claim_source_matrix.md`,
  `results/final_status_note.md`, `results/verification/verification_summary.md`,
  `results/evaluation/literature_comparison.md`,
  `results/research_note_outline.md`, and the supporting local experiment artifacts.
- Focus: evidence traceability and citation support only.

## Overall Assessment

- The provenance baseline is supported. OEIS `A129258`, OEIS `A129259`, and
  Kimberling's problem page are the right sources for the array definition, first-row
  problem statement, and public provenance.
- The finite-horizon empirical claims are also supported, but mostly by local JSON/MD
  artifacts rather than by literature citations. The strongest support comes from:
  - `results/experiments/run_1000000/contract.json`
  - `results/experiments/variant_comparison.md`
  - `results/analysis/h1_h2_gap_summary.json`
  - `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json`
- The weak point is citation placement and comparison discipline. Most final notes cite
  only by indirection through `results/verification/claim_source_matrix.md`, and some
  literature comparisons are broader than the cited sources actually justify.

## Priority Findings

### 1. Missing claim-site citations in the final outputs

Affected files:

- `results/final_status_note.md:12-25`
- `results/verification/verification_summary.md:11-21`
- `results/evaluation/literature_comparison.md:17-35`

Issue:

- These sections make concrete numerical and interpretive claims, but the only source
  note is a generic end pointer to `claim_source_matrix.md` and `sources.bib`.
- That is enough for internal traceability, but it is weak citation practice because the
  reader cannot tell which claims come from OEIS/Kimberling, which come from Ford, and
  which come from local experiment artifacts.

Impact:

- High. The claims are mostly supportable, but the support is not attached at the point
  of use.

Recommended fix:

- Add direct local-artifact citations next to empirical claims.
- Reserve bibliography citations for provenance and literature comparisons.

### 2. The Ford overlap comparison is under-cited and too coarse

Affected files:

- `results/evaluation/literature_comparison.md:37-61`
- `results/literature/prior_art_gap.md:31-46`
- `results/verification/claim_source_matrix.md:14-17`

Issue:

- The repo repeatedly says the witness story is "Ford-like", "closer to
  divisor/product coverage", or collapses toward the Ford branch.
- The matrix maps these sections to `ford2011multiplicationtable` and
  `ford2008divisorinterval`, but no claim is tied to a specific theorem, section, or
  result from those papers.
- As written, this is a valid research concern, but not a fully cited mathematical
  comparison.

Impact:

- High. This is the main literature-overlap claim in the package.

Recommended fix:

- Either cite the exact Ford results being invoked, or soften the language to
  "overlap risk / heuristic resemblance" rather than a source-backed comparison.
- Promote `ford2006divisor2y` when the point is specifically local divisor coverage in
  a short interval; that source is closer to the frontier-coverage language than the
  multiplication-table paper alone.

### 3. Section 4 of the literature memo contains uncited cross-domain comparisons

Affected file:

- `results/evaluation/literature_comparison.md:81-106`

Issue:

- The memo compares the data against nonunique factorization theory, combinatorics on
  words / symbolic dynamics, Beatty/complementary-sequence framing, uniform mex
  periodicity, and statistical-physics / adsorption language.
- `results/verification/claim_source_matrix.md:14` does not map any sources for those
  domains, and `sources.bib` contains none of them.

Impact:

- High for external-facing writing, medium for internal brainstorming.

Recommended fix:

- Remove these comparisons from any final paper/note unless they are backed by actual
  references.
- If the factorization framing is kept, add a real source for that domain; otherwise
  present the section as internal pruning only, not literature comparison.

### 4. The claim-source matrix is too coarse and sometimes mismatched

Affected file:

- `results/verification/claim_source_matrix.md:9-17`

Issue:

- The matrix is artifact-level, not claim-level.
- Example: `results/final_status_note.md` is mapped to the Ford papers, but its most
  important support is local evidence about gaps `25`, `28`, `30`, and variant gap `31`.
- Example: the "strongest supported mechanism" in `results/final_status_note.md:20-25`
  depends directly on the hypergraph and gap-summary exports, but those artifacts are
  not named in the matrix row for that file.

Impact:

- Medium. The matrix helps, but it overstates precision.

Recommended fix:

- Split the matrix by claim family, not only by artifact.
- For each claim family, list the exact local artifact and the exact literature source,
  if any.

### 5. Two bibliography entries are weak metadata placeholders

Affected file:

- `sources.bib:72-79`
- `sources.bib:143-149`

Issue:

- `koukoulopoulos2010restrictedtables` is currently only a Semantic Scholar metadata
  landing page.
- `brent2019algorithmsmultiplicationtable` is also stored only as Semantic Scholar
  metadata.
- These entries are not obvious hallucinations, but they are weak bibliographic records
  and should not be load-bearing.

Impact:

- Medium. They are currently peripheral, but they are the most plausible citation-risk
  entries in the bibliography.

Recommended fix:

- Replace `koukoulopoulos2010restrictedtables` with a primary thesis/dissertation
  citation for *Generalized and Restricted Multiplication Tables of Integers*.
- Replace `brent2019algorithmsmultiplicationtable` with the actual arXiv and/or journal
  record for *Algorithms for the Multiplication Table Problem*.

## Supported Claims

These claims do have identifiable support in the current repo.

- Provenance of the object and target question:
  supported by `oeisA129258`, `oeisA129259`, and `kimberling100conjectures`.
- "Still unresolved" as the global status:
  supported by the combination of the million-step baseline, the two nearby variants,
  and the absence of any proof-level invariant in the stored claim sheets.
- Large composite-only record gaps:
  supported by `results/experiments/run_1000000/contract.json`,
  `results/experiments/variant_comparison.md`, and
  `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json`.
- Rejection of the strong raw-witness certificate claim:
  supported by `results/claims/h1_frontier_witness_certificate.md`,
  `results/analysis/h1_h2_gap_summary.json`, and the late-gap hypergraph export.
- Rejection of H2 as an explanatory mechanism:
  supported by `results/claims/h2_prime_support_fixed_point.md` and the shared-corpus
  summaries in `results/analysis/h1_h2_gap_summary.json`.

## Likely Hallucinations Or Weak Citations

- No obvious hallucination appears among the load-bearing provenance and Ford entries.
- The closest citation-risk items are the metadata-only placeholders:
  - `koukoulopoulos2010restrictedtables`
  - `brent2019algorithmsmultiplicationtable`
- The more immediate problem is not fabricated sources, but unsupported comparison
  language and missing claim-site attribution.

## Most Important Sources To Add Or Promote

1. Promote direct local evidence citations in the final outputs:
   - `results/experiments/run_1000000/contract.json`
   - `results/experiments/variant_comparison.md`
   - `results/analysis/h1_h2_gap_summary.json`
   - `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json`

2. Promote `ford2006divisor2y` into the comparison memo when the argument is specifically
   about short-interval divisor coverage near the frontier.

3. Replace the metadata-only Koukoulopoulos entry with the primary thesis/dissertation
   record for *Generalized and Restricted Multiplication Tables of Integers*.

4. Replace the metadata-only Brent entry with the actual arXiv and/or journal record for
   *Algorithms for the Multiplication Table Problem*.

5. If `results/evaluation/literature_comparison.md:81-106` is kept, add real references
   for whichever external framing survives; otherwise delete that comparison block from
   any external-facing note.

## Bottom Line

- The repo's key empirical and provenance claims are mostly supportable.
- The main citation debt is structural:
  - evidence is routed through a coarse source matrix instead of being cited at the
    claim site;
  - the Ford overlap comparison is broader than the current citations justify;
  - the cross-domain comparison block is uncited.
- Before any manuscript draft, tighten the comparison claims first and replace the two
  metadata-only bibliography placeholders.
