# Baselines

- `fixed_startup_path/`
  - Fixed startup path baseline with no source-aware scouting.
  - Netlist: `fixed_startup_path/fixed_startup_path.cir`
- `nonaware_multi_input_startup/`
  - Multi-input startup/arbitration baseline without source-aware ranking.
  - Netlist: `nonaware_multi_input_startup/nonaware_multi_input_startup.cir`

Both baselines share the same source model, startup pump abstraction, node names, current-sense elements, and control-energy monitor path.
