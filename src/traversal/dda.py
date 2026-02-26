"""Amanatides-Woo DDA voxel traversal (1987).

Returns ordered list of (voxel_index, t_enter, t_exit) for all voxels
intersected by a ray through a uniform grid.
"""

import numpy as np
from ..core.voxel_grid import VoxelGrid
from ..core.ray import Ray


def _ray_grid_intersection(ray: Ray, grid_size: int):
    """Compute t_min and t_max where ray enters/exits the [0, grid_size]^3 box.

    Returns (t_min, t_max) or (None, None) if ray misses the grid.
    """
    inv_dir = ray.inv_direction
    t0 = (0.0 - ray.origin) * inv_dir
    t1 = (float(grid_size) - ray.origin) * inv_dir

    t_enter = np.minimum(t0, t1)
    t_exit = np.maximum(t0, t1)

    t_min = np.max(t_enter)
    t_max = np.min(t_exit)

    # Handle rays with zero direction components
    for i in range(3):
        if ray.direction[i] == 0.0:
            if ray.origin[i] < 0.0 or ray.origin[i] > grid_size:
                return None, None

    if t_max < max(t_min, 0.0):
        return None, None

    t_min = max(t_min, 0.0)
    return t_min, t_max


def dda_traversal(grid: VoxelGrid, ray: Ray):
    """Amanatides-Woo DDA traversal.

    Args:
        grid: VoxelGrid to traverse
        ray: Ray to cast through the grid

    Returns:
        List of (voxel_tuple, t_enter, t_exit) for each traversed voxel.
        voxel_tuple is (x, y, z) integer indices.
    """
    size = grid.size
    t_min, t_max = _ray_grid_intersection(ray, size)
    if t_min is None:
        return []

    # Entry point
    eps = 1e-10
    entry = ray.at(t_min + eps)

    # Initial voxel
    voxel = [int(np.floor(entry[i])) for i in range(3)]
    for i in range(3):
        voxel[i] = max(0, min(size - 1, voxel[i]))

    # Step direction
    step = [0, 0, 0]
    t_delta = [np.inf, np.inf, np.inf]
    t_max_arr = [np.inf, np.inf, np.inf]

    for i in range(3):
        if ray.direction[i] > 0:
            step[i] = 1
            t_delta[i] = 1.0 / ray.direction[i]
            # Distance to next boundary in this axis
            boundary = voxel[i] + 1.0
            t_max_arr[i] = t_min + (boundary - entry[i]) / ray.direction[i]
        elif ray.direction[i] < 0:
            step[i] = -1
            t_delta[i] = 1.0 / abs(ray.direction[i])
            boundary = float(voxel[i])
            t_max_arr[i] = t_min + (boundary - entry[i]) / ray.direction[i]
        else:
            step[i] = 0
            t_delta[i] = np.inf
            t_max_arr[i] = np.inf

    result = []
    t_current = t_min

    while True:
        # Find which axis has the smallest tMax
        min_axis = 0
        if t_max_arr[1] < t_max_arr[min_axis]:
            min_axis = 1
        if t_max_arr[2] < t_max_arr[min_axis]:
            min_axis = 2

        t_next = min(t_max_arr[min_axis], t_max)

        # Record this voxel
        if 0 <= voxel[0] < size and 0 <= voxel[1] < size and 0 <= voxel[2] < size:
            result.append((tuple(voxel), t_current, t_next))

        if t_next >= t_max - eps:
            break

        # Step along the axis with smallest tMax
        voxel[min_axis] += step[min_axis]
        t_current = t_max_arr[min_axis]
        t_max_arr[min_axis] += t_delta[min_axis]

        # Check bounds
        if voxel[min_axis] < 0 or voxel[min_axis] >= size:
            break

    return result
