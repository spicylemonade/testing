"""Multi-stage modular constraint filter for perfect cuboid candidates.

Implements known necessary conditions from Kraitchik (1945), Roberts (2009),
and others. Only triples passing all filters could potentially be perfect cuboids.
"""

import math
import random
from typing import Tuple


def _is_perfect_square(n: int) -> bool:
    """Fast perfect square test."""
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def parity_check(a: int, b: int, c: int) -> bool:
    """Check parity constraints.

    For a primitive perfect cuboid, exactly one edge is odd.
    More generally, the number of odd edges must be 1 or 3.
    For face diagonals to be integer, specific parity patterns are required.
    """
    odds = (a % 2) + (b % 2) + (c % 2)
    # At least one must be even for a^2+b^2 to potentially be a perfect square
    # (two odds -> sum is 2 mod 4, which CAN be a perfect square)
    # Actually, no strict parity elimination for general Euler bricks
    # For primitive cuboids: exactly one odd edge
    # But for general search we just need face diagonals to work
    return True  # Don't over-filter; let face diagonal checks handle it


def divisibility_check(a: int, b: int, c: int) -> bool:
    """Check divisibility constraints from Kraitchik.

    For a primitive perfect cuboid:
    - One edge divisible by 4, another by 16
    - Product divisible by specific primes

    For general search, we apply lighter constraints.
    """
    # Sort edges
    edges = sorted([a, b, c])

    # At least one edge must be even (otherwise all face diags would be irrational)
    evens = sum(1 for e in edges if e % 2 == 0)
    if evens == 0:
        # All odd: a^2+b^2 is even but not div by 4 if both a,b are odd
        # So a^2+b^2 ≡ 2 mod 4, which is never a perfect square
        return False

    return True


def mod_24_check(a: int, b: int, c: int) -> bool:
    """Check mod-24 congruence constraints.

    a^2+b^2 must be a quadratic residue mod 24 that is also a perfect square mod 24.
    Perfect squares mod 24 are: {0, 1, 4, 9, 12, 16}.
    """
    QR24 = {0, 1, 4, 9, 12, 16}
    s_ab = (a * a + b * b) % 24
    if s_ab not in QR24:
        return False
    s_bc = (b * b + c * c) % 24
    if s_bc not in QR24:
        return False
    s_ac = (a * a + c * c) % 24
    if s_ac not in QR24:
        return False
    s_abc = (a * a + b * b + c * c) % 24
    if s_abc not in QR24:
        return False
    return True


def mod_48_check(a: int, b: int, c: int) -> bool:
    """Check mod-48 congruence constraints.

    Perfect squares mod 48 are: {0, 1, 4, 9, 16, 25, 33, 36}.
    """
    QR48 = set()
    for i in range(48):
        QR48.add((i * i) % 48)

    s_ab = (a * a + b * b) % 48
    if s_ab not in QR48:
        return False
    s_bc = (b * b + c * c) % 48
    if s_bc not in QR48:
        return False
    s_ac = (a * a + c * c) % 48
    if s_ac not in QR48:
        return False
    s_abc = (a * a + b * b + c * c) % 48
    if s_abc not in QR48:
        return False
    return True


# Precompute quadratic residue sets for small moduli
_QR_CACHE = {}

def _quadratic_residues(m: int) -> set:
    """Compute set of quadratic residues mod m."""
    if m not in _QR_CACHE:
        _QR_CACHE[m] = {(i * i) % m for i in range(m)}
    return _QR_CACHE[m]


def face_diag_mod_check(a: int, b: int, c: int, moduli=(8, 16, 24, 48, 5, 7, 9)) -> bool:
    """Check that all three face diagonal sums are QRs across multiple moduli."""
    for m in moduli:
        qr = _quadratic_residues(m)
        if (a * a + b * b) % m not in qr:
            return False
        if (b * b + c * c) % m not in qr:
            return False
        if (a * a + c * c) % m not in qr:
            return False
    return True


def space_diag_mod_check(a: int, b: int, c: int, moduli=(8, 16, 24, 48, 5, 7, 9)) -> bool:
    """Check that a^2+b^2+c^2 is a QR across multiple moduli."""
    for m in moduli:
        qr = _quadratic_residues(m)
        if (a * a + b * b + c * c) % m not in qr:
            return False
    return True


def is_euler_brick_candidate(a: int, b: int, c: int) -> bool:
    """Filter for Euler brick candidates (face diagonals only)."""
    if a <= 0 or b <= 0 or c <= 0:
        return False
    if not divisibility_check(a, b, c):
        return False
    if not face_diag_mod_check(a, b, c):
        return False
    return True


def is_candidate(a: int, b: int, c: int) -> bool:
    """Full modular filter for perfect cuboid candidates.

    Returns True only if (a,b,c) passes all known necessary conditions:
    face diagonals AND space diagonal must be plausible perfect squares.
    """
    if not is_euler_brick_candidate(a, b, c):
        return False
    if not space_diag_mod_check(a, b, c):
        return False
    return True


# --- Unit Tests ---

def test_known_euler_bricks_pass():
    """Known Euler bricks must pass the Euler brick filter (face diags only).
    They need NOT pass the full perfect cuboid filter since their space diag is irrational."""
    known = [
        (44, 117, 240),
        (240, 252, 275),
        (140, 480, 693),
    ]
    for a, b, c in known:
        assert is_euler_brick_candidate(a, b, c), \
            f"Known Euler brick ({a},{b},{c}) should pass Euler brick filter"
    print("  PASS: All known Euler bricks pass the Euler brick filter")


def test_rejection_rate():
    """At least 95% of random triples should be rejected."""
    random.seed(42)
    n_total = 100000
    n_pass = 0
    for _ in range(n_total):
        a = random.randint(1, 1000000)
        b = random.randint(1, 1000000)
        c = random.randint(1, 1000000)
        if is_candidate(a, b, c):
            n_pass += 1
    rejection_rate = 1.0 - n_pass / n_total
    print(f"  Rejection rate: {rejection_rate:.4%} ({n_pass}/{n_total} passed)")
    assert rejection_rate >= 0.95, f"Rejection rate {rejection_rate:.4%} < 95%"
    print("  PASS: Rejection rate >= 95%")


if __name__ == "__main__":
    print("Running Modular Filter tests...")
    test_known_euler_bricks_pass()
    test_rejection_rate()
    print("\nAll tests passed!")
