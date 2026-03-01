"""Core component: Hop-Guided Frontier Partition.

Implements the novel decomposition technique for the HopGuidedSSSP algorithm.
The key idea: partition vertices by BFS hop-layers using geometric grouping,
avoiding the O(n log n) comparison cost of distance-rank-based partitioning.

This module provides:
- compute_hop_layers: BFS-based hop-distance computation in O(m) time
- geometric_hop_partition: partition vertices into geometrically-sized
  hop-layer groups in O(n) time with zero weight comparisons
"""

from collections import deque
import math


def compute_hop_layers(adj, source, n):
    """Compute BFS hop-layers from source, ignoring edge weights.

    Returns
    -------
    hop_layer : list[int]
        hop_layer[v] = number of hops from source to v (or -1 if unreachable)
    max_depth : int
        Maximum hop-layer index (the hop-diameter from source)
    layer_vertices : dict[int, list[int]]
        Mapping from layer index to list of vertices in that layer
    """
    hop_layer = [-1] * n
    hop_layer[source] = 0
    layer_vertices = {0: [source]}
    max_depth = 0

    queue = deque([source])
    while queue:
        u = queue.popleft()
        h = hop_layer[u]
        for v, _w in adj.get(u, []):
            if hop_layer[v] == -1:
                hop_layer[v] = h + 1
                if h + 1 > max_depth:
                    max_depth = h + 1
                layer_vertices.setdefault(h + 1, []).append(v)
                queue.append(v)

    return hop_layer, max_depth, layer_vertices


def geometric_hop_partition(frontier, hop_layer, max_depth, R=None):
    """Partition frontier vertices into geometric hop-layer blocks.

    Uses exponentially increasing block sizes:
    Block j contains vertices in hop-layers [2^j, 2^{j+1}).

    Parameters
    ----------
    frontier : set or list of vertex IDs
    hop_layer : list[int] from compute_hop_layers
    max_depth : int, maximum hop-layer
    R : int, optional recursion depth (used for sub-partitioning)

    Returns
    -------
    blocks : list[set]
        List of vertex sets, one per block, ordered by increasing hop-layer
    block_hop_ranges : list[tuple[int, int]]
        (min_hop, max_hop) for each block
    """
    if max_depth <= 0:
        return [set(frontier)], [(0, 0)]

    # Determine number of geometric blocks
    num_blocks = max(1, int(math.ceil(math.log2(max_depth + 1))))

    blocks = []
    block_ranges = []

    for j in range(num_blocks):
        lo = (1 << j) if j > 0 else 0
        hi = (1 << (j + 1))  # exclusive

        block_verts = set()
        for v in frontier:
            h = hop_layer[v]
            if lo <= h < hi:
                block_verts.add(v)

        if block_verts:
            blocks.append(block_verts)
            block_ranges.append((lo, hi - 1))

    # Handle vertices beyond the geometric range
    remaining = set()
    covered = set()
    for block in blocks:
        covered.update(block)
    for v in frontier:
        if v not in covered and hop_layer[v] >= 0:
            remaining.add(v)
    if remaining:
        blocks.append(remaining)
        block_ranges.append((1 << num_blocks, max_depth))

    return blocks, block_ranges


def uniform_hop_partition(frontier, hop_layer, max_depth, k):
    """Partition frontier into k blocks of approximately equal hop-span.

    Parameters
    ----------
    frontier : set or list
    hop_layer : list[int]
    max_depth : int
    k : int, number of blocks

    Returns
    -------
    blocks : list[set]
    """
    if k <= 1 or max_depth <= 0:
        return [set(frontier)]

    layers_per_block = max(1, int(math.ceil((max_depth + 1) / k)))
    blocks = [set() for _ in range(k)]

    for v in frontier:
        h = hop_layer[v]
        if h >= 0:
            block_idx = min(k - 1, h // layers_per_block)
            blocks[block_idx].add(v)

    return [b for b in blocks if b]


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

def _test_hop_layers():
    """Test hop-layer computation on a simple graph."""
    adj = {
        0: [(1, 1.0), (2, 5.0)],
        1: [(3, 1.0)],
        2: [(3, 1.0), (4, 2.0)],
        3: [(4, 1.0)],
        4: [],
    }
    hop, depth, layers = compute_hop_layers(adj, 0, 5)
    assert hop == [0, 1, 1, 2, 2], f"Wrong hop layers: {hop}"
    assert depth == 2
    assert set(layers[0]) == {0}
    assert set(layers[1]) == {1, 2}
    assert set(layers[2]) == {3, 4}
    print("  hop_layers: OK")


def _test_geometric_partition():
    """Test geometric hop partition."""
    hop_layer = [0, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8]
    frontier = set(range(1, 12))
    blocks, ranges = geometric_hop_partition(frontier, hop_layer, 8)
    # Verify all frontier vertices are covered
    covered = set()
    for b in blocks:
        covered.update(b)
    assert covered == frontier, f"Missing vertices: {frontier - covered}"
    # Verify blocks are disjoint
    total = sum(len(b) for b in blocks)
    assert total == len(frontier), f"Overlapping blocks"
    print(f"  geometric_partition: OK ({len(blocks)} blocks)")


def _test_uniform_partition():
    """Test uniform hop partition."""
    hop_layer = list(range(20))
    frontier = set(range(1, 20))
    blocks = uniform_hop_partition(frontier, hop_layer, 19, k=4)
    covered = set()
    for b in blocks:
        covered.update(b)
    assert covered == frontier
    print(f"  uniform_partition: OK ({len(blocks)} blocks)")


if __name__ == '__main__':
    print("Running core component tests...")
    _test_hop_layers()
    _test_geometric_partition()
    _test_uniform_partition()
    print("All core tests PASSED")
