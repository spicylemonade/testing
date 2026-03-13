# Tool Plan

Date: 2026-03-13
Task: Improve the Ramsey number `R(5,5)` bound
Mode: synthesis-only planning; execution remains gated

## Global Routing

- Route order:
  `H1` champion,
  `H1B` backup,
  `H2` tertiary fallback.
- Bound-moving thresholds:
  only an independently verified `44`-vertex witness counts on the lower-bound side,
  and only a machine-checkable `45`-vertex impossibility proof, or a residue with a clear certificate path, counts on the upper-bound side.
- Global stop codes:
  `anti_exoo_holdout`,
  `witness_killed`,
  `stale_baseline`,
  `missing_certificate_path`,
  `rare_core_tail`.
- Global governance:
  use the existing Ramsey corpus and existing repo tooling first;
  do not reopen broad literature search, write new exploration code, or run wide benchmark sweeps unless a named blocker forces one narrow verification.

## Orchestrator

- Route:
  keep all active planning on `H1` until the first atlas gate is decided;
  unlock `H1B` only if `H1` yields stable signatures worth abstracting;
  unlock `H2` only if `H1` or `H1B` fail decisively or if an upper-bound-first fallback is explicitly requested.
- Allowed tools and work products:
  repo inspection,
  existing helper scripts,
  routing memos,
  blocker logs,
  markdown or JSON synthesis in `results/swarm/`.
- Stop conditions:
  the next step requires writing new exploration code,
  the claim depends on a missing artifact rather than a defined blocker,
  or the route collapses into imported-vocabulary theater.
- Budget envelope:
  one routing cycle per gate,
  zero broad web or literature sweeps,
  at most one narrow blocker-clarification check.

## Researcher

- Route:
  execute only the exact next experiment attached to the active route,
  using existing repo tooling only;
  if the needed enumerator, verifier, or checker does not already exist, stop and log the blocker instead of building new tooling inside this stage.
- Allowed tools and work products:
  `frontier_parent`,
  `extension_case`,
  `failure_witness`,
  witness-survival ledgers,
  matched ablation tables,
  proof or residue manifests.
- Stop conditions:
  `H1`: coverage misses the threshold, anti-Exoo transfer collapses, or any known witness is deleted;
  `H1B`: one witness is lost or the abstract layer shows no matched pre-decomposition gain;
  `H2`: non-equivalence fails or certificate metrics do not beat the split/glue baseline.
- Budget envelope:
  `H1`: one minimal corpus build, one anti-Exoo transfer audit, one witness-safety audit;
  `H1B`: one soundness spec plus one matched on/off ablation;
  `H2`: one small solved-rung non-equivalence check plus one matched benchmark ladder before any `n = 45` residue.

## Falsifier

- Route:
  apply the fastest invalidator before any wider compute;
  force every route to survive transfer, soundness, and matched-baseline checks.
- Allowed tools and work products:
  held-out parent families,
  saved witness sets,
  filter or lemma audits,
  comparator sheets,
  failure-code memos.
- Stop conditions:
  no transfer beyond Exoo-like lineages,
  any witness loss,
  proxy-metric-only gains,
  or no certificate-bearing path to the claimed bound side.
- Budget envelope:
  run the decisive gate for the active route first and stop on the first clear failure.

## Writer

- Route:
  document only what survives the active falsifier gate;
  keep every claim at route-specification scope until an artifact path exists.
- Allowed tools and work products:
  `results/swarm/hypotheses.json`,
  `results/swarm/director_brief.md`,
  handoff notes,
  scoped comparison tables.
- Stop conditions:
  novelty lacks a closest-overlap anchor,
  scope drifts from route specification to implied result,
  or proxy metrics are presented as bound progress.
- Budget envelope:
  one draft plus one revision per gate;
  no new literature mining.

## Reviewer

- Route:
  review findings first on novelty, scope control, blocker clarity, and stop-rule quality.
- Allowed tools and work products:
  repo diff review,
  claim-versus-source audit,
  short risk memo.
- Stop conditions:
  undefined falsifier,
  undefined blocker,
  backup route overlaps too heavily with the falsifier memo,
  or attachment-only infrastructure is being sold as a main hypothesis.
- Budget envelope:
  one review pass per artifact set;
  do not clear the route if champion and backup are not both defensible.

## Citation Auditor

- Route:
  anchor every novelty sentence to the Ramsey-specific packet before asking for any external confirmation.
- Allowed tools and work products:
  `results/literature/prior_art_gap.md`,
  `results/swarm/gap_map.md`,
  `results/swarm/hypothesis_bridge.md`,
  `results/swarm/hypothesis_negative_space.md`,
  `results/swarm/falsifier.md`,
  a short missing-source note.
- Stop conditions:
  `H1` is not explicitly differentiated from Ge and Lehavi,
  `H1B` is not explicitly differentiated from cheap filters or prior degree-matrix abstractions,
  `H2` is not explicitly differentiated from McKay-Radziszowski, Angeltveit-McKay, and Gauthier,
  or a generic watchlist item is being treated as active prior art.
- Budget envelope:
  repo-local audit first;
  at most three narrow source checks only if a concrete citation blocker remains.

## Benchmark Auditor

- Route:
  audit matched baselines and certificate metrics, not branch counts, defect scores, or unlabeled residue shrinkage.
- Allowed tools and work products:
  verified ladder rungs,
  matched compute tuples,
  proof bytes,
  checker runtime,
  witness-survival reports,
  residue manifests.
- Stop conditions:
  mismatched solver or proof settings,
  no primitive-only or layer-only toggle,
  no witness-safety ledger,
  or no machine-checkable artifact path.
- Budget envelope:
  audit the first solved-rung comparison before any larger run;
  authorize wider compute only after one clean matched pass.

## Explicit Non-Routes

- Do not pitch plain GA, simulated annealing, RL, rare-event search, or defect minimization as standalone novelty.
- Do not pitch generic LP, flag, SDP, Terwilliger, or spectral tightening without an exact finite-`n` certificate path.
- Do not pitch decision diagrams, proof logging, or reusable certificates as a standalone headline route.
- Do not count fewer defects, fewer branches, or smaller unverified residues as a bound improvement.
