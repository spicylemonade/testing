* Shared startup abstractions for H1 cold-start experiments.

.func pos(x) { 0.5 * (x + abs(x)) }
.func neg(x) { 0.5 * (-x + abs(x)) }

.param RON_ROUTE=2
.param ROFF_ROUTE=200k
.param ROUTE_HYST=1u
.param G_PUMP=50u
.param ETA_PUMP=3
.param VSTART_DEAD=5m

.model SWROUTE SW(Ron={RON_ROUTE} Roff={ROFF_ROUTE} Vt=0 Vh={ROUTE_HYST})

.subckt fw_router in_p in_n out_p out_n
BCTRL ctrl 0 V = { V(in_p,in_n) }
SROUTE_P out_p in_p ctrl 0 SWROUTE
SROUTE_N out_n in_n ctrl 0 SWROUTE
SROUTE_XP out_p in_n 0 ctrl SWROUTE
SROUTE_XN out_n in_p 0 ctrl SWROUTE
.ends fw_router

.subckt startup_pump in_p in_n n_store n_handoff
BIN_LOAD in_p in_n I = { G_PUMP * pos(V(in_p,in_n) - VSTART_DEAD) }
BSTORE 0 n_store I = { ETA_PUMP * G_PUMP * pos(V(in_p,in_n) - VSTART_DEAD) }
BHANDOFF n_handoff 0 V = { V(n_store) >= V_HANDOFF ? 1 : 0 }
.ends startup_pump
