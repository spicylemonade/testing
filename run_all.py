#!/usr/bin/env python3
"""Run the complete experimental pipeline for the perfect cuboid project.

Executes all search methods, collects results, runs analysis, and generates figures.
"""

import json
import os
import sys
import time

# Ensure src/ is importable
sys.path.insert(0, os.path.dirname(__file__))

from src.brute_force import find_euler_bricks
from src.modular_sieve import find_euler_bricks_sieved
from src.novel_search import novel_search
from src.parametric import saunderson_family, euler_family_1, bremner_family
from src.near_miss import collect_near_misses, analyze_distribution, create_histogram
from src.verifier import verify_cuboid

BOUND = 5000
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "figures")


def ensure_dirs():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)


def run_brute_force():
    print(f"[1/6] Brute force search (bound={BOUND})...")
    t0 = time.time()
    results = find_euler_bricks(BOUND)
    elapsed = time.time() - t0
    print(f"       Found {len(results)} Euler bricks in {elapsed:.2f}s")
    return results


def run_modular_sieve():
    print(f"[2/6] Modular sieve search (bound={BOUND})...")
    t0 = time.time()
    results = find_euler_bricks_sieved(BOUND)
    elapsed = time.time() - t0
    print(f"       Found {len(results)} Euler bricks in {elapsed:.2f}s")
    return results


def run_novel_search():
    print(f"[3/6] Novel triple intersection search (bound={BOUND})...")
    t0 = time.time()
    results = novel_search(BOUND)
    elapsed = time.time() - t0
    print(f"       Found {len(results)} Euler bricks in {elapsed:.2f}s")
    return results


def run_parametric():
    print("[4/6] Parametric family generation...")
    saunderson = saunderson_family(50)
    euler = euler_family_1(50)
    bremner = bremner_family(50)
    total = len(saunderson) + len(euler) + len(bremner)
    print(f"       Saunderson: {len(saunderson)}, Euler: {len(euler)}, Bremner: {len(bremner)}")
    print(f"       Total: {total} bricks from parametric families")
    return saunderson, euler, bremner


def run_verification(brute_results):
    print("[5/6] Verifying all Euler bricks...")
    verified = 0
    for brick in brute_results:
        edges = brick["edges"]
        report = verify_cuboid(*edges)
        if report["is_euler_brick"]:
            verified += 1
        if report["is_perfect_cuboid"]:
            print(f"  *** PERFECT CUBOID FOUND: {edges} ***")
    print(f"       Verified {verified}/{len(brute_results)} Euler bricks")
    return verified


def run_near_miss_analysis(all_bricks):
    print("[6/6] Near-miss analysis...")
    near_misses = collect_near_misses(all_bricks)
    stats = analyze_distribution(near_misses)
    print(f"       Analyzed {len(near_misses)} bricks")
    print(f"       Mean gap: {stats.get('mean_gap', 'N/A'):.4f}")
    print(f"       Chi-squared: {stats.get('chi_squared', 'N/A'):.2f}")
    print(f"       Interpretation: {stats.get('interpretation', 'N/A')}")

    hist_path = os.path.join(FIGURES_DIR, "near_miss_distribution.png")
    try:
        create_histogram(near_misses, hist_path)
        print(f"       Histogram saved to {hist_path}")
    except Exception as e:
        print(f"       Warning: Could not create histogram: {e}")

    return near_misses, stats


def main():
    print("=" * 60)
    print("Perfect Cuboid Research: Complete Pipeline")
    print("=" * 60)
    print()

    ensure_dirs()

    # Run all search methods
    bf_results = run_brute_force()
    sieve_results = run_modular_sieve()
    novel_results = run_novel_search()
    saunderson, euler, bremner = run_parametric()

    # Verify brute force results
    run_verification(bf_results)

    # Combine all bricks for near-miss analysis
    all_bricks = []
    seen = set()
    for brick_list in [bf_results, sieve_results, novel_results]:
        for brick in brick_list:
            key = tuple(sorted(brick["edges"]))
            if key not in seen:
                seen.add(key)
                all_bricks.append(brick)

    for family_results in [saunderson, euler, bremner]:
        for brick in family_results:
            edges = brick.get("edges", [])
            if len(edges) == 3:
                key = tuple(sorted(edges))
                if key not in seen:
                    seen.add(key)
                    all_bricks.append(brick)

    print(f"\nTotal unique Euler bricks: {len(all_bricks)}")

    # Near-miss analysis
    near_misses, stats = run_near_miss_analysis(all_bricks)

    # Check for perfect cuboid
    perfect_found = any(
        b.get("is_perfect_cuboid", False) for b in all_bricks
    )

    print()
    print("=" * 60)
    if perfect_found:
        print("RESULT: PERFECT CUBOID FOUND!")
    else:
        print("RESULT: No perfect cuboid found.")
    print("=" * 60)


if __name__ == "__main__":
    main()
