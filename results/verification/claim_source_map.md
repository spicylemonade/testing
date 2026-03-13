# Claim Source Map

Date: 2026-03-13
Rubric item: `item_023`
Task: Improve the Ramsey number `R(5,5)` bound

This file is the claim-to-evidence spine for the current run. Every structural or experimental statement in the reviewer packet must map to at least one local artifact and at least one bibliography entry unless the claim is explicitly internal-only.

## Active Claim Map

| Claim | Claim class | Local artifact anchor(s) | Bibliography anchor(s) | Current status |
| --- | --- | --- | --- | --- |
| The current frontier target is `43 <= R(5,5) <= 46`. | literature baseline | `results/literature/literature_snapshot.json` (`ramsey_specific_review` only), `results/research_context.md` | `exoo1989`, `ge2022`, `angeltveitmckay2024`, `radziszowski2024ds1` | usable |
| `H1` is a cross-family canonical obstruction atlas for failed `42 -> 43` extensions, not a new OVE algorithm. | structural route definition | `results/plans/phase3_route_sheet.md`, `results/plans/claim_grammar.md` | `ge2022`, `lehavi2024`, `lehavirepo` | route target only |
| `H1` only earns structural credit if recurrence, held-out transfer, and witness-safety all pass. | structural gate | `results/plans/phase3_route_sheet.md`, `results/verification/novelty_report.md`, `results/plans/claim_grammar.md` | `ge2022`, `lehavi2024` | required gate |
| Optimizer-only or symmetry-only lower-bound narratives are overlap-only and do not define novelty in this run. | overlap kill rule | `results/literature/prior_art_gap.md`, `results/plans/phase4_evaluation_sheet.md` | `aijaam2010`, `ge2022` | fixed |
| `H2` is inactive unless it introduces a genuinely different decomposition primitive under matched certificate metrics. | bounded backup route | `results/plans/phase3_route_sheet.md`, `results/swarm/phase3_stress_test.md` | `mckay1992`, `angeltveit2018`, `angeltveitmckay2024`, `gauthier2025` | demoted |
| `H3` is infrastructure-only unless attached to a transferable structural object from `H1` or `H2`. | infrastructure rule | `results/plans/phase3_route_sheet.md`, `results/swarm/phase3_stress_test.md`, `results/plans/claim_grammar.md` | `gauthier2024`, `gauthierbrown2024arxiv`, `barakeel2025`, `barakeelramseyrepo` | demoted |
| Only an independently verified `44`-vertex witness or a machine-checkable `45`-vertex impossibility proof counts as a bound improvement. | claim grammar / benchmark rule | `results/plans/phase2_baseline_sheet.md`, `results/plans/phase4_evaluation_sheet.md`, `results/plans/claim_grammar.md` | `exoo1989`, `angeltveitmckay2024`, `radziszowski2024ds1` | fixed |
| The current run is `No-go` on any bound-improvement claim and on any claim that `H1` is already an achieved structural intermediate result. | current verdict | `results/verification/verification_summary.md`, `results/verification/evaluation_rehearsal.md`, `results/verification/h1_acceptance_contract.md` | `angeltveitmckay2024`, `radziszowski2024ds1` | active |

## Verification And Reproducibility Anchors

- Benchmark equality and anti-proxy rules: `results/verification/benchmark_report.md`
- Citation-strength review and open bibliography debt: `results/verification/citation_audit.md`
- Fixed `H1` pass/fail contract: `results/verification/h1_acceptance_contract.md`
- Novelty threshold and closest-overlap check: `results/verification/novelty_report.md`
- Cross-artifact go or no-go state: `results/verification/verification_summary.md`
- Evaluation order and sequencing risks: `results/verification/evaluation_rehearsal.md`

## Remaining Citation Gaps

- `aijaam2010` remains an overlap-only citation grounded only by institutional-repository or conference-level metadata, so it must not carry comparison-grade argumentative weight.
- `mckay1992` still lacks a direct publisher or journal-hosted landing page in `sources.bib`; it remains usable as a classical baseline anchor, but the URL is still a discovery mirror.
- `noga2022` remains a background-only survey entry with a discovery URL and must not be used as a load-bearing source in any final memo.
- `results/literature/literature_snapshot.json` is not discovery-safe by itself because its original seed query was noisy; only the curated Ramsey-specific sections are safe to cite directly.

## Writer Constraint

No writer draft is accepted unless each paragraph-level claim can be traced back to one row in the table above or to a new row added here with the same local-artifact and bibliography anchors.
