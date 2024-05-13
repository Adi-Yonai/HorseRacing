import streamlit as st
import pandas as pd

@st.cache_data
def load_stats():
    return pd.read_csv('stats.csv')

def butt_list(obList, formatter):
    for i, x in enumerate(obList):
        if st.button(formatter(x)):
            del obList[i]
            st.rerun()

def track_formatter(x):
   return x[0][0] + ' ' + str(x[1]) + ' ' + {0: "Turf", 1: "Dirt"}.get(x[2])