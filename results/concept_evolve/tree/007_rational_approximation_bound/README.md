# Rational Approximation Bound

## Topic Context

The Collatz function alternates between multiplying by 3/2 (odd steps) and dividing by 2 (even steps). The net growth rate after k steps with f odd steps is approximately 3^f / 2^k. Since ln(3)/ln(2) ≈ 1.585, a trajectory descends when the fraction of odd steps is below 1/ln(3/2) ≈ 63.1%.

The rational approximation 485/306 provides a rigorous upper bound for ln(3)/ln(2) that converts the descent check into exact integer arithmetic: 485*f <= 306*k. This is a convergent of the continued fraction expansion of ln(3)/ln(2).

## Cross-Domain Bridges

- **Diophantine approximation**: Rational bounds for irrational quantities
- **Fixed-point DSP**: Replace floating-point with integer ratios for determinism
- **Dynamical systems**: Lyapunov exponent bounds for stability analysis

## Implementation Backlog

- [ ] Implement integer descent check: 485*f <= 306*k
- [ ] Compute continued fraction convergents of ln(3)/ln(2)
- [ ] Test next convergent (306191/193205) for improved pruning
- [ ] Analyze minimum n threshold (99781) sensitivity to approximation quality
- [ ] Integrate into bitvector dip_B computation
