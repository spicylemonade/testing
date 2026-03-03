# Subagent Phase-1 Synthesis

- Synthesis subagent type: `general`
- Task id: `ses_34e54ef32ffe0o0gvSx2zZpSzn`

## Citation chains (>=5)

1. Barnes & Hut (1986) -> Hernquist (1987) -> Dehnen (2000) -> Dehnen (2002)
2. Wisdom & Holman (1991) -> Saha & Tremaine (1992) -> Chambers (1999) -> Rein & Tamayo (2015)
3. Ahmad & Cohen (1973) -> Makino (1991) -> Makino & Aarseth (1992) -> Aarseth (2003)
4. Hockney & Eastwood (1981) -> Couchman (1991) -> Bagla (2002) -> Springel (2005)
5. Greengard & Rokhlin (1987) -> Carrier et al. (1988) -> Dehnen (2014)
6. Athanassoula et al. (2000) -> Dehnen (2001) -> Barnes (2012)

## Transferable techniques (>=3)

1. **KDK leapfrog as default integrator:** preserves long-horizon structure at low complexity.
2. **Barnes-Hut opening-angle control (`theta`):** supports tunable speed-accuracy tradeoffs for N growth.
3. **Softening calibration sweeps:** quantify force bias/variance and avoid unstable close-encounter artifacts.
4. **Invariant regression tests:** use energy and angular-momentum drift as automated gates in every run.

## Priority implications for downstream rubric items

- `item_006`-`item_008`: start with deterministic direct-force baseline and invariant metrics.
- `item_011`-`item_013`: compare symplectic and scalable-force upgrades against baseline with matched seeds.
- `item_016`-`item_019`: preregister softening/timestep sweeps and report confidence intervals for drift and runtime effects.
