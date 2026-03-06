# Tool Plan

- Mission: support the `H1` champion and `H2` backup in `results/swarm/hypotheses.json` without drifting into broad, low-yield literature search.
- Source order of operations:
  1. `results/research_context.md`
  2. `results/literature/prior_art_watchlist.md`
  3. `results/literature/prior_art_gap.md`
  4. `results/literature/gap_frontier.md`
  5. `results/swarm/gap_map.md`
  6. `results/swarm/falsifier.md`
  7. `results/swarm/hypotheses.json`
  8. `results/swarm/director_brief.md`

## Governance

- Spend the first budget on planning, synthesis, benchmark design, and claim-sharpening.
- Treat broad `semantic_scholar.search` as disallowed by default; only use targeted validation after existing artifacts are exhausted.
- Prefer watchlist, gap frontier, and swarm outputs over new external search.
- Any external query must name the exact invalidation branch it is testing, not the generic task string.
- Kill any direction whose remaining claim is only `minimal`, `interactive`, `web-based`, or `from scratch`.

## Global Budget Envelope

- `60%` local synthesis and claim pruning.
- `25%` benchmark and falsification design.
- `15%` targeted citation validation.
- `0%` broad literature expansion unless the orchestrator explicitly opens an exception.

## Role Routing

### Orchestrator

- Primary tools: `read`, `glob`, `grep`, `todowrite`.
- Route: gather existing artifacts, keep the claim narrow, and authorize external search only when a concrete novelty or citation risk remains unresolved.
- Budget envelope: `85%` local synthesis, `15%` coordination, `0` broad external searches.
- Escalation trigger: one unresolved yes-or-no question about whether the champion angle already exists in lightweight audited form.

### Researcher

- Primary tools: `read`, `grep`, `semantic_scholar.search`, `semantic_scholar.graph`.
- Route: mine the watchlist, gap files, and falsifier first; then run narrow validation against the champion or backup only.
- Budget envelope: up to `3` targeted Semantic Scholar queries for `H1`, plus `1` extra only if `H2` is activated.
- Preferred query shapes:
  - `gravity simulator energy conservation benchmark`
  - `browser WASM orbit simulator determinism`
  - `minimal n-body close encounter integrator`

### Falsifier

- Primary tools: `read`, `grep`, targeted `semantic_scholar.search`.
- Route: attack the selected direction using the literature branches already named in `results/swarm/falsifier.md` before opening any new branch.
- Budget envelope: up to `2` targeted invalidation queries, `0` graph wandering, `0` broad search.
- Required checks: educational orbit simulators, REBOUND-like audited baselines, and hobby/student demos that might erase the novelty claim.

### Writer

- Primary tools: `read`.
- Route: write only from accepted evidence and benchmark commitments already cleared by the orchestrator and reviewer.
- Budget envelope: `100%` synthesis, `0` external search.
- Constraint: no novelty language without a named control, baseline, or benchmark artifact.

### Reviewer

- Primary tools: `read`, `grep`.
- Route: strip cosmetic novelty, enforce scope discipline, and ensure every claim maps to a falsifier or evidence item.
- Budget envelope: `100%` local review, `0` external search unless a claim cannot be supported or cut.
- Required red flags: `textbook exercise`, `thin clone of REBOUND`, `pretty orbit demo`, and `educational sandbox` language.

### Citation Auditor

- Primary tools: `read`, `semantic_scholar.search`, `semantic_scholar.bibtex`.
- Route: verify only the specific papers, tools, and software branches that end up cited in the brief and benchmark write-up.
- Budget envelope: up to `2` metadata checks and `2` BibTeX pulls; no open-ended search.
- Priority targets: REBOUND, poliastro, the educational two-body branch, and any direct benchmark or determinism source used to defend `H1`.

### Benchmark Auditor

- Primary tools: `read`, `bash`.
- Route: convert research claims into executable gates and reject directions that cannot be benchmarked cleanly.
- Budget envelope: `70%` local benchmark design and execution, `30%` baseline plumbing, `0` literature search by default.
- Mandatory gates for `H1`: analytic two-body controls, invariant drift, timestep convergence, reference baseline agreement, and cross-runtime reproducibility.
- Mandatory gates for `H2`: close-encounter stress tests, epsilon sensitivity, policy ablations, and explicit failure-envelope reporting.

## Exception Policy

- Allow a broad Semantic Scholar search only if targeted queries still cannot answer a single decisive novelty question.
- If an exception is opened, cap it at `1` broad query and route the result straight back through the falsifier before any new writing begins.
