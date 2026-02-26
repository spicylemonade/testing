#!/usr/bin/env python3
"""Baseline benchmark: brute-force O(N^2) solver timing and energy drift."""

import json
import time
import signal
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bodies import Body, System
from src.forces.brute_force import compute_forces
from src.integrators.leapfrog import leapfrog_step
from src.metrics import total_energy


class ComputeTimeout(Exception):
    pass


def _handler(signum, frame):
    raise ComputeTimeout()


def generate_plummer_sphere(N, seed=42):
    """Generate N bodies from a Plummer model distribution."""
    rng = np.random.RandomState(seed)
    bodies = []
    for _ in range(N):
        # Plummer model: rejection sampling
        r = 1.0 / np.sqrt(rng.uniform(0, 1) ** (-2.0 / 3.0) - 1.0)
        theta = rng.uniform(0, 2 * np.pi)
        pos = np.array([r * np.cos(theta), r * np.sin(theta)])

        # Velocity from virial equilibrium (simplified)
        v_esc = np.sqrt(2.0) * (1 + r**2) ** (-0.25)
        q = 0.0
        while True:
            q = rng.uniform(0, 1)
            g = q**2 * (1 - q**2) ** 3.5
            if rng.uniform(0, 0.1) < g:
                break
        v = q * v_esc
        v_theta = rng.uniform(0, 2 * np.pi)
        vel = np.array([v * np.cos(v_theta), v * np.sin(v_theta)])

        bodies.append(Body(mass=1.0 / N, position=pos, velocity=vel))
    return bodies


def run_benchmark(N, n_steps=100, dt=0.01, timeout_sec=300):
    """Run brute-force benchmark for N particles."""
    bodies = generate_plummer_sphere(N)
    system = System(bodies=bodies, G=1.0, epsilon=0.01)

    E0 = total_energy(system)

    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(timeout_sec)

    try:
        t_start = time.perf_counter()
        acc = compute_forces(system)
        for step in range(n_steps):
            acc = leapfrog_step(system, acc, dt, force_func=compute_forces)
        t_elapsed = time.perf_counter() - t_start
        signal.alarm(0)
    except ComputeTimeout:
        signal.alarm(0)
        return {"N": N, "time_s": None, "energy_drift": None, "status": "timeout"}

    E_final = total_energy(system)
    energy_drift = abs((E_final - E0) / E0) if E0 != 0 else 0.0

    return {
        "N": N,
        "time_s": round(t_elapsed, 4),
        "energy_drift": float(energy_drift),
        "status": "ok",
    }


def main():
    N_values = [10, 50, 100, 500, 1000]
    results = []

    for N in N_values:
        print(f"Running N={N}...")
        result = run_benchmark(N, n_steps=100, timeout_sec=300)
        results.append(result)
        if result["time_s"] is not None:
            print(f"  N={N}: time={result['time_s']:.4f}s, drift={result['energy_drift']:.2e}")
        else:
            print(f"  N={N}: TIMEOUT")

    # Check O(N^2) scaling
    print("\nScaling analysis:")
    for i in range(1, len(results)):
        if results[i]["time_s"] and results[i - 1]["time_s"] and results[i - 1]["time_s"] > 0:
            N_ratio = results[i]["N"] / results[i - 1]["N"]
            time_ratio = results[i]["time_s"] / results[i - 1]["time_s"]
            expected_ratio = N_ratio ** 2
            print(f"  N: {results[i-1]['N']} -> {results[i]['N']} "
                  f"(ratio {N_ratio:.1f}x): time ratio = {time_ratio:.1f}x "
                  f"(expected ~{expected_ratio:.1f}x for O(N^2))")

    # Save results
    os.makedirs("results", exist_ok=True)
    output = {
        "benchmark": "brute_force_baseline",
        "n_steps": 100,
        "dt": 0.01,
        "epsilon": 0.01,
        "results": results,
    }
    with open("results/benchmark_baseline.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to results/benchmark_baseline.json")


if __name__ == "__main__":
    main()
