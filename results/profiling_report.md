# Profiling Report: Brute Force Euler Brick Search

## Time Breakdown

The brute force search has three main operations:
1. **Iteration**: Nested loops over (a, b, c) triples with a <= b <= c <= max_edge
2. **Integer square root check**: `is_perfect_square()` using `math.isqrt()`
3. **Filtering**: Early exit when a^2+b^2 is not a perfect square (eliminates inner loop iterations)

The dominant cost is the iteration + integer square root check for a^2+b^2 in the outer two loops. The innermost loop (checking a^2+c^2 and b^2+c^2) only executes for Pythagorean pairs (a,b).

## Performance by Bound

| Bound | Euler Bricks | Candidates Checked | Filtered | Time (s) | Rate (cand/s) |
|-------|-------------|-------------------|----------|----------|---------------|
| 1000  | 10          | 474,638           | 974,094  | 0.54     | 873,245       |
| 2000  | 23          | 2,149,200         | 4,444,801| 2.32     | 925,850       |
| 5000  | 69          | 15,432,906        | 32,093,219| 15.71   | 982,118       |

## Scaling Analysis

- **Runtime scaling**: O(n^2.09) — approximately quadratic in edge bound
- **Candidate count scaling**: O(n^2.16) — slightly super-quadratic
- **Rate**: ~870K-980K candidates/second (fairly stable)

The search space is O(n^3) for unrestricted triples, but the Pythagorean pair filter on (a,b) reduces this to approximately O(n^2) effective candidates.

## Filter Efficiency

| Bound | Total candidates | Survived all filters | Filter rate |
|-------|-----------------|---------------------|-------------|
| 1000  | 1,448,732       | 10                  | 99.9993%    |
| 2000  | 6,594,001       | 23                  | 99.9997%    |
| 5000  | 47,526,125      | 69                  | 99.9999%    |

The first filter (a^2+b^2 must be perfect square) eliminates ~67% of (a,b) pairs, preventing the inner c-loop from executing. Combined with the second and third filters, >99.999% of candidates are eliminated.

## Memory Usage

Memory usage is minimal — the algorithm uses O(1) working memory per candidate. Only the results list grows, and Euler bricks are extremely sparse (10 out of ~1.4M candidates at bound=1000).

## Bottleneck Identification

1. **Primary bottleneck**: The O(n^2) iteration over (a,b) pairs and the `is_perfect_square()` check for a^2+b^2. This accounts for the majority of runtime since most pairs are filtered here.
2. **Secondary**: The inner c-loop for surviving (a,b) pairs. This is much cheaper since few pairs survive.
3. **`is_perfect_square()` is fast**: Python's `math.isqrt()` is implemented in C and takes ~100ns per call.

## Extrapolation

| Bound   | Estimated Time | Estimated Candidates |
|---------|---------------|---------------------|
| 10,000  | ~60s          | ~60M                |
| 100,000 | ~6,000s (1.7h)| ~6B                 |
| 1,000,000| ~600,000s (7d)| ~600B               |

Reaching the published search frontier of 10^10 would require ~10^17 seconds with this approach — clearly infeasible. Advanced sieving (Phase 3) is essential.

## Scaling Plot

See `figures/scaling_brute_force.png` for log-log scaling plots of runtime and candidate count vs. edge bound.
