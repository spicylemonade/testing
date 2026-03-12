* Shared floating two-source Thevenin model for H1 cold-start experiments.

.param VOC_A=100m
.param VOC_B=100m
.param POL_A=1
.param POL_B=-1
.param R_A=1k
.param R_B=1k
.param RAMP_MVPS=10
.param RAMP_VPS={RAMP_MVPS * 1e-3}

.subckt source_pair src_a_p src_a_n src_b_p src_b_n
BSRC_A va_p va_n V = { POL_A * min(VOC_A, RAMP_VPS * time) }
RA_P va_p src_a_p {R_A / 2}
RA_N src_a_n va_n {R_A / 2}

BSRC_B vb_p vb_n V = { POL_B * min(VOC_B, RAMP_VPS * time) }
RB_P vb_p src_b_p {R_B / 2}
RB_N src_b_n vb_n {R_B / 2}
.ends source_pair
