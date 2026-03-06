# Failure Envelope

## Close-Encounter Limits (H1, H2)

- Plain direct kernel
  - Unsafe on the `star_grazing_two_body` stress case at `dt = 0.04, 0.02, 0.01, 0.005` under the current safe-regime rule.
  - Main failure mode: energy drift grows too quickly near periapsis, even when the integrator remains internally reversible.

- Encounter-microstep kernel
  - Safe on the same stress case at `dt = 0.02, 0.01, 0.005`.
  - Still unsafe at `dt = 0.04`, where energy drift stays slightly above the declared gate even though final-state error is already much smaller than the plain direct path.

## Unit And Scale Caveats (H1, H3)

- Current verified scenarios are primarily in normalized units.
- The architecture supports explicit unit-system labels, but a full SI normalization audit is still a required follow-up before claiming unit-safe coverage.
- Resolution-coupled softening behaves more like a visualization or teaching regime than a fidelity-preserving physical fix.

## Dimensionality Limits (H1)

- The kernel state is 3D, but most encounter-specific experiments are planar because the promoted angular-sweep queue assumes nearly planar motion.
- A truly general 3D encounter broad phase remains future work; the current close-encounter novelty claim should therefore stay tied to nearly planar or low-inclination scenes.

## Runtime-Specific Divergence (H1)

- Python and Node direct-sum replays agree to machine-precision scale on the canonical scenario bundle, so no material divergence was observed on the tested bundle.
- The claim remains bounded, not absolute: future runtimes with different NaN, SIMD, or host-import behavior could widen the envelope if the runtime policy changes.

## Open Questions

- `H1`: can the encounter queue and micro-step branch stay effective on unequal-mass flybys and simple chaotic three-body scenes, not just the current star-grazing two-body stress case?
- `H2`: what is the smallest explicit policy set - shrink, merge, abort, or soften - that communicates failure honestly without hiding it?
- `H3`: can unit-safe authoring and scale guards be added without rebranding the project away from the current audit-first contribution?
- Falsifier concern: can any future round-trip trust signal be made predictive of external reference error, or will it remain a self-consistency metric only?
