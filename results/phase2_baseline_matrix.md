# Phase 2 Baseline Matrix

## Metric

The primary metric for every family and every control is the exact extracted score

`S = (m(G) + |R|) / (n(G) - |T|)`.

No proxy metric is allowed to stand in for score.

Secondary diagnostics may be logged, but only alongside exact score:

- forcing success or failure under the exact verifier,
- interface mismatch count,
- rational-complexity summary of `X`,
- search budget consumed,
- transfer delta from level 1 to level 2.
- state alphabet size `|Sigma|`,
- extractor table size and serialized grammar description length.

## Active Geometry

Matched geometry for `H1` and all baselines:

- corridor family with `k = 2`,
- fixed height `H in {2,3,4}`,
- width generated either by substitution (`H1`) or by a non-CA baseline on the same `H x W` corridor.

## Baseline Rows

### 1. Direct no-CA certificate search

- Same `H`, same `W`, same `X`, same allowed `|R|`, same allowed `|T|`.
- `f_1`, `f_2`, `R`, and `T` are searched directly with no substitution grammar and no state sharing.
- Purpose: detect whether the CA grammar is doing more than imposing a search prior.

### 2. Low-height asymmetric `X` enumeration

- Enumerate small `X` with bounded coordinate height and explicit asymmetry.
- Match `|X|` and coordinate-height budgets against the CA family.
- Purpose: test whether arithmetic asymmetry in `X` alone explains any gains.

### 3. Bounded-slope controls

- Freeze a tiny nonzero slope alphabet and search only within that fixed bounded-slope regime.
- Purpose: check whether any observed pattern is merely the Tao-2025 bounded-many-slopes basin.

### 4. Slowly growing-`X` controls

- Allow `|X|` to increase with width under a pre-registered budget schedule.
- Purpose: compare fixed finite CA alphabets against the known tendency for explicit upper-bound constructions to improve when `X` grows.

### 5. Isotropic controls

- Force horizontal extractor rows to share the same pattern, or compare against the transposed corridor when valid.
- Purpose: test whether anisotropy is the real lever.

### 6. Random-label controls

- Randomize nonzero entries of `eta`, `seed_tag`, and `solved_tag` at matched densities.
- Purpose: estimate how much of the frontier is simple luck under the same budget.

### 7. Stage-order perturbation controls

- Swap the stage order when the extractor remains legal, treating the transposed family as a distinct control rather than as a quotient.
- Purpose: test whether the score gain is only an artifact of where the grammar places `f_1` versus `f_2`.

### 8. Aspect-ratio perturbation controls

- Vary `H` and `W` around the active family while keeping the search and `X` budgets matched.
- Purpose: test whether the frontier is boundary-sensitive or genuinely transferable.

### 9. Boundary-seed removal controls

- Remove or shrink the boundary-focused parts of `R` and `T` while keeping the extracted `f_i` fixed.
- Purpose: detect whether the apparent gain is mostly boundary programming.

### 10. Separate randomization ablations

- Randomize `R` only.
- Randomize `T` only.
- Randomize `X` only at matched `|X|` and coordinate height.
- Purpose: isolate which part of the pipeline carries the gain.

### 11. Exact-elimination replacement controls

- Replace any local decoding or CA surrogate ranking step with exact elimination on the same candidate set.
- Purpose: distinguish mathematical gain from search-prior gain.

### 12. Freeze-`X` scaling controls

- Hold `X` fixed while increasing `W`.
- Purpose: test whether the route survives without silently enlarging the alphabet.

## Required Matched Controls For Every Reported Result

- same `H`,
- same `W`,
- same `|X|`,
- same coordinate-height budget for `X`,
- same optimizer/search budget,
- same score formula,
- same verifier backend,
- same canonicalization policy,
- same state alphabet cap and same serialized grammar-size cap.

## Reporting Discipline

- Report frontiers over search budget and family size, not best-of-many isolated hits.
- Every table must include:
  - exact score,
  - success/failure under the exact verifier,
  - search budget,
  - `|Sigma|`,
  - extractor/grammar description length,
  - whether the candidate survived stage-order, aspect-ratio, and boundary ablations.

## Stop-Go Triggers

Go:

- only if the CA family beats the matched no-CA baseline on exact score on a frontier over budget and family size, or matches the best exact score while using no more hidden complexity and materially improving verifier-success efficiency.

Stop or pivot:

- if level-2 transfer is flat or worse than level-1;
- if exact extraction requires any global repair;
- if gains disappear under isotropic, direct-search, stage-order, aspect-ratio, boundary-seed, or randomization controls;
- if the best extracted CA family stays in a clearly bounded-slope / low-rational-complexity basin.
