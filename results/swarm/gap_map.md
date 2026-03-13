# Gap Map: Negative Space Around Improving `R(5,5)`

Date: 2026-03-13
Mode: repo-local synthesis only
Working frontier: `43 <= R(5,5) <= 46`

## Scope

- Required inputs were read first: `results/research_context.md`, `results/literature/prior_art_watchlist.md`, `results/literature/prior_art_gap.md`, and `results/literature/gap_frontier.md`.
- This refresh stayed inside the existing repo packet. No new web sweep or broad Semantic Scholar search was used.
- Ranking rule: prefer missing structural objects, transfer tests, and certificate paths over popular optimizer or solver stories.

## Ranked Gaps

### 1. Cross-family canonical obstruction atlas for failed `42 -> 43` extensions

- Route: `H1`
- Why it is genuinely under-served:
  The workspace keeps converging on the same missing object, but it still does not exist locally: a canonical `frontier_parent` / `extension_case` / `failure_witness` corpus plus a mined atlas of recurring minimal obstruction cores. The frontier is described, not structurally compressed.
- What it should not be confused with:
  Not Exoo re-verification, not another one-vertex-extension checker, and not a better low-defect search loop.
- Concrete failure mode:
  Without a shared obstruction atlas, every lower-bound or proof-oriented branch re-learns the same `42 -> 43` failures from scratch and cannot tell recurrence from lineage-specific noise.
- Entry experiment / kill test:
  Run `Rung 0/1` only. If the top-25 canonical cores fail to cover at least 30 percent of failed orbit-distinct extensions across at least 3 non-isomorphic parent families, or held-out coverage collapses on the anti-Exoo family, kill the route.

### 2. Anti-Exoo holdout and deliberately asymmetric parent families

- Route: `H1` evaluation setting
- Why it is genuinely under-served:
  The local falsifier repeatedly warns that Exoo-lineage parents and symmetry-favored starts can masquerade as structure. The missing setting is not "more search"; it is a hostile evaluation regime where Exoo-like families are held out and asymmetric perturbations are first-class inputs.
- What it should not be confused with:
  Not the older symmetric-heuristic GA line, not curated near-miss optimization, and not seed engineering dressed up as discovery.
- Concrete failure mode:
  A purported obstruction library or search heuristic may merely memorize one parent lineage and collapse the moment favored symmetry priors disappear.
- Entry experiment / kill test:
  Recover known `42`- and `43`-vertex witnesses from neutral random starts plus deliberately asymmetric parent families. If success disappears off Exoo-like seeds or held-out families, demote the route to overfit heuristic evidence.

### 3. Witness-safe upper-bound filter bank inside constructive lower-bound search

- Route: bridge attached to `H1`
- Why it is genuinely under-served:
  The lower-bound and upper-bound lines are still siloed in the local materials. Cheap upper-bound necessities such as degree admissibility, neighborhood profiles, LP-feasible count vectors, and small gluing impossibility templates are not yet organized as a witness-safe live filter bank for constructive search.
- What it should not be confused with:
  Not an upper-bound proof, not heuristic evidence of impossibility, and not pruning justified only by imported SAT or LP terminology.
- Concrete failure mode:
  Constructive search keeps revisiting regions that the upper-bound line already knows are impossible, while any unsound imported filter risks deleting a real witness.
- Entry experiment / kill test:
  Add only the cheapest necessary conditions as rejection or scoring oracles, then run full witness-survival and filter-ablation audits. If any known `42`- or `43`-vertex witness is lost, shut the bridge down immediately.

### 4. Decomposition-primitive replacement beyond split-vertex and transverse-edge gluing

- Route: `H2`
- Why it is genuinely under-served:
  The current upper-bound bottleneck looks structural rather than purely computational. The popular route keeps the same split/gluing language and swaps in a stronger solver, better branch order, or better clause learning. The missing question is whether a genuinely different proof object shrinks the exact residue.
- What it should not be confused with:
  Not "same decomposition, better SAT," not IC3/PDR/CEGAR on the existing state space, and not residue laundering where the hard cases are handed back to the old pipeline.
- Concrete failure mode:
  Case explosion survives because the decomposition primitive is too weak, so solver improvements only compress the easy part of the tree.
- Entry experiment / kill test:
  Benchmark adjacent-pair, nonadjacent-pair, and small-shell decompositions on a solved smaller certificate rung under a fixed matched-compute tuple. Kill any candidate that cannot clear the non-equivalence gate or improve verified residue size, proof bytes, or checker runtime.

### 5. Replayable canonical obstruction certificates from failed exact branches

- Route: `H3` attachment only
- Why it is genuinely under-served:
  The workspace has proof logs and failed branches, but not a reusable library of canonical obstruction certificates that survive branch changes, family changes, and proof-format replay. Exact computation is still mostly one-shot.
- What it should not be confused with:
  Not generic proof logging, not formal packaging by itself, and not encoding-specific clause reuse.
- Concrete failure mode:
  Dead branches remain archived solver debris instead of becoming reusable forbidden-partial-coloring lemmas, so later runs pay the same proof cost again.
- Entry experiment / kill test:
  On one verified smaller rung, extract a canonical UNSAT core or forbidden-pattern lemma from a failed branch and replay it in a disjoint branch family and proof format. If it does not transfer or does not reduce checked proof cost, keep it as infrastructure only.

## Why These Five

- They are the least crowded parts of the current `R(5,5)` workspace.
- Each one names a concrete missing object, hostile evaluation setting, or stop rule.
- Each one has a fast falsifier, which keeps the program from drifting into optimizer theater, solver theater, or proxy-metric inflation.

## Deprioritized For This Pass

- Plain GA, simulated annealing, RL, rare-event sampling, or defect minimization without a reusable obstruction object.
- Plain LP, flag, SDP, Terwilliger, or spectral tightening without an exact finite-`n` certificate path.
- Solver-only retellings of the current split-vertex or transverse-edge gluing line.

## Working Thesis

If `R(5,5)` moves from the current frontier, the most credible path is still structural compression of the exact frontier and the proof endgame, not a better generic search or a faster generic solver. The top under-served targets are therefore:

1. the missing obstruction atlas,
2. the anti-Exoo transfer setting,
3. the witness-safe filter bridge,
4. a genuinely new decomposition primitive, and
5. replayable obstruction certificates.
