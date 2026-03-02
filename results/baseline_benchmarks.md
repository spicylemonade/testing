# Baseline Search Benchmarks

## Configuration
- Search bound: 1000
- Modular filter: True

## Results
- Total candidates: 167,167,000
- Passed modular filter: 21,119
- Euler bricks found: 10
- Perfect cuboids found: 0
- Near-misses tracked: 10
- Wall clock time: 1.35s
- Throughput: 124,143,678 candidates/sec

## Without Modular Filter
- Throughput: 300,254,377 candidates/sec
- Euler bricks found: 10

## Filter Effectiveness
- Modular filter rejection rate: 99.9874%
- Speedup from filtering: reduces face diagonal checks significantly
