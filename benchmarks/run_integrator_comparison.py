"""Compare integrator accuracy: Euler, leapfrog, Yoshida on Kepler and Pythagorean 3-body.

Records energy drift |dE/E0| time series and produces log-scale plots.
"""

import json
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bodies import Body, System
from src.forces.brute_force_vec import compute_forces_vectorized
from src.integrators.euler import euler_step
from src.integrators.leapfrog import leapfrog_step
from src.integrators.yoshida import yoshida_step
from src.metrics import total_energy
from src.initial_conditions import kepler_elliptical

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def pythagorean_3body(G=1.0, epsilon=1e-10):
    """Pythagorean 3-body problem: masses 3, 4, 5 at vertices of a right triangle."""
    bodies = [
        Body(mass=3.0, position=[1.0, 3.0], velocity=[0.0, 0.0]),
        Body(mass=4.0, position=[-2.0, -1.0], velocity=[0.0, 0.0]),
        Body(mass=5.0, position=[1.0, -1.0], velocity=[0.0, 0.0]),
    ]
    return System(bodies=bodies, G=G, epsilon=epsilon)


def run_simulation(system_factory, integrator_name, dt, total_time, sample_interval=1.0):
    """Run simulation and collect energy drift time series."""
    system = system_factory()
    force_func = compute_forces_vectorized

    E0 = total_energy(system)
    acc = force_func(system)

    n_steps = int(total_time / dt)
    sample_every = max(1, int(sample_interval / dt))

    times = [0.0]
    drifts = [0.0]

    for step in range(1, n_steps + 1):
        if integrator_name == "euler":
            euler_step(system, acc, dt)
            acc = force_func(system)
        elif integrator_name == "leapfrog":
            acc = leapfrog_step(system, acc, dt, force_func=force_func)
        elif integrator_name == "yoshida":
            acc = yoshida_step(system, acc, dt, force_func=force_func)

        if step % sample_every == 0:
            E = total_energy(system)
            drift = abs((E - E0) / E0) if E0 != 0 else 0.0
            times.append(step * dt)
            drifts.append(drift)

    return times, drifts


def make_plot(results, title, filename):
    """Create log-scale energy drift plot."""
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    colors = {"euler": "#e74c3c", "leapfrog": "#2ecc71", "yoshida": "#3498db"}
    labels = {"euler": "Symplectic Euler (1st)", "leapfrog": "Leapfrog (2nd)", "yoshida": "Yoshida (4th)"}

    for name, (times, drifts) in results.items():
        # Replace zeros with small value for log scale
        drifts_plot = [max(d, 1e-16) for d in drifts]
        ax.semilogy(times, drifts_plot, label=labels[name], color=colors[name], linewidth=1.5)

    ax.set_xlabel("Time")
    ax.set_ylabel(r"$|\Delta E / E_0|$")
    ax.set_title(title)
    ax.legend(frameon=True)
    ax.set_ylim(bottom=1e-16)

    fig.tight_layout()
    fig.savefig(filename, dpi=150, bbox_inches="tight")
    fig.savefig(filename.replace(".png", ".pdf"), bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {filename}")


def main():
    results_data = {}

    # --- Kepler orbit ---
    print("=== Kepler Orbit (e=0.5) ===")
    dt = 0.001
    total_time = 1000.0
    # Yoshida uses 3 force evals per step, so use 3x larger dt for fair comparison
    kepler_results = {}
    for name, step_dt in [("euler", dt), ("leapfrog", dt), ("yoshida", dt * 3)]:
        print(f"  Running {name} (dt={step_dt})...", flush=True)
        times, drifts = run_simulation(
            lambda: kepler_elliptical(e=0.5, epsilon=1e-10),
            name, step_dt, total_time, sample_interval=10.0
        )
        kepler_results[name] = (times, drifts)
        final_drift = drifts[-1] if drifts else 0
        print(f"    Final drift: {final_drift:.2e}")

    make_plot(kepler_results, "Energy Drift: Kepler Orbit (e=0.5)",
              os.path.join("figures", "integrator_kepler.png"))

    results_data["kepler"] = {
        name: {"times": t, "drifts": d, "final_drift": d[-1]}
        for name, (t, d) in kepler_results.items()
    }

    # --- Pythagorean 3-body ---
    # Large softening (0.05) to regularize close encounters in this chaotic problem.
    # Equal step counts for all integrators.
    print("\n=== Pythagorean 3-Body ===")
    dt = 0.0001
    total_time = 10.0  # Before first close encounter/ejection
    pyth_results = {}
    for name in ["euler", "leapfrog", "yoshida"]:
        print(f"  Running {name} (dt={dt})...", flush=True)
        times, drifts = run_simulation(
            lambda: pythagorean_3body(epsilon=0.05),
            name, dt, total_time, sample_interval=0.5
        )
        pyth_results[name] = (times, drifts)
        final_drift = drifts[-1] if drifts else 0
        print(f"    Final drift: {final_drift:.2e}")

    make_plot(pyth_results, "Energy Drift: Pythagorean 3-Body Problem",
              os.path.join("figures", "integrator_pythagorean.png"))

    results_data["pythagorean"] = {
        name: {"times": t, "drifts": d, "final_drift": d[-1]}
        for name, (t, d) in pyth_results.items()
    }

    # Save results
    out_path = os.path.join("results", "integrator_comparison.json")
    with open(out_path, "w") as f:
        json.dump(results_data, f, indent=2)
    print(f"\nResults saved to {out_path}")

    # Summary
    print("\n=== Summary ===")
    for problem in ["kepler", "pythagorean"]:
        print(f"\n{problem.upper()}:")
        for name in ["euler", "leapfrog", "yoshida"]:
            fd = results_data[problem][name]["final_drift"]
            print(f"  {name:12s}: final |dE/E0| = {fd:.2e}")


if __name__ == "__main__":
    main()
