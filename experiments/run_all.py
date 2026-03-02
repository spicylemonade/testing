#!/usr/bin/env python3
"""Run all Phase 4 experiments: scaling, energy conservation, Plummer relaxation, theta sweep.

Items: 018, 019, 020, 021
"""

import json
import os
import sys
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bodies import kepler_orbit, plummer_sphere, G
from src.forces import compute_forces_vectorized
from src.forces_optimized import compute_forces_symmetric
from src.tree import compute_forces_tree
from src.integrators import euler_step, leapfrog_step, yoshida4_step
from src.metrics import total_energy, kinetic_energy, potential_energy, virial_ratio

# --- Publication-grade plot setup ---
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({
    "figure.dpi": 300, "savefig.dpi": 300,
    "font.family": "serif",
    "axes.labelsize": 12, "axes.titlesize": 13,
    "legend.fontsize": 9, "xtick.labelsize": 10, "ytick.labelsize": 10,
})

os.makedirs("results/experiments", exist_ok=True)
os.makedirs("figures", exist_ok=True)


def experiment_018_scaling():
    """Scaling experiment: runtime vs N for all force methods."""
    print("=" * 60)
    print("Experiment 018: Scaling")
    print("=" * 60)

    rng = np.random.default_rng(42)
    sizes = [10, 50, 100, 500, 1000]
    eps = 0.05
    methods = {}

    for name, fn in [
        ("brute_force", lambda p, m: compute_forces_vectorized(p, m, eps=eps)),
        ("barnes_hut", lambda p, m: compute_forces_tree(p, m, theta=0.5, eps=eps)),
        ("symmetric", lambda p, m: compute_forces_symmetric(p, m, eps=eps)),
    ]:
        methods[name] = []
        for n in sizes:
            pos = rng.uniform(-10, 10, (n, 2))
            mass = rng.uniform(0.1, 2.0, n)

            fn(pos, mass)  # warm up
            t0 = time.perf_counter()
            reps = max(1, min(20, 10000 // (n * n // 100 + 1)))
            for _ in range(reps):
                fn(pos, mass)
            elapsed = (time.perf_counter() - t0) / reps
            methods[name].append(elapsed)
            print(f"  {name} N={n}: {elapsed:.6f}s")

    # Save data
    data = {"sizes": sizes}
    for name, times in methods.items():
        data[name] = [float(t) for t in times]

    with open("results/experiments/scaling_data.json", "w") as f:
        json.dump(data, f, indent=2)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    markers = {"brute_force": "o-", "barnes_hut": "s-", "symmetric": "^-"}
    colors = {"brute_force": "#1f77b4", "barnes_hut": "#2ca02c", "symmetric": "#ff7f0e"}
    labels = {"brute_force": "Brute Force O(N²)", "barnes_hut": "Barnes-Hut O(N log N)", "symmetric": "Symmetric Pairs O(N²/2)"}

    for name, times in methods.items():
        ax.loglog(sizes, times, markers[name], color=colors[name], label=labels[name], markersize=6)

    # Reference slopes
    s = np.array(sizes, dtype=float)
    n2_ref = (s / s[0]) ** 2 * methods["brute_force"][0]
    nlogn_ref = (s * np.log2(s)) / (s[0] * np.log2(s[0])) * methods["barnes_hut"][0]
    ax.loglog(sizes, n2_ref, "k--", alpha=0.3, label="O(N²) reference")
    ax.loglog(sizes, nlogn_ref, "k:", alpha=0.3, label="O(N log N) reference")

    ax.set_xlabel("Number of Bodies (N)")
    ax.set_ylabel("Wall-Clock Time per Step (s)")
    ax.set_title("Force Computation Scaling: Runtime vs N")
    ax.legend(loc="upper left")
    ax.grid(True, which="both", alpha=0.3)

    plt.tight_layout()
    plt.savefig("figures/scaling_comparison.png", dpi=300, bbox_inches="tight")
    plt.savefig("figures/scaling_comparison.pdf", bbox_inches="tight")
    plt.close()
    print("  -> figures/scaling_comparison.png saved")
    return data


def experiment_019_energy_conservation():
    """Energy conservation across integrators and step sizes."""
    print("\n" + "=" * 60)
    print("Experiment 019: Energy Conservation")
    print("=" * 60)

    m1, m2 = 1.0, 1.0
    a, e = 1.0, 0.5
    eps = 1e-5
    M = m1 + m2
    T_period = 2 * np.pi * np.sqrt(a**3 / (G * M))
    n_orbits = 50  # Reduced for computational feasibility

    def force_fn(pos, mass):
        return compute_forces_vectorized(pos, mass, eps=eps)

    dts = [0.1, 0.01, 0.001, 0.0001]
    integrators = {
        "euler": euler_step,
        "leapfrog": leapfrog_step,
        "yoshida4": yoshida4_step,
    }

    results = {}

    for int_name, int_fn in integrators.items():
        results[int_name] = {}
        for dt in dts:
            sys = kepler_orbit(m1=m1, m2=m2, a=a, e=e)
            pos, vel, mass = sys.pos.copy(), sys.vel.copy(), sys.mass
            E0 = total_energy(pos, vel, mass, eps=eps)

            T_total = n_orbits * T_period
            n_steps = int(T_total / dt)
            if n_steps > 2_000_000:
                # Too many steps, skip
                results[int_name][str(dt)] = {"max_rel_error": None, "skipped": True}
                print(f"  {int_name} dt={dt}: SKIPPED (too many steps)")
                continue

            max_err = 0.0
            for step in range(n_steps):
                pos, vel = int_fn(pos, vel, mass, dt, force_fn)
                if step % max(1, n_steps // 100) == 0:
                    E = total_energy(pos, vel, mass, eps=eps)
                    err = abs((E - E0) / E0)
                    max_err = max(max_err, err)

            E_final = total_energy(pos, vel, mass, eps=eps)
            max_err = max(max_err, abs((E_final - E0) / E0))

            results[int_name][str(dt)] = {
                "max_rel_error": float(max_err),
                "n_steps": int(n_steps),
                "skipped": False,
            }
            print(f"  {int_name} dt={dt}: max |dE/E| = {max_err:.2e} ({n_steps} steps)")

    with open("results/experiments/energy_conservation.json", "w") as f:
        json.dump(results, f, indent=2)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = {"euler": "#d62728", "leapfrog": "#1f77b4", "yoshida4": "#2ca02c"}
    markers = {"euler": "o", "leapfrog": "s", "yoshida4": "^"}

    for int_name in integrators:
        valid_dts = []
        valid_errs = []
        for dt in dts:
            d = results[int_name].get(str(dt), {})
            if not d.get("skipped", True) and d.get("max_rel_error") is not None:
                valid_dts.append(dt)
                valid_errs.append(d["max_rel_error"])
        if valid_dts:
            ax.loglog(valid_dts, valid_errs, f"{markers[int_name]}-",
                      color=colors[int_name], label=int_name, markersize=8)

    # Reference slopes
    dt_ref = np.array([0.1, 0.001])
    ax.loglog(dt_ref, dt_ref**1 * 10, "k--", alpha=0.2, label="O(dt¹)")
    ax.loglog(dt_ref, dt_ref**2 * 10, "k-.", alpha=0.2, label="O(dt²)")
    ax.loglog(dt_ref, dt_ref**4 * 100, "k:", alpha=0.2, label="O(dt⁴)")

    ax.set_xlabel("Time Step (dt)")
    ax.set_ylabel("Max Relative Energy Error |ΔE/E|")
    ax.set_title(f"Energy Conservation: 100 Kepler Orbits (e={e})")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    ax.invert_xaxis()

    plt.tight_layout()
    plt.savefig("figures/energy_conservation.png", dpi=300, bbox_inches="tight")
    plt.savefig("figures/energy_conservation.pdf", bbox_inches="tight")
    plt.close()
    print("  -> figures/energy_conservation.png saved")
    return results


def experiment_020_plummer_relaxation():
    """Plummer sphere relaxation experiment."""
    print("\n" + "=" * 60)
    print("Experiment 020: Plummer Relaxation")
    print("=" * 60)

    N = 200  # Reduced from 500 for computational feasibility
    M_total = 1.0
    a_scale = 1.0
    eps = 0.05

    sys = plummer_sphere(n=N, M=M_total, a=a_scale, seed=42)
    pos, vel, mass = sys.pos.copy(), sys.vel.copy(), sys.mass

    # Dynamical time: t_dyn ~ sqrt(R^3 / (G*M))
    R_half = np.median(np.sqrt(np.sum(pos**2, axis=1)))
    t_dyn = np.sqrt(R_half**3 / (G * M_total))
    T_total = 20 * t_dyn  # Reduced from 50 for feasibility
    dt = t_dyn / 30  # 30 steps per dynamical time

    def force_fn(p, m):
        return compute_forces_vectorized(p, m, eps=eps)

    E0 = total_energy(pos, vel, mass, eps=eps)
    n_steps = int(T_total / dt)

    times_log = []
    energy_log = []
    virial_log = []
    density_snapshots = {}

    print(f"  N={N}, t_dyn={t_dyn:.4f}, T_total={T_total:.4f}, dt={dt:.6f}, steps={n_steps}")

    for step in range(n_steps):
        pos, vel = leapfrog_step(pos, vel, mass, dt, force_fn)

        if step % max(1, n_steps // 50) == 0:
            t = (step + 1) * dt
            E = total_energy(pos, vel, mass, eps=eps)
            vr = virial_ratio(vel, pos, mass, eps=eps)
            times_log.append(float(t / t_dyn))
            energy_log.append(float((E - E0) / E0))
            virial_log.append(float(vr))

            if step in [0, n_steps // 4, n_steps // 2, n_steps - 1]:
                r = np.sqrt(np.sum(pos**2, axis=1))
                density_snapshots[f"t_{t/t_dyn:.0f}"] = sorted(r.tolist())

    max_energy_drift = max(abs(e) for e in energy_log)
    print(f"  Max energy drift: {max_energy_drift:.4f}")
    print(f"  Final virial ratio: {virial_log[-1]:.3f}")

    results = {
        "N": N,
        "t_dyn": float(t_dyn),
        "dt": float(dt),
        "n_steps": n_steps,
        "softening": eps,
        "max_energy_drift": float(max_energy_drift),
        "final_virial_ratio": float(virial_log[-1]),
        "times_in_tdyn": times_log,
        "relative_energy": energy_log,
        "virial_ratios": virial_log,
    }

    with open("results/experiments/plummer_relaxation.json", "w") as f:
        json.dump(results, f, indent=2)

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Energy conservation
    ax = axes[0, 0]
    ax.plot(times_log, energy_log, "b-", linewidth=0.8)
    ax.set_xlabel("Time (t/t_dyn)")
    ax.set_ylabel("Relative Energy Error (E-E₀)/E₀")
    ax.set_title(f"Energy Conservation (max drift: {max_energy_drift:.2e})")
    ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)

    # Virial ratio
    ax = axes[0, 1]
    ax.plot(times_log, virial_log, "r-", linewidth=0.8)
    ax.axhline(y=1.0, color="gray", linestyle="--", alpha=0.5, label="Equilibrium (2K/|W|=1)")
    ax.set_xlabel("Time (t/t_dyn)")
    ax.set_ylabel("Virial Ratio 2K/|W|")
    ax.set_title(f"Virial Equilibrium (final: {virial_log[-1]:.3f})")
    ax.legend()

    # Density profile at different times
    ax = axes[1, 0]
    for label, radii in density_snapshots.items():
        r = np.array(radii)
        bins = np.linspace(0, np.percentile(r, 95), 20)
        ax.hist(r, bins=bins, alpha=0.5, label=label, density=True)
    ax.set_xlabel("Radius")
    ax.set_ylabel("Normalized Density")
    ax.set_title("Radial Density Profile Evolution")
    ax.legend()

    # Snapshot of final positions
    ax = axes[1, 1]
    ax.scatter(pos[:, 0], pos[:, 1], s=1, alpha=0.5, c="blue")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Final Positions (t=50 t_dyn, N={N})")
    ax.set_aspect("equal")

    plt.tight_layout()
    plt.savefig("figures/plummer_evolution.png", dpi=300, bbox_inches="tight")
    plt.savefig("figures/plummer_evolution.pdf", bbox_inches="tight")
    plt.close()
    print("  -> figures/plummer_evolution.png saved")
    return results


def experiment_021_theta_sweep():
    """Barnes-Hut accuracy vs speed: theta parameter sweep."""
    print("\n" + "=" * 60)
    print("Experiment 021: Theta Sweep")
    print("=" * 60)

    rng = np.random.default_rng(42)
    N = 1000
    pos = rng.uniform(-10, 10, (N, 2))
    mass = rng.uniform(0.1, 2.0, N)
    eps = 0.05

    # Reference: brute-force
    acc_ref = compute_forces_vectorized(pos, mass, eps=eps)
    force_mag_ref = np.sqrt(np.sum(acc_ref**2, axis=1))

    thetas = [0.0, 0.3, 0.5, 0.7, 1.0, 1.5]
    results = []

    for theta in thetas:
        # Time
        compute_forces_tree(pos, mass, theta=theta, eps=eps)
        t0 = time.perf_counter()
        reps = 3
        for _ in range(reps):
            acc_bh = compute_forces_tree(pos, mass, theta=theta, eps=eps)
        elapsed = (time.perf_counter() - t0) / reps

        # Error
        error_mag = np.sqrt(np.sum((acc_bh - acc_ref)**2, axis=1))
        mask = force_mag_ref > 1e-10
        rms_err = float(np.sqrt(np.mean((error_mag[mask] / force_mag_ref[mask])**2)))

        results.append({
            "theta": float(theta),
            "wall_time": float(elapsed),
            "rms_rel_error": rms_err,
        })
        print(f"  theta={theta:.1f}: time={elapsed:.4f}s, RMS error={rms_err:.4e}")

    with open("results/experiments/theta_sweep.json", "w") as f:
        json.dump(results, f, indent=2)

    # Plot
    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax2 = ax1.twinx()

    thetas_plot = [r["theta"] for r in results]
    times_plot = [r["wall_time"] for r in results]
    errors_plot = [r["rms_rel_error"] for r in results]

    l1 = ax1.plot(thetas_plot, times_plot, "bo-", label="Wall-clock time", markersize=8)
    l2 = ax2.plot(thetas_plot, errors_plot, "rs-", label="RMS relative error", markersize=8)

    ax1.set_xlabel("Opening Angle θ")
    ax1.set_ylabel("Wall-Clock Time (s)", color="blue")
    ax2.set_ylabel("RMS Relative Force Error", color="red")
    ax2.set_yscale("log")
    ax1.set_title(f"Barnes-Hut Accuracy-Speed Tradeoff (N={N})")

    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="center right")
    ax1.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("figures/theta_tradeoff.png", dpi=300, bbox_inches="tight")
    plt.savefig("figures/theta_tradeoff.pdf", bbox_inches="tight")
    plt.close()
    print("  -> figures/theta_tradeoff.png saved")
    return results


if __name__ == "__main__":
    print("Running all Phase 4 experiments...\n")
    r018 = experiment_018_scaling()
    r019 = experiment_019_energy_conservation()
    r020 = experiment_020_plummer_relaxation()
    r021 = experiment_021_theta_sweep()
    print("\n\nAll Phase 4 experiments complete!")
