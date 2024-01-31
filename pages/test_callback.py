import streamlit as st

def waschanged(key):
    st.info(st.session_state[key])

setBrightness = st.slider("Brightness", -10, 10, 0, step=1, key="Brightness", on_change=waschanged, args=("Brightness",))