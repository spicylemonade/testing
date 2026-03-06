# Problem Statement

## Default Hypothesis (H1)

- Champion hypothesis: `H1` audit-first deterministic reference kernel.
- Core claim: the contribution is a tiny Newtonian gravity simulator whose value comes from auditability - invariant tracking, timestep-halving convergence checks, and reproducibility hooks - rather than from flashy rendering or a new integrator.
- Target scope: deterministic Newtonian mutual-gravity simulation for 2-body, 3-body, and small-N direct-sum reference scenarios with matched, fixed-step update order.

## Backup Hypothesis (H2)

- Backup hypothesis: `H2` honest close-encounter minimal core.
- Activation rule: promote `H2` only if the audit-first wedge is already crowded or the determinism claim collapses under close-encounter stress.
- If activated, the publishable output narrows to failure-envelope disclosure and explicit close-pass policies rather than broad simulator capability claims.

## Held Hypothesis (H3)

- `H3` remains a useful guardrail, not the headline claim.
- Unit safety and scale sanity will be treated as supporting controls inside scenario authoring and reporting, not as the main research contribution.

## Research Wedge

- Build a deterministic Newtonian reference kernel first.
- Add audit surfaces that ordinary toy simulators omit: energy and angular-momentum drift, center-of-mass drift, round-trip reversibility diagnostics, timestep-halving convergence, and scenario-level benchmark metadata.
- Use close-encounter handling and reproducibility checks as falsifiers of the claim, not as optional polish.

## Explicit Non-Claims

- This project does not claim a new integrator family; baseline stepping will use well-known fixed-step symplectic updates plus carefully labeled audit or stabilization layers.
- This project does not claim a large-N engine, Barnes-Hut breakthrough, GPU/HPC contribution, or production astrophysics replacement.
- This project does not claim UI, rendering, browser delivery, or classroom friendliness as the research novelty.
- This project does not claim relativistic gravity, domain-specific solar modeling, borehole modeling, or black-hole trajectory novelty.

## Success Criteria

- Closed-form two-body controls are recovered within declared tolerances.
- Long-horizon invariant drift and timestep-halving behavior are measured rather than assumed.
- Matched scenarios agree with a trusted reference such as REBOUND within declared envelopes.
- The same scenario bundle can be replayed across at least two runtimes or numeric targets with documented tolerances and failure cases.
