"""Barnes-Hut tree-based approximate force computation (2D quadtree).

Implements the hierarchical O(N log N) force calculation with monopole
and quadrupole moments for improved accuracy (Barnes & Hut 1986).
"""

import numpy as np
from src.bodies import System


class QuadTreeNode:
    """A node in the Barnes-Hut quadtree with monopole + quadrupole moments."""

    __slots__ = ('center', 'size', 'total_mass', 'com', 'quad',
                 'children', 'body_idx')

    def __init__(self, center: np.ndarray, size: float):
        self.center = center
        self.size = size
        self.total_mass = 0.0
        self.com = np.zeros(2)
        self.quad = np.zeros((2, 2))  # quadrupole moment tensor
        self.children = [None, None, None, None]
        self.body_idx = -1

    def is_leaf(self) -> bool:
        return all(c is None for c in self.children)

    def is_empty(self) -> bool:
        return self.total_mass == 0.0


def _quadrant(pos, center):
    """Return quadrant index (0=NW, 1=NE, 2=SW, 3=SE)."""
    ix = 0 if pos[0] < center[0] else 1
    iy = 0 if pos[1] >= center[1] else 2
    return ix + iy


def _child_center(parent_center, parent_size, quadrant):
    """Compute center of child cell given quadrant."""
    half = parent_size / 2
    dx = -half if quadrant % 2 == 0 else half
    dy = half if quadrant < 2 else -half
    return parent_center + np.array([dx, dy])


def build_tree(system: System) -> QuadTreeNode:
    """Build a Barnes-Hut quadtree from the system's particles."""
    pos = system.positions
    masses = system.masses

    min_pos = pos.min(axis=0)
    max_pos = pos.max(axis=0)
    center = 0.5 * (min_pos + max_pos)
    size = max(max_pos[0] - min_pos[0], max_pos[1] - min_pos[1]) / 2 * 1.01

    root = QuadTreeNode(center, size)

    for i in range(system.n):
        _insert(root, i, pos[i], masses[i])

    # Compute quadrupole moments bottom-up
    _compute_quadrupole(root, pos, masses)

    return root


def _insert(node: QuadTreeNode, idx: int, pos: np.ndarray, mass: float):
    """Insert a body into the quadtree (updates monopole = COM + total mass)."""
    if node.is_empty():
        node.total_mass = mass
        node.com = pos.copy()
        node.body_idx = idx
        return

    if node.is_leaf():
        old_idx = node.body_idx
        old_pos = node.com.copy()
        old_mass = node.total_mass
        node.body_idx = -1

        q = _quadrant(old_pos, node.center)
        child_center = _child_center(node.center, node.size, q)
        child_size = node.size / 2
        node.children[q] = QuadTreeNode(child_center, child_size)
        _insert(node.children[q], old_idx, old_pos, old_mass)

    q = _quadrant(pos, node.center)
    if node.children[q] is None:
        child_center = _child_center(node.center, node.size, q)
        child_size = node.size / 2
        node.children[q] = QuadTreeNode(child_center, child_size)
    _insert(node.children[q], idx, pos, mass)

    new_mass = node.total_mass + mass
    node.com = (node.com * node.total_mass + pos * mass) / new_mass
    node.total_mass = new_mass


def _compute_quadrupole(node, positions, masses):
    """Recursively compute the traceless quadrupole tensor for each node."""
    if node is None or node.is_empty():
        return

    if node.is_leaf():
        # Single body: quadrupole is zero (point mass at COM)
        node.quad = np.zeros((2, 2))
        return

    for child in node.children:
        _compute_quadrupole(child, positions, masses)

    # Compute Q_ij = sum_k m_k * (3 * dr_i * dr_j - |dr|^2 * delta_ij)
    # where dr = r_k - r_com
    # We accumulate from children using parallel axis theorem
    Q = np.zeros((2, 2))
    for child in node.children:
        if child is None or child.is_empty():
            continue
        # Child's contribution: its own quadrupole + parallel axis shift
        dr = child.com - node.com
        dr2 = np.dot(dr, dr)
        Q += child.quad + child.total_mass * (3 * np.outer(dr, dr) - dr2 * np.eye(2))
    node.quad = Q


def _compute_force_on_body(node, pos, G, eps2, theta, body_idx):
    """Compute gravitational acceleration on a body from the tree."""
    if node is None or node.is_empty():
        return np.zeros(2)

    diff = node.com - pos
    r2 = np.dot(diff, diff)
    dist2 = r2 + eps2

    if node.is_leaf():
        if node.body_idx == body_idx:
            return np.zeros(2)
        return G * node.total_mass * diff / (dist2 ** 1.5)

    # Opening angle criterion: s/d < theta
    s = 2 * node.size  # full cell width
    d = np.sqrt(r2)

    if d > 0 and s / d < theta:
        # Monopole contribution
        inv_dist3 = dist2 ** (-1.5)
        acc = G * node.total_mass * diff * inv_dist3

        # Quadrupole correction: a = G*(-Q.r/|r|^5 + 5/2 * (r^T Q r)*r/|r|^7)
        # where r = com - pos = diff, Q is the traceless quadrupole tensor
        inv_dist5 = dist2 ** (-2.5)
        inv_dist7 = dist2 ** (-3.5)
        Qd = node.quad @ diff
        dQd = np.dot(diff, Qd)
        acc += G * (-inv_dist5 * Qd + 2.5 * inv_dist7 * dQd * diff)

        return acc

    # Recurse into children
    acc = np.zeros(2)
    for child in node.children:
        acc += _compute_force_on_body(child, pos, G, eps2, theta, body_idx)
    return acc


def compute_forces_barnes_hut(system: System, theta: float = 0.5) -> np.ndarray:
    """Compute gravitational accelerations using Barnes-Hut tree.

    Args:
        system: N-body system
        theta: opening angle (0 = exact, larger = faster but less accurate)

    Returns:
        accelerations: (N, dim) array
    """
    tree = build_tree(system)
    G = system.G
    eps2 = system.epsilon ** 2
    acc = np.zeros_like(system.positions)

    for i in range(system.n):
        acc[i] = _compute_force_on_body(tree, system.positions[i], G, eps2, theta, i)

    return acc
