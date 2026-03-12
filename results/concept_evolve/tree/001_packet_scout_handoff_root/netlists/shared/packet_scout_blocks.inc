* Shared packet-scout blocks for champion and ablation decks.

.param SCOUT_R=150k
.param SCOUT_C=5n
.param SEL_GAIN=20
.param G_SCOUT_CTRL=40n
.param MERGE_R=5
.param TC_FAST_R=30k
.param TC_FAST_C=1.5n
.param TC_SLOW_R=220k
.param TC_SLOW_C=7n
.param TC_GAIN=26
.param TC_TIE=6
.param G_TC_CTRL=18n

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
XHANDOFF n_store n_handoff handoff_flag
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
XHANDOFF n_store n_handoff handoff_flag
.ends source_blind_packet_gate

.subckt blind_packet_merge_gate a_p a_n b_p b_n n_store n_ctrl n_handoff
EOBS_A a_obs 0 VALUE = { V(a_p,a_n) }
RSCOUT_A a_obs a_probe {SCOUT_R}
CSCOUT_A a_probe 0 {SCOUT_C}

EOBS_B b_obs 0 VALUE = { V(b_p,b_n) }
RSCOUT_B b_obs b_probe {SCOUT_R}
CSCOUT_B b_probe 0 {SCOUT_C}

RMERGE_AP a_p merge_p {MERGE_R}
RMERGE_BP b_p merge_p {MERGE_R}
RMERGE_AN a_n merge_n {MERGE_R}
RMERGE_BN b_n merge_n {MERGE_R}

BIN_M merge_p merge_n I = { G_PUMP * pos(V(merge_p,merge_n) - VSTART_DEAD) }
BSTORE_M 0 n_store I = { ETA_PUMP * G_PUMP * pos(V(merge_p,merge_n) - VSTART_DEAD) }

BCTRL_SCOUT n_ctrl 0 I = { G_SCOUT_CTRL * V(n_ctrl) }
XHANDOFF n_store n_handoff handoff_flag
.ends blind_packet_merge_gate

.subckt time_constant_ranked_arbiter a_p a_n b_p b_n n_store n_ctrl n_handoff
EOBS_A a_obs 0 VALUE = { V(a_p,a_n) }
RFAST_A a_obs a_fast {TC_FAST_R}
CFAST_A a_fast 0 {TC_FAST_C}
RSLOW_A a_obs a_slow {TC_SLOW_R}
CSLOW_A a_slow 0 {TC_SLOW_C}

EOBS_B b_obs 0 VALUE = { V(b_p,b_n) }
RFAST_B b_obs b_fast {TC_FAST_R}
CFAST_B b_fast 0 {TC_FAST_C}
RSLOW_B b_obs b_slow {TC_SLOW_R}
CSLOW_B b_slow 0 {TC_SLOW_C}

BRANK_A rank_a 0 V = { V(a_fast) - V(a_slow) }
BRANK_B rank_b 0 V = { V(b_fast) - V(b_slow) }
*
* The tie term keeps the selector well behaved when both fast-slow windows are
* nearly equal under very slow ramps.
BSEL_A sel_a 0 V = { 0.5 * (1 + tanh(TC_GAIN * ((V(rank_a) - V(rank_b)) + TC_TIE * (V(a_fast) - V(b_fast))))) }
BSEL_B sel_b 0 V = { 1 - V(sel_a) }

BIN_A a_p a_n I = { G_PUMP * pos(V(a_p,a_n) - VSTART_DEAD) * V(sel_a) }
BIN_B b_p b_n I = { G_PUMP * pos(V(b_p,b_n) - VSTART_DEAD) * V(sel_b) }

BSTORE_A 0 n_store I = { ETA_PUMP * G_PUMP * pos(V(a_p,a_n) - VSTART_DEAD) * V(sel_a) }
BSTORE_B 0 n_store I = { ETA_PUMP * G_PUMP * pos(V(b_p,b_n) - VSTART_DEAD) * V(sel_b) }

BCTRL_TC n_ctrl 0 I = { G_TC_CTRL * V(n_ctrl) }
XHANDOFF n_store n_handoff handoff_flag
.ends time_constant_ranked_arbiter
