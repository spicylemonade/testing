# Hypothesis Bridge Memo

Generated: 2026-03-12
Role: `hypothesis_scout`

Screening note:
- I did not reuse the current `H1_multisource_cold_start` packet-scout family.
- I also avoided generic "better adaptive MPPT," generic cryogenic reference, and generic harsh-environment compensation pitches. Each candidate only survives as a cross-domain bridge with a concrete kill rule.

## 1. Spread-Spectrum Admittance Probe for Self-Powered Harvest Interfaces

- **Title:** Spread-Spectrum Admittance Probe for Self-Powered Harvest Interfaces
- **Closest prior art:** `H3_dynamic_source_impedance` in `results/swarm/hypotheses.json`; *A Variable Impedance and Voltage Converter for Efficiently Harvesting Energy from Time-Varying Power Sources with Varying Internal Resistance* (2025); *Adaptable interface conditioning circuit for power harvesting from triboelectric nanogenerator* (2019); *Impedance spectroscopy analysis of thermoelectric modules under actual energy harvesting operating conditions and a small temperature difference* (2024).
- **Why it is different:** The reserve harvester lane is still too close to "estimate source resistance and retune." This bridge only survives if it imports spread-spectrum impedance identification from battery and grid diagnostics into a self-powered analog front end: the same switched-cap packets used for extraction are coded as a short PRBS-like micro-probe, and a charge-domain demodulator estimates incremental admittance plus relaxation time without a digital supervisor. That is narrower than generic adaptive MPPT and farther from the repo's one-shot source-ranking ideas.
- **Falsifiable prediction:** Under sources whose internal resistance or charge-delivery slope moves with motion, contact state, or bias history, a coded micro-probe front end should improve net delivered energy or sensor uptime by at least `10%` versus strong hysteretic and single-pulse-probe baselines under equal probe-energy accounting. Kill it if probe overhead or source collapse erases that margin.
- **Required experiments:**
  1. Build an ngspice behavioral source family with time-varying `R_th`, `C_eq`, and relaxation dynamics for triboelectric, thermoelectric, and electrochemical sources.
  2. Implement four controllers: fixed-threshold loading, low-overhead hysteretic loading, single-pulse probing, and the coded-probe admittance estimator.
  3. Sweep source-memory strength, motion/ramp trajectories, and probe budgets; report net delivered energy, source-collapse rate, estimator error, retune overhead, and sensor uptime.
  4. Rerun the separator cases with Monte Carlo mismatch and injected noise, then publish a no-free-lunch accounting table that charges every probe packet, latch event, and retune action.

## 2. Sequential-Evidence Charge Comparator for Sub-10 K Support Blocks

- **Title:** Sequential-Evidence Charge Comparator for Sub-10 K Support Blocks
- **Closest prior art:** `H2_cryo_support_blocks` in `results/swarm/hypotheses.json`; *Design and analysis of a high-speed low-power comparator with regeneration enhancement and through current suppression techniques from 4 K to 300 K in 65-nm Cryo-CMOS* (2023); *Cryo-CMOS Voltage References for the Ultrawide Temperature Range From 300 K Down to 4.2 K* (2024); *Analysis of Low-Frequency Noise in 40-nm CMOS at Cryogenic Temperatures* (2023).
- **Why it is different:** The local cryogenic lane becomes derivative if it turns into "another low-power cryo reference." This bridge only stays alive if it imports sequential evidence accumulation from low-power decision circuits: instead of trusting one absolute threshold under cryogenic `V_th` shift and RTS/`1/f` noise, the block performs many tiny charge comparisons and decides on accumulated evidence or resolution order. That converts model uncertainty into a packet-count or latency observable and makes graceful monotonic degradation the headline property.
- **Falsifiable prediction:** Across widened `4 K` to `10 K` threshold-shift, mismatch, and low-frequency-noise corners, an evidence-accumulating comparator/reference pair should preserve output ordering and cut false decisions by at least `2x` relative to a one-shot dynamic comparator or static cryogenic reference at the same average energy per decision. Kill it if leakage, delay, or calibration burden dominates before monotonicity improves.
- **Required experiments:**
  1. Use a validated cryogenic PDK if available; otherwise create a documented surrogate deck with widened `V_th`, mismatch, kink, and low-frequency-noise assumptions from `300 K` down to `4 K`.
  2. Implement three macro-blocks in ngspice: static cryogenic reference plus comparator, standard one-shot dynamic latch, and the sequential-evidence charge comparator.
  3. Inject fitted RTS and low-frequency-noise sources, then run Monte Carlo and transient-noise sweeps on slow ramps and small differential steps.
  4. Report false-trip rate, monotonicity violations, delay-energy product, and calibration burden. Kill the lane if it only works under gentle corners or impractically long averaging windows.

## 3. Pilot-Tone Channel Estimation for Greater-Than-225 C Sensor Interfaces

- **Title:** Pilot-Tone Channel Estimation for Greater-Than-225 C Sensor Interfaces
- **Closest prior art:** *A High-Temperature Piezoresistive Pressure Sensor with an Integrated Signal-Conditioning Circuit* (2016); *A Dual-Frequency Parasitic-Insensitive Switched-Capacitor Sensor Interface for Capacitive Sensors* (2016); *A Remote Temperature-Sensing Chip Adaptive to Parasitic and Discrete Transistors with an Inaccuracy of +/-0.25 C from -55 C to 125 C* (2025).
- **Why it is different:** High-temperature sensor interfaces usually compensate temperature drift or package a custom AFE, while parasitic-aware remote-sensor work mostly targets milder environments. This bridge imports communication-style channel estimation into the harsh-temperature readout path: the sensor, leadframe, leakage paths, and contacts are treated as a slowly varying channel, and two orthogonal low-amplitude pilot tones or coded calibration packets are injected through the same interface. A synchronous analog demodulator estimates lead resistance, leakage conductance, and contact drift separately from the measurand, which is more specific than generic recalibration and more circuit-grounded than an ML compensation story.
- **Falsifiable prediction:** Across repeated thermal cycles above `225 C` with drifting leakage and interconnect parasitics, a pilot-tone-compensated interface should cut full-scale error by at least `2x` relative to static temperature compensation, single-tone calibration, or periodic two-point recalibration while adding less than `10%` readout-energy overhead. Kill it if a single calibration tone or passive compensation matches the result once realistic leakage and contact drift are included.
- **Required experiments:**
  1. Create a SPICE sensor-interface deck with temperature-dependent leakage, lead resistance, contact aging drift, and parasitic capacitance.
  2. Compare no compensation, static temperature compensation, single-tone calibration, and dual-pilot estimation under the same excitation budget.
  3. Report recovered sensor error, calibration latency, energy overhead, and robustness after repeated thermal-cycle stress and parasitic drift.
  4. If the lane survives simulation, move to a bench emulation with programmable parasitics, heated interconnect, and drift injection to verify identifiability outside the compact model.
