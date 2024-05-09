import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from util import load_stats

stats = load_stats()

venue = st.multiselect(
    "Choose Venue", (('ST',14),('HV', 12)), format_func =lambda x: {('ST',14): "Sha Tin", ('HV', 12): "Happy Valley"}.get(x)
    )

distance = st.multiselect(
    "Choose Distance", stats['distance'].unique()
    )

surface = st.multiselect(
    "Choose Surface", (0,1), format_func =lambda x: {0: "Turf", 1: "Dirt"}.get(x)
    )

metric = st.selectbox(
    "Choose Success Metric", ("won", "top_3", "result"), format_func =lambda x: {"won": "Win Rate", "top_3": "Place Rate (Top 3)", "result": "Avg Position"}.get(x)
    )
perCoeff = 1 if metric == 'result' else 100

condition1 = stats['distance'].isin(distance) if distance else True
condition2 = stats['surface'].isin(surface) if surface else True
condition3 = (stats['venue'] == venue[0][0]) & (stats['run_count'] == venue[0][1]) if len(venue) == 1 else stats['run_count'] >11

filtered_df = perCoeff*stats.loc[condition1 & condition2 & condition3][['draw', metric]].groupby(by = 'draw').mean()

chart = (
   alt.Chart(filtered_df.round(1).reset_index())
   .mark_bar(size = 30)
   .encode(
    x='draw:Q',
    y=metric + ':Q'
).interactive()
)

st.altair_chart(chart, use_container_width=True)
