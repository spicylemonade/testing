"""VoxelGrid: 3D occupancy grid stored as a compact uint8 array."""

import numpy as np


class VoxelGrid:
    """NxNxN voxel occupancy grid with O(1) access.

    Stores occupancy as a flat uint8 array in row-major order.
    Supports grids up to 512^3 (134M voxels, ~128MB).
    """

    def __init__(self, size: int, data: np.ndarray = None):
        self.size = size
        if data is not None:
            assert data.shape == (size, size, size), f"Expected ({size},{size},{size}), got {data.shape}"
            self.data = data.astype(np.uint8)
        else:
            self.data = np.zeros((size, size, size), dtype=np.uint8)

    def get(self, x: int, y: int, z: int) -> bool:
        return bool(self.data[x, y, z])

    def set(self, x: int, y: int, z: int, val: bool = True):
        self.data[x, y, z] = np.uint8(val)

    def in_bounds(self, x: int, y: int, z: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size and 0 <= z < self.size

    @property
    def occupancy_fraction(self) -> float:
        return float(np.count_nonzero(self.data)) / self.data.size

    @property
    def total_voxels(self) -> int:
        return self.data.size

    @property
    def occupied_count(self) -> int:
        return int(np.count_nonzero(self.data))

    def __repr__(self):
        return f"VoxelGrid(size={self.size}, occupancy={self.occupancy_fraction:.2%})"
