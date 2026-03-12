* Shared floating two-source Thevenin model for H1 cold-start experiments.

.param VOC_A=100m
.param VOC_B=100m
.param POL_A=1
.param POL_B=-1
.param R_A=1k
.param R_B=1k
.param RAMP_MVPS=10
.param RAMP_VPS={RAMP_MVPS * 1e-3}
.param T_COLLAPSE_A=1e12
.param T_RECOVER_A=1e12
.param COLLAPSE_SCALE_A=1
.param T_COLLAPSE_B=1e12
.param T_RECOVER_B=1e12
.param COLLAPSE_SCALE_B=1
.param T_COLLAPSE_EDGE=10m

.subckt source_pair src_a_p src_a_n src_b_p src_b_n
BWIN_A win_a 0 V = { 0.5 * (tanh((time - T_COLLAPSE_A) / T_COLLAPSE_EDGE) + 1) - 0.5 * (tanh((time - T_RECOVER_A) / T_COLLAPSE_EDGE) + 1) }
BWIN_B win_b 0 V = { 0.5 * (tanh((time - T_COLLAPSE_B) / T_COLLAPSE_EDGE) + 1) - 0.5 * (tanh((time - T_RECOVER_B) / T_COLLAPSE_EDGE) + 1) }

BSRC_A va_p va_n V = { POL_A * min(VOC_A, RAMP_VPS * time) * (1 - (1 - COLLAPSE_SCALE_A) * V(win_a)) }
RA_P va_p src_a_p {R_A / 2}
RA_N src_a_n va_n {R_A / 2}

BSRC_B vb_p vb_n V = { POL_B * min(VOC_B, RAMP_VPS * time) * (1 - (1 - COLLAPSE_SCALE_B) * V(win_b)) }
RB_P vb_p src_b_p {R_B / 2}
RB_N src_b_n vb_n {R_B / 2}
.ends source_pair
