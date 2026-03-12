# Modular-Shadow Schema

Each candidate-positive baseline case is stored with the following fields.

- `candidate_from_prefix`: exact integer-coefficient recurrence recovered from the fit prefix.
- `full_length_verification`: whether the same recurrence survives the longer exact sequence.
- `density_class`: `positive_density` or `zero_density`.
- `residue_profiles`: one entry for each modulus in `{2,3,5,7,11,25}` containing:
  - the residue sequence,
  - whether the candidate recurrence still holds modulo that modulus,
  - the first failing window if it does not,
  - a short tail-period guess.
- `classification`: one of
  - `exact_recurrence`,
  - `prefix_fit`,
  - `sparse_subsequence_leak`,
  - `selector_shadow_failure`,
  - `no_candidate`.

The smoke artifact `results/baseline/modular_shadow_smoke.json` exercises the schema on:
- a certified rational arithmetic progression,
- a zero-density linear-recursive prefix mirage,
- a finite-union selector whose apparent low-order fit collapses under holdout and modular replay.
