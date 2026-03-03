# Baseline Metrics

Generated at: 2026-03-03T03:47:28.363601+00:00
Commit: 4b95a84

## Definitions

- Energy drift %: `|E_final-E_0|/|E_0|*100`
- Angular momentum drift %: `|L_final-L_0|/|L_0|*100`
- Center-of-mass drift: `||COM_final - COM_0||`
- Mean step time: wall-clock simulation time divided by step count
- Memory usage: process RSS/peak memory footprint during run (MB)

## Results

| N | Energy drift % | Angular momentum drift % | COM drift | Mean step time (ms) | Memory usage (MB) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 25422.631159 | 214.910732 | 0.000000e+00 | 1.151592 | 845.105 |
| 64 | 2338.059630 | 3792.846614 | 0.000000e+00 | 18.151563 | 845.105 |
| 256 | 3945.645582 | 1807.757930 | 0.000000e+00 | 287.923911 | 845.105 |
