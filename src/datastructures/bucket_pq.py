"""Bucketed Priority Queue for SSSP.

A bucket-based priority queue that provides O(1) amortized insert and
extract-batch operations by grouping elements into buckets of fixed width.
This avoids comparison-based O(log n) extract-min operations.

Operations:
- insert(vertex, key): O(1) — place into appropriate bucket
- extract_min_batch(): O(bucket_size) — extract all elements from the
  smallest non-empty bucket
- decrease_key(vertex, new_key): O(1) — move to appropriate bucket
- is_empty(): O(1)

Time complexity per operation documented below.
"""


class BucketPQ:
    """Bucket-based priority queue for bounded-range keys.

    Parameters
    ----------
    n_buckets : int
        Number of buckets.
    bucket_width : float
        Width of each bucket. Bucket i covers [i*width, (i+1)*width).
    offset : float
        Minimum key value (keys are shifted by -offset before bucketing).
    """

    __slots__ = ('n_buckets', 'width', 'offset', 'buckets', 'vertex_bucket',
                 'current', 'size', 'stats')

    def __init__(self, n_buckets, bucket_width, offset=0.0):
        self.n_buckets = n_buckets
        self.width = bucket_width
        self.offset = offset
        self.buckets = [set() for _ in range(n_buckets + 1)]  # +1 overflow
        self.vertex_bucket = {}  # vertex -> bucket index
        self.current = 0
        self.size = 0
        self.stats = {'comparisons': 0, 'heap_ops': 0}

    def _bucket_index(self, key):
        """Compute bucket index for a key. O(1) — one addition + one comparison."""
        idx = int((key - self.offset) / self.width) if self.width > 0 else 0
        self.stats['comparisons'] += 1
        if idx < 0:
            return 0
        if idx >= self.n_buckets:
            return self.n_buckets
        return idx

    def insert(self, vertex, key):
        """Insert vertex with given key. O(1) amortized."""
        self.stats['heap_ops'] += 1
        idx = self._bucket_index(key)
        # Remove from old bucket if present
        if vertex in self.vertex_bucket:
            old_idx = self.vertex_bucket[vertex]
            self.buckets[old_idx].discard(vertex)
        else:
            self.size += 1
        self.buckets[idx].add(vertex)
        self.vertex_bucket[vertex] = idx

    def decrease_key(self, vertex, new_key):
        """Move vertex to a (possibly different) bucket. O(1)."""
        self.stats['heap_ops'] += 1
        new_idx = self._bucket_index(new_key)
        if vertex in self.vertex_bucket:
            old_idx = self.vertex_bucket[vertex]
            if new_idx < old_idx:
                self.buckets[old_idx].discard(vertex)
                self.buckets[new_idx].add(vertex)
                self.vertex_bucket[vertex] = new_idx
                if new_idx < self.current:
                    self.current = new_idx
        else:
            self.size += 1
            self.buckets[new_idx].add(vertex)
            self.vertex_bucket[vertex] = new_idx
            if new_idx < self.current:
                self.current = new_idx

    def extract_min_batch(self):
        """Extract all vertices from the smallest non-empty bucket.

        Returns
        -------
        set of vertices in the minimum bucket, or empty set.

        O(batch_size + skipped_empty_buckets).
        """
        while self.current <= self.n_buckets:
            self.stats['comparisons'] += 1
            if self.buckets[self.current]:
                batch = self.buckets[self.current]
                self.buckets[self.current] = set()
                for v in batch:
                    del self.vertex_bucket[v]
                self.size -= len(batch)
                self.stats['heap_ops'] += len(batch)
                return batch
            self.current += 1
        return set()

    def is_empty(self):
        return self.size <= 0
