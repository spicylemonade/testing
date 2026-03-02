"""Barnes-Hut quadtree for O(N log N) gravitational force approximation.

Implements a 2D quadtree with center-of-mass summaries at each node.
The Barnes-Hut opening criterion (s/d < theta) controls the accuracy-speed
tradeoff.

References:
  - Barnes, J. & Hut, P. (1986). A hierarchical O(N log N) force-calculation
    algorithm. Nature, 324, 446-449.
"""

from __future__ import annotations

from typing import Optional, List, Tuple

import numpy as np

from .bodies import G


class QuadTreeNode:
    """A node in the Barnes-Hut quadtree.

    Each node represents a square region of space. Internal nodes have 4
    children (NW, NE, SW, SE). Leaf nodes contain at most one body.

    Attributes:
        cx, cy: Center of the square region.
        size: Side length of the square region.
        total_mass: Total mass in this node's subtree.
        com_x, com_y: Center of mass coordinates.
        body_idx: Index of the body (leaf only, -1 for internal).
        children: List of 4 child nodes (None if leaf).
        is_leaf: True if this is a leaf node.
    """

    __slots__ = [
        "cx", "cy", "size", "total_mass", "com_x", "com_y",
        "body_idx", "children", "is_leaf",
    ]

    def __init__(self, cx: float, cy: float, size: float):
        self.cx = cx
        self.cy = cy
        self.size = size
        self.total_mass = 0.0
        self.com_x = 0.0
        self.com_y = 0.0
        self.body_idx = -1
        self.children: List[Optional[QuadTreeNode]] = [None, None, None, None]
        self.is_leaf = True


def _quadrant(node: QuadTreeNode, x: float, y: float) -> int:
    """Determine which quadrant a point falls into.

    Returns 0=NW, 1=NE, 2=SW, 3=SE.
    """
    if y >= node.cy:
        return 0 if x < node.cx else 1
    else:
        return 2 if x < node.cx else 3


def _child_center(node: QuadTreeNode, quadrant: int) -> Tuple[float, float]:
    """Compute the center of a child quadrant."""
    hs = node.size / 4.0  # half of child size
    if quadrant == 0:    # NW
        return node.cx - hs, node.cy + hs
    elif quadrant == 1:  # NE
        return node.cx + hs, node.cy + hs
    elif quadrant == 2:  # SW
        return node.cx - hs, node.cy - hs
    else:                # SE
        return node.cx + hs, node.cy - hs


def build_tree(pos: np.ndarray, mass: np.ndarray) -> QuadTreeNode:
    """Build a Barnes-Hut quadtree from particle positions and masses.

    Args:
        pos: Positions array, shape (N, 2).
        mass: Masses array, shape (N,).

    Returns:
        Root node of the quadtree.
    """
    n = pos.shape[0]
    if n == 0:
        return QuadTreeNode(0.0, 0.0, 1.0)

    # Determine bounding box
    xmin, ymin = pos[:, 0].min(), pos[:, 1].min()
    xmax, ymax = pos[:, 0].max(), pos[:, 1].max()
    size = max(xmax - xmin, ymax - ymin) * 1.01 + 1e-10  # small padding
    cx = (xmin + xmax) / 2.0
    cy = (ymin + ymax) / 2.0

    root = QuadTreeNode(cx, cy, size)

    for i in range(n):
        _insert(root, i, pos[i, 0], pos[i, 1], mass[i])

    return root


def _insert(
    node: QuadTreeNode,
    idx: int,
    x: float,
    y: float,
    m: float,
) -> None:
    """Insert a body into the tree."""
    if node.total_mass == 0.0:
        # Empty leaf: place body here
        node.body_idx = idx
        node.total_mass = m
        node.com_x = x
        node.com_y = y
        node.is_leaf = True
        return

    if node.is_leaf:
        # Leaf with existing body: need to subdivide
        old_idx = node.body_idx
        old_x = node.com_x
        old_y = node.com_y
        old_m = node.total_mass

        node.is_leaf = False
        node.body_idx = -1

        # Re-insert existing body
        _insert_into_child(node, old_idx, old_x, old_y, old_m)

    # Insert new body into appropriate child
    _insert_into_child(node, idx, x, y, m)

    # Update center of mass
    total = node.total_mass + m
    node.com_x = (node.com_x * node.total_mass + x * m) / total
    node.com_y = (node.com_y * node.total_mass + y * m) / total
    node.total_mass = total


def _insert_into_child(
    node: QuadTreeNode,
    idx: int,
    x: float,
    y: float,
    m: float,
) -> None:
    """Insert a body into the appropriate child of an internal node."""
    q = _quadrant(node, x, y)
    if node.children[q] is None:
        ccx, ccy = _child_center(node, q)
        node.children[q] = QuadTreeNode(ccx, ccy, node.size / 2.0)
    _insert(node.children[q], idx, x, y, m)


def compute_forces_tree(
    pos: np.ndarray,
    mass: np.ndarray,
    theta: float = 0.5,
    eps: float = 0.01,
) -> np.ndarray:
    """Compute gravitational accelerations using Barnes-Hut tree.

    Args:
        pos: Positions array, shape (N, 2).
        mass: Masses array, shape (N,).
        theta: Opening angle parameter (0 = exact, larger = faster/less accurate).
        eps: Plummer softening length.

    Returns:
        Accelerations array, shape (N, 2).
    """
    n = pos.shape[0]
    if n == 0:
        return np.zeros_like(pos)

    tree = build_tree(pos, mass)
    acc = np.zeros_like(pos)

    for i in range(n):
        ax, ay = _tree_force(tree, pos[i, 0], pos[i, 1], i, theta, eps)
        acc[i, 0] = ax
        acc[i, 1] = ay

    return acc


def _tree_force(
    node: QuadTreeNode,
    x: float,
    y: float,
    body_idx: int,
    theta: float,
    eps: float,
) -> Tuple[float, float]:
    """Recursively compute force on a body from a tree node.

    Uses the Barnes-Hut opening criterion: if s/d < theta, treat the
    node as a point mass at its center of mass.

    Returns:
        (ax, ay) acceleration components.
    """
    if node.total_mass == 0.0:
        return 0.0, 0.0

    dx = node.com_x - x
    dy = node.com_y - y
    r2 = dx * dx + dy * dy + eps * eps

    # Skip self-interaction
    if node.is_leaf and node.body_idx == body_idx:
        return 0.0, 0.0

    # Check opening criterion
    if node.is_leaf or (node.size * node.size / r2 < theta * theta):
        # Treat as point mass
        r_inv3 = r2 ** (-1.5)
        f = G * node.total_mass * r_inv3
        return f * dx, f * dy

    # Recurse into children
    ax, ay = 0.0, 0.0
    for child in node.children:
        if child is not None:
            cax, cay = _tree_force(child, x, y, body_idx, theta, eps)
            ax += cax
            ay += cay

    return ax, ay


def tree_depth(node: QuadTreeNode) -> int:
    """Compute the depth of the tree."""
    if node.is_leaf:
        return 1
    max_child = 0
    for child in node.children:
        if child is not None:
            max_child = max(max_child, tree_depth(child))
    return 1 + max_child


def tree_node_count(node: QuadTreeNode) -> int:
    """Count total nodes in the tree."""
    count = 1
    if not node.is_leaf:
        for child in node.children:
            if child is not None:
                count += tree_node_count(child)
    return count
