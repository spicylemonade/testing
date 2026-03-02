"""Core data structures for the Perfect Cuboid problem.

Provides Cuboid class for representing rectangular boxes with integer edge
analysis, plus Pythagorean triple generators using the (m,n) parametrization.
"""

import math
from typing import List, Tuple, Optional


def isqrt(n: int) -> int:
    """Integer square root. Returns floor(sqrt(n))."""
    if n < 0:
        raise ValueError("Square root of negative number")
    if n == 0:
        return 0
    x = int(math.isqrt(n))
    # Verify (math.isqrt is exact for Python >= 3.8)
    if x * x == n:
        return x
    return x


def is_perfect_square(n: int) -> bool:
    """Check if n is a perfect square using exact integer arithmetic."""
    if n < 0:
        return False
    r = isqrt(n)
    return r * r == n


class Cuboid:
    """Rectangular box with edges (a, b, c) and computed diagonals."""

    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c
        self._a2 = a * a
        self._b2 = b * b
        self._c2 = c * c

    @property
    def face_diagonal_ab_sq(self) -> int:
        return self._a2 + self._b2

    @property
    def face_diagonal_ac_sq(self) -> int:
        return self._a2 + self._c2

    @property
    def face_diagonal_bc_sq(self) -> int:
        return self._b2 + self._c2

    @property
    def space_diagonal_sq(self) -> int:
        return self._a2 + self._b2 + self._c2

    def face_diagonal_ab(self) -> float:
        return math.sqrt(self.face_diagonal_ab_sq)

    def face_diagonal_ac(self) -> float:
        return math.sqrt(self.face_diagonal_ac_sq)

    def face_diagonal_bc(self) -> float:
        return math.sqrt(self.face_diagonal_bc_sq)

    def space_diagonal(self) -> float:
        return math.sqrt(self.space_diagonal_sq)

    def is_euler_brick(self) -> bool:
        """True iff all three face diagonals are integers."""
        return (is_perfect_square(self.face_diagonal_ab_sq) and
                is_perfect_square(self.face_diagonal_ac_sq) and
                is_perfect_square(self.face_diagonal_bc_sq))

    def is_perfect_cuboid(self) -> bool:
        """True iff all face diagonals AND space diagonal are integers."""
        return self.is_euler_brick() and is_perfect_square(self.space_diagonal_sq)

    def space_diagonal_gap(self) -> float:
        """How close the space diagonal is to an integer.
        Returns min(frac, 1-frac) where frac is the fractional part."""
        sd = self.space_diagonal()
        frac = sd - math.floor(sd)
        return min(frac, 1.0 - frac)

    def to_dict(self) -> dict:
        """Full report of the cuboid."""
        d_ab = self.face_diagonal_ab()
        d_ac = self.face_diagonal_ac()
        d_bc = self.face_diagonal_bc()
        d_s = self.space_diagonal()
        return {
            "edges": [self.a, self.b, self.c],
            "face_diagonals": {
                "d_ab": d_ab,
                "d_ac": d_ac,
                "d_bc": d_bc,
            },
            "space_diagonal": d_s,
            "is_euler_brick": self.is_euler_brick(),
            "is_perfect_cuboid": self.is_perfect_cuboid(),
            "space_diagonal_gap": self.space_diagonal_gap(),
        }

    def __repr__(self):
        return f"Cuboid({self.a}, {self.b}, {self.c})"


def pythagorean_triples(max_hyp: int) -> List[Tuple[int, int, int]]:
    """Generate all primitive Pythagorean triples (a, b, c) with a < b < c <= max_hyp
    using the (m, n) parametrization: a = m^2 - n^2, b = 2mn, c = m^2 + n^2."""
    triples = []
    m = 2
    while m * m + 1 <= max_hyp:
        for n in range(1, m):
            if (m - n) % 2 == 0:
                continue  # m and n must have opposite parity
            if math.gcd(m, n) != 1:
                continue  # must be coprime
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            if c > max_hyp:
                break
            if a > b:
                a, b = b, a
            triples.append((a, b, c))
        m += 1
    return sorted(triples, key=lambda t: t[2])


def all_pythagorean_triples(max_leg: int) -> List[Tuple[int, int, int]]:
    """Generate all Pythagorean triples (a, b, c) with a, b <= max_leg,
    including non-primitive (multiples of primitive triples)."""
    triples = set()
    primitives = pythagorean_triples(2 * max_leg * max_leg)
    for a, b, c in primitives:
        k = 1
        while k * a <= max_leg or k * b <= max_leg:
            if k * a <= max_leg and k * b <= max_leg:
                triples.add((min(k * a, k * b), max(k * a, k * b), k * c))
            k += 1
    return sorted(triples, key=lambda t: (t[2], t[0]))
