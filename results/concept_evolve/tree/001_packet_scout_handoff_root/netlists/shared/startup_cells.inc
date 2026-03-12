* Shared startup abstractions for H1 cold-start experiments.

.func pos(x) { 0.5 * (x + abs(x)) }
.func neg(x) { 0.5 * (-x + abs(x)) }

.param RON_ROUTE=5
.param ROFF_ROUTE=200k
.param RLEAK_ROUTE=1e15
.param ROUTE_HYST=2m
.param G_PUMP=50u
.param ETA_PUMP=3
.param VSTART_DEAD=5m

.model SWROUTE SW(Ron={RON_ROUTE} Roff={ROFF_ROUTE} Vt=1m Vh={ROUTE_HYST})
.model SWHANDOFF SW(
  Ron=1m
  Roff=1e12
  Vt={(V_HANDOFF + V_HANDOFF_FALL) / 2}
  Vh={(V_HANDOFF - V_HANDOFF_FALL) / 2}
)

.subckt fw_router in_p in_n out_p out_n
BCTRL ctrl 0 V = { V(in_p,in_n) }
SROUTE_P out_p in_p ctrl 0 SWROUTE
SROUTE_N out_n in_n ctrl 0 SWROUTE
SROUTE_XP out_p in_n 0 ctrl SWROUTE
SROUTE_XN out_n in_p 0 ctrl SWROUTE
RLEAK_PP out_p in_p {RLEAK_ROUTE}
RLEAK_NN out_n in_n {RLEAK_ROUTE}
RLEAK_PN out_p in_n {RLEAK_ROUTE}
RLEAK_NP out_n in_p {RLEAK_ROUTE}
.ends fw_router

.subckt handoff_flag n_store n_handoff
VHAND_REF n_hand_ref 0 1
SHAND n_handoff n_hand_ref n_store 0 SWHANDOFF
RHAND_PD n_handoff 0 10k
.ends handoff_flag

.subckt startup_pump in_p in_n n_store n_handoff
BIN_LOAD in_p in_n I = { G_PUMP * pos(V(in_p,in_n) - VSTART_DEAD) }
BSTORE 0 n_store I = { ETA_PUMP * G_PUMP * pos(V(in_p,in_n) - VSTART_DEAD) }
XHANDOFF n_store n_handoff handoff_flag
.ends startup_pump
