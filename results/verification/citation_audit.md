# Citation Audit

Snapshot date: 2026-03-18 UTC
Verification phase: `review_round_1`

## Scope

- Primary inputs audited:
  - `research_paper.tex`
  - `sources.bib`
  - `results/research_context.md`
  - `results/literature/semantic_scholar_manifest.json`
- Support tracing also checked against:
  - `results/baselines/witness_spec.md`
  - `results/baselines/benchmark_spec.md`
  - `results/core/h1_design.md`
  - `results/core/lane_gates.md`
  - `results/experiments/h1_tiny_grid_report.md`
  - `results/experiments/h1_controls.md`
  - `results/experiments/complexity_sweep.md`
  - `results/verification/verification_summary.md`
  - `results/verification/benchmark_report.md`
  - `results/final_assessment.md`
  - `results/concept_evolve/concept_delta.md`
  - `results/concept_evolve/bridge_candidates.json`
- Web spot-checks were limited to high-risk citation-integrity questions:
  - `leng2024`
  - AlphaEvolve
  - Georgiev et al.
  - Cowen-Breen et al.
  - Pohoata-Zakharov
  - Tao (2025)
  - Green-Ruzsa
  - Hickman-Wright
  - Dennunzio et al.
  - Faldor-Cully

## Verdict

- `Pass` for blocker-level and repo-internal negative claims.
- `Revise` for manuscript-level citation support and evidence traceability.

Most important issues:

1. One likely source misfit / citation hallucination remains in the manuscript (`leng2024`).
2. The `<= 1.675` target and other prompt-derived formulation details still lack a direct provenance citation.
3. Several Related Work comparisons are interpretive and only weakly supported by the cited papers.
4. One important results claim is not fully traceable because repo artifacts disagree on bridge status.

## Claims With Solid Support

- Missing exact verifier / decoder and blocked phase-4 execution are strongly supported:
  - `research_paper.tex:109-117`
  - `research_paper.tex:147-157`
  - `research_paper.tex:476-492`
  - `research_paper.tex:808-828`
  - `research_paper.tex:913-983`
  - `research_paper.tex:1125-1130`
  - `results/repo_map.md:32-38`
  - `results/experiments/h1_tiny_grid_report.md:7-38`
  - `results/experiments/h1_controls.md:7-45`
  - `results/experiments/complexity_sweep.md:7-31`
  - `results/verification/verification_summary.md:21-28`

- The six-line witness format, exact score, no-repair decoder, and matched-budget benchmark contract are well supported internally:
  - `research_paper.tex:347-558`
  - `research_paper.tex:621-828`
  - `results/baselines/witness_spec.md:7-94`
  - `results/baselines/benchmark_spec.md:7-129`
  - `results/core/h1_design.md:7-120`
  - `results/core/lane_gates.md:7-56`

- The paper is generally honest about negative outcomes and does not overclaim a verified witness or benchmark win:
  - `research_paper.tex:830-835`
  - `research_paper.tex:1032-1043`
  - `research_paper.tex:1125-1135`
  - `results/verification/benchmark_report.md:29-38`
  - `results/verification/benchmark_report.md:80-90`
  - `results/final_assessment.md:7-28`

## Findings

### 1. `leng2024` is a likely source misfit, and currently the closest thing to a citation hallucination

- Claim location:
  - `research_paper.tex:340-344`
  - repeated upstream in `results/research_context.json:5` and `results/research_context.json:46`
- Citation used:
  - `sources.bib:126-133`
- Problem:
  - The cited paper is `Improved Bounds for Szemeredi's Theorem`, but the manuscript uses it to support a Kakeya-specific motivation claim about a Hausdorff-dimension upgrade.
  - `results/research_context.md:33-35` shows the repo searched for the Szemeredi paper itself, not for a Kakeya paper by these authors.
  - Web spot-checks confirm `2402.17995` is a Szemeredi-theorem paper, not a Kakeya paper.
- Audit judgment:
  - Real paper, wrong role. This is not a fabricated citation, but it is not adequate support for the sentence as written.
- Required fix:
  - Remove the Leng-Sah-Sawhney sentence, or replace it with a real Kakeya-dimension source.
  - If the sentence is meant as prompt provenance rather than literature support, cite the prompt/provenance artifact instead of `leng2024`.

### 2. The `<= 1.675` target and prompt-derived formulation still lack a direct provenance citation

- Claim location:
  - `research_paper.tex:91-99`
  - `research_paper.tex:129-131`
  - `research_paper.tex:212-213`
  - `research_paper.tex:324-338`
- Available support:
  - `results/research_context.json:5`
  - `results/research_context.json:46`
  - `results/verification/verification_summary.md:41-42`
- Problem:
  - The manuscript correctly says the `1.675` threshold is task provenance, not a theorem from the repo, but it does not cite the provenance source.
  - The same issue applies to phrases such as "the repository prompt adopts this formulation" and "the repository prompt uses the notation `AK(alpha)`".
- Audit judgment:
  - Missing provenance citation, not missing mathematics citation.
- Required fix:
  - Add an explicit provenance reference to the stored task text or another authoritative repo artifact whenever the paper attributes content to "the repository prompt".

### 3. Several comparative claims in Related Work are only weakly supported by the cited papers

- Claim cluster:
  - `research_paper.tex:213-227`
  - `research_paper.tex:246-269`
  - `research_paper.tex:291-301`
- Examples:
  - `research_paper.tex:216-225` turns Green-Ruzsa, Cowen-Breen et al., Pohoata-Zakharov, Tao, and Hickman-Wright into very specific warnings about proxy tasks, bounded-slope regimes, and modular mirages.
  - `research_paper.tex:263-269` and `research_paper.tex:291-295` use AlphaEvolve and Georgiev et al. to support the manuscript's "novelty floor" framing.
  - The same interpretive layer appears in `results/literature/prior_art_gap.md:72-133`.
- Problem:
  - These papers are relevant, but much of the current prose goes beyond straightforward source content and into manuscript interpretation.
  - The citations support adjacency and relevance; they do not, by themselves, prove each specific comparative statement as currently phrased.
- Audit judgment:
  - Mostly weak citations, not false citations.
- Required fix:
  - Soften the prose to make the interpretive layer explicit, e.g. "we treat X as a warning/adjacent constraint".
  - Where stronger phrasing matters, anchor it to a specific theorem/result/abstract claim instead of a title-level comparison.

### 4. The bridge-status narrative is not fully traceable because repo artifacts disagree

- Claim location:
  - `research_paper.tex:989-995`
  - `research_paper.tex:1013-1021`
  - `research_paper.tex:1039`
- Supporting artifacts currently disagree:
  - `results/concept_evolve/bridge_candidates.json:3-33` gives `2` promoted, `3` held, `4` retired, with `spatially_coupled_peeling_ladders` on `hold`.
  - `results/concept_evolve/concept_delta.md:20-27` says `spatially_coupled_peeling_ladders` was promoted.
  - `results/final_assessment.md:32-36` lists three surviving bridges, including `spatially_coupled_peeling_ladders`.
  - `results/concept_evolve/tree/phase_5_retrospective/001_surviving_exact_decoder_bridges/README.md:9-13` also describes three surviving bridges.
- Audit judgment:
  - This is not a literature-citation problem, but it is a major evidence-traceability problem.
  - The manuscript's `2/3/4` split is defensible if `bridge_candidates.json` is the source of truth, but that needs to be stated explicitly.
- Required fix:
  - Choose one authoritative artifact for final bridge status, or explain the stage distinction between "iterate-time decision" and "post-pivot surviving shortlist".

### 5. The results sections are supported, but traceability is thinner than it needs to be in the abstract and introduction

- Claim cluster:
  - `research_paper.tex:109-117`
  - `research_paper.tex:147-157`
  - `research_paper.tex:171-177`
- Available support:
  - `results/experiments/h1_tiny_grid_report.md:20-30`
  - `results/experiments/h1_controls.md:16-45`
  - `results/experiments/complexity_sweep.md:20-40`
  - `results/verification/benchmark_report.md:29-38`
- Problem:
  - The claims are supported later in the paper and in repo artifacts, but the early summary sections ask the reader to trust the narrative before seeing the artifact trail.
- Audit judgment:
  - Supported but lightly wired.
- Suggested fix:
  - Add one short artifact-provenance footnote or parenthetical reference in the abstract or introduction for the `0/3`, `0` decodes, and missing-verifier claims.

## Bibliography Integrity Notes

- No obviously fabricated paper was found in the high-risk spot checks.
- The main integrity problem is source fit, not source existence.
- Remaining lower-severity hygiene issues:
  - citation keys such as `green2017`, `bond2013`, and `bond2014` encode older scout/preprint years while the `year` fields point to later publication records (`sources.bib:13-20`, `sources.bib:61-76`);
  - most entries still use Semantic Scholar URLs instead of canonical publisher/arXiv URLs;
  - `novikov2025` and `georgiev2025` are adequate, but their `journal={arXiv.org}` style is inconsistent with the other arXiv records.

## Most Important Sources To Add Or Replace

1. Add a provenance citation for the task prompt that supplies:
   - the `<= 1.675` target,
   - the prompt-derived `AK(alpha)` wording,
   - and any statement explicitly attributed to "the repository prompt".
   Candidate artifact: `results/research_context.json:5`.

2. Replace `leng2024` as Kakeya motivation.
   - If the goal is still modern Kakeya-dimension motivation, add an actual Kakeya paper rather than a Szemeredi paper.
   - Concrete recent option from web spot-checking: Hong Wang and Joshua Zahl, `Volume estimates for unions of convex sets, and the Kakeya set conjecture in three dimensions` (arXiv:2502.17655).

3. If the stronger Related Work comparisons stay in place, add precise theorem/result anchors or brief section-level references for:
   - Tao (bounded slopes / rational complexity),
   - Hickman-Wright (modular adjacency),
   - AlphaEvolve and Georgiev et al. (automated-discovery comparison class).

## Bottom Line

- The paper's blocker story and negative empirical claims are well supported.
- The biggest citation problem is not missing general background; it is one misapplied source (`leng2024`) plus missing provenance wiring for prompt-derived claims.
- After fixing the Leng citation, adding prompt provenance, and resolving the bridge-status source-of-truth issue, the manuscript will have a much cleaner evidence trail.
