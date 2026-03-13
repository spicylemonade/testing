# Benchmark Report

Date: 2026-03-13
Owner role: `benchmark_auditor`
Rubric item: `item_010`
Active hypothesis: `H1`
Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof
Reviewed artifacts:
- `results/plans/phase2_baseline_sheet.md`
- `results/plans/ramsey_research_program.md`

## Audit Verdict

The baseline is coherent enough to proceed, but it was not fully audit-safe before this report.
Two concrete fixes were required:

1. Upper-bound residues with a `clear certificate path` are now classified as certificate-path progress or intermediate evidence, never as bound improvements.
2. The benchmark protocol now fixes the matched-compute tuple and the upper-bound win rule instead of letting those choices drift after the run.

## Findings

- Lower-bound and upper-bound work are both constrained by hard artifact thresholds rather than proxy metrics.
- Certificate requirements are explicit on both sides, but the upper-bound threshold needed clarification so residue-only improvements could not be over-credited.
- The baseline lacked a fully fixed matched-compute tuple before this audit.
- The baseline lacked a predeclared upper-bound win rule before this audit.
- The concept-tree line in the main program had a stale blocker; the actual first-pass tree already exists locally.

## Baseline Integrity Rules

1. Only independently verified `44`-vertex witnesses count as lower-bound progress.
2. Any upper-bound result without an independently checked `45`-vertex impossibility proof is labeled `improves certificate path` or `intermediate evidence`, never `improves bound`.
3. A `clear certificate path` is valid only when the artifact includes a machine-readable residue, residue hash, remaining-open-case count, target proof format, checker name and version, and an exact replay plan.
4. Every benchmark row must log the full matched-compute tuple: solver version, proof format, preprocessing, thread count, hardware class, timeout policy, branch-order policy, random-seed policy, and warm-start or cached-clause policy.
5. Warm starts, oracle seeds, cached clauses, proof reuse, and hand-picked symmetry priors are excluded from headline comparisons unless they are enabled symmetrically for both baseline and candidate.
6. The upper-bound win rule is fixed in advance as `bound status > certificate class > verified residue size > proof bytes > checker runtime`; no headline claim survives a regression on a higher-priority metric.
7. Every pruning object, kernel, lemma, or certificate-reuse object must have an on/off ablation on the same rung set under the same compute tuple.
8. Every accepted witness or certificate artifact must be replayed outside the generating workflow with hashes, checker version, and pass/fail result recorded.
9. Every upper-bound primitive must reproduce at least one solved smaller certificate case before it is trusted on `R(5,5)`.
10. Every benchmark manifest must be frozen before tuning, and every run must emit one failure code from the closed taxonomy.

## Remaining Enforcement Gaps

- The repo still lacks a local `frontier_parent` corpus, an orbit-distinct `42 -> 43` extension enumerator, an independent `44`-vertex witness verifier, and a `45`-vertex certificate checker.
- Transfer and diversity gates are still qualitative; later experiment artifacts should add numeric pass thresholds.
- Cross-route comparison tables still need an explicit `shared comparison object` column to avoid non-commensurable `H1` vs `H2` comparisons.
