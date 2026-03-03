from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class QuadNode:
    cx: float
    cy: float
    half: float
    body_indices: list[int] = field(default_factory=list)
    children: list["QuadNode"] | None = None
    mass: float = 0.0
    com_x: float = 0.0
    com_y: float = 0.0
    n_bodies: int = 0

    @property
    def is_leaf(self) -> bool:
        return self.children is None


def _accelerations_direct(positions: np.ndarray, masses: np.ndarray, g: float, softening: float) -> np.ndarray:
    n = positions.shape[0]
    acc = np.zeros_like(positions, dtype=np.float64)
    eps2 = softening * softening
    for i in range(n):
        for j in range(i + 1, n):
            delta = positions[j] - positions[i]
            r2 = float(delta[0] * delta[0] + delta[1] * delta[1] + eps2)
            inv_r = 1.0 / np.sqrt(r2)
            inv_r3 = inv_r / r2
            force = g * delta * inv_r3
            acc[i] += masses[j] * force
            acc[j] -= masses[i] * force
    return acc


def _compute_root_bounds(positions: np.ndarray) -> tuple[float, float, float]:
    min_xy = positions.min(axis=0)
    max_xy = positions.max(axis=0)
    center = 0.5 * (min_xy + max_xy)
    extent = float(max(max_xy[0] - min_xy[0], max_xy[1] - min_xy[1]))
    half = max(1e-3, 0.5 * extent + 1e-6)
    return float(center[0]), float(center[1]), half


def _subdivide(node: QuadNode) -> None:
    q = 0.5 * node.half
    node.children = [
        QuadNode(node.cx - q, node.cy - q, q),
        QuadNode(node.cx + q, node.cy - q, q),
        QuadNode(node.cx - q, node.cy + q, q),
        QuadNode(node.cx + q, node.cy + q, q),
    ]


def _child_index(node: QuadNode, x: float, y: float) -> int:
    ix = 1 if x >= node.cx else 0
    iy = 1 if y >= node.cy else 0
    return iy * 2 + ix


def _insert(node: QuadNode, idx: int, positions: np.ndarray, leaf_size: int, min_half: float) -> None:
    x, y = float(positions[idx, 0]), float(positions[idx, 1])

    if node.is_leaf:
        if len(node.body_indices) < leaf_size or node.half <= min_half:
            node.body_indices.append(idx)
            return

        existing = list(node.body_indices)
        node.body_indices.clear()
        _subdivide(node)
        for ex in existing:
            exx, exy = float(positions[ex, 0]), float(positions[ex, 1])
            child = node.children[_child_index(node, exx, exy)]
            _insert(child, ex, positions, leaf_size, min_half)

    child = node.children[_child_index(node, x, y)]
    _insert(child, idx, positions, leaf_size, min_half)


def _accumulate_mass(node: QuadNode, positions: np.ndarray, masses: np.ndarray) -> tuple[float, float, float, int]:
    if node.is_leaf:
        if not node.body_indices:
            node.mass = 0.0
            node.com_x = node.cx
            node.com_y = node.cy
            node.n_bodies = 0
            return node.mass, node.com_x, node.com_y, node.n_bodies

        total_m = 0.0
        cx = 0.0
        cy = 0.0
        for idx in node.body_indices:
            m = float(masses[idx])
            total_m += m
            cx += m * float(positions[idx, 0])
            cy += m * float(positions[idx, 1])
        node.mass = total_m
        node.com_x = cx / total_m
        node.com_y = cy / total_m
        node.n_bodies = len(node.body_indices)
        return node.mass, node.com_x, node.com_y, node.n_bodies

    total_m = 0.0
    cx = 0.0
    cy = 0.0
    total_n = 0
    for child in node.children:
        cm, ccx, ccy, cn = _accumulate_mass(child, positions, masses)
        total_m += cm
        cx += cm * ccx
        cy += cm * ccy
        total_n += cn

    if total_m <= 0.0:
        node.mass = 0.0
        node.com_x = node.cx
        node.com_y = node.cy
        node.n_bodies = 0
    else:
        node.mass = total_m
        node.com_x = cx / total_m
        node.com_y = cy / total_m
        node.n_bodies = total_n

    return node.mass, node.com_x, node.com_y, node.n_bodies


def _contains(node: QuadNode, x: float, y: float) -> bool:
    return (abs(x - node.cx) <= node.half) and (abs(y - node.cy) <= node.half)


def _acc_body(
    node: QuadNode,
    i: int,
    px: float,
    py: float,
    positions: np.ndarray,
    masses: np.ndarray,
    g: float,
    softening: float,
    theta: float,
) -> tuple[float, float]:
    if node.mass <= 0.0 or node.n_bodies == 0:
        return 0.0, 0.0

    if node.is_leaf:
        ax = 0.0
        ay = 0.0
        eps2 = softening * softening
        for j in node.body_indices:
            if j == i:
                continue
            dx = float(positions[j, 0]) - px
            dy = float(positions[j, 1]) - py
            r2 = dx * dx + dy * dy + eps2
            inv_r = 1.0 / np.sqrt(r2)
            inv_r3 = inv_r / r2
            scale = g * float(masses[j]) * inv_r3
            ax += scale * dx
            ay += scale * dy
        return ax, ay

    dx = node.com_x - px
    dy = node.com_y - py
    r2 = dx * dx + dy * dy + softening * softening
    r = np.sqrt(r2)
    s = 2.0 * node.half

    contains = _contains(node, px, py)
    if (not contains) and (s / max(1e-15, r) < theta):
        inv_r3 = 1.0 / (r2 * r)
        scale = g * node.mass * inv_r3
        return scale * dx, scale * dy

    ax = 0.0
    ay = 0.0
    for child in node.children:
        cax, cay = _acc_body(child, i, px, py, positions, masses, g, softening, theta)
        ax += cax
        ay += cay
    return ax, ay


def accelerations_barnes_hut(
    positions: np.ndarray,
    masses: np.ndarray,
    g: float,
    softening: float,
    theta: float = 0.7,
    leaf_size: int = 8,
    min_n_direct: int = 64,
) -> np.ndarray:
    n = positions.shape[0]
    if n < min_n_direct:
        return _accelerations_direct(positions, masses, g, softening)

    cx, cy, half = _compute_root_bounds(positions)
    root = QuadNode(cx, cy, half)
    min_half = max(1e-6, half * 1e-6)
    for idx in range(n):
        _insert(root, idx, positions, leaf_size=max(1, leaf_size), min_half=min_half)
    _accumulate_mass(root, positions, masses)

    acc = np.zeros_like(positions, dtype=np.float64)
    for i in range(n):
        px = float(positions[i, 0])
        py = float(positions[i, 1])
        ax, ay = _acc_body(root, i, px, py, positions, masses, g, softening, theta)
        acc[i, 0] = ax
        acc[i, 1] = ay
    return acc
