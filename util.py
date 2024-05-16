import streamlit as st
import pandas as pd

@st.cache_data
def load_stats():
    return pd.read_csv('stats.csv')

def butt_list(obList, formatter, twoCol = True):
    col21, col22 = st.columns(2)
    col31, col32, col33 = st.columns(3)
    if twoCol == True:
        for i, x in enumerate(obList):
            with {0: col21, 1: col22}.get(i%2):
                if st.button(formatter(x) + ' ❌'):
                    del obList[i]
                    st.rerun()
    else:
        for i, x in enumerate(obList):
            with {0: col31, 1: col32, 2: col33}.get(i%3):
                if st.button(formatter(x) + ' ❌'):
                    del obList[i]
                    st.rerun()

def track_formatter(x):
   return x[0][0] + ' ' + str(x[1]) + ' ' + {0: "Turf", 1: "Dirt"}.get(x[2])
