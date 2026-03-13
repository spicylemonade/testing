# Claim Grammar

Date: 2026-03-13
Task: Improve the Ramsey number `R(5,5)` bound

Source anchors:
- `results/plans/ramsey_research_program.md`
- `results/plans/phase4_evaluation_sheet.md`
- `results/verification/verification_summary.md`

## 1. Reporting Rule

Every title, abstract, table caption, and opening sentence must choose exactly one claim class:

| Claim class | Minimum evidence | Allowed headline verbs | Forbidden shortcuts |
| --- | --- | --- | --- |
| Bound improvement | independently verified `44`-vertex witness, or machine-checkable `45`-vertex impossibility proof | `improves bound`, `raises lower bound`, `lowers upper bound`, `closes frontier` | do not use for smaller residues, defect reductions, search speedups, pruning counts, or unchecked proofs |
| Structural intermediate result | transferable obstruction atlas, decomposition primitive, or certificate object that passes the required transfer and witness-safety or replay audits | `extracts`, `identifies`, `transfers`, `reuses`, `compresses` | do not use when the object is family-specific, proxy-only, or not audited on held-out families |
| Negative result | explicit route failure under a named stop rule, with failure artifacts and rollback notes | `rules out`, `kills`, `demotes`, `fails transfer`, `fails witness-safety` | do not hide a failed route inside optimistic wording such as `promising` or `suggestive` |
| Infrastructure-only result | reproducibility tool, corpus pack, checker wrapper, proof package, or bibliography repair with no structural or bound movement | `packages`, `reconstructs`, `indexes`, `audits`, `reproduces` | do not imply structural novelty, bound movement, or proof progress |

## 2. Current Ceiling

As of 2026-03-13, the allowed top-line report state is:

- No bound-improvement claim.
- No structural intermediate claim until `H1` survives `Rung 1` through `Rung 3`.
- Planning, governance, citation, and verification outputs are infrastructure-only.
- Any route killed by `anti_exoo_holdout`, witness death, or missing certificate path must be reported as a negative result.

## 3. Forbidden Phrasings

- Do not write `improves the bound` unless the artifact is an independently verified `44`-vertex witness or a checked `45`-vertex impossibility proof.
- Do not write `improves the upper bound` for a smaller residue unless the residue comes with a clear certificate path; without that path it is `residue_only`.
- Do not write `finds new structure` or `discovers reusable obstructions` unless held-out transfer and witness-safety both pass.
- Do not write `beats prior work` when the comparison table lacks the named prior row, shared comparison object, matched compute condition, and result-type column.
- Do not write `formalized`, `verified`, or `certificate-carrying novelty` for proof logging, proof export, or checker plumbing alone.
- Do not write `progress` for better defect scores, faster search, fewer branches, or stronger heuristics unless those metrics accompany the evidence required by the selected claim class.
- Do not blur `clear certificate path`, `intermediate evidence`, and `bound improvement`; they are separate report labels.

## 4. Required Claim Anchors

Every nontrivial claim must point to both:

1. A local artifact under `results/` that contains the exact evidence.
2. A bibliography entry in `sources.bib` or an explicit note that the claim is internal-only and not literature-backed.

Minimum anchor rules:

- Bound-improvement claims must cite the witness or certificate artifact plus the relevant comparison row from the Phase 4 matrix.
- Structural intermediate claims must cite the transfer record and the witness-safety or replay audit.
- Negative results must cite the stop-rule source and the failure artifact.
- Infrastructure-only claims must name the packaged artifact and explicitly say that no bound moved.

## 5. Wording Constraints By Route

- `H1` wording must include `R(5,5)`, `failed 42 -> 43 extensions`, `minimal obstruction cores`, and either `held-out transfer` or `witness-safety`.
- `H2` wording must name the decomposition primitive and at least one certificate metric: verified residue size, proof bytes, or checker runtime.
- `H3` wording must say that it is attached to `H1` or `H2` and must name the reuse test: cross-branch, cross-family, or orbit-stable transfer.

## 6. Title And Abstract Scrub

Before any writer draft is accepted:

1. The first sentence must contain `R(5,5)` and the concrete Ramsey object under discussion.
2. The first paragraph must name the claim class explicitly.
3. Any sentence containing `improve`, `better`, `stronger`, or `progress` must be checked against Sections 1 through 4.
