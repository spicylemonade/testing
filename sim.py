#!/usr/bin/env python3
"""Main entry point for the gravity simulation."""

import argparse
import numpy as np
from src.bodies import Body, System
from src.forces.brute_force import compute_forces
from src.integrators.leapfrog import leapfrog_step
from src.metrics import total_energy


def main():
    parser = argparse.ArgumentParser(description="Minimal N-body gravity simulation")
    parser.add_argument("--n", type=int, default=3, help="Number of bodies")
    parser.add_argument("--dt", type=float, default=0.01, help="Timestep")
    parser.add_argument("--steps", type=int, default=1000, help="Number of steps")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    np.random.seed(args.seed)

    bodies = []
    for i in range(args.n):
        mass = np.random.uniform(0.5, 2.0)
        pos = np.random.uniform(-5, 5, size=2)
        vel = np.random.uniform(-0.5, 0.5, size=2)
        bodies.append(Body(mass=mass, position=pos, velocity=vel))

    system = System(bodies=bodies)
    E0 = total_energy(system)
    print(f"Initial energy: {E0:.6f}")

    for step in range(args.steps):
        acc = compute_forces(system)
        leapfrog_step(system, acc, args.dt)
        if (step + 1) % 100 == 0:
            E = total_energy(system)
            dE = abs((E - E0) / E0)
            print(f"Step {step+1}: E={E:.6f}, |dE/E0|={dE:.2e}")

    Ef = total_energy(system)
    print(f"Final energy: {Ef:.6f}, drift: {abs((Ef-E0)/E0):.2e}")


if __name__ == "__main__":
    main()
