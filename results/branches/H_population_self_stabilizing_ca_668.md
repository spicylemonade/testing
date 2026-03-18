# H Population Self-Stabilizing CA 668

This branch keeps the rule table fixed from non-frontier controls and adds a stochastic population layer that must self-contract onto one orbit class before any frontier update is accepted.

## Control-Only Rule Table

- `control_n5_q0`: `24` control states, `162` improving representatives.
- `control_n7_q0`: `24` control states, `338` improving representatives.
- `control_n9_hardest_pair`: `64` control states, `2259` improving representatives.

## Self-Stabilization Rule

- Each step forms a population over the current orbit representatives.
- Coupling reinforces previously concentrated votes across neighboring orbit classes.
- An update is accepted only after the population crosses the contraction threshold; otherwise the run is classified as diffusion and stops.

## Canonical Frontier Result

- Population median: `13/2744/480`.
- Zero-coupling median: `13/2744/480`.
- Raw local baseline: `13/2880/512`.
- Scorer-only: `13/2880/512`.
- Population contractions: `3/5` seeds.

## Phase Map

- Selected operating point: coupling `1.6`, threshold `0.42`.
- Phase map artifact: `results/analysis/frontier_population_phase_map.md`.

## Verdict

- The population branch fails honestly. Canonical success = `False` and perturbation-suite wins = `0` of `5` after equal seed coverage, so the coupled rule never establishes a robust self-stabilizing advantage over zero_coupling.
