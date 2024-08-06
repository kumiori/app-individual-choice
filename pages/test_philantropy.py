import streamlit as st
st.set_page_config(
    page_title="Social Contract From Philanthropic Scratch",
    page_icon="🍥",
    initial_sidebar_state="collapsed",
)



import markdown

import codecs
import datetime
import hashlib
import random
import time

import bibtexparser
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import streamlit_player as st_player
import streamlit_survey as ss
import streamlit_tags as st_tags
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from streamlit_extras.row import row
from streamlit_extras.stateful_button import button as stateful_button
from streamlit_extras.streaming_write import write as streamwrite
from streamlit_vertical_slider import vertical_slider

from lib.dictionary_manip import (display_dictionary, display_dictionary_by_indices, display_details_description)
from lib.io import (conn, create_button, create_checkbox, create_dichotomy, create_equaliser, create_globe,
                    create_next, create_qualitative, create_textinput, create_yesno, fetch_and_display_data)
from lib.matrices import display_matrix, encode_matrix, generate_random_matrix
from lib.texts import _stream_example, corrupt_string
from pages.test_geocage import get_coordinates
from pages.test_injection import CustomStreamlitSurvey
# from pages.test_paged import PagedContainer

with open("pages/settimia.css", "r") as f:
# with open("assets/light-theme.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.write(f.read())
    
def display_dictionary(dictionary):
    """
    Function to display dictionary keys and content.
    """

    for key, content in dictionary.items():
        col1, _, col2 = st.columns([2, .1, 2])
        with col1:
            st.markdown(f"{key}")
        with col2:
            st.markdown(f"{content}", unsafe_allow_html=True)
        st.divider()


keywords = [
    "Emancipatory",
    "Multiscale",
    "Multidimensional",
    "Perspectives",
    "Vision",
    "Sustainability",
    "Trust",
    "Social",
    "Cohesion",
    "Contr$\\small{\\forall}$ct",
    "Contract",]

# Function to load and read the markdown content
def load_markdown(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def download_pdf():
    pdf_file_path = "data/presentation_en.pdf"

    with open(pdf_file_path, "rb") as f:
        pdf_bytes = f.read()
        
    st.download_button(label="Presentation (En)", data=pdf_bytes, 
                       file_name=f".pdf", mime="application/pdf",
                       use_container_width=True)

    pdf_file_path = "data/presentation_fr.pdf"

    # with open(pdf_file_path, "rb") as f:
    #     pdf_bytes = f.read()

    # st.download_button(label="Présentation (PDF 🇫🇷)", data=pdf_bytes, 
    #                    file_name=f"presentation_atelier_cryosphere_stabilité_fr.pdf", mime="application/pdf",
    #                    use_container_width=True)

def panel_contributions():
    panel_contributions = {
    "## Le Gai Savoir \n ## `Ariane Ahmadi`": "### A new ethic of power and action grounded in mutual support and shared values.",
    "## The Anarchist Banker \n ## `Nils Andersen`": "### A timely exploration of freedom, wealth, and societal roles.",
    "## Âmes de Paname \n ## `Bianca Apollonio`": "### Ethnographic and narrative insights into Parisian life and its broader European implications.",
    "## Je suis l'eau \n ## `Alessandra Carosi`": "### Artistic exploration of emotional landscapes through ecological transformations.",
    "## Retribution and Reform \n ## `Gabrielle Dyson`": "### The impact of European agricultural policy on human and microbial ecosystems.",
    "## Navigating Interactions \n ## `flcalb`": "### Experimental inquiry into trust and strategic thinking in social interactions.",
    "## Pulse \n ## `Giorgio Funaro`": "### Audiovisual installation tracing the journey of impulses in the human nervous system.",
    "## Moon Module \n ## `Hugues Genevois & Laurence White-Bouckaert`": "### Fusion of art and science in improvisational electroacoustic music.",
    "## Aligning Automated Decision Making \n ## `Claire Glanois`": "### Aligning AI systems with European values and ethical principles.",
    "## Power to Words \n ## `Amir Issaa`": "### The transformative power of rap as a medium for social commentary and engagement.",
    "## Encoded in Writing \n ## `Andrés León Baldelli`": "### Exploration of interfaces for coordination and communication in the urban jungle.",
    "## Rethinking Solutions \n ## `Graziano Mazza`": "### Economic theology as a lens for understanding European management and policy.",
    "## We Are Enough \n ## `Roger Niyigena Karera`": "### Artistic introspection on contemporary societal challenges.",
    "## Cultural Systems and Political Body \n ## `Francesco Raneri`": "### The role of cultural diversity in shaping European identity.",
    "## Engagement with the Sea \n ## `Antonia Taddei`": "### Legal, artistic, and scientific perspectives on granting personhood to ecosystems.",
    "## The Aftermath Of Political Violence \n ## `Sophie Wahnich`": "### Historical analysis of social trust and civil resilience, at the present tense."
    }
    return panel_contributions
# Main function to create the Streamlit page
def main():
    st.markdown("# ")


    now = datetime.datetime.now()
    st.markdown("# <center>The Social Contract from Scratch: A Philanthropic Approach</center>", unsafe_allow_html=True)
    st.markdown('#### `The social contract is a foundational concept in political philosophy, suggesting that individuals consent, either implicitly or explicitly, to form a society and abide by its rules, norms, and laws for` _mutual benefit_.') 
    st.markdown('#### `It posits that in exchange for giving up certain freedoms, individuals receive protection and order provided by the collective governance structure.`')
    st.markdown('#### `Historically articulated by philosophers, the social contract addresses questions of legitimacy, authority, and the origins of societal organisation.`') 
    st.markdown('#### `We articulate this discourse with you because, right now, ____________________________?`', unsafe_allow_html=True)
    # st.markdown("### <center>nous organisons : </center>", unsafe_allow_html=True)
    st.markdown("# <center>Panel Discussion</center>", unsafe_allow_html=True)
    st.markdown("### <center>Europe in Discourse, 25-28 September 2024, `Athens`</center>", unsafe_allow_html=True)
    st.markdown("#### Called by: Gabrielle Dyson, Andrés León Baldelli, Graziano Mazza", unsafe_allow_html=True)
    st.divider()
    random.shuffle(keywords)
    concatenated_keywords = " • ".join([f"**{keyword}**" for keyword in keywords])
    st.markdown(f"### <center> Keywords: {concatenated_keywords}  </center>", unsafe_allow_html=True)


    st.divider()
    st.markdown("## Overview")    
    st.markdown("""#### The "Social Contract from Scratch" is a panel discussion at the Europe in Discourse 2024 conference, seeking to explore and redefine the fundamental principles of societal cooperation and governance in an era marked by simultaneous and interconnected 'polycrises'. These crises encompass systemic inequality, environmental degradation, resource scarcity, and geopolitical tensions, all of which challenge the effectiveness of traditional multilateral frameworks.
    """)
    st.markdown("## Interdisciplinary Approach")    
    st.markdown("""#### Our panel integrates insights from social sciences, natural sciences, philosophy, and the arts to construct a holistic perspective on addressing contemporary uncertainties and risks. By bridging diverse viewpoints, we foster a comprehensive dialogue that goes beyond disciplinary boundaries.
    """)
    
    st.markdown("## Digital Platform")    

    st.markdown("""#### A core feature of our initiative is the deployment of an interactive digital platform designed to facilitate discussion and connect theoretical insights with actionable strategies. This versatile coordination tool encourages inclusive participation, allowing all voices to be equally heard and contributing to the construction of new narratives based on collective understanding.
    """)
    """_🎊 Presentation document_
    
    🧾 Discover more about our workshop discussions, download the latest presentation. 
    """
    
    download_pdf()
    

    # Load the content from the one_pager.md file
    # markdown_content = load_markdown('data/one_pager.md')

    # Display the content using markdown
    # st.markdown(markdown_content)

    st.write("\n\n**Let's work together to bring this vision to life!**")

    # tab1, 
    tab2, tab3, tab4, tab5, tab6 = st.tabs([
    # "Overview", 
    "Committee", 
    "Contributions", 
    "Minimal Necessities", 
    "Frequently Asked Questions", 
    "Seldom Asked Questions"]
    )
    

    with tab2:
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
            "Maurice Rossi, Institut ∂'Alembert, Paris",
            "Flaviana Iurlano, DIMA, Genova",
            "Giuliano Lazzaroni, Dipartimento di Matematica e Informatica, Firenze",
            "Pierluigi Cesana, Fukuoka University, Kyushu-Japan",
            "Masato Kimura, Institute of Science and Engineering, Kanazawa-Japan",
            "Garth Wells, Department of Engineering, Cambridge",
            "Jorgen Dokken, Simula, Oslo",
            "Sebastien Neukirch, Institut ∂'Alembert, Paris",
            "Patrick Farrell, Mathematical Institute, ",
            "Lev Truskinovsky, ESPCI, Paris",
            "Gui-Qiang Chen, Mathematical Institute, Oxford",
        ]

    with tab3:
        display_dictionary(panel_contributions())


if __name__ == "__main__":
    main()