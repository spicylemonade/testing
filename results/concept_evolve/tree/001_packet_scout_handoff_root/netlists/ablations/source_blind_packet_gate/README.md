# Source-Blind Packet Gate

- Role: source-awareness ablation for the packet-scout family
- Mechanism:
  - keeps the same routed packet scaffold and shared startup reservoir as the champion deck
  - removes ranking by splitting packet drive evenly across the two routed source branches
- Dependency list:
  - `netlists/shared/source_pair_models.inc`
  - `netlists/shared/startup_cells.inc`
  - `netlists/shared/packet_scout_blocks.inc`
- Predicted failure mode:
  - under impedance asymmetry or mixed polarity, the equal split wastes startup effort on the wrong branch and loses handoff time without reducing control overhead enough to compensate
- Netlist:
  - `source_blind_packet_gate.cir`
