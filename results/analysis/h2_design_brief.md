# H2 Design Brief

Prepared for rubric `item_012`.

## Branch identity

- Name: `Defect-Transport CA on the 64-modular 668 seed`
- Status: initially dormant behind `H1`; promoted only after `H1` failed; retired after the matched `668` seed attempt tied the non-CA baseline
- Exact source artifact: [`results/artifacts/seed_668_mod64.json`](/home/archivara/work/repo/results/artifacts/seed_668_mod64.json)
- Positive-control ladder: [`results/artifacts/h2_control_structured_n9.json`](/home/archivara/work/repo/results/artifacts/h2_control_structured_n9.json)

## State representation

- Core state: a structured pair `(q, s)` of length `n`, from which the four `pm1` sequences `A, B, C, D` are derived.
- Derived sequence construction is implemented in [`hadamard668/verifiers.py`](/home/archivara/work/repo/hadamard668/verifiers.py) through `structured_sequences`.
- Defect encoding:
  - the load-bearing observable is the combined aperiodic autocorrelation vector of `A, B, C, D`,
  - defects are recorded as nonzero shifts with their signed values,
  - quality is summarized by `two_adic_modulus`, `l1_defect`, `defect_count`, and `max_defect_magnitude`.
- Canonical orbit representative: signed reversal on the `(q, s)` pair.

## Local update rules

- Local phases:
  - the variable line is split into two parity phases, even and odd indices,
  - one step is one parity phase.
- Candidate operations:
  - for `s` updates, flipping one index changes all four derived sequences,
  - for `q` updates, flipping one index changes only the `C` and `D` derived sequences.
- Active CA rule:
  - compute exact modular-objective gain for each candidate flip,
  - select locally dominant improving flips,
  - fire several per phase, capped by `phase_move_cap = 4`.
- Matched comparator:
  - `direct_greedy` uses the same candidate family, same phase schedule, same cap, and same modular objective,
  - it chooses the best improving flips rather than the CA-style local-dominance rule.

## Promotion condition and comparator lock

- Promotion condition:
  - `H2` stays dormant until `H1` fails its first registered gate.
- Comparator lock:
  - on the real `668` attempt, `q` stays fixed and both CA and non-CA methods search only by local `s` flips,
  - on the small structured ladder, both methods use the same declared variable family for each start.

## Conserved quantities and verifier contract

- Conserved quantities:
  - sequence length,
  - declared variable family for a run,
  - exact verifier and objective ranking across all methods,
  - fixed `q` on the real `668` attempt.
- Verifier state:
  - `combined_aperiodic_pm1_autocorrelation`,
  - `nonzero_defects`,
  - `defect_count`,
  - `max_defect_magnitude`,
  - `l1_defect`,
  - `two_adic_modulus`,
  - `exact_certificate`,
  - `target_modulus_met`,
  - `quality_rank`.
- Registered success condition:
  - exact repair on the toy ladder,
  - modulus-lift on the real `668` attempt, tracked as `goal_hit`.

## Why this is not just a rephrased exact construction paper

- The branch does not claim a new modular-Hadamard construction.
- It starts from the published seed and tests only local defect transport in a fixed neighborhood.
- The search rule never manipulates external family parameters or an exact solver oracle.

## Decision

- The design was sufficiently constrained to make a fair claim.
- The claim failed on the decisive test: on the degraded order-668 seed, `parallel_gain_ca` and `direct_greedy` tie exactly on every decisive verifier metric, so the CA contributes no measurable repair advantage.
