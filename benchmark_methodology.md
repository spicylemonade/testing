# Benchmark Methodology

## Timing Protocol

1. **Warmup runs:** 2 warmup runs are executed and discarded before measurement. This ensures JIT compilation effects (in Python/PyPy), cache warming, and initial memory allocation are excluded from measurements.

2. **Timed runs:** Minimum 5 timed runs per configuration.

3. **GC disabled:** Python's garbage collector is disabled during each timed run (`gc.disable()` / `gc.enable()`) to avoid GC pauses affecting measurements.

4. **Timer:** `time.perf_counter()` is used for sub-microsecond resolution wall-clock timing.

5. **No I/O during timing:** Graph generation, output formatting, and file I/O occur outside the timed sections.

## Statistical Reporting

For each configuration, we report:
- **Mean** wall-clock time
- **Median** wall-clock time (robust to outliers)
- **Standard deviation**
- **Min and Max** times

We use the **median** as the primary metric and report standard deviation to assess measurement stability.

## Operation Counting

Each algorithm implementation tracks:
- **Comparisons:** Number of key comparisons (priority queue comparisons + edge weight comparisons)
- **Additions:** Number of arithmetic additions (distance computations: d(u) + w(u,v))
- **Heap operations:** Number of priority queue operations (insert, extract-min, decrease-key)

Operation counts are deterministic (same for every run) and are taken from the last timed run.

## Memory Tracking

Peak resident set size (RSS) is measured via `resource.getrusage(RUSAGE_SELF).ru_maxrss`. We record the difference between pre-benchmark and post-benchmark peak RSS.

## Graph Generation

All graphs are generated with fixed random seed (42) for reproducibility. Graph types:
- **Sparse:** m = 3n edges (Erdos-Renyi with appropriate p)
- **Dense:** m = n²/2 edges
- **Grid:** sqrt(n) × sqrt(n) directed grid
- **Power-law:** Barabasi-Albert preferential attachment, m₀=3
- **Worst-case:** Chain + shortcuts forcing Θ(n log n) heap operations
- **Road network:** 2D geometric random graph

## Size Matrix

Testing sizes: n ∈ {1000, 10000, 100000, 1000000} for baselines. For the novel algorithm, additional sizes at n ∈ {5000, 50000, 500000} may be included.

Bellman-Ford is excluded for n ≥ 100000 due to O(mn) complexity making it impractical.

## Process Isolation

Benchmarks are run within a single Python process. While this doesn't provide full process isolation, GC disabling and warmup runs mitigate the main sources of measurement noise.

## Threats to Validity

1. **Python overhead:** Python implementations have significant constant-factor overhead compared to C/C++. Operation counts are a better measure of algorithmic complexity than wall-clock time.
2. **Cache effects:** Larger graphs may not fit in cache, causing cache misses that disproportionately affect some algorithms.
3. **Memory allocation:** Python's memory allocator can introduce variance.
4. **Single machine:** Results may not generalize to other hardware configurations.
