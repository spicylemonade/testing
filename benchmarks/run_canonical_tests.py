"""Run canonical test problems with trajectory visualizations.

(1) Kepler 2-body elliptical orbit (e=0.5)
(2) Figure-eight 3-body choreography
(3) Plummer sphere N=500
"""

import json
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bodies import Body, System
from src.initial_conditions import kepler_elliptical, figure_eight, plummer_sphere
from src.forces.brute_force_vec import compute_forces_vectorized
from src.integrators.leapfrog import leapfrog_step
from src.integrators.yoshida import yoshida_step
from src.metrics import total_energy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def run_kepler():
    """Run Kepler orbit for one period and check closure."""
    print("=== Kepler Orbit (e=0.5) ===")
    system = kepler_elliptical(e=0.5, epsilon=1e-10)
    # Period: T = 2*pi*sqrt(a^3/(G*M)) = 2*pi for a=1, G=1, M=1
    T = 2 * np.pi
    dt = 0.001
    n_steps = int(T / dt)

    force_func = compute_forces_vectorized
    acc = force_func(system)

    # Record trajectory of orbiting body
    positions = [system.positions[1].copy()]
    initial_pos = system.positions[1].copy()

    for _ in range(n_steps):
        acc = yoshida_step(system, acc, dt, force_func=force_func)
        positions.append(system.positions[1].copy())

    positions = np.array(positions)
    final_pos = system.positions[1]

    # Check closure
    closure_error = np.linalg.norm(final_pos - initial_pos)
    closure_pct = closure_error / np.linalg.norm(initial_pos) * 100
    print(f"  Period: T={T:.4f}")
    print(f"  Closure error: {closure_error:.6e} ({closure_pct:.4f}%)")

    # Plot
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(positions[:, 0], positions[:, 1], color="#3498db", linewidth=1.0, alpha=0.8)
    ax.plot(0, 0, "o", color="#e74c3c", markersize=12, label="Central mass", zorder=5)
    ax.plot(initial_pos[0], initial_pos[1], "s", color="#2ecc71", markersize=8,
            label="Start (periapsis)", zorder=5)
    ax.plot(final_pos[0], final_pos[1], "^", color="#f39c12", markersize=8,
            label="End (1 period)", zorder=5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Kepler Orbit (e=0.5), closure: {closure_pct:.4f}%")
    ax.set_aspect("equal")
    ax.legend()
    fig.tight_layout()
    fig.savefig("figures/kepler_orbit.png", dpi=150, bbox_inches="tight")
    fig.savefig("figures/kepler_orbit.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Saved: figures/kepler_orbit.png")

    return {"closure_error": float(closure_error), "closure_pct": float(closure_pct)}


def run_figure_eight():
    """Run figure-eight 3-body choreography."""
    print("\n=== Figure-Eight 3-Body ===")
    system = figure_eight(epsilon=1e-10)
    # Period: T ≈ 6.3259
    T = 6.3259
    dt = 0.0005
    n_steps = int(T / dt)

    force_func = compute_forces_vectorized
    acc = force_func(system)
    E0 = total_energy(system)

    traj = [[] for _ in range(3)]
    for i in range(3):
        traj[i].append(system.positions[i].copy())

    for _ in range(n_steps):
        acc = yoshida_step(system, acc, dt, force_func=force_func)
        for i in range(3):
            traj[i].append(system.positions[i].copy())

    E_final = total_energy(system)
    drift = abs((E_final - E0) / E0)
    print(f"  Energy drift: {drift:.2e}")

    traj = [np.array(t) for t in traj]

    # Plot
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#e74c3c", "#3498db", "#2ecc71"]
    for i in range(3):
        ax.plot(traj[i][:, 0], traj[i][:, 1], color=colors[i], linewidth=0.8, alpha=0.7,
                label=f"Body {i+1}")
        ax.plot(traj[i][0, 0], traj[i][0, 1], "o", color=colors[i], markersize=8, zorder=5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Figure-Eight Choreography (1 period, |ΔE/E₀|={drift:.1e})")
    ax.set_aspect("equal")
    ax.legend()
    fig.tight_layout()
    fig.savefig("figures/figure_eight_orbit.png", dpi=150, bbox_inches="tight")
    fig.savefig("figures/figure_eight_orbit.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Saved: figures/figure_eight_orbit.png")

    return {"energy_drift": float(drift), "period": T}


def run_plummer():
    """Run Plummer sphere N=500."""
    print("\n=== Plummer Sphere (N=500) ===")
    system = plummer_sphere(N=500, seed=42)
    dt = 0.01
    n_steps = 200  # 2 dynamical times approximately

    force_func = compute_forces_vectorized
    acc = force_func(system)
    E0 = total_energy(system)

    # Save initial and final snapshots
    initial_pos = system.positions.copy()

    for step in range(n_steps):
        acc = leapfrog_step(system, acc, dt, force_func=force_func)

    E_final = total_energy(system)
    drift = abs((E_final - E0) / E0)
    final_pos = system.positions.copy()
    print(f"  Energy drift: {drift:.2e}")

    # Plot: initial and final side by side
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.scatter(initial_pos[:, 0], initial_pos[:, 1], s=2, alpha=0.5, color="#3498db")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_title("t = 0")
    ax1.set_aspect("equal")
    lim = 5
    ax1.set_xlim(-lim, lim)
    ax1.set_ylim(-lim, lim)

    ax2.scatter(final_pos[:, 0], final_pos[:, 1], s=2, alpha=0.5, color="#e74c3c")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_title(f"t = {n_steps * dt:.1f}")
    ax2.set_aspect("equal")
    ax2.set_xlim(-lim, lim)
    ax2.set_ylim(-lim, lim)

    fig.suptitle(f"Plummer Sphere N=500 (|ΔE/E₀|={drift:.1e})", fontsize=14)
    fig.tight_layout()
    fig.savefig("figures/plummer_sphere.png", dpi=150, bbox_inches="tight")
    fig.savefig("figures/plummer_sphere.pdf", bbox_inches="tight")
    plt.close(fig)
    print("  Saved: figures/plummer_sphere.png")

    return {"energy_drift": float(drift), "n_particles": 500, "n_steps": n_steps}


def main():
    results = {}

    results["kepler"] = run_kepler()
    results["figure_eight"] = run_figure_eight()
    results["plummer"] = run_plummer()

    out_path = os.path.join("results", "canonical_tests.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")

    # Verify acceptance: Kepler closure < 1%
    kc = results["kepler"]["closure_pct"]
    print(f"\nKepler closure: {kc:.4f}% {'PASS' if kc < 1.0 else 'FAIL'} (< 1% required)")


if __name__ == "__main__":
    main()
