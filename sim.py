"""Minimal simulation loop for N-body gravity.

Runs a two-body Kepler validation, logging conservation metrics and
generating trajectory plots.

Reference: Danby (1988) for analytical Kepler solution.
"""

from __future__ import annotations

import json
import sys
import os
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from src.forces.brute_force import compute_forces_brute
from src.integrators.leapfrog import step_leapfrog
from src.metrics import (
    total_energy,
    linear_momentum,
    angular_momentum,
    relative_energy_error,
)


def setup_kepler_orbit(
    M: float = 1.0,
    m: float = 1e-6,
    a: float = 1.0,
    e: float = 0.0,
    G: float = 1.0,
) -> dict:
    """Set up a Kepler two-body problem.

    Places the massive body at origin and the test particle at
    pericenter on the positive x-axis.

    Args:
        M: Central mass.
        m: Orbiting mass (test particle).
        a: Semi-major axis.
        e: Eccentricity (0 = circular).
        G: Gravitational constant.

    Returns:
        Dictionary with masses, positions, velocities, and orbital parameters.
    """
    r_peri = a * (1 - e)
    # Vis-viva: v^2 = GM(2/r - 1/a)
    v_peri = np.sqrt(G * (M + m) * (2.0 / r_peri - 1.0 / a))

    masses = np.array([M, m])
    positions = np.array([[0.0, 0.0], [r_peri, 0.0]])
    velocities = np.array([[0.0, 0.0], [0.0, v_peri]])

    period = 2 * np.pi * np.sqrt(a ** 3 / (G * (M + m)))

    return {
        "masses": masses,
        "positions": positions,
        "velocities": velocities,
        "G": G,
        "epsilon": 0.0,  # No softening for analytical comparison
        "period": period,
        "semi_major_axis": a,
        "eccentricity": e,
    }


def run_simulation(
    masses: np.ndarray,
    positions: np.ndarray,
    velocities: np.ndarray,
    G: float,
    epsilon: float,
    dt: float,
    n_steps: int,
    log_interval: int = 1,
) -> dict:
    """Run N-body simulation with leapfrog integrator.

    Args:
        masses: (N,) mass array.
        positions: (N, 2) initial positions.
        velocities: (N, 2) initial velocities.
        G: Gravitational constant.
        epsilon: Softening length.
        dt: Timestep.
        n_steps: Total steps.
        log_interval: Steps between metric logging.

    Returns:
        Dictionary with trajectory data and conservation metrics.
    """
    def force_fn(m, p, **kw):
        return compute_forces_brute(m, p, G=G, epsilon=epsilon)

    pos = positions.copy()
    vel = velocities.copy()
    acc = force_fn(masses, pos)

    # Initial conservation quantities
    E0 = total_energy(masses, pos, vel, G=G, epsilon=epsilon)
    p0 = linear_momentum(masses, vel)
    L0 = angular_momentum(masses, pos, vel)

    # Storage
    n = len(masses)
    trajectory = np.zeros((n_steps // log_interval + 1, n, 2))
    energy_log = []
    momentum_log = []
    angular_momentum_log = []
    times = []

    trajectory[0] = pos.copy()
    energy_log.append({"t": 0.0, "E": E0, "dE_rel": 0.0})
    momentum_log.append({"t": 0.0, "px": float(p0[0]), "py": float(p0[1])})
    angular_momentum_log.append({"t": 0.0, "L": L0})
    times.append(0.0)

    log_idx = 1

    for step in range(1, n_steps + 1):
        pos, vel, acc = step_leapfrog(masses, pos, vel, force_fn, dt, acc)

        if step % log_interval == 0:
            t = step * dt
            E = total_energy(masses, pos, vel, G=G, epsilon=epsilon)
            p = linear_momentum(masses, vel)
            L = angular_momentum(masses, pos, vel)

            trajectory[log_idx] = pos.copy()
            energy_log.append({
                "t": t,
                "E": E,
                "dE_rel": relative_energy_error(E, E0),
            })
            momentum_log.append({
                "t": t,
                "px": float(p[0]),
                "py": float(p[1]),
            })
            angular_momentum_log.append({"t": t, "L": L})
            times.append(t)
            log_idx += 1

    return {
        "trajectory": trajectory[:log_idx],
        "energy": energy_log,
        "momentum": momentum_log,
        "angular_momentum": angular_momentum_log,
        "times": times,
        "E0": E0,
        "final_E": energy_log[-1]["E"],
        "max_dE_rel": max(abs(e["dE_rel"]) for e in energy_log),
    }


def plot_kepler_orbit(trajectory: np.ndarray, output_path: str):
    """Generate Kepler orbit trajectory plot.

    Args:
        trajectory: (n_frames, n_bodies, 2) position history.
        output_path: Path to save PNG figure.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Publication-quality styling
    sns.set_theme(style="whitegrid", font_scale=1.2)
    plt.rcParams.update({
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "font.size": 12,
        "axes.linewidth": 1.2,
        "lines.linewidth": 1.5,
    })

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))

    # Plot orbiting body trajectory
    ax.plot(
        trajectory[:, 1, 0],
        trajectory[:, 1, 1],
        color=sns.color_palette("deep")[0],
        linewidth=1.0,
        alpha=0.8,
        label="Orbiting body",
    )

    # Mark central body
    ax.plot(0, 0, "o", color=sns.color_palette("deep")[1], markersize=10, label="Central body")

    # Mark start position
    ax.plot(
        trajectory[0, 1, 0],
        trajectory[0, 1, 1],
        "s",
        color=sns.color_palette("deep")[2],
        markersize=8,
        label="Start",
    )

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Kepler Two-Body Orbit (Leapfrog)")
    ax.set_aspect("equal")
    ax.legend(loc="upper right")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight")
    # Also save PDF
    pdf_path = output_path.replace(".png", ".pdf")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)


def main():
    """Run Kepler two-body validation."""
    print("Setting up Kepler two-body problem...")
    setup = setup_kepler_orbit(M=1.0, m=1e-6, a=1.0, e=0.0, G=1.0)

    dt = 0.01
    n_orbits = 10
    n_steps = int(n_orbits * setup["period"] / dt)
    log_interval = 10

    print(f"Running {n_steps} steps (dt={dt}, {n_orbits} orbits)...")
    results = run_simulation(
        masses=setup["masses"],
        positions=setup["positions"],
        velocities=setup["velocities"],
        G=setup["G"],
        epsilon=setup["epsilon"],
        dt=dt,
        n_steps=n_steps,
        log_interval=log_interval,
    )

    max_dE = results["max_dE_rel"]
    print(f"Max relative energy error: {max_dE:.2e}")
    print(f"E0 = {results['E0']:.6f}, E_final = {results['final_E']:.6f}")

    # Check acceptance criteria
    assert max_dE < 0.001, f"Energy drift {max_dE:.6f} exceeds 0.1%"
    print("PASS: Energy drift < 0.1% over 10 orbits")

    # Check orbital period
    # Detect crossings of positive x-axis
    traj = results["trajectory"]
    times = results["times"]
    crossings = []
    for i in range(1, len(traj)):
        prev_y = traj[i - 1, 1, 1]
        curr_y = traj[i, 1, 1]
        if prev_y < 0 and curr_y >= 0:
            crossings.append(times[i])

    if len(crossings) >= 2:
        measured_period = crossings[1] - crossings[0]
        analytical_period = setup["period"]
        period_error = abs(measured_period - analytical_period) / analytical_period
        print(f"Measured period: {measured_period:.4f}, analytical: {analytical_period:.4f}")
        print(f"Period error: {period_error:.4f}")
        assert period_error < 0.01, f"Period error {period_error:.4f} exceeds 1%"
        print("PASS: Period accuracy within 1%")

    # Save results
    Path("results/phase2").mkdir(parents=True, exist_ok=True)

    # Save validation data (without numpy arrays in JSON)
    validation = {
        "setup": {
            "M": 1.0, "m": 1e-6, "a": 1.0, "e": 0.0, "G": 1.0,
            "dt": dt, "n_steps": n_steps, "n_orbits": n_orbits,
            "analytical_period": setup["period"],
        },
        "results": {
            "E0": results["E0"],
            "final_E": results["final_E"],
            "max_dE_rel": max_dE,
            "measured_period": measured_period if len(crossings) >= 2 else None,
            "period_error": period_error if len(crossings) >= 2 else None,
        },
        "energy_log": results["energy"],
        "momentum_log": results["momentum"],
        "angular_momentum_log": results["angular_momentum"],
    }
    with open("results/phase2/kepler_validation.json", "w") as f:
        json.dump(validation, f, indent=2)
    print("Saved results/phase2/kepler_validation.json")

    # Generate trajectory plot
    plot_kepler_orbit(results["trajectory"], "figures/kepler_orbit.png")
    print("Saved figures/kepler_orbit.png")

    print("\nKepler validation complete. All checks passed.")


if __name__ == "__main__":
    main()
