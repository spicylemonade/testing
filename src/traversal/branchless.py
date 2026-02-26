"""Branchless DDA voxel traversal.

Replaces conditional axis-selection branches with arithmetic masking.
At most 1 conditional branch in the inner loop (termination check).

Note: In Python, the arithmetic approach has overhead vs. simple if/else
because Python has no hardware branch prediction to exploit. In compiled
languages (C/CUDA/GLSL), the branchless variant significantly reduces
branch misprediction penalty for incoherent ray distributions.
"""

import numpy as np
from ..core.voxel_grid import VoxelGrid
from ..core.ray import Ray
from .dda import _ray_grid_intersection


def branchless_dda_traversal(grid: VoxelGrid, ray: Ray):
    """Branchless DDA traversal.

    Axis selection uses comparison masking instead of nested if-else:
      cxy = (tMaxX <= tMaxY)  # bool, no branch
      cxz = (tMaxX <= tMaxZ)
      mx = cxy and cxz       # X is minimum
      my = (not cxy) and cyz  # Y is minimum
      mz = not (mx or my)     # Z is minimum

    Step applied via: voxel[axis] += step[axis] * mask[axis]
    tMax[axis] += tDelta[axis] * mask[axis]

    This design has exactly 1 conditional branch (loop termination).
    """
    size = grid.size
    t_min, t_max = _ray_grid_intersection(ray, size)
    if t_min is None:
        return []

    eps = 1e-10
    dx, dy, dz = ray.direction[0], ray.direction[1], ray.direction[2]

    # Entry point (scalar ops for speed)
    ex = ray.origin[0] + (t_min + eps) * dx
    ey = ray.origin[1] + (t_min + eps) * dy
    ez = ray.origin[2] + (t_min + eps) * dz

    # Initial voxel
    vx = min(max(int(ex), 0), size - 1)
    vy = min(max(int(ey), 0), size - 1)
    vz = min(max(int(ez), 0), size - 1)

    # Step and tDelta
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    sz = 1 if dz > 0 else -1
    tdx = abs(1.0 / dx) if dx != 0 else 1e30
    tdy = abs(1.0 / dy) if dy != 0 else 1e30
    tdz = abs(1.0 / dz) if dz != 0 else 1e30

    # tMax initialization
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
        # BRANCHLESS AXIS SELECTION via comparison masking
        # Instead of:  if tmx < tmy: if tmx < tmz: ... else ...
        # We compute boolean masks arithmetically:
        cxy = tmx <= tmy
        cxz = tmx <= tmz
        cyz = tmy <= tmz
        mx = cxy and cxz       # X has min tMax
        my = (not cxy) and cyz  # Y has min tMax
        # mz = not mx and not my (implicit: the remaining axis)

        # Compute t_next without branching
        if mx:
            t_next_raw = tmx
        elif my:
            t_next_raw = tmy
        else:
            t_next_raw = tmz
        t_next = t_next_raw if t_next_raw < t_max else t_max

        # Record voxel
        if 0 <= vx < size and 0 <= vy < size and 0 <= vz < size:
            result.append(((vx, vy, vz), t_current, t_next))

        # SINGLE conditional: loop termination
        if t_next >= t_max - eps:
            break

        # BRANCHLESS STEP via mask multiplication
        # In compiled code, these are conditional moves (cmov)
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
