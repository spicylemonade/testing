# Tool Plan

Date: 2026-03-13
Task: Improve the Ramsey number `R(5,5)` bound
Mode: synthesis-only, execution-gated

## Global Routing

- Champion route: `H1` orbit-stable extension-obstruction atlas for lifting `42`-vertex frontier colorings.
- Backup route: `H2` decomposition-primitive upgrade beyond split-vertex and transverse-edge gluing.
- Reserve route: `H3` proof-carrying reusable obstruction certificates from failed exact branches.
- Bound-moving thresholds are strict:
  - only an independently verified `44`-vertex witness counts on the lower-bound side
  - only a machine-checkable `45`-vertex impossibility proof, or a residue with a clear certificate path, counts on the upper-bound side
- Route novelty decisions through the Ramsey-specific local artifacts, not the noisy generic watchlist:
  - `results/literature/prior_art_gap.md`
  - `results/literature/gap_probe_1.json`
  - `results/swarm/gap_map.md`
  - `results/swarm/falsifier.md`
- `results/swarm/hypothesis_bridge.md` and `results/swarm/hypothesis_negative_space.md` were absent at synthesis time. Treat `gap_map.md` as the operative substitute unless the orchestrator later restores those files.
- Under synthesis-only governance:
  - do not run new experiments, benchmark scripts, ILPs, LPs, theorem searches, or constructive exploration
  - do not create new solver, notebook, scratch, or helper artifacts
  - do not widen literature search unless a concrete blocker forces one narrowly targeted verification

## Orchestrator

- Route:
  - keep the team on `H1` first
  - switch to `H2` only if `H1` fails transfer or witness-safety gates
  - unlock `H3` only as an attachment to `H1` or `H2`, never as a standalone first-line direction
- Allowed tools and work products:
  - repo inspection with `rg`, `sed`, `jq`, and `git diff`
  - synthesis-only markdown or JSON updates in `results/swarm/`
  - blocker logs and routing decisions
- Stop conditions:
  - a claim depends on a missing scout artifact
  - novelty collapses into an imported-engine story
  - the task would require writing new exploration code during synthesis-only mode
- Budget envelope:
  - one synthesis cycle
  - zero broad web or literature sweeps
  - at most one blocker-clarification check

## Researcher

- Route:
  - execute only the next exact experiment attached to the chosen hypothesis
  - use existing helper scripts and existing repo tooling only
  - if the needed tool does not already exist, stop and escalate rather than creating new exploration code inside this stage
- Allowed tools and work products:
  - canonicalization logs
  - obstruction tables
  - benchmark configurations
  - proof artifacts and result summaries
- Stop conditions:
  - `H1`: leave-one-parent-out transfer fails, or any mined obstruction kills a known witness
  - `H2`: no decomposition primitive beats the split-vertex baseline on certificate metrics
  - `H3`: extracted canonical cores fail held-out transfer or increase checked proof cost more than they prune
- Budget envelope:
  - `H1`: one atlas pass, one held-out transfer pass, one witness-safety pass
  - `H2`: two to three decomposition prototypes on verified ladder rungs before any `n=45` residue
  - `H3`: one canonical-core transfer audit on a verified ladder only

## Falsifier

- Route:
  - apply the fastest invalidators before any compute expansion
  - demand proof of transfer, soundness, and exactness before accepting any structural claim
- Allowed tools and work products:
  - known witness sets
  - held-out parent families
  - exact filter audits
  - benchmark comparison sheets
- Stop conditions:
  - no direct path to a verified `44` witness or a certificate-bearing `45` impossibility claim
  - no transfer beyond Exoo-like families
  - unsound pruning
  - proxy-metric-only gains
- Budget envelope:
  - run the five fast invalidators already listed in `results/swarm/falsifier.md`
  - stop at the first decisive failure

## Writer

- Route:
  - document only what survives falsification and has a clear witness or certificate path
  - state non-claims explicitly
- Allowed tools and work products:
  - `results/swarm/hypotheses.json`
  - `results/swarm/director_brief.md`
  - comparison tables and scoped handoff notes
- Stop conditions:
  - any novelty sentence lacks a closest-overlap anchor
  - any progress claim is really a proxy metric
- Budget envelope:
  - one draft
  - one revision
  - no fresh literature mining

## Reviewer

- Route:
  - perform findings-first review on novelty, falsifiability, and scope control
- Allowed tools and work products:
  - repo diff review
  - claim-versus-source comparison
  - short risk memo
- Stop conditions:
  - undefined falsifier
  - unclear stop rule
  - overlap with the watchlist or falsifier report remains too heavy
- Budget envelope:
  - one review pass per artifact set
  - block merge until both the champion and backup remain defensible

## Citation Auditor

- Route:
  - anchor every novelty claim to the Ramsey-specific local sources before any external verification
- Allowed tools and work products:
  - `results/literature/prior_art_gap.md`
  - `results/literature/gap_probe_1.json`
  - `results/swarm/gap_map.md`
  - `results/swarm/falsifier.md`
  - a short missing-source note if a claim still lacks a local anchor
- Stop conditions:
  - a claim leans on the noisy generic watchlist
  - the closest prior art is missing or too vague
  - a method label is cited in place of the actual overlap source
- Budget envelope:
  - repo-local audit first
  - at most three narrowly targeted source checks only if a blocker remains

## Benchmark Auditor

- Route:
  - audit equalized baselines and certificate metrics, not branch counts or defect scores alone
- Allowed tools and work products:
  - verified benchmark ladder
  - proof bytes
  - checker runtime
  - witness-safety reports
  - equalized compute tables
- Stop conditions:
  - mismatched baselines
  - unverified residue claims
  - no machine-checkable artifact path
- Budget envelope:
  - audit the first exact ladder rung before any larger run
  - authorize wider compute only after one clean pass

## Explicit Non-Routes

- Do not propose plain GA, simulated annealing, RL, rare-event sampling, or multicanonical search as standalone novelty.
- Do not propose generic flag, SDP, Terwilliger, spectral, or finite-stability tightening without an exact finite-`n` rigidity statement and certificate path.
- Do not propose IC3, PDR, clause learning, or CEGAR on the same split-vertex or transverse-edge decomposition as the main novelty claim.
- Do not treat lower defect, fewer branches, smaller relaxations, or cleaner heuristics as a bound improvement.
