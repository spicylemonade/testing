"""True Fibonacci heap implementation.

Supports O(1) amortized insert, decrease-key, and find-min,
and O(log n) amortized extract-min and delete.

Integrated with OpCounter for comparison-addition model tracking.
"""

import math


class FibNode:
    __slots__ = ('key', 'value', 'degree', 'mark', 'parent', 'child',
                 'left', 'right')

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.degree = 0
        self.mark = False
        self.parent = None
        self.child = None
        self.left = self
        self.right = self


class FibonacciHeap:
    """Fibonacci heap with operation counting via OpCounter."""

    def __init__(self, counter=None):
        self.min_node = None
        self.total_nodes = 0
        self.counter = counter

    def _cmp_lt(self, a, b):
        if self.counter:
            return self.counter.less_than(a, b)
        return a < b

    def is_empty(self):
        return self.total_nodes == 0

    def insert(self, key, value):
        """Insert a new key-value pair. Returns the node for decrease_key."""
        node = FibNode(key, value)
        self.total_nodes += 1
        if self.counter:
            self.counter.record_insert()
        if self.min_node is None:
            self.min_node = node
        else:
            self._insert_into_root_list(node)
            if self._cmp_lt(node.key, self.min_node.key):
                self.min_node = node
        return node

    def find_min(self):
        if self.min_node is None:
            return None
        return self.min_node.key, self.min_node.value

    def extract_min(self):
        """Remove and return (key, value) of minimum element."""
        z = self.min_node
        if z is None:
            return None
        if self.counter:
            self.counter.record_extract_min()

        # Collect z's children
        children = self._collect_list(z.child)

        # Add all children to root list
        for c in children:
            c.parent = None
            self._insert_into_root_list(c)

        # Remove z from root list
        self._remove_from_list(z)
        self.total_nodes -= 1

        if self.total_nodes == 0:
            self.min_node = None
        else:
            # Set min_node to some root (z.right, unless z was removed)
            self.min_node = z.right if z.right != z else children[0] if children else None
            self._consolidate()

        return z.key, z.value

    def decrease_key(self, node, new_key):
        """Decrease the key of node to new_key."""
        if self.counter:
            self.counter.record_decrease_key()

        if not self._cmp_lt(new_key, node.key):
            return  # new_key >= node.key, nothing to do

        node.key = new_key
        parent = node.parent

        if parent is not None and self._cmp_lt(node.key, parent.key):
            self._cut(node, parent)
            self._cascading_cut(parent)

        if self._cmp_lt(node.key, self.min_node.key):
            self.min_node = node

    def _insert_into_root_list(self, node):
        """Insert node into the root circular doubly linked list."""
        mn = self.min_node
        node.left = mn
        node.right = mn.right
        mn.right.left = node
        mn.right = node

    def _remove_from_list(self, node):
        """Remove node from its circular doubly linked list."""
        if node.right == node:
            # Only element in list — if it's a root, min_node handled by caller
            return
        node.left.right = node.right
        node.right.left = node.left

    def _collect_list(self, head):
        """Collect all nodes in a circular list into a Python list."""
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
        """Consolidate trees in root list so no two roots have same degree."""
        if self.min_node is None:
            return

        max_degree = int(math.log2(self.total_nodes)) + 3
        degree_table = [None] * (max_degree + 1)

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

        # Rebuild root list from degree table
        self.min_node = None
        for node in degree_table:
            if node is not None:
                node.parent = None
                node.left = node
                node.right = node
                if self.min_node is None:
                    self.min_node = node
                else:
                    self._insert_into_root_list(node)
                    if self._cmp_lt(node.key, self.min_node.key):
                        self.min_node = node

    def _link(self, y, x):
        """Make y a child of x. Both must be roots."""
        # y is removed from root list in consolidate's rebuild, so just reparent
        y.parent = x
        if x.child is None:
            x.child = y
            y.left = y
            y.right = y
        else:
            # Insert y into x's child list
            c = x.child
            y.left = c
            y.right = c.right
            c.right.left = y
            c.right = y
        x.degree += 1
        y.mark = False

    def _cut(self, x, y):
        """Cut x from y's child list, add x to root list."""
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
        x.left = x
        x.right = x
        self._insert_into_root_list(x)

    def _cascading_cut(self, y):
        """Cascading cut to maintain amortized bounds."""
        z = y.parent
        if z is not None:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)
