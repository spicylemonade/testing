"""Trajectory encoding and feature extraction pipeline for Collatz analysis."""

import math
import numpy as np
from collections import Counter
from collatz_engine import collatz_parity_sequence, collatz_trajectory_features

SEED = 42


def encode_trajectory_binary(n):
    """Convert parity sequence to numpy array of 0s and 1s."""
    ps = collatz_parity_sequence(n)
    if len(ps) == 0:
        return np.array([], dtype=np.int8)
    return np.array([int(c) for c in ps], dtype=np.int8)


def _shannon_entropy(arr):
    """Compute Shannon entropy of a binary sequence."""
    if len(arr) == 0:
        return 0.0
    p1 = np.mean(arr)
    p0 = 1 - p1
    ent = 0.0
    if p0 > 0:
        ent -= p0 * math.log2(p0)
    if p1 > 0:
        ent -= p1 * math.log2(p1)
    return ent


def _trailing_ones(n):
    """Count trailing 1-bits in binary representation of n."""
    if n == 0:
        return 0
    count = 0
    while n & 1:
        count += 1
        n >>= 1
    return count


def _two_adic_valuation(n):
    """Compute the 2-adic valuation v_2(n) = max k such that 2^k divides n."""
    if n == 0:
        return float('inf')
    v = 0
    while n % 2 == 0:
        v += 1
        n //= 2
    return v


def trajectory_to_point_cloud(n_range):
    """Map each n in range to a 6D feature vector, return as numpy array.

    Features: (stopping_time, log_max_value, odd_ratio,
               entropy_of_parity_seq, trailing_ones_in_binary_n, 2adic_valuation_n)
    """
    start, end = n_range[0], n_range[-1]
    N = end - start + 1
    cloud = np.zeros((N, 6), dtype=np.float64)

    for i, n in enumerate(range(start, end + 1)):
        feats = collatz_trajectory_features(n)
        parity = encode_trajectory_binary(n)
        entropy = _shannon_entropy(parity)

        cloud[i, 0] = feats["stopping_time"]
        cloud[i, 1] = math.log(feats["max_value"]) if feats["max_value"] > 0 else 0.0
        cloud[i, 2] = feats["odd_ratio"]
        cloud[i, 3] = entropy
        cloud[i, 4] = _trailing_ones(n)
        cloud[i, 5] = _two_adic_valuation(n)

    return cloud


def parity_ngrams(n, k):
    """Return frequency distribution of all k-grams in the parity sequence of n."""
    ps = collatz_parity_sequence(n)
    if len(ps) < k:
        return Counter()
    counts = Counter()
    for i in range(len(ps) - k + 1):
        counts[ps[i:i + k]] += 1
    return counts


if __name__ == "__main__":
    # Test encode_trajectory_binary
    arr = encode_trajectory_binary(27)
    assert arr.dtype == np.int8
    assert len(arr) == 111

    # Test point cloud
    cloud = trajectory_to_point_cloud(range(1, 10001))
    assert cloud.shape == (10000, 6), f"Shape: {cloud.shape}"
    assert np.all(np.isfinite(cloud)), "Non-finite values in point cloud"
    print(f"Point cloud shape: {cloud.shape}")
    print(f"Feature ranges: {cloud.min(axis=0)} to {cloud.max(axis=0)}")

    # Test parity ngrams
    ngrams = parity_ngrams(27, 4)
    assert sum(ngrams.values()) == 111 - 4 + 1  # = 108
    print(f"4-grams for n=27: {len(ngrams)} unique patterns")

    print("All tests passed!")
