# Gap Map

## Selection Filter

- The required repo artifacts were read first and were mostly bootstrap noise, not a usable EE frontier.
- Broad Semantic Scholar re-querying was intentionally avoided after the seed watchlist proved off-target.
- The final shortlist only keeps gaps that satisfy all three tests:
  - a concrete circuit-level failure mode exists
  - the operating regime is important but still under-served
  - a plausible ngspice-first falsification path exists

## Explicitly Deprioritized

- Generic analog-AI, memristor, or CIM work without a sharply defined nonideality.
- Generic GaN switching-loss or EMI tuning without an unusual operating regime.
- Generic wearable-sensor demos that mainly change packaging or form factor.
- Steady-state MPPT papers that never stress startup, source collapse, or intermittency.

## Ranked Gaps

### 1. Source-Adaptive Cold Start For Weak Multi-Source Harvesters Under Ultra-Slow Ramps

- **Why this looks genuinely under-served:** Cold start is still hard even for one weak source. The problem gets materially worse when multiple harvesters with different source impedances, polarities, and ramp rates share the same startup path, but much of the literature still evaluates one benign source at a time.
- **Concrete failure mode:** The startup path chatters around UVLO, one source back-drives another, or the oscillator/control loop burns the entire startup budget before enough charge accumulates to hand over to the main converter.
- **Evidence anchors:**
  - *Review of Fully Integrated Startup Techniques for Thermoelectric Energy Harvesting Systems* (2023) highlights that fully integrated cold start below threshold remains difficult and that oscillator-based startup can be fragile to noise and variation.
  - *Power Management for Multi-Source Energy Harvesting Systems: A Review* (2024) identifies cold start, source intermittency, threshold mismatch, isolation, and low-overhead control as unresolved multi-source bottlenecks.
  - *Fully Autonomous Self-Starting Interface Circuit for Piezoelectric Energy Harvesting from Multi-Source Inputs* (2024) shows that even recent silicon still has to work around startup/arbitration complexity when several sources are present.
- **Why it beats crowded decoys:** This is a hard power-interface problem, not another steady-state harvester-efficiency paper.
- **Plausible circuit thesis:** An asynchronous startup front end that first infers source impedance and polarity, then chooses a kick-start mode and only enables arbitration/anti-backflow devices after a minimum energy packet is available.
- **Fast falsifier:** If a tighter prior-art pass finds a fully integrated result that already cold-starts across mixed 20-300 mV sources with source-aware arbitration and no external helper supply, this gap should be downgraded.

### 2. Dynamic-Source-Impedance-Aware Harvest Interfaces For Self-Powered Sensors

- **Why this looks genuinely under-served:** Real harvesters are often not fixed Thevenin sources. Triboelectric, piezoelectric, electrochemical, and self-powered sensing sources can change their internal impedance with motion, contact state, bias history, or the measurand itself. Many control laws still assume the source model is stationary enough for fixed-threshold MPPT or one-time tuning.
- **Concrete failure mode:** The interface tunes itself to the wrong load line, collapses the source during acquisition, or mistakes source dynamics for usable energy and wastes charge on reconfiguration.
- **Evidence anchors:**
  - *A Variable Impedance and Voltage Converter for Efficiently Harvesting Energy from Time-Varying Power Sources with Varying Internal Resistance* (2025) directly targets the fact that internal resistance can move enough to break conventional fixed-interface assumptions.
  - *Mismatch Between Dynamic Input Impedance and Load Impedance Causes Poor Real-Time Power Supply from Triboelectric Nanogenerator* (2025) shows that dynamic impedance mismatch can materially degrade delivered power.
  - *Effect of Energy Management Circuitry on Optimum Source Configuration in Vibration Energy Harvesting Systems* (2022) shows that the interface itself shifts the source optimum, which means source and converter cannot be treated as separable.
- **Why it beats crowded decoys:** The missing piece is not “better MPPT” in the abstract; it is source-model uncertainty coupled back into the circuit.
- **Plausible circuit thesis:** A source-probing interface that periodically estimates incremental source resistance or charge-delivery slope using charge-domain probes, then retunes the rectifier/converter loading without a digital supervisor.
- **Fast falsifier:** If the adaptive scheme cannot beat a simple hysteretic controller once realistic probing overhead is included, this direction should be killed.

### 3. Cryogenic Low-Frequency-Noise-Resilient Bias, Reference, Comparator, And ADC Support Blocks Below 10 K

- **Why this looks genuinely under-served:** Cryogenic CMOS is now visible because of quantum-control systems, but the literature still skews toward RF, oscillators, and system narratives. The boring precision primitives that make a stack deployable at 4 K to sub-10 K are much thinner, especially under low-power constraints.
- **Concrete failure mode:** Threshold-voltage shift, kink effects, altered mismatch, and defect-dominated low-frequency noise break room-temperature bias assumptions, so a reference or comparator that looks fine in nominal cryo corners either loses monotonicity, burns too much power, or becomes uncalibratable.
- **Evidence anchors:**
  - *A Review of Cryogenic CMOS Electronics for Quantum Computing* (2022) explicitly calls out analog signal processing and data conversion as less explored than RF front ends and oscillators.
  - *Toward Cryogenic CMOS Electronics for Quantum Computing: An Updated Review of Cryogenic CMOS Technology for Quantum Computing* (2024) emphasizes that device behavior changes strongly below 10 K and that compact-model coverage remains limited.
  - *Analysis of Low-Frequency Noise in 40-nm CMOS at Cryogenic Temperatures* (2023) reports cryogenic noise behavior that is not a trivial room-temperature extrapolation.
  - *Design of 1 V sub-1 µW 5 ppm/C Voltage References in a 65nm Cryogenic CMOS PDK* (2024) is evidence that useful references are only starting to become practical and still occupy a narrow design space.
- **Why it beats crowded decoys:** This is less fashionable than “cryo-CMOS for quantum computing” as a slogan, but it is closer to a real circuit moat.
- **Plausible circuit thesis:** A PTAT-light charge-domain reference/comparator path that avoids classical bandgap assumptions, uses capacitor ratios plus sparse trimming, and explicitly targets graceful degradation under cryogenic model uncertainty.
- **Fast falsifier:** If the concept only works under unrealistically gentle cryogenic corners and collapses when low-frequency noise and mismatch are widened, it is not a serious gap.

### 4. Restart-Safe Radiation-Tolerant Low-Power Regulators And Bias Loops For Cold-Redundant Or Intermittent Space Hardware

- **Why this looks genuinely under-served:** Radiation-hard literature is deep in digital logic and robust power conversion at a high level, but low-power analog restart behavior under both total ionizing dose and single-event disturbance is still patchier, especially for cold-redundant or intermittently awakened hardware.
- **Concrete failure mode:** Dose-induced degradation in the auxiliary supply or startup chain shrinks margin until the converter or LDO fails to restart, while a single-event transient on a lightly biased internal node creates a long dropout or a stuck bias state.
- **Evidence anchors:**
  - *Radiation-Induced Degradation on the Cold-Redundant DC/DC Converter for Space Application* (2025) reports startup-margin loss because the auxiliary supply degrades under total ionizing dose.
  - *SET-Hardened LDO for Single Event Mitigation* (2021) notes that single-event transients in on-chip LDOs are less studied than digital SEU effects and proposes explicit hardening.
  - *Single-Event Transient Effects in On-Chip Low-Dropout Voltage Regulators Designed for Space Applications* (2020) shows that regulator internal nodes can be a real analog weak point under radiation.
- **Why it beats crowded decoys:** The novelty is not generic rad-hard design. The narrow gap is self-recovery and restart correctness in low-power analog power loops.
- **Plausible circuit thesis:** A dual-path startup and bias network with transient-aware clamps, state scrubbing, and a self-checking restart sequencer that guarantees recovery after TID-shifted bias points or SET hits.
- **Fast falsifier:** If the proposed hardening only improves transient rejection in one nominal operating point but still fails after realistic dose-shifted startup margins, drop it.

### 5. Greater-Than-225 C Sensor Interfaces With In-Situ Co-Drift And Parasitic Compensation

- **Why this looks genuinely under-served:** High-temperature sensing is real, but much of the literature still emphasizes sensors, packaging, or discrete signal conditioning. Integrated readout that jointly compensates sensor drift, circuit drift, leakage, and package/lead parasitics across repeated thermal cycles is much thinner.
- **Concrete failure mode:** The sensor element remains functional, but the readout chain loses accuracy because leakage rises, offsets drift, contacts age, and long interconnects or package parasitics swamp the signal.
- **Evidence anchors:**
  - *Electronic Sensors and Circuits for High-Temperature Dynamic Pressure Monitoring: A Review* argues that high-temperature electronics remain a system bottleneck rather than a solved support problem.
  - *High-Temperature Stable Silicon-on-Insulator Precision Low-Power Analog Front-End Amplifier for SiC MEMS Accelerometer* demonstrates that even useful front ends in this area are specialized and sparse.
  - *Compensation Techniques for Improving Accuracy in Sensor Circuits Over Wide Temperature Range* (2025) confirms that active compensation is still a live problem, not a closed chapter.
  - *Silicon Carbide MEMS Sensors for Harsh Radiation Extreme Environments* (2024) adds that contacts, leakage, isolation, and packaging stability remain practical blockers in harsh settings.
- **Why it beats crowded decoys:** This is not “another harsh-environment sensor.” The gap is the co-designed interface circuit that keeps the sensor useful after the environment attacks everything around it.
- **Plausible circuit thesis:** A leakage-balanced chopper or incremental sigma-delta readout with on-line parasitic identification and periodic thermal-cycle recalibration, built to survive above 225 C without relying on remote room-temperature conditioning.
- **Fast falsifier:** If a larger reservoir, remote conditioner, or periodic factory recalibration solves the same problem with less complexity, this direction loses force.

## Priority For Follow-On Work

1. **Gap 1** if the near-term goal is a publishable ngspice-first PMIC concept with a clean falsification path.
2. **Gap 3** if access to cryogenic models or collaborators exists and the goal is a higher-moat analog block.
3. **Gap 2** if the program wants a more novel harvester problem than plain MPPT.
4. **Gap 4** if the target program has a space-electronics angle and can support radiation validation later.
5. **Gap 5** if the team can tolerate a longer device-and-packaging tail.

## Best Immediate Bet

- **Most simulation-ready:** Gap 1.
- **Most likely under-served but still important:** Gap 3.
- **Most surprising without drifting into hype:** Gap 2.
