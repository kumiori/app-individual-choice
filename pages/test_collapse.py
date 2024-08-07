import streamlit as st


st.set_page_config(
    page_title="Celestial Verse Portal",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
