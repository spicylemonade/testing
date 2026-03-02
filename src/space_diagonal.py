"""Space diagonal integer test and near-miss tracking for perfect cuboid search.

Provides:
- is_perfect(a, b, c): Check if all face diags AND space diag are integers
- near_miss_score(a, b, c): How close the space diagonal is to an integer
- NearMissTracker: Maintains sorted list of top-K near-misses
"""

import math
import heapq
from typing import Optional, List, Tuple


def isqrt(n: int) -> Optional[int]:
    """Return integer sqrt if n is a perfect square, else None."""
    if n < 0:
        return None
    r = math.isqrt(n)
    if r * r == n:
        return r
    return None


def is_perfect(a: int, b: int, c: int) -> bool:
    """Check whether (a,b,c) forms a perfect cuboid.

    All face diagonals AND the space diagonal must be integers.
    """
    if isqrt(a * a + b * b) is None:
        return False
    if isqrt(b * b + c * c) is None:
        return False
    if isqrt(a * a + c * c) is None:
        return False
    if isqrt(a * a + b * b + c * c) is None:
        return False
    return True


def near_miss_score(a: int, b: int, c: int) -> float:
    """Return how close a^2+b^2+c^2 is to the nearest perfect square.

    Score = |a^2+b^2+c^2 - nearest_square| / (a^2+b^2+c^2)

    Lower score = closer to a perfect cuboid.
    Returns float('inf') if any face diagonal is not an integer.
    """
    if isqrt(a * a + b * b) is None:
        return float('inf')
    if isqrt(b * b + c * c) is None:
        return float('inf')
    if isqrt(a * a + c * c) is None:
        return float('inf')

    s = a * a + b * b + c * c
    r = math.isqrt(s)
    # Check both r^2 and (r+1)^2
    diff1 = abs(s - r * r)
    diff2 = abs(s - (r + 1) * (r + 1))
    residual = min(diff1, diff2)

    if s == 0:
        return float('inf')
    return residual / s


class NearMissTracker:
    """Maintains a sorted list of the top-K closest near-misses found."""

    def __init__(self, k: int = 100):
        self.k = k
        # Max-heap (negate scores since heapq is a min-heap)
        self._heap: List[Tuple[float, Tuple[int, int, int]]] = []
        self._seen = set()

    def add(self, a: int, b: int, c: int, score: float):
        """Add a near-miss candidate."""
        key = tuple(sorted([a, b, c]))
        if key in self._seen:
            return
        if score == float('inf'):
            return

        if len(self._heap) < self.k:
            heapq.heappush(self._heap, (-score, key))
            self._seen.add(key)
        elif score < -self._heap[0][0]:
            # Better than worst in heap
            _, removed_key = heapq.heapreplace(self._heap, (-score, key))
            self._seen.discard(removed_key)
            self._seen.add(key)

    def get_top(self, n: Optional[int] = None) -> List[Tuple[float, Tuple[int, int, int]]]:
        """Return the top-n near-misses sorted by score (best first)."""
        results = [(-s, edges) for s, edges in self._heap]
        results.sort(key=lambda x: x[0])
        if n is not None:
            return results[:n]
        return results

    def __len__(self):
        return len(self._heap)


# --- Unit Tests ---

def test_is_perfect_known_euler_brick():
    """Known Euler bricks are NOT perfect cuboids (space diagonal is irrational)."""
    assert not is_perfect(44, 117, 240), "(44,117,240) should not be a perfect cuboid"
    assert not is_perfect(240, 252, 275), "(240,252,275) should not be a perfect cuboid"
    print("  PASS: Known Euler bricks correctly identified as non-perfect")


def test_near_miss_score_euler_brick():
    """Test near-miss score for (44, 117, 240)."""
    score = near_miss_score(44, 117, 240)
    # 44^2 + 117^2 + 240^2 = 1936 + 13689 + 57600 = 73225
    # sqrt(73225) ≈ 270.6
    # 270^2 = 72900, 271^2 = 73441
    # residual = min(73225-72900, 73441-73225) = min(325, 216) = 216
    # score = 216 / 73225 ≈ 0.00295
    assert score != float('inf'), "Score should be finite for an Euler brick"
    expected = 216 / 73225
    assert abs(score - expected) < 1e-10, f"Expected {expected}, got {score}"
    print(f"  PASS: near_miss_score(44,117,240) = {score:.6f} (residual=216)")


def test_near_miss_tracker():
    """Test NearMissTracker functionality."""
    tracker = NearMissTracker(k=3)
    tracker.add(44, 117, 240, 0.01)
    tracker.add(240, 252, 275, 0.02)
    tracker.add(140, 480, 693, 0.005)
    tracker.add(100, 200, 300, 0.001)  # Should replace worst

    assert len(tracker) == 3, f"Expected 3 items, got {len(tracker)}"
    top = tracker.get_top()
    assert top[0][0] < top[-1][0], "Should be sorted best-first"
    print(f"  PASS: NearMissTracker correctly maintains top-K={len(tracker)}")


def test_non_euler_brick_score():
    """Non-Euler bricks should have infinite score."""
    score = near_miss_score(1, 2, 3)
    assert score == float('inf'), "Non-Euler brick should have infinite score"
    print("  PASS: Non-Euler brick correctly gets infinite score")


if __name__ == "__main__":
    print("Running Space Diagonal tests...")
    test_is_perfect_known_euler_brick()
    test_near_miss_score_euler_brick()
    test_near_miss_tracker()
    test_non_euler_brick_score()
    print("\nAll tests passed!")
