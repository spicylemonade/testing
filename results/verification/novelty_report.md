# Novelty Report

Date: 2026-03-13
Owner role: `novelty_checker`
Verification phase: `post_researcher`
Active hypothesis: `H1` = `Cross-family canonical obstruction atlas for failed 42 -> 43 extensions in R(5,5)`
Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof

Reviewed artifacts:
- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/literature/gap_frontier.md`
- `results/literature/literature_snapshot.json`
- `results/swarm/director_brief.md`
- `results/swarm/falsifier.md`
- `results/swarm/gap_map.md`
- `results/swarm/phase1_cleanup.md`
- `results/swarm/phase3_stress_test.md`
- `results/swarm/hypotheses.json`
- `results/plans/claim_grammar.md`
- `results/plans/phase3_route_sheet.md`
- `results/plans/phase4_evaluation_sheet.md`
- `results/verification/claim_source_map.md`
- `results/verification/h1_acceptance_contract.md`
- `results/verification/verification_summary.md`
- `results/verification/evaluation_rehearsal.md`
- `sources.bib`

## Audit Verdict

The packet identifies a real negative-space gap, but the claimed contribution is only materially distinct in its narrowest `H1` form and only as a route target, not as an achieved result. The genuinely new part is not one-vertex extension, witness re-verification, lower-defect search, decomposition engineering, or proof packaging by itself. The only plausible novelty moat is a small, canonical, transfer-safe obstruction dictionary that recurs across non-isomorphic parent families and survives witness-safety checks. Without that object, the contribution collapses into already occupied surfaces: Lehavi 2024 for one-vertex extension and counterexample checking, Ge et al. 2022 for Exoo-line witness analysis and low-defect `K_43` structure, the Angeltveit-McKay and Gauthier line for upper-bound decomposition, and the formal-proof line around `R(4,5)=25` for certificate infrastructure.

## Major Claims Versus Closest Prior Art

| Major claim | Closest paper or line of work | Novelty assessment |
| --- | --- | --- |
| `H1`: canonical obstruction atlas for failed `42 -> 43` extensions | Lehavi 2024, `Ramsey Number Counterexample Checking and One Vertex Extension Linearly Bound by s and t`; Ge et al. 2022, `Study of Exoo's Lower Bound for Ramsey number R(5,5)` | This is the closest plausible novelty claim, but only if the output is a reusable cross-family obstruction object. If the work mainly reconstructs extension cases, verifies `R(5,5,43)` emptiness from `R(5,5,42)`, or catalogs failure witnesses, it is too close to Lehavi's OVE/checking surface. If it mainly studies Exoo-line near-miss structure or low-defect `K_43` variants, it is too close to Ge et al. |
| `H1` reuse claim: the same cores support lower-bound pruning and upper-bound lemma candidates | Ge et al. 2022 on Exoo-line structure; Angeltveit-McKay 2024, `R(5,5) <= 46`; the broader McKay-Radziszowski to Angeltveit-McKay upper-bound line | This is the right bridge to aim for, but the packet has no executed evidence that the same canonical core survives the jump from lower-bound extension failures into proof-grade upper-bound use. At present this is a conjectured bridge, not demonstrated differentiation. |
| `H2`: better decomposition primitive beyond split-vertex and transverse-edge gluing | McKay-Radziszowski 1992; Angeltveit-McKay 2018 and 2024; Gauthier 2025, `Decreasing the upper bound on the Ramsey number R(5,5)` | Weak differentiation on the current record. Unless the primitive is non-equivalent to the existing split/glue language and wins on verified residue or certificate metrics under matched conditions, this is just the same proof object with a stronger engine or different branching order. |
| `H3`: proof-carrying reusable obstruction certificates | Gauthier-Brown 2024, `A Formal Proof of R(4,5)=25`; Barakeel-Gauthier-Commelin 2025; nearby SAT proof-logging and certificate-reuse lines | Not materially distinct as a standalone contribution. Proof packaging, replay, or checker plumbing overlaps heavily with existing formal-verification and certificate lines unless it is attached to a new transferable structural object from `H1` or `H2`. |
| Optimizer- or symmetry-driven lower-bound narrative | Exoo constructive search line; Aija'am 2010, `Can genetic algorithms with the symmetric heuristic find the Ramsey number R(5,5)`; Ge et al. 2022 | Not novel for this packet. Any story centered on better search, lower defect, or symmetry handling is explicitly overlap-only and fails the packet's own novelty guard. |

## Material Distinctness Assessment

### `H1`

`H1` is materially distinct only in its most demanding formulation: recurring minimal obstruction cores extracted from failed orbit-distinct `42 -> 43` extensions, transferring across at least 3 non-isomorphic parent families, retaining coverage under leave-one-parent-out evaluation, and preserving all known `42`- and `43`-vertex witnesses. That combination would be more than witness re-verification, more than one-vertex extension checking, and more than optimizer tuning.

The problem is that the current repo does not yet contain the evidence that separates that story from prior work. There is no local `frontier_parent` corpus, no orbit-distinct `42 -> 43` enumerator, no `results/h1/obstruction_cores.jsonl`, no `results/h1/transfer_records.jsonl`, and no witness-safety audit. On today's record, `H1` is a well-posed novelty hypothesis, not a defended contribution.

The closest direct novelty threat is Lehavi 2024 because both operate on the same one-vertex-extension surface and both depend on the `R(5,5,42)` to `R(5,5,43)` regime. The closest lower-bound structural overlap is Ge et al. 2022 because that paper already turns Exoo's witness line into explicit analysis and low-defect structural discussion. The report should therefore treat `H1` as novel only if it demonstrates transfer-safe compression across parent families, not if it merely reconstructs or explains extension failures more cleanly.

### `H2`

`H2` does not currently clear the novelty bar. The repo itself demotes it because the dominant overlap is too strong: McKay-Radziszowski's case-analysis ancestor, Angeltveit-McKay's exact upper-bound program, and Gauthier's split-vertex/transverse-edge successor line already occupy the main decomposition-plus-SAT surface. A decomposition story earns novelty only if the decomposition primitive itself changes the proof object and the gain survives matched proof metrics. Nothing in the current packet shows that yet.

### `H3`

`H3` is infrastructure unless attached to a real structural object. The closest comparison line is already formalized exact Ramsey certification, especially `R(4,5)=25`, plus adjacent certificate and proof-logging workflows. The packet is correct to demote `H3`: without cross-family or cross-branch transfer of the same canonical core, this is packaging, not material novelty.

## Novelty Illusions To Call Out Explicitly

1. OVE relabeling illusion.
   If `H1` outputs a better-organized extension table, emptiness-checking workflow, or failure catalog, it overlaps with Lehavi 2024 rather than escaping it.

2. Exoo-line memorization illusion.
   If the recurring cores are carried mainly by Exoo-like parents or by one seed family, the result is a family-specific digest of the Ge/Exoo line, not a new Ramsey object.

3. Optimizer theater.
   Any shift toward better search, lower defect counts, GA tuning, or symmetry heuristics collapses into existing constructive-search overlap already flagged by the Aija'am and Exoo/Ge lines.

4. Solver-shopping illusion.
   Any `H2` story that keeps split-vertex or transverse-edge gluing intact and changes only SAT strength, branch order, warm starts, or engineering presentation is not a new decomposition result.

5. Proof-packaging illusion.
   Any `H3` story centered on proof export, checker wrappers, or formalization scaffolding without a transferable structural core overlaps with existing exact-proof infrastructure.

6. Query-noise illusion.
   The lexical watchlist and early snapshot artifacts are noisy enough that broad novelty language can look safer than it is. Only the curated Ramsey-specific corpus should carry argumentative weight.

## Missing Gap Evidence

The report should not overstate novelty because the decisive gap evidence is still absent:

- no local `frontier_parent`, `extension_case`, or `failure_witness` corpus
- no orbit-distinct `42 -> 43` extension enumerator
- no `results/h1/*` artifact layer showing recurrence, family balance, or canonical core compression
- no `anti_exoo_holdout` result establishing transfer beyond the Exoo lineage
- no witness-safety audit showing zero known-witness deletions
- no replayable certificate path showing that any `H1` core actually becomes a usable upper-bound lemma
- no independent `44`-vertex witness verifier or `45`-vertex certificate checker, which blocks any stronger progress claim

These omissions matter directly for novelty, not just execution readiness. Until they are filled, the packet cannot show that its claimed object exists, transfers, or stays sound.

## Bottom Line

The repo's narrow positive claim is defensible: there may be a missing structural layer between lower-bound constructions and upper-bound case proofs, and the best shot at it is a transfer-safe obstruction atlas over failed `42 -> 43` extensions. But the novelty moat is still mostly prospective. `H1` remains the only route with a credible path to material distinctness; `H2` is too close to the live upper-bound line, and `H3` is not novel on its own.

Verdict: DEEPEN
