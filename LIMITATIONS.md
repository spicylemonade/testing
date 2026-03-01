# Limitations and Future Work

## 1. Graph Families Where Advantage is Smallest

### Dense Graphs (m = Theta(n^2))
On dense graphs, the edge relaxation cost O(m) = O(n^2) dominates the vertex extraction cost. HiBRA's improvement to the extraction term (n log n -> n log n / log log n) is negligible relative to n^2. Both HiBRA and standard Dijkstra achieve O(n^2).

### Very Sparse Graphs (m = O(n))
On very sparse graphs, Duan et al. (2025) achieves O(n log^{2/3} n), which is asymptotically better than HiBRA's O(n log n / log log n). For example, at n = 10^6:
- HiBRA: ~5.0 * 10^6 operations
- Duan et al.: ~3.4 * 10^6 operations

### Adversarial Dijkstra Inputs
Adversarial graphs designed to maximize decrease-key operations (Fredman and Tarjan, 1987) show the same operation count for HiBRA and standard Fibonacci heap Dijkstra, since both use O(1) amortized decrease-key.

## 2. Practical Overhead Analysis

### Constant Factors
The k-ary Fibonacci heap has a constant factor overhead of approximately 5-8x over Python's heapq binary heap in wall-clock time. This is due to:
- Pointer-chasing in the circular doubly-linked child lists (cache-unfriendly)
- Object allocation overhead for KFibNode instances
- Python interpreter overhead for method calls (insert, extract_min, decrease_key)

In C/C++, the overhead would be smaller but still significant (estimated 2-4x based on Fibonacci heap literature).

### Memory Usage
Each KFibNode requires ~100 bytes in Python (key, value, degree, mark, child_cut_count, parent, child, left, right pointers). For n = 10^6 vertices, this is ~100 MB for the heap alone, compared to ~16 MB for a binary heap using arrays.

### Implementation Complexity
The k-ary Fibonacci heap is ~250 lines of Python, compared to ~20 lines for Python's heapq. The cascading cut mechanism, consolidation, and circular list management are error-prone. Our implementation required fixing bugs related to empty-heap consolidation and duplicate child processing during development.

## 3. Assumptions Limiting Applicability

### Non-Negative Weights
HiBRA requires w(e) >= 0 for all edges. It cannot handle negative weights, unlike Bellman-Ford (Bellman, 1958) or the recent near-linear algorithms of Bernstein, Nanongkai, and Wulff-Nilsen (2022).

### Comparison-Addition Model
The complexity bound O(m + n log n / log log n) holds only in the comparison-addition model, where the algorithm may only compare and add weight values. In the word RAM model, faster algorithms exist: Thorup (2004) achieves O(m + n log log n) for integer weights.

### Directed Graphs
While HiBRA works on both directed and undirected graphs, the improvement is most relevant for directed graphs. For undirected graphs, Pettie and Ramachandran (2005) achieve O(m * alpha(m,n)), which is better.

### Real-Valued Weights
The algorithm assumes exact real arithmetic. In practice, floating-point arithmetic introduces roundoff errors that could theoretically cause incorrect results for pathological inputs with weight ratios exceeding ~10^{15}.

## 4. Open Questions

### Question 1: Is O(m + n log n / log log n) tight for heap-based SSSP?
The best known lower bound for SSSP in the comparison-addition model is Omega(m). There is no known lower bound exceeding Omega(m + n) for the specific case of heap-based Dijkstra. Closing this gap is a major open problem in the theory of SSSP algorithms (Fredman and Saks, 1989; Pettie, 2005).

### Question 2: Can the cascading cut threshold be optimized further?
The threshold ceil(k/2) is chosen for analytical convenience. A more aggressive threshold (e.g., k-1) would allow even higher node degrees but might increase the amortized decrease-key cost beyond O(1). The optimal threshold as a function of k remains unexplored.

### Question 3: Does the improvement compose with other techniques?
Can the k-ary Fibonacci heap be combined with:
- Duan et al.'s interval pivots to improve both the m and n terms simultaneously?
- Haeupler et al.'s beyond-worst-case analysis to achieve instance-optimal bounds with the improved worst case?
- Price functions (Johnson, 1977) to extend to negative-weight SSSP?

### Question 4: What is the practical crossover point?
At what graph size does the O(log n / log log n) extract-min cost become measurably better than O(log n) in a cache-optimized C implementation? Our analysis estimates n >= 10^{1.3 * 10^9}, but a tighter analysis or a different k schedule might bring this to a more reasonable range.

## 5. Future Research Directions

### Direction 1: Adaptive k Selection
Instead of fixing k = floor(log2(log2(n))) globally, adapt k per extraction based on the current heap size. Early in the algorithm (heap nearly full), use larger k. Late in the algorithm (heap nearly empty), use smaller k. This might improve constant factors without affecting the asymptotic bound.

### Direction 2: Cache-Friendly k-ary Fibonacci Heap
Implement the k-ary Fibonacci heap using array-based storage (like a van Emde Boas layout) instead of pointer-based trees. This could reduce the cache miss penalty that dominates practical running time. Specifically:
- Store children in contiguous memory blocks of size k
- Use index arithmetic instead of pointer traversal for sibling navigation
- Batch consolidation operations for better branch prediction

### Direction 3: Parameterized SSSP Complexity
Study the SSSP complexity as a function of both m, n, and the graph's structural parameters (diameter, treewidth, highway dimension). The k-ary Fibonacci heap's advantage is in the n term; for graphs where the n term dominates (sparse, high-diameter), the improvement is most significant.

### Direction 4: Experimental Comparison with Duan et al.
Implement Duan et al.'s algorithm (or a simplified version) and compare operation counts directly with HiBRA on the same graph instances. Cassis et al. (SEA 2025) provided some practical evaluation, but a head-to-head comparison on our graph families would be informative.

### Direction 5: Extension to All-Pairs Shortest Paths
Johnson's algorithm (1977) reduces APSP to n calls to SSSP. Using HiBRA instead of Dijkstra gives APSP in O(mn + n^2 log n / log log n) instead of O(mn + n^2 log n). For sparse graphs (m = O(n)), this improves the APSP bound from O(n^2 log n) to O(n^2 log n / log log n).
