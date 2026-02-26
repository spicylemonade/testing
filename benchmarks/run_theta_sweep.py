"""Test accuracy vs theta parameter for Barnes-Hut approximation.

Runs Barnes-Hut with theta = 0.3, 0.5, 0.7, 1.0 on a 1000-particle
Plummer sphere for 100 timesteps. Records RMS force error and energy drift.
"""

import json
import time
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.initial_conditions import plummer_sphere
from src.forces.brute_force_vec import compute_forces_vectorized
from src.forces.barnes_hut import compute_forces_barnes_hut
from src.integrators.leapfrog import leapfrog_step
from src.metrics import kinetic_energy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def potential_energy_vec(system):
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


def main():
    N = 1000
    n_steps = 100
    dt = 0.01
    seed = 42
    thetas = [0.3, 0.5, 0.7, 1.0]

    results = []

    for theta in thetas:
        print(f"\n--- theta={theta} ---", flush=True)
        system = plummer_sphere(N=N, seed=seed)

        # Force accuracy (single evaluation)
        acc_exact = compute_forces_vectorized(system)
        t0 = time.perf_counter()
        acc_bh = compute_forces_barnes_hut(system, theta=theta)
        t_bh = time.perf_counter() - t0

        norms = np.sqrt(np.sum(acc_exact ** 2, axis=1))
        mask = norms > 1e-12
        rel_err = np.sqrt(np.sum((acc_bh[mask] - acc_exact[mask]) ** 2, axis=1)) / norms[mask]
        rms_err = float(np.sqrt(np.mean(rel_err ** 2)))
        max_err = float(np.max(rel_err))
        print(f"  Force RMS error: {rms_err:.4e}, max: {max_err:.4e}")
        print(f"  Force eval time: {t_bh:.3f}s")

        # Energy drift (100 steps)
        system = plummer_sphere(N=N, seed=seed)
        E0 = total_energy_vec(system)
        force_func = lambda s, th=theta: compute_forces_barnes_hut(s, theta=th)
        acc = force_func(system)
        t0 = time.perf_counter()
        for _ in range(n_steps):
            acc = leapfrog_step(system, acc, dt, force_func=force_func)
        t_sim = time.perf_counter() - t0
        E_final = total_energy_vec(system)
        drift = abs((E_final - E0) / E0) if E0 != 0 else 0.0
        print(f"  Energy drift: {drift:.4e}")
        print(f"  Sim time: {t_sim:.1f}s")

        results.append({
            "theta": theta,
            "N": N,
            "rms_force_error": rms_err,
            "max_force_error": max_err,
            "energy_drift": float(drift),
            "force_eval_time_s": round(t_bh, 4),
            "sim_100steps_time_s": round(t_sim, 2),
        })

    # Save results
    out_path = os.path.join("results", "theta_sweep.json")
    with open(out_path, "w") as f:
        json.dump({"theta_sweep": results, "N": N, "n_steps": n_steps, "dt": dt}, f, indent=2)
    print(f"\nResults saved to {out_path}")

    # Plot accuracy vs speed
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ts = [r["theta"] for r in results]
    rms_errs = [r["rms_force_error"] for r in results]
    drifts = [r["energy_drift"] for r in results]
    times = [r["force_eval_time_s"] for r in results]

    # Left: error vs theta
    ax1.semilogy(ts, rms_errs, "o-", color="#e74c3c", label="RMS force error", linewidth=2, markersize=8)
    ax1.semilogy(ts, drifts, "s-", color="#3498db", label="Energy drift (100 steps)", linewidth=2, markersize=8)
    ax1.set_xlabel(r"Opening angle $\theta$")
    ax1.set_ylabel("Relative error")
    ax1.set_title("Accuracy vs Opening Angle")
    ax1.legend()

    # Right: error vs speed (trade-off)
    ax2.loglog(times, rms_errs, "o-", color="#e74c3c", linewidth=2, markersize=8)
    for i, t in enumerate(ts):
        ax2.annotate(f"θ={t}", (times[i], rms_errs[i]), textcoords="offset points",
                     xytext=(10, 5), fontsize=9)
    ax2.set_xlabel("Force evaluation time (s)")
    ax2.set_ylabel("RMS force error")
    ax2.set_title("Accuracy–Speed Trade-off")

    fig.suptitle("Barnes-Hut: Opening Angle Parameter Study (N=1000)", fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig("figures/theta_sweep.png", dpi=150, bbox_inches="tight")
    fig.savefig("figures/theta_sweep.pdf", bbox_inches="tight")
    plt.close(fig)
    print("Saved figures/theta_sweep.png and .pdf")


if __name__ == "__main__":
    main()
