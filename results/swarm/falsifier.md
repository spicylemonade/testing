# Falsifier Memo

Generated: 2026-03-12

Scope: adversarial review of the candidate directions in `results/swarm/hypothesis_bridge.md` and `results/swarm/hypothesis_negative_space.md`, with emphasis on the easiest failure modes, strongest rehash accusations, missing controls, benchmark traps, and literature branches that would invalidate weak claims.

Budget discipline: no new directions are proposed here except minimal pivots needed to explain why the current ones would otherwise fail.

## Executive Triage

- Already near-dead as a headline novelty claim: oscillator-based interleaving for multiphase converters.
- Highest "metaphor laundering" risk: reaction-diffusion gate-bias mesh, converter-ringing reservoir, exceptional-point gate-loop probe.
- Highest "peripheral overhead erases the effect" risk: ferroionic lock-in observer, electrocaloric tile driver.
- Highest "good microscopy, weak circuit thesis" risk: phased strain-wave mesh.

## 1. Reaction-Diffusion Gate-Bias Mesh for Self-Equalizing Wide-Bandgap Arrays

- Easiest rehash accusation: this is active gate control and electrothermal current balancing with a Turing-pattern story layered on top.
- Weak claim collapses if:
  - the advantage disappears once compared against strong active-balancing baselines instead of fixed gate resistors;
  - the mesh needs per-device observables or tuning effort comparable to an explicit controller;
  - the result only holds for threshold mismatch, not for package inductance spread, Miller coupling, dead-time skew, and thermal asymmetry.
  - the claimed gain is mostly in static current equalization, where layout and temperature-coefficient effects already help, rather than in the harder dynamic current-sharing regime during switching.
- Missing controls:
  - fixed gate resistor;
  - passive dynamic current balancing;
  - per-device active gate driver or local analog current-balancing loop;
  - same-complexity local coupling network without reaction-diffusion framing;
  - equal switching-loss and EMI conditions across all baselines.
- Benchmark traps:
  - double-pulse-only evidence that does not survive PWM operation or repeated thermal cycling;
  - electrothermal SPICE models that expose hidden junction states the real circuit cannot sense;
  - IR thermography used as if it were calibrated junction-temperature truth;
  - claiming current-sharing improvement without loss, stability, false-turn-on, and EMI penalties.
- Literature branches likely to sink weak novelty:
  - active gate drivers for current balancing of parallel GaN and SiC devices;
  - passive dynamic current balancing for parallel SiC MOSFETs;
  - electrothermal balancing and junction-temperature-aware gate-drive work for parallel WBG devices.
- Weaponized papers or search terms:
  - `Advanced Gate Drive Unit to Achieve Junction Temperature Monitoring and Dynamic Current Balancing for Parallel-Connected GaN Transistors`
  - `Active Gate Driver for Current Balancing of Parallel-Connected SiC MOSFETs`
  - `electrothermal balancing parallel GaN HEMT`
- Minimal pivot that might survive: only claim novelty if strictly local analog couplings, with no explicit per-device current sensing, still beat strong active-balancing baselines under realistic parasitic and thermal spread.

## 2. Converter Ringing as a Physical Reservoir for Self-Sensing Stability and Aging

- Easiest rehash accusation: this is ordinary transient-feature extraction or system identification with `reservoir computing` used as branding.
- Weak claim collapses if:
  - a raw-waveform linear model, PCA/PLS pipeline, or small neural regressor matches the claimed performance;
  - training and test data share the same compact-model assumptions, parasitic distributions, or board layout fingerprints;
  - the result depends on one monotonic drift variable that conventional ringing-frequency or overshoot features already capture.
  - multiple parasitic changes produce nearly the same ring-down once temperature, probe placement, and fixture spread are included, making the inverse problem under-identified.
- Missing controls:
  - scalar handcrafted features such as overshoot, dominant ringing frequency, damping ratio, and pulse-width features;
  - raw transient plus linear readout;
  - raw transient plus small CNN or MLP with identical sampling bandwidth and latency;
  - explicit train/test splits across operating point, temperature, aging state, and board instance.
- Benchmark traps:
  - leakage between simulation and test distributions;
  - unrealistic 10-50 ns acquisition windows that assume lab-grade probes and ADCs not available in deployment;
  - claiming `physical reservoir` value while the real computation sits in preprocessing, alignment, denoising, or calibration;
  - comparing only against weak scalar baselines rather than other full-waveform regressors.
- Literature branches likely to sink weak novelty:
  - condition monitoring of power modules from electrical transients and thermo-sensitive parameters;
  - ESR and parasitic estimation in buck converters using ANN, ML, or waveform fitting;
  - physical reservoir-computing hardware papers where the novelty already lies in exploiting native nonlinear dynamics.
- Weaponized papers or search terms:
  - `Machine-Learning-Based Condition Monitoring of Power Electronic Modules in Modern Electric Drives`
  - `Artificial Neural Networks Based Capacitor Equivalent Series Resistance Estimation in Buck Converters`
  - `transient voltage waveform condition prediction power device`
- Minimal pivot that might survive: show that the reservoir framing materially improves cross-condition generalization or calibration burden, not just in-distribution regression error.

## 3. Exceptional-Point Gate-Loop Probe for Wide-Bandgap Package Health Sensing

- Easiest rehash accusation: this is exceptional-point sensor hype inserted into a gate loop where a conventional resonator, ring oscillator, or TSEP monitor is simpler and more robust.
- Weak claim collapses if:
  - the claimed gain is only a slope or eigenvalue-splitting effect, not absolute resolution under realistic noise and drift;
  - exceptional-point tuning needs active compensation, negative resistance, or repeated recalibration that is not counted in the budget;
  - the probe perturbs switching loss, EMI, or gate-loop stability more than the claimed sensing benefit justifies.
  - the sensor advantage vanishes once the readout is evaluated by end-to-end estimation error rather than normalized sensitivity plots.
- Missing controls:
  - matched single-resonator sensor with identical Q, power, and area;
  - operation away from the exceptional point;
  - ring-oscillator or impedance-probe baseline in the same gate/package environment;
  - standard health monitors based on `Vds,on`, threshold shift, gate plateau, or thermo-sensitive electrical parameters.
- Benchmark traps:
  - normalized sensitivity plots with no absolute uncertainty floor;
  - calibrated benchtop perturbations that do not reflect real package aging, charge trapping, or power-cycling drift;
  - temperature and parasitic changes treated as separable when the sensor may conflate them;
  - ignoring the difficulty of staying tuned to the exceptional point over time.
- Literature branches likely to sink weak novelty:
  - critiques showing no fundamental sensitivity advantage once noise is treated properly;
  - electronic exceptional-point sensor demonstrations in resonator networks;
  - package-health and junction-temperature monitoring for GaN and SiC modules using conventional electrical observables.
- Weaponized papers or search terms:
  - `Fundamental Sensitivity Limit of Exceptional Point Sensors`
  - `Exceptional points and the response of open systems`
  - `GaN package parasitic health monitoring ring oscillator`
- Minimal pivot that might survive: only claim novelty if the exceptional-point probe still wins after equalizing noise, tuning overhead, and switching perturbation against a matched conventional resonant sensor.

## 4. Oscillator-Based Interleaving for Parallel or Multiphase Converters

- Easiest rehash accusation: decentralized oscillator-based synchronization in converters is already a known branch, so a generic `firefly`, `quorum`, or `pulse-coupled` controller is old news.
- Weak claim collapses if:
  - the target is stable interleaving rather than a sharply different spectral objective;
  - the method is compared only against centralized PWM or open-loop phase staggering, not against prior decentralized interleaving work.
- Missing controls:
  - distributed phase-management baselines;
  - coupled-oscillator interleaving baselines;
  - EMI-spectrum comparisons, not just phase-lock plots.
- Benchmark traps:
  - showing synchronization without showing why synchronization quality matters more than converter loss, transient response, or EMI;
  - avoiding load-transient or component-spread conditions where decentralized schemes usually get tested.
- Literature branches likely to sink weak novelty:
  - decentralized interleaving of parallel-connected buck converters;
  - distributed phase-management schemes for interleaved buck converters;
  - pulse-coupled or oscillator-synchronization converter control.
- Weaponized papers or search terms:
  - `Decentralized Interleaving of Parallel-connected Buck Converters`
  - `A Distributed Phase Management Scheme for Interleaved Buck Converters`
  - `oscillator synchronization interleaved buck converter`
- Minimal pivot that might survive: only a narrow spectral-control claim, such as deliberate cluster synchrony for EMI shaping under load changes, has any remaining novelty margin.

## 5. Dual-Band Lock-In Observer for Ferroionic Cells

- Easiest rehash accusation: this is inline impedance spectroscopy or operando admittance probing for a memristive/ferroelectric cell, with a control wrapper added afterward.
- Weak claim collapses if:
  - a single-frequency probe or a simple relaxation-time heuristic works nearly as well;
  - the compact model makes the hidden ionic state unrealistically observable;
  - endurance gains come mostly from gentler write schedules rather than from genuine hidden-state estimation.
  - two-frequency admittance signatures are not unique once temperature, oxidation, contact resistance, thickness spread, and partial electrochemical switching are allowed to vary.
- Missing controls:
  - conductance-only verify-and-write;
  - single-frequency probe;
  - open-loop cooldown or recovery heuristics;
  - equal-energy slower-write baseline;
  - full accounting of area, latency, and energy in the lock-in front end and estimator.
- Benchmark traps:
  - counting only cell energy while hiding probe and compute overhead in the periphery;
  - using post-write relaxation measurements that are easier than true in-situ observation;
  - ignoring read disturb, line resistance, device variability, and array throughput penalties;
  - claiming `observer` value without proving that the inferred hidden state is identifiable across temperature and device age.
  - assuming the probe is non-perturbative even though extra excitation can itself move ions or alter fatigue.
- Literature branches likely to sink weak novelty:
  - ferroionic and van der Waals ferroelectric fatigue papers where ionic dynamics already dominate the device story;
  - operando impedance or admittance characterization of resistive-switching devices;
  - refreshable memristor work that already exploits ferro-ionic phase coexistence.
- Weaponized papers or search terms:
  - `Unconventional polarization fatigue in van der Waals layered ferroelectric ionic conductor CuInP2S6`
  - `Transition from ferroelectric polarization reversal to electrochemical resistive switching due to ion migration`
  - `Dynamic allocation of ferro-ionic phase for refreshable memristor and embodied synaptic learning`
- Minimal pivot that might survive: only claim novelty if dual-band sensing improves endurance or analog-update linearity per total write energy and per array throughput, not just per isolated device cycle.

## 6. Resonant Charge-Sharing Electrocaloric Tile Driver

- Easiest rehash accusation: electrical energy recovery in electrocaloric cycles is already known, and tile-to-tile charge shuttling is just a more complicated driver whose overhead may erase the gain.
- Weak claim collapses if:
  - the system-level COP gain vanishes once routing parasitics, switch loss, dielectric loss, and controller overhead are included;
  - a simpler rail-driven energy-recovery driver plus a hotspot scheduler does almost as well;
  - the result only holds for one tile or one benign frequency point.
  - the electrothermal dynamics remain so slow that elaborate shuttling and scheduling add switching overhead without changing the useful cooling-control envelope.
- Missing controls:
  - optimized rail-to-tile energy-recovery baseline;
  - fixed scheduling baseline with identical thermal workload;
  - total electrical plus thermal accounting at array scale;
  - sensitivity to tile mismatch, thermal cross-coupling, and interconnect parasitics.
- Benchmark traps:
  - quoting recycled electrical energy instead of end-to-end cooling benefit;
  - evaluating single-tile hardware while claiming array-level routing value;
  - assuming ideal nonlinear capacitors with no hysteresis or leakage penalty;
  - ignoring the bandwidth limit imposed by thermal time constants and driver resonances.
- Literature branches likely to sink weak novelty:
  - electrocaloric energy-recovery cycles;
  - integrated electrocaloric actuation and cooling drivers;
  - array-level switched-capacitor or resonant charge-routing work in adjacent actuator domains.
- Weaponized papers or search terms:
  - `High efficient electrocaloric cooling cycles enabled by electrical energy recovery`
  - `Integrated solid-state cooling by electrocaloric and electrostatic actuation at frequencies up to 25 Hz`
  - `electrocaloric energy recovery driver array`
- Minimal pivot that might survive: only claim novelty if array-scale charge shuttling changes the thermal control envelope after realistic driver loss, not if it merely recovers charge in a prettier schematic.

## 7. Phased Strain-Wave Mesh for Topological Ferroelectric Control

- Easiest rehash accusation: mechanical and flexoelectric writing of topological ferroelectric textures already exists; the proposed contribution is just a more elaborate actuator stack without proof of practical addressability.
- Weak claim collapses if:
  - selectivity disappears once neighboring actuators, resonance spread, clamps, and package mechanics are modeled;
  - microscopy is required to close the loop, leaving no credible circuit-level readout path;
  - direct electrical writing or static strain patterning achieves the same state changes with less complexity.
  - actuator-to-actuator phase or resonance spread destroys coherent wave steering before the mesh reaches a meaningful array size.
- Missing controls:
  - direct electrical-write baseline;
  - static strain-pattern baseline;
  - array addressing with neighbor cross-talk, not single-spot demonstrations;
  - correlation between electrical readout and direct domain/topology imaging.
- Benchmark traps:
  - inferring topological state from resistance alone;
  - treating one-shot creation as if it proved programmable transport, merge, or erase operations;
  - ignoring actuator aging, resonance drift, and mechanical boundary conditions;
  - claiming lower write stress without quantifying the actuator power and complexity needed to generate the strain field.
- Literature branches likely to sink weak novelty:
  - dynamic mechanical generation of topological ferroelectric structures;
  - low-force mechanical domain switching and polarity reversal;
  - scalable flexoelectric engineering of polar skyrmion bubble arrays;
  - broader strain-mediated ferroelectric domain-control and acoustic-wave domain-motion literature.
- Weaponized papers or search terms:
  - `Dynamic mechanical generation of topological ferroelectric structures in oxide superlattices`
  - `Low-force pulse tip-induced ferroelectric domain switching and mechanical polarity reversal`
  - `Scalable and controllable flexoelectric engineering of van der Waals polar skyrmion bubble arrays`
- Minimal pivot that might survive: only claim novelty if phased strain provides a qualitatively unique transport or locality advantage that direct electrical control and static flexoelectric patterning cannot match.

## Cross-Cutting Invalidators

- Weak baselines: any claim that only beats `fixed`, `open-loop`, or `single-feature` baselines is not publishable as a novelty argument.
- Hidden observability: if the simulation exposes internal states or perfectly labeled degradation variables that hardware cannot access, the claim is inflated by construction.
- Peripheral accounting failure: if sensing, calibration, actuation, or compute energy is not counted, especially for ferroionic and electrocaloric ideas, the headline result is probably fictitious.
- In-distribution benchmarking: if train and test data share the same compact model, board, or perturbation family, the apparent intelligence may just be template matching.
- Proxy confusion: if resistance, overshoot, or a microscopy image is used as a loose proxy for the claimed hidden state without a validated mapping, the claim is under-identified.
- Scaling dodge: if the effect is only shown in a single device, a single tile, or a single paired resonator, the array-level thesis remains unproven.

## Literature Branches That Should Be Exhausted Before Any Novelty Claim

- Active and passive current balancing for parallel GaN and SiC power devices.
- Decentralized interleaving and distributed phase management in multiphase converters.
- Condition monitoring of power modules from switching transients, raw waveform ML, and thermo-sensitive electrical parameters.
- Exceptional-point sensing critiques that analyze noise and resolution, not just eigenvalue splitting.
- Operando impedance and admittance probing of ferroelectric, memristive, and ferroionic devices.
- Electrocaloric energy-recovery drivers and system-level COP accounting.
- Mechanical, flexoelectric, and acoustic-wave control of ferroelectric domains and topological textures.

## Bottom Line

- The easiest ideas to accuse of rehashing prior art are the oscillator-interleaving concept, the reaction-diffusion gate mesh, and the converter-ringing reservoir.
- The easiest ideas to kill with honest accounting are the ferroionic observer and electrocaloric tile driver because the periphery can dominate the claimed gain.
- The easiest idea to make look scientifically impressive but circuit-irrelevant is the phased strain-wave mesh unless it proves electrical addressability without leaning on microscopy.
