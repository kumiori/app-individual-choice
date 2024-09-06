import streamlit as st

if st.secrets["runtime"]["STATUS"] == "Production":
    # st.set_page_config(
    #     page_title="Celestial Verse Portal",
    #     page_icon="✨",
    #     layout="wide",
    #     initial_sidebar_state="collapsed"
    # )

    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        [data-testid="stHeader"] {
            display: none
            }
    </style>
    """,
        unsafe_allow_html=True,
    )
