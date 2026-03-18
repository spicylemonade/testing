# Citation Audit

## Scope

- `research_paper.tex` is not present in this repo, so this audit covers source support and evidence traceability for the current evidence packet rather than manuscript-level citation placement.
- Audited inputs: `sources.bib`, `results/research_context.md`, `results/literature/semantic_scholar_manifest.json`, `results/literature/literature_snapshot.json`, `results/literature/prior_art_gap.md`, `results/analysis/branch_brief.md`, `results/analysis/baseline_benchmark_sheet.md`, `results/analysis/experiment_readout.md`, `results/analysis/phase2_baseline_review.md`, `results/swarm/falsifier.md`, `results/swarm/gap_map.md`, `results/swarm/hypothesis_negative_space.md`, and the verification summaries under `results/verification/`.

## Verdict

- Narrow final claim: `pass`
  - The repo tested cellular-automata branches for Hadamard `668`, and the implemented `H1` and `H2` branches failed under matched controls.
- Publication-ready citation layer for broader novelty / prior-art discussion: `qualified fail`
  - The active source basis is present, but several surrounding memos still contain uncatalogued, weakly mapped, or likely hallucinated references.

## Load-bearing source map

- Exact `H1` obstruction:
  - `constantine2025cyclic`
- Exact `H2` seed:
  - `eliahou2025mod64`
- Modular / general Hadamard background:
  - `eliahoukervaire2005survey`
  - `horadam2007applications`
- Structured exact and family-level competitors:
  - `bright2018satcas`
  - `fitzpatrick2023williamson`
  - `djokovic2018goethalsseidel`
- CA-side prior art and novelty guards:
  - `manzoni2025survey`
  - `mariot2016ols`
  - `gadouleau2020bent`
  - `mariot2021semibent`
  - `bagnoli2025controllability`
  - `herold2014decoder`
- Direct heuristic competitors:
  - `suksmono2016sa`
  - `suksmono2018sqa`
  - `suksmono2022quantum`
  - `suksmono2024qaoa`

## What Is Supported

- The active literature basis itself is complete enough for the executed branches. The 13 focused papers in `results/literature/literature_snapshot.json:455-559` are all represented in `sources.bib`, and the manifest shows the key paper IDs were actually queried or recorded during the run.
- The `H1` branch is tied to a concrete external anchor. `results/analysis/branch_brief.md:15-18` and `results/literature/prior_art_gap.md:51-56` align the branch to the exact `167/80` cyclic obstruction, and `results/artifacts/target_167_weight_80.json:695` records that the stored target vector came from the cited paper.
- The `H2` branch is tied to a concrete external anchor. `results/analysis/branch_brief.md:21-23` and `results/literature/prior_art_gap.md:58-63` tie the branch to the published `64`-modular order-668 seed, and `results/artifacts/seed_668_mod64.json:1010-1011` records the mod-64 certificate facts used by the experiments.
- The final no-go decision is traceable to local evidence rather than to vague narrative. `results/analysis/experiment_readout.md:5-73`, `results/analysis/phase2_baseline_review.md:11-29`, `results/verification/benchmark_report.md:8-26`, and the four JSON run packets under `results/experiments/` consistently support the claims that `H1` lost to `direct_greedy` and that `H2` failed to beat the matched baseline on the real `668` attempt.
- The active novelty-collapse comparisons are at least anchored to relevant families. `results/literature/prior_art_gap.md:65-91` maps the branch against SAT+CAS, Williamson / Goethals-Seidel, CA design work, and direct Hadamard heuristics using sources that are already in `sources.bib`.

## Missing Citations, Weak Citations, And Likely Hallucinations

- `High`: no manuscript-level citation binding can be checked because `research_paper.tex` is absent. The current packet shows source availability, not whether final prose actually cites each load-bearing claim where it appears.
- `High`: `results/swarm/falsifier.md:37`, `results/swarm/falsifier.md:82`, and `results/swarm/falsifier.md:102` use the bundled label `Suksmono 2019/2022`, but `sources.bib` only contains the 2022 paper (`suksmono2022quantum`). The 2019 `Finding Hadamard Matrices by a Quantum Annealing Machine` source is missing from the bibliography, so those comparisons are only partly citation-bound.
- `High`: `results/swarm/gap_map.md:108-109` and `results/swarm/hypothesis_negative_space.md:125-128` appear to misattribute existing competitor papers. The repo bibliography maps those titles to `A. B. Suksmono` (and `Yuichiro Minato` for the 2022 paper), but the memos use `Bambang et al.`, `Suprijadi et al.`, `Solihah et al.`, and `Arostegui et al.`. Those look like citation hallucinations or stale name substitutions, not harmless formatting drift.
- `Medium`: `results/swarm/hypothesis_negative_space.md:122-132` lists several papers that are not in `sources.bib` at all: Piza Volio on Turyn sequences, Kharaghani / Djokovic / Tayfeh-Rezaie on new Hadamard orders, `Mutually Orthogonal Latin Squares based on Cellular Automata`, and Wolnik et al. on number-conserving CA. They are reserve-branch references, so they do not sink the narrow no-go claim, but they are uncited comparisons if that memo language is promoted into final prose.
- `Medium`: `results/swarm/gap_map.md:104` uses OEIS `A007299` as the anchor for the `668` open-case status, but OEIS is not in `sources.bib`. This is unnecessary because the same status claim can be tied directly to `eliahou2025mod64` or another standard Hadamard reference already in scope.
- `Medium`: search-process claims are not always marked as search-process claims. Statements such as `I did not find evidence of a direct cellular-automata search for a real Hadamard matrix of order 668` in `results/swarm/gap_map.md:22` and `direct order-668 CA search appears underexplored` in `results/swarm/falsifier.md:17` are not facts proved by a single external paper. They should be tied to the internal search trace in `results/literature/literature_snapshot.json:579-603` and `results/literature/semantic_scholar_manifest.json`, or softened as scoped literature-search conclusions.
- `Low`: bibliographic metadata quality is still weak. Fifteen of the 23 `sources.bib` entries use Semantic Scholar landing pages instead of canonical DOI, publisher, arXiv, or journal URLs. This does not invalidate the narrow claim, but it weakens traceability and makes downstream citation export brittle.
- `Low`: a few keys encode stale years or labels (`herold2014decoder` has year `2015`; `suksmono2024qaoa` has year `2025`; `bagnoli2025controllability` is cited elsewhere as a `2026` journal article). These are hygiene problems, not claim failures, but they should be normalized before manuscript writing.

## Uncited Or Weakly Cited Comparisons To Watch

- The watchlist papers in `sources.bib` are fine as lexical-noise guards, but they should not be cited as if they were technical competitors. Keep them tied to the novelty-filtering role described in `results/literature/prior_art_gap.md:5-45`.
- Any claim that a CA branch is distinct because it acts on `167`-cycle supports or on the `64`-modular defect pattern should stay linked to the exact anchors in `constantine2025cyclic` and `eliahou2025mod64`; otherwise the comparison drifts into vague `CA for Hadamard search` language that the current literature packet does not support.
- If reserve branches are discussed, they need their own explicit source map. Right now `results/swarm/hypothesis_bridge.md:6-28` and `results/swarm/hypothesis_negative_space.md:119-132` contain comparative claims that are not fully mapped to bib keys.

## Highest-Priority Concrete Sources To Add

- `Finding Hadamard Matrices by a Quantum Annealing Machine` (A. B. Suksmono, 2019).
  - Needed to repair the missing half of the bundled `Suksmono 2019/2022` comparison in `results/swarm/falsifier.md`.
- `Search of Hadamard Matrices by Turyn Sequences` (Jorge Piza Volio, 2011).
  - Add only if `results/swarm/hypothesis_negative_space.md` continues to compare against Turyn-sequence search rather than dropping that line.
- `Some new orders of Hadamard and skew-Hadamard matrices` (Kharaghani / Djokovic / Tayfeh-Rezaie, 2013/2014).
  - Add if the reserve memo keeps claims about the classical exact-family frontier beyond the already-cited Williamson / Goethals-Seidel sources.
- `Mutually Orthogonal Latin Squares based on Cellular Automata` (Mariot et al., 2019).
  - Add only if the reserve memo keeps that exact CA-design comparison; otherwise replace it with the already-bibliographed 2016 Latin-squares paper.
- Canonical URLs for the active basis.
  - Replace Semantic Scholar URLs for the load-bearing entries first, especially `bright2018satcas`, `mariot2016ols`, `mariot2021semibent`, `bagnoli2025controllability`, `suksmono2016sa`, `suksmono2018sqa`, `suksmono2022quantum`, and `djokovic2018goethalsseidel`.

## Bottom Line

- The repo has enough literature and experiment support for a narrow negative-result packet.
- The citation layer is not ready for broader novelty claims until the misattributed reserve-memo references are cleaned up, the missing 2019 quantum-annealing paper is added, and a real manuscript exists so in-text citation placement can be audited.
