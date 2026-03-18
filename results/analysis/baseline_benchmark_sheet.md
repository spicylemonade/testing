# Baseline Benchmark Sheet

Prepared for rubric `item_008`.

## H1 matched comparison

- Active branch: `Autocorrelation-Realization CA on the 167-cycle`.
- Representation: binary support vector on the exact cycle length with a fixed Hamming weight.
- Neighborhood: adjacent swaps on the same odd-cycle matching schedule used by both CA and baseline.
- Budget lock:
  - one step = one matching sweep,
  - same `budget_steps`,
  - same edge set inspected per step,
  - same accepted-move cap per phase (`phase_move_cap = 4`) for `parallel_gain_ca` and `direct_greedy`,
  - same exact verifier.
- Methods:
  - `parallel_gain_ca`: active CA rule, parallel local updates gated by local dominance and exact swap gain.
  - `direct_greedy`: matched direct-search baseline, same edge neighborhood, one best improving swap per step.
  - `random_rule_ca`: random-rule CA negative control on the same matching schedule.
  - `random_walk`: intentionally weak baseline on the same neighborhood.
- Seed sets:
  - `control_4x79`: 8 perturbed-solution seeds plus 8 random-weight seeds.
  - `target_167_weight_80`: 16 random-weight seeds plus 8 deterministic projections from the published modular seed.
- Fairness notes:
  - no method gets a richer representation than the others,
  - no method sees a weaker verifier,
  - orbit accounting uses the same dihedral canonicalization for all methods,
  - summaries are recorded both by method and by `seed_family` to expose representation leakage.

## H2 matched comparison

- Backup branch: `Defect-Transport CA lift from the 64-modular 668 seed`.
- Representation:
  - small ladder: structured `(q, s)` seeds with derived `A, B, C, D`,
  - 668 attempt: published `q` fixed, local search only in `s`.
- Neighborhood:
  - small ladder: one local `q` or `s` flip per candidate family,
  - 668 attempt: one local `s` flip per candidate.
- Budget lock:
  - one step = one parity phase of local variable flips,
  - same `budget_steps`,
  - same inspected variable set per step,
  - same accepted-move cap per phase (`phase_move_cap = 4`) for `parallel_gain_ca` and `direct_greedy`,
  - same modular verifier.
- Methods:
  - `parallel_gain_ca`: active defect-transport CA.
  - `direct_greedy`: matched non-CA local-search baseline.
  - `random_rule_ca`: random-rule CA negative control.
  - `random_walk`: intentionally weak baseline.
- Start states:
  - small ladder: [`results/artifacts/h2_control_structured_n9.json`](/home/archivara/work/repo/results/artifacts/h2_control_structured_n9.json)
  - 668 attempt: deterministic `s[41]` flip of the published seed, degrading the modulus from `64` to `16`.
- Fairness notes:
  - the 668 baseline uses the same `s`-only neighborhood as the CA,
  - the small ladder keeps the same exact verifier across all methods,
  - orbit accounting uses the same signed-reversal canonicalization for all methods,
  - summaries are recorded both by method and by `seed_family` to expose family-specific failures.
