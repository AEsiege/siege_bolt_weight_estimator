import streamlit as st
import scipy.stats as stats
import numpy as np
import math
from time import sleep

max_wt = 16.05

def reset_cb():
    st.session_state['how_many_bolts'] = ""
    del st.session_state['answer']

st.title("Bolt Weight Calculator")
n_bolts = st.text_input("How many bolts?",
                        key="how_many_bolts")
samps_space = st.empty()
reset_button = st.button("Clear and start over?",
                         key="reset_button",
                         on_click=reset_cb)

def calc_prob(*args, **kwargs):
    if not args:
        return
    elt = args[0]
    key = args[1]
    val = st.session_state[key]
    if val:
        try:
            val = float(val)
        except:
            st.error("Please enter a decimal number")
    n_bolts = kwargs['n_bolts']
    n_samps = kwargs['n_samps']
    all_entries = []
    for idx in range(n_samps):
        filled_val = st.session_state[f"wt_{idx}"]
        if filled_val:
            try:
                all_entries.append(float(filled_val))
            except:
                pass
    if len(all_entries) == n_samps:
        samps = np.array(all_entries)
        est_mean = samps.mean()
        est_stdv = np.std(samps, ddof=1)
        est_dist = stats.norm(est_mean, est_stdv)
        odds_per_bolt = 1.0 - est_dist.cdf(max_wt)
        odds_all_good = math.pow(1.0 - odds_per_bolt, n_bolts)
        st.session_state['answer'] = odds_all_good
    
try:
    if n_bolts:
        n_bolts = int(n_bolts)
    else:
        n_bolts = 0
except:
    st.error("Please enter an integer")
    n_bolts = 0

n_samps = int(max(np.round(math.sqrt(n_bolts)), 10))
if st.session_state['how_many_bolts']:
    samps_space.empty()
    with samps_space.container():
        st.write(f"Collect {n_samps} bolts from this group of {n_bolts} at random."
                 " Please enter their weights below as decimal ounces.")
        samp_wt_d = {}
        cols = st.columns(4)
        for elt in range(n_samps):
            which_col = cols[elt % len(cols)]
            key= f"wt_{elt}"
            samp_wt_d[elt] = which_col.text_input(key, label_visibility="collapsed",
                                                  key=key,
                                                  on_change=calc_prob,
                                                  kwargs={"weights": samp_wt_d,
                                                          "n_samps": n_samps,
                                                          "n_bolts": n_bolts},
                                                  args=[elt, key])
        if 'answer' in st.session_state:
            pct_str = "{:2.1%}".format(st.session_state['answer'])
            st.subheader(f"The chance that all bolts are below the limit is {pct_str}")
    


