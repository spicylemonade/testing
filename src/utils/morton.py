"""Morton code (Z-order curve) utilities for 3D voxel grids.

Provides encoding/decoding between 3D coordinates and Morton codes,
used for cache-friendly memory layout of voxel grids.
"""


def _spread_bits(v):
    """Spread bits of a 10-bit integer into every 3rd bit position.

    Input:  bits b9 b8 b7 b6 b5 b4 b3 b2 b1 b0
    Output: 0 0 b9 0 0 b8 0 0 b7 ... 0 0 b0
    """
    v &= 0x000003FF  # 10 bits
    v = (v | (v << 16)) & 0x030000FF
    v = (v | (v << 8))  & 0x0300F00F
    v = (v | (v << 4))  & 0x030C30C3
    v = (v | (v << 2))  & 0x09249249
    return v


def _compact_bits(v):
    """Compact every 3rd bit back to a contiguous integer."""
    v &= 0x09249249
    v = (v | (v >> 2))  & 0x030C30C3
    v = (v | (v >> 4))  & 0x0300F00F
    v = (v | (v >> 8))  & 0x030000FF
    v = (v | (v >> 16)) & 0x000003FF
    return v


def encode_morton(x, y, z):
    """Encode 3D coordinates to Morton code (Z-order curve).

    Supports coordinates up to 1023 (10 bits each → 30-bit Morton code).
    """
    return _spread_bits(x) | (_spread_bits(y) << 1) | (_spread_bits(z) << 2)


def decode_morton(code):
    """Decode Morton code back to (x, y, z) coordinates."""
    x = _compact_bits(code)
    y = _compact_bits(code >> 1)
    z = _compact_bits(code >> 2)
    return x, y, z
