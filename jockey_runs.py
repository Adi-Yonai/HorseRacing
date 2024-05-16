import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from util import load_stats, butt_list, track_formatter

def butt_func(state):
    st.session_state['isTrack'] = state

def jockey_runs():
    if 'stats' not in st.session_state:
        st.session_state['stats'] = load_stats()

    if 'jr-track' not in st.session_state:
        st.session_state['jr-track'] = None
    
    if 'jockey_count' not in st.session_state:
        st.session_state['jockey_count'] = 10
    
    if 'isTrack' not in st.session_state:
        st.session_state['isTrack'] = False

    stats = st.session_state['stats']
    track = st.session_state['jr-track']
    strict = None

    st.title('Jockey Run Numbers')
    st.write('Check the Jockeys with the most runs for an individual race or overall.')
    st.write('Strict mode will only check full races.')
    col1, col2 = st.columns(2)
    
    with col1:
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
        track = st.session_state['jr-track']
        st.session_state['isTrack'] = True
        with col1:
            butt_func(True)

    if st.session_state['isTrack'] == True:
        with col1:
            st.button('Reset Track', type = 'primary', on_click = butt_func, args = [False])
            strict = st.checkbox('Strict Mode', key = 'jrs')
    else:
        st.session_state['jr-track'] = None
        track = st.session_state['jr-track']
        
    with col1:
        st.session_state['jockey_count'] = st.number_input('Number of Jockeys to Show', min_value = 1, value = 10)
    
    if track:
        condition1 = (stats['venue'] == track[0][0]) & (stats['run_count'] == track[0][1]) if strict else stats['venue'] == track[0][0]
        condition2 = stats['distance'] == track[1]
        condition3 = stats['surface'] == track[2]
        df = stats.loc[condition1 & condition2 & condition3]['jockey_id'].value_counts()[0:st.session_state['jockey_count']]
    else:
        df = stats['jockey_id'].value_counts()[0:st.session_state['jockey_count']]
    if track:
        st.title(track_formatter(track))
    else:
        with col2:
            st.title('All Tracks')
    if not df.empty:
        with col2:
            st.write(df)
