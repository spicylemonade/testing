# Research Context

Date: 2026-03-13
Stage: phase_5_final_review
Task: Improve the Ramsey number `R(5,5)` bound

## Current State

- Rubric progress: `25/25` completed
- Active hypothesis: `H1` = `Cross-family canonical obstruction atlas for failed 42 -> 43 extensions in R(5,5)`
- Route status: `H1` champion, `H2` backup only, `H3` attachment-only infrastructure
- Current frontier target: `43 <= R(5,5) <= 46`
- Bound-moving threshold: independently verified `44`-vertex witness or machine-checkable `45`-vertex impossibility proof
- Current claim ceiling: constrained no-go memo only; `H1` remains a route target until the fixed `H1` acceptance contract and the `results/h1/*` artifact requirements are satisfied
- `sources.bib` entries: `18`
- Verification packet present: yes
- Final review present: yes

## Major Route Changes

### 2026-03-13: Lexical Watchlist Demoted, Fixed Ramsey Corpus Adopted

- Chosen hypothesis: keep `H1` as champion.
- Trigger artifact: `results/swarm/phase1_cleanup.md`
- Active blockers at the time: no local `frontier_parent` corpus, no orbit-distinct `42 -> 43` enumerator, no independent witness verifier, no certificate checker.
- Differentiation notes:
  - Against Ge et al. 2022: the run does not stop at re-verifying Exoo-line witnesses or cataloging low-defect near misses; it targets transferable minimal obstruction cores across parent families.
  - Against Aija'am 2010: the run does not claim novelty from a better optimizer, better symmetry handling, or better defect minimization.
  - Against the lexical watchlist: `Senolytics`, `GWAS`, `robotic grasping`, and `EPR effect` entries are query-noise only and excluded from real prior-art comparison.

### 2026-03-13: Stress Test Demoted `H2` And `H3`

- Chosen hypothesis: keep `H1` under explicit recurrence, transfer, and witness-safety thresholds.
- Trigger artifact: `results/swarm/phase3_stress_test.md`
- Active blockers at the time: still missing `frontier_parent` corpus, extension enumerator, independent `44`-vertex verifier, and `45`-vertex certificate checker.
- Differentiation notes:
  - Against Lehavi 2024: `H1` uses the one-vertex-extension surface area as an input regime, not as the novelty claim itself.
  - Against Angeltveit-McKay 2024 and Gauthier 2025: `H2` remains inactive unless it can state and validate a genuinely different decomposition primitive instead of stronger execution on the same split/gluing line.
  - Against proof-engineering work such as Gauthier-Brown 2024 and Barakeel-Gauthier-Commelin 2025: `H3` is not a standalone novelty route and receives credit only as an attachment to a transferable structural object.

### 2026-03-13: Evaluation Rehearsal Locked A No-Go Ceiling

- Chosen hypothesis: keep `H1`, but authorize only `Rung 0` reconstruction plus the bounded Phase 4 ladder as intermediate structural work.
- Trigger artifacts:
  - `results/verification/evaluation_rehearsal.md`
  - `results/verification/verification_summary.md`
- Active blockers now:
  - local `frontier_parent` corpus
  - orbit-distinct `42 -> 43` extension enumerator
  - independent `44`-vertex witness verifier
  - `45`-vertex certificate checker
  - missing `results/h1/*` evidence artifacts for the fixed `H1` acceptance contract
- Differentiation notes:
  - Against Ge et al. 2022 and Exoo-line work: no structural claim is allowed unless obstruction recurrence transfers across held-out parent families.
  - Against Lehavi 2024: the project cannot describe itself as an OVE or emptiness-checking advance without collapsing into prior work.
  - Against upper-bound lines from McKay-Radziszowski 1992 through Gauthier 2025: smaller residues, proof plumbing, or faster branching are not bound movement without a certificate path and a checked `45`-vertex impossibility proof.

## Active Blockers

- No repo-local `frontier_parent` / `extension_case` / `failure_witness` corpus for `Rung 0`
- No orbit-distinct `42 -> 43` extension enumerator
- No independent `44`-vertex witness verifier
- No machine-readable `45`-vertex certificate checker
- No `results/h1/*` evidence artifacts yet exist, so `H1` is still a route target rather than an achieved structural contribution

## Memo-Safe State

- Safe memo type now: constrained no-go or planning memo only
- Not safe to claim now: bound improvement, achieved `H1` structural intermediate result, or material novelty over Lehavi 2024 on evidence
- Authoritative gate: `results/verification/h1_acceptance_contract.md`

## Nearest Real Prior Art

- Ge et al. 2022: closest lower-bound structural overlap
- Lehavi 2024: closest one-vertex-extension and counterexample-checking overlap
- Angeltveit-McKay 2024 `R(5,5) <= 46`: current upper-bound frontier source of truth
- Gauthier 2025: closest split-vertex/transverse-edge gluing successor for any `H2` claim

## Canonical Memory

- Literature search memory: `results/literature/semantic_scholar_manifest.json`
- Route and kill criteria: `results/plans/phase3_route_sheet.md`
- Evaluation order and anti-proxy rules: `results/plans/phase4_evaluation_sheet.md`
- Fixed `H1` pass/fail contract: `results/verification/h1_acceptance_contract.md`
- Verification gate: `results/verification/verification_summary.md`
- Reporting policy: `results/plans/claim_grammar.md`
