* Shared packet-scout blocks for champion and ablation decks.

.param SCOUT_R=150k
.param SCOUT_C=5n
.param SEL_GAIN=20
.param G_SCOUT_CTRL=40n

.subckt rc_rank_packet_gate a_p a_n b_p b_n n_store n_ctrl n_handoff
EOBS_A a_obs 0 VALUE = { V(a_p,a_n) }
RSCOUT_A a_obs a_probe {SCOUT_R}
CSCOUT_A a_probe 0 {SCOUT_C}

EOBS_B b_obs 0 VALUE = { V(b_p,b_n) }
RSCOUT_B b_obs b_probe {SCOUT_R}
CSCOUT_B b_probe 0 {SCOUT_C}

BSEL_A sel_a 0 V = { 0.5 * (1 + tanh(SEL_GAIN * (V(a_probe) - V(b_probe)))) }
BSEL_B sel_b 0 V = { 1 - V(sel_a) }

BIN_A a_p a_n I = { G_PUMP * pos(V(a_p,a_n) - VSTART_DEAD) * V(sel_a) }
BIN_B b_p b_n I = { G_PUMP * pos(V(b_p,b_n) - VSTART_DEAD) * V(sel_b) }

BSTORE_A 0 n_store I = { ETA_PUMP * G_PUMP * pos(V(a_p,a_n) - VSTART_DEAD) * V(sel_a) }
BSTORE_B 0 n_store I = { ETA_PUMP * G_PUMP * pos(V(b_p,b_n) - VSTART_DEAD) * V(sel_b) }

BCTRL_SCOUT n_ctrl 0 I = { G_SCOUT_CTRL * V(n_ctrl) }
BHANDOFF n_handoff 0 V = { V(n_store) >= V_HANDOFF ? 1 : 0 }
.ends rc_rank_packet_gate

.subckt source_blind_packet_gate a_p a_n b_p b_n n_store n_ctrl n_handoff
EOBS_A a_obs 0 VALUE = { V(a_p,a_n) }
RSCOUT_A a_obs a_probe {SCOUT_R}
CSCOUT_A a_probe 0 {SCOUT_C}

EOBS_B b_obs 0 VALUE = { V(b_p,b_n) }
RSCOUT_B b_obs b_probe {SCOUT_R}
CSCOUT_B b_probe 0 {SCOUT_C}

BIN_A a_p a_n I = { G_PUMP * pos(V(a_p,a_n) - VSTART_DEAD) * 0.5 }
BIN_B b_p b_n I = { G_PUMP * pos(V(b_p,b_n) - VSTART_DEAD) * 0.5 }

BSTORE_A 0 n_store I = { ETA_PUMP * G_PUMP * pos(V(a_p,a_n) - VSTART_DEAD) * 0.5 }
BSTORE_B 0 n_store I = { ETA_PUMP * G_PUMP * pos(V(b_p,b_n) - VSTART_DEAD) * 0.5 }

BCTRL_SCOUT n_ctrl 0 I = { G_SCOUT_CTRL * V(n_ctrl) }
BHANDOFF n_handoff 0 V = { V(n_store) >= V_HANDOFF ? 1 : 0 }
.ends source_blind_packet_gate
