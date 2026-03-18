# Citation Audit

## Scope

`research_paper.tex` is not present in the repo, so this audit targets the current writeup-facing artifacts instead:

- `results/writeup/methods_brief.md`
- `results/writeup/claims_table.md`
- `results/writeup/repro.md`
- `results/verification/verification_summary.md`
- `results/verification/benchmark_report.md`
- `results/verification/novelty_report.md`
- `results/verification/runtime_audit.md`
- `results/analysis/prior_work_comparison.md`
- `results/frontier/order_668_64m/seed_manifest.json`
- `results/frontier/order_668_64m/source_excerpt.txt`
- `results/experiments/order_668_64m/summary.json`
- `results/experiments/controls/summary.json`
- `results/experiments/order_668_64m/runs/*.json`
- `results/experiments/order_668_64m/configs/*.json`
- `hadamard_ca/harness.py`
- `sources.bib`
- `results/research_context.md`
- `results/literature/semantic_scholar_manifest.json`

This phase checks evidence traceability and citation support only.

## Executive Summary

- The strongest claims are well supported by direct internal artifacts: seed provenance, shared-harness accounting, the negative frontier result, the absence of an exact order-668 hit, and runtime-package completeness.
- The weakest claims are the literature-facing interpretation claims: the narrow novelty framing, the "not competitive with broader literature" framing, the `pivot to H2` mechanism rationale, and the causal explanation for the H1 runtime cost.
- The main traceability problem is not total absence of evidence; it is over-reliance on derivative summaries. The current writeup repeatedly cites `results/verification/benchmark_report.md`, `results/verification/novelty_report.md`, and this audit file itself where direct artifacts are available.
- No load-bearing paper key looks fabricated, but several BibTeX entries carry citation-hallucination risk through mixed or weak metadata: `tsompanas2017`, `ghaleb2019`, and `leeuwen2000`. `suksmono2024` should also be corrected before use.

## Claim Support Map

| Claim(s) | Status | Best direct support | Audit note |
| --- | --- | --- | --- |
| `C1`, `C11` | supported | `results/frontier/order_668_64m/seed_manifest.json`; `results/frontier/order_668_64m/source_excerpt.txt`; `results/experiments/order_668_64m/summary.json`; `eliahou2025_64mod668` | Strong seed-provenance chain. Prefer the seed manifest and source excerpt over derivative report citations. |
| `C2` | supported | `results/experiments/controls/summary.json`; control run files under `results/experiments/controls/runs/` | Strongly supported. The control exact-hit readout is directly visible in saved outputs. |
| `C3`, `C4`, `C5`, `C10`, `C12` | supported | `results/experiments/order_668_64m/summary.json`; frontier run files under `results/experiments/order_668_64m/runs/`; `results/verification/benchmark_gate.md`; `hadamard_ca/harness.py`; configs under `results/experiments/order_668_64m/configs/` | Strong internal support. The current writeup should point to `summary.json` and the harness/config files more often than to `benchmark_report.md`. |
| `C8` | supported | `results/verification/runtime_inventory.json`; run files in both experiment batches; `results/verification/runtime_audit.md` | Strongly supported. `runtime_audit.md` is acceptable as a summary, but the raw run files and inventory remain the primary evidence. |
| `C6` | partial / weak | `results/literature/prior_art_gap.md`; `results/verification/novelty_citation_note.md`; `tsompanas2017`; `eliahou2025_64mod668` | The safe narrow claim is defensible, but the current evidence chain is partly circular because the writeup cites `results/verification/citation_audit.md` as support. `tsompanas2017` supports only the generic point that CA-for-search prior art exists; it does not by itself close the question of Hadamard-specific CA novelty. |
| `C7` | partial / weak | `results/verification/benchmark_gate.md`; `results/experiments/order_668_64m/summary.json`; `suksmono2018`; `suksmono2019`; `bright2019` | "Fair enough for branch elimination" is supported internally. The broader comparison to Hadamard-search literature is under-cited and should be widened if retained. |
| `C9` | partial / weak | `results/verification/verification_summary.md`; `results/branches/H2_gate.md`; `results/concept_evolve/probe_result.json` | The branch decision is documented. The stronger mechanism statement about `locality / actuator-basis mismatch` is still an inference, not a separately established result. |
| `C13` | mixed | `results/experiments/order_668_64m/summary.json`; `results/experiments/order_668_64m/runs/H1_defect_syndrome_ca_64m.json` | The numeric part (`32` evaluations, `2.129s`) is direct. The explanation "this reflects CA field-evaluation cost" is plausible but not directly measured. Mark it as interpretation or add profiling evidence. |

## Missing Citations, Weak Citations, And Uncited Comparisons

### 1. Circular or derivative evidence chains

- `results/writeup/claims_table.md` uses `results/verification/citation_audit.md` as evidence for `C1`, `C6`, and `C7`.
- `results/writeup/methods_brief.md` also cites `results/verification/citation_audit.md` for the novelty and literature-scope claims.
- That is weak traceability. A citation audit is a synthesis artifact, not a primary source. Replace those links with direct paper keys and direct repo artifacts.

### 2. Derivative summaries are carrying too much weight

- `results/verification/benchmark_report.md` and `results/verification/novelty_report.md` are useful summaries, but many load-bearing claims can point directly to:
  - `results/frontier/order_668_64m/seed_manifest.json`
  - `results/frontier/order_668_64m/source_excerpt.txt`
  - `results/experiments/order_668_64m/summary.json`
  - `results/experiments/controls/summary.json`
  - `results/experiments/order_668_64m/configs/*.json`
  - `hadamard_ca/harness.py`
- For the current paper, those direct artifacts should be first-line evidence and the reports should be secondary support.

### 3. Comparison language that is really inference

- `results/verification/benchmark_report.md`
  - "Relative to `tsompanas2017`, the answer in this batch is no."
  - This is not something `tsompanas2017` itself supports. It is an internal inference from the saved run outcomes plus a generic CA prior-art anchor.
- `results/analysis/prior_work_comparison.md`
  - Claims such as "much weaker on certification," "seed dependence is stronger," and "closer to CA-flavored local repair" are reasonable, but they are comparative interpretations, not direct quotations or direct paper-supported facts.
- `results/verification/verification_summary.md` and `results/writeup/methods_brief.md`
  - The `pivot to H2` rationale invokes `locality / actuator-basis mismatch`. That is a repo-level interpretation and should be labeled as such unless stronger evidence is added.

### 4. Weak watchlist citations should not carry substantive claims

- `ghaleb2019`, `ghaemi2022`, and `leeuwen2000` are all treated elsewhere in the repo as watchlist or false-positive comparators.
- That is the correct role for them. They should not be promoted into substantive novelty support for H1/H2/H3.
- If formal text needs a real novelty comparator, use direct Hadamard-search or modular-Hadamard sources instead.

## Likely Citation Hallucinations Or Metadata Risks

No load-bearing paper appears fabricated. The risk is weaker than "fake paper" and closer to "mixed or unstable metadata that could lead to bad paraphrase."

- `tsompanas2017`
  - Real paper.
  - Current BibTeX is internally inconsistent: it combines `journal={arXiv.org}` with a Springer chapter DOI.
  - Fix by choosing one version and citing it cleanly.
- `ghaleb2019`
  - Real learning-automata elevator paper.
  - Repo notes already flag a single-elevator / multi-elevator metadata mismatch.
  - Keep only as a broad watchlist comparator until revalidated. Do not paraphrase detailed content from it.
- `leeuwen2000`
  - Likely points to an LNCS proceedings volume rather than a chapter-specific contribution.
  - Adequate only as a lexical false positive or rhetorical-drift warning.
- `ghaemi2022`
  - Real paper, but domain-irrelevant to the actual Hadamard-search claims.
  - Keep it out of claim-bearing verification text.
- `suksmono2024`
  - Not currently load-bearing in the writeup.
  - Correct its metadata before use; the current year field is not reliable enough for a formal citation.

## Most Important Concrete Sources To Add

These are the most useful source additions for the current writeup. Several are already present in `sources.bib` but are not yet carrying the claims they should.

1. `eliahou2005`
   - Use for modular-Hadamard background and for placing the 2025 frontier object in context.
   - This is the most important missing background citation if the manuscript explains what a `64`-modular Hadamard matrix is or why the seed matters.

2. `eliahou2001`
   - Use if the writeup mentions the earlier modular-sequence lineage behind the order-668 result.
   - This gives the frontier anchor a stronger historical chain than `eliahou2025_64mod668` alone.

3. `bright2018`
   - Use as a stronger exact structured-search comparator than `bright2019` alone.
   - Especially important if the H2 family-leakage discussion keeps references to `Williamson`, `Turyn`, or exact structured-family search.

4. `suksmono2022` and/or corrected `suksmono2024`
   - Use if the paper keeps the sentence about "broader annealing or SAT+CAS Hadamard-search literature."
   - The current writeup leans too heavily on only `suksmono2018` and `suksmono2019` for that broader claim.

5. `cati2024`
   - Use for claims about known Hadamard constructions, solved orders, or literature landscape coverage.
   - This is also a cleaner citation than generic watchlist noise when the text needs a survey/database-style anchor.

6. Add a BibTeX entry for `Learning Automata-Based Solutions to the Multi-Elevator Problem` only if that watchlist comparator will remain in formal prose.
   - Otherwise, remove the comparator instead of citing it.

7. `sudhakaran2022`
   - Optional and not needed for the current H1 negative-result writeup.
   - Add only if future drafts discuss learned or goal-guided CA control, not just fixed-rule seeded repair.

## Recommended Fixes Before Final Paper Assembly

- Replace self-citation to `results/verification/citation_audit.md` with direct evidence.
- For seed provenance, cite `results/frontier/order_668_64m/seed_manifest.json`, `results/frontier/order_668_64m/source_excerpt.txt`, and `eliahou2025_64mod668`.
- For benchmark and exactness claims, cite `results/experiments/order_668_64m/summary.json`, the frontier run files, `results/experiments/order_668_64m/configs/*.json`, and `hadamard_ca/harness.py`.
- Keep `C6`, `C7`, `C9`, and the causal half of `C13` explicitly labeled as interpretation-level claims unless stronger external support is added.
- Demote `ghaleb2019`, `ghaemi2022`, and `leeuwen2000` to watchlist-only status in any formal manuscript text.

## Bottom Line

The current repo can support a narrow negative-result paper, but only if the citation structure is cleaned up:

- primary quantitative claims should cite direct artifacts rather than summary reports
- novelty and literature-competitiveness claims should stay narrow and inference-labeled
- weak watchlist citations should not carry any substantive argument
- the most important missing support is not more rhetoric about CA novelty; it is better grounding in modular-Hadamard background and direct Hadamard-search comparators
