# Phase 6 Boundary Controller

## Equal-Expressivity H2 Search

- Family: `asym_a`.
- Word alphabet: `['S', 'D', 'P']` with identity symmetry quotient.
- Total exact controller programs checked: `75276`.
- Forcing controller programs: `48`.
- Best controller word: `SDP`.
- Best controller certificate: `13/7 m=10 r=3 n=8 t=1`.
- Direct certificate solver matches controller frontier: `True`.

## H3 UNSAT Core

- Controller search: unsat by row-quotient obstruction before enumeration.
- Matched unrestricted direct H3 hit rate: `0.0`.
- Core statement: In the passive-middle H=3 lift, every middle-row contribution lies in Z*c at its vertex, so no nonzero anti-diagonal singleton can appear on the middle row.
- Stronger-than-one-seed note: This obstruction allows arbitrary boundary seeds and arbitrary width inside the passive-middle family, unlike the old one-seed argument.

## Decision

- Exact H=2 controller search finds the same 13/7 frontier as direct certificate search under equal expressivity, so boundary programming buys no solver lift. The only surviving contribution is the stronger H=3 row-quotient UNSAT core.
