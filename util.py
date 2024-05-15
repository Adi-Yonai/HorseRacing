import streamlit as st
import pandas as pd

@st.cache_data
def load_stats():
    return pd.read_csv('stats.csv')

def butt_list(obList, formatter):
    col1, col2 = st.columns(2)
    for i, x in enumerate(obList):
        with (lambda num: col1 if num % 2 == 0 else col2)(i):
            if st.button(formatter(x)):
                del obList[i]
                st.rerun()

def track_formatter(x):
   return x[0][0] + ' ' + str(x[1]) + ' ' + {0: "Turf", 1: "Dirt"}.get(x[2])
