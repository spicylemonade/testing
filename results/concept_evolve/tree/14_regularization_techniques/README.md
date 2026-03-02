# ORBITAL_STATE_CLASSIFIER

Classify orbital states in real time: bound elliptical (E<0), parabolic escape (E=0), hyperbolic flyby (E>0). Detect binary formation, three-body ejection, and resonance capture as discrete state transitions in a continuous dynamical system.

## Mathematical Formalization

For pair (i,j): E_ij = 0.5*mu*v_rel^2 - G*m_i*m_j/r_ij, where mu = m_i*m_j/(m_i+m_j).  E_ij < 0 => bound.  Eccentricity: e = sqrt(1 + 2*E_ij*L_ij^2/(G^2*m_i^2*m_j^2*mu)).  State transitions: bound->unbound = ejection event.

## Analogical Connections

- Orbital classification <-> anomaly detection (continuous signal crossing a threshold)
- Binary capture <-> phase transition (discrete change from continuous dynamics)
- Three-body ejection <-> bankruptcy in economic models (one agent expelled by collective dynamics)
- Resonance <-> mode-locking in coupled oscillators

## Implementation Hypothesis

Per-pair energy computation at each step. Maintain a state matrix S[i,j] in {unbound, bound, resonant}. Emit events on state transitions. ~50 lines.

## Experiment Seed

Run 10 random 3-body simulations. Log all state transitions. Verify that ejection events correlate with energy transfer: the ejected body gains KE equal to the PE lost by the remaining binary.
