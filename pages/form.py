import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from util import load_stats

if 'stats' not in st.session_state:
    st.session_state['stats'] = load_stats()

stats = st.session_state['stats']

metric = st.selectbox(
    "Choose Success Metric", ("won", "top_3", "result"), format_func =lambda x: {"won": "Win Rate", "top_3": "Place Rate (Top 3)", "result": "Avg Position"}.get(x)
    )
perCoeff = 1 if metric == 'result' else 100

scatter_plot = stats[['form', metric]].groupby('form').mean()*100

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

chart = (
   alt.Chart(scatter_plot.reset_index())
   .mark_circle()
   .encode(
    x='form:Q',
    y=metric + ':Q',
).interactive()
)

st.altair_chart(chart, use_container_width=True)