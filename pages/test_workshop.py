import streamlit as st
import streamlit.components.v1 as components
import hashlib
import datetime
import time
import streamlit_tags as st_tags
import pandas as pd
import streamlit_player as st_player

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


# Combien avons nous besoin de:
# (equaliser)
# pargager des connaissances
# pargager des ressources
# pargager des approches
# pargager des données
# pargager des perspectives
# pargager des problèmes


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
    
    
keywords = [
    "Cryosphere",
    "Ice Shelf",
    "Climate Science",
    "Scientific Workshop",
    "Environmental Research",
    "Glaciology",
    "Irreversible Evolution",
    "Energy",
    "Scientific Collaboration",
    "*quels mots clé ?*"
]

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
    st.markdown("# <center>Atelier, Cryosphère et Stabilité</center>", unsafe_allow_html=True)
    st.markdown("### <center>Grenoble, 2024</center>", unsafe_allow_html=True)
    st.markdown("### <center> . nous Nous organisons : </center>", unsafe_allow_html=True)
    
    concatenated_keywords = " • ".join([f"**{keyword}**" for keyword in keywords])
    # st.write(concatenated_keywords)
    st.markdown(f"### <center> K > {concatenated_keywords}  </center>", unsafe_allow_html=True)
    st.markdown('<center>``wait a minute``</center>', unsafe_allow_html=True)
    st.markdown('`Do we have any data?`', unsafe_allow_html=True)
    st.markdown('', unsafe_allow_html=True)

    # def st_tags(label: str,
    #         text: str,
    #         value: list,
    #         suggestions: list,
    #         key=None) -> list:
    tags = st_tags.st_tags(label = "## Collaborons...",
        text="Quels mots à ajouter ?",
                    suggestions=keywords,)
    # give your partner a sexy dance
    # 
    if tags:
        st.write(f"`Juste le temps de connecter une base de données...`")
        st.write(f"`{tags}`")
    
    invited_list = [
        "Sedhar Chozam, Oxford",
"Stéphane Perrard, PMMH, Paris",
"Véronique Dansereau, ..., Grenoble",
"Jérôme Weiss, ..., Grenoble",
"Florent Gimbert, ..., Grenoble",
"Olivier Gagliardini, ..., Grenoble",
"David Marsan, ..., Grenoble",
"Benoit Roman, PMMH, Paris",
"Maurice Rossi, dAlembert, Paris",
"Flaviana Iurlano, U. Genova",
"Giuliano Lazzaroni, ..., Pisa",
"Pierluigi Cesana, Fukuoka University, Kyushu, Japan",
"Masato Kimura, Kanazawa University, Kyushu, Japan",
"Garth Wells, , ",
"Jorgen Dokken, , ",
"Patrick Farrell, , ",
"Gui-Qiang Chen, Mathematical Institute, Oxford",
    ]
if __name__ == "__main__":
    
    survey = main()
    # add_vertical_space(1)
    # more()
    create_globe("Settimia", kwargs={'database': 'gathering'})
    
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Connecting...", 
    "Contributions", 
    "Contact", 
    "Minimal Glossary", 
    "Frequency Asked Questions", 
    "References",
    "Never Asked Questions"])
    with tab1:
        st.markdown("## Une connexion fortuite ?")
        st_player.st_player("https://www.youtube.com/watch?v=zROrdF5IXC8")

    with tab3:

        invited_list = [
            "Sedhar Chozam, Oxford",
            "Stéphane Perrard, PMMH, Paris",
            "Véronique Dansereau, ..., Grenoble",
            "Jérôme Weiss, ..., Grenoble",
            "Florent Gimbert, ..., Grenoble",
            "Olivier Gagliardini, ..., Grenoble",
            "David Marsan, ..., Grenoble",
            "Benoit Roman, PMMH, Paris",
            "Jean-Jacques Marigo, ..., Pyrenées",
            "Maurice Rossi, dAlembert, Paris",
            "Flaviana Iurlano, U. Genova",
            "Giuliano Lazzaroni, ..., Pisa",
            "Pierluigi Cesana, Fukuoka University, Kyushu-Japan",
            "Masato Kimura, Institute of Science and Engineering, Kanazawa-Japan",
            "Garth Wells, , ",
            "Jorgen Dokken, , ",
            "Patrick Farrell, , ",
            "Gui-Qiang Chen, Mathematical Institute, Oxford",
        ]

        # Splitting data into name, affiliation, and location
        data = [entry.split(', ') for entry in invited_list]
        headers = ["name", "affiliation", "location"]

        # Create a Pandas DataFrame
        df = pd.DataFrame(data)
        st.table(df)
