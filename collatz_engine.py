"""High-performance Collatz trajectory computation engine.

Provides core functions for computing trajectories, stopping times,
parity sequences, and trajectory features for the 3x+1 map.
"""

import math


def collatz_trajectory(n):
    """Return the full Collatz trajectory from n to 1 as a list."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    traj = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        traj.append(n)
    return traj


def collatz_stopping_time(n):
    """Return the total stopping time (steps to reach 1)."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return 0
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


def collatz_parity_sequence(n):
    """Return binary string of odd/even steps (1=odd, 0=even)."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return ""
    parities = []
    while n != 1:
        if n % 2 == 0:
            parities.append('0')
            n = n // 2
        else:
            parities.append('1')
            n = 3 * n + 1
    return "".join(parities)


def collatz_trajectory_features(n):
    """Return dict of trajectory features for starting value n."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return {
            "stopping_time": 0,
            "max_value": 1,
            "num_odd_steps": 0,
            "num_even_steps": 0,
            "odd_ratio": 0.0,
            "max_value_ratio": 1.0,
        }
    current = n
    max_val = n
    odd_steps = 0
    even_steps = 0
    while current != 1:
        if current % 2 == 0:
            current = current // 2
            even_steps += 1
        else:
            current = 3 * current + 1
            odd_steps += 1
        if current > max_val:
            max_val = current
    total = odd_steps + even_steps
    return {
        "stopping_time": total,
        "max_value": max_val,
        "num_odd_steps": odd_steps,
        "num_even_steps": even_steps,
        "odd_ratio": odd_steps / total if total > 0 else 0.0,
        "max_value_ratio": max_val / n,
    }


def batch_stopping_times(max_n):
    """Compute stopping times for n=1..max_n efficiently using memoization."""
    cache = {1: 0}
    results = [0] * (max_n + 1)
    for n in range(2, max_n + 1):
        seq = []
        current = n
        while current not in cache:
            seq.append(current)
            if current % 2 == 0:
                current = current // 2
            else:
                current = 3 * current + 1
        base = cache[current]
        for i, val in enumerate(reversed(seq)):
            cache[val] = base + i + 1
        results[n] = cache[n]
    return results


# Unit tests
if __name__ == "__main__":
    import time

    # Test known values
    assert collatz_stopping_time(27) == 111, f"n=27: expected 111, got {collatz_stopping_time(27)}"
    assert collatz_stopping_time(9663) == 184, f"n=9663: expected 184, got {collatz_stopping_time(9663)}"
    assert collatz_stopping_time(1) == 0, f"n=1: expected 0, got {collatz_stopping_time(1)}"

    # Test trajectory
    traj = collatz_trajectory(27)
    assert traj[0] == 27
    assert traj[-1] == 1
    assert len(traj) == 112  # 111 steps + starting value

    # Test parity sequence
    ps = collatz_parity_sequence(27)
    assert len(ps) == 111

    # Test features
    feats = collatz_trajectory_features(27)
    assert feats["stopping_time"] == 111
    assert feats["num_odd_steps"] + feats["num_even_steps"] == 111

    # Test large number handling (10^15)
    st = collatz_stopping_time(10**15 + 1)
    assert st > 0

    # Performance test: all stopping times for n=1..10^6 under 60 seconds
    start = time.time()
    results = batch_stopping_times(1_000_000)
    elapsed = time.time() - start
    print(f"batch_stopping_times(10^6): {elapsed:.2f}s")
    assert elapsed < 60, f"Too slow: {elapsed:.2f}s"
    assert results[27] == 111
    assert results[9663] == 184
    assert results[1] == 0

    print("All tests passed!")
