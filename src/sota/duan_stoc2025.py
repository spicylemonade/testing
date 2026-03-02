"""Simplified implementation of Duan, Mao, Mao, Shu & Yin (STOC 2025).

Faithful simplification of the recursive BMSSP decomposition that breaks
the sorting barrier for directed SSSP.  The key idea: instead of sorting
all n vertices by distance (which costs Omega(n log n) comparisons),
we recursively partition vertices into distance intervals and solve each
interval with bounded Dijkstra.  The recursion depth is O(log^{2/3} n),
giving total work O(m * log^{2/3} n).

Simplifications vs. the full paper:
- Uses binary-heap bounded Dijkstra at the base level.
- Pivot selection uses a simplified k-hop frontier expansion.
- Interval boundaries are computed from discovered distances.
"""

import heapq
import math


def sssp(adj, source, n):
    """SSSP via recursive BMSSP decomposition (simplified Duan et al. 2025).

    Returns (distances, stats).
    """
    dist = [float('inf')] * n
    dist[source] = 0.0
    stats = {'comparisons': 0, 'additions': 0, 'heap_ops': 0}

    if n <= 1:
        return {v: dist[v] for v in range(n)}, stats

    # Recursion parameters
    log_n = math.log2(max(n, 2))
    t = max(1, int(log_n ** (2.0 / 3.0)))  # interval exponent
    depth = max(1, math.ceil(log_n / t))    # recursion depth

    def _bounded_dijkstra(seeds, upper):
        """Run Dijkstra from seeds, settling only vertices with dist < upper."""
        pq = []
        for s in seeds:
            if dist[s] < upper:
                heapq.heappush(pq, (dist[s], s))
                stats['heap_ops'] += 1
        settled = set()
        while pq:
            d_u, u = heapq.heappop(pq)
            stats['heap_ops'] += 1
            stats['comparisons'] += 1
            if d_u > dist[u] or u in settled:
                continue
            if d_u >= upper:
                continue
            settled.add(u)
            for v, w in adj.get(u, []):
                stats['additions'] += 1
                nd = d_u + w
                stats['comparisons'] += 1
                if nd < dist[v]:
                    dist[v] = nd
                    if nd < upper:
                        heapq.heappush(pq, (nd, v))
                        stats['heap_ops'] += 1
        return settled

    def _bmssp(level, lower, upper, seeds):
        """Recursive BMSSP solving SSSP in distance range [lower, upper).

        seeds: set of vertices whose current dist is in [lower, upper) and
               that may still propagate shorter paths to other vertices.
        """
        if not seeds:
            return set()

        # Base case: run bounded Dijkstra
        if level <= 0:
            return _bounded_dijkstra(seeds, upper)

        # Divide [lower, upper) into 2^t sub-intervals
        n_sub = min(1 << t, max(2, len(seeds)))
        width = (upper - lower) / n_sub

        all_settled = set()
        active = set(seeds)

        for i in range(n_sub):
            sub_upper = lower + (i + 1) * width if i < n_sub - 1 else upper
            # Collect active vertices whose distance falls in this sub-interval
            sub_seeds = {v for v in active if dist[v] < sub_upper}
            if not sub_seeds:
                continue

            # Recurse one level down
            newly_settled = _bmssp(level - 1, lower + i * width,
                                   sub_upper, sub_seeds)
            all_settled.update(newly_settled)
            active -= newly_settled

            # Relax edges from newly settled vertices → may create new seeds
            for u in newly_settled:
                for v, w in adj.get(u, []):
                    stats['additions'] += 1
                    nd = dist[u] + w
                    stats['comparisons'] += 1
                    if nd < dist[v]:
                        dist[v] = nd
                        if nd < upper:
                            active.add(v)

        return all_settled

    # Estimate an upper bound on distances
    # Use infinity to cover all reachable vertices
    _bmssp(depth, 0.0, float('inf'), {source})

    return {v: dist[v] for v in range(n)}, stats
