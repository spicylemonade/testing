* Shared measurements for H1 baseline and champion netlists.

BPAWR_A pwr_back_a 0 V = { neg(V(n_src_a_p,n_src_a_n) * I(VMEAS_A)) }
BPAWR_B pwr_back_b 0 V = { neg(V(n_src_b_p,n_src_b_n) * I(VMEAS_B)) }
BPCTRL pwr_ctrl 0 V = { pos(V(n_store) * I(VCTRL_MON)) }

.measure tran vstore_final find v(n_store) at={TSTOP}
.measure tran t_handoff when v(n_handoff)=0.5 rise=1
.measure tran e_back_a integ v(pwr_back_a) from=0 to={TSTOP}
.measure tran e_back_b integ v(pwr_back_b) from=0 to={TSTOP}
.measure tran e_backdrive param='e_back_a + e_back_b'
.measure tran e_ctrl integ v(pwr_ctrl) from=0 to={TSTOP}
.measure tran startup_ok param='(vstore_final >= V_HANDOFF)'
