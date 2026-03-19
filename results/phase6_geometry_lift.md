# Phase 6 Geometry Lift

## Benchmark Spec

- Route geometry: `height 3, width 4 passive-middle extrusion`.
- Direct comparator geometry: `height 3, width 4 unrestricted direct search`.
- Seed budget: `4`; initial-T budget: `1`; boundary band: `1`.
- Direct-search RNG seeds: `[7201, 7202]` with `10` exact trials per seed.

## Family Results

### asym_a

- Route candidate words checked: `39`.
- Route forcing words found: `0`.
- Vertical label: `[1, 1]` with coordinate sum `2`.
- Matched unrestricted direct hit rate: `0.0000` over `20` exact trials.
- Best matched unrestricted direct certificate: `none`.

### asym_b

- Route candidate words checked: `39`.
- Route forcing words found: `0`.
- Vertical label: `[2, -1]` with coordinate sum `1`.
- Matched unrestricted direct hit rate: `0.0000` over `20` exact trials.
- Best matched unrestricted direct certificate: `none`.

### asym_c

- Route candidate words checked: `39`.
- Route forcing words found: `0`.
- Vertical label: `[1, 2]` with coordinate sum `3`.
- Matched unrestricted direct hit rate: `0.0000` over `20` exact trials.
- Best matched unrestricted direct certificate: `none`.

## Obstruction

- For the passive-middle H=3 extrusion of the H4 extractor, every generator with middle-row support is a multiple of the vertical label c at a middle-row vertex. Because c_1 + c_2 != 0 on asym_a, asym_b, and asym_c, no nonzero multiple of c is anti-diagonal. Therefore no middle-row vertex can ever satisfy the forcing criterion, so no member of this entire higher-geometry family can be forcing.
- Stronger than the one-seed obstruction because: The old H1 obstruction depended on a unique initial seed label. The new obstruction allows arbitrary top- and bottom-row boundary seeds and arbitrary width, and it kills the whole passive-middle H=3 family by a row-quotient invariant instead of by seed uniqueness.
- Broader-than-corridor note: This rules out an entire higher-geometry family under unchanged extractor logic, rather than only a single width-2 corridor template.
