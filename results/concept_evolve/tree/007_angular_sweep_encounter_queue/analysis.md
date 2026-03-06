# Analysis

The angular sweep queue is validated as a sparse trigger mechanism.

- On `star_grazing_two_body`, mean recall is `1.0` with a mean candidate load of only `0.18` pairs per sampled step.
- On `small_n_ring`, the queue emits no false positives across the sampled rollout, which is exactly what an encounter-specific trigger should do in a calm regime.

Result: geometry-based triage is cheap, deterministic, and selective enough to drive the promoted encounter branch.
