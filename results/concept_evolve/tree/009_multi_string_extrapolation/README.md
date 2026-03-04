# Multi-String Extrapolation for Chvatal-Sankoff Estimation

## Topic Context

The generalized Chvatal-Sankoff constant gamma_{k,d} is the normalized expected LCS of d
strings over alphabet size k. Li, Ren, and Wen (2025) proved the first asymptotically tight
result: gamma_{2,d} = 1/2 + Theta(1/sqrt(d)).

This means the d-dependence of the constant has a known functional form. By measuring
gamma_{2,d} for d = 2, 3, 4, ..., 20 (using the automaton method or Monte Carlo) and
fitting the asymptotic expansion, we can extrapolate back to d=2 with quantified error.

## Why This Helps

The key advantage is that gamma_{2,d} for d >= 5 can be estimated more precisely (the
constant is smaller, closer to 1/2, so finite-n effects are weaker). These precise estimates
at large d constrain the functional form, which in turn constrains gamma_{2,2}.

## Implementation Backlog

1. [ ] Compile all known bounds for gamma_{2,d}, d=2..20
2. [ ] For d=3..8, run Monte Carlo simulations with n=5000 to get precise estimates
3. [ ] Fit 3-parameter model: gamma_{2,d} = 0.5 + c1/sqrt(d) + c2/d + c3/d^{3/2}
4. [ ] Compute confidence interval for gamma_{2,2} from the fit
5. [ ] Cross-validate: leave out d=3, predict it, check error
6. [ ] If prediction is within [0.7927, 0.8263], report as narrowed estimate
