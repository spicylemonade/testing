# Citation Audit

Date: 2026-03-13
Owner role: `citation_auditor`
Verification phase: `review_round_1`
Task: Improve the Ramsey number `R(5,5)` bound
Active hypothesis: `H1`
Active hypothesis label: `Cross-family canonical obstruction atlas for failed 42 -> 43 extensions in R(5,5)`
Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof

## Scope

Reviewed directly:

- `research_paper.tex`
- `sources.bib`
- `results/research_context.md`
- `results/research_context.json`
- `results/literature/semantic_scholar_manifest.json`
- `results/literature/literature_snapshot.json`
- `results/literature/prior_art_gap.md`
- `results/plans/claim_grammar.md`
- `results/plans/phase3_route_sheet.md`
- `results/plans/phase4_evaluation_sheet.md`
- `results/verification/claim_source_map.md`
- `results/verification/benchmark_report.md`
- `results/verification/h1_acceptance_contract.md`
- `results/verification/verification_summary.md`

External spot checks were used only to verify disputed or weak bibliography metadata:

- `gauthier2025`
- `radziszowski2024ds1`
- `narvez2024`
- `aijaam2010`

## Verdict

The manuscript is citation-safe for the main frontier baseline and for the repository-state no-go result, but it is not fully evidence-traceable yet.

The main blockers are:

1. one stale exact-measurement row in the results table;
2. one broken bibliography URL for `gauthier2025`;
3. one overbroad comparison paragraph that leans on `aijaam2010` far beyond what that weak overlap-only source can support; and
4. a mismatch between the repaired bibliography used in the paper and the older literature snapshot used for some corpus-count claims.

No clearly fabricated paper remains in the manuscript citation spine itself. The problems are weaker than the earlier packet defects, but they are still material for evidence traceability.

## Findings

### 1. `Known papers tracked = 106` is unsupported as an exact deterministic measurement.

- `research_paper.tex:556` reports `Known papers tracked & 106`.
- The current packet records `111` at `results/research_context.md:9`, `results/research_context.json:42`, and `results/literature/semantic_scholar_manifest.json:556`.
- The results table is introduced at `research_paper.tex:549` as exact deterministic measurements extracted from the repository, so this is a real support failure rather than a wording nit.

Status: unsupported exact claim.

### 2. `gauthier2025` has broken metadata, and the manuscript still uses it slightly too strongly.

- `sources.bib:120-125` stores `gauthier2025` as `A Strategy for Lowering the Upper Bound of R(5,5)`, which is the right qualitative object, but the URL points to `AITP_2025_paper_7.pdf`.
- External verification shows the actual Gauthier abstract is paper `3`, not paper `7`; the stored URL now resolves to an unrelated abstract.
- In the manuscript, `research_paper.tex:132` and `research_paper.tex:153` use `gauthier2025` as evidence that split-vertex / transverse-edge gluing is the live continuation surface for `H2`.
- The local packet itself already downgrades this item to overlap-only status at `sources.bib:125` and `results/verification/claim_source_map.md:33`.

Status: broken citation metadata plus mildly overstated weight.

### 3. The broad rejection paragraph at `research_paper.tex:138` is under-cited and contains uncited comparison families.

- `research_paper.tex:138` rejects generic GA or symmetry stories, generic rare-event narratives, solver-shopping, and pure proof export, but cites only `aijaam2010`.
- `sources.bib:21-26` already labels `aijaam2010` as an overlap-only citation and explicitly warns not to treat it as a comparison-grade source.
- The broader comparison families appear only as prose in `results/literature/prior_art_gap.md:38-55` and `results/swarm/falsifier.md:23-24`, `results/swarm/falsifier.md:51-53`, `results/swarm/falsifier.md:118-122`, without a matching manuscript citation cluster.

Status: weak citation plus uncited comparisons.

### 4. The fixed-corpus sentence omits the dynamic survey even though it names that source explicitly.

- `research_paper.tex:257` says the fixed Ramsey-specific corpus includes the dynamic survey for the current frontier.
- The citation cluster on that sentence omits `radziszowski2024ds1`, even though the bibliography row exists at `sources.bib:138-143`.
- Because this sentence defines the manuscript's corpus boundary, the omission is more important than a routine missing citation.

Status: missing citation.

### 5. Present-tense frontier-status claims in Related Work should cite a current frontier source, not only milestone papers.

- `research_paper.tex:126` says Exoo's line "remains the best published lower-bound witness family".
- `research_paper.tex:132` says Angeltveit--McKay 2024 reaches the "current best published upper bound".
- Those are present-tense status claims as of 2026-03-13, but they cite only the milestone papers themselves.
- The manuscript already uses the stronger current-frontier spine at `research_paper.tex:77` and `research_paper.tex:178`, where `radziszowski2024ds1` is included.

Status: weak current-state anchoring.

### 6. The corpus count and the corpus definition do not resolve to one auditable source of truth.

- `research_paper.tex:257` defines the fixed corpus in prose using the repaired bibliography.
- `research_paper.tex:557` reports `Curated Ramsey-specific papers & 13`.
- The `13` count is consistent with the `papers` array in `results/literature/literature_snapshot.json:607`, but that same snapshot still contains stale or unreconciled rows at `results/literature/literature_snapshot.json:749-767` (`Decreasing the upper bound on the Ramsey number R(5,5)` with the stale ACM DOI story) and `results/literature/literature_snapshot.json:863-883` (`Formalizing Ramsey Theory in Lean: Towards the proof that Ramsey(4,5)=25`).
- The paper itself no longer cites those stale entries directly, which is good, but the exact count still appears to be inherited from that older snapshot rather than from the repaired writer-stage bibliography.

Status: evidence-traceability mismatch.

### 7. The `Survey sources` interpretation overclaims what the local evidence supports.

- `research_paper.tex:559` says the two survey sources support the frontier framing.
- The two survey rows are `results/literature/literature_snapshot.json:926-944`, namely Radziszowski's dynamic survey and Noga Alon's broad extremal-combinatorics survey.
- The packet already marks `noga2022` as background-only at `results/verification/claim_source_map.md:35-36`.

Status: interpretation overclaim.

### 8. Several bibliography entries are real but still weaker than they should be.

- `sources.bib:128-135` (`narvez2024`) uses a Semantic Scholar mirror instead of the official Springer chapter landing page.
- `sources.bib:138-143` (`radziszowski2024ds1`) does not record the survey DOI or exact revision/date, even though the paper uses it for current-state frontier claims.
- `sources.bib:29-35`, `sources.bib:38-44`, and `sources.bib:1-7` could all be strengthened with fuller journal metadata.
- `sources.bib:175-180` (`lehavirepo`) is acceptable as an artifact citation but would be stronger with a tag, commit, or release anchor.

Status: metadata weakness, not hallucination.

### 9. `results/research_context.md` still presents lexical false positives as `Closest Prior Art`.

- `results/research_context.md:14-18` still lists biomedical and robotics false positives as the closest prior art.
- This is not a direct manuscript citation defect, since the paper itself avoids them.
- It is still a downstream traceability risk for any later synthesis pass that reuses the context file.

Status: residual pipeline context risk.

## Key Claim Coverage

| Key claim | Current support | Status | Notes |
| --- | --- | --- | --- |
| `43 <= R(5,5) <= 46` is the active frontier. | `research_paper.tex:77`, `research_paper.tex:178`; `exoo1989`, `ge2022`, `angeltveitmckay2024`, `radziszowski2024ds1` | supported | This is the cleanest citation spine in the paper. |
| The manuscript is a no-go / infrastructure-only checkpoint rather than a bound-improvement paper. | `research_paper.tex:454-483`; `results/verification/benchmark_report.md:28-45`; `results/verification/h1_acceptance_contract.md:27-35` | supported | Internal evidence traceability is good enough here. |
| `H1` remains the only live route, while `H2` and `H3` are demoted. | `research_paper.tex:572-595`; `results/concept_evolve/bridge_candidates.json`; `results/decision_log.md` | supported | Internal claim; not primarily a literature citation issue. |
| The lower-bound / OVE / formal-proof framing in Related Work is basically sound. | `research_paper.tex:126-135`; `exoo1989`, `ge2022`, `lehavi2024`, `gauthier2024`, `gauthierbrown2024arxiv`, `narvez2024`, `heule2018schur`, `li2025ramseycert` | mostly supported | The Gauthier strategy note and the overbroad `aijaam2010` paragraph are the main exceptions. |
| The measurement table is entirely exact and repository-derived. | `research_paper.tex:549-567` plus local packet files | mixed | Most rows check out; `Known papers tracked = 106` does not. |

## Most Important Concrete Sources Or Repairs To Add

### Repair immediately

1. Fix `gauthier2025` to the official AITP 2025 abstract PDF for paper `3`, not paper `7`.
2. Add `radziszowski2024ds1` survey DOI (`10.37236/21`) plus the exact revision/date used for the frontier claim.
3. Replace the `narvez2024` Semantic Scholar mirror URL with the official Springer chapter metadata.

### Add if the current broad comparison prose stays

1. Add a direct rare-event / RL-style Ramsey-search source if `research_paper.tex:138` continues to reject those narratives explicitly.
   A strong candidate identified during spot checks was `RamseyRL: A Framework for Intelligent Ramsey Number Counterexample Searching`.
2. Add a direct analog lower-bound search source if the packet keeps referring to analog Max-SAT overlap.
   A concrete candidate identified during spot checks was `A high-performance analog Max-SAT solver and its application to Ramsey numbers`.
3. Add a direct semidefinite-Ramsey source if the packet continues to use "prior SDP/flag-algebra applications to Ramsey numbers" as a comparison family in reviewer-facing documents.
   A concrete candidate identified during spot checks was `Semidefinite Programming and Ramsey Numbers`.

### Metadata upgrades with high return

1. Fill volume/issue/pages for `exoo1989`, `mckay1992`, and `angeltveit2018`.
2. Add a stable release or commit anchor for `lehavirepo` if the repository citation remains in the manuscript.

## Bottom Line

The manuscript's main scientific ceiling is citation-safe:

- the frontier claim is well supported;
- the no-go result is adequately supported by internal packet evidence; and
- the repaired formal-proof paragraph is substantially stronger than the earlier packet.

The remaining citation work is targeted, not global:

1. fix the bad `gauthier2025` URL and keep that source explicitly strategy-only;
2. repair the stale `106` exact-count row;
3. either narrow or properly source the overbroad comparison paragraph at `research_paper.tex:138`; and
4. align the corpus-count story with one authoritative source instead of mixing repaired bibliography rows with a stale literature snapshot.
