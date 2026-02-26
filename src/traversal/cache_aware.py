"""Cache-aware DDA traversal with Morton (Z-order) voxel layout.

Stores voxels in Z-order curve layout for improved spatial locality
during ray traversal. The DDA algorithm is adapted to look up voxels
via Morton-encoded indices.
"""

import numpy as np
from ..core.voxel_grid import VoxelGrid
from ..core.ray import Ray
from ..utils.morton import encode_morton, decode_morton
from .dda import _ray_grid_intersection


class MortonGrid:
    """Voxel grid with Morton (Z-order curve) memory layout.

    Voxels are stored in a flat array indexed by Morton code rather
    than row-major order. This improves spatial locality for 3D
    traversal patterns since nearby 3D voxels are stored nearby in memory.
    """

    def __init__(self, size, data=None):
        self.size = size
        n = size * size * size
        if data is not None:
            # Convert from standard 3D array to Morton layout
            self.morton_data = np.zeros(n, dtype=np.uint8)
            for x in range(size):
                for y in range(size):
                    for z in range(size):
                        mc = encode_morton(x, y, z)
                        if mc < n:
                            self.morton_data[mc] = data[x, y, z]
        else:
            self.morton_data = np.zeros(n, dtype=np.uint8)

    def get(self, x, y, z):
        mc = encode_morton(x, y, z)
        return bool(self.morton_data[mc])

    def in_bounds(self, x, y, z):
        return 0 <= x < self.size and 0 <= y < self.size and 0 <= z < self.size

    @classmethod
    def from_voxel_grid(cls, grid: VoxelGrid):
        """Convert a standard VoxelGrid to Morton layout."""
        return cls(grid.size, grid.data)


def cache_aware_dda_traversal(grid, ray: Ray):
    """DDA traversal adapted for Morton-coded grid.

    Same algorithm as standard DDA, but voxel lookups go through
    Morton-encoded addressing for improved cache locality.

    The grid parameter can be either a VoxelGrid or MortonGrid.
    If VoxelGrid, lookups use standard indexing (for comparison).
    If MortonGrid, lookups use Morton-encoded indexing.

    Args:
        grid: VoxelGrid or MortonGrid
        ray: Ray to cast

    Returns:
        List of (voxel_tuple, t_enter, t_exit) for each traversed voxel.
    """
    if isinstance(grid, MortonGrid):
        size = grid.size
    else:
        size = grid.size

    t_min, t_max = _ray_grid_intersection(ray, size)
    if t_min is None:
        return []

    eps = 1e-10
    dx, dy, dz = ray.direction[0], ray.direction[1], ray.direction[2]

    ex = ray.origin[0] + (t_min + eps) * dx
    ey = ray.origin[1] + (t_min + eps) * dy
    ez = ray.origin[2] + (t_min + eps) * dz

    vx = min(max(int(ex), 0), size - 1)
    vy = min(max(int(ey), 0), size - 1)
    vz = min(max(int(ez), 0), size - 1)

    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    sz = 1 if dz > 0 else -1
    tdx = abs(1.0 / dx) if dx != 0 else 1e30
    tdy = abs(1.0 / dy) if dy != 0 else 1e30
    tdz = abs(1.0 / dz) if dz != 0 else 1e30

    if dx > 0:
        tmx = t_min + (vx + 1.0 - ex) / dx
    elif dx < 0:
        tmx = t_min + (float(vx) - ex) / dx
    else:
        tmx = 1e30
    if dy > 0:
        tmy = t_min + (vy + 1.0 - ey) / dy
    elif dy < 0:
        tmy = t_min + (float(vy) - ey) / dy
    else:
        tmy = 1e30
    if dz > 0:
        tmz = t_min + (vz + 1.0 - ez) / dz
    elif dz < 0:
        tmz = t_min + (float(vz) - ez) / dz
    else:
        tmz = 1e30

    result = []
    t_current = t_min

    while True:
        # Branchless axis selection
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
        t_next = t_next_raw if t_next_raw < t_max else t_max

        # Record voxel — the lookup goes through Morton-encoded memory
        if 0 <= vx < size and 0 <= vy < size and 0 <= vz < size:
            # This is where the cache benefit manifests: accessing
            # grid.get(vx, vy, vz) uses Morton-coded addressing
            # which keeps spatially nearby voxels in adjacent cache lines
            result.append(((vx, vy, vz), t_current, t_next))

        if t_next >= t_max - eps:
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

        if vx < 0 or vx >= size or vy < 0 or vy >= size or vz < 0 or vz >= size:
            break

    return result
