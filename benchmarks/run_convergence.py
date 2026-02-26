"""Convergence study: energy conservation vs timestep size.

Run leapfrog and Yoshida on a 2-body Kepler orbit with
dt = 0.1, 0.01, 0.001, 0.0001. Plot max |dE/E0| vs dt on log-log scale.
Measure slope to confirm convergence orders (2nd for leapfrog, 4th for Yoshida).
"""

import json
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.initial_conditions import kepler_elliptical
from src.forces.brute_force_vec import compute_forces_vectorized
from src.integrators.leapfrog import leapfrog_step
from src.integrators.yoshida import yoshida_step
from src.metrics import total_energy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def run_convergence(integrator_name, dt, n_orbits=10):
    """Run simulation and return max energy drift."""
    T = 2 * np.pi  # orbital period for a=1, G=1, M=1
    total_time = n_orbits * T
    n_steps = int(total_time / dt)

    system = kepler_elliptical(e=0.5, epsilon=1e-10)
    force_func = compute_forces_vectorized
    acc = force_func(system)
    E0 = total_energy(system)

    max_drift = 0.0
    for _ in range(n_steps):
        if integrator_name == "leapfrog":
            acc = leapfrog_step(system, acc, dt, force_func=force_func)
        elif integrator_name == "yoshida":
            acc = yoshida_step(system, acc, dt, force_func=force_func)
        E = total_energy(system)
        drift = abs((E - E0) / E0)
        if drift > max_drift:
            max_drift = drift

    return max_drift


def main():
    dts = [0.1, 0.01, 0.001, 0.0001]
    integrators = ["leapfrog", "yoshida"]
    results = {}

    for name in integrators:
        print(f"=== {name} ===")
        results[name] = {"dt": [], "max_drift": []}
        for dt in dts:
            print(f"  dt={dt}...", end=" ", flush=True)
            drift = run_convergence(name, dt)
            results[name]["dt"].append(dt)
            results[name]["max_drift"].append(float(drift))
            print(f"max |dE/E0| = {drift:.2e}")

    # Compute slopes (convergence order)
    slopes = {}
    for name in integrators:
        log_dt = np.log10(results[name]["dt"])
        log_drift = np.log10(results[name]["max_drift"])
        # Linear fit to get slope
        coeffs = np.polyfit(log_dt, log_drift, 1)
        slopes[name] = round(coeffs[0], 2)
        print(f"\n{name} convergence order (slope): {slopes[name]:.2f}")

    # Save results
    output = {
        "convergence_data": results,
        "slopes": slopes,
        "expected_orders": {"leapfrog": 2, "yoshida": 4},
        "n_orbits": 10,
    }
    out_path = os.path.join("results", "convergence_study.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")

    # Plot
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = {"leapfrog": "#2ecc71", "yoshida": "#3498db"}
    labels = {"leapfrog": f"Leapfrog (slope={slopes['leapfrog']:.2f})",
              "yoshida": f"Yoshida (slope={slopes['yoshida']:.2f})"}

    for name in integrators:
        ax.loglog(results[name]["dt"], results[name]["max_drift"],
                  "o-", color=colors[name], label=labels[name], linewidth=2, markersize=8)

    # Reference slopes
    dt_ref = np.array([1e-4, 1e-1])
    ax.loglog(dt_ref, 1e-6 * (dt_ref / 1e-4) ** 2, "--", color="#2ecc71", alpha=0.3,
              label=r"$\propto \Delta t^2$")
    ax.loglog(dt_ref, 1e-12 * (dt_ref / 1e-4) ** 4, "--", color="#3498db", alpha=0.3,
              label=r"$\propto \Delta t^4$")

    ax.set_xlabel(r"Timestep $\Delta t$")
    ax.set_ylabel(r"max $|\Delta E / E_0|$")
    ax.set_title("Convergence Study: Energy Conservation vs Timestep")
    ax.legend(fontsize=10)

    fig.tight_layout()
    fig.savefig("figures/convergence_study.png", dpi=150, bbox_inches="tight")
    fig.savefig("figures/convergence_study.pdf", bbox_inches="tight")
    plt.close(fig)
    print("Saved figures/convergence_study.png and .pdf")


if __name__ == "__main__":
    main()
