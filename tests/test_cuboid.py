"""Tests for src/cuboid.py — Cuboid class and Pythagorean triple generators."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.cuboid import Cuboid, is_perfect_square, isqrt, pythagorean_triples


def test_isqrt_perfect():
    assert isqrt(0) == 0
    assert isqrt(1) == 1
    assert isqrt(4) == 2
    assert isqrt(144) == 12
    assert isqrt(10000) == 100


def test_isqrt_non_perfect():
    assert isqrt(2) == 1
    assert isqrt(3) == 1
    assert isqrt(5) == 2
    assert isqrt(99) == 9


def test_is_perfect_square():
    assert is_perfect_square(0) is True
    assert is_perfect_square(1) is True
    assert is_perfect_square(4) is True
    assert is_perfect_square(2) is False
    assert is_perfect_square(3) is False
    assert is_perfect_square(73225) is False  # 44^2 + 117^2 + 240^2


def test_cuboid_known_euler_brick():
    """The smallest Euler brick (44, 117, 240) must be detected."""
    c = Cuboid(44, 117, 240)
    assert c.is_euler_brick() is True
    assert c.is_perfect_cuboid() is False


def test_cuboid_face_diagonals_values():
    """Check exact face diagonal values for (44, 117, 240)."""
    c = Cuboid(44, 117, 240)
    # d_ab = sqrt(44^2 + 117^2) = sqrt(1936 + 13689) = sqrt(15625) = 125
    assert c.face_diagonal_ab_sq == 15625
    assert is_perfect_square(15625)
    # d_ac = sqrt(44^2 + 240^2) = sqrt(1936 + 57600) = sqrt(59536) = 244
    assert c.face_diagonal_ac_sq == 59536
    assert is_perfect_square(59536)
    # d_bc = sqrt(117^2 + 240^2) = sqrt(13689 + 57600) = sqrt(71289) = 267
    assert c.face_diagonal_bc_sq == 71289
    assert is_perfect_square(71289)


def test_cuboid_space_diagonal_not_integer():
    """Space diagonal of (44, 117, 240) is not an integer."""
    c = Cuboid(44, 117, 240)
    # a^2 + b^2 + c^2 = 1936 + 13689 + 57600 = 73225
    assert c.space_diagonal_sq == 73225
    assert is_perfect_square(73225) is False


def test_cuboid_non_euler_brick():
    """A random triple should not be an Euler brick."""
    c = Cuboid(1, 2, 3)
    assert c.is_euler_brick() is False
    assert c.is_perfect_cuboid() is False


def test_cuboid_second_euler_brick():
    """(240, 252, 275) is known to be an Euler brick."""
    c = Cuboid(240, 252, 275)
    assert c.is_euler_brick() is True
    assert c.is_perfect_cuboid() is False


def test_cuboid_third_euler_brick():
    """(85, 132, 720) is a known Euler brick."""
    c = Cuboid(85, 132, 720)
    assert c.is_euler_brick() is True


def test_cuboid_to_dict():
    c = Cuboid(44, 117, 240)
    d = c.to_dict()
    assert d["edges"] == [44, 117, 240]
    assert d["is_euler_brick"] is True
    assert d["is_perfect_cuboid"] is False


def test_pythagorean_triples_basic():
    """Check basic primitive triples."""
    triples = pythagorean_triples(50)
    assert (3, 4, 5) in triples
    assert (5, 12, 13) in triples
    assert (8, 15, 17) in triples
    assert (7, 24, 25) in triples


def test_pythagorean_triples_primitive_only():
    """Ensure only primitive triples are generated."""
    triples = pythagorean_triples(100)
    # (6, 8, 10) is non-primitive (2 * (3, 4, 5))
    assert (6, 8, 10) not in triples


def test_space_diagonal_gap():
    """Gap should be < 0.5 for Euler brick (85, 132, 720)."""
    c = Cuboid(85, 132, 720)
    gap = c.space_diagonal_gap()
    assert 0 < gap < 0.5  # Not a perfect cuboid, gap is in (0, 0.5)


if __name__ == "__main__":
    tests = [f for f in dir() if f.startswith("test_")]
    passed = 0
    failed = 0
    for t in tests:
        try:
            globals()[t]()
            print(f"  PASS: {t}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {t} — {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR: {t} — {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed out of {passed + failed}")
