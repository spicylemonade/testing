# Citation Audit

## Scope

- Review round: `review_round_1`.
- Primary inputs reviewed:
  - `research_paper.tex`
  - `sources.bib`
  - `results/research_context.md`
  - `results/literature/semantic_scholar_manifest.json`
- Additional repo spot-checks used for evidence traceability:
  - `scripts/prime_separator.py`
  - `scripts/prime_separator_variants.py`
  - `scripts/make_paper_figures.py`
  - `tests/test_prime_separator.py`
  - `results/experiments/run_1000000/contract.json`
  - `results/experiments/run_1000000/row_terms.json`
  - `results/experiments/run_1000000/column_terms.json`
  - `results/experiments/run_1000000/record_gap_summary.json`
  - `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json`
- Focus: evidence traceability and citation support only.

## Overall Assessment

- The manuscript's theorem-level claims are mostly well supported internally. The exact recurrence identities, interleaving, unique column term, forced unit witness, prime separation, and variant identities are proved in `research_paper.tex`; these are not missing-citation problems.
- The manuscript's main computational claims are also mostly supported. The million-step record-gap totals, late-record locations, offset maximum, witness shares, and late-gap hypergraph counts all trace to concrete local artifacts and are consistent with the repo's scripts and tests.
- The main citation debt is in the literature-positioning language. The paper repeatedly presents novelty-boundary judgments and prior-art comparisons as if the cited literature itself proves those judgments. In most cases, the citations establish topic adjacency, not the stronger claims actually written.
- No load-bearing cited source looks fabricated. The highest source-quality risk is instead two uncited metadata-only bibliography placeholders in `sources.bib`.

## Key Claims That Are Supported

### Provenance and public problem statement

- `research_paper.tex:60`, `research_paper.tex:84-90`, and `research_paper.tex:107-108` are supported by `oeisA129258`, `oeisA129259`, and `kimberling100conjectures`.
- These sources are the right support for:
  - the array definition and initial block,
  - the first-row sequence provenance,
  - the statement that the bounded-difference question is already public.

### Structural and variant claims

- `research_paper.tex:95-97`, `research_paper.tex:227-376`, `research_paper.tex:423-429`, and `research_paper.tex:530-537` are internally supported by the paper's proofs.
- Repo-level implementation support also exists:
  - `scripts/prime_separator.py` defines the baseline recurrence, prefix validation, and structural digest.
  - `scripts/prime_separator_variants.py` encodes the `row_immediate` and `column_immediate` runs.
  - `tests/test_prime_separator.py` checks:
    - exact baseline prefix reproduction,
    - repeatable structural digest,
    - exact equality of `row_immediate` with baseline over 200 steps,
    - exact axis-swap behavior of `column_immediate` over 200 steps.

### Quantitative computational claims

- `research_paper.tex:439` is supported by direct scan of `results/experiments/run_1000000/row_terms.json` and `results/experiments/run_1000000/column_terms.json`:
  - maximum observed offset `24`,
  - attained at step `464334`.
- `research_paper.tex:449-455` and Table 1 are supported by `results/experiments/run_1000000/contract.json`:
  - `record_gap_count = 17`,
  - `largest_record_gap = 30`,
  - late record locations:
    - gap `25` at step `92320`,
    - gap `28` at step `247399`,
    - gap `30` at step `729353`.
- `research_paper.tex:494-503` and the supplementary table are supported by `results/experiments/run_1000000/record_gap_summary.json`:
  - gap `19`: singleton `15/18`, balanced `1/18`,
  - gap `20`: singleton `17/19`, balanced `1/19`,
  - gap `21`: singleton `16/20`, balanced `3/20`,
  - gap `25`: singleton `18/24`, balanced `7/24`,
  - gap `28`: singleton `18/27`, balanced `9/27`,
  - gap `30`: singleton `19/29`, balanced `13/29`.
- `research_paper.tex:513-521` is supported by `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json`:
  - gap `30` has `29` skipped values,
  - `43` full witness pairs,
  - `39` distinct row factors,
  - `41` distinct column factors,
  - multiplicity histogram `19 x 1`, `8 x 2`, `1 x 3`, `1 x 5`.

## Priority Findings

### 1. High: the Ford-overlap claims are stronger than the citations support

Affected text:

- `research_paper.tex:90`
- `research_paper.tex:110-112`
- `research_paper.tex:174`
- `research_paper.tex:580`

Issue:

- The Ford citations support that multiplication-table and divisor-in-interval problems are nearby mathematical territory.
- They do not, by themselves, support stronger claims such as:
  - this is the "nearest serious literature branch",
  - this is the "correct overlap branch",
  - local factor-coverage explanations would amount to a "renaming" of the Ford phenomenon,
  - clearing the "Ford overlap boundary" is the decisive novelty test.
- Those are author judgments about novelty and overlap, not direct consequences of the Ford papers.

Why this matters:

- This is the manuscript's main literature-positioning argument.
- As written, it risks reading as source-backed prior-art exclusion when it is really a comparative assessment.

Recommended fix:

- Rephrase these sentences as explicit author judgments: "In our assessment...", "The closest overlap risk appears to be...", or "A plausible prior-art branch is...".
- If the stronger boundary language is retained, cite the internal novelty artifacts at the claim site:
  - `results/literature/prior_art_gap.md`
  - `results/verification/novelty_report.md`
- If "Ford and its descendants" remains, either cite the descendants actually meant or drop that phrase.

### 2. High: novelty conclusions are presented as if OEIS/Kimberling themselves prove them

Affected text:

- `research_paper.tex:107`
- `research_paper.tex:118`

Issue:

- The OEIS and Kimberling sources support public provenance.
- They do not themselves prove the manuscript-level conclusions that:
  - no paper on the object can claim novelty from reconstruction/reproduction alone,
  - the present work adds exactly the three named items beyond OEIS/Kimberling.
- Those are reasonable inferences, but still inferences.

Why this matters:

- The paper is disciplined about not overclaiming mathematically, but these novelty statements are currently stronger than the citations attached to them.

Recommended fix:

- Mark these as inference: "Accordingly, we do not treat reconstruction alone as novel."
- Or attach the repo's internal novelty analysis directly at those sentences:
  - `results/literature/prior_art_gap.md`
  - `results/verification/novelty_report.md`

### 3. Medium: the multiplicative-basis comparison is weakly cited and partly interpretive

Affected text:

- `research_paper.tex:114-118`

Issue:

- The cited multiplicative-basis papers support the existence of that literature class.
- They do not directly support the stronger warning that adopting that framing would make the project "drift away from the actual recurrence and toward a different established topic."

Why this matters:

- This is another literature-pruning argument. It is plausible, but the current references support the domain, not the pruning decision.

Recommended fix:

- Soften to "would move the discussion toward a different comparison class" or similar.
- Or add a direct citation to the internal novelty analysis where this pruning judgment is actually made.

### 4. Medium: several load-bearing negative computational conclusions are supported by artifacts but not cited at their strongest claim sites

Affected text:

- `research_paper.tex:70`
- `research_paper.tex:98-99`
- `research_paper.tex:494-503`
- `research_paper.tex:521`
- `research_paper.tex:564`
- `research_paper.tex:588`

Issue:

- The underlying support exists, but the strongest interpretive claims often appear in abstract/introduction/discussion/conclusion form with no direct artifact attached at the sentence level.
- Example phrases:
  - "composite-only large gaps persist",
  - "singleton witnesses dominate",
  - "balanced witnesses grow rather than compress",
  - "the witness data do not compress into a compact frontier certificate",
  - "prime obstruction is not the governing phenomenon".

Why this matters:

- These are among the most important takeaways of the paper.
- The relevant artifacts are present, but a reader has to infer which dataset supports which conclusion.

Recommended fix:

- Add explicit artifact references when these claims first appear outside the detailed results section:
  - `results/experiments/run_1000000/record_gap_summary.json`
  - `results/analysis/full_witness_hypergraphs_gap21_25_28_30.json`
  - the corresponding tables/figures already in the manuscript.

### 5. Medium: "prediction" language for the rejected compact-certificate hypothesis is not sourced

Affected text:

- `research_paper.tex:494`
- `research_paper.tex:503`
- `research_paper.tex:526`

Issue:

- The data do support the observed trends.
- What is not cited is the stronger comparative language about what a "compact tiny-factor certificate would predict" or what would count as a "low-description frontier certificate."

Why this matters:

- This is hypothesis language imported from the repo's internal program rather than from a cited external source.

Recommended fix:

- Either recast as internal hypothesis framing:
  - "under the repository's compact-certificate hypothesis..."
- Or cite the internal claim documents directly:
  - `results/claims/h1_frontier_witness_certificate.md`
  - `results/analysis/h1_h2_gap_summary.json`

### 6. Low: `results/research_context.md` is not a reliable traceability summary

Affected files:

- `results/research_context.md:14-25`
- `results/literature/semantic_scholar_manifest.json:276-388`

Issue:

- `results/research_context.md` lists obviously irrelevant "Closest Prior Art" items and reports only three BibTeX pulls in its activity summary.
- The manifest records six `bibtex` fetches.

Why this matters:

- This does not directly break the paper's citations, but it weakens the pipeline's evidence ledger and makes traceability summaries harder to trust.

Recommended fix:

- Treat `results/research_context.md` as stale metadata, not as an authoritative literature ledger.
- If it remains in the pipeline, regenerate it from the manifest rather than from a lossy summary path.

## Weak Citations And Likely Citation-Risk Entries

- No obvious citation hallucination appears among the ten bibliography entries actually cited in `research_paper.tex`.
- The two clearest weak bibliography entries are uncited metadata-only placeholders:
  - `sources.bib:72-79` — `koukoulopoulos2010restrictedtables`
  - `sources.bib:143-149` — `brent2019algorithmsmultiplicationtable`
- Both entries point only to Semantic Scholar landing pages, not primary records.
- Five of the fifteen `sources.bib` entries are uncited:
  - `brent2019algorithmsmultiplicationtable`
  - `ford2020roughdivisorinterval`
  - `koukoulopoulos2010restrictedtables`
  - `mehdizadeh2021smoothmultiplicationtable`
  - `meisner2018functionfieldmultiplicationtable`

## Most Important Concrete Sources To Add Or Promote

1. Replace the metadata-only Koukoulopoulos placeholder with a primary record if the paper keeps "restricted/generalized multiplication table" descendant language.
   Suggested source:
   - Dimitris Koukoulopoulos, `On the number of integers in a generalized multiplication table` (arXiv:1102.3236; Journal fur die reine und angewandte Mathematik 689 (2014), 33-99).

2. Replace the metadata-only Brent placeholder with the primary preprint or published record if algorithmic multiplication-table comparison remains in `sources.bib`.
   Suggested source:
   - Richard Brent, Carl Pomerance, David Purdum, Jonathan Webster, `Algorithms for the Multiplication Table Problem` (arXiv:1908.04251; later published in `INTEGERS` 21 (2021), Paper A92).

3. If the manuscript keeps the phrase "Ford and its descendants," either cite or remove the descendants actually meant.
   Already in `sources.bib` and available to promote:
   - `ford2020roughdivisorinterval`
   - `mehdizadeh2021smoothmultiplicationtable`

4. If the compact-certificate rejection remains a central framing device, cite the repo's own hypothesis artifacts where that framing is introduced:
   - `results/claims/h1_frontier_witness_certificate.md`
   - `results/analysis/h1_h2_gap_summary.json`

## Bottom Line

- The paper's main mathematical and finite-horizon computational claims do have support.
- The most important problems are not missing facts but overstated source roles:
  - literature-comparison claims are stronger than the papers cited for them,
  - novelty conclusions are written as if they are source-backed rather than inferred,
  - the strongest negative computational conclusions need more explicit artifact references at first mention.
- Before external circulation, the highest-value repair is to tighten the Ford/novelty language and attach claim-site evidence to the abstract/introduction/conclusion summaries.
