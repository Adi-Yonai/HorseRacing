import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from util import load_stats, butt_list, track_formatter
from jockey_stats import jockey_stats
from jockey_runs import jockey_runs

tab1, tab2 = st.tabs(['Stats', 'Run Numbers'])

with tab1:
    jockey_stats()

with tab2:
    jockey_runs()