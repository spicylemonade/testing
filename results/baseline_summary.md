# Baseline Benchmark Results

## 1. LKH-3 Reference Tour Costs

| Instance | n | City | Type | LKH-3 Cost (s) | LKH-3 Time (s) |
|----------|---|------|------|-----------------|-----------------|
| berlin_75 | 75 | berlin | mixed | 17766.4 | 1.689 |
| chicago_500 | 500 | chicago | grid | 20074.7 | 20.493 |
| london_500 | 500 | london | organic | 30140.2 | 21.905 |
| los_angeles_200 | 200 | los_angeles | mixed | 33488.3 | 6.258 |
| manhattan_200 | 200 | manhattan | grid | 25585.2 | 4.647 |
| manhattan_75 | 75 | manhattan | grid | 15748.0 | 0.796 |
| paris_75 | 75 | paris | organic | 18832.3 | 1.436 |
| rome_200 | 200 | rome | organic | 29294.3 | 6.024 |
| tokyo_500 | 500 | tokyo | mixed | 21815.8 | 21.020 |

## 2. Gap vs LKH-3 per Instance

| Instance | n | NN Gap (%) | Rand-Ins Gap (%) | VROOM Gap (%) |
|----------|---|-----------|-----------------|--------------|
| berlin_75 | 75 | 21.42 | 2.01 | 3.02 |
| chicago_500 | 500 | 31.78 | 28.68 | 12.04 |
| london_500 | 500 | 30.00 | 24.15 | 11.57 |
| los_angeles_200 | 200 | 18.56 | 6.73 | 2.73 |
| manhattan_200 | 200 | 27.46 | 10.44 | 2.85 |
| manhattan_75 | 75 | 24.98 | 8.49 | 1.39 |
| paris_75 | 75 | 16.10 | 12.81 | 3.94 |
| rome_200 | 200 | 28.95 | 5.83 | 3.23 |
| tokyo_500 | 500 | 28.95 | 22.11 | 10.38 |

## 3. Runtime Comparison

| Instance | n | LKH-3 (s) | NN (s) | Rand-Ins (s) | VROOM (s) |
|----------|---|-----------|--------|-------------|-----------|
| berlin_75 | 75 | 1.689 | 0.001 | 0.026 | 1.072 |
| chicago_500 | 500 | 20.493 | 0.020 | 0.060 | 191.689 |
| london_500 | 500 | 21.905 | 0.021 | 0.059 | 195.865 |
| los_angeles_200 | 200 | 6.258 | 0.003 | 0.009 | 11.803 |
| manhattan_200 | 200 | 4.647 | 0.003 | 0.009 | 9.232 |
| manhattan_75 | 75 | 0.796 | 0.001 | 0.002 | 0.596 |
| paris_75 | 75 | 1.436 | 0.001 | 0.002 | 0.566 |
| rome_200 | 200 | 6.024 | 0.003 | 0.009 | 8.849 |
| tokyo_500 | 500 | 21.020 | 0.020 | 0.062 | 202.572 |

## 4. Summary Statistics

| Solver | Mean Gap (%) | Median Gap (%) | Max Gap (%) | Mean Time (s) |
|--------|-------------|---------------|------------|--------------|
| lkh3 | 0.00 | 0.00 | 0.00 | 9.363 |
| nearest_neighbor | 25.35 | 27.46 | 31.78 | 0.008 |
| random_insertion | 13.47 | 10.44 | 28.68 | 0.026 |
| vroom | 5.68 | 3.23 | 12.04 | 69.138 |

## 5. Analysis: Where LKH-3 Leaves Room for Improvement

### By City Type

**nearest_neighbor:**
- grid: 28.07% mean gap
- organic: 25.01% mean gap
- mixed: 22.97% mean gap

**random_insertion:**
- grid: 15.87% mean gap
- organic: 14.27% mean gap
- mixed: 10.28% mean gap

**vroom:**
- grid: 5.42% mean gap
- organic: 6.24% mean gap
- mixed: 5.37% mean gap

### Key Observations

1. **LKH-3 dominates all baselines** across all instances, confirming it as the
   correct reference solver for this benchmark.

2. **VROOM is the strongest baseline** with the lowest gap to LKH-3, but still
   leaves significant room (especially on larger instances).

3. **Asymmetry exploitation opportunity:** LKH-3 internally transforms ATSP to
   symmetric TSP using Jonker-Volgenant, doubling the problem size. A solver that
   directly exploits asymmetric cost structure could potentially improve.

4. **Grid cities tend to have higher asymmetry** (one-way streets, traffic flow),
   suggesting these are the instances where asymmetry-aware heuristics could gain most.

5. **Scale matters:** On large instances (n=500), LKH-3's advantage over simple
   heuristics is even larger, suggesting the LKH search structure (k-opt with
   candidate sets) is critical at scale.
