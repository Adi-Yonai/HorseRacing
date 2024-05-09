import streamlit as st
import pandas as pd

def load_stats():
    return pd.read_csv('stats.csv')