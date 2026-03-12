* Shared packet-scout front end for champion and blind-merge ablation.

.param G_SCOUT=20u
.param T_SCOUT_WIDTH=5m
.param T_SCOUT_PERIOD=20m
.param T_SCOUT_DELAY_B=10m
.param T_SCOUT_DONE=80m
.param R_ENV=100k
.param C_ENV=2u
.param RON_SELECT=1
.param ROFF_SELECT=1meg
.param VSELECT_HYST=50m

.model SWSELECT SW(Ron={RON_SELECT} Roff={ROFF_SELECT} Vt=0.5 Vh={VSELECT_HYST})

.subckt packet_scout_frontend src_a_p src_a_n src_b_p src_b_n start_p start_n env_a env_b sel_a sel_b params: aware=1
XROUTE_A src_a_p src_a_n a_bus_p a_bus_n fw_router
XROUTE_B src_b_p src_b_n b_bus_p b_bus_n fw_router

VCLK_A clk_a 0 PULSE(0 1 0 500u 500u {T_SCOUT_WIDTH} {T_SCOUT_PERIOD})
VCLK_B clk_b 0 PULSE(0 1 {T_SCOUT_DELAY_B} 500u 500u {T_SCOUT_WIDTH} {T_SCOUT_PERIOD})

BSCOUT_A a_bus_p a_bus_n I = { G_SCOUT * V(clk_a) }
BSCOUT_B b_bus_p b_bus_n I = { G_SCOUT * V(clk_b) }

BBUSMON_A bus_a_mon 0 V = { V(a_bus_p,a_bus_n) }
BBUSMON_B bus_b_mon 0 V = { V(b_bus_p,b_bus_n) }
RENV_A bus_a_mon env_a {R_ENV}
RENV_B bus_b_mon env_b {R_ENV}
CENV_A env_a 0 {C_ENV}
CENV_B env_b 0 {C_ENV}

BSEL_A sel_a 0 V = { time > T_SCOUT_DONE ? (aware * (V(env_a) >= V(env_b)) + (1 - aware)) : 0 }
BSEL_B sel_b 0 V = { time > T_SCOUT_DONE ? (aware * (V(env_b) > V(env_a)) + (1 - aware)) : 0 }

SSEL_A_P start_p a_bus_p sel_a 0 SWSELECT
SSEL_A_N start_n a_bus_n sel_a 0 SWSELECT
SSEL_B_P start_p b_bus_p sel_b 0 SWSELECT
SSEL_B_N start_n b_bus_n sel_b 0 SWSELECT
.ends packet_scout_frontend
