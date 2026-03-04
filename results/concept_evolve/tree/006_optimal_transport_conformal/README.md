# Optimal Transport and Conformal Mapping

## Topic Context

Optimal transport (OT) theory provides powerful tools for comparing probability measures and understanding the geometry of measure spaces. The connection between OT and conformal mapping is through the Jacobian: for a conformal map f, the pushforward measure has density |f'|^2 with respect to area.

## Key Idea

For a univalent f: D → C with f'(0) = 1, the image f(D) must contain a disk of radius B_f. The optimal transport cost from the pushforward of Lebesgue on D to the uniform measure on D(0,B_f) provides a lower bound on the "effort" needed to cover a disk of that radius. If this cost exceeds a threshold, then B_f cannot be too large — giving an upper bound on B_u.

Conversely, if the OT cost is small for all univalent f, then f(D) is "close" to a disk in transport distance, which could give lower bounds.

## Implementation Backlog

1. **[P0]** Implement discrete OT for conformal image measures
2. **[P1]** Compute W_2 for Koebe function and rotations
3. **[P2]** Map out the (W_2, B_f) plane for random univalent functions
4. **[P3]** Derive analytical transport inequality
