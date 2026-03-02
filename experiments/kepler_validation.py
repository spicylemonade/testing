#!/usr/bin/env python3
"""Kepler orbit validation experiment (item_010).

Runs a two-body simulation for 10+ orbital periods using the leapfrog
integrator and measures energy conservation and orbital period accuracy.
"""

import json
import sys
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bodies import kepler_orbit, G
from src.forces import compute_forces_vectorized
from src.integrators import leapfrog_step
from src.metrics import total_energy, total_momentum, angular_momentum

# --- Publication-grade plot setup ---
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({
    "figure.figsize": (10, 8),
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.family": "serif",
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})


def run_kepler_validation():
    # --- Setup ---
    m1, m2 = 1.0, 1.0
    a = 1.0      # semi-major axis
    e = 0.5      # eccentricity
    eps = 1e-6   # very small softening for validation

    sys = kepler_orbit(m1=m1, m2=m2, a=a, e=e)

    # Analytical orbital period: T = 2*pi*sqrt(a^3/(G*M))
    M = m1 + m2
    T_analytical = 2 * np.pi * np.sqrt(a**3 / (G * M))

    # Simulation parameters
    n_orbits = 10
    dt = T_analytical / 20000  # ~20000 steps per orbit for tight energy conservation
    n_steps = int(n_orbits * T_analytical / dt)
    T_total = n_steps * dt

    print(f"Kepler validation: e={e}, a={a}, T_analytical={T_analytical:.6f}")
    print(f"dt={dt:.6f}, n_steps={n_steps}, T_total={T_total:.4f}")

    # Force function
    def force_fn(pos, mass):
        return compute_forces_vectorized(pos, mass, eps=eps)

    # --- Run simulation ---
    pos = sys.pos.copy()
    vel = sys.vel.copy()
    mass = sys.mass

    E0 = total_energy(pos, vel, mass, eps=eps)
    P0 = total_momentum(vel, mass)
    L0 = angular_momentum(pos, vel, mass)

    # Storage
    trajectory_x = [pos[:, 0].copy()]
    trajectory_y = [pos[:, 1].copy()]
    times = [0.0]
    energies = [E0]
    rel_sep = [np.linalg.norm(pos[1] - pos[0])]

    for step in range(n_steps):
        pos, vel = leapfrog_step(pos, vel, mass, dt, force_fn)

        t = (step + 1) * dt
        if step % 10 == 0 or step == n_steps - 1:
            trajectory_x.append(pos[:, 0].copy())
            trajectory_y.append(pos[:, 1].copy())
            times.append(t)
            energies.append(total_energy(pos, vel, mass, eps=eps))
            rel_sep.append(np.linalg.norm(pos[1] - pos[0]))

    # --- Compute metrics ---
    E_final = total_energy(pos, vel, mass, eps=eps)
    P_final = total_momentum(vel, mass)
    L_final = angular_momentum(pos, vel, mass)

    max_rel_energy_err = max(abs((E - E0) / E0) for E in energies)
    final_rel_energy_err = abs((E_final - E0) / E0)
    momentum_drift = np.linalg.norm(P_final - P0)
    angular_momentum_drift = abs(L_final - L0) / abs(L0)

    # --- Estimate orbital period from separation oscillation ---
    rel_sep = np.array(rel_sep)
    times_arr = np.array(times)

    # Find periapsis passages (local minima in separation)
    peri_times = []
    for i in range(1, len(rel_sep) - 1):
        if rel_sep[i] < rel_sep[i - 1] and rel_sep[i] < rel_sep[i + 1]:
            peri_times.append(times_arr[i])

    if len(peri_times) >= 2:
        measured_periods = np.diff(peri_times)
        T_measured = np.mean(measured_periods)
        T_error = abs(T_measured - T_analytical) / T_analytical
    else:
        T_measured = float("nan")
        T_error = float("nan")

    print(f"\n--- Results ---")
    print(f"Max relative energy error:    {max_rel_energy_err:.2e}")
    print(f"Final relative energy error:  {final_rel_energy_err:.2e}")
    print(f"Momentum drift:               {momentum_drift:.2e}")
    print(f"Angular momentum drift:       {angular_momentum_drift:.2e}")
    print(f"Analytical period:            {T_analytical:.6f}")
    print(f"Measured period:              {T_measured:.6f}")
    print(f"Period error:                 {T_error:.2e}")
    print(f"Periapsis passages found:     {len(peri_times)}")

    # --- Save results ---
    results = {
        "eccentricity": float(e),
        "semi_major_axis": float(a),
        "softening": float(eps),
        "dt": float(dt),
        "n_steps": int(n_steps),
        "n_orbits": int(n_orbits),
        "T_analytical": float(T_analytical),
        "T_measured": float(T_measured),
        "T_error": float(T_error),
        "max_relative_energy_error": float(max_rel_energy_err),
        "final_relative_energy_error": float(final_rel_energy_err),
        "momentum_drift": float(momentum_drift),
        "angular_momentum_relative_drift": float(angular_momentum_drift),
        "n_periapsis_passages": len(peri_times),
        "acceptance": {
            "energy_drift_lt_1e-6": bool(max_rel_energy_err < 1e-6),
            "period_error_lt_1pct": bool(T_error < 0.01) if not np.isnan(T_error) else False,
        },
    }

    os.makedirs("results/baseline", exist_ok=True)
    with open("results/baseline/kepler_validation.json", "w") as f:
        json.dump(results, f, indent=2)

    # --- Create figure ---
    traj_x = np.array(trajectory_x)
    traj_y = np.array(trajectory_y)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Panel 1: Trajectory
    ax = axes[0, 0]
    ax.plot(traj_x[:, 0], traj_y[:, 0], "b-", alpha=0.7, linewidth=0.5, label="Body 1")
    ax.plot(traj_x[:, 1], traj_y[:, 1], "r-", alpha=0.7, linewidth=0.5, label="Body 2")
    ax.plot(traj_x[0, 0], traj_y[0, 0], "bo", markersize=8)
    ax.plot(traj_x[0, 1], traj_y[0, 1], "ro", markersize=8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Kepler Orbit (e={e}, {n_orbits} periods)")
    ax.set_aspect("equal")
    ax.legend()

    # Panel 2: Energy conservation
    ax = axes[0, 1]
    rel_errors = [(E - E0) / E0 for E in energies]
    ax.plot(times, rel_errors, "k-", linewidth=0.5)
    ax.set_xlabel("Time")
    ax.set_ylabel("Relative Energy Error (E-E₀)/E₀")
    ax.set_title(f"Energy Conservation (max |dE/E| = {max_rel_energy_err:.2e})")
    ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)

    # Panel 3: Separation vs time
    ax = axes[1, 0]
    ax.plot(times_arr, rel_sep, "g-", linewidth=0.8)
    ax.set_xlabel("Time")
    ax.set_ylabel("Separation |r₂ - r₁|")
    ax.set_title(f"Orbital Separation (T_meas={T_measured:.4f}, err={T_error:.2e})")
    for pt in peri_times[:5]:
        ax.axvline(x=pt, color="red", alpha=0.3, linestyle="--")

    # Panel 4: Relative orbit
    ax = axes[1, 1]
    rel_x = traj_x[:, 1] - traj_x[:, 0]
    rel_y = traj_y[:, 1] - traj_y[:, 0]
    ax.plot(rel_x, rel_y, "purple", linewidth=0.5, alpha=0.8)
    ax.plot(rel_x[0], rel_y[0], "ko", markersize=8, label="Start")
    ax.set_xlabel("Δx")
    ax.set_ylabel("Δy")
    ax.set_title("Relative Orbit (should be closed ellipse)")
    ax.set_aspect("equal")
    ax.legend()

    plt.tight_layout()

    os.makedirs("figures", exist_ok=True)
    plt.savefig("figures/kepler_validation.png", dpi=300, bbox_inches="tight")
    plt.savefig("figures/kepler_validation.pdf", bbox_inches="tight")
    plt.close()

    print(f"\nFigures saved to figures/kepler_validation.png and .pdf")
    print(f"Results saved to results/baseline/kepler_validation.json")

    return results


if __name__ == "__main__":
    results = run_kepler_validation()
    # Verify acceptance criteria
    assert results["acceptance"]["energy_drift_lt_1e-6"], \
        f"Energy drift {results['max_relative_energy_error']:.2e} exceeds 1e-6"
    assert results["acceptance"]["period_error_lt_1pct"], \
        f"Period error {results['T_error']:.2e} exceeds 1%"
    print("\nAll acceptance criteria met!")
