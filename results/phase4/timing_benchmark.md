# End-to-End Timing Benchmark

**GPU:** NVIDIA A100-SXM4-40GB

**Peak GPU memory:** 3.13 GB
**All k<=6, len<=400 under 15 min:** YES

## Results

| Length | k | Total (s) | Total (min) | Single | Epistasis | Optimize | GPU (GB) | Pass? |
|--------|---|-----------|-------------|--------|-----------|----------|----------|-------|
| 108 | 3 | 37.0 | 0.62 | 19.7 | 16.1 | 1.2 | 2.68 | PASS |
| 108 | 4 | 29.3 | 0.49 | 10.7 | 16.9 | 1.7 | 2.68 | PASS |
| 108 | 6 | 31.4 | 0.52 | 11.9 | 16.8 | 2.8 | 2.68 | PASS |
| 108 | 8 | 23.9 | 0.4 | 6.1 | 14.5 | 3.3 | 2.68 | PASS |
| 200 | 4 | 21.4 | 0.36 | 6.9 | 12.6 | 1.9 | 2.82 | PASS |
| 200 | 6 | 26.6 | 0.44 | 9.2 | 14.1 | 3.3 | 2.82 | PASS |
| 300 | 4 | 30.9 | 0.51 | 14.0 | 14.9 | 2.0 | 2.97 | PASS |
| 300 | 6 | 36.1 | 0.6 | 17.7 | 14.3 | 4.1 | 2.97 | PASS |
| 400 | 4 | 38.4 | 0.64 | 21.4 | 14.8 | 2.2 | 3.13 | PASS |
| 400 | 6 | 45.4 | 0.76 | 21.6 | 19.2 | 4.6 | 3.13 | PASS |

All runs complete well under the 15-minute budget.
The bottleneck is ESM-2 single-mutation scoring and epistasis computation,
which together account for ~90% of total runtime.
