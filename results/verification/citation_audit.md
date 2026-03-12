# Citation Audit

## Scope

- Verification phase: `post_deepen`
- Primary inputs reviewed:
  - `research_paper.tex`
  - `sources.bib`
  - `results/research_context.md`
  - `results/literature/semantic_scholar_manifest.json`
- Local artifact spot-checks used for traceability:
  - `results/experiments/run_1000000/contract.json`
  - `results/experiments/run_1000000/record_gap_summary.json`
  - `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json`
  - `results/novelty_deepening/checker_agreement.json`
  - `results/novelty_deepening/shared_corpus.json`
  - `results/novelty_deepening/item_026_anchor_metrics.json`
  - `results/novelty_deepening/item_027_schedule_metrics.json`
  - `results/novelty_deepening/item_028_prefix_metrics.json`
  - `results/novelty_deepening/item_029_hypergraph_metrics.json`
  - `results/novelty_deepening/item_029_hypergraph_invariants.md`
  - `results/novelty_deepening/item_030_modular_metrics.json`
  - `results/experiments/runtime_repeats_1000000.json`
  - `results/experiments/variant_comparison.md`
  - `tests/test_prime_separator.py`
  - `tests/test_novelty_deepening.py`
- Focus: evidence traceability and citation support only.

## Overall Assessment

- The manuscript's theorem-level structural claims are supported internally. The paper proves the first-two-missing-values formulation, strict interleaving, unique column term in each row gap, forced axis-1 witness, exact `row_immediate` identity, exact `column_immediate` axis swap, and prime separation from the recurrence itself.
- The main quantitative claims also check out against the stored artifacts. I did not find a numeric mismatch in the spot-checked Results, Discussion, or Conclusion claims.
- The main citation debt is not fabricated numbers but sentence-level traceability. Several strong summary claims in the abstract, discussion, and conclusion restate quantitative findings without the underlying local artifacts at the strongest claim site.
- The main literature-side weakness is over-strengthened positioning language. The active external citations support provenance and nearby comparison classes, but not the stronger novelty-boundary judgments in every place they are currently used.
- No currently cited bibliography key looks fabricated. The highest hallucination risk comes instead from stale or metadata-only supporting infrastructure: `results/research_context.md` and a few dormant `sources.bib` placeholders.

## Key Claims With Adequate Support

### Public provenance

- `research_paper.tex:61`, `research_paper.tex:72`, `research_paper.tex:90`, and `research_paper.tex:110` are adequately supported by `oeisA129258`, `oeisA129259`, and `kimberling100conjectures` for the narrow claims actually made there:
  - the array and first row are public,
  - the opening block and first-row prefix are public,
  - the bounded-difference question is public.

### Structural claims

- `research_paper.tex:72`, `research_paper.tex:99`, `research_paper.tex:261-420`, `research_paper.tex:423-435`, and `research_paper.tex:639-648` are internally supported by the paper's proofs.
- Repo-level support exists in the implementation and tests:
  - `tests/test_prime_separator.py` verifies exact prefix reproduction, repeatable structural digest, `row_immediate == baseline` over 200 steps, and `column_immediate` as an axis swap.

### Baseline computation and replay

- `research_paper.tex:100`, `research_paper.tex:443-462`, and `research_paper.tex:503-545` are supported by:
  - `results/experiments/run_1000000/contract.json`
  - `results/experiments/run_1000000/experiment_note.md`
  - `results/experiments/runtime_repeats_1000000.json`
- The following spot-checks matched exactly:
  - `record_gap_count = 17`
  - `largest_record_gap = 30`
  - late records at steps `92320`, `247399`, and `729353`
  - structural digest `3680d24d2073239978438eaf02f8f05a1ed81da4e52927909c4dc47c0d0291e3`
  - max observed offset `24`, first attained at step `464334`

### Witness and hypergraph summaries

- `research_paper.tex:549-580` is supported by:
  - `results/experiments/run_1000000/record_gap_summary.json`
  - `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json`
- The paper's late-gap composition numbers match the stored artifacts, including:
  - singleton shares `15/18`, `17/19`, `16/20`, `18/24`, `18/27`, `19/29`
  - balanced shares rising from `1/18` to `13/29`
  - composite-only late record gaps `20`, `21`, `28`, and `30`
  - gap-30 full-witness totals: `29` skipped values, `43` admissible pairs, `39` distinct row factors, `41` distinct column factors

### Late matched-control audit metrics

- `research_paper.tex:101`, `research_paper.tex:584-615`, and Supplementary Tables are supported by:
  - `results/novelty_deepening/checker_agreement.json`
  - `results/novelty_deepening/shared_corpus.json`
  - `results/novelty_deepening/item_026_anchor_metrics.json`
  - `results/novelty_deepening/item_027_schedule_metrics.json`
  - `results/novelty_deepening/item_028_prefix_metrics.json`
  - `results/novelty_deepening/item_029_hypergraph_metrics.json`
  - `results/novelty_deepening/item_030_modular_metrics.json`
- The paper's quoted values match the artifacts, including:
  - checker agreement through `10^5` steps
  - shared corpus counts `5` records, `45` controls, `50` surrogates
  - anchor AUROC `0.9224`
  - schedule AUROC `0.9569` versus `0.5259` for length alone
  - prefix depths `27675`, `29372`, `92319`, `247398`, `729352`
  - hypergraph near-miss AUROC `0.8711` with `28.9%` matched-control overlap
  - best small-modulus AUROC `0.5259`

## Priority Findings

### 1. High: literature-positioning claims are stronger than the external citations support

Affected text:

- `research_paper.tex:94`
- `research_paper.tex:110-119`

Issue:

- OEIS and Kimberling support provenance.
- Ford and the multiplicative-basis papers support nearby comparison classes.
- They do not themselves prove stronger judgments such as:
  - reconstruction/reproduction cannot be novel,
  - Ford is the decisive overlap boundary,
  - local factor-coverage explanations would amount to a reformulation of an existing restricted-product-set question,
  - the paper's novelty boundary is settled by those sources alone.

Assessment:

- Most of this language is already close to the right shape because the paper sometimes says "In our assessment".
- The problem is inconsistent sentence-level grounding: some novelty-boundary conclusions still read as source-proved rather than author-judgment plus internal audit.

Recommended fix:

- Keep the novelty and overlap language explicitly as author assessment.
- At the strongest comparison sites, pair the external citations with the internal novelty artifacts:
  - `results/literature/prior_art_gap.md`
  - `results/verification/novelty_report.md`

### 2. Medium: strong summary claims are supported by artifacts but under-cited at the strongest claim site

Affected text:

- `research_paper.tex:72`
- `research_paper.tex:100-102`
- `research_paper.tex:558`
- `research_paper.tex:606-615`
- `research_paper.tex:653-659`
- `research_paper.tex:685-687`

Issue:

- The underlying support exists.
- The abstract, discussion, and conclusion often restate the strongest quantitative takeaways without the relevant artifact at the sentence where the takeaway is made most forcefully.

Examples:

- The abstract says the artifacts show composite-only late records, failure of bounded witness grammar, failure of anchor/backbone, near-miss hypergraph invariants, and nonpredictive modular locking.
- The discussion says the trajectory reaches `30` in baseline and `31` in the axis-swapped run, that composite-only large late gaps occur, and that the anchor geometry is discriminative but not bounded-memory.
- The conclusion compresses several audit outcomes into one paragraph without local citations.

Recommended fix:

- Add local artifact references at the first strong claim site, not only later in tables:
  - `results/experiments/run_1000000/record_gap_summary.json`
  - `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json`
  - `results/novelty_deepening/checker_agreement.json`
  - `results/novelty_deepening/shared_corpus.json`
  - `results/novelty_deepening/item_026_anchor_metrics.json`
  - `results/novelty_deepening/item_027_schedule_metrics.json`
  - `results/novelty_deepening/item_028_prefix_metrics.json`
  - `results/novelty_deepening/item_029_hypergraph_metrics.json`
  - `results/novelty_deepening/item_030_modular_metrics.json`
  - `results/experiments/column_immediate_1000000/contract.json` if the `31` claim stays in Discussion.

### 3. Medium: one table row overstates what its cited JSON alone supports

Affected text:

- `research_paper.tex:599`

Issue:

- The table row says full witness cycle rank is `0` on records, controls, and surrogates.
- The cited JSONs support the AUROC, overlap, and modulus values.
- The explicit cycle-rank statement is surfaced in `results/novelty_deepening/item_029_hypergraph_invariants.md`, not in `results/novelty_deepening/item_029_hypergraph_metrics.json`.

Recommended fix:

- Either cite `results/novelty_deepening/item_029_hypergraph_invariants.md` alongside the JSON, or weaken the row so it states only what is directly present in the cited metrics JSON.

### 4. Medium: `results/research_context.md` is stale and should not be treated as authoritative

Affected files:

- `results/research_context.md`
- `results/literature/semantic_scholar_manifest.json`

Issue:

- `results/research_context.md` contains obviously irrelevant "Closest Prior Art" entries.
- Its activity summary is incomplete relative to the manifest.
- The manifest itself is a query log, not an audit-ready bibliography ledger for the claimed `105` tracked papers.

Implication:

- This does not break the paper's active citations directly.
- It does make the repo's literature-traceability layer unreliable if a reader treats it as authoritative.

Recommended fix:

- Demote `results/research_context.md` to non-authoritative metadata unless regenerated.
- Do not rely on it as a literature audit source in the manuscript or downstream verification notes.

### 5. Low to Medium: bibliography quality is uneven outside the active citation spine

Findings:

- The `10` keys actually cited in `research_paper.tex` all exist in `sources.bib`.
- `5` bibliography entries are currently uncited:
  - `brent2019algorithmsmultiplicationtable`
  - `ford2020roughdivisorinterval`
  - `koukoulopoulos2010restrictedtables`
  - `mehdizadeh2021smoothmultiplicationtable`
  - `meisner2018functionfieldmultiplicationtable`
- The clearest weak entries are metadata-only placeholders:
  - `koukoulopoulos2010restrictedtables`
  - `brent2019algorithmsmultiplicationtable`
- The weakest cited scholarly key is `ford2006divisor2y`, which is presently entered only as an arXiv preprint even though a stronger published chapter record exists.

Assessment:

- This is not an active citation hallucination problem today because the metadata-only entries are not currently cited in the manuscript.
- It becomes a real risk immediately if broader "descendants" or algorithmic multiplication-table language is reintroduced.

## Likely Citation Hallucinations

- No likely citation hallucination appears among the `10` bibliography entries actually cited in `research_paper.tex`.
- The biggest hallucination-risk objects are not active citations but stale support artifacts:
  - `results/research_context.md`
  - metadata-only `sources.bib` placeholders

## Uncited Comparisons To Watch

- `research_paper.tex:119` contrasts the paper with "Ford-style local coverage" and "the multiplicative-basis branch" in a way that is conceptually fair but still interpretive.
- `research_paper.tex:654-658` compares baseline and axis-swapped trajectories while drawing mechanism conclusions. The numbers are supported, but the compressed comparison would benefit from direct local artifacts at the claim site.
- Any future language about "Ford and its descendants", generalized/restricted multiplication tables, or algorithmic multiplication-table comparisons would currently outrun the active citation set.

## Most Important Concrete Sources To Add Or Promote

1. Promote Kevin Ford's published chapter version of `Integers with a divisor in (y, 2y]` if the paper keeps that overlap branch active.
   - This is a better primary record than the current preprint-style `ford2006divisor2y` entry.

2. Replace `koukoulopoulos2010restrictedtables` with a primary thesis or publisher record for:
   - Dimitrios Koukoulopoulos, `Generalized and Restricted Multiplication Tables of Integers`

3. Replace `brent2019algorithmsmultiplicationtable` with the primary publication record for:
   - Brent, Pomerance, Purdum, and Webster, `Algorithms for the Multiplication Table Problem`

4. If the paper broadens into explicit descendant language, promote the already-listed but dormant published descendants:
   - `ford2020roughdivisorinterval`
   - `mehdizadeh2021smoothmultiplicationtable`

## Bottom Line

- The current manuscript is in decent shape for a narrow paper.
- Its core structural and quantitative claims are supported.
- The most important remaining work is not arithmetic correction; it is tightening sentence-level traceability and keeping literature-positioning claims at the level the sources actually support.
