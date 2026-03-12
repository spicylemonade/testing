# Ablations

- `time_constant_ranked_arbiter/`
  - Lower-overhead source-aware ablation used as the required benchmark line.
- `source_blind_packet_gate/`
  - Packet-gate ablation that keeps the same startup scaffold but removes source-aware ranking.
  - This is the current gate-ready ablation paired with the champion RC-ranked packet gate.
