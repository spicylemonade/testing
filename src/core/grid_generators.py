"""Grid generators: produce test VoxelGrid instances for benchmarking."""

import numpy as np
from .voxel_grid import VoxelGrid


def empty_grid(size: int) -> VoxelGrid:
    """Fully empty grid."""
    return VoxelGrid(size)


def full_grid(size: int) -> VoxelGrid:
    """Fully occupied grid."""
    data = np.ones((size, size, size), dtype=np.uint8)
    return VoxelGrid(size, data)


def random_grid(size: int, density: float = 0.5, seed: int = 42) -> VoxelGrid:
    """Random occupancy grid at configurable density."""
    rng = np.random.RandomState(seed)
    data = (rng.random((size, size, size)) < density).astype(np.uint8)
    return VoxelGrid(size, data)


def sphere_shell_grid(size: int, radius_frac: float = 0.4,
                      thickness_frac: float = 0.05) -> VoxelGrid:
    """Spherical shell centered in the grid."""
    center = size / 2.0
    radius = radius_frac * size
    thickness = thickness_frac * size

    coords = np.arange(size) + 0.5
    x, y, z = np.meshgrid(coords, coords, coords, indexing='ij')
    dist = np.sqrt((x - center)**2 + (y - center)**2 + (z - center)**2)
    data = ((dist >= radius - thickness / 2) &
            (dist <= radius + thickness / 2)).astype(np.uint8)
    return VoxelGrid(size, data)


def axis_planes_grid(size: int, thickness: int = 1) -> VoxelGrid:
    """Three axis-aligned planes through the center of the grid."""
    data = np.zeros((size, size, size), dtype=np.uint8)
    mid = size // 2
    half_t = max(1, thickness // 2)
    # XY plane (constant Z)
    data[:, :, mid - half_t:mid + half_t] = 1
    # XZ plane (constant Y)
    data[:, mid - half_t:mid + half_t, :] = 1
    # YZ plane (constant X)
    data[mid - half_t:mid + half_t, :, :] = 1
    return VoxelGrid(size, data)
