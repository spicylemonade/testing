# Novelty Report

Date: 2026-03-13
Owner role: `novelty_checker`
Verification phase: `review_round_1`
Active hypothesis: `H1` = `Cross-family canonical obstruction atlas for failed 42 -> 43 extensions in R(5,5)`
Manuscript scope on the current record: `infrastructure-only` + `negative result`, with a prospective `H1` structural route target only
Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof

Reviewed artifacts:
- `research_paper.tex`
- `results/research_context.md`
- `results/literature/prior_art_watchlist.md`
- `results/literature/prior_art_gap.md`
- `results/swarm/director_brief.md`
- `results/swarm/falsifier.md`
- `results/swarm/gap_map.md`
- `results/plans/claim_grammar.md`
- `results/plans/phase3_route_sheet.md`
- `results/verification/claim_source_map.md`
- `results/verification/h1_acceptance_contract.md`
- `results/verification/verification_summary.md`
- `results/verification/final_review.md`
- `results/verification/benchmark_report.md`
- `results/verification/citation_audit.md`
- `sources.bib`
- targeted primary-source web checks for `angeltveitmckay2024` and the overlap-only `gauthier2025` strategy abstract

## Audit Verdict

The manuscript is novelty-safe only under its current narrow framing. As written in `research_paper.tex`, the achieved contribution is not a new Ramsey object, not a new bound, and not an executed `H1` structural result. The achieved contribution is a constrained no-go / route-specification memo: it packages the only remaining novelty-safe route, formalizes the claim contract, and proves that the present repository state does not justify stronger claims.

That means the paper has two different novelty standards. The prospective novelty standard belongs to `H1`: a transfer-safe cross-family obstruction atlas over failed `42 -> 43` extensions. The achieved novelty standard belongs to the actual manuscript scope: infrastructure, governance, and a negative result. `H1` is the only route with a plausible moat, but it is still unexecuted. The achieved manuscript is materially distinct only as a disciplined checkpoint memo; it is not materially distinct as an established structural Ramsey contribution.

## Major Claims Versus Closest Prior Art

| Major claim as written now | Claim class | Closest paper or line of work | Overlap signal | Distinctness judgment |
| --- | --- | --- | --- | --- |
| A transfer-safe obstruction atlas over failed `42 -> 43` extensions is the only credible positive route. | prospective structural route | `ge2022`; `lehavi2024` and `lehavirepo` | Same Exoo-derived `42/43` witness surface and same one-vertex-extension / counterexample-checking regime. | This is the only potentially material novelty claim. It is distinct only if it produces recurring canonical cores that transfer across parent families, survive witness-safety, and do more than extension-table reorganization or Exoo-line structural digestion. On the current record it is a route target, not a defended contribution. |
| The paper reconstructs that route as a precise data model, evaluation ladder, and kill-switch program. | infrastructure-only | `lehavi2024` operationally; `ge2022` for the Exoo structural surface; local route docs in `results/plans/phase3_route_sheet.md` | Same underlying objects: frontier parents, failed extensions, witness extraction, and family-specific structure. | Useful synthesis, but not a strong field-level novelty moat by itself. This is mostly disciplined packaging of a plausible route rather than a new Ramsey result. |
| The paper proves protocol-level results about canonicalization, witness-oracle safety, and the acceptance contract. | infrastructure-only | formal proof / certified exact-computation line: `gauthier2024`, `gauthierbrown2024arxiv`, `narvez2024`, `heule2018schur`, `li2025ramseycert` | Same emphasis on admissible proof objects, replayable evidence, and sharp separation between heuristic evidence and checked claims. | These results increase rigor inside the repo, but they are closer to formalized governance than to new combinatorics. As external novelty they are weakly differentiated. As internal claim-control machinery they are valid and useful. |
| The paper gives a publication-grade synthesis of prior art, chronology, and evidence inventory. | infrastructure-only | `radziszowski2024ds1`; related-work baselines in `angeltveitmckay2024`; local synthesis in `results/literature/prior_art_gap.md` | Surveying the frontier and aligning route choice to prior work is already part of the surrounding literature and the repo’s own gap notes. | Not materially novel research. This is review and integration work, valuable for packet integrity but not a scientific moat. |
| The paper proves a repository-state no-go theorem: no bound movement and no achieved `H1` structural intermediate result are currently supportable. | negative result | exact-frontier and certification discipline rather than a single technical precursor: `exoo1989`, `ge2022`, `angeltveitmckay2024`, `radziszowski2024ds1`, with proof-discipline context from `gauthier2024`, `heule2018schur`, and `li2025ramseycert` | The theorem is driven by claim grammar plus absence of required artifacts, not by new Ramsey mathematics. | Honest and defensible at packet level, but its novelty is mostly governance-level. It is best sold as a disciplined stop signal, not as a new mathematical theorem about `R(5,5)`. |

## Closest Prior Art For The Named Alternative Routes

| Route or narrative | Closest paper or line of work | Novelty assessment |
| --- | --- | --- |
| `H2` decomposition upgrade beyond split-vertex / transverse-edge gluing | `mckay1992`, `angeltveit2018`, `angeltveitmckay2024`, plus overlap-only `gauthier2025` | Weak differentiation on the current record. Unless the primitive itself changes the proof object and wins on verified residue, proof bytes, or checker runtime under matched conditions, this is the same upper-bound surface with a stronger engine. |
| `H3` proof-carrying reusable obstruction certificates | `gauthier2024`, `gauthierbrown2024arxiv`, `narvez2024`, `heule2018schur`, `li2025ramseycert` | Not materially distinct as a standalone route. Proof packaging or replay infrastructure is prior-covered unless attached to a transferable obstruction object from `H1` or a genuinely new `H2` primitive. |
| Optimizer / symmetry / GA / rare-event lower-bound narratives | Exoo’s constructive line, `aijaam2010`, `ge2022` | Not novel for this packet. The gap note is correct that better search trajectories, better defect scores, or better symmetry handling do not define a novelty moat here. |

## Novelty Illusions And Weak Differentiation

1. OVE relabeling illusion.
   - Grounding: `lehavi2024`, `lehavirepo`, and the paper’s own related-work warning.
   - Risk: if `H1` mainly reconstructs the `R(5,5,42)` to `R(5,5,43)` transition, catalogs failed extensions, or improves emptiness checking organization, it sits on Lehavi’s one-vertex-extension surface rather than escaping it.

2. Exoo-line digest illusion.
   - Grounding: `exoo1989`, `ge2022`, `results/literature/prior_art_gap.md`.
   - Risk: if the recurring cores are mostly carried by one Exoo-like lineage, the result is a sharper digest of known witness structure, not a new cross-family Ramsey object.

3. Governance-theorem inflation.
   - Grounding: `research_paper.tex` contributions 2 and 4; `results/plans/claim_grammar.md`; `results/verification/h1_acceptance_contract.md`.
   - Risk: quotient lemmas, witness-oracle safety, and the no-go theorem are important for claim discipline, but they mostly formalize the repo’s reporting contract. That is weaker scientific differentiation than the manuscript’s theorem language may suggest.

4. Bridge-without-bridge-evidence illusion.
   - Grounding: `results/plans/phase3_route_sheet.md` reuse claim; `results/swarm/director_brief.md`; `results/swarm/gap_map.md`.
   - Risk: the strongest rhetorical differentiator is that the same core family could link lower-bound pruning and upper-bound lemma generation. No current artifact demonstrates that identity-preserving bridge. Right now it is a hypothesis, not evidence.

5. Solver-shopping illusion for `H2`.
   - Grounding: `results/literature/prior_art_gap.md`; `results/swarm/falsifier.md`; `gauthier2025`.
   - Risk: branch ordering, SAT strength, warm starts, or residue shrinkage without a changed decomposition primitive is not material novelty over the McKay -> Angeltveit-McKay -> Gauthier line.

6. Proof-packaging illusion for `H3`.
   - Grounding: `gauthier2024`, `narvez2024`, `heule2018schur`, `li2025ramseycert`.
   - Risk: certificate wrappers, replay plumbing, or Lean-facing packaging are infrastructure unless the same structural object transfers across branches or families and reduces checked proof cost.

7. Overlap-only bibliography inflation.
   - Grounding: `results/verification/citation_audit.md`, `sources.bib`.
   - Risk: `aijaam2010` and `gauthier2025` are useful overlap notes, but not comparison-grade baseline wins. `noga2022` is background-only. `lehavirepo`, `barakeelramseyrepo`, and `mckayramseydata` are artifact rows, not standalone novelty anchors.

## Missing Gap Evidence

The current packet does not yet supply the evidence that would turn `H1` from a plausible gap into a materially distinct contribution.

- `results/h1/` is absent, so none of the route-defining artifact files exists.
- There is no local `frontier_parent`, `extension_case`, or `failure_witness` corpus.
- There is no orbit-distinct `42 -> 43` extension enumerator.
- There is no `results/h1/obstruction_cores.jsonl` demonstrating recurring canonical cores.
- There is no `results/h1/transfer_records.jsonl` demonstrating leave-one-parent-out transfer or the decisive `anti_exoo_holdout`.
- There is no `results/h1/witness_safety_audit.md` demonstrating zero known-witness deletions.
- There is no replayable upper-bound lemma path showing that any canonical core survives intact when moved from lower-bound pruning to upper-bound proof use.
- There is no independently verified `44`-vertex witness and no machine-checkable `45`-vertex impossibility proof, so no stronger novelty framing can be attached to bound movement.

These are not generic execution gaps. They are exactly the missing evidence needed to prove that the claimed object is new rather than a relabeling of Lehavi-style OVE work or Ge-style witness analysis.

## What Would Count As Material Distinctness

`H1` becomes materially distinct only if the repo can show all of the following at once:

1. A small canonical obstruction library recurs across at least 3 non-isomorphic parent families rather than one Exoo-like lineage.
2. Leave-one-parent-out transfer, especially the decisive `anti_exoo_holdout`, preserves a substantial fraction of training-side coverage.
3. Every core-derived filter is witness-safe on the stored `42`- and `43`-vertex constructions.
4. At least one canonical core family keeps the same identity when reused as both lower-bound pruning evidence and an upper-bound lemma candidate.

Without that package, the manuscript’s honest novelty lies in disciplined scoping and claim control, not in a demonstrated new Ramsey object.

## Bottom Line

The manuscript is defensible as a constrained no-go / route-specification paper. That is its strongest honest scope, and on that scope it is adequately differentiated from the prior art because it is not claiming a new bound, a new OVE algorithm, a new decomposition primitive, or a new proof-transfer artifact.

The moment the paper asks for credit beyond that scope, the differentiation weakens sharply. `H1` is still prospective, `H2` is too close to the live upper-bound line, and `H3` is infrastructure-only unless attached to a transferable structural object. The real novelty moat is therefore not yet demonstrated; it is only specified.

Verdict: DEEPEN
