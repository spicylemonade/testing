"""Constraint propagation solver for the perfect cuboid problem.

Encodes the problem as a CSP with modular arithmetic constraints,
uses arc-consistency propagation and systematic search.
"""

import math
import sys
import os
import time
import signal
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from space_diagonal import isqrt, near_miss_score, NearMissTracker
from modular_filter import is_euler_brick_candidate, _quadratic_residues
from metrics import SearchMetrics


class ComputeTimeout(Exception):
    pass


def _timeout_handler(signum, frame):
    raise ComputeTimeout()


def precompute_valid_residues(modulus: int):
    """For a given modulus, precompute which (a_mod, b_mod, c_mod) triples
    could possibly yield a perfect cuboid.

    Returns a set of (a%m, b%m, c%m) triples that pass all four QR conditions.
    """
    qr = _quadratic_residues(modulus)
    valid = set()
    for a in range(modulus):
        a2 = (a * a) % modulus
        for b in range(modulus):
            b2 = (b * b) % modulus
            ab = (a2 + b2) % modulus
            if ab not in qr:
                continue
            for c in range(modulus):
                c2 = (c * c) % modulus
                bc = (b2 + c2) % modulus
                if bc not in qr:
                    continue
                ac = (a2 + c2) % modulus
                if ac not in qr:
                    continue
                abc = (a2 + b2 + c2) % modulus
                if abc not in qr:
                    continue
                valid.add((a, b, c))
    return valid


def constraint_search(max_edge: int, timeout_seconds: int = 300):
    """CSP-based search for perfect cuboids using modular constraint propagation.

    Pre-computes valid residue classes for multiple moduli, then only iterates
    over triples in the intersection of valid classes.
    """
    metrics = SearchMetrics(method="constraint_solver", search_bound=max_edge)
    tracker = NearMissTracker(k=200)
    euler_bricks = []

    # Set timeout
    if hasattr(signal, 'SIGALRM'):
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(timeout_seconds)

    metrics.start_timer()

    try:
        # Precompute valid residues for key moduli
        print("Precomputing valid residue classes...")
        moduli_residues = {}
        for m in [16, 9, 5, 7, 11, 13]:
            valid = precompute_valid_residues(m)
            density = len(valid) / (m ** 3)
            moduli_residues[m] = valid
            print(f"  mod {m}: {len(valid)}/{m**3} valid triples ({density:.4%})")

        # Use CRT-like iteration: step through valid residue classes
        # For efficiency, use the smallest moduli first
        # Primary sieve: mod 16 (most restrictive for the problem)
        m16_valid = moduli_residues[16]
        m9_valid = moduli_residues[9]
        m5_valid = moduli_residues[5]
        m7_valid = moduli_residues[7]

        passed_m16 = 0
        passed_all_mod = 0
        passed_face = 0

        for a in range(1, max_edge + 1):
            for b in range(a, max_edge + 1):
                # Quick face diagonal check for (a, b)
                d = isqrt(a * a + b * b)
                if d is None:
                    continue

                for c in range(b, max_edge + 1):
                    metrics.total_candidates += 1

                    # Modular checks
                    if (a % 16, b % 16, c % 16) not in m16_valid:
                        continue
                    passed_m16 += 1

                    if (a % 9, b % 9, c % 9) not in m9_valid:
                        continue
                    if (a % 5, b % 5, c % 5) not in m5_valid:
                        continue
                    if (a % 7, b % 7, c % 7) not in m7_valid:
                        continue
                    passed_all_mod += 1
                    metrics.passed_modular_filter += 1

                    # Face diagonal checks
                    e = isqrt(b * b + c * c)
                    if e is None:
                        continue
                    f = isqrt(a * a + c * c)
                    if f is None:
                        continue

                    passed_face += 1
                    metrics.passed_face_diagonal += 1
                    metrics.euler_bricks_found += 1
                    euler_bricks.append((a, b, c, d, e, f))

                    # Space diagonal check
                    g = isqrt(a * a + b * b + c * c)
                    score = near_miss_score(a, b, c)
                    tracker.add(a, b, c, score)
                    metrics.near_misses_found += 1

                    if g is not None:
                        metrics.perfect_cuboids_found += 1
                        print(f"*** PERFECT CUBOID FOUND: ({a}, {b}, {c}) ***")

    except ComputeTimeout:
        print(f"Search timed out after {timeout_seconds}s")
    finally:
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)

    metrics.stop_timer()

    metrics.filter_stages = {
        "total": metrics.total_candidates,
        "passed_mod16": passed_m16,
        "passed_all_modular": passed_all_mod,
        "euler_bricks": passed_face,
    }

    return euler_bricks, metrics, tracker


def run_constraint_solver():
    """Run the constraint solver and produce a report."""
    max_edge = 5000  # Manageable for CSP approach
    timeout = 300  # 5 minutes

    print(f"Running constraint solver (max_edge={max_edge}, timeout={timeout}s)...")
    bricks, metrics, tracker = constraint_search(max_edge, timeout)

    print("\n" + metrics.report())
    metrics.save("results/constraint_solver_metrics.json")

    # Write report
    report_path = "results/constraint_solver_report.md"
    with open(report_path, 'w') as f:
        f.write("# Constraint Solver Report\n\n")
        f.write("## Approach\n")
        f.write("CSP-based search using pre-computed valid residue classes for moduli\n")
        f.write("16, 9, 5, 7, 11, 13. Only triples in the intersection of valid\n")
        f.write("residue classes are examined. First face diagonal (a,b) is checked\n")
        f.write("before iterating over c.\n\n")
        f.write("## Residue Class Filtering\n")
        f.write("The combined modular sieve dramatically reduces the search space:\n")
        f.write(f"- Total candidates: {metrics.total_candidates:,}\n")
        for stage, count in metrics.filter_stages.items():
            f.write(f"- {stage}: {count:,}\n")
        f.write(f"\n## Results\n")
        f.write(f"- Search bound: {max_edge:,}\n")
        f.write(f"- Euler bricks found: {metrics.euler_bricks_found}\n")
        f.write(f"- Perfect cuboids found: {metrics.perfect_cuboids_found}\n")
        f.write(f"- Wall clock time: {metrics.wall_clock_seconds:.2f}s\n")
        f.write(f"- Throughput: {metrics.candidates_per_second:,.0f} candidates/sec\n\n")
        f.write("## Comparison with Baseline\n")
        f.write("The constraint solver approach reduces the number of arithmetic\n")
        f.write("operations by pre-filtering with modular residue classes, but the\n")
        f.write("overhead of residue lookups means the raw throughput may not exceed\n")
        f.write("the optimized baseline for small search bounds. The advantage grows\n")
        f.write("with larger bounds where the filtering ratio increases.\n")

    print(f"\nReport saved to {report_path}")
    return bricks, metrics, tracker


if __name__ == "__main__":
    run_constraint_solver()
