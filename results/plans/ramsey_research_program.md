# Ramsey Research Program

Date: 2026-03-13
Task: Improve the Ramsey number `R(5,5)` bound
Current frontier target: `43 <= R(5,5) <= 46`

## 0. Fixed Ramsey Corpus And Framing Guard

Source of truth for the Phase 1 cleanup:
- `results/swarm/phase1_cleanup.md`

Do not widen literature search again until the fixed corpus from that synthesis is exhausted.

Active reading order:
1. `Small Ramsey Numbers Dynamic Survey 1`
2. Exoo 1989
3. Ge et al. 2022
4. Lehavi 2024
5. Angeltveit-McKay 2024 `R(5,5) <= 46`
6. Angeltveit-McKay 2018 `R(5,5) <= 48`
7. McKay-Radziszowski 1992
8. Aija'am 2010, overlap-only
9. Gauthier 2025, only if `H2` is opened
10. Gauthier-Brown 2024 and Barakeel-Gauthier-Commelin 2025, only for `H3` or certificate packaging

Framing guard:
- The active `H1` label is `Cross-family canonical obstruction atlas for failed 42 -> 43 extensions in R(5,5)`.
- All outward-facing first sentences must contain `R(5,5)` and the concrete object under study (`obstruction atlas`, `decomposition primitive`, or `certificate reuse`).
- The lexical watchlist is evidence of query noise only, not substantive prior art.

## 1. Route Arbitration

Primary source anchors:
- `results/swarm/hypotheses.json`
- `results/swarm/tool_plan.md`
- `results/swarm/director_brief.md`
- `results/swarm/gap_map.md`
- `results/swarm/falsifier.md`

Operational decision:
- Keep `H1` as champion. The local swarm materials agree that the only credible novelty moat is a reusable obstruction object extracted from failed `42 -> 43` extensions, not another optimizer or another solver narrative.
- Keep `H2` as backup only. It opens only if `H1` fails transfer or witness-safety gates.
- Keep `H3` as reserve only. It is infrastructure unless attached to a structural object from `H1` or a genuinely new decomposition primitive from `H2`.
- Phrase `H1` as an object claim, not as a new one-vertex extension algorithm or an emptiness checker.

Explicit kill criteria:
- `H1`: kill if minimal obstruction cores do not recur across orbit-distinct parents, fail leave-one-parent-out transfer, or kill any known `42`/`43` witness during witness-safety audits.
- `H2`: kill if adjacent-pair, nonadjacent-pair, or shell-based decompositions do not beat the split-vertex/transverse-edge gluing baseline on residue size, proof bytes, or checker runtime under matched solver and proof-logging conditions.
- `H3`: kill or demote to infrastructure if extracted canonical cores fail held-out transfer, become encoding-specific, or increase checked proof cost more than they prune.

## 2. Baseline Matrix

| Planned activity | Existing utility or artifact | Expected output | Current blocker |
| --- | --- | --- | --- |
| Ramsey literature refresh | `.archivara/semantic_scholar.py`, `results/literature/literature_snapshot.json`, `results/literature/semantic_scholar_manifest.json`, `results/swarm/phase1_cleanup.md` | Fixed Ramsey corpus, ranked reading order, and frontier notes | No widening allowed until the fixed corpus is exhausted |
| Concept branching and route expansion | `.archivara/concept_evolve.py`, `results/concept_evolve/tree/` | Cross-domain concept cards, promoted folders, walk paths | First-pass tree exists locally; further branching is gated by `Rung 0` frontier reconstruction |
| Route arbitration | `results/swarm/director_brief.md`, `results/swarm/hypotheses.json`, `results/swarm/tool_plan.md`, `results/swarm/falsifier.md` | Fixed `H1/H2/H3` ordering with explicit stop rules | None |
| Lower-bound baseline definition | Exoo 1989, Ge et al. 2022, Lehavi 2024, `results/literature/gap_probe_1.json`, `results/swarm/phase1_cleanup.md` | Witness standards, search-effort normalization, failure log schema | No repo-local `frontier_parent` corpus, witness enumerator, or verifier exists yet |
| Upper-bound baseline definition | McKay-Radziszowski 1992, Angeltveit-McKay 2018 and 2024, Gauthier 2025 | Residue/certificate metrics and matched-baseline comparison plan | No repo-local proof checker or residue reducer exists yet |
| Novelty differentiation | `results/literature/prior_art_gap.md`, `results/literature/prior_art_watchlist.md`, `results/literature/novelty_guard.json`, `results/swarm/phase1_cleanup.md` | Closest-overlap notes, lexical-noise exclusions, and branch-kill decisions | Keep lexical watchlist out of baseline and novelty claims |
| Citation packaging | `sources.bib`, `results/verification/citation_audit.md` | Complete bibliography and claim-to-source coverage | `sources.bib` absent at run start |
| Final verification routing | `results/verification/novelty_report.md`, `results/verification/benchmark_report.md`, `results/verification/verification_summary.md` | Publishability gate and no-go documentation | Verification directory empty at run start |

Indispensable missing-tool blockers to log rather than implement ad hoc:
- No existing repo utility materializes the `frontier_parent` / `extension_case` / `failure_witness` corpus required for `Rung 0`.
- No existing repo utility enumerates orbit-distinct `42 -> 43` extensions.
- No existing repo utility independently verifies a `44`-vertex witness.
- No existing repo utility checks a machine-readable `45`-vertex impossibility certificate.

## 3. Lower-Bound Baseline Metrics

Lower-bound work counts as progress only if it yields an independently verified `44`-vertex witness. All lower-bound experiments must track:

1. Witness recovery rate from neutral random starts, not only Exoo-like seeds.
2. Family diversity: how many non-isomorphic parent families beyond Exoo-style constructions contribute candidate improvements.
3. Witness-safety under filters: every pruning rule must be audited against all known `42`- and `43`-vertex witnesses.
4. Equalized search effort: edge flips, neighborhood evaluations, SAT/LP calls, and CPU budget must be normalized before comparing methods.
5. Failure-mode logging: each run records the exact reason for failure, including overfit seeds, unsound filters, and transfer collapse.
6. Structural transfer score: recurring obstruction cores must generalize across held-out parent families rather than only improving proxy defect values.

## 4. Upper-Bound Baseline Metrics

Upper-bound work counts as bound progress only if it yields a machine-checkable proof that `45`-vertex colorings are impossible.
A residue with a clear certificate path counts only as `improves certificate path` or intermediate evidence. All upper-bound experiments must track:

1. Residue size after decomposition and pruning.
2. Proof bytes or certificate size.
3. Checker runtime on the emitted proof or residue certificate.
4. Exactness or rationalization status of every claimed impossibility step.
5. Matched-baseline runtime against the current split-vertex/transverse-edge gluing line.
6. Transferability of learned obstruction or kernel artifacts across decomposition families.

Upper-bound comparison protocol:
- A `clear certificate path` requires a machine-readable residue, residue hash, remaining-open-case count, target proof format, checker name and version, and an exact replay plan.
- Every benchmark row must log a fixed matched-compute tuple: solver binary and version, proof format, preprocessing passes, thread count, hardware class, timeout policy, branch-order policy, random-seed policy, and warm-start or cached-clause policy.
- Warm starts, oracle seeds, cached clauses, proof reuse, and hand-picked symmetry priors are allowed only if enabled symmetrically for both baseline and candidate.
- The upper-bound win rule is fixed in advance as `bound status > certificate class > verified residue size > proof bytes > checker runtime`.
- No headline claim survives a regression on a higher-priority metric.
- Every upper-bound artifact must be replayed outside the generating workflow, with input hash, artifact hash, checker version, and pass/fail result recorded.
- Every upper-bound primitive must reproduce at least one solved smaller certificate case before it is trusted on `R(5,5)`.

## 5. Concept-Tree Operating Rules

Required ConceptEvolve sequence:
- Completed in Phase 1: `.archivara/concept_evolve.py evolve "Improve the Ramsey number R(5,5) bound"` and `.archivara/concept_evolve.py walk`.
- Entering core research, run `.archivara/concept_evolve.py probe "<biggest open question>"`.
- Entering experiments, run `.archivara/concept_evolve.py reframe "Improve the Ramsey number R(5,5) bound"`.
- After verification artifacts exist, run `.archivara/concept_evolve.py iterate "Improve the Ramsey number R(5,5) bound"`.

Concept-drift guard:
- No further concept branching occurs until `Rung 0` materializes the `frontier_parent`, `extension_case`, and `failure_witness` schema.

Acceptance floor for the concept tree:
- At least 10 folders under `results/concept_evolve/tree/`.
- Each promoted folder must contain a concrete experiment seed.
- Each promoted folder must name the closest prior art.
- Each promoted folder must map explicitly to `H1`, `H2`, or `H3`.

## 6. Champion `H1` Program Specification

`H1` must be described as an object, not a mechanism:
- Do not call it a new one-vertex extension algorithm.
- Do not call it an improved lower-bound search.
- Do not call it an emptiness checker for `R(5,5,43)`.
- Call it a cross-family canonical obstruction atlas for failed `42 -> 43` extensions in `R(5,5)`.

Canonical `H1` data model:
- `frontier_parent`: a known `42`-vertex critical coloring, with automorphism metadata, orbit partition, degree profile, and provenance.
- `extension_case`: an orbit-distinct proposal for a `42 -> 43` one-vertex extension.
- `failure_witness`: the exact local pattern that forces a monochromatic `K_5`.
- `minimal_obstruction_core`: a canonicalized minimal witness extracted from one or more failed extensions.
- `transfer_record`: a held-out-family evaluation of whether the same obstruction core recurs and remains sound.

Input artifacts:
- Known `42`-vertex frontier colorings and their canonical metadata.
- Orbit-distinct `42 -> 43` extension records.
- Known `43`-vertex witnesses for witness-safety checks.

Output artifacts:
- Obstruction atlas table.
- Core-frequency summary.
- Leave-one-parent-out transfer sheet.
- Witness-safety audit sheet.
- Reusable forbidden-pattern candidate library.

Falsifiable `H1` claims:
- Recurrence claim: a small dictionary of obstruction cores covers a nontrivial fraction of failed extensions across multiple parent families.
- Transfer claim: the cores survive leave-one-parent-out evaluation.
- Reuse claim: the same cores are useful both as lower-bound pruning objects and as upper-bound lemma candidates.

## 7. `H1` Transfer, Soundness, and Stop Rules

Mandatory `H1` checks before any scale-up:
- Leave-one-parent-out transfer on all known parent families.
- Witness-survival audit on every known `42`- and `43`-vertex witness.
- Family-balance audit to ensure the atlas is not just an Exoo-lineage memorizer.
- Filter-ablation audit: remove each pruning rule independently and confirm no hidden unsoundness.
- Do not report pruning gains, SAT-clause reuse, or upper-bound lemma reuse as a structural advance before the transfer and witness-safety checks pass.

Pivot rule:
- Open `H2` only after `H1` fails recurrence or transfer on held-out families, or after witness-safety detects unsound pruning.

## 8. Bounded `H2` and `H3` Routes

Allowed `H2` decomposition primitives:
- Adjacent-pair split: decompose around two adjacent anchor vertices rather than one.
- Nonadjacent-pair split: decompose around two nonadjacent anchors to expose different residue symmetry.
- Small-shell decomposition: use a forced `K_4` shell or an independent-4 shell to define a stronger case partition.

`H2` non-equivalence gate:
- Before any benchmark, each candidate primitive must state why it is not reducible to split-vertex or transverse-edge gluing plus a different branching order.
- If that statement is weak or purely rhetorical, kill `H2` early.

`H2` success criteria:
- Smaller verified residue than split-vertex/transverse-edge gluing.
- Smaller proof footprint under the same solver/proof-logging setup.
- Faster checker runtime on matched benchmark rungs.

`H2` non-claims:
- It does not get credit for a faster SAT engine alone.
- It does not get credit for smaller branch counts without certificate improvements.

Allowed `H3` attachment:
- Canonical obstruction certificates extracted from failed `H1` or `H2` branches and reused across later branches.

`H3` non-route:
- No standalone `H3` track proceeds before `H1` or `H2` yields a transferable structural object.

`H3` evaluation baselines:
- Formal `R(4,5) = 25` proof practice.
- Lean formalization work on Ramsey theory and `R(4,5) = 25`.

`H3` credit rule:
- `H3` gets structural credit only if transfer survives cross-branch or cross-family tests and checked proof size or checker runtime decreases.

## 9. Exact Experiment Ladder

The first exact ladder must start with the fastest invalidators from `results/swarm/falsifier.md`.

Rung 0: frontier reconstruction pass
- Goal: reconstruct the Exoo/Ge/Lehavi one-vertex-extension setting and materialize the canonical `frontier_parent`, `extension_case`, and `failure_witness` schema.
- Expected artifact: frontier corpus table, extension-case schema, and failure-witness schema with provenance fields.

Rung 1: `H1` atlas pass
- Goal: build the parent/extension/failure-core schema on the smallest decisive frontier set.
- Expected artifact: obstruction atlas draft plus core canonicalization rules.

Rung 2: held-out transfer pass
- Goal: test whether recurring cores generalize beyond the parent families used to mine them.
- Expected artifact: leave-one-parent-out transfer table with pass/fail labels.

Rung 3: witness-safety pass
- Goal: verify that no obstruction rule deletes a known witness.
- Expected artifact: witness-survival matrix and unsound-filter log.

Expansion gate:
- No wider compute is authorized before all three rungs pass cleanly.

## 10. Prior-Work Comparison Matrix

Every evaluation table must include the following named rows:
- Exoo 1989 lower-bound line.
- Ge et al. 2022 `Study of Exoo's Lower Bound for Ramsey number R(5,5)`.
- Lehavi 2024 `Ramsey Number Counterexample Checking and One Vertex Extension Linearly Bound by s and t`.
- Aija'am 2010 `Can genetic algorithms with the symmetric heuristic find the Ramsey number R(5,5)`.
- McKay-Radziszowski 1992 `A new upper bound on the Ramsey number R(5,5)`.
- Angeltveit-McKay 2018 `R(5,5) <= 48`.
- The `R(5,5) <= 46` line.
- Gauthier 2025 `Decreasing the upper bound on the Ramsey number R(5,5)`.

`H3`-specific evaluation tables must also include:
- The formal `R(4,5) = 25` certificate line.
- The Lean formalization line for Ramsey theory and `R(4,5) = 25`.

Every row must include:
- comparison object
- baseline artifact
- matched compute condition
- result type: `improves bound`, `improves certificate path`, or `improves neither`

## 11. Verification Artifact Ownership

| Artifact | Owner role | Required content |
| --- | --- | --- |
| `results/verification/novelty_report.md` | `novelty_checker` | Closest Ramsey overlap, differentiation test, active hypothesis, bound-moving threshold |
| `results/verification/citation_audit.md` | `citation_auditor` | Claim-to-source coverage, bibliography gaps, active hypothesis, bound-moving threshold |
| `results/verification/benchmark_report.md` | `benchmark_auditor` | Equalized baselines, certificate metrics, artifact checks, active hypothesis, bound-moving threshold |
| `results/verification/verification_summary.md` | parent synthesis | Cross-reference of all three specialist reports plus final go/no-go status |

## 12. Compute Governance and Anti-Proxy Rules

| Stop condition | Meaning | Action |
| --- | --- | --- |
| Proxy-only gain | Better defect, branch count, or SDP size without a witness/certificate path | Roll back the claim to intermediate evidence only |
| Unsound pruning | A filter kills any known witness or lacks a soundness argument | Shut down that branch immediately |
| Non-transfer | Obstruction cores or kernels fail held-out-family tests | Kill `H1` or demote `H3` to infrastructure |
| Missing certificate path | Upper-bound residue cannot be rationalized or checked | Block any bound-improvement claim |
| Stale baseline | New method is compared to a weaker or mismatched baseline | Re-audit before proceeding |
| Overfit seed family | Gains disappear off Exoo-like seeds or favored symmetry priors | Demote to overfit heuristic evidence |

## 13. Claim Grammar

Allowed claim classes:
- Bound improvement: an independently verified `44`-vertex witness or a machine-checkable `45`-vertex impossibility proof.
- Structural intermediate result: a transferable obstruction atlas, decomposition primitive, or certificate object with passed transfer and soundness audits.
- Negative result: a hypothesis killed by explicit stop rules, with artifacted failure evidence.
- Infrastructure-only result: a tool, proof package, or dataset that improves reproducibility without moving the bound.

Forbidden phrasings:
- Do not present lower defect, better search trajectories, or more branches pruned as a bound improvement.
- Do not present a smaller residue without a certificate path as an upper-bound improvement.
- Do not present a residue with a certificate path but without a checked `45`-vertex impossibility proof as a bound improvement; that is at most `improves certificate path`.
- Do not present proof logging alone as structural novelty.
- Do not blur heuristic impossibility evidence into a proof of impossibility.

Wording constraints:
- `H1` wording must include `R(5,5)`, `failed 42 -> 43 extensions`, `minimal obstruction cores`, and either `held-out transfer` or `witness-safety`.
- `H2` wording must name the exact decomposition primitive and at least one certificate metric such as verified residue size, proof bytes, or checker runtime.
- `H3` wording must say that it is attached to `H1` or `H2` and must name the reuse test: cross-branch, cross-family, or orbit-stable transfer.
- Run a lexical scrub on every outward-facing title, abstract, and comparison table. If the first sentence does not contain `R(5,5)` and the concrete Ramsey object, rewrite it.
