"""Barnes-Hut O(N log N) gravitational force computation.

Implements a 2D quadtree with center-of-mass approximation
for hierarchical force evaluation.

Reference: Barnes & Hut (1986), Pfalzner & Gibbon (1996)
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np


class QuadTreeNode:
    """A node in the Barnes-Hut quadtree.

    Attributes:
        center: (2,) center of the bounding box.
        size: Side length of the bounding box.
        mass: Total mass of bodies in this node.
        com: (2,) center of mass position.
        body_index: Index of the body if this is a leaf with one body.
        children: List of 4 child nodes (NW, NE, SW, SE) or None.
    """

    __slots__ = ("center", "size", "mass", "com", "body_index", "children")

    def __init__(self, center: np.ndarray, size: float):
        self.center = center
        self.size = size
        self.mass: float = 0.0
        self.com: np.ndarray = np.zeros(2)
        self.body_index: Optional[int] = None
        self.children: Optional[List[Optional[QuadTreeNode]]] = None

    def is_leaf(self) -> bool:
        return self.children is None

    def is_empty(self) -> bool:
        return self.mass == 0.0


def _quadrant(pos: np.ndarray, center: np.ndarray) -> int:
    """Determine which quadrant a position falls in.

    Returns 0=NW, 1=NE, 2=SW, 3=SE.
    """
    ix = 1 if pos[0] >= center[0] else 0
    iy = 0 if pos[1] >= center[1] else 2
    return ix + iy


def _child_center(parent_center: np.ndarray, quadrant: int, half_size: float) -> np.ndarray:
    """Compute the center of a child quadrant."""
    offset = half_size / 2
    dx = offset if (quadrant & 1) else -offset
    dy = offset if (quadrant < 2) else -offset
    return parent_center + np.array([dx, dy])


def build_quadtree(
    masses: np.ndarray,
    positions: np.ndarray,
) -> QuadTreeNode:
    """Build a Barnes-Hut quadtree from body data.

    Args:
        masses: (N,) mass array.
        positions: (N, 2) position array.

    Returns:
        Root QuadTreeNode.
    """
    n = len(masses)
    if n == 0:
        return QuadTreeNode(np.zeros(2), 1.0)

    # Determine bounding box
    min_pos = positions.min(axis=0)
    max_pos = positions.max(axis=0)
    center = 0.5 * (min_pos + max_pos)
    size = max(max_pos[0] - min_pos[0], max_pos[1] - min_pos[1]) * 1.01 + 1e-10

    root = QuadTreeNode(center, size)

    for i in range(n):
        _insert(root, i, masses[i], positions[i])

    return root


def _insert(node: QuadTreeNode, idx: int, mass: float, pos: np.ndarray):
    """Insert a body into the quadtree."""
    if node.is_empty():
        # Empty leaf: just store the body
        node.mass = mass
        node.com = pos.copy()
        node.body_index = idx
        return

    if node.is_leaf():
        # Occupied leaf: subdivide
        old_idx = node.body_index
        old_mass = node.mass
        old_com = node.com.copy()

        node.children = [None, None, None, None]
        node.body_index = None

        # Re-insert the existing body
        _insert_into_children(node, old_idx, old_mass, old_com)

    # Insert new body into children
    _insert_into_children(node, idx, mass, pos)

    # Update center of mass
    total_mass = node.mass + mass
    node.com = (node.mass * node.com + mass * pos) / total_mass
    node.mass = total_mass


def _insert_into_children(node: QuadTreeNode, idx: int, mass: float, pos: np.ndarray):
    """Insert a body into the appropriate child of an internal node."""
    q = _quadrant(pos, node.center)
    half_size = node.size / 2

    if node.children[q] is None:
        child_center = _child_center(node.center, q, node.size)
        node.children[q] = QuadTreeNode(child_center, half_size)

    _insert(node.children[q], idx, mass, pos)


def compute_forces_barnes_hut(
    masses: np.ndarray,
    positions: np.ndarray,
    G: float = 1.0,
    epsilon: float = 0.01,
    theta: float = 0.5,
) -> np.ndarray:
    """Compute gravitational accelerations using Barnes-Hut algorithm.

    Args:
        masses: (N,) mass array.
        positions: (N, 2) position array.
        G: Gravitational constant.
        epsilon: Softening length.
        theta: Opening angle (accuracy parameter). Smaller = more accurate.

    Returns:
        (N, 2) acceleration array.
    """
    n = len(masses)
    if n == 0:
        return np.zeros((0, 2))
    if n == 1:
        return np.zeros((1, 2))

    root = build_quadtree(masses, positions)
    accelerations = np.zeros((n, 2))

    for i in range(n):
        accelerations[i] = _compute_force_on_body(
            root, i, positions[i], G, epsilon, theta
        )

    return accelerations


def _compute_force_on_body(
    node: QuadTreeNode,
    body_idx: int,
    body_pos: np.ndarray,
    G: float,
    epsilon: float,
    theta: float,
) -> np.ndarray:
    """Recursively compute force on a single body from a tree node."""
    if node.is_empty():
        return np.zeros(2)

    diff = node.com - body_pos
    dist_sq = np.dot(diff, diff) + epsilon ** 2
    dist = np.sqrt(dist_sq)

    if node.is_leaf():
        # Leaf node: compute direct force (skip self)
        if node.body_index == body_idx:
            return np.zeros(2)
        return G * node.mass * diff / (dist_sq * dist)

    # Internal node: check opening angle criterion
    if node.size / dist < theta:
        # Far enough: use center-of-mass approximation
        return G * node.mass * diff / (dist_sq * dist)

    # Too close: recurse into children
    acc = np.zeros(2)
    for child in node.children:
        if child is not None:
            acc += _compute_force_on_body(
                child, body_idx, body_pos, G, epsilon, theta
            )
    return acc
