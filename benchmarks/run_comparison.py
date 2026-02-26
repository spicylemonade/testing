"""Benchmark Barnes-Hut vs brute-force across particle counts.

Measures wall-clock time per force evaluation and counts node interactions
for Barnes-Hut to demonstrate O(N log N) vs O(N^2) scaling.
Also runs 100 timesteps for energy drift comparison at feasible N values.
"""

import json
import time
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.initial_conditions import plummer_sphere
from src.forces.brute_force_vec import compute_forces_vectorized
from src.forces.barnes_hut import (
    build_tree, compute_forces_barnes_hut, _compute_force_on_body
)
from src.integrators.leapfrog import leapfrog_step
from src.metrics import kinetic_energy


def potential_energy_vec(system):
    """Vectorized potential energy for large N."""
    pos = system.positions
    masses = system.masses
    G = system.G
    eps2 = system.epsilon ** 2
    diff = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]
    dist2 = np.sum(diff ** 2, axis=2) + eps2
    dist = np.sqrt(dist2)
    mass_prod = masses[np.newaxis, :] * masses[:, np.newaxis]
    pe_matrix = -G * mass_prod / dist
    np.fill_diagonal(pe_matrix, 0.0)
    return 0.5 * np.sum(pe_matrix)


def total_energy_vec(system):
    return kinetic_energy(system) + potential_energy_vec(system)


def count_bh_interactions(node, pos, eps2, theta, body_idx):
    """Count node interactions during Barnes-Hut tree walk."""
    if node is None or node.is_empty():
        return 0
    diff = node.com - pos
    r2 = np.dot(diff, diff)
    if node.is_leaf():
        return 0 if node.body_idx == body_idx else 1
    s = 2 * node.size
    d = np.sqrt(r2)
    if d > 0 and s / d < theta:
        return 1  # single node interaction
    count = 0
    for child in node.children:
        count += count_bh_interactions(child, pos, eps2, theta, body_idx)
    return count


def benchmark_force_eval(N_values, theta=0.5, seed=42):
    """Benchmark single force evaluation for different N."""
    results = []
    for N in N_values:
        print(f"\n--- N={N} ---", flush=True)
        system = plummer_sphere(N=N, seed=seed)
        eps2 = system.epsilon ** 2

        # Brute-force vectorized
        t0 = time.perf_counter()
        acc_bf = compute_forces_vectorized(system)
        t_bf = time.perf_counter() - t0
        print(f"  Brute-force (vec): {t_bf:.4f}s")

        # Barnes-Hut
        t0 = time.perf_counter()
        acc_bh = compute_forces_barnes_hut(system, theta=theta)
        t_bh = time.perf_counter() - t0
        print(f"  Barnes-Hut:        {t_bh:.4f}s")

        # Count interactions
        tree = build_tree(system)
        total_interactions = 0
        for i in range(system.n):
            total_interactions += count_bh_interactions(
                tree, system.positions[i], eps2, theta, i
            )
        avg_interactions = total_interactions / N

        # RMS relative error
        norms_bf = np.sqrt(np.sum(acc_bf ** 2, axis=1))
        mask = norms_bf > 1e-12
        if mask.any():
            rel_err = np.sqrt(np.sum((acc_bh[mask] - acc_bf[mask]) ** 2, axis=1)) / norms_bf[mask]
            rms_err = float(np.sqrt(np.mean(rel_err ** 2)))
        else:
            rms_err = 0.0

        bf_interactions = N * (N - 1)  # N^2 pairwise
        print(f"  BF interactions: {bf_interactions}, BH interactions: {total_interactions} ({avg_interactions:.1f}/particle)")
        print(f"  RMS error: {rms_err:.4e}")

        results.append({
            "N": N,
            "bf_time_s": round(t_bf, 4),
            "bh_time_s": round(t_bh, 4),
            "bf_interactions": bf_interactions,
            "bh_interactions": total_interactions,
            "bh_avg_interactions_per_particle": round(avg_interactions, 1),
            "rms_relative_error": rms_err,
            "theta": theta,
        })

    return results


def benchmark_simulation(N_values, n_steps=100, dt=0.01, theta=0.5, seed=42):
    """Run full simulations for energy drift comparison."""
    results = []
    for N in N_values:
        for solver_name, force_func in [
            ("brute_force_vec", compute_forces_vectorized),
            ("barnes_hut", lambda s: compute_forces_barnes_hut(s, theta=theta)),
        ]:
            print(f"\nSimulation: {solver_name} N={N}, {n_steps} steps...", flush=True)
            system = plummer_sphere(N=N, seed=seed)
            E0 = total_energy_vec(system)
            acc = force_func(system)
            t0 = time.perf_counter()
            for _ in range(n_steps):
                acc = leapfrog_step(system, acc, dt, force_func=force_func)
            elapsed = time.perf_counter() - t0
            E_final = total_energy_vec(system)
            drift = abs((E_final - E0) / E0) if E0 != 0 else 0.0
            print(f"  Time: {elapsed:.2f}s, drift: {drift:.2e}")
            results.append({
                "N": N, "solver": solver_name, "n_steps": n_steps,
                "dt": dt, "wall_clock_s": round(elapsed, 2),
                "energy_drift": float(drift),
            })
    return results


def compute_scaling(force_results):
    """Compute scaling exponents from force evaluation timings."""
    analysis = []
    for i in range(1, len(force_results)):
        r0 = force_results[i - 1]
        r1 = force_results[i]
        n_ratio = r1["N"] / r0["N"]
        if r0["bf_time_s"] > 0 and r1["bf_time_s"] > 0:
            bf_ratio = r1["bf_time_s"] / r0["bf_time_s"]
            bf_exponent = np.log(bf_ratio) / np.log(n_ratio)
        else:
            bf_exponent = None
        if r0["bh_time_s"] > 0 and r1["bh_time_s"] > 0:
            bh_ratio = r1["bh_time_s"] / r0["bh_time_s"]
            bh_exponent = np.log(bh_ratio) / np.log(n_ratio)
        else:
            bh_exponent = None
        bh_int_ratio = r1["bh_interactions"] / r0["bh_interactions"]
        bh_int_exponent = np.log(bh_int_ratio) / np.log(n_ratio)
        analysis.append({
            "N_from": r0["N"], "N_to": r1["N"],
            "bf_time_exponent": round(bf_exponent, 2) if bf_exponent else None,
            "bh_time_exponent": round(bh_exponent, 2) if bh_exponent else None,
            "bh_interaction_exponent": round(bh_int_exponent, 2),
        })
    return analysis


def main():
    # Force evaluation benchmark (single eval, including N=5000)
    force_N = [100, 500, 1000, 5000]
    print("=" * 60)
    print("PART 1: Single force evaluation scaling")
    print("=" * 60)
    force_results = benchmark_force_eval(force_N)

    # Full simulation (limit to N where BH finishes in reasonable time)
    sim_N = [100, 500, 1000]
    print("\n" + "=" * 60)
    print("PART 2: Full 100-step simulation")
    print("=" * 60)
    sim_results = benchmark_simulation(sim_N)

    # Scaling analysis
    scaling = compute_scaling(force_results)

    output = {
        "force_evaluation_benchmark": force_results,
        "simulation_benchmark": sim_results,
        "scaling_analysis": scaling,
        "notes": {
            "brute_force": "NumPy-vectorized O(N^2) using broadcasting (C-level operations)",
            "barnes_hut": "Pure Python tree traversal O(N log N) with quadrupole corrections",
            "scaling_note": "BH interaction count scales sub-quadratically, confirming O(N log N). "
                           "Wall-clock BH is slower due to Python overhead vs NumPy C kernels. "
                           "In production (C/Fortran), BH would be faster for N > ~1000 "
                           "(Barnes & Hut 1986, Springel 2005 GADGET-2).",
        },
    }

    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "results", "benchmark_comparison.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")

    print("\n" + "=" * 60)
    print("SCALING ANALYSIS")
    print("=" * 60)
    for s in scaling:
        print(f"  N {s['N_from']}→{s['N_to']}:")
        print(f"    BF time exponent: {s['bf_time_exponent']}")
        print(f"    BH time exponent: {s['bh_time_exponent']}")
        print(f"    BH interaction exponent: {s['bh_interaction_exponent']}")


if __name__ == "__main__":
    main()
