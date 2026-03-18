# Citation Audit

Review phase: `review_round_1`

## Scope

Read directly:

- `research_paper.tex`
- `sources.bib`
- `results/research_context.md`
- `results/literature/semantic_scholar_manifest.json`

Checked against direct support artifacts:

- `results/frontier/order_668_64m/seed_manifest.json`
- `results/frontier/order_668_64m/source_excerpt.txt`
- `results/analysis/frontier_locality_scan.json`
- `results/experiments/order_668_64m/summary.json`
- `results/experiments/controls/summary.json`
- `results/experiments/order_668_64m/runs/H1_defect_syndrome_ca_64m.json`
- `results/branches/H1_frontier_sensitivity_probe.json`
- `results/verification/benchmark_gate.md`
- `hadamard_ca/harness.py`
- `hadamard_ca/h1_ca.py`

Also spot-checked a small number of cited bibliography entries against primary web sources to distinguish real citation gaps from metadata problems.

## Bottom Line

- The paper's core quantitative negative-result claims are mostly supported by direct repo artifacts.
- The weakest part of the citation story is not the main numbers. It is the literature-positioning and interpretation language around lines `115-127`, `624`, `650-655`, `686-698`, and `702`.
- No citation key used in `research_paper.tex` looks fabricated. The real risk is weaker than a fake-paper failure: several BibTeX entries have mixed, incomplete, or likely incorrect metadata.
- The highest-value fixes are:
  - tighten or re-cite the related-work comparison paragraphs
  - label mechanism and runtime explanations as inference unless new evidence is added
  - correct a few bibliography entries before final paper assembly
  - promote direct artifact paths near the paper's load-bearing quantitative claims

## Prioritized Findings

### 1. Related-work comparison language outruns the cited sources

`research_paper.tex:115-127` contains the strongest citation-support problem in the manuscript.

- Line `115` cites `suksmono2018`, `suksmono2019`, and `suksmono2022` for broader Hadamard-search heuristics, which is fine.
- The next sentence goes further and says those papers are "the correct literature comparators" and that the repo pilot is "fair enough for branch elimination." Those are author judgments, not claims directly supported by the cited papers.
- Line `121` uses `tsompanas2017` appropriately for "CA have been used in search," but line `123` then narrows the defensible niche for H1 to seed-specific repair on order `668`. That narrowing is an inference, not something established by `tsompanas2017`, `mariot2019_mols`, or `gadouleau2020`.
- Line `127` compresses four comparison claims into one paragraph:
  - versus `eliahou2025_64mod668`
  - versus `tsompanas2017`
  - versus the Suksmono papers
  - versus the Bright papers
  Only the final clause in that paragraph carries an explicit citation. As written, this reads as an uncited synthesis.

Audit judgment:

- Support status: `partial / weak`
- Fix: either attach citations to each comparison clause or explicitly label the whole paragraph as the paper's synthesis of the sources cited in the preceding subsections.

### 2. Several mechanism and causal statements are interpretation, not evidence

The manuscript is generally careful, but a few passages still read more strongly than the evidence supports.

- `research_paper.tex:73`
  - "If a future CA branch is to remain credible, it must change the actuator basis or the locality graph rather than merely retune the present rule weights."
  - The one-packet scan and sensitivity probe support this as a reasonable recommendation, but not as a proven necessity.
- `research_paper.tex:624`
  - "H1 is substantially slower despite fewer objective evaluations, reflecting the heavier internal field computation tracked separately by the CA metadata."
  - The measured part is supported: H1 is slower and uses fewer objective evaluations.
  - The causal clause is only partly supported. The appendix proves arithmetic consistency of `ca_field_evaluations`; it does not isolate runtime causality.
- `research_paper.tex:650-655`
  - "The problem is not an obviously omitted scalar hyperparameter. It is a structural mismatch between the frontier defect geometry and the current single-packet actuator library."
  - The sensitivity probe supports "simple nearby parameter changes did not help." It does not fully prove the stronger structural diagnosis.
- `research_paper.tex:686-698`
  - The "fake locality" diagnosis is well motivated by the exhaustive one-packet scan.
  - The next-step claims about representation-changing variants are still recommendation-level inferences, not citation-backed results.

Audit judgment:

- Support status: `mixed`
- Fix: keep the numerical observations, but relabel the mechanism story as interpretation unless matched actuator-basis ablations or profiling are added.

### 3. Direct quantitative claims are mostly supported, but artifact traceability in the manuscript is thinner than it should be

The paper's main numbers are in good shape when checked against saved artifacts:

- Seed provenance and the `13` exceptional coefficients:
  - supported by `results/frontier/order_668_64m/seed_manifest.json`
  - supported by `results/frontier/order_668_64m/source_excerpt.txt`
  - supported externally by `eliahou2025_64mod668`
- Control exactness claims:
  - supported by `results/experiments/controls/summary.json`
- Frontier negative-result claims:
  - supported by `results/experiments/order_668_64m/summary.json`
  - supported by `results/verification/benchmark_gate.md`
- One-packet freeze and locality-footprint claims:
  - supported by `results/analysis/frontier_locality_scan.json`
- H1 sensitivity claims:
  - supported by `results/branches/H1_frontier_sensitivity_probe.json`
- Harness and exactness-accounting claims:
  - supported by `hadamard_ca/harness.py`
- Internal-work counter discussion:
  - supported by `hadamard_ca/h1_ca.py`
  - supported by `results/experiments/order_668_64m/runs/H1_defect_syndrome_ca_64m.json`

The traceability weakness is presentation-level:

- the paper explicitly names `results/analysis/frontier_locality_scan.json`
- but most other load-bearing result claims are not tied in-text to the exact JSON or code artifact that supports them

Audit judgment:

- Support status: `supported, but artifact pointers should be strengthened`
- Fix: add artifact-path pointers in Methods, Results, and the appendix for the seed manifest, experiment summaries, sensitivity probe, and harness/code locations.

### 4. Two nontrivial claims need better citation or rewriting

- `research_paper.tex:123`
  - "Bent functions are directly Hadamard-adjacent through Walsh spectra"
  - `gadouleau2020` supports CA-generated bent functions and is directionally related, but it is not an ideal citation for the Walsh-spectrum bridge as phrased.
  - Fix: either add a bent-functions background source that explicitly covers the Walsh/Hadamard relationship, or rephrase the sentence more narrowly.

- `research_paper.tex:702`
  - "AI-assisted research pipelines are particularly vulnerable to novelty inflation and to confusing near-solutions with exact results."
  - This is a broad external claim with no citation.
  - Fix: either cite a relevant metascience / AI-science source or rewrite it as a repo-specific observation.

### 5. `artacho2013` is acceptable only as a distant analogy

`research_paper.tex:117` cites `artacho2013` as "a different non-CA baseline family."

- The manuscript partly protects itself by saying H1 does not resemble that line closely.
- Even so, "baseline family" is still a bit strong for a matrix-completion feasibility paper that is not a direct Hadamard-search comparator.

Audit judgment:

- Support status: `weak but usable if phrasing stays narrow`
- Fix: keep it only as an example of matrix-structured search language, not as a close baseline comparator.

## Claim Support Map

| Manuscript area | Status | Direct support | Audit note |
| --- | --- | --- | --- |
| `research_paper.tex:82`, `109`, `195`, `213` seed provenance and published coefficient profile | supported | `results/frontier/order_668_64m/seed_manifest.json`; `results/frontier/order_668_64m/source_excerpt.txt`; `eliahou2025_64mod668` | Strong chain. |
| `research_paper.tex:69-73`, `229`, `586-591`, `604-608` control executability and exactness | supported | `results/experiments/controls/summary.json`; control run JSONs; `hadamard_ca/harness.py` | Strong chain. |
| `research_paper.tex:71`, `91`, `462-471`, `567-579`, `686-688`, `706` one-packet scan, freeze, and locality-footprint claims | supported | `results/analysis/frontier_locality_scan.json` | Strong chain; already the best-cited artifact in the paper. |
| `research_paper.tex:615-646`, `706` frontier negative result and gate failure | supported | `results/experiments/order_668_64m/summary.json`; `results/verification/benchmark_gate.md` | Strong chain. |
| `research_paper.tex:650-655`, `660` H1 sensitivity claim that nearby variants stay pinned to the seed | supported for the observed numbers; partial for the diagnosis | `results/branches/H1_frontier_sensitivity_probe.json` | The numbers are direct; the structural conclusion is inference. |
| `research_paper.tex:624`, `678`, `725-731` runtime explanation via CA field work | partial | `results/experiments/order_668_64m/summary.json`; H1 run JSON; `hadamard_ca/h1_ca.py` | Slower runtime is measured. Causality is not isolated. |
| `research_paper.tex:115-127` literature positioning and novelty narrowing | partial / weak | cited literature plus author synthesis | Needs explicit synthesis labeling or tighter support. |
| `research_paper.tex:702` AI-assisted pipeline vulnerability claim | unsupported | none in manuscript | Cite or rewrite. |

## Missing Citations And Uncited Comparisons

Highest-priority manuscript fixes:

1. `research_paper.tex:115-127`
   - comparison-heavy synthesis needs either clause-level citations or softer framing

2. `research_paper.tex:123`
   - add a source for the bent-function / Walsh / Hadamard bridge if that exact phrasing stays

3. `research_paper.tex:624`
   - runtime interpretation should point to the appendix counter discussion or be rewritten as a plausible explanation

4. `research_paper.tex:702`
   - add a citation or rewrite as a repo-specific observation

Lower-priority but real:

- `research_paper.tex:84`
  - "CA are already known as generic local search or propagation mechanisms" is thinly supported by one shortest-path paper
  - either soften to "have been used" or add a broader CA-search / CA-control source if the generic claim stays

## Likely Citation Hallucinations Or Metadata Risks

No cited key in the manuscript currently looks fabricated. The actual risk is metadata quality.

### Fix now

- `tsompanas2017`
  - internal inconsistency in `sources.bib`
  - current entry mixes `journal={arXiv.org}` with Springer chapter DOI `10.1007/978-3-319-77510-4_8`
  - this should be corrected before final assembly

- `mariot2019_mols`
  - metadata is too thin for formal use
  - author list is truncated with `and others`
  - the cited journal version appears to be a `2020` article rather than `2019`
  - DOI and pages are missing

- `artacho2013`
  - usable as a citation, but the BibTeX entry is incomplete for formal use
  - volume / issue / page metadata should be filled from the journal record

### Fix before future use

- `suksmono2024`
  - not cited in `research_paper.tex`
  - this should be corrected to the `2025` `Scientific Reports` record before citation

- `bright2018`
  - likely better represented as `@inproceedings` than `@article`

- `bright2019_williamson`
  - unused in the paper
  - `journal={ACCA}` is too vague to trust without cleanup

### Keep out of the manuscript unless revalidated

- `ghaleb2019`
- `ghaemi2022`
- `leeuwen2000`

These are unused in `research_paper.tex` and should remain watchlist-only. They do not help the current paper's citation support.

## Most Important Concrete Sources To Add Or Promote

### Promote direct artifact citations first

These are the most valuable support additions because they directly anchor the paper's own quantitative claims:

1. `results/frontier/order_668_64m/seed_manifest.json`
2. `results/frontier/order_668_64m/source_excerpt.txt`
3. `results/experiments/order_668_64m/summary.json`
4. `results/experiments/controls/summary.json`
5. `results/analysis/frontier_locality_scan.json`
6. `results/branches/H1_frontier_sensitivity_probe.json`
7. `results/verification/benchmark_gate.md`
8. `hadamard_ca/harness.py`
9. `hadamard_ca/h1_ca.py`

### Correct or add external bibliography support

1. Correct `tsompanas2017` to the actual Springer chapter metadata.
   - This is the most urgent external bibliography fix because the current entry is internally inconsistent.

2. Correct `mariot2019_mols` to the full journal metadata.
   - This is the next most important fix among the sources actually cited in the paper.

3. Fill in the official metadata for `artacho2013`.
   - This is lower priority than the two entries above, but it is still a cited paper and should not go out with incomplete journal fields.

4. Add a bent-functions background source if line `123` keeps the Walsh-spectrum wording.
   - A survey or monograph that explicitly links bent functions, Walsh spectra, and Hadamard matrices is the cleanest repair.

5. Add a citation for the AI-assisted research-pipeline sentence at line `702` only if that sentence is worth keeping.
   - Otherwise rewrite it as a repo-specific observation and avoid widening the citation burden.

## Recommended Disposition

- Keep the paper's narrow quantitative contribution.
- Revise the literature-positioning paragraphs and discussion so they do not ask the citations to do more than they can support.
- Correct the bibliography metadata before treating this as submission-grade.

Current citation-support verdict for `research_paper.tex`: `REVISE`, but the problems are fixable without new experiments.
