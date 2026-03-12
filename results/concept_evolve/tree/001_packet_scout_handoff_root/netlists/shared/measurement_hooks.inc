* Shared measurements for H1 baseline and champion netlists.
*
* The latch below records the first handoff event without loading the design
* itself. That lets the "pre-handoff" metrics stop permanently after the first
* successful release while failed cases still integrate across the full window.

BSEEN_DRV seen_drv 0 V = { V(n_handoff) > 0.5 ? 1 : 0 }
DSEEN seen_drv n_seen DSEENMOD
CSEEN n_seen 0 1p ic=0
RSEEN n_seen 0 1e12
BHAND_EVT_DRV handoff_evt_drv 0 V = { V(n_handoff) }
REVT handoff_evt_drv n_handoff_evt 1k
CEVT n_handoff_evt 0 1u ic=0
.model DSEENMOD D(Is=1e-18 N=1 Rs=1m Cjo=0)

BLATCH handoff_latched 0 V = { 0.5 * (1 + tanh(80 * (V(n_seen) - 0.5))) }
BPAWR_A pwr_back_a 0 V = { neg(V(n_src_a_p,n_src_a_n) * I(VMEAS_A)) }
BPAWR_B pwr_back_b 0 V = { neg(V(n_src_b_p,n_src_b_n) * I(VMEAS_B)) }
BPCTRL pwr_ctrl 0 V = { pos(V(n_store) * I(VCTRL_MON)) }
BPAWR_A_PRE pwr_back_a_pre 0 V = { V(pwr_back_a) * (1 - V(handoff_latched)) }
BPAWR_B_PRE pwr_back_b_pre 0 V = { V(pwr_back_b) * (1 - V(handoff_latched)) }
BPCTRL_PRE pwr_ctrl_pre 0 V = { V(pwr_ctrl) * (1 - V(handoff_latched)) }

.measure tran vstore_final find v(n_store) at={TSTOP}
.measure tran handoff_seen_final find v(n_seen) at={TSTOP}
.measure tran t_handoff when v(n_handoff_evt)=0.5 rise=1
.measure tran t_handoff_fall when v(n_handoff_evt)=0.5 fall=1
.measure tran t_handoff_rise2 when v(n_handoff_evt)=0.5 rise=2
.measure tran t_store_proxy when v(n_store)={V_HANDOFF} rise=1
.measure tran t_store_proxy_fall when v(n_store)={V_HANDOFF_FALL} fall=1
.measure tran t_store_proxy_rise2 when v(n_store)={V_HANDOFF} rise=2
.measure tran e_back_a integ v(pwr_back_a_pre) from=0 to={TSTOP}
.measure tran e_back_b integ v(pwr_back_b_pre) from=0 to={TSTOP}
.measure tran e_backdrive param='e_back_a + e_back_b'
.measure tran e_ctrl integ v(pwr_ctrl_pre) from=0 to={TSTOP}
.measure tran e_back_a_full integ v(pwr_back_a) from=0 to={TSTOP}
.measure tran e_back_b_full integ v(pwr_back_b) from=0 to={TSTOP}
.measure tran e_backdrive_full param='e_back_a_full + e_back_b_full'
.measure tran e_ctrl_full integ v(pwr_ctrl) from=0 to={TSTOP}
.measure tran startup_ok param='(vstore_final >= V_HANDOFF) * (handoff_seen_final >= 0.5)'
