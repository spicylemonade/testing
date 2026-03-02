#!/usr/bin/env python3
"""Adaptive time-stepping experiment (item_014).

Compares fixed-dt vs adaptive-dt leapfrog on a highly eccentric orbit.
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bodies import kepler_orbit, G
from src.forces import compute_forces_vectorized
from src.integrators import leapfrog_step, adaptive_leapfrog
from src.metrics import total_energy


def run_adaptive_experiment():
    # High eccentricity orbit
    e = 0.95
    m1, m2 = 1.0, 1.0
    a = 1.0
    eps = 1e-4  # very small softening

    sys = kepler_orbit(m1=m1, m2=m2, a=a, e=e)
    M = m1 + m2
    T_period = 2 * np.pi * np.sqrt(a**3 / (G * M))

    n_orbits = 5
    T_total = n_orbits * T_period

    def force_fn(pos, mass):
        return compute_forces_vectorized(pos, mass, eps=eps)

    # --- Fixed dt ---
    # Use dt that would be reasonable for circular orbit
    dt_fixed = T_period / 1000
    n_steps_fixed = int(T_total / dt_fixed)

    pos_f = sys.pos.copy()
    vel_f = sys.vel.copy()
    E0 = total_energy(pos_f, vel_f, sys.mass, eps=eps)

    max_err_fixed = 0.0
    for step in range(n_steps_fixed):
        pos_f, vel_f = leapfrog_step(pos_f, vel_f, sys.mass, dt_fixed, force_fn)
        E = total_energy(pos_f, vel_f, sys.mass, eps=eps)
        err = abs((E - E0) / E0)
        max_err_fixed = max(max_err_fixed, err)

    # --- Adaptive dt ---
    pos_a = sys.pos.copy()
    vel_a = sys.vel.copy()
    E0_a = total_energy(pos_a, vel_a, sys.mass, eps=eps)

    t = 0.0
    max_err_adaptive = 0.0
    n_steps_adaptive = 0
    dt_min_used = float("inf")
    dt_max_used = 0.0

    while t < T_total:
        pos_a, vel_a, dt_used = adaptive_leapfrog(
            pos_a, vel_a, sys.mass,
            dt_max=T_period / 100,
            force_fn=force_fn,
            eps=eps,
            eta=0.02,
        )
        t += dt_used
        n_steps_adaptive += 1
        dt_min_used = min(dt_min_used, dt_used)
        dt_max_used = max(dt_max_used, dt_used)

        E = total_energy(pos_a, vel_a, sys.mass, eps=eps)
        err = abs((E - E0_a) / E0_a)
        max_err_adaptive = max(max_err_adaptive, err)

    print(f"Eccentricity: {e}")
    print(f"Period: {T_period:.4f}, Total time: {T_total:.4f}")
    print(f"\n--- Fixed dt={dt_fixed:.6f} ---")
    print(f"Steps: {n_steps_fixed}")
    print(f"Max |dE/E|: {max_err_fixed:.2e}")
    print(f"\n--- Adaptive dt ---")
    print(f"Steps: {n_steps_adaptive}")
    print(f"dt range: [{dt_min_used:.6f}, {dt_max_used:.6f}]")
    print(f"Max |dE/E|: {max_err_adaptive:.2e}")
    print(f"\nImprovement factor: {max_err_fixed / max(max_err_adaptive, 1e-30):.1f}x")

    results = {
        "eccentricity": float(e),
        "n_orbits": int(n_orbits),
        "T_period": float(T_period),
        "fixed_dt": {
            "dt": float(dt_fixed),
            "n_steps": int(n_steps_fixed),
            "max_relative_energy_error": float(max_err_fixed),
        },
        "adaptive_dt": {
            "dt_min": float(dt_min_used),
            "dt_max": float(dt_max_used),
            "n_steps": int(n_steps_adaptive),
            "max_relative_energy_error": float(max_err_adaptive),
            "eta": 0.02,
        },
        "improvement_factor": float(max_err_fixed / max(max_err_adaptive, 1e-30)),
    }

    os.makedirs("results/experiments", exist_ok=True)
    with open("results/experiments/adaptive_dt.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to results/experiments/adaptive_dt.json")
    return results


if __name__ == "__main__":
    run_adaptive_experiment()
