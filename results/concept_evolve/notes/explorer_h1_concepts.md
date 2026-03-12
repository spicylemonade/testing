# Explorer H1 Concepts

Parent reconstruction after codex child-pass stream disconnect.

## impedance_ranked_packet_probe
- Key mechanism: Capacitive packet probe plus passive recovery-timing latch chooses the initial source path and delays multi-input arbitration until the reservoir can pay for it.
- Why it matters: Closest surviving concept to the H1 thesis because it adds cheap source awareness before full arbitration instead of claiming generic multi-source harvesting.
- Closest overlaps: Power management unit for multi-source energy harvesting in wearable electronics; Single- and multi-source battery-less power management circuits for piezoelectric energy harvesting systems; Configurable Hybrid Energy Synchronous Extraction Interface With Serial Stack Resonance for Multi-Source Energy Harvesting

## dual_path_helperless_startup
- Key mechanism: Self-referenced mode selection between two startup paths before the main PMU comes alive.
- Why it matters: Distinct from low-voltage single-source startup papers because the claim is about helper-free mode selection among heterogeneous weak sources.
- Closest overlaps: Fully Integrated Startup at 70 mV of Boost Converters for Thermoelectric Energy Harvesting; A CMOS Startup Circuit for Thermoelectric Energy Harvesting Systems; A Thermoelectric Energy Harvesting System Assisted by a Piezoelectric Transducer Achieving 10-MV Cold-Startup and 82.7% Peak Efficiency

## polarity_split_dual_bucket_bootstrap
- Key mechanism: Dual scout buckets plus cross-coupled merge gating delay shared-reservoir exposure until startup is safe.
- Why it matters: Targets the exact mixed-polarity startup regime that most recovered overlap papers do not benchmark explicitly.
- Closest overlaps: Self-Powered Collaborative Energy Harvesting Interface Circuit for Stacked Multiple Piezoelectric Elements; A self-powered multi-input OSECE interface circuit for multiple piezoelectric transducers; Configurable Hybrid Energy Synchronous Extraction Interface With Serial Stack Resonance for Multi-Source Energy Harvesting

## source_signature_charge_packet_startup
- Key mechanism: Local recovery signature gates packet transfer into the shared reservoir.
- Why it matters: More adaptive than ordinary time-division multiplexing, but closer to existing multi-input extraction papers than the top three concepts.
- Closest overlaps: Configurable Hybrid Energy Synchronous Extraction Interface With Serial Stack Resonance for Multi-Source Energy Harvesting; A self-powered multi-input OSECE interface circuit for multiple piezoelectric transducers

## anti_backdrive_latched_oring
- Key mechanism: Source-local latch delays and direction-locks OR-ing devices during startup.
- Why it matters: Important enabling block for H1, but too narrow to carry the full claim alone.
- Closest overlaps: Single- and multi-source battery-less power management circuits for piezoelectric energy harvesting systems; Self-Powered Collaborative Energy Harvesting Interface Circuit for Stacked Multiple Piezoelectric Elements

## uvlo_deglitched_token_handoff
- Key mechanism: Token accumulator measures sustained energy margin before handoff.
- Why it matters: High practical value for H1 experiments, but too incremental to headline by itself.
- Closest overlaps: A 220-mV Power-on-Reset Based Self-Starter With 2-nW Quiescent Power for Thermoelectric Energy Harvesting Systems; A CMOS Startup Circuit for Thermoelectric Energy Harvesting Systems
