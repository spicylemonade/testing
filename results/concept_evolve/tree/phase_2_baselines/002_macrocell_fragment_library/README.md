# Macrocell Fragment Library

Status: promoted

## Encoding

Each cell stores a small verified fragment type rather than a raw slope label. A fragment bundles local `f_i` incidence, seed-marker permissions for `R` and `T`, and simple conservation or legality flags, so the global board composes directly into a witness candidate.

## Why It Survives

- It is proof-carrying enough to stay aligned with the `H1` lane.
- It is baseline-compatible: non-CA baselines can search over the same fragment library and the same decoder interface, which makes compute parity and decoder-matched comparisons clean.
- It is the best adaptation of the generated `macrocell_curriculum_nca` idea to a fair benchmark setting.

## Decision

Promote as the default baseline-compatible encoding for both CA and non-CA search comparisons.
