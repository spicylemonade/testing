# Citation Audit

Snapshot date: 2026-03-19 UTC
Verification phase: `post_deepen`

## Scope

- Primary files audited:
  - `research_paper.tex`
  - `sources.bib`
  - `results/research_context.md`
  - `results/literature/semantic_scholar_manifest.json`
- Support tracing also checked against:
  - `results/research_context.json`
  - `results/theory/forcing_trace_normal_form.md`
  - `results/theory/local_rule_no_go_atlas.md`
  - `results/theory/forcing_traces/tiny_2x2_full_seeds_le3/corpus_summary.json`
  - `results/experiments/h1_exact_advantage.md`
  - `results/concept_evolve/bridge_candidates.json`
  - `results/literature/prior_art_gap.md`
- External spot-checks were limited to recent higher-risk entries and the leftover `leng2024` line. No blocker-level existence problem was found in the manuscript's cited 2024-2025 papers.

## Verdict

- `Pass` for the manuscript's core theorem/results support.
- `Revise` for literature framing and repo-level provenance hygiene.

Current status is materially better than the earlier audit trail:

- the manuscript now cites `archivara2026task` for the prompt-derived target and witness language in the body (`research_paper.tex:142`, `research_paper.tex:305`, `research_paper.tex:367`);
- the current manuscript does **not** cite `leng2024`;
- the key exact-result claims are traceable to machine-readable repo artifacts.

The remaining citation problems are narrower:

1. several Related Work comparisons are still stronger than the cited papers warrant;
2. one introduction sentence overuses `wang2025`;
3. the abstract and early summary sections still make high-load repo-result claims without direct provenance pointers;
4. upstream provenance files remain stale and still carry the old `leng2024` misfit.

## Claims With Strong Support

- Prompt-derived target and notation are now wired to explicit provenance in the manuscript body:
  - `research_paper.tex:140-142`
  - `research_paper.tex:302-305`
  - `research_paper.tex:364-367`
  - `sources.bib:153-158`
  - `results/research_context.json:5`

- The exact-verifier and finite-audit claims are strongly supported by repo artifacts:
  - `research_paper.tex:154-162`
  - `research_paper.tex:172-182`
  - `research_paper.tex:101-121`
  - `results/theory/forcing_trace_normal_form.md:41-57`
  - `results/theory/local_rule_no_go_atlas.md:23-38`
  - `results/theory/forcing_traces/tiny_2x2_full_seeds_le3/corpus_summary.json`

- The larger-search negative frontier is traceable to stored experiment summaries:
  - `research_paper.tex:1125-1169`
  - `results/experiments/h1_exact_advantage.md:17-27`

- The bridge-status paragraph is currently supported by the chosen source of truth:
  - `research_paper.tex:1173-1188`
  - `research_paper.tex:959-960`
  - `results/concept_evolve/bridge_candidates.json:1-45`

- All in-paper citation keys resolve in `sources.bib`. The only high-risk bibliography entry left outside the paper is `leng2024` (`sources.bib:126-133`).

## Findings

### 1. Related Work still contains weak or over-interpreted citations

- `research_paper.tex:219-227` uses real and relevant papers, but several claims go beyond what those citations directly establish.
- Weak spots:
  - `research_paper.tex:220-223`: Cowen-Breen et al. are used to motivate "proxy optimization" drift. `sources.bib:22-30` supports adjacency, but not that exact warning as written.
  - `research_paper.tex:224-227`: Tao is turned into a direct warning about "small fixed alphabets," and Hickman-Wright is called the "natural modular comparison class." `sources.bib:42-58` supports relevance, but the prose is more interpretive than evidentiary.
  - `research_paper.tex:259-267`: AlphaEvolve and Georgiev et al. are used to set a "novelty floor" and the "correct comparison class" for automation. `sources.bib:99-115` shows these systems exist and are relevant, but does not itself prove that stronger normative framing.

Audit judgment:

- Mostly weak citations, not hallucinations.

Required fix:

- Soften these sentences to authorial framing, e.g. "we treat X as the closest comparison class" or "we use Y as a cautionary adjacent regime."
- If stronger wording is important, anchor it to a specific theorem, result, or section of the cited paper rather than to a title-level summary.

### 2. One introduction sentence is broader than the single Wang-Zahl source

- Claim location:
  - `research_paper.tex:136-139`
- Problem:
  - `wang2025` cleanly supports recent three-dimensional Kakeya progress (`sources.bib:145-150`), but the sentence also uses it to support the broader statement that "the broader Kakeya program remains active."

Audit judgment:

- Adequate for the 3D-progress clause, weak for the broader field-status clause.

Suggested fix:

- Either narrow the sentence to the specific 3D result already cited, or add another recent Kakeya-specific survey/result if the broader field-status sentence is meant to stay.

### 3. The abstract and early summary sections still under-cite repo evidence

- Claim cluster:
  - `research_paper.tex:80-86`
  - `research_paper.tex:94-121`
  - `research_paper.tex:154-182`
- Problem:
  - These sections now make accurate claims, and the support exists later in the paper and in repo artifacts, but the reader sees the highest-load counts and status updates before seeing explicit provenance.

Audit judgment:

- Supported, but thinly wired.

Suggested fix:

- Add one short provenance footnote or parenthetical reference in the title-page note, abstract, or first introduction page pointing to:
  - `results/research_context.json` for the prompt target;
  - `results/theory/forcing_traces/tiny_2x2_full_seeds_le3/corpus_summary.json` for the `44,608 / 48 / 7/4 / 1+3` claim cluster;
  - `results/theory/forcing_traces/index.json` or `results/theory/local_rule_no_go_atlas.md` for the `256 / 8,192 / 0` one-sided atlas claims;
  - `results/experiments/h1_exact_advantage.md` for the larger-family negative frontier.

### 4. `leng2024` is no longer a manuscript blocker, but it remains stale citation debt upstream

- Current good news:
  - the manuscript no longer cites `leng2024`.
- Remaining repo-level problem:
  - `sources.bib:126-133` still contains `Improved Bounds for Szemeredi's Theorem`;
  - `results/research_context.json:5` still embeds the old prompt text that links a Hausdorff-dimension upgrade to Leng-Sah-Sawhney;
  - `results/research_context.md:33-37` and `results/literature/semantic_scholar_manifest.json:725-742` show repeated Szemeredi searches and a failed `Leng Sah Sawhney Kakeya` search.

Audit judgment:

- Real paper, wrong role.
- This is no longer an in-paper citation hallucination, but it is still a provenance hazard because it can easily be recycled back into later drafts.

Required fix:

- Remove or quarantine `leng2024` from `sources.bib` unless a future draft actually needs it.
- If it is kept for provenance reasons, mark it explicitly as an unused stale upstream lead rather than scientific support.
- Clean the corresponding line out of `results/research_context.json` or annotate it as legacy prompt text rather than validated mathematical background.

### 5. Research-context provenance is stale and audit-thin

- Stale counts:
  - `results/research_context.md:9-10` says `106` tracked papers and `14` bibliography entries;
  - `results/literature/semantic_scholar_manifest.json:921-926` says `114` unique papers;
  - `sources.bib` now has `17` entries.
- Malformed prior-art lane:
  - `results/research_context.md:14-30` still lists obviously irrelevant "Closest Prior Art" titles generated from token collisions.
- Thin manifest:
  - `results/literature/semantic_scholar_manifest.json:1-3`, `results/literature/semantic_scholar_manifest.json:805-926` preserves query history and paper IDs, but not a query-to-selection explanation that would let a later auditor reconstruct why specific papers entered `sources.bib`.

Audit judgment:

- Not a blocker for the manuscript's current citations, but a real evidence-traceability weakness for the repo.

Suggested fix:

- Refresh the context summary counts.
- Replace the malformed "Closest Prior Art" block with the curated boundary already written in `results/literature/prior_art_gap.md`.
- If the manifest is meant to support future audits, add a compact per-paper selection record rather than only a query log and `seen_paper_ids`.

### 6. Low-severity uncited background remains in the first introduction paragraph

- Claim location:
  - `research_paper.tex:132-134`
- Problem:
  - These are standard Kakeya facts, so this is low severity, but they are still external mathematical background with no direct citation.

Suggested fix:

- Add `katz1999` or `bourgain1999` earlier in the paragraph if the draft is aiming for maximal citation tightness.

## Likely Citation Hallucinations

- None found in the current manuscript's cited keys.
- The higher-risk recent entries that matter for the paper's external framing appear real and broadly fit their stated roles:
  - `pohoata2024`
  - `tao2025`
  - `novikov2025`
  - `georgiev2025`
  - `wang2025`
- The remaining integrity problem is source fit and provenance hygiene, not fabricated references.

## Most Important Sources To Add Or Wire In

1. Wire `archivara2026task` into the abstract or first introduction page, not only the later background section.
   - Best existing source: `sources.bib:153-158` backed by `results/research_context.json:5`.

2. If the broad "Kakeya program remains active" sentence stays, either narrow it to the specific Wang-Zahl result already cited or add another recent Kakeya-specific source.
   - Best current source already in hand: `sources.bib:145-150`.

3. If the stronger Related Work comparisons remain, add section- or theorem-level anchors for the specific claims currently attached to:
   - `sources.bib:22-30`
   - `sources.bib:42-58`
   - `sources.bib:99-115`

4. Remove or explicitly quarantine `leng2024` and the corresponding upstream prompt sentence.
   - High-risk locations:
     - `sources.bib:126-133`
     - `results/research_context.json:5`
     - `results/research_context.md:33-37`

5. Replace the malformed context-level prior-art block with the curated literature boundary already present in:
   - `results/literature/prior_art_gap.md`

## Bottom Line

- The manuscript's core exact claims are now well supported.
- The biggest citation problem from the earlier round, the in-paper `leng2024` misfit, has already been removed from the manuscript.
- The remaining work is mostly cleanup:
  - soften over-strong comparative framing,
  - add one early provenance pointer for the abstract-level repo claims,
  - and clean the stale upstream provenance files so the old `leng2024` error does not re-enter a future draft.
