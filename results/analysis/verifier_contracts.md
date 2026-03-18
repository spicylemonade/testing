# Verifier Contracts

Prepared for rubric `item_007`.

## Machine-readable schemas

- [`results/contracts/support_state.schema.json`](/home/archivara/work/repo/results/contracts/support_state.schema.json)
- [`results/contracts/modular_state.schema.json`](/home/archivara/work/repo/results/contracts/modular_state.schema.json)
- [`results/contracts/run_record.schema.json`](/home/archivara/work/repo/results/contracts/run_record.schema.json)

## H1 support-state contract

- Representation: binary support vector of fixed length and fixed weight.
- Canonical representative: dihedral orbit representative from `cyclic_canonical_binary`.
- Exact verifier fields:
  - `periodic_autocorrelation_half`
  - `autocorrelation_debt`
  - `closest_target_distance`
  - `max_defect_magnitude`
  - `exact_hit`
- PSD check: diagnostic only, stored as `psd_check` using a numeric DFT summary. It is not a pass criterion by itself.
- Pass / fail rule:
  - Exact pass: `exact_hit == true` and `weight` equals the instance weight.
  - Ranked fallback: minimize `closest_target_distance`, then `max_defect_magnitude`.

## H2 modular-state contract

- Representation: structured `q/s` seed plus derived sequences `A, B, C, D`.
- Canonical representative: signed-reversal canonical form of the `(q, s)` pair.
- Exact verifier fields:
  - `combined_aperiodic_pm1_autocorrelation`
  - `nonzero_defects`
  - `defect_count`
  - `max_defect_magnitude`
  - `l1_defect`
  - `two_adic_modulus`
  - `exact_certificate`
  - `target_modulus_met`
  - `quality_rank`
- Pass / fail rule:
  - Exact-repair pass: `exact_certificate == true`.
  - Modulus-lift pass: `two_adic_modulus >= target_modulus`.
  - Ranked fallback: maximize `quality_rank`, then minimize `l1_defect`, `defect_count`, and `max_defect_magnitude`.
- Run-record note:
  - `exact_hit` remains literal exact repair.
  - `goal_hit` is the registered success condition for the current control mode and is the field that matters for modulus-lift runs.

## Run-record contract

- Every recorded run must include:
  - deterministic seed metadata,
  - the matched-budget schedule,
  - accepted-move count,
  - visited-state and unique-orbit counts,
  - `best_state`,
  - `final_state`,
  - elapsed wall-clock time,
  - lightweight snapshots.
- H1 runs record `edge_evaluations`.
- H2 runs record `variable_evaluations`.
- H2 modulus-lift runs also record `goal_hit` and `goal_hit_step`.

## Reproduction commands

- Artifact refresh: `python3 -m hadamard668.artifacts export`
- H1-only outputs: `python3 -m hadamard668.experiments run-h1`
- H2-only outputs: `python3 -m hadamard668.experiments run-h2`
- Full experiment outputs: `python3 -m hadamard668.experiments run-all`
