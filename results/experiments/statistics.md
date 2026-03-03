# Statistical Analysis and Robustness Checks

Generated at: 2026-03-03T05:06:28.124863+00:00
Commit: 0a455b418f75f4256b1015701caf74cb8d723c7a

## Confidence intervals (median, bootstrap 95%)

| Method | Scenario | Metric | n | Median | 95% CI |
| --- | --- | --- | ---: | ---: | ---: |
| barnes_hut | random | max_energy_drift_pct | 5 | 8154.874973 | [1542.379776, 15430.838491] |
| barnes_hut | random | max_angular_momentum_drift_pct | 5 | 7249.844492 | [1127.164061, 8943.588983] |
| barnes_hut | random | center_of_mass_drift | 5 | 0.000420 | [0.000107, 0.001783] |
| barnes_hut | random | runtime_per_step_ms | 5 | 11.810874 | [11.671331, 12.147543] |
| barnes_hut | random | throughput_steps_per_s | 5 | 84.667739 | [82.321177, 85.680033] |
| barnes_hut | three_body | max_energy_drift_pct | 5 | 1764098.861714 | [1764098.861714, 1764098.861714] |
| barnes_hut | three_body | max_angular_momentum_drift_pct | 5 | 0.000000 | [0.000000, 0.000000] |
| barnes_hut | three_body | center_of_mass_drift | 5 | 0.000000 | [0.000000, 0.000000] |
| barnes_hut | three_body | runtime_per_step_ms | 5 | 0.074828 | [0.073810, 0.078608] |
| barnes_hut | three_body | throughput_steps_per_s | 5 | 13364.068017 | [12721.321443, 13548.241562] |
| barnes_hut | two_body | max_energy_drift_pct | 5 | 1.869582 | [1.869582, 1.869582] |
| barnes_hut | two_body | max_angular_momentum_drift_pct | 5 | 0.944569 | [0.944569, 0.944569] |
| barnes_hut | two_body | center_of_mass_drift | 5 | 0.000000 | [0.000000, 0.000000] |
| barnes_hut | two_body | runtime_per_step_ms | 5 | 0.054556 | [0.053800, 0.055276] |
| barnes_hut | two_body | throughput_steps_per_s | 5 | 18329.773615 | [18091.158180, 18587.344760] |
| baseline | random | max_energy_drift_pct | 5 | 7200.133936 | [2321.885085, 15582.557557] |
| baseline | random | max_angular_momentum_drift_pct | 5 | 5422.517311 | [1137.074861, 7682.962909] |
| baseline | random | center_of_mass_drift | 5 | 0.000000 | [0.000000, 0.000000] |
| baseline | random | runtime_per_step_ms | 5 | 17.929302 | [17.895225, 18.004235] |
| baseline | random | throughput_steps_per_s | 5 | 55.774620 | [55.542487, 55.880827] |
| baseline | three_body | max_energy_drift_pct | 5 | 1764098.861714 | [1764098.861714, 1764098.861714] |
| baseline | three_body | max_angular_momentum_drift_pct | 5 | 0.000000 | [0.000000, 0.000000] |
| baseline | three_body | center_of_mass_drift | 5 | 0.000000 | [0.000000, 0.000000] |
| baseline | three_body | runtime_per_step_ms | 5 | 0.073516 | [0.072815, 0.079776] |
| baseline | three_body | throughput_steps_per_s | 5 | 13602.460585 | [12535.063183, 13733.365047] |
| baseline | two_body | max_energy_drift_pct | 5 | 1.869582 | [1.869582, 1.869582] |
| baseline | two_body | max_angular_momentum_drift_pct | 5 | 0.944569 | [0.944569, 0.944569] |
| baseline | two_body | center_of_mass_drift | 5 | 0.000000 | [0.000000, 0.000000] |
| baseline | two_body | runtime_per_step_ms | 5 | 0.053002 | [0.051565, 0.056581] |
| baseline | two_body | throughput_steps_per_s | 5 | 18867.114073 | [17673.849260, 19392.992859] |
| symplectic | random | max_energy_drift_pct | 5 | 9466.710616 | [4999.402900, 12120.869340] |
| symplectic | random | max_angular_momentum_drift_pct | 5 | 0.000000 | [0.000000, 0.000000] |
| symplectic | random | center_of_mass_drift | 5 | 0.000000 | [0.000000, 0.000000] |
| symplectic | random | runtime_per_step_ms | 5 | 17.858629 | [17.843887, 17.942558] |
| symplectic | random | throughput_steps_per_s | 5 | 55.995339 | [55.733413, 56.041600] |
| symplectic | three_body | max_energy_drift_pct | 5 | 510626.610583 | [510626.610583, 510626.610583] |
| symplectic | three_body | max_angular_momentum_drift_pct | 5 | 0.000000 | [0.000000, 0.000000] |
| symplectic | three_body | center_of_mass_drift | 5 | 0.000000 | [0.000000, 0.000000] |
| symplectic | three_body | runtime_per_step_ms | 5 | 0.073511 | [0.071540, 0.077587] |
| symplectic | three_body | throughput_steps_per_s | 5 | 13603.341987 | [12888.710624, 13978.135726] |
| symplectic | two_body | max_energy_drift_pct | 5 | 0.000800 | [0.000800, 0.000800] |
| symplectic | two_body | max_angular_momentum_drift_pct | 5 | 0.000000 | [0.000000, 0.000000] |
| symplectic | two_body | center_of_mass_drift | 5 | 0.000000 | [0.000000, 0.000000] |
| symplectic | two_body | runtime_per_step_ms | 5 | 0.052449 | [0.052018, 0.052651] |
| symplectic | two_body | throughput_steps_per_s | 5 | 19066.131353 | [18993.000905, 19223.975527] |

## Effect sizes vs baseline

| Scenario | Method | Metric | Median diff | 95% CI diff | Median % change | Win rate |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| random | barnes_hut | max_energy_drift_pct | -151.719066 | [-779.505309, 1109.116753] | -0.97% [-33.57, 15.18] | 60.0% |
| random | barnes_hut | max_angular_momentum_drift_pct | -9.910800 | [-319.306217, 1827.327181] | -0.35% [-19.65, 33.70] | 60.0% |
| random | barnes_hut | runtime_per_step_ms | -6.118428 | [-6.298599, -5.747683] | -34.13% [-35.05, -32.12] | 100.0% |
| random | symplectic | max_energy_drift_pct | 2853.786513 | [-6862.854555, 8062.874167] | 39.05% [-44.04, 307.72] | 40.0% |
| random | symplectic | max_angular_momentum_drift_pct | -5422.517311 | [-7682.962909, -1137.074861] | -100.00% [-100.00, -100.00] | 100.0% |
| random | symplectic | runtime_per_step_ms | -0.063956 | [-0.103522, -0.036596] | -0.36% [-0.58, -0.20] | 100.0% |
| three_body | barnes_hut | max_energy_drift_pct | 0.000000 | [0.000000, 0.000000] | 0.00% [0.00, 0.00] | 0.0% |
| three_body | barnes_hut | max_angular_momentum_drift_pct | 0.000000 | [0.000000, 0.000000] | 0.00% [0.00, 0.00] | 0.0% |
| three_body | barnes_hut | runtime_per_step_ms | 0.001823 | [-0.005825, 0.005519] | 2.48% [-7.30, 7.55] | 40.0% |
| three_body | symplectic | max_energy_drift_pct | -1253472.251131 | [-1253472.251131, -1253472.251131] | -71.05% [-71.05, -71.05] | 100.0% |
| three_body | symplectic | max_angular_momentum_drift_pct | 0.000000 | [0.000000, 0.000000] | 0.00% [0.00, 0.00] | 0.0% |
| three_body | symplectic | runtime_per_step_ms | -0.001549 | [-0.006265, 0.004772] | -2.12% [-7.85, 6.55] | 80.0% |
| two_body | barnes_hut | max_energy_drift_pct | 0.000000 | [0.000000, 0.000000] | 0.00% [0.00, 0.00] | 0.0% |
| two_body | barnes_hut | max_angular_momentum_drift_pct | 0.000000 | [0.000000, 0.000000] | 0.00% [0.00, 0.00] | 0.0% |
| two_body | barnes_hut | runtime_per_step_ms | 0.001554 | [-0.001305, 0.003036] | 2.93% [-2.31, 5.89] | 40.0% |
| two_body | symplectic | max_energy_drift_pct | -1.868782 | [-1.868782, -1.868782] | -99.96% [-99.96, -99.96] | 100.0% |
| two_body | symplectic | max_angular_momentum_drift_pct | -0.944569 | [-0.944569, -0.944569] | -100.00% [-100.00, -100.00] | 100.0% |
| two_body | symplectic | runtime_per_step_ms | -0.000984 | [-0.004132, 0.000923] | -1.86% [-7.30, 1.79] | 60.0% |

## dt sensitivity (baseline random-N64)

| dt | Median energy drift % | 95% CI |
| ---: | ---: | ---: |
| 0.000500 | 3197.464263 | [876.640869, 8762.052064] |
| 0.001000 | 4051.764098 | [1903.679853, 15689.471820] |
| 0.002000 | 8826.059932 | [3211.221084, 14368.767821] |

## softening sensitivity (baseline random-N64)

| softening | Median energy drift % | 95% CI |
| ---: | ---: | ---: |
| 0.000500 | 13708.421681 | [8762.052064, 50418.831210] |
| 0.001000 | 4051.764098 | [3197.464263, 8826.059932] |
| 0.002000 | 1223.107275 | [876.640869, 1961.478024] |

## Threshold pass/fail against item_002

| Metric | Threshold | Estimate | 95% CI | Status | Source |
| --- | ---: | ---: | ---: | --- | --- |
| energy_drift_pct | 0.100000 | 0.000800 | [0.000800, 0.000800] | PASS | symplectic two_body (seeded runs) |
| angular_drift_pct | 0.010000 | 0.000000 | [0.000000, 0.000000] | PASS | symplectic two_body (seeded runs) |
| orbit_error_pct | 1.000000 | 0.095946 | [0.095946, 0.095946] | PASS | symplectic two_body derived orbit-radius RMS |
| runtime_per_step_ms | 1.000000 | 287.923911 | [287.923911, 287.923911] | FAIL | baseline N=256 from results/baseline/metrics.json |

Overall threshold verdict: **FAIL**.
