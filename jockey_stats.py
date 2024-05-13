import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from util import load_stats, butt_list, track_formatter

def jockey_stats():
    if 'stats' not in st.session_state:
        st.session_state['stats'] = load_stats()

    if 'js-tracks' not in st.session_state:
        st.session_state['js-tracks'] = []

    if 'jockey_id' not in st.session_state:
        st.session_state['jockey_id'] = []

    stats = st.session_state['stats']
    trackNames = list(map(track_formatter, st.session_state['js-tracks']))

    with st.form('Stats Track selection'):
        venue = st.selectbox(
            "Choose Venue", (('ST',14),('HV', 12)), format_func =lambda x: {('ST',14): "Sha Tin", ('HV', 12): "Happy Valley"}.get(x),
            key = 'sfv'
            )

        distance = st.selectbox(
            "Choose Distance", np.sort(stats['distance'].unique()),
            key = 'sfd'
            )

        surface = st.selectbox(
            "Choose Surface", (0,1), format_func =lambda x: {0: "Turf", 1: "Dirt"}.get(x),
            key = 'sfs'
            )
        submitTrack = st.form_submit_button('Submit Track')

    if submitTrack:
        subTrack = [venue, distance, surface]
        if subTrack not in st.session_state['js-tracks']:
            st.session_state['js-tracks'].append(subTrack)
            trackNames = list(map(track_formatter, st.session_state['js-tracks']))
    butt_list(st.session_state['js-tracks'], track_formatter)

    with st.form('Jockey selection'):
        jockey_id = st.number_input('Pick Jockey ID', min_value = 0, max_value = 184)
        submitJockey = st.form_submit_button('Submit Jockey')

    if submitJockey:
        if jockey_id not in st.session_state['jockey_id']:
            st.session_state['jockey_id'].append(jockey_id)
            st.session_state['jockey_id'].sort()
    butt_list(st.session_state['jockey_id'], str)

    metric = st.selectbox(
        "Choose Success Metric", ("won", "top_3", "result"), format_func =lambda x: {"won": "Win Rate", "top_3": "Place Rate (Top 3)", "result": "Avg Position"}.get(x)
        )
    perCoeff = 1 if metric == 'result' else 100

    strict = st.checkbox('Strict Mode', key = 'jss')
    st.write(st.session_state['jockey_id'])
    df = pd.DataFrame([], index = st.session_state['jockey_id'], columns = ['All Tracks'] + trackNames)
    filtered_df = perCoeff*stats[['jockey_id', metric]].groupby(by = 'jockey_id').mean()
    for jockey in st.session_state['jockey_id']:
        if jockey in filtered_df.index:
            df.loc[jockey, 'All Tracks'] = filtered_df.loc[jockey, metric].round(1) if metric == 'result' else str(filtered_df.loc[jockey, metric].round(1)) + '%'
    for track in st.session_state['js-tracks']:
        condition1 = (stats['venue'] == track[0][0]) & (stats['run_count'] == track[0][1]) if strict else stats['venue'] == track[0][0]
        condition2 = stats['distance'] == track[1]
        condition3 = stats['surface'] == track[2]
        filtered_df = perCoeff*stats.loc[condition1 & condition2 & condition3][['jockey_id', metric]].groupby(by = 'jockey_id').mean()
        for jockey in st.session_state['jockey_id']:
            if jockey in filtered_df.index:
                df.loc[jockey, track_formatter(track)] = filtered_df.loc[jockey, metric].round(1) if metric == 'result' else str(filtered_df.loc[jockey, metric].round(1)) + '%'

    if not df.empty:
        st.write(df)  