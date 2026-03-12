# Variant 01: RC-Ranked Packet Gate

- Role: preferred champion variant
- Source inference:
  - inject a small scout packet and rank branches by recovery slope and settling time
- Minimum-energy accumulation:
  - allow only the winning branch to feed the shared startup reservoir until one clean handoff packet exists
- Handoff gating:
  - release the main arbiter when `n_store` crosses the handoff threshold without a separate token chain
- Dependency list:
  - `netlists/shared/source_pair_models.inc`
  - `netlists/shared/startup_cells.inc`
  - scout packet capacitor
  - recovery timing capacitor
  - branch-isolation switch
  - handoff threshold gate
- Predicted failure mode:
  - under ultra-slow ramps or weak packets, the recovery signatures collapse together and the ranking overhead exceeds the saved back-drive loss
