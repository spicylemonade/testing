# Composite Packet Locality Atlas

Retained actuator-library scan for the Novelty Deepening pass.

## Frontier Reference

- Frontier seed: `results/frontier/order_668_64m/seed_sequences.json`
- Frontier one-packet changed-lag median: `51.0` with low-splash cutoff `<= 25.5`.
- Frontier seed objective: support `13`, `l1 = 2880`, `max_abs = 512`.

## Harder Control

- Harder control seed: `results/experiments/controls/seeds/control_n9_hardest_pair.json`
- Control one-packet changed-lag median: `3.0` with control-specific low-splash cutoff `<= 1.5`.
- Control seed objective: support `4`, `l1 = 40`, `max_abs = 20`.

## Family Scan

- `balanced4`: `13861` candidates, frontier median changed-lag count `50.0`, low-splash candidates `362`, comparison counts `{'worse': 13861}`.
- `boundary_quad`: `85` candidates, frontier median changed-lag count `34.0`, low-splash candidates `7`, comparison counts `{'worse': 85}`.
- `pair`: `55611` candidates, frontier median changed-lag count `57.0`, low-splash candidates `860`, comparison counts `{'equal': 1, 'worse': 55610}`.
- `q_boundary_pair`: `3` candidates, frontier median changed-lag count `42.0`, low-splash candidates `0`, comparison counts `{'worse': 3}`.
- `s_boundary_pair`: `84` candidates, frontier median changed-lag count `33.5`, low-splash candidates `9`, comparison counts `{'worse': 84}`.

## Retained Library

- Selection rule: Pareto frontier over (changed_lag_count, support_size, l1, max_abs) inside the frontier low-splash composite set. The retained set has median changed-lag count `9.0`.
- Frontier retained outcomes: `0` better, `1` equal, `8` worse.
- Frontier conclusion: no retained composite improves the canonical order-668 seed, but the retained basis is still nonempty because one two-packet action is exactly neutral and the rest form the locality-vs-damage Pareto front.

Retained composite records:
- `pair` ['s[84]', 's[166]']: changed lags `0`, `equal`, objective `13/2880/512`.
- `pair` ['s[39]', 's[43]']: changed lags `4`, `worse`, objective `15/2896/496`.
- `balanced4` ['q[39]', 's[39]', 'q[43]', 's[43]']: changed lags `5`, `worse`, objective `16/2888/504`.
- `pair` ['q[53]', 'q[136]']: changed lags `9`, `worse`, objective `14/2820/496`.
- `pair` ['s[35]', 's[47]']: changed lags `9`, `worse`, objective `17/2864/480`.
- `pair` ['s[29]', 's[114]']: changed lags `10`, `worse`, objective `15/2768/480`.
- `pair` ['s[53]', 's[136]']: changed lags `10`, `worse`, objective `15/2768/480`.
- `balanced4` ['q[29]', 's[29]', 'q[114]', 's[114]']: changed lags `11`, `worse`, objective `14/2812/496`.
- `pair` ['s[38]', 's[44]']: changed lags `12`, `worse`, objective `16/2656/480`.

## Control Cross-Check

- The length-9 hardest-pair control does admit improving low-splash pair and balanced-four actions, so the retained-library scan is not vacuous. The frontier is the outlier.
- This keeps packet-space CA alive only in the retained composite basis. The old one-packet H1 basis remains retired.
