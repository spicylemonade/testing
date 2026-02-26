"""3D Bresenham / supercover voxel traversal.

Enumerates all voxels intersected by a line segment between two 3D points.
Supports 6-connected (supercover) and 26-connected modes.
"""

import numpy as np


def bresenham_traversal(p0, p1, connectivity=26):
    """3D Bresenham-based voxel traversal.

    Args:
        p0: Start point (3D float array) — will be floored to voxel coords
        p1: End point (3D float array) — will be floored to voxel coords
        connectivity: 6 for supercover (visits all voxels line touches),
                      26 for thin line (standard Bresenham)

    Returns:
        List of (x, y, z) voxel tuples traversed.
    """
    p0 = np.asarray(p0, dtype=np.float64)
    p1 = np.asarray(p1, dtype=np.float64)

    x0, y0, z0 = int(np.floor(p0[0])), int(np.floor(p0[1])), int(np.floor(p0[2]))
    x1, y1, z1 = int(np.floor(p1[0])), int(np.floor(p1[1])), int(np.floor(p1[2]))

    if connectivity == 6:
        return _supercover_3d(x0, y0, z0, x1, y1, z1)
    else:
        return _bresenham_3d_26(x0, y0, z0, x1, y1, z1)


def _bresenham_3d_26(x0, y0, z0, x1, y1, z1):
    """Standard 3D Bresenham: 26-connected (thin) line."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    dz = abs(z1 - z0)

    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    sz = 1 if z1 > z0 else -1

    result = []
    x, y, z = x0, y0, z0

    # Determine dominant axis
    if dx >= dy and dx >= dz:
        # X dominant
        err_y = 2 * dy - dx
        err_z = 2 * dz - dx
        for _ in range(dx + 1):
            result.append((x, y, z))
            if err_y > 0:
                y += sy
                err_y -= 2 * dx
            if err_z > 0:
                z += sz
                err_z -= 2 * dx
            err_y += 2 * dy
            err_z += 2 * dz
            x += sx
    elif dy >= dx and dy >= dz:
        # Y dominant
        err_x = 2 * dx - dy
        err_z = 2 * dz - dy
        for _ in range(dy + 1):
            result.append((x, y, z))
            if err_x > 0:
                x += sx
                err_x -= 2 * dy
            if err_z > 0:
                z += sz
                err_z -= 2 * dy
            err_x += 2 * dx
            err_z += 2 * dz
            y += sy
    else:
        # Z dominant
        err_x = 2 * dx - dz
        err_y = 2 * dy - dz
        for _ in range(dz + 1):
            result.append((x, y, z))
            if err_x > 0:
                x += sx
                err_x -= 2 * dz
            if err_y > 0:
                y += sy
                err_y -= 2 * dz
            err_x += 2 * dx
            err_y += 2 * dy
            z += sz

    return result


def _supercover_3d(x0, y0, z0, x1, y1, z1):
    """Supercover 3D line voxelization: 6-connected, visits ALL voxels
    that the continuous line segment passes through.

    Based on the 3D extension of the 2D supercover algorithm.
    """
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    dz = abs(z1 - z0)

    sx = 1 if x1 >= x0 else -1
    sy = 1 if y1 >= y0 else -1
    sz = 1 if z1 >= z0 else -1

    x, y, z = x0, y0, z0
    result = [(x, y, z)]

    # Error terms: 2*dy*dx cross products for axis comparisons
    # We use a DDA-like approach with careful handling of ties
    if dx == 0 and dy == 0 and dz == 0:
        return result

    # Error accumulators — using scaled integer arithmetic
    # err_xy > 0 means we should step in Y before X (or both)
    ax = 2 * dx
    ay = 2 * dy
    az = 2 * dz

    # t-like error terms for each axis
    # We track when each axis "should" step next
    n = dx + dy + dz  # maximum number of steps

    err_x = dx
    err_y = dy
    err_z = dz

    # Threshold: half the sum
    for _ in range(n):
        # Find which axis has crossed threshold first
        # The one with the largest error / delta ratio steps first
        # We compare: err_x/dx vs err_y/dy vs err_z/dz
        # Equivalently: err_x*dy*dz vs err_y*dx*dz vs err_z*dx*dy

        # Simplified: compare scaled errors
        ex = err_x * (ay if dy > 0 else 1) * (az if dz > 0 else 1) if dx > 0 else -1
        ey = err_y * (ax if dx > 0 else 1) * (az if dz > 0 else 1) if dy > 0 else -1
        ez = err_z * (ax if dx > 0 else 1) * (ay if dy > 0 else 1) if dz > 0 else -1

        if ex >= ey and ex >= ez and dx > 0:
            x += sx
            err_x -= 1
            # Check if Y or Z should also step (supercover: emit intermediate voxels)
            if dy > 0 and err_y * dx >= err_x * dy:
                result.append((x - sx, y + sy, z))
                y += sy
                err_y -= 1
            if dz > 0 and err_z * dx >= err_x * dz:
                result.append((x - sx, y, z))  # may need previous x
                z += sz
                err_z -= 1
        elif ey >= ez and dy > 0:
            y += sy
            err_y -= 1
            if dz > 0 and err_z * dy >= err_y * dz:
                result.append((x, y - sy, z + sz))
                z += sz
                err_z -= 1
        elif dz > 0:
            z += sz
            err_z -= 1

        result.append((x, y, z))

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for v in result:
        if v not in seen:
            seen.add(v)
            deduped.append(v)
    return deduped
