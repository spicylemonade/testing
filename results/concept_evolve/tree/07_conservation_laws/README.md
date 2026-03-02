# CONSERVATION_SENTINEL

Runtime monitors for total energy, linear momentum, and angular momentum. Not just diagnostics -- they are the primary correctness signal. A simulation that doesn't conserve energy is wrong, period.

## Mathematical Formalization

E = sum(0.5*m_i*|v_i|^2) + sum_{i<j}(-G*m_i*m_j/sqrt(|r_ij|^2+eps^2)).  P = sum(m_i*v_i).  L = sum(m_i * r_i x v_i).  For symplectic integrators: |dE/E| bounded, |dP| = 0 to machine precision, |dL| = 0 to machine precision.

## Analogical Connections

- Conservation metrics <-> loss curves in training (the signal that tells you if learning is working)
- Energy conservation <-> checksum verification (detects corruption in the computation)
- Noether's theorem <-> symmetry-based invariant testing (every symmetry implies a conserved quantity)

## Implementation Hypothesis

Functions: kinetic_energy(vel, mass), potential_energy(pos, mass, eps), total_momentum(vel, mass), angular_momentum(pos, vel, mass). Called once per frame, results logged. ~30 lines.

## Experiment Seed

Deliberately break symplecticity (use Euler) and show that the conservation sentinel detects it within 10 orbits. Then switch to leapfrog and show the sentinel stays green indefinitely.
