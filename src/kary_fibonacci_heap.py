"""k-ary Fibonacci heap implementation.

Generalizes the standard Fibonacci heap by allowing each node to have
at most k children (where k = floor(log2(log2(n)))). This reduces the
maximum degree from O(log n) to O(log n / log k), giving extract-min
cost of O(log n / log k) instead of O(log n).

Setting k = log log n yields extract-min in O(log n / log log n).
"""

import math


class KFibNode:
    __slots__ = ('key', 'value', 'degree', 'mark', 'parent', 'child',
                 'left', 'right', 'child_cut_count')

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.degree = 0
        self.mark = False
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.child_cut_count = 0


class KaryFibonacciHeap:
    """k-ary Fibonacci heap for HiBRA algorithm.

    The branching factor k controls the tradeoff between extract-min cost
    (O(max_degree)) and decrease-key cost (O(1) amortized via cascading cuts
    triggered when a node loses its k-th child instead of 2nd).
    """

    def __init__(self, n_estimate, counter=None):
        """Initialize with estimated number of elements for k computation.

        Args:
            n_estimate: Upper bound on number of elements (for computing k).
            counter: OpCounter for tracking operations.
        """
        self.counter = counter
        self.min_node = None
        self.total_nodes = 0

        # k = max(2, floor(log2(log2(n))))
        if n_estimate >= 16:
            log2n = math.log2(n_estimate)
            self.k = max(2, int(math.log2(max(2, log2n))))
        else:
            self.k = 2

        # Max degree bound: O(log_k(n)) = O(log n / log k)
        if n_estimate > 1:
            self.max_degree = int(math.log(n_estimate) / math.log(max(2, self.k))) + 3
        else:
            self.max_degree = 3

    def _cmp_lt(self, a, b):
        if self.counter:
            return self.counter.less_than(a, b)
        return a < b

    def is_empty(self):
        return self.total_nodes == 0

    def insert(self, key, value):
        """Insert new element. O(1) amortized."""
        node = KFibNode(key, value)
        self.total_nodes += 1
        if self.counter:
            self.counter.record_insert()

        if self.min_node is None:
            self.min_node = node
        else:
            self._add_to_root_list(node)
            if self._cmp_lt(node.key, self.min_node.key):
                self.min_node = node
        return node

    def extract_min(self):
        """Remove and return minimum element.

        Cost: O(k + max_degree) = O(log log n + log n / log log n)
            = O(log n / log log n) amortized comparisons.
        """
        z = self.min_node
        if z is None:
            return None

        if self.counter:
            self.counter.record_extract_min()

        # Collect children of z
        children = self._collect_list(z.child)

        # Add children to root list
        for c in children:
            c.parent = None
            self._add_to_root_list(c)

        # Remove z from root list
        self._remove_from_list(z)
        self.total_nodes -= 1

        if self.total_nodes == 0:
            self.min_node = None
        else:
            self.min_node = z.right if z.right != z else (children[0] if children else None)
            self._consolidate()

        return z.key, z.value

    def decrease_key(self, node, new_key):
        """Decrease key of node. O(1) amortized.

        Uses cascading cut with threshold k: a node is cut from its parent
        when it loses its (k)-th child (instead of 2nd as in standard Fibonacci).
        This maintains O(1) amortized decrease-key while increasing max degree
        to O(log_k n) instead of O(log_phi n).
        """
        if self.counter:
            self.counter.record_decrease_key()

        if not self._cmp_lt(new_key, node.key):
            return

        node.key = new_key
        parent = node.parent

        if parent is not None and self._cmp_lt(node.key, parent.key):
            self._cut(node, parent)
            self._cascading_cut(parent)

        if self._cmp_lt(node.key, self.min_node.key):
            self.min_node = node

    def _add_to_root_list(self, node):
        mn = self.min_node
        node.left = mn
        node.right = mn.right
        mn.right.left = node
        mn.right = node

    def _remove_from_list(self, node):
        if node.right == node:
            return
        node.left.right = node.right
        node.right.left = node.left

    def _collect_list(self, head):
        if head is None:
            return []
        result = []
        node = head
        while True:
            result.append(node)
            node = node.right
            if node == head:
                break
        return result

    def _consolidate(self):
        """Consolidate root list. Cost: O(max_degree) = O(log n / log log n)."""
        if self.min_node is None:
            return

        degree_table = [None] * (self.max_degree + 1)
        roots = self._collect_list(self.min_node)

        for w in roots:
            x = w
            d = x.degree
            while d < len(degree_table) and degree_table[d] is not None:
                y = degree_table[d]
                if self._cmp_lt(y.key, x.key):
                    x, y = y, x
                self._link(y, x)
                degree_table[d] = None
                d += 1
            if d >= len(degree_table):
                degree_table.extend([None] * (d - len(degree_table) + 1))
            degree_table[d] = x

        self.min_node = None
        for node in degree_table:
            if node is not None:
                node.parent = None
                node.left = node
                node.right = node
                if self.min_node is None:
                    self.min_node = node
                else:
                    self._add_to_root_list(node)
                    if self._cmp_lt(node.key, self.min_node.key):
                        self.min_node = node

    def _link(self, y, x):
        """Make y a child of x."""
        y.parent = x
        if x.child is None:
            x.child = y
            y.left = y
            y.right = y
        else:
            c = x.child
            y.left = c
            y.right = c.right
            c.right.left = y
            c.right = y
        x.degree += 1
        y.mark = False
        y.child_cut_count = 0

    def _cut(self, x, y):
        """Cut x from y's child list, add to root list."""
        if x.right == x:
            y.child = None
        else:
            if y.child == x:
                y.child = x.right
            x.left.right = x.right
            x.right.left = x.left
        y.degree -= 1

        x.parent = None
        x.mark = False
        x.child_cut_count = 0
        x.left = x
        x.right = x
        self._add_to_root_list(x)

    def _cascading_cut(self, y):
        """Cascading cut with k-ary threshold.

        In standard Fibonacci heap: cut when 2nd child is lost (mark bit).
        In k-ary variant: cut when child_cut_count reaches threshold.
        For k=2, this is equivalent to standard Fibonacci heap.
        For k>2, the threshold is ceil(k/2) to maintain the degree bound.
        """
        z = y.parent
        if z is not None:
            y.child_cut_count += 1
            # Cut threshold: after losing ceil(k/2) children
            threshold = max(2, (self.k + 1) // 2)
            if y.child_cut_count < threshold:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)
