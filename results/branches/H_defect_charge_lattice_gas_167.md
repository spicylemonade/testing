# H Defect-Charge Lattice-Gas 167

This branch moves from packet coordinates to the exact lag-defect field on the `167` core.

## Continuity Law

Let `rho_t(k)` be the exact signed defect coefficient at lag `k in {1, ..., 166}`.
For any accepted actuator or carrier macro-event, define `delta(k) = rho_{t+1}(k) - rho_t(k)` and `R = sum_k delta(k)`.
The branch uses an open-core continuity law with a single boundary reservoir:

`rho_{t+1}(k) - rho_t(k) = J(k-1) - J(k) + R * 1[k = 166]`,

where `J(k) = -sum_{i <= k} (delta(i) - R * 1[i = 166])` is the exact nearest-neighbor transport current.

The local rule ranks candidates by:

- nonincreasing support first,
- then smaller reservoir exchange `|R|`,
- then smaller transport span `sum_k |J(k)|`,
- then larger `l1` and max-defect reduction.

## Split / Move / Annihilation Rules

- Single-action annihilation: accept a direct move if it strictly improves the lexicographic objective.
- Conservative move: if no direct annihilation exists, inspect precomputed two-step carrier cones whose final support does not exceed the current support.
- Split then annihilate: allow a temporary support increase only inside a two-step carrier cone whose final state returns to nonincreasing support and strictly lowers the objective.

## Canonical Frontier Result

- Lattice-gas best objective: `13/2744/480`.
- Lag-greedy control: `13/2880/512`.
- Warning-field control: `13/2880/512`.
- Accepted carrier: `[['q[53]', 'q[136]'], ['q[29]', 's[29]', 'q[114]', 's[114]']]`.
- Carrier signature: support flux `0`, reservoir `|R| = 8`, transport span `1600`, `l1` gain `136`.

## Harder Control Cross-Check

- On `control_n9_hardest_pair`, the same fixed rule reaches `0/0/0`.
- The harder control improves via direct single-action annihilation, so the frontier gain is not an artifact of freezing the single-action layer everywhere.

## Promotion Verdict

- Promote the branch for this pass: it strictly improves the canonical frontier objective without introducing any detected Williamson, Turyn, Goethals-Seidel, cocyclic, or block-circulant leakage.
