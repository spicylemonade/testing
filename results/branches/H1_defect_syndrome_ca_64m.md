# H1 Defect-Syndrome CA 64m

## Scope

This branch implements `H1_defect_syndrome_ca_64m` as a compressed defect-repair cellular automaton anchored to the recovered order-668 `64`-modular seed.

Implemented files:

- `hadamard_ca/h1_ca.py`
- `scripts/run_h1_ca.py`
- `results/branches/H1_defect_syndrome_ca_64m_config.json`
- `results/branches/H1_smoke_control.json`
- `results/branches/H1_smoke_cli.json`
- `results/branches/H1_frontier_micro_smoke.json`
- `results/branches/H1_frontier_sensitivity_probe.json`

## Compressed State

The branch does not evolve the raw `668 x 668` sign lattice.

It operates on:

- a `334`-cell packet lattice made from the `167` q-packets and `167` s-packets
- a `166`-lag defect field from the combined aperiodic autocorrelation coefficients
- a sparse active-lag mask around the current nonzero lag support
- a refractory memory over packet cells to suppress immediate flip-back oscillations

The derived lift stays fixed:

- `A = s`
- `B = s'`
- `C = sq`
- `D = (sq)'`

where prime is the fixed second-half sign involution already used elsewhere in the repo.

## Local Update Rule

At each CA step:

1. Compute the current lag-defect field from the compact q/s state.
2. Build the active lag neighborhood from the nonzero lag support.
3. For each q/s packet, compute an exact lag-delta signature without materializing the full order-668 matrix.
4. Score each packet by weighted local defect reduction on the active lag neighborhood, plus spill penalties for creating new support outside that neighborhood.
5. Smooth packet pressure on a local packet graph:
   - same-channel cyclic radius `packet_neighborhood_radius`
   - opposite-channel packet at the same site
6. Apply refractory penalties, then activate nonconflicting local maxima.
7. Flip the selected packets and repeat until exactness, stagnation, or budget exhaustion.

## Neighborhood

- Lag neighborhood:
  - active nonzero lags plus radius `lag_neighborhood_radius`
- Packet neighborhood:
  - same-channel cyclic neighborhood on the q-ring or s-ring
  - cross-channel coupling between `q[i]` and `s[i]`
- Conflict rule:
  - no two simultaneously fired packets may occupy the same local packet neighborhood or the same q/s site

## Conserved Quantities

- fixed compact length `167` and order `668`
- binary packet alphabet `{-1, +1}`
- fixed q/s coordinate system
- fixed prime-involution lift into the derived quadruple
- fixed packet-graph topology for a chosen config

## Seed Loading

The branch loads the same q/s JSON format as the baseline methods.

- small control seed: `results/baselines/smoke_seed_n7_q3.json`
- canonical frontier seed: `results/frontier/order_668_64m/seed_sequences.json`

Runner:

```bash
python3 scripts/run_h1_ca.py \
  --config results/branches/H1_defect_syndrome_ca_64m_config.json \
  --seed-file results/frontier/order_668_64m/seed_sequences.json \
  --output results/experiments/order_668_64m/H1_defect_syndrome_ca_64m.json
```

## Verification Notes

- `results/branches/H1_smoke_control.json`
  - direct harness smoke reaches exactness on the shared non-exact length-7 q/s seed
- `results/branches/H1_smoke_cli.json`
  - the intended CLI runner also reaches exactness on the same seed
- `results/branches/H1_frontier_micro_smoke.json`
  - the branch runs on the canonical order-668 seed, but support can diffuse from `13` to much larger values even while `l1` and `max_abs` improve temporarily
- `results/branches/H1_frontier_sensitivity_probe.json`
  - with stronger spill control and conservative activation, 8 small parameter variants all stay pinned to the original frontier objective: support `13`, `l1 = 2880`, `max_abs = 512`

## Current Interpretation

This branch is implemented and executable, but not yet validated as a useful frontier method.

The current frontier picture has two failure signatures:

- weak spill control diffuses support
- stronger spill control preserves the seed but does not improve it

The updated `results/concept_evolve/probe_result.json` sharpens the likely cause: the present single-bit q/s packet basis appears frozen on the canonical seed, with no improving one-packet or two-packet moves reported there. That means rule tuning alone may not rescue H1 unless the actuator basis itself changes.

The next question is whether there is a narrow parameter regime between those two failures where H1 can beat the matched non-CA baselines on exact-feasibility outcomes.
