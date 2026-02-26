"""Hierarchical two-level DDA with bitmask-based empty space skipping.

Uses coarse blocks (bricks) with per-block occupancy bitmask at the
top level, and fine per-voxel DDA within occupied blocks. Empty blocks
are skipped entirely, providing significant speedup on sparse grids.

Inspired by MultiDDA/XBrickMap approaches from VoxelRT.
"""

import numpy as np
from ..core.voxel_grid import VoxelGrid
from ..core.ray import Ray
from .dda import _ray_grid_intersection


class HierarchicalGrid:
    """Two-level voxel grid with per-brick occupancy bitmask.

    The grid is divided into bricks of BRICK_SIZE^3 voxels.
    Each brick has an occupancy flag (occupied if any voxel is set).
    The coarse-level DDA skips empty bricks entirely.
    """

    BRICK_SIZE = 8  # 8^3 = 512 voxels per brick

    def __init__(self, grid: VoxelGrid):
        self.size = grid.size
        self.data = grid.data
        bs = self.BRICK_SIZE
        self.n_bricks = (grid.size + bs - 1) // bs

        # Build occupancy bitmask: one bool per brick
        self.brick_occupied = np.zeros(
            (self.n_bricks, self.n_bricks, self.n_bricks), dtype=np.uint8
        )
        for bx in range(self.n_bricks):
            for by in range(self.n_bricks):
                for bz in range(self.n_bricks):
                    x0, x1 = bx * bs, min((bx + 1) * bs, grid.size)
                    y0, y1 = by * bs, min((by + 1) * bs, grid.size)
                    z0, z1 = bz * bs, min((bz + 1) * bs, grid.size)
                    if np.any(grid.data[x0:x1, y0:y1, z0:z1]):
                        self.brick_occupied[bx, by, bz] = 1

    @classmethod
    def from_voxel_grid(cls, grid: VoxelGrid):
        return cls(grid)


def hierarchical_traversal(grid, ray: Ray):
    """Two-level hierarchical DDA traversal.

    Level 1 (coarse): DDA over brick grid, skipping empty bricks.
    Level 2 (fine): DDA over voxels within each occupied brick.

    Args:
        grid: VoxelGrid or HierarchicalGrid
        ray: Ray to cast

    Returns:
        List of (voxel_tuple, t_enter, t_exit) for each traversed voxel.
    """
    if isinstance(grid, HierarchicalGrid):
        hgrid = grid
    else:
        hgrid = HierarchicalGrid(grid)

    size = hgrid.size
    bs = hgrid.BRICK_SIZE
    n_bricks = hgrid.n_bricks

    # Coarse-level: DDA over brick grid
    t_min, t_max = _ray_grid_intersection(ray, size)
    if t_min is None:
        return []

    eps = 1e-10
    dx, dy, dz = ray.direction[0], ray.direction[1], ray.direction[2]

    # Entry point into the grid
    ex = ray.origin[0] + (t_min + eps) * dx
    ey = ray.origin[1] + (t_min + eps) * dy
    ez = ray.origin[2] + (t_min + eps) * dz

    # Coarse-level DDA (brick coordinates)
    brick_size_f = float(bs)

    # Convert entry to brick coordinates
    bx = min(max(int(ex / brick_size_f), 0), n_bricks - 1)
    by = min(max(int(ey / brick_size_f), 0), n_bricks - 1)
    bz = min(max(int(ez / brick_size_f), 0), n_bricks - 1)

    # Steps in brick space
    bsx = 1 if dx > 0 else -1
    bsy = 1 if dy > 0 else -1
    bsz = 1 if dz > 0 else -1

    # tDelta for brick-level step
    btdx = abs(brick_size_f / dx) if dx != 0 else 1e30
    btdy = abs(brick_size_f / dy) if dy != 0 else 1e30
    btdz = abs(brick_size_f / dz) if dz != 0 else 1e30

    # tMax for brick boundaries
    if dx > 0:
        btmx = t_min + ((bx + 1) * brick_size_f - ex) / dx
    elif dx < 0:
        btmx = t_min + (bx * brick_size_f - ex) / dx
    else:
        btmx = 1e30
    if dy > 0:
        btmy = t_min + ((by + 1) * brick_size_f - ey) / dy
    elif dy < 0:
        btmy = t_min + (by * brick_size_f - ey) / dy
    else:
        btmy = 1e30
    if dz > 0:
        btmz = t_min + ((bz + 1) * brick_size_f - ez) / dz
    elif dz < 0:
        btmz = t_min + (bz * brick_size_f - ez) / dz
    else:
        btmz = 1e30

    result = []
    bt_current = t_min

    while True:
        # Coarse-level axis selection (branchless)
        cxy = btmx <= btmy
        cxz = btmx <= btmz
        cyz = btmy <= btmz
        bmx = cxy and cxz
        bmy = (not cxy) and cyz

        if bmx:
            bt_next = btmx
        elif bmy:
            bt_next = btmy
        else:
            bt_next = btmz
        bt_next = min(bt_next, t_max)

        # Check if this brick is occupied
        if (0 <= bx < n_bricks and 0 <= by < n_bricks and 0 <= bz < n_bricks
                and hgrid.brick_occupied[bx, by, bz]):
            # FINE-LEVEL DDA within this brick
            _traverse_brick(ray, hgrid, bx, by, bz, bs, size,
                            bt_current, bt_next, result)

        if bt_next >= t_max - eps:
            break

        # Step to next brick
        if bmx:
            bx += bsx
            bt_current = btmx
            btmx += btdx
        elif bmy:
            by += bsy
            bt_current = btmy
            btmy += btdy
        else:
            bz += bsz
            bt_current = btmz
            btmz += btdz

        if bx < 0 or bx >= n_bricks or by < 0 or by >= n_bricks or bz < 0 or bz >= n_bricks:
            break

    return result


def _traverse_brick(ray, hgrid, bx, by, bz, bs, size, t_enter, t_exit, result):
    """Fine-level DDA within a single brick."""
    dx, dy, dz = ray.direction[0], ray.direction[1], ray.direction[2]
    eps = 1e-10

    # Clamp entry/exit to brick bounds
    bx0 = bx * bs
    by0 = by * bs
    bz0 = bz * bs

    # Entry point for this brick
    ex = ray.origin[0] + (t_enter + eps) * dx
    ey = ray.origin[1] + (t_enter + eps) * dy
    ez = ray.origin[2] + (t_enter + eps) * dz

    vx = min(max(int(ex), bx0), min(bx0 + bs - 1, size - 1))
    vy = min(max(int(ey), by0), min(by0 + bs - 1, size - 1))
    vz = min(max(int(ez), bz0), min(bz0 + bs - 1, size - 1))

    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    sz = 1 if dz > 0 else -1
    tdx = abs(1.0 / dx) if dx != 0 else 1e30
    tdy = abs(1.0 / dy) if dy != 0 else 1e30
    tdz = abs(1.0 / dz) if dz != 0 else 1e30

    if dx > 0:
        tmx = t_enter + (vx + 1.0 - ex) / dx
    elif dx < 0:
        tmx = t_enter + (float(vx) - ex) / dx
    else:
        tmx = 1e30
    if dy > 0:
        tmy = t_enter + (vy + 1.0 - ey) / dy
    elif dy < 0:
        tmy = t_enter + (float(vy) - ey) / dy
    else:
        tmy = 1e30
    if dz > 0:
        tmz = t_enter + (vz + 1.0 - ez) / dz
    elif dz < 0:
        tmz = t_enter + (float(vz) - ez) / dz
    else:
        tmz = 1e30

    t_current = t_enter
    bx1 = min(bx0 + bs, size)
    by1 = min(by0 + bs, size)
    bz1 = min(bz0 + bs, size)

    while True:
        cxy = tmx <= tmy
        cxz = tmx <= tmz
        cyz = tmy <= tmz
        mx = cxy and cxz
        my = (not cxy) and cyz

        if mx:
            t_next_raw = tmx
        elif my:
            t_next_raw = tmy
        else:
            t_next_raw = tmz
        t_next = min(t_next_raw, t_exit)

        if 0 <= vx < size and 0 <= vy < size and 0 <= vz < size:
            result.append(((vx, vy, vz), t_current, t_next))

        if t_next >= t_exit - eps:
            break

        if mx:
            vx += sx
            t_current = tmx
            tmx += tdx
        elif my:
            vy += sy
            t_current = tmy
            tmy += tdy
        else:
            vz += sz
            t_current = tmz
            tmz += tdz

        if vx < bx0 or vx >= bx1 or vy < by0 or vy >= by1 or vz < bz0 or vz >= bz1:
            break
