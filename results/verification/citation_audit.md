# Citation Audit

Date: 2026-03-13
Owner role: `citation_auditor`
Verification phase: `post_researcher`
Task: Improve the Ramsey number `R(5,5)` bound
Active hypothesis: `H1`
Active hypothesis label: `Cross-family canonical obstruction atlas for failed 42 -> 43 extensions in R(5,5)`
Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof

## Scope

- `research_paper.tex` is not present in this workspace, so this is a packet-level audit rather than a paragraph-level manuscript audit.
- Reviewed local artifacts:
  - `sources.bib`
  - `results/research_context.md`
  - `results/literature/semantic_scholar_manifest.json`
  - `results/literature/literature_snapshot.json`
  - `results/literature/prior_art_gap.md`
  - `results/plans/claim_grammar.md`
  - `results/plans/phase2_baseline_sheet.md`
  - `results/plans/phase3_route_sheet.md`
  - `results/plans/phase4_evaluation_sheet.md`
  - `results/plans/ramsey_research_program.md`
  - `results/swarm/falsifier.md`
  - `results/swarm/hypotheses.json`
  - `results/verification/claim_source_map.md`
  - `results/verification/verification_summary.md`
  - `results/verification/novelty_report.md`
  - `results/verification/final_review.md`

## Audit Verdict

The packet is citation-safe enough for the constrained `H1` no-go memo, but it is not fully citation-safe for the broader comparison framing now embedded in the route and falsifier documents.

The good news:

- The load-bearing frontier claim `43 <= R(5,5) <= 46` is adequately anchored by `exoo1989`, `ge2022`, `angeltveitmckay2024`, and `radziszowski2024ds1`; see `results/verification/claim_source_map.md:13` and `results/literature/literature_snapshot.json:567-583`.
- The core `H1` overlap framing against Ge 2022 and Lehavi 2024 is adequately grounded for route triage; see `results/verification/claim_source_map.md:14-15`, `results/plans/phase3_route_sheet.md:45-47`, and `sources.bib:10-19,47-57`.
- The current `No-go` verdict on any bound-improvement claim is adequately supported at the packet level; see `results/verification/claim_source_map.md:19-20`, `results/plans/claim_grammar.md:10-42`, and `results/verification/verification_summary.md`.

The remaining problems are narrower but important:

- one likely corrupted `H2` citation row,
- one likely corrupted `H3` citation row,
- several uncited comparison families that appear in novelty and benchmark framing,
- and a few weak discovery-only rows that are still being given more argumentative weight than they should carry.

## Findings

### 1. `gauthier2025` is not audit-safe and is the most serious live citation problem.

- `sources.bib:120-128` claims that `gauthier2025` is `Decreasing the upper bound on the Ramsey number R(5,5)` with DOI `10.1145/3727993.3728010`.
- Direct DOI verification during this audit showed that `10.1145/3727993.3728010` resolves to an unrelated smart-city bibliometrics paper, not to a Ramsey paper.
- A targeted official search did recover a real AITP 2025 abstract by Thibault Gauthier, but under the title `A Strategy for Lowering the Upper Bound of R(5,5)`, not the title or DOI currently stored in `sources.bib`.
- This matters because the corrupted row is load-bearing in the current packet:
  - `results/verification/claim_source_map.md:17`
  - `results/plans/phase4_evaluation_sheet.md:64`
  - `results/verification/novelty_report.md:26`
  - `results/literature/literature_snapshot.json:582,748-767`

Audit status: likely citation hallucination or metadata conflation. Until this row is repaired, `H2` cannot be presented as having a verified comparison-grade `Gauthier 2025` baseline. At most, it has an overlap note pointing to an AITP 2025 abstract.

### 2. `barakeel2025` is also not audit-safe and likely conflates a nonexistent paper with the general Lean/Ramsey line.

- `sources.bib:130-136` claims a paper titled `Formalizing Ramsey Theory in Lean: Towards the proof that Ramsey(4,5)=25` with DOI `10.1007/978-3-031-66998-9_13`.
- DOI resolution during this audit returned `DOI Not Found`.
- Exact-title searches did not recover the claimed paper. The recoverable Lean/Ramsey literature found during this audit instead points to a different formalization paper, `Formalizing Finite Ramsey Theory in Lean 4`.
- This matters because `results/verification/claim_source_map.md:18` uses `barakeel2025` as one of the explicit bibliography anchors for the `H3` infrastructure rule.

Audit status: likely citation hallucination or at minimum badly corrupted metadata. `H3` still has partial support from `gauthier2024`, `gauthierbrown2024arxiv`, and `barakeelramseyrepo`, but the current packet overstates the solidity of its Lean-formalization bibliography.

### 3. Several comparison claims remain uncited even though the packet treats them as named benchmark or novelty baselines.

The biggest missing bibliography families are:

- `Schur Number Five` proof-logging and certificate practice
  - used in `results/swarm/falsifier.md:107,120`
  - used in `results/swarm/hypotheses.json:37-40`
  - implicitly required by `results/plans/ramsey_research_program.md:231-233`
- `SAT+CAS verified Ramsey certificates for nearby exact problems`
  - used in `results/swarm/falsifier.md:107,121`
  - used in `results/swarm/hypotheses.json:39`
- `prior SDP/flag-algebra applications to Ramsey numbers`
  - used in `results/literature/prior_art_gap.md:45-49`
- `statistical-physics framing of Ramsey lower bounds`, `RL-style Ramsey search`, and `analog Max-SAT work`
  - used in `results/literature/prior_art_gap.md:40-43`
  - used in `results/swarm/falsifier.md:23`

None of those comparison families currently has a corresponding `sources.bib` row. That is a direct violation of the writer constraint in `results/verification/claim_source_map.md:40` and the minimum-anchor rule in `results/plans/claim_grammar.md:49-57` whenever these comparisons are treated as reviewer-facing evidence rather than internal brainstorming.

Audit status: missing citations / uncited comparisons.

### 4. `aijaam2010` is real enough to keep, but it is still packaged too weakly for the role it is currently assigned.

- `sources.bib:21-27` stores `aijaam2010` as an overlap-only `@misc` entry with a QSpace handle and a warning note.
- The packet still elevates it to a required comparison row in:
  - `results/plans/phase4_evaluation_sheet.md:60`
  - `results/plans/ramsey_research_program.md:225`
- Exact-title search during this audit recovered the QSpace record and confirmed that it is at least a 2010 IEEE conference item, so the row is not a hallucination.

Audit status: weak citation, not a false citation. Keep it overlap-only, enrich the metadata if retained, and do not use it as a comparison-grade baseline row next to Exoo, Ge, Lehavi, or Angeltveit-McKay.

### 5. `mckay1992` and `noga2022` remain weak/discovery-only, but they are not the main citation risk right now.

- `mckay1992` at `sources.bib:29-36` still points to a Semantic Scholar mirror instead of a journal-hosted or society-hosted landing page.
- `noga2022` at `sources.bib:79-85` is still a discovery-link survey entry and should remain background-only.
- `results/verification/claim_source_map.md:33-35` already recognizes both limits correctly.

Audit status: weak but mostly contained, provided neither row is allowed to become load-bearing in a final memo.

### 6. `results/research_context.md` still exposes lexical false positives as `Closest Prior Art`.

- `results/research_context.md:14-18` lists biomedical and robotics papers as `Closest Prior Art`.
- Those rows are already recognized elsewhere in the packet as lexical false positives rather than genuine Ramsey overlap; see `results/literature/prior_art_gap.md:57-104` and `results/literature/prior_art_watchlist.md`.
- Leaving them in the top-level context file is citation-unsafe because downstream synthesis can easily mistake that section for the actual prior-art shortlist.

Audit status: misleading citation context. This does not break the constrained `H1` no-go memo by itself, but it should not survive into any final packet or writer-facing context summary.

## Key Claim Coverage Check

| Key packet claim | Current support | Status | Notes |
| --- | --- | --- | --- |
| `43 <= R(5,5) <= 46` is the working frontier. | `exoo1989`, `ge2022`, `angeltveitmckay2024`, `radziszowski2024ds1` | supported | Safe to keep as a top-line packet claim. |
| `H1` should be framed as an obstruction-atlas route, not as a new OVE algorithm. | `ge2022`, `lehavi2024`, `lehavirepo` plus local route docs | supported | Safe for route framing; still a route target, not an achieved result. |
| Only an independently verified `44`-vertex witness or a checked `45`-vertex impossibility proof counts as a bound improvement. | local claim grammar plus frontier literature anchors | supported | Internal governance claim, appropriately tied to frontier literature. |
| `H2` must be compared against the split-vertex / transverse-edge gluing line, especially Gauthier 2025. | `mckay1992`, `angeltveit2018`, `angeltveitmckay2024`, corrupted `gauthier2025` row | weak | Comparison intent is valid, but the named `gauthier2025` anchor is not stable enough. |
| `H3` sits against formal Ramsey proof / Lean formalization baselines. | `gauthier2024`, `gauthierbrown2024arxiv`, corrupted `barakeel2025`, `barakeelramseyrepo` | weak | Needs one verified Lean-formalization paper and one verified proof-logging/certificate baseline. |
| The current run is `No-go` on bound movement and on any achieved `H1` structural-result claim. | local verification artifacts plus frontier anchors | supported | Safe for the constrained memo. |

## Highest-Value Concrete Sources To Add

1. Add `Schur Number Five` as an explicit bibliography row.
   - This is the missing anchor for the `H3` benchmark ladder and proof-logging comparisons now present in `results/swarm/falsifier.md` and `results/swarm/hypotheses.json`.

2. Add `Efficient Certified SAT+CAS Bounds for Ramsey Numbers via Fine-Grained Proof Logging` as an explicit bibliography row.
   - This is the cleanest nearby exact-certification anchor for the packet's `SAT+CAS verified Ramsey certificates` language.

3. Replace `gauthier2025` with the verified official item actually recovered during this audit.
   - If the packet wants the AITP 2025 overlap note, use `A Strategy for Lowering the Upper Bound of R(5,5)` and treat it as an overlap/strategy source until a stable proceedings record exists.
   - Do not keep DOI `10.1145/3727993.3728010` on any Ramsey row.

4. Replace or remove `barakeel2025`.
   - If the packet wants a Lean/Ramsey formalization anchor, cite a verified formalization paper rather than the current unrecoverable row.
   - The closest verified replacement found during this audit was `Formalizing Finite Ramsey Theory in Lean 4`, though that paper is not by the authors currently listed in `sources.bib`.

5. Upgrade `aijaam2010` metadata if the row stays.
   - Use the QSpace conference metadata and full author name, but continue labeling it as overlap-only rather than comparison-grade.

## Required Repair Actions Before Any Stronger Memo

1. Repair `sources.bib` by removing or replacing the corrupted `gauthier2025` and `barakeel2025` rows.
2. Add explicit bibliography rows for `Schur Number Five` and for the `SAT+CAS verified Ramsey certificates` line if those comparisons remain in any reviewer-facing document.
3. Downgrade or source the generic comparison language in `results/literature/prior_art_gap.md` and `results/swarm/falsifier.md` where it currently names literature families without bibliography anchors.
4. Remove or relabel the lexical-noise `Closest Prior Art` block in `results/research_context.md:14-18`.
5. Update `results/verification/claim_source_map.md:17-18` after the bibliography repair so the `H2` and `H3` rows no longer depend on corrupted anchors.

## Bottom Line

For the current constrained `H1` no-go memo, the citation spine is adequate.

For any stronger memo that leans on `H2` or `H3` comparison framing, the packet is not yet citation-safe. The blocker is no longer the Exoo/Ge/Lehavi frontier spine; it is the combination of one corrupted `H2` row, one corrupted `H3` row, and several uncited comparison families that still appear in reviewer-facing reasoning.

## Writer-Stage Repair Addendum (2026-03-13)

- `mckay1992` now uses the official Australasian Journal of Combinatorics PDF rather than a discovery mirror.
- `gauthier2025` has been downgraded to an overlap-only AITP 2025 abstract with an official conference PDF and no bogus DOI.
- `barakeel2025` has been explicitly demoted to a non-load-bearing placeholder.
- Added `narvez2024` (`Formalizing Finite Ramsey Theory in Lean 4`) as a verified Lean-formalization anchor for reviewer-facing `H3` context.
- `results/verification/claim_source_map.md` no longer uses `gauthier2025` or `barakeel2025` as load-bearing bibliography anchors.


## Writer Repair Addendum

Date: 2026-03-13
Owner role: `writer`

The following writer-side citation and context repairs were applied after the audit above so the constrained manuscript no longer depends on the stale packet defects listed in Findings 1, 2, and 6.

- `sources.bib` now treats `gauthier2025` as the verified AITP 2025 strategy abstract `A Strategy for Lowering the Upper Bound of R(5,5)` rather than as a corrupted proceedings or DOI row.
- The unrecoverable `barakeel2025` placeholder was removed from the active citation spine and replaced, for reviewer-facing H3 context, by the verified Lean 4 formalization source `narvez2024` (`Formalizing Finite Ramsey Theory in Lean 4`).
- `sources.bib` now includes `heule2018schur` and `li2025ramseycert`, which cover the `Schur Number Five` and certified `SAT+CAS` comparison families named elsewhere in the packet.
- `results/verification/claim_source_map.md` now routes H3 comparison language through `narvez2024`, `heule2018schur`, and `li2025ramseycert` instead of the earlier corrupted placeholder row.
- `results/research_context.md` was relabeled so the top-level prior-art section now lists the closest Ramsey-specific overlap and relegates the biomedical and robotics items to an explicitly excluded lexical-watchlist block.

These repairs do not change the scientific verdict. The packet remains benchmark-empty and cannot support any bound-improvement claim or achieved H1 structural-result claim. They do, however, remove the writer-facing citation and context defects that would otherwise have carried into the constrained no-go manuscript.
