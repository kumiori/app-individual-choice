import streamlit as st
import streamlit.components.v1 as components
import hashlib
import datetime
import time

if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Infinite Potential - Settimia",
        page_icon="✨",
        # layout="wide",
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

st.write(st.secrets["runtime"]["STATUS"])



from streamlit_vertical_slider import vertical_slider 
from lib.texts import _stream_example, corrupt_string
from pages.test_geocage import get_coordinates
from pages.test_injection import CustomStreamlitSurvey
from streamlit_extras.streaming_write import write as streamwrite 
import time
import string
import streamlit_survey as ss
from streamlit_extras.row import row
from streamlit_extras.stateful_button import button as stateful_button
import random
from pages.test_settimia import fetch_and_display_data
from pages.test_location import conn
from pages.test_paged import PagedContainer
# from pages.test_game import display_dictionary_by_indices
# from pages.test_pleasure import display_dictionary

from lib.matrices import generate_random_matrix, encode_matrix, display_matrix
from lib.matrices import generate_random_matrix, encode_matrix, display_matrix
from lib.dictionary_manip import display_dictionary, display_dictionary_by_indices, display_details_description
from lib.io import create_button, create_dichotomy, create_qualitative, create_yesno, create_next, create_globe, create_textinput, create_checkbox,create_equaliser

update_frequency = 500  # in milliseconds

with open("pages/settimia.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.write(f.read())
    
# Main function
def main():
    # Page title
    # st.title(":circus_tent: Europe in Discourse")
    # st.title(":fountain: Athens Conference, :satellite: 2024")

    # survey = ss.StreamlitSurvey("Home")
    col1, col2, col3 = st.columns(3)

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    
    if 'damage_parameter' not in st.session_state:
        st.session_state.damage_parameter = 0.0  # Initial damage parameter
    
    if 'location' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter
    
    if 'coordinates' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter

    # once usage:
    # streamwrite(_stream_once(intro_text, 0))
    # st.markdown()
    st.divider()
    now = datetime.datetime.now()
    st.markdown("# <center>The Fellowship of the Infinite Potential</center>", unsafe_allow_html=True)
    st.markdown("### <center>Let's meet, Settimia...</center>", unsafe_allow_html=True)
    st.markdown('<center>``wait a minute``</center>', unsafe_allow_html=True)
    st.markdown('', unsafe_allow_html=True)
    
    
if __name__ == "__main__":
    
    survey = main()
    # add_vertical_space(1)
    # more()
    create_globe("Settimia")