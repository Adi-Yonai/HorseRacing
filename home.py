import streamlit as st

st.title('Horse Racing Analysys App')

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.page_link('pages/draw.py', )

with col2:
    st.page_link('pages/form.py', )

with col3:
    st.page_link('pages/jockey.py', )

with col4:
    st.page_link('pages/run_style.py', )
