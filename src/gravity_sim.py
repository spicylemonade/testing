"""
Minimal N-body Gravity Simulator
=================================
Core simulation engine supporting multiple integrators and force methods.

Usage:
    python src/gravity_sim.py --N 50 --steps 1000 --integrator euler --output results/baseline/
    python src/gravity_sim.py --N 50 --steps 1000 --integrator verlet --output results/verlet/
    python src/gravity_sim.py --N 50 --steps 1000 --integrator leapfrog --output results/leapfrog/

References:
    - Verlet (1967), Phys. Rev. 159, 98
    - Barnes & Hut (1986), Nature 324, 446
    - Gladman, Duncan, Candy (1991), Celest. Mech. 52, 221
"""

import argparse
import json
import os
import time

import numpy as np


# ---------------------------------------------------------------------------
# Physics engine
# ---------------------------------------------------------------------------

def compute_forces_direct(positions, masses, G=1.0, softening=0.01):
    """
    O(N^2) direct pairwise gravitational force computation.

    Parameters
    ----------
    positions : ndarray, shape (N, 2)
        Body positions in 2D.
    masses : ndarray, shape (N,)
        Body masses.
    G : float
        Gravitational constant.
    softening : float
        Softening length to avoid singularities.

    Returns
    -------
    accelerations : ndarray, shape (N, 2)
        Gravitational acceleration on each body.
    """
    N = len(masses)
    accelerations = np.zeros_like(positions)
    for i in range(N):
        for j in range(i + 1, N):
            rij = positions[j] - positions[i]
            dist_sq = np.dot(rij, rij) + softening ** 2
            dist = np.sqrt(dist_sq)
            force_mag = G * masses[i] * masses[j] / dist_sq
            force_dir = rij / dist
            accelerations[i] += force_mag / masses[i] * force_dir
            accelerations[j] -= force_mag / masses[j] * force_dir
    return accelerations


def compute_forces_vectorized(positions, masses, G=1.0, softening=0.01):
    """
    Vectorized O(N^2) pairwise gravitational force computation using NumPy
    broadcasting. Significantly faster than the loop version for N > ~20.

    Parameters
    ----------
    positions : ndarray, shape (N, 2)
    masses : ndarray, shape (N,)
    G : float
    softening : float

    Returns
    -------
    accelerations : ndarray, shape (N, 2)
    """
    N = len(masses)
    # Pairwise displacement vectors: diff[i, j] = positions[j] - positions[i]
    diff = positions[np.newaxis, :, :] - positions[:, np.newaxis, :]  # (N, N, 2)
    dist_sq = np.sum(diff ** 2, axis=2) + softening ** 2  # (N, N)
    dist = np.sqrt(dist_sq)  # (N, N)

    # Force magnitude: G * m_j / dist^2, direction: diff / dist
    # acceleration[i] = sum_j G * m_j * diff[i,j] / dist[i,j]^3
    inv_dist_cube = 1.0 / (dist_sq * dist)  # (N, N)
    np.fill_diagonal(inv_dist_cube, 0.0)  # no self-interaction

    # acc_i = G * sum_j m_j * (r_j - r_i) / |r_j - r_i|^3
    ax = G * np.sum(diff[:, :, 0] * inv_dist_cube * masses[np.newaxis, :], axis=1)
    ay = G * np.sum(diff[:, :, 1] * inv_dist_cube * masses[np.newaxis, :], axis=1)
    return np.column_stack([ax, ay])


# ---------------------------------------------------------------------------
# Energy computation
# ---------------------------------------------------------------------------

def compute_kinetic_energy(velocities, masses):
    """Compute total kinetic energy: sum(0.5 * m * v^2)."""
    return 0.5 * np.sum(masses * np.sum(velocities ** 2, axis=1))


def compute_potential_energy(positions, masses, G=1.0, softening=0.01):
    """Compute total gravitational potential energy (softened)."""
    N = len(masses)
    pe = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            rij = positions[j] - positions[i]
            dist = np.sqrt(np.dot(rij, rij) + softening ** 2)
            pe -= G * masses[i] * masses[j] / dist
    return pe


def compute_potential_energy_vectorized(positions, masses, G=1.0, softening=0.01):
    """Vectorized gravitational potential energy computation."""
    diff = positions[np.newaxis, :, :] - positions[:, np.newaxis, :]
    dist_sq = np.sum(diff ** 2, axis=2) + softening ** 2
    dist = np.sqrt(dist_sq)
    np.fill_diagonal(dist, np.inf)  # exclude self-interaction
    # Upper triangle only (avoid double counting)
    pe_matrix = -G * masses[:, np.newaxis] * masses[np.newaxis, :] / dist
    return np.sum(np.triu(pe_matrix, k=1))


def compute_total_energy(positions, velocities, masses, G=1.0, softening=0.01):
    """Compute total energy (kinetic + potential)."""
    ke = compute_kinetic_energy(velocities, masses)
    pe = compute_potential_energy_vectorized(positions, masses, G, softening)
    return ke + pe, ke, pe


def compute_momentum(velocities, masses):
    """Compute total momentum vector."""
    return np.sum(masses[:, np.newaxis] * velocities, axis=0)


# ---------------------------------------------------------------------------
# Collision detection
# ---------------------------------------------------------------------------

def detect_collisions(positions, masses, velocities, softening=0.01,
                      mode="merge"):
    """
    Detect and handle collisions between bodies closer than softening radius.

    Parameters
    ----------
    positions, masses, velocities : current state arrays
    softening : collision distance threshold
    mode : 'merge' (inelastic) or 'bounce' (elastic)

    Returns
    -------
    positions, masses, velocities : updated arrays (possibly fewer bodies)
    collision_events : list of (body_i, body_j, mode) tuples
    """
    N = len(masses)
    collision_events = []
    merged = set()

    for i in range(N):
        if i in merged:
            continue
        for j in range(i + 1, N):
            if j in merged:
                continue
            rij = positions[j] - positions[i]
            dist = np.sqrt(np.dot(rij, rij))
            if dist < softening:
                collision_events.append((i, j, mode))
                if mode == "merge":
                    # Inelastic merge: conserve momentum
                    total_mass = masses[i] + masses[j]
                    positions[i] = (masses[i] * positions[i] + masses[j] * positions[j]) / total_mass
                    velocities[i] = (masses[i] * velocities[i] + masses[j] * velocities[j]) / total_mass
                    masses[i] = total_mass
                    merged.add(j)
                elif mode == "bounce":
                    # Elastic bounce: reverse relative velocity component
                    rij_norm = rij / (dist + 1e-30)
                    v_rel = velocities[j] - velocities[i]
                    v_rel_n = np.dot(v_rel, rij_norm)
                    if v_rel_n < 0:  # approaching
                        impulse = 2.0 * v_rel_n / (1.0 / masses[i] + 1.0 / masses[j])
                        velocities[i] += impulse / masses[i] * rij_norm
                        velocities[j] -= impulse / masses[j] * rij_norm

    if merged:
        keep = [i for i in range(N) if i not in merged]
        positions = positions[keep]
        velocities = velocities[keep]
        masses = masses[keep]

    return positions, masses, velocities, collision_events


# ---------------------------------------------------------------------------
# Integrators
# ---------------------------------------------------------------------------

def step_euler(positions, velocities, masses, dt, G=1.0, softening=0.01,
               force_func=None):
    """Forward Euler integration step."""
    if force_func is None:
        force_func = compute_forces_vectorized
    acc = force_func(positions, masses, G, softening)
    positions_new = positions + velocities * dt
    velocities_new = velocities + acc * dt
    return positions_new, velocities_new


def step_verlet(positions, velocities, masses, dt, G=1.0, softening=0.01,
                force_func=None, acc_prev=None):
    """
    Velocity Verlet (Stormer-Verlet) integration step.

    Returns (positions_new, velocities_new, acc_new) so the caller can
    reuse acc_new as acc_prev for the next step.
    """
    if force_func is None:
        force_func = compute_forces_vectorized
    if acc_prev is None:
        acc_prev = force_func(positions, masses, G, softening)

    # Position update
    positions_new = positions + velocities * dt + 0.5 * acc_prev * dt ** 2
    # New acceleration
    acc_new = force_func(positions_new, masses, G, softening)
    # Velocity update
    velocities_new = velocities + 0.5 * (acc_prev + acc_new) * dt

    return positions_new, velocities_new, acc_new


def step_leapfrog(positions, velocities, masses, dt, G=1.0, softening=0.01,
                  force_func=None, acc_prev=None):
    """
    Leapfrog (kick-drift-kick) symplectic integration step.

    Returns (positions_new, velocities_new, acc_new).
    """
    if force_func is None:
        force_func = compute_forces_vectorized
    if acc_prev is None:
        acc_prev = force_func(positions, masses, G, softening)

    # Kick (half step)
    velocities_half = velocities + 0.5 * acc_prev * dt
    # Drift (full step)
    positions_new = positions + velocities_half * dt
    # Compute new accelerations
    acc_new = force_func(positions_new, masses, G, softening)
    # Kick (half step)
    velocities_new = velocities_half + 0.5 * acc_new * dt

    return positions_new, velocities_new, acc_new


# ---------------------------------------------------------------------------
# Initial conditions
# ---------------------------------------------------------------------------

def random_initial_conditions(N, seed=42, box_size=10.0, max_vel=0.5,
                              mass_range=(0.5, 2.0)):
    """Generate random initial conditions for N bodies in 2D."""
    rng = np.random.RandomState(seed)
    positions = (rng.rand(N, 2) - 0.5) * box_size
    velocities = (rng.rand(N, 2) - 0.5) * 2 * max_vel
    masses = rng.uniform(mass_range[0], mass_range[1], N)
    return positions, velocities, masses


def load_scenario(filepath):
    """Load initial conditions from a JSON scenario file."""
    with open(filepath, "r") as f:
        data = json.load(f)
    positions = np.array(data["positions"])
    velocities = np.array(data["velocities"])
    masses = np.array(data["masses"])
    params = data.get("params", {})
    return positions, velocities, masses, params


# ---------------------------------------------------------------------------
# Simulation runner
# ---------------------------------------------------------------------------

def run_simulation(positions, velocities, masses, n_steps=1000, dt=0.01,
                   integrator="euler", G=1.0, softening=0.01,
                   force_func=None, track_energy=True,
                   collisions=False, collision_mode="merge",
                   adaptive=False, adaptive_eta=0.01):
    """
    Run the N-body simulation.

    Parameters
    ----------
    positions, velocities, masses : initial state
    n_steps : number of timesteps
    dt : timestep size (or initial dt for adaptive)
    integrator : 'euler', 'verlet', or 'leapfrog'
    G : gravitational constant
    softening : softening length
    force_func : force computation function (default: vectorized direct)
    track_energy : whether to compute and store energy at each step
    collisions : whether to detect and handle collisions
    collision_mode : 'merge' or 'bounce'
    adaptive : whether to use adaptive timestepping
    adaptive_eta : accuracy parameter for adaptive timestep

    Returns
    -------
    results : dict with keys 'positions', 'velocities', 'energy', 'timing', etc.
    """
    if force_func is None:
        force_func = compute_forces_vectorized

    step_funcs = {
        "euler": step_euler,
        "verlet": step_verlet,
        "leapfrog": step_leapfrog,
    }
    if integrator not in step_funcs:
        raise ValueError(f"Unknown integrator: {integrator}")

    pos = positions.copy()
    vel = velocities.copy()
    mass = masses.copy()
    N_initial = len(mass)

    # Storage
    pos_history = [pos.copy()]
    vel_history = [vel.copy()]
    energy_log = []
    collision_log = []
    dt_log = [dt]
    timing = []

    # Initial energy
    if track_energy:
        te, ke, pe = compute_total_energy(pos, vel, mass, G, softening)
        energy_log.append({"step": 0, "total": te, "kinetic": ke, "potential": pe})

    # For Verlet/leapfrog, compute initial acceleration
    acc_prev = None
    if integrator in ("verlet", "leapfrog"):
        acc_prev = force_func(pos, mass, G, softening)

    for step in range(1, n_steps + 1):
        t0 = time.perf_counter()

        # Adaptive timestep
        current_dt = dt
        if adaptive:
            current_dt = compute_adaptive_dt(pos, vel, mass, G, softening,
                                             dt, adaptive_eta, force_func)
            dt_log.append(current_dt)

        # Integration step
        if integrator == "euler":
            pos, vel = step_euler(pos, vel, mass, current_dt, G, softening,
                                  force_func)
        elif integrator == "verlet":
            pos, vel, acc_prev = step_verlet(pos, vel, mass, current_dt, G,
                                             softening, force_func, acc_prev)
        elif integrator == "leapfrog":
            pos, vel, acc_prev = step_leapfrog(pos, vel, mass, current_dt, G,
                                               softening, force_func, acc_prev)

        # Collision detection
        if collisions:
            pos, mass, vel, events = detect_collisions(
                pos, mass, vel, softening, collision_mode)
            for ev in events:
                collision_log.append({
                    "step": step,
                    "body_i": int(ev[0]),
                    "body_j": int(ev[1]),
                    "type": ev[2],
                })
            # Reset acc_prev if bodies were removed
            if events and integrator in ("verlet", "leapfrog"):
                acc_prev = force_func(pos, mass, G, softening)

        t1 = time.perf_counter()
        timing.append(t1 - t0)

        pos_history.append(pos.copy())
        vel_history.append(vel.copy())

        if track_energy:
            te, ke, pe = compute_total_energy(pos, vel, mass, G, softening)
            energy_log.append({
                "step": step,
                "total": te,
                "kinetic": ke,
                "potential": pe,
            })

    return {
        "positions": pos_history,
        "velocities": vel_history,
        "energy": energy_log,
        "collisions": collision_log,
        "timing": timing,
        "dt_log": dt_log,
        "final_N": len(mass),
        "initial_N": N_initial,
        "masses_final": mass.tolist(),
        "integrator": integrator,
        "n_steps": n_steps,
        "dt": dt,
        "G": G,
        "softening": softening,
    }


def compute_adaptive_dt(positions, velocities, masses, G, softening, dt_base,
                        eta, force_func):
    """
    Compute adaptive timestep based on maximum acceleration.

    dt_adaptive = eta * sqrt(softening / max_acc)

    Clamped to [dt_base/10, dt_base*2] for stability.
    """
    acc = force_func(positions, masses, G, softening)
    max_acc = np.max(np.sqrt(np.sum(acc ** 2, axis=1)))
    if max_acc > 0:
        dt_adaptive = eta * np.sqrt(softening / max_acc)
    else:
        dt_adaptive = dt_base
    return np.clip(dt_adaptive, dt_base / 10.0, dt_base * 2.0)


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def save_results(results, output_dir):
    """Save simulation results to output directory."""
    os.makedirs(output_dir, exist_ok=True)

    # Save position data as numpy arrays
    # Handle variable-size arrays (from collisions reducing body count)
    try:
        pos_array = np.array([p for p in results["positions"]])
        np.save(os.path.join(output_dir, "positions.npy"), pos_array)
    except ValueError:
        # Inhomogeneous shapes due to merging — save as list of arrays
        import pickle
        with open(os.path.join(output_dir, "positions.pkl"), "wb") as f:
            pickle.dump(results["positions"], f)

    # Save energy log as CSV
    if results["energy"]:
        import csv
        energy_path = os.path.join(output_dir, "energy_drift.csv")
        with open(energy_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestep", "total_energy",
                                                    "kinetic_energy",
                                                    "potential_energy"])
            writer.writeheader()
            for e in results["energy"]:
                writer.writerow({
                    "timestep": e["step"],
                    "total_energy": e["total"],
                    "kinetic_energy": e["kinetic"],
                    "potential_energy": e["potential"],
                })

    # Save collision log
    if results["collisions"]:
        import csv
        collision_path = os.path.join(output_dir, "collision_log.csv")
        with open(collision_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestep", "body_i",
                                                    "body_j", "type"])
            writer.writeheader()
            for c in results["collisions"]:
                writer.writerow({
                    "timestep": c["step"],
                    "body_i": c["body_i"],
                    "body_j": c["body_j"],
                    "type": c["type"],
                })

    # Save metadata
    meta = {
        "integrator": results["integrator"],
        "n_steps": results["n_steps"],
        "dt": results["dt"],
        "G": results["G"],
        "softening": results["softening"],
        "initial_N": results["initial_N"],
        "final_N": results["final_N"],
        "mean_step_time_ms": float(np.mean(results["timing"])) * 1000
                             if results["timing"] else 0,
    }
    if results["energy"]:
        e0 = results["energy"][0]["total"]
        ef = results["energy"][-1]["total"]
        if abs(e0) > 1e-30:
            meta["energy_drift_pct"] = abs((ef - e0) / e0) * 100
        else:
            meta["energy_drift_pct"] = 0.0
    with open(os.path.join(output_dir, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Minimal N-body Gravity Simulator")
    parser.add_argument("--N", type=int, default=50, help="Number of bodies")
    parser.add_argument("--steps", type=int, default=1000, help="Number of timesteps")
    parser.add_argument("--dt", type=float, default=0.01, help="Timestep size")
    parser.add_argument("--integrator", type=str, default="euler",
                        choices=["euler", "verlet", "leapfrog"],
                        help="Integration method")
    parser.add_argument("--G", type=float, default=1.0, help="Gravitational constant")
    parser.add_argument("--softening", type=float, default=0.1,
                        help="Softening length")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=str, default="results/baseline/",
                        help="Output directory")
    parser.add_argument("--scenario", type=str, default=None,
                        help="Path to scenario JSON file")
    parser.add_argument("--collisions", action="store_true",
                        help="Enable collision detection")
    parser.add_argument("--collision-mode", type=str, default="merge",
                        choices=["merge", "bounce"])
    parser.add_argument("--adaptive", action="store_true",
                        help="Enable adaptive timestepping")
    parser.add_argument("--adaptive-eta", type=float, default=0.01,
                        help="Adaptive timestep accuracy parameter")

    args = parser.parse_args()

    # Initialize
    if args.scenario:
        positions, velocities, masses, params = load_scenario(args.scenario)
        # Override dt, G, softening from scenario if present
        args.dt = params.get("dt", args.dt)
        args.G = params.get("G", args.G)
        args.softening = params.get("softening", args.softening)
        args.steps = params.get("steps", args.steps)
    else:
        positions, velocities, masses = random_initial_conditions(
            args.N, seed=args.seed)

    print(f"Running simulation: N={len(masses)}, steps={args.steps}, "
          f"dt={args.dt}, integrator={args.integrator}")

    results = run_simulation(
        positions, velocities, masses,
        n_steps=args.steps, dt=args.dt,
        integrator=args.integrator,
        G=args.G, softening=args.softening,
        collisions=args.collisions,
        collision_mode=args.collision_mode,
        adaptive=args.adaptive,
        adaptive_eta=args.adaptive_eta,
    )

    save_results(results, args.output)
    print(f"Results saved to {args.output}")

    if results["energy"]:
        e0 = results["energy"][0]["total"]
        ef = results["energy"][-1]["total"]
        if abs(e0) > 1e-30:
            drift = abs((ef - e0) / e0) * 100
            print(f"Energy drift: {drift:.4f}%")

    if results["timing"]:
        mean_ms = np.mean(results["timing"]) * 1000
        print(f"Mean step time: {mean_ms:.2f} ms")


if __name__ == "__main__":
    main()
