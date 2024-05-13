import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from util import load_stats, butt_list, track_formatter

def jockey_runs():
    if 'stats' not in st.session_state:
        st.session_state['stats'] = load_stats()

    if 'jr-track' not in st.session_state:
        st.session_state['jr-track'] = None
    
    if 'jockey_count' not in st.session_state:
        st.session_state['jockey_count'] = None

    stats = st.session_state['stats']
    track = st.session_state['jr-track']
    strict = None


    with st.form('rf'):
        venue = st.selectbox(
            "Choose Venue", (('ST',14),('HV', 12)), format_func =lambda x: {('ST',14): "Sha Tin", ('HV', 12): "Happy Valley"}.get(x),
            key = 'rfv'
            )

        distance = st.selectbox(
            "Choose Distance", np.sort(stats['distance'].unique()),
            key = 'rfd'
            )

        surface = st.selectbox(
            "Choose Surface", (0,1), format_func =lambda x: {0: "Turf", 1: "Dirt"}.get(x),
            key = 'rfs'
            )
        submitTrack = st.form_submit_button('Submit Track')

    if submitTrack:
        st.session_state['jr-track'] = [venue, distance, surface]
        st.rerun()       

    if track:
        if st.button('Reset Track', type = 'primary'):
            st.session_state['jr-track'] = None
            st.rerun()
            
        strict = st.checkbox('Strict Mode', key = 'jrs')
    
    jockey_count = st.session_state['jockey_count']
    st.session_state['jockey_count'] = st.number_input('Number of Jockeys to Show', min_value = 1, value = 10)

    #filtered_df = stats[['jockey_id', metric]].groupby(by = 'jockey_id').mean()
    #for jockey in st.session_state['jockey_id']:
    #    if jockey in filtered_df.index:
    #        df.loc[jockey, 'All Tracks'] = filtered_df.loc[jockey, metric].round(1) if metric == 'result' else str(filtered_df.loc[jockey, metric].round(1)) + '%'
    if track:
        condition1 = (stats['venue'] == track[0][0]) & (stats['run_count'] == track[0][1]) if strict else stats['venue'] == track[0][0]
        condition2 = stats['distance'] == track[1]
        condition3 = stats['surface'] == track[2]
        df = stats.loc[condition1 & condition2 & condition3]['jockey_id'].value_counts()[0:jockey_count]
    else:
        df = stats['jockey_id'].value_counts()[0:jockey_count]
    st.write(jockey_count)
    if track:
        st.title(track_formatter(track))
    else: st.title('All Tracks')
    if not df.empty:
        st.write(df)